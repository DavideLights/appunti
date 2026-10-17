# Walkthrough: Empirical Benchmark Suite with 100ms CPU/RAM Telemetry & Synchronized Verification

All objectives have been successfully implemented, executed, and documented.

---

## 1. What Was Implemented

### 1.1 Dedicated 100ms CPU & RAM Subprocess Sampler ([`resource_sampler.py`](file:///home/davidel/.gemini/antigravity/brain/335ea41a-df46-4ffa-bb4c-eefc5a5248cd/scratch/resource_sampler.py))
- Reads `/proc/stat` to calculate exact CPU utilization (total %, user %, system %, and iowait %).
- Reads `/proc/meminfo` and `/proc/spl/kstat/zfs/arcstats` to isolate **net container RAM** (`ram_used_mb - zfs_arc_mb`), preventing ZFS Adaptive Replacement Cache growth from skewing container memory measurements.
- Synchronously tags every barrier lifecycle step with duration, CPU statistics ($avg, p95, max, iowait$), and RAM deltas.

### 1.2 Synchronized 6-Barrier Lifecycle
- **[services/challenges.py](file:///home/debian/bluectfd/blueagent/src/blueagent/services/challenges.py):** Added `skip_cleanup: bool = False` to `verify_challenge()` and created `cleanup_verify_sandbox()` to stop/delete ephemeral clones and OVN switches on demand.
- **[api/challenges.py](file:///home/debian/bluectfd/blueagent/src/blueagent/api/challenges.py):** Added `POST /teams/{team_k}/verificator?skip_cleanup=true` and `DELETE /teams/{team_k}/verificator`.
- **[ovn.py](file:///home/debian/bluectfd/blueagent/src/blueagent/verifier/ovn.py):** Statically bound IPv4 addresses directly during network attachment to eliminate OVN dynamic allocation pool contention under burst concurrency.
- **[client.py](file:///home/debian/bluectfd/blueagent/tests/usability/client.py):** Added client methods for `verify_challenge(skip_cleanup=True)` and `cleanup_verify()`.

### 1.3 "Heavy" CTF Challenge Image (`ubuntu-heavy`)
- Built from Ubuntu 24.04 (`ubuntu/noble`) with `systemd`, `nginx`, `postgresql-16`, `sqlite3`, and `python3` (544.18 MiB compressed, ~1.5 GB uncompressed).
- Published to Incus storage as alias `ubuntu-heavy` and registered in `blueagent.db`.

---

## 2. Experimental Verification Results

The full 9-scenario evaluation matrix (Test 1 Baseline 10 cycles + 8 scaling scenarios up to 50 live / **100 peak concurrent containers**) was executed with **100% pass rate** for both container types:

### 2.1 Core Thesis Metric: ZFS CoW Speedup Factor
Because ZFS cloning references existing block trees ($O(1)$ metadata pointers), cloning scales with kernel metadata operations rather than storage I/O bandwidth:

| Scenario ($M \times N$) | Peak Cts | Alpine Deploy Create (s) | Alpine CoW Clone (s) | **Alpine Speedup** | Ubuntu Deploy Create (s) | Ubuntu CoW Clone (s) | **Ubuntu Speedup** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$M=1, N=1$** | 2 | 0.99s | 0.75s | **$1.32\times$** | 1.23s | 0.92s | **$1.33\times$** |
| **$M=2, N=5$** | 20 | 8.16s | 8.65s | **$0.94\times$** | 9.51s | 8.62s | **$1.10\times$** |
| **$M=2, N=7$** | 28 | 13.45s | 10.13s | **$1.33\times$** | 16.50s | 15.33s | **$1.08\times$** |
| **$M=2, N=10$**| 40 | 15.68s | 13.49s | **$1.16\times$** | 19.71s | 21.50s | **$0.92\times$** |
| **$M=5, N=5$** | 50 | 23.57s | 8.44s | **$2.79\times$** | 30.10s | 13.62s | **$2.21\times$** |
| **$M=5, N=7$** | 70 | 32.11s | 14.13s | **$2.27\times$** | 42.82s | 21.75s | **$1.97\times$** |
| **$M=5, N=10$**| 100 | 45.36s | 19.95s | **$2.27\times$** | 63.28s | 34.35s | **$1.84\times$** |
| **$M=10, N=2$**| 40 | 19.32s | 5.26s | **$3.68\times$** | 22.72s | 7.81s | **$2.91\times$** |
| **$M=10, N=5$**| 100 | 50.61s | 14.06s | **$3.60\times$** | 76.19s | 22.17s | **$3.44\times$** |

### 2.2 Memory Density & CPU Utilization
| Scenario | Peak Cts | Alpine Deploy CPU (%) | Ubuntu Deploy CPU (%) | Alpine Peak RAM | Ubuntu Peak RAM | Alpine Net RAM Delta | Ubuntu Net RAM Delta |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$M=1, N=1$** | 2 | 11.4% | 10.0% | 3,506 MB | 3,881 MB | **+38 MB** | **+98 MB** |
| **$M=2, N=5$** | 20 | 13.4% | 16.4% | 3,819 MB | 4,860 MB | **+309 MB** | **+973 MB** |
| **$M=2, N=7$** | 28 | 13.7% | 15.4% | 3,960 MB | 5,309 MB | **+370 MB** | **+1,333 MB** |
| **$M=2, N=10$**| 40 | 16.1% | 20.3% | 4,153 MB | 6,070 MB | **+563 MB** | **+1,976 MB** |
| **$M=5, N=5$** | 50 | 16.5% | 22.0% | 4,375 MB | 6,751 MB | **+729 MB** | **+2,531 MB** |
| **$M=5, N=7$** | 70 | 19.4% | 21.7% | 4,757 MB | 7,973 MB | **+1,028 MB** | **+3,568 MB** |
| **$M=5, N=10$**| 100 | 19.7% | 23.1% | 5,282 MB | 9,145 MB | **+1,445 MB** | **+5,156 MB** |
| **$M=10, N=2$**| 40 | 18.1% | 23.1% | 4,384 MB | 5,686 MB | **+611 MB** | **+1,931 MB** |
| **$M=10, N=5$**| 100 | 17.2% | 20.9% | 5,417 MB | 9,233 MB | **+1,533 MB** | **+5,247 MB** |

- **Density:** Alpine idles at **~15.3 MB/container**, while Ubuntu Heavy idles at **~52.5 MB/container**.
- **Host Capacity:** 100 concurrent Ubuntu service containers fit comfortably in **9.23 GiB** host RAM with 0 swap usage.

---

## 3. Generated Datasets & Thesis Artifacts

All files are preserved on the remote server (`/home/debian/bluectfd/blueagent/tests/`) and mirrored locally in the scratch directory:

- **Thesis Documentation:**
  - Remote: `/home/debian/bluectfd/thesis_notes.md`
  - Local: [thesis_notes.md](file:///home/davidel/.gemini/antigravity/brain/335ea41a-df46-4ffa-bb4c-eefc5a5248cd/thesis_notes.md)
- **Alpine Linux Datasets:**
  - [thesis_alpine_results.csv](file:///home/davidel/.gemini/antigravity/brain/335ea41a-df46-4ffa-bb4c-eefc5a5248cd/scratch/thesis_alpine_results.csv) (Summary rows for master tables)
  - [thesis_alpine_step_resources.csv](file:///home/davidel/.gemini/antigravity/brain/335ea41a-df46-4ffa-bb4c-eefc5a5248cd/scratch/thesis_alpine_step_resources.csv) (108 long-format step resource rows)
  - [thesis_alpine_timeseries.csv](file:///home/davidel/.gemini/antigravity/brain/335ea41a-df46-4ffa-bb4c-eefc5a5248cd/scratch/thesis_alpine_timeseries.csv) (8,634 raw 100ms telemetry samples)
  - [thesis_alpine_report.md](file:///home/davidel/.gemini/antigravity/brain/335ea41a-df46-4ffa-bb4c-eefc5a5248cd/scratch/thesis_alpine_report.md)
- **Ubuntu Heavy Datasets:**
  - [thesis_ubuntu_results.csv](file:///home/davidel/.gemini/antigravity/brain/335ea41a-df46-4ffa-bb4c-eefc5a5248cd/scratch/thesis_ubuntu_results.csv) (Summary rows for master tables)
  - [thesis_ubuntu_step_resources.csv](file:///home/davidel/.gemini/antigravity/brain/335ea41a-df46-4ffa-bb4c-eefc5a5248cd/scratch/thesis_ubuntu_step_resources.csv) (108 long-format step resource rows)
  - [thesis_ubuntu_timeseries.csv](file:///home/davidel/.gemini/antigravity/brain/335ea41a-df46-4ffa-bb4c-eefc5a5248cd/scratch/thesis_ubuntu_timeseries.csv) (10,833 raw 100ms telemetry samples)
  - [thesis_ubuntu_report.md](file:///home/davidel/.gemini/antigravity/brain/335ea41a-df46-4ffa-bb4c-eefc5a5248cd/scratch/thesis_ubuntu_report.md)
