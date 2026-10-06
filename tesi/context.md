# BlueAgent / BlueCTFd: Reference Knowledge Base

## 1. System Identity & Core Paradigm
- **System**: BlueCTFd (CTFd plugin) + BlueAgent (FastAPI async daemon on Debian 13).
- **Target**: Stateful Defense & Patch Management CTFs (multi-tier system containers with `systemd`).
- **Production Path**: WireGuard (`wg-k`, `10.k.0.0/24`) $\rightarrow$ unmanaged Linux Bridge (`br-team-k`, `10.k.1.1/24`) $\rightarrow$ container `eth0` (`10.k.1.x`). Native I/O, zero SDN overhead, native `tcpdump` sniffing.
- **Verification Path**: Ephemeral Incus OVN dark L2 switch (`verify-xxxx`, `ipv4.address: none`) $\rightarrow$ ZFS CoW clones $\rightarrow$ optional verifier runner (`verify-runner-xxxx`). Zero host route clash, zero side-channel leaks, zero live crash risk.
- **Topological Fidelity**: Instances retain single `eth0`, static IP (`10.k.1.x`), and gateway (`10.k.1.1`) identically across live and sandbox. Static IP injected in rootfs via `systemd-networkd` (`/etc/systemd/network/10-eth0.network`).
- **Cloning Speed**: Block-level ZFS snapshots (`POST /1.0/instances` copy, `instance_only=True`) in ~100 ms (~500 ms total verification setup).

---

## 2. Network Plan & Addressing
- **Scope**: $0 \le k \le 254$ (Hard limit: 254 teams due to `10.k.x.x/16` partitioning).
- **VPN Domain (`wg-k`)**:
  - Subnet: `10.k.0.0/24`, Gateway: `10.k.0.1/24`, Port: `51820 + k`.
  - Members: `10.k.0.2` – `10.k.0.254` (cap 253 members, dynamic hole-filling).
  - Cryptokey Routing: Peer `AllowedIPs = 10.k.0.x/32` bound to client public key.
- **LAN Domain (`br-team-k`)**:
  - Subnet: `10.k.1.0/24`, Gateway: `10.k.1.1/24`.
  - Target Containers: `10.k.1.2` (Web), `10.k.1.3` (DB), up to `10.k.1.249`.
  - Ephemeral Verifier Runner: `10.k.1.250`.
- **Traffic Rules (`nftables`, table `inet blueagent`)**:
  - Forward priority filter: MSS clamping before accept (`tcp flags syn / syn,rst tcp option maxseg size set rt mtu`).
  - Isolation: Forwarding allowed only within pair `@team_links` (`(wg-k, br-team-k)`). Cross-team traffic dropped.
  - Postrouting priority srcnat: Masquerade `10.0.0.0/8` exiting non-private interfaces.
- **MTU & Encapsulation Headers**:
  - WireGuard MTU: `1420` (60–80 byte header).
  - OVN Geneve MTU: `1442` (host MTU - 58 bytes, UDP port 6081).

---

## 3. Comparison with State of the Art (Thesis Cap. 1)

| Platform | Technology | Workload | Latency | Verification Method | Fatal Limitation for Patch CTF |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **kCTF** | GKE + nsjail | Stateless OCI | ~10 ms | TCP disconnect / flag output | Read-only rootfs; RAM wiped on disconnect; no systemd / multi-container DB. |
| **CTFBox** | Incus + Docker | System container / VM | 1–5 s | Periodic tick on live service | Live checks cause SLA penalty / crash; leaks exploit payloads to competitors. |
| **CyTrONE** | OpenStack VMs | Full VMs | 5–15 min | Static YAML / live check | Massive VM RAM/CPU footprint; slow setup; requires external LMS (Moodle). |
| **KYPO** | OpenStack Cloud | Full VMs | Minutes | SSH daemon polling | Requires heavy cloud cluster (16 cores, 128 GB RAM); heavy per-team cost. |
| **CyberPatriot** | Desktop VMs | Desktop OS | Offline | Local CSS daemon vs specs | Closed-source; local config diff only; cannot test dynamic network exploits. |
| **DARPA CGC** | DECREE / QEMU | Custom 32-bit binaries | Variable | Formal PoV + pollers | Synthetic binaries; non-standard OS; no standard Linux network stack. |
| **BlueAgent** | Incus + OVN + ZFS | Stateful system containers | **~500 ms** | **CoW Clone + Dark OVN Switch** | Low RAM (~200MB/team); zero live interference; zero side-channel leaks. |

### Verification Taxonomy
1. **Static Analysis (SAST / Diff)**: Storage scan without execution. Fails to verify runtime functional correctness.
2. **Dynamic Live Attacker**: Exploit sent to live `br-team-k`. Risks crashing live service; payload sniffable via `tcpdump`.
3. **Command Injection Live (`incus exec`)**: Direct command execution. Leaks via `pspy` / `/proc`; risks file conflicts.
4. **Dark Sandbox Cloning (BlueAgent)**: Block CoW clone into isolated dark OVN switch. Full execution, zero leak, zero live risk.

---

## 4. Alternative Architectures & Trade-Offs (Thesis Cap. 3)

| Design | Topology | Pro | Con / Fatal Flaw |
| :--- | :--- | :--- | :--- |
| **3.1 Shadow Bridge (No GW)** | Unmanaged L2 bridge without IP | Simple, pure kernel | **No WAN**: `apt`, DNS, external webhooks fail inside sandbox. |
| **3.2 Dual NIC (`eth0` + `wan1`)** | `eth0` on shadow bridge, `wan1` on `incusbr0` | Restores WAN egress | **Breaks fidelity**: asymmetric routing inside container; dual veth overhead. |
| **3.3 PID Namespace Split** | Exec in child PID netns in live container | No cloning needed | **Leaky**: visible via `/proc` timing / eBPF; crashes corrupt live state. |
| **3.4 Kernel `netns` Split** | Separate host netns per verification | Pure kernel, no OVN | **Complex routing**: managing dynamic netns veth routing tables drifts; no cluster support. |
| **3.5 In-Memory `/proc` Masking** | `memfd_create` + `libprocesshider` | Conceals process | **Obscurity**: bypassed by Go/Rust, static binaries, direct `sys_getdents64`. |
| **BlueAgent Hybrid** | Live Linux bridge + Ephemeral OVN | Sub-second, isolated, WAN | Requires OVS/OVN daemons on host. |

---

## 5. Actors, Use Cases & System Requirements (Thesis Cap. 2)

### Actors
- **Partecipante**: Uses WireGuard (`10.k.0.x`), accesses `10.k.1.x`, patches code, requests verification.
- **Autore Sfida**: Writes `challenge.yaml` (topology, images, cgroup limits, readiness, verification commands).
- **CTFd**: REST client with Bearer token. Provisions teams, generates configs, triggers verifications.
- **LifecycleManager**: Background daemon sweeping orphaned `verify-*` resources older than 90s.

### Use Case Codes
- `UC-P01`: WireGuard connection (`wg-quick up wg-k.conf`).
- `UC-P02`: Live service reconnaissance (`br-team-k`, SSH/HTTP).
- `UC-P03`: Patch application on container rootfs.
- `UC-P04`: Verification result consultation on CTFd scoreboard (`VerifyResultResp`).
- `UC-A01`: Declarative IaC challenge authoring (`ChallengeConfig`).
- `UC-A02`: Cgroups resource allocation (`limits.cpu`, `limits.memory`).
- `UC-A03`: Readiness health check definition (`readiness_commands`).
- `UC-A04`: In-Container white-box check definition (`target: "container"` via `incus exec`).
- `UC-A05`: Black-box exploit check definition (`target: "verifier"` via runner container).
- `UC-O01`: Team provisioning & WireGuard setup (`POST /teams`).
- `UC-O02`: Team inspection (`GET /teams/{k}`).
- `UC-O03`: Challenge deployment (`POST /challenges`).
- `UC-O04`: List active challenges (`GET /challenges`).
- `UC-O05`: Automated verification dispatch (`POST /challenges/{id}/verify?team_k={k}`).
- `UC-O07`: Teardown challenge (`DELETE /challenges/{id}/teams/{k}`).
- `UC-O08`: Teardown team (`DELETE /teams/{k}`).
- `UC-S02`: Orphan cleanup daemon (`reconcile_once`, 90s grace).

### System Requirements Matrix
- `SR-HST-01`: Debian 13, kernel modules (wireguard, nftables), `net.ipv4.ip_forward=1`.
- `SR-HST-02`: ZFS storage pool `blueagent-zfs` for sub-second snapshots.
- `SR-HST-03`: OVS/OVN daemons (`ovs-vswitchd`, `ovsdb-server`, `ovn-northd`, `ovn-controller`) listening on `tcp:127.0.0.1:6641`.
- `SR-HST-04`: Parent bridge `incusbr0` defining `ipv4.ovn.ranges` (`172.16.0.100-172.16.0.199`).
- `SR-ENG-01..05`: `ContainerEngine` ABC, `IncusEngine` over UDS `/var/lib/incus/unix.socket`, long-polling `/operations/{uuid}/wait`, CoW snapshot cloning $\le 100\text{ ms}$, cgroups v2 limits.
- `SR-NET-01..06`: `wg-k` L3, `br-team-k` L2, OVN dark sandbox, topological fidelity, TCP MSS clamping, NAT masquerade.
- `SR-VRF-01..05`: `OVNVerifier` RAII context manager, dynamic `eth0` rebinding, verifier runner container, reverse LIFO teardown, command runner with timeout.
- `SR-CON-01..04`: FastAPI REST, `TwoTierLock` (asyncio + flock), `LifecycleManager` 90s grace period, `GET /health`.
- `SR-MOD-01..03`: Pydantic v2 schemas, `challenge.yaml` parser, deterministic IP planner.

---

## 6. Implementation Architecture & Codebase Contracts

### Module Map (`src/blueagent/`)
- `config.py`: `Settings` (env prefix `BLUEAGENT_`, socket path, DB path, tokens, lock dir).
- `models.py`: `CommandSpec`, `ContainerSpec`, `VerifierSpec`, `ChallengeConfig`, `VerifyResultResp`, `TeamMemberWG`, `PeerStats`.
- `database.py`: Async SQLite (`aiosqlite`) with member IP hole-filling (`allocate_member_ip`).
- `locks.py`: `TwoTierLock` (`asyncio.Lock` + `fcntl.flock` on `/tmp/blueagent_locks/<name>.lock`).
- `engine/base.py` & `engine/incus.py`: `ContainerEngine` ABC and `IncusEngine` (UDS client, `_wait_op` polling).
- `network/addressing.py`: `plan_for(team_k)` and `allocate_member_ip(team_k, used_ips)`.
- `network/host_net.py`: Linux bridge setup/teardown, nftables `inet blueagent` table, `@team_links` set.
- `network/wireguard.py`: Interface creation, Curve25519 keys, PSK, config generation & idempotent re-render.
- `network/_runner.py`: Subprocess execution; fixes pipe `ENXIO` via anonymous `tempfile.TemporaryFile()` descriptors.
- `verifier/ovn.py`: `OVNVerifier` RAII context manager.
- `lifecycle/manager.py`: `LifecycleManager` background task (90s grace period).
- `api/`: `teams.py`, `challenges.py`, `health.py`.

### OVNVerifier Invariants
1. Network Name: `verify-{session_id[:4]}` (strictly $\le 11$ characters due to Incus limit).
2. Isolated L2 Config: `ipv4.address: "none"` (no parent uplink `network` parameter) $\rightarrow$ avoids host route conflict with `br-team-k` (`10.k.1.1/24`).
3. Re-binding: `devices.eth0.network = verify-xxxx` without setting `ipv4.address` on the device $\rightarrow$ avoids Incus 500 DHCP error. IP assigned inside container via `ip addr replace 10.k.1.x/24 dev eth0`.
4. Reverse LIFO Cleanup: Stop/delete verifier container $\rightarrow$ Stop/delete clones $\rightarrow$ Delete OVN network.

---

## 7. Critical Gotchas, Edge Cases & Constraints

1. **UDP Path MTU Blackhole**:
   - WireGuard MTU: `1420`. OVN Geneve MTU: `1442`.
   - nftables MSS clamping (`rt mtu`) **only affects TCP**.
   - Large UDP datagrams (> 1420 bytes) with Don't Fragment (DF) flag set (DNSSEC, custom UDP protocols) are **silently dropped without warning**.
2. **Multi-Worker ASGI Lock**:
   - `LockRegistry` uses in-memory `asyncio.Lock`.
   - If running multi-worker Uvicorn/Gunicorn without `BLUEAGENT_USE_FILE_LOCKS=true`, concurrent requests for the same team trigger Incus `HTTP 409 Conflict`.
   - Multi-node setups require Redis `Redlock`.
3. **Scale Ceiling**:
   - 254 teams max ($0 \le k \le 254$) due to `10.k.x.x` single-byte scheme.
4. **Intra-Bridge Sniffing**:
   - `tcpdump -i br-team-k` sees ingress/egress and host-to-container packets, but container-to-container traffic on the same bridge does not cross the host routing stack.
5. **Incus 11-Character OVN Name Limit**:
   - Session prefix must never exceed 4 hex chars: `verify-{id[:4]}` ($6 + 4 = 10 \le 11$).
6. **Linux Pipe `ENXIO`**:
   - Piping secrets to `wg set ... /dev/stdin` over `asyncio.subprocess.PIPE` fails with `ENXIO`. Resolved via anonymous unlinked `tempfile.TemporaryFile()`.

---

## 8. Theoretical Appendices Summary (Thesis Cap. 4 & 5)
- **4.1 Linux Networking**: `netns` provides separate network stack instances; `veth` pairs act as bi-directional pipes; Linux bridges operate as L2 MAC-learning switches (FDB); Netfilter hooks (`PREROUTING`, `FORWARD`, `POSTROUTING`) process packets in `nftables`; cgroups v2 enforces CPU (`cpu.max`) and memory (`memory.max`) quotas.
- **4.2 VPN & SDN**: WireGuard provides kernel-space crypto routing; Open vSwitch (OVS) runs user space `ovs-vswitchd` and transactional `ovsdb-server` with kernel fast-path datapath; OVN coordinates distributed SDN via Northbound DB, `ovn-northd`, Southbound DB, and `ovn-controller`; Geneve encapsulates L2 packets over UDP port 6081 with a 58-byte overhead.
- **4.3 ZFS**: Uses tree-structured block pointers with Copy-on-Write (never overwrites blocks in-place); `zfs snapshot` freezes block pointers in ~100 ms; `zfs clone` creates writable branches with zero initial storage overhead.
- **5.1 nsjail**: Uses chroot, namespaces, and seccomp-bpf to fork isolated processes per TCP connection; ideal for stateless single-binary tasks; unsuitable for multi-tier persistent system containers due to read-only rootfs and state loss on disconnect.

---

## 9. Thesis Writing Tasks & Gaps to Fill
- [x] **1. Introduzione**: Complete draft covering problem, CTF types, and alternative ranges.
- [x] **2.6 Difesa dell'architettura**: Complete draft covering strong ideas, feasibility, practicality, audience, and architectural critique.
- [x] **3.3 PID namespace separato**: Complete write-up on filesystem/log leaks, pspy detection, live service crash blast radius, and network transparency.
- [x] **3.4 Network namespace separato**: Complete write-up on host routing drift, Incus API bypass, absence of cluster support, and kernel lock contention.
- [x] **3.5 Esecuzione in-memory con mascheramento**: Complete write-up on LD_PRELOAD bypass, kernel eBPF detection, log persistence, and live blast radius.
- [x] **4. & 5. Appendici**: Complete theoretical drafts on Linux networking, WireGuard/OVN, ZFS, and nsjail.
