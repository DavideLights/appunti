# BlueAgent & Thesis Engineering Context

> **AI Engineer System Context & Resource Navigation Index**  
> *Primary Single-Source-of-Truth across Antigravity chat sessions, thesis writeup, and codebase environments.*

---

## 1. System Mission & Architectural Philosophy

This workspace hosts the engineering assets, empirical datasets, and compilation pipeline for the Master's Thesis:  
**"BlueAgent: Multi-Tenant Cyber Range Verification and Isolation with Incus and Open Virtual Network (OVN)"**.

### Core Technical Pillars & Invariants
1. **Client-Agnostic Container Orchestration:**
   - BlueAgent manages container topologies per team on isolated host bridges without coupling to upstream competition state.
   - CTFd acts as the game manager; BlueAgent provides the container and network fabric.
2. **Strict Identity Model (`team_k`):**
   - Teams and namespaces are strictly indexed by integer `team_k` where `0 <= team_k <= 254`.
   - The legacy string `team_id` is deprecated and forbidden in all schemas, APIs, and models.
   - Member identities: composite string `ctfd-{team_k}-{ctfd_user_id}`.
3. **Dual-Plane Hybrid Network Split:**
   - **Production Plane (Live Kernel Bridge):** WireGuard (`wg-k`, `10.k.0.0/24`) terminated into unmanaged Linux bridge (`br-team-k`, gateway `10.k.1.1/24`). Containers run with static IPs (`10.k.1.x`) on `eth0`. Yields bare-metal I/O, zero SDN packet encapsulation overhead, and native `tcpdump` wire visibility.
   - **Verification Plane (Dark Ephemeral OVN Overlay):** Ephemeral Incus OVN overlay network (`verify-<session_id>`, parent `incusbr0`). Clones are rebound to this dark switch with zero host routing collisions.
4. **Topological Fidelity & Invariance:**
   - Containers maintain a single virtual NIC (`eth0`) with identical IP (`10.k.1.x`) and gateway (`10.k.1.1`) across live production and verification sandbox.
   - Network config pre-baked in rootfs: `systemd-networkd` (`/etc/systemd/network/10-eth0.network`) and OpenRC/ifupdown (`/etc/network/interfaces`).
5. **Sub-Second ZFS Copy-on-Write (CoW) Sandboxing:**
   - Incus container instances reside on ZFS storage pool `blueagent-zfs`.
   - Sandboxes clone running instances via block-level snapshot metadata pointers (`incus copy --instance-only`), completing in $O(1)$ time (~100 ms to ~1s) independent of image size (1.5 GB Ubuntu Heavy vs 3 MB Alpine).
6. **Concurrency & Reconciliation:**
   - Two-tier locking: `asyncio.Lock` (coroutine) + `filelock.AsyncFileLock` (`/tmp/blueagent_locks/<name>.lock`).
   - Background reconciler enforces a 90-second grace period to clean up orphan sandboxes without race conditions.

---

## 2. Directory Layout & Resource Navigation Map

```
/home/davidel/
├── obsidian-notes/appunti/tesi/           # Master Thesis Vault & LaTeX Pipeline
│   ├── antigravity/                       # [ACTIVE WORKSPACE] Testing Source & Evaluation Hub
│   │   ├── context.md                     # <-- This resource index & operational guide
│   │   ├── README.md                      # Directory index of testing & benchmark taxonomy
│   │   ├── notes/                         # Evaluation chapter draft, notes, and walkthroughs
│   │   ├── data/                          # Telemetry datasets (raw/, processed/, reports/)
│   │   ├── scripts/                       # Benchmark runners, samplers, and plotting tools
│   │   └── figures/                       # Publication-ready evaluation plots (.pdf & .png)
│   ├── 1._Introduzione/                   # Chapter 1: Introduction, motivation, objectives
│   ├── 2._Contesto_e_Confronto_con_.../  # Chapter 2: State of the Art, CyTrONE comparison
│   ├── 3._BlueAgent/                      # Chapter 3: BlueAgent architectural design
│   ├── 4._Architettura_Rete_Alto_.../     # Chapter 4: Dual-plane network design & WireGuard
│   ├── 5._Architettura_Nel_Dettaglio_.../ # Chapter 5: In-depth architecture & empirical validation
│   ├── 6._Architetture_Rete__.../         # Chapter 6: Alternative network topologies & tradeoffs
│   ├── 7._Appendice/                      # Chapter 7: Appendices, configs, and specifications
│   ├── Bibliography.bib                   # BibTeX references
│   ├── compile.sh                         # Markdown -> LaTeX -> PDF compilation script
│   ├── convert_thesis.py                  # Pandoc & regex processor (Mermaid, math, footnotes)
│   ├── latex/                             # Target LaTeX build tree (template.tex, main.tex)
│   └── main.pdf                           # Compiled thesis PDF output
│
├── blueagent/                             # Local BlueAgent Development Codebase
│   ├── context.md                         # Codebase-specific architecture & component inventory
│   ├── src/blueagent/                     # Core Python package (FastAPI, Incus, OVN, WireGuard)
│   │   ├── api/                           # Thin FastAPI routes (teams, challenges, images, health)
│   │   ├── services/                      # Domain logic (ChallengeService, TeamService, ImageService)
│   │   ├── engine/                        # Incus REST engine over /var/lib/incus/unix.socket
│   │   ├── network/                       # Addressing, host_net (Linux bridge/nftables), wireguard
│   │   ├── verifier/ovn.py                # RAII context manager for dark OVN verification sandboxes
│   │   └── lifecycle/manager.py           # Self-healing reconciler (sweeper daemon)
│   └── tests/                             # Unit, usability, and scaling benchmark tests
│
└── bluectfd/                              # Monorepo containing CTFd + BlueAgent plugins
```

---

## 3. Remote Infrastructure & Execution Environment

All production and heavy benchmark executions target the dedicated benchmark testbed:

| Parameter | Value | Operational Details |
| :--- | :--- | :--- |
| **Primary Host IP** | `192.168.1.107` | Active remote testbed VM (Debian 13) |
| **Alternative/Old IPs**| `10.226.253.215`, `192.168.0.100` | Lab network / historical interfaces |
| **SSH Target** | `debian@192.168.1.107` | Password: `debian` (also authorized via `~/.ssh/id_ed25519`) |
| **SSH Fast Command** | `ssh -o StrictHostKeyChecking=no debian@192.168.1.107` | Key-based or non-interactive SSH access |
| **Hardware Specs** | **AMD Ryzen 7 7700X** (8 cores / 16 threads), **15 GiB RAM**, 2 GiB swap | Kernel 6.12, Incus 6.0, ZFS on Linux (`blueagent-zfs`) |
| **Remote Directory** | `/home/debian/bluectfd/` | Root of remote testbed and service scripts |
| **CTFd Web UI** | `http://192.168.1.107:4000` | Competition management interface |
| **BlueAgent REST** | `http://192.168.1.107:8000` | FastAPI daemon listener |
| **Auth Token** | `BLUEAGENT_CTFD_API_TOKEN=blueagent_secret_token_123` | Shared secret header (`X-API-Key`) |
| **Remote Service Daemon** | `/home/debian/bluectfd/start_services.sh` | Subcommands: `start`, `stop`, `status`, `restart` |

---

## 4. Operational Command Cheatsheet

### 4.1 Compiling the Thesis PDF
Execute from `/home/davidel/obsidian-notes/appunti/tesi`:
```bash
# Full build: Markdown -> LaTeX -> pdflatex (x3) + bibtex
./compile.sh

# On LaTeX compile error, inspect log immediately:
tail -n 40 latex/main.log
```

### 4.2 Querying / Managing Remote Services
```bash
# Check running daemon status on testbed:
ssh debian@192.168.1.107 "bash /home/debian/bluectfd/start_services.sh status"

# Check Incus container status:
ssh debian@192.168.1.107 "incus list"

# Monitor ZFS ARC & container RAM:
ssh debian@192.168.1.107 "free -m && cat /proc/spl/kstat/zfs/arcstats | grep -E '^size'"
```

### 4.3 Synchronizing Cross-Chat Context
```bash
# Run the automated multi-session context updater:
python3 /home/davidel/.gemini/config/skills/update-context/scripts/sync_context.py --workspace /home/davidel/obsidian-notes/appunti/tesi/antigravity
```

---

## 5. Key Empirical Benchmarks Summary (At a Glance)

*Extracted from 9-scenario benchmark matrix (Test 1 Baseline to $M=10, N=5$ at 100 peak containers).*

| Scenario ($M \times N$) | Peak Cts | Alpine Deploy (s) | Alpine Clone (s) | Alpine Speedup | Ubuntu Heavy Deploy (s) | Ubuntu Heavy Clone (s) | Ubuntu Heavy Speedup | Net Host RAM |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$M=1, N=1$** | 2 | 0.99s | 0.75s | **$1.32\times$** | 1.23s | 0.92s | **$1.33\times$** | +98 MB |
| **$M=2, N=5$** | 20 | 8.16s | 8.65s | **$0.94\times$** | 9.51s | 8.62s | **$1.10\times$** | +973 MB |
| **$M=2, N=10$**| 40 | 15.68s | 13.49s | **$1.16\times$** | 19.71s | 21.50s | **$0.92\times$** | +1,976 MB |
| **$M=5, N=5$** | 50 | 23.57s | 8.44s | **$2.79\times$** | 30.10s | 13.62s | **$2.21\times$** | +2,531 MB |
| **$M=5, N=10$**| 100 | 45.36s | 19.95s | **$2.27\times$** | 63.28s | 34.35s | **$1.84\times$** | +5,156 MB |
| **$M=10, N=2$**| 40 | 19.32s | 5.26s | **$3.68\times$** | 22.72s | 7.81s | **$2.91\times$** | +1,931 MB |
| **$M=10, N=5$**| 100 | 50.61s | 14.06s | **$3.60\times$** | 76.19s | 22.17s | **$3.44\times$** | +5,247 MB |

- **ZFS CoW Scaling Advantage:** Under peak concurrency ($M=10, N=5$), cloning running containers is **$3.44\times$ to $3.60\times$ faster** than cold provisioning ($22.2s$ vs $76.2s$).
- **Memory Density:** Alpine containers idle at **~15.3 MB/ct**; full Ubuntu Heavy instances (with systemd, PostgreSQL 16, Nginx, Python) idle at **~52.5 MB/ct**. 100 concurrent Ubuntu instances fit in 9.23 GiB host RAM with 0 swap.

---

<!-- BEGIN CROSS-CHAT SYNC -->
## Cross-Chat Multi-Session Synchronization
*Last Synchronized: 2026-10-17 across project sessions*

### 1. Discovered Infrastructure & Runtime Parameters

| Category | Value | Notes / Origin |
| :--- | :--- | :--- |
| **Target Host / VM IP** | `192.168.1.107` | Active remote testbed VM (Debian 13) |
| **Alternative/Old IPs** | `10.226.253.215`, `192.168.0.100` | Historical testbed / secondary interfaces |
| **SSH Target** | `debian@192.168.1.107` (pass: `debian`) | Key and password authenticated remote execution |
| **Service Ports** | `4000` (CTFd Web), `8000` (BlueAgent REST API) | Active network service listeners |
| **Discovered Auth / Token** | `BLUEAGENT_CTFD_API_TOKEN=blueagent_secret_token_123` | Authentication header `X-API-Key` |
| **Automation Script** | `/home/debian/bluectfd/start_services.sh` | Remote multi-service startup/shutdown script |
| **Local Thesis Root** | `/home/davidel/obsidian-notes/appunti/tesi/` | Obsidian markdown chapters + LaTeX compilation pipeline |
| **Local Code Root** | `/home/davidel/blueagent/` | Core Python package source & tests |

---

### 2. Multi-Chat Session Directory

| Conversation ID | Chat Title | Last Activity | Primary Objective / Request | Status |
| :--- | :--- | :--- | :--- | :--- |
| `f8e7a793` | **AI Engineer Context File Setup** | 2026-10-17 13:21:16 | write a context file that is useful to you to access resources faster... | `Active / Complete` |
| `430a2f9a` | **CTFd and Blueagent Testing Plan** | 2026-10-16 11:32:13 | use ssh to login into debian@10.226.253.215... run ctfd and blueagent | `Testing / Complete` |
| `4e891783` | **Git Project Backup Strategy** | 2026-10-16 11:16:51 | do a backup of the whole project using git, go! | `Backup / Complete` |
| `07ba0c08` | **Cross Chat Context Updater Skill** | 2026-10-16 11:14:59 | create a skill that updates on context.md between all the project chats | `Skill Active` |

---

### 3. Detailed Cross-Chat Activity & Progress Log

#### Session: AI Engineer Context File Setup (`f8e7a793`)
- **Objective:** Design and generate a high-signal AI Engineer context file enabling instantaneous resource lookup, command navigation, and environment awareness across workspaces.
- **Key Actions:** Audited workspace topography, thesis chapter pipeline, benchmark artifacts, and existing `blueagent/context.md` structures. Created comprehensive multi-plane context file.

#### Session: CTFd and Blueagent Testing Plan (`430a2f9a`)
- **Objective:** Validate end-to-end service orchestration and test runner on Debian VM (`10.226.253.215`).
- **Key Actions:** Deployed `start_services.sh`, checked daemon states, verified WireGuard interface creation, and benchmarked container provisioning.

#### Session: Git Project Backup Strategy (`4e891783`)
- **Objective:** Create complete version-controlled git bundles and repository backups.
- **Key Actions:** Created bundle backups in `/home/davidel/git_backups_bluectfd/`.

#### Session: Cross Chat Context Updater Skill (`07ba0c08`)
- **Objective:** Implement the `/update-context` skill to automate SQLite transcript synthesis across sessions.
- **Key Actions:** Created `sync_context.py` and skill definition in `~/.gemini/config/skills/update-context/`.

---

### 4. Consolidated Open Tasks & Multi-Chat Next Steps
- [x] Create comprehensive AI engineer context file for rapid resource navigation.
- [ ] Integrate Chapter 5 empirical benchmark tables and charts from `thesis_evaluation_chapter.md` into `5._Architettura_Nel_Dettaglio_e_Validazione/`.
- [ ] Execute `./compile.sh` to produce final verified thesis PDF with updated benchmark figures.
- [ ] Verify CTFd live competition scoring round timings against ZFS CoW ephemeral sandboxing clone speeds.
<!-- END CROSS-CHAT SYNC -->
