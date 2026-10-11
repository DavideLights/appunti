# BlueAgent v2 — Network & Subnet Topology Recap

This document outlines the deterministic IP subnet plan, resource allocations, interface mappings, and boundary rules across BlueAgent v2.

---

## 1. Global IP Hierarchy

```
10.0.0.0/8 (Platform Envelope — Masqueraded to WAN via nftables)
 │
 └── 10.k.0.0/16 (Per-Team Address Space, where k ∈ [0, 254])
      ├── 10.k.0.0/24 ── WireGuard L3 VPN Subnet (Remote access & players)
      └── 10.k.1.0/24 ── Production LAN & Container Subnet (Target challenge services)

172.16.0.0/24 (Underlay / Host Uplink Bridge — incusbr0)
 ├── 172.16.0.1       ── Gateway on host bridge incusbr0
 ├── 172.16.0.2-99    ── Incus Host DHCP Range
 └── 172.16.0.100-199 ── Incus OVN Uplink / NAT Range
```

---

## 2. Subnet Allocation Matrix

| Subnet CIDR | Domain / Scope | Gateway / Host Interface | Assigned To | IP Allocation Details |
| :--- | :--- | :--- | :--- | :--- |
| **`10.k.0.0/24`** | **VPN (L3)** | `10.k.0.1`<br>Interface: `wg-k`<br>Port: `51820 + k` | **Team Members / Players** | • `10.k.0.1`: Host WireGuard endpoint gateway<br>• `10.k.0.2` – `10.k.0.254`: Client member configs (`/32` cryptokey routing, dynamic hole-filling)<br>• Capacity: 253 members per team |
| **`10.k.1.0/24`** | **Production LAN (L2)** | `10.k.1.1`<br>Interface: `br-team-k` | **Challenge Target Containers** | • `10.k.1.1`: Host default gateway on bridge `br-team-k`<br>• `10.k.1.2` – `10.k.1.254`: Challenge instances (`c-k-{name}` via `ip_suffix`, e.g. `.2` web, `.3` db) |
| **`10.k.1.0/24`** *(Isolated)* | **Dark Sandbox (OVN L2)** | No host IP<br>(Switch: `verify-k`) | **Ephemeral Verification Clones** | • CoW snapshot clones (`verify-k-{name}`) preserve identical `10.k.1.x` static IPs<br>• Verifier runner (`verify-runner-k`): `10.k.1.250` (or `verifier.ip_suffix`)<br>• Zero host routing conflicts (`ipv4.address: none`) |
| **`172.16.0.0/24`** | **Incus Underlay** | `172.16.0.1`<br>Interface: `incusbr0` | **Incus & OVN External Uplink** | • `172.16.0.2` – `172.16.0.99`: Standard Incus DHCP<br>• `172.16.0.100` – `172.16.0.199`: OVN uplink NAT pool |

---

## 3. Visual Topology Diagram

```
                                          +----------------------------------------+
                                          |          Host Kernel / nftables        |
                                          |   ip saddr 10.0.0.0/8 masquerade -> WAN|
                                          +-------------------+--------------------+
                                                              |
                          +-----------------------------------+-----------------------------------+
                          |                                                                       |
              [ Team k VPN: 10.k.0.0/24 ]                                             [ Team k LAN: 10.k.1.0/24 ]
           WireGuard Interface: wg-k (:51820+k)                                      Linux Host Bridge: br-team-k
                Host Gateway: 10.k.0.1                                                  Host Gateway: 10.k.1.1
                          |                                                                       |
     +--------------------+--------------------+                             +--------------------+--------------------+
     |                    |                    |                             |                    |                    |
Player 1              Player 2             Player 253                     c-k-web              c-k-db              c-k-...
10.k.0.2/32          10.k.0.3/32          10.k.0.254/32                 10.k.1.2/24          10.k.1.3/24          10.k.1.x/24
(AllowedIPs)         (AllowedIPs)         (AllowedIPs)                  (veth / eth0)        (veth / eth0)        (veth / eth0)

                                                      [ Verification Trigger: POST /teams/{k}/verificator ]
                                                                                |
                                                                                v  (Fast CoW ZFS Snapshot)
                                                              +---------------------------------------------------+
                                                              |           Dark OVN L2 Switch: verify-k            |
                                                              |   (No host routing collision; ipv4.address: none) |
                                                              +-------------------------+-------------------------+
                                                                                        |
                                                               +------------------------+------------------------+
                                                               |                                                 |
                                                       verify-k-web                                      verify-runner-k
                                                       10.k.1.2/24                                       10.k.1.250/24
                                                       (Cloned container)                                (Ephemeral test runner)
```

---

## 4. Key Architectural & Operational Rules

1. **Subnet Independence per Team ($0 \le k \le 254$):**
   - Each team operates strictly in its designated `10.k.0.0/16` boundary.
   - Cross-team routing is blocked at the firewall level (`nftables` set `@team_links` only authorizes pairs `(wg-k, br-team-k)`).

2. **Reserved IP Conventions in Subnets:**
   - `.0` — Subnet Network address.
   - `.1` — Gateway address (Host endpoint on `wg-k` and `br-team-k`).
   - `.2` to `.254` — Usable host/container IPs.
   - `.250` — Default host byte for ephemeral verifier runner instances.
   - `.255` — Subnet Broadcast address.

3. **Dark OVN vs Host Route Collision Avoidance:**
   - Because `br-team-k` already occupies `10.k.1.1/24` in the Linux host routing table, the ephemeral OVN test switch is created without an IP gateway (`ipv4.address: none`).
   - Clones communicate on an isolated broadcast domain at full native wire speed without host kernel ARP/IP collision.

4. **Path MTU & Clamping:**
   - WireGuard MTU: `1420`
   - OVN Geneve Encapsulation MTU: `1442`
   - `nftables` forces TCP MSS clamping (`tcp option maxseg size set rt mtu`) before forwarding to avoid PMTU discovery blackholes.
