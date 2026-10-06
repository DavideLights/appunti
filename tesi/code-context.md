# BlueAgent v2: Architectural Context & Implementation Reference

## 1. System Philosophy & Paradigms

1. **Hybrid Network Split:**
   - **Production (Live Kernel):** WireGuard (`wg-k`, `10.k.0.0/24`) terminated into unmanaged Linux Bridge (`br-team-k`, gateway `10.k.1.1/24`). Containers run on `eth0` with static IPs (`10.k.1.x`). Maximum I/O, zero SDN overhead, native `tcpdump` sniffing.
   - **Verification (Dark Sandbox):** Ephemeral Incus OVN overlay network (`verify-ovn-<uuid>`, parent `incusbr0`). Clones rebound to OVN switch without host routing table conflicts.
2. **Topological Fidelity:**
   - Instances maintain single `eth0`, identical IP (`10.k.1.x`), and gateway (`10.k.1.1`) across live and sandbox. Application code is unaware of sandboxing.
   - Static IP injected via `systemd-networkd` (`/etc/systemd/network/10-eth0.network`) pre-baked into rootfs; preserved across CoW snapshots without cloud-init.
3. **Sub-Second Copy-on-Write (CoW) Duplication:**
   - Incus instances reside on ZFS/Btrfs storage pools. Cloned via block-level snapshots (`POST /1.0/instances` copy) in ~100 ms.
4. **Dual-Mode Verification:**
   - *In-Container (Agentless):* Executed inside target clone via `incus exec` (`check.target == "container"`).
   - *Ephemeral Verifier Runner:* Ephemeral container (`verify-runner-<uuid>`, `check.target == "verifier"`) attached directly to OVN switch for black-box network checks.
5. **Two-Tier Synchronization (Anti-HTTP 409):**
   - Intra-process coroutine lock (`asyncio.Lock`) + inter-process OS lock (`filelock.AsyncFileLock` on `/tmp/blueagent_locks/<name>.lock`) with task-level reentrancy.
6. **Self-Healing State Reconciliation:**
   - Background daemon sweeps orphan `verify-*` containers and OVN networks. Enforces 90s grace period to prevent race conditions on newly created networks.
7. **Traffic Engineering:**
   - Cryptokey Routing: Peer WireGuard `AllowedIPs = 10.k.0.x/32` tied to public key.
   - MSS Clamping: Enforced in `nftables` before accept rules to prevent PMTU blackhole packet drops (WireGuard MTU: `1420`, Geneve: `1442`).

---

## 2. Directory Layout & Module Responsibilities

```
src/blueagent/
├── config.py              # Pydantic BaseSettings (env prefix: BLUEAGENT_)
├── models.py              # Pydantic v2 domain schemas, IaC definitions, API models
├── database.py            # SQLite async database manager (aiosqlite)
├── locks.py               # TwoTierLock & LockRegistry (process & file locks)
├── dependencies.py        # FastAPI dependency injection providers
├── main.py                # FastAPI entrypoint, lifespan startup/shutdown
├── engine/
│   ├── base.py            # ContainerEngine ABC & ExecResult
│   ├── incus.py           # Concrete IncusEngine (UDS client /var/lib/incus/unix.socket)
│   └── network.py         # Incus OVN/bridge device helpers
├── network/
│   ├── addressing.py      # Pure IP plan generator (plan_for, allocate_member_ip)
│   ├── host_net.py        # HostNetworkManager (Linux bridges, routing, nftables)
│   ├── wireguard.py       # WireGuardManager (wg-k interface, peer allocation, keys)
│   └── _runner.py         # Async subprocess execution wrapper
├── verifier/
│   └── ovn.py             # OVNVerifier async context manager (RAII verification)
├── lifecycle/
│   └── manager.py         # LifecycleManager (reconciliation loop, 90s grace period)
└── api/
    ├── teams.py           # /teams endpoints (create, list, get, delete, wg members)
    ├── challenges.py      # /challenges endpoints (deploy, verify)
    └── health.py          # /health & liveness probe
```

---

## 3. Core Classes, Methods & Type Contracts

### Configuration (`config.py`)
- `Settings`: Exposes `incus_socket_path`, `incus_uplink_network` (`incusbr0`), `database_path`, `lock_directory`, `resource_grace_period_seconds` (90), `wg_base_port` (51820), `wg_mtu` (1420), `nft_table` (`blueagent`).

### Domain Models (`models.py`)
- `ExecResult`: `exit_code: int`, `stdout: str`, `stderr: str`.
- `CommandSpec`: `target: Literal["container", "verifier"]`, `container_name: Optional[str]`, `cmd: List[str]`, `env: Dict[str, str]`, `timeout: int`.
- `ContainerSpec`: `name: str`, `image: str`, `ip_suffix: int` (2-254), `limits_cpu: str`, `limits_memory: str`.
- `VerifierSpec`: `image: str`, `ip_suffix: int = 250`, `limits_cpu: str`, `limits_memory: str`.
- `ChallengeConfig`: `challenge_id: str`, `team_k: int`, `verify_internet_access: bool`, `verifier: Optional[VerifierSpec]`, `containers: List[ContainerSpec]`, `readiness_commands: List[CommandSpec]`, `verify_commands: List[CommandSpec]`.
- `VerifyResultResp`: `success: bool`, `passed: bool`, `message: str`, `details: Optional[Dict[str, Any]]`.
- `TeamRecord`, `TeamMemberWG`, `ActiveChallengeRecord`: Database models.

### Container Engine Interface (`engine/base.py` & `engine/incus.py`)
- `ContainerEngine(ABC)`:
  - `create_instance(spec: ContainerSpec) -> str`
  - `start_instance(name: str) -> None`
  - `stop_instance(name: str, force: bool = False) -> None`
  - `delete_instance(name: str) -> None`
  - `clone_instance(source: str, target: str) -> str` (CoW `instance_only=True`)
  - `connect_network(instance: str, network: str, ip: Optional[str] = None) -> None` (`PATCH /instances/{name}` device override)
  - `disconnect_network(instance: str, network: str) -> None`
  - `exec_command(name: str, cmd: List[str], env: Optional[Dict], timeout: int) -> ExecResult`
  - `get_instance_status(name: str) -> str`
- `IncusEngine`: Implements `ContainerEngine` over `/var/lib/incus/unix.socket` using `httpx.AsyncClient` with `/operations/{uuid}/wait` long-polling.

### Network Subsystem (`network/`)
- `addressing.plan_for(team_k: int) -> TeamNetPlan`:
  - Supports `0 <= team_k <= 254` (e.g., team 0 -> `10.0.0.0/24`, `br-team-0` on `10.0.1.1/24`, `wg-0` on `51820`).
  - Returns `bridge_name` (`br-team-k`), `bridge_ip` (`10.k.1.1`), `bridge_cidr` (`10.k.1.1/24`), `lan_subnet` (`10.k.1.0/24`), `wg_iface` (`wg-k`), `wg_server_ip` (`10.k.0.1`), `vpn_subnet` (`10.k.0.0/24`), `listen_port` (`51820 + team_k`).
- `addressing.allocate_member_ip(team_k: int, used_ips: Iterable[str]) -> str`:
  - Scans host range `.2` to `.254` on `10.k.0.0/24` with automatic hole-filling (cap: 253 members).
- `HostNetworkManager`:
  - `setup_team_bridge(team_k: int, gateway_ip: Optional[str]) -> str`: Creates bridge, sets IP, enables link, updates nftables `@team_links`.
  - `teardown_team_bridge(team_k: int) -> None`: Deletes bridge interface and removes nftables pairing.
  - `setup_nftables() -> None`: Initializes base tables, MSS clamping on forward, and NAT masquerade.
- `WireGuardManager`:
  - `setup_team_interface(team_k: int, private_key: Optional[str]) -> Tuple[str, str]`: Generates keys, creates `wg-k`, sets address `10.k.0.1/24`, binds port.
  - `add_member_peer(team_k: int, member_name: str, client_pubkey: Optional[str]) -> TeamMemberWG`: Allocates client IP, binds `/32` AllowedIP, writes client config.
  - `generate_member_config(team_k: int, client_ip: str, client_pubkey: str, preshared_key: Optional[str], private_key: Optional[str]) -> str`: Renders WireGuard `.conf`, supports re-rendering with stored private key.
  - `remove_member_peer(team_k: int, public_key: str) -> None`
  - `teardown_team_interface(team_k: int) -> None`
- `SubprocessRunner`:
  - Solved Linux pipe re-opening `ENXIO` (`/dev/stdin`) by routing `stdin` through anonymous `tempfile.TemporaryFile()` descriptors.

### Authentication & Dependencies (`dependencies.py` & `config.py`)
- `require_ctfd_token`: Validates incoming requests against `config.ctfd_api_token` via `Authorization: Bearer <token>` or `X-CTFd-Token` header.
- `get_host_net`, `get_wg`: Injected via FastAPI application state initialized in `lifespan`.

### Concurrency & Locks (`locks.py`)
- `TwoTierLock(lock_path, resource_name, timeout)`: Combines in-process `asyncio.Lock` with OS `AsyncFileLock`. Tracks task reentrancy.
- `LockRegistry`:
  - `lock_team(team_k: int) -> AsyncIterator[TwoTierLock]`
  - `lock_instance(instance_name: str) -> AsyncIterator[TwoTierLock]`

### Team API & Multi-Member WireGuard (`api/teams.py`)
- `POST /teams`: Idempotent team bridge + WireGuard setup. Maps `ctfd_team_id` to `team_k` (range 0–254).
- `GET /teams`, `GET /teams/{team_k}`, `DELETE /teams/{team_k}`: Team listing, retrieval, and teardown. Completely blows away `wg-k` and `br-team-k` kernel interfaces and drops nftables pairings.
- `POST /teams/{team_k}/members`: Idempotent WireGuard peer setup. Supports lazy team creation, Curve25519 key generation, PSK, IP allocation (.2-.254 with hole-filling, cap 253), and re-click config return.
- `GET /teams/{team_k}/members`: Lists registered peers with secrets masked.
- `GET /teams/{team_k}/members/{member_id}` & `/config`: Fetches member details or raw `.conf` WireGuard text.
- `DELETE /teams/{team_k}/members/{member_id}`: Removes peer from WireGuard and frees allocated IP.
- `GET /teams/{team_k}/peers`: Telemetry correlating SQLite members with active `wg show dump` stats.

### Verification Orchestration (`verifier/ovn.py`)
- `OVNVerifier(engine, config, session_id)`:
  - Incus OVN network name cap: 11 characters (`verify-{session_id[:4]}`).
  - Isolated dark L2 switch created with `ipv4.address: "none"` (omits uplink `network` parameter) to completely prevent host routing conflicts with live `br-team-k` (`10.k.1.1/24`).
  - Container NIC `eth0` bound to `verify-{session_id[:4]}` without `ipv4.address` property (avoids Incus 500 error when DHCP disabled). Static IP configured inside container namespace.
  - `__aenter__()`:
    1. Provisions dark OVN L2 network `verify-{session_id[:4]}`.
    2. CoW clones challenge containers, patches NIC `eth0` to dark network, boots clones, assigns IP inside container.
    3. If `config.verifier` defined, provisions ephemeral verifier runner on dark network.
  - `run_checks() -> VerifyResultResp`:
    - Dispatches commands to target clone or verifier runner; evaluates exit codes.
    - Catches Incus operation timeout (`context deadline exceeded` / `timed out`) and returns `VerifyResultResp(success=False, passed=False, message="Command timed out...")`.
  - `__aexit__()`:
    - Strict reverse LIFO cleanup: stops/deletes verifier runner $\rightarrow$ stops/deletes clones $\rightarrow$ deletes OVN network.

### Lifecycle Daemon (`lifecycle/manager.py`)
- `LifecycleManager(engine, host_net, db, config)`:
  - Runs periodic background task (`reconcile_once`).
  - Queries active containers matching `verify-*` and OVN networks.
  - Evaluates creation timestamp against `resource_grace_period_seconds` (default: 90s). Prunes expired/orphaned resources.

---

## 4. Current Implementation Status & Roadmap

| Component | Status | Location | Notes |
| :--- | :--- | :--- | :--- |
| **Settings & Config** | Complete | `src/blueagent/config.py` | Full 12-factor env management + CTFd token |
| **Pydantic v2 Models** | Complete | `src/blueagent/models.py` | Full schema validation + CTFd & PeerStats (team_k 0-254) |
| **Database Manager** | Complete | `src/blueagent/database.py` | Async SQLite with CTFd mappings & IP hole filling |
| **Two-Tier Locks** | Complete | `src/blueagent/locks.py` | In-process + flock with task reentrancy |
| **Addressing Planner** | Complete (Tested) | `src/blueagent/network/addressing.py` | Deterministic IP mapping for 255 teams (0–254) |
| **Host Bridge & nftables**| Complete (Tested) | `src/blueagent/network/host_net.py` | Linux bridge + MSS clamping + sysctl |
| **WireGuard Manager** | Complete (Tested) | `src/blueagent/network/wireguard.py` | Interface, peers, keys & member configs (with re-render) |
| **Subprocess Runner** | Complete (Tested) | `src/blueagent/network/_runner.py` | Async executor, tempfile stdin descriptor fix for ENXIO |
| **Incus Engine** | Complete (Tested) | `src/blueagent/engine/incus.py` | UDS async client, dark OVN support, operation polling |
| **Lifecycle Manager** | Complete (Tested) | `src/blueagent/lifecycle/manager.py` | 90s grace period orphan cleaner |
| **Team API Routes** | Complete (Verified) | `src/blueagent/api/teams.py` | Verified live: team create, members, configs, peers, destroy |
| **Challenge API Routes** | Complete (Verified) | `src/blueagent/api/challenges.py` | Deploy, list, get, teardown, and verify endpoints |
| **OVNVerifier Logic** | Complete (Verified) | `src/blueagent/verifier/ovn.py` | CoW cloning, dark OVN L2 switch, in-container & verifier checks, timeouts |
| **Health API Route** | Complete | `src/blueagent/api/health.py` | Liveness & ready checks |

### Live Integration Verification Completed:
1. **Team & Network Lifecycle (`tests/usability/test_1_team_and_network.py`):**
   - Verified team bridge and WireGuard creation, member IP allocation, config generation, and complete kernel cleanup.
2. **Image Creation & Pipeline (`tests/usability/test_2_image_creation.py`):**
   - Verified Distrobuilder tarball upload, unpack, build, import into Incus image store, and duplicate submission idempotency.
3. **Challenge Deployment & Multi-Container Topology (`tests/usability/test_3_challenge_and_instance.py`):**
   - Verified deployment of multi-container challenge topologies, static IP binding to `br-team-k`, readiness commands, and container rollback on failure.
4. **Dataplane Usability (`tests/usability/test_4_dataplane_usability.py`):**
   - Verified end-to-end VPN client connectivity to container web services through Linux bridge.
5. **Edge Cases & Cascades (`tests/usability/test_5_edge_cases.py`):**
   - Verified deletion conflict on in-use images, cascading team teardown container destruction, and invalid reference rejection.
6. **OVN Verifier Usability (`tests/usability/test_6_verifier.py`):**
   - Verified successful checks (both in-container and verifier runner probe), command failure propagation, command timeout handling, and rejection of concurrent verifications with HTTP 409 Conflict.

### Test Suite Execution Summary:
- **Unit & Mock Tests (`tests/test_*.py`):** 99 passed in 16s.
- **Usability Integration Tests (`tests/usability/`):** 18 passed in 94s.
