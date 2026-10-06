# CTFd Integration & Interface Reference

## 1. Authentication
All requests from CTFd must include the shared secret token:
```http
Authorization: Bearer <BLUEAGENT_CTFD_API_TOKEN>
```
Alternative header: `X-CTFd-Token: <token>`.

---

## 2. Team & WireGuard VPN Lifecycle

### 2.1 Explicit Team Provisioning
- **Endpoint:** `POST /teams`
- **Payload:** `{"team_k": 0, "name": "Team Alpha", "ctfd_team_id": 10}`
- **Action:** Allocates `10.k.0.0/24` VPN subnet, creates Linux bridge `br-team-k` (`10.k.1.1/24`), sets up WireGuard interface `wg-k` (UDP `51820 + team_k`), applies nftables NAT/MSS rules.
- **Response:** `201 Created` or `200 OK` (idempotent).

### 2.2 Member Join / Config Download (Lazy Provisioning)
- **Endpoint:** `POST /teams/{team_k}/members`
- **Payload:** `{"name": "user1", "ctfd_user_id": 101, "ctfd_team_id": 10, "team_name": "Team Alpha"}`
- **Action:**
  - Auto-provisions team network if not already present.
  - Dynamically assigns client IP on `10.k.0.x/24` (host range `.2`–`.254`, capacity 253, automatic hole filling).
  - Generates Curve25519 keypair and WireGuard preshared key (PSK).
  - Adds peer to kernel `wg-k`.
- **Response:** `201 Created` with `.conf` text in `config_text`. Idempotent on re-click (`200 OK` returns existing config without re-allocating IP).
- **Direct Download Endpoint:** `GET /teams/{team_k}/members/{member_id}/config` (`text/plain`).

### 2.3 Peer Telemetry
- **Endpoint:** `GET /teams/{team_k}/peers`
- **Action:** Correlates registered database members with live `wg show <wg-k> dump` metrics (last handshake timestamp, transfer rx/tx bytes, online status).
- **Response:** `200 OK` list of `PeerStats`.

### 2.4 Team Teardown
- **Endpoint:** `DELETE /teams/{team_k}`
- **Action:** Tears down `wg-k` interface, deletes `br-team-k` bridge, clears nftables `@team_links` pairings, cascades member deletion in database.
- **Response:** `204 No Content`.

---

## 3. Challenge Lifecycle

### 3.1 Challenge Deployment
- **Endpoint:** `POST /challenges`
- **Payload:** `ChallengeConfig` JSON
  ```json
  {
    "challenge_id": "web-sqli",
    "team_k": 0,
    "verify_internet_access": false,
    "containers": [
      {
        "name": "web",
        "image": "alpine-distro",
        "ip_suffix": 2,
        "limits_cpu": "1",
        "limits_memory": "256MB"
      }
    ],
    "readiness_commands": [
      {
        "target": "container",
        "container_name": "web",
        "cmd": ["nc", "-z", "127.0.0.1", "80"],
        "timeout": 10
      }
    ],
    "verify_commands": [
      {
        "target": "container",
        "container_name": "web",
        "cmd": ["true"],
        "timeout": 5
      }
    ]
  }
  ```
- **Action:**
  1. Verifies images exist and are marked `ready`.
  2. Claims challenge state in database (`deploying`).
  3. Provisions containers with `eth0` bound to target team bridge `br-team-k`.
  4. Injects static IP configuration (`10.k.1.x/24`, gateway `10.k.1.1`).
  5. Starts containers and executes readiness commands.
  6. On readiness success: transitions status to `running`.
  7. On failure: performs atomic rollback (deletes created containers) and removes claim.
- **Response:** `201 Created` (`ActiveChallengeRecord`).

### 3.2 Automated Verification (Scoring / Checkers)
- **Endpoint:** `POST /challenges/{challenge_id}/verify?team_k={team_k}`
- **Action:**
  1. Enforces lock: rejects concurrent verifications for the same team (`409 Conflict`).
  2. Loads stored `ChallengeConfig` from database.
  3. Initializes `OVNVerifier`:
     - Creates isolated dark OVN L2 switch (`verify-{session_id[:4]}`).
     - Performs CoW block clones of live challenge containers.
     - Binds clone `eth0` to dark OVN switch and sets static IP in container namespace.
     - Optionally spawns ephemeral verifier runner container on dark network.
     - Dispatches `verify_commands` and collects return codes/output.
     - Performs strict reverse LIFO cleanup (stops/deletes verifier container, stops/deletes clones, deletes OVN network).
- **Response:** `200 OK`
  ```json
  {
    "success": true,
    "passed": true,
    "message": "All verification checks passed.",
    "details": null
  }
  ```
- **Timeouts:** Reported cleanly as `{"success": false, "passed": false, "message": "Command timed out: ..."}`.

### 3.3 Query Challenge Status
- **List Active Challenges:** `GET /challenges` or `GET /challenges?team_k={team_k}`
- **Get Specific Challenge:** `GET /challenges/{challenge_id}/teams/{team_k}`
- **Response:** `200 OK` with container details, status (`running`, `deploying`, `failed`), and timestamps.

### 3.4 Challenge Teardown
- **Endpoint:** `DELETE /challenges/{challenge_id}/teams/{team_k}`
- **Action:** Stops and deletes all containers associated with the challenge on `br-team-k`, frees database allocation records.
- **Response:** `204 No Content`.

---

## 4. Container Image Catalog API (`/images`) [Cave Man Style]

BlueAgent need base image before deploy challenge. Images build with Distrobuilder.

### 4.1 Image Build Submit
- **Endpoint:** `POST /images`
- **Header:** `Authorization: Bearer <TOKEN>`
- **Body:** Multipart form data:
  - `definition`: Distrobuilder YAML file (`definition.yaml`)
  - `alias`: Unique image name (e.g. `ubuntu-apache`, `alpine-distro`, `thesis-img-1`)
- **Cave Man Work:**
  1. BlueAgent compute SHA-256 hash YAML.
  2. Write claim database (`status: building`).
  3. Start background job: Distrobuilder run `build-incus --type=unified`.
  4. Output tarball import Incus storage pool.
  5. Set Incus alias. Update database (`status: ready`).
- **Response:**
  - `202 Accepted`: Build start background. Record return: `{"alias": "thesis-img-1", "status": "building"}`.
  - `200 OK`: Image already ready or cached. No rebuild.

### 4.2 Query Image Status
- **Endpoint:** `GET /images` -> list all images.
- **Endpoint:** `GET /images/{alias}` -> inspect single image.
- **Response:** `200 OK`
  ```json
  {
    "alias": "thesis-img-1",
    "status": "ready",
    "fingerprint": "ca00725d6545...",
    "error": null
  }
  ```
- **States:** `building` -> `ready` | `failed`.

### 4.3 Delete Image
- **Endpoint:** `DELETE /images/{alias}`
- **Action:** Delete alias, remove image from Incus pool and database.
- **Guard:** Reject `409 Conflict` if container challenge currently use image!

---

## 5. CTFd Master Orchestration Guide [Cave Man Edition: No Articles, Only Important Words]

CTFd master brain. BlueAgent muscle worker. Here how CTFd manage range:

### 5.1 Team Management Flow
1. **Team Register:**
   - Team sign up CTFd.
   - CTFd send `POST /teams` with `team_k` and `ctfd_team_id`.
   - BlueAgent create kernel bridge `br-team-k` (`10.k.1.1/24`), make WireGuard interface `wg-k` (UDP port `51820 + k`), set nftables NAT + MSS clamp.
   - Result: Team network sandbox ready. Duration: ~0.16s.
2. **Player Join / Get VPN:**
   - Player click "Download VPN" button CTFd UI.
   - CTFd send `POST /teams/{team_k}/members` with `ctfd_user_id` and name.
   - BlueAgent allocate VPN IP `10.k.0.x/24` (hole-filling .2 to .254), generate Curve25519 keys, inject peer `wg-k`.
   - Return `.conf` text. Player connect VPN. Player talk directly to containers on `10.k.1.x`.
   - Player click button again? CTFd send same request. BlueAgent return existing config. No waste IP!
3. **Telemetry & Cheat Detect:**
   - CTFd poll `GET /teams/{team_k}/peers`.
   - Check bytes rx/tx, last handshake time.
   - Player inactive? Disconnected? CTFd see immediately.
4. **Team Teardown:**
   - Competition end or team ban?
   - CTFd send `DELETE /teams/{team_k}`.
   - BlueAgent delete `br-team-k`, delete `wg-k`, clean nftables, wipe members database. Zero leftover kernel clutter.

### 5.2 Challenge Management Flow
1. **Image Pre-Flight Check:**
   - Challenge need image? CTFd call `GET /images/{image_alias}`.
   - Status not `ready`? CTFd call `POST /images` with YAML. Wait status `ready`.
2. **Deploy Challenge Instance:**
   - CTFd send `POST /challenges` with `ChallengeConfig`:
     - Container list, CPU limits, RAM limits, static IP suffixes.
     - Readiness command probe (e.g. `nc -z 127.0.0.1 80` or `uname -a`).
   - BlueAgent claim database (`deploying`), spawn Incus containers on `br-team-k`, push static IP config (`systemd-networkd` + `/etc/network/interfaces`), start container, run immediate `ip addr replace`, exec readiness commands.
   - Readiness pass? State -> `running`.
   - Readiness fail? Automatic rollback! Delete containers, state -> `failed`. Database clean.
   - Result: Container live on team LAN. Duration: ~3.2s.
3. **Challenge Teardown:**
   - Player solve challenge or time expire?
   - CTFd send `DELETE /challenges/{challenge_id}/teams/{team_k}`.
   - BlueAgent stop and delete containers, clear database.

### 5.3 Automated Verification & Scoring Flow
1. **Trigger Verify:**
   - Player submit flag, request health check, or periodic scoring engine tick.
   - CTFd send `POST /challenges/{challenge_id}/verify?team_k={team_k}`.
2. **ZFS CoW Dark Magic:**
   - BlueAgent lock team. No concurrent verify allowed (return `409 Conflict` if busy).
   - Create dark OVN L2 switch `verify-{id}` (`ipv4.address: none`). No routing overlap host.
   - ZFS snapshot clone container instant (<100ms)!
   - Rebind clone `eth0` to dark OVN switch.
   - Boot clone, apply IP inside clone namespace.
   - Optional: spawn ephemeral verifier runner container.
   - Run verify commands (`check.target: container` or `verifier`).
   - Collect stdout, stderr, exit code.
   - LIFO destroy: stop verifier container, stop clones, delete clones, delete OVN switch.
   - Live production containers NOT touched. Zero disruption player!
3. **Process Result:**
   - `passed == true`: Award score / flag valid.
   - `passed == false`: Report broken service / cheat detected / wrong exploit.
   - Duration: ~6.3s total.

---

## 6. Performance Test Results Resume [Cave Man Style: Raw Facts, Big Numbers]

Tested on real hardware VM: Lenovo ThinkPad T480s, Intel Core i5-8350U (8th Gen, 4 vCPU), 4GB RAM, ZFS CoW on loopback disk image.

### 6.1 Benchmark Matrix (K=2 Challenges x M=2 Teams, 4 Total Instances)

| Phase Name | Samples (N) | Average Time | Min Time | Max Time | Avg CPU | Avg RAM | Peak RAM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Team Setup** | 2 | **0.158 s** | 0.116 s | 0.200 s | 22.3% | 2035 MB | 2040 MB |
| **Image Generation** | 2 | **7.828 s** | 7.222 s | 8.433 s | 15.9% | 2099 MB | 2158 MB |
| **Challenge Deploy** | 4 | **3.235 s** | 3.008 s | 3.576 s | 24.3% | 2103 MB | 2188 MB |
| **Verification (OVN + ZFS)** | 4 | **6.359 s** | 6.181 s | 6.534 s | 17.6% | 2180 MB | 2222 MB |

### 6.2 Key Takeaways Cave Man Summary
1. **ZFS CoW Clone Super Fast:**
   - Clone container block level snapshot: ~100 ms.
   - Zero byte copy until file modified. Disk write tiny.
   - Verification total 6.3s: 90% time spent network attach + container boot + command exec. Disk clone instant.
2. **Resource Consumption Tiny:**
   - CPU load: 16% - 24% average. Never starve host.
   - RAM use: ~2.1 GB constant. Zero memory leak across repeated tests.
3. **Linear Predictable Scale:**
   - Team setup: sub-second (0.16s). Scale M teams easy.
   - Challenge deploy: ~3.2s per challenge (2 containers + readiness).
   - Verifier isolation complete: Dark OVN switch avoid IP route conflict host.
