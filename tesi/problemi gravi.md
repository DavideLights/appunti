### aggiungere controllo sull'utilizzo delle risorse

#### A. The UDP Path MTU Blackhole

- **Cause**: WireGuard encapsulates packets with a 60–80 byte header (interface MTU 1420), and OVN overlays add Geneve headers (host MTU - 58).
- **Impact**: BlueAgent enforces TCP MSS Clamping (`rt mtu`) via nftables, which **only fixes TCP packets**. If a challenge uses large **UDP datagrams** with the Don't Fragment (DF) flag set (e.g., large DNSSEC responses, UDP VPNs, or custom binary game protocols), packets exceeding ~1420 bytes will be **silently dropped without warning**.

#### A. Process-Local Locks in Multi-Worker ASGI

- **Cause**: By default, `LockRegistry` uses Python's in-memory `asyncio.Lock`.
- **Impact**: If FastAPI/Uvicorn is deployed behind multi-process workers (e.g., Gunicorn with 4 workers) without setting `BLUEAGENT_USE_FILE_LOCKS=true`, two requests for the same team hitting different worker processes can execute concurrently, triggering Incus `HTTP 409 Conflict` errors. For multi-node distributed setups, Redis-backed distributed locks (`Redlock`) would be required.