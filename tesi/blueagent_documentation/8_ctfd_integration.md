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
