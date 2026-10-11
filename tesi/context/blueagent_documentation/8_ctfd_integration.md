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
- **Payload:** `{"team_k": 0, "name": "Team Alpha"}`
- **Action:** Allocates `10.k.0.0/24` VPN subnet, creates Linux bridge `br-team-k` (`10.k.1.1/24`), sets up WireGuard interface `wg-k` (UDP `51820 + team_k`), applies nftables NAT/MSS rules.
- **Response:** `201 Created` or `200 OK` (idempotent).

### 2.2 Member Join / Config Download (Lazy Provisioning)
- **Endpoint:** `POST /teams/{team_k}/members`
- **Payload:** `{"name": "user1", "ctfd_user_id": 101, "team_name": "Team Alpha"}`
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
- **Action:** Tears down all running challenge containers, deletes `wg-k` interface, deletes `br-team-k` bridge, clears nftables `@team_links` pairings, cascades member deletion in database.
- **Response:** `204 No Content`.

---

## 3. Challenge Lifecycle & Container Management

### 3.1 Container Deployment (`machines`)
- **Endpoint:** `POST /teams/{team_k}/machines`
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
  2. Provisions containers with `eth0` bound to target team bridge `br-team-k`.
  3. Injects static IP configuration (`10.k.1.x/24`, gateway `10.k.1.1`) via `systemd-networkd` and `/etc/network/interfaces`.
  4. Starts containers and applies immediate runtime static routes via `ip addr replace`.
  5. Records containers in SQLite database. Readiness checks are deferred to verification phase.
  6. On failure: executes atomic rollback (deletes created instances and records).
- **Response:** `201 Created` (`DeployResponse`).

### 3.2 Automated Verification (`verificator`)
- **Endpoint:** `POST /teams/{team_k}/verificator`
- **Payload:** `ChallengeConfig` JSON
- **Action:**
  1. Enforces lock: rejects concurrent verifications for the same team (`409 Conflict`).
  2. Initializes `OVNVerifier`:
     - Creates isolated dark OVN L2 switch (`verify-{session_id[:4]}`).
     - Performs CoW block clones of live challenge containers.
     - Binds clone `eth0` to dark OVN switch and sets static IP in container namespace.
     - Optionally spawns ephemeral verifier runner container on dark network.
     - Executes `readiness_commands` in a retry loop until container services are listening.
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

### 3.3 Query Active Running Containers
- **Endpoint:** `GET /teams/{team_k}/machines`
- **Response:** `200 OK` list of `RunningContainerRecord` with container instance names, spec names, IP addresses, image aliases, and timestamps.

### 3.4 Container Teardown
- **Endpoint:** `DELETE /teams/{team_k}/machines`
- **Payload:** Optional `ChallengeConfig` JSON (if omitted or empty, tears down all containers for `team_k`)
- **Action:** Stops and deletes containers associated with the team on `br-team-k`, clears database records.
- **Response:** `204 No Content`.

---

## 4. Container Image Catalog API (`/images`)

BlueAgent requires base images before deploying challenges. Images are built with Distrobuilder.

### 4.1 Image Build Submit
- **Endpoint:** `POST /images`
- **Header:** `Authorization: Bearer <TOKEN>`
- **Body:** Multipart form data:
  - `definition`: Distrobuilder YAML file (`definition.yaml`)
  - `alias`: Unique image name (e.g. `ubuntu-apache`, `alpine-distro`, `thesis-img-1`)
- **Workflow:**
  1. Computes SHA-256 hash of YAML definition.
  2. Claims image in database (`status: building`).
  3. Starts background job: Distrobuilder executes `build-incus --type=unified`.
  4. Imports output tarball into Incus storage pool.
  5. Sets Incus alias and updates database (`status: ready`).
- **Response:**
  - `202 Accepted`: Build started in background.
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

### 4.3 Delete Image
- **Endpoint:** `DELETE /images/{alias}`
- **Action:** Deletes alias, removes image from Incus pool and database.
- **Guard:** Rejects with `409 Conflict` if containers currently reference the image!

---

## 5. CTFd Master Orchestration Guide

CTFd coordinates the competition while BlueAgent executes container and networking tasks:

### 5.1 Team Management Flow
1. **Team Register:**
   - CTFd sends `POST /teams` with `team_k` and `name`.
   - BlueAgent creates kernel bridge `br-team-k` (`10.k.1.1/24`), WireGuard interface `wg-k` (UDP port `51820 + k`), and nftables NAT + MSS clamp.
2. **Player Join / Get VPN:**
   - Player clicks "Download VPN" button in CTFd UI.
   - CTFd sends `POST /teams/{team_k}/members` with `ctfd_user_id` and `name`.
   - BlueAgent allocates VPN IP `10.k.0.x/24` (hole-filling .2 to .254), generates Curve25519 keys, registers peer in `wg-k`.
   - Returns `.conf` text. Player connects to VPN and reaches containers directly on `10.k.1.x`.
   - Repeated requests return the existing configuration without re-allocating IPs.
3. **Telemetry & Activity Check:**
   - CTFd polls `GET /teams/{team_k}/peers`.
   - Inspects bytes rx/tx, last handshake timestamp, and online status.
4. **Team Teardown:**
   - CTFd sends `DELETE /teams/{team_k}`.
   - BlueAgent tears down containers, `br-team-k`, `wg-k`, nftables rules, and database records.

### 5.2 Challenge Deployment Flow
1. **Image Pre-Flight Check:**
   - CTFd checks `GET /images/{image_alias}`. If not ready, calls `POST /images` and waits for `status: ready`.
2. **Deploy Challenge Containers:**
   - CTFd sends `POST /teams/{team_k}/machines` with `ChallengeConfig`.
   - BlueAgent creates Incus containers on `br-team-k`, injects static network configs (`systemd-networkd` + `/etc/network/interfaces`), starts containers, and runs immediate `ip addr replace`.
   - Result: Containers live on team LAN `10.k.1.x`.
3. **Challenge Teardown:**
   - CTFd sends `DELETE /teams/{team_k}/machines`.
   - BlueAgent stops and deletes containers and clears database records.

### 5.3 Automated Verification & Scoring Flow
1. **Trigger Verify:**
   - Player submits flag or requests service check.
   - CTFd sends `POST /teams/{team_k}/verificator`.
2. **ZFS CoW Dark Sandbox Execution:**
   - BlueAgent acquires team lock (returns `409 Conflict` if verification is already in progress).
   - Creates dark OVN L2 switch `verify-{session_id}` (`ipv4.address: none`).
   - Clones containers via ZFS block snapshot (<100ms).
   - Rebinds clone `eth0` to dark OVN switch and starts clones.
   - Runs `readiness_commands` until services are listening.
   - Runs `verify_commands` against clones or via ephemeral verifier runner.
   - LIFO cleanup: stops/deletes verifier container, stops/deletes clones, deletes OVN switch.
   - Production containers remain untouched throughout verification.
3. **Process Result:**
   - `passed == true`: Award score / flag valid.
   - `passed == false`: Report broken service / cheat detected.
