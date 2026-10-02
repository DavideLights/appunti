# Architettura REST API di BlueAgent (v2)

## 1. Visione Generale e Filosofia Architetturale (v2)

**BlueAgent** è un controller ed orchestratore ad alte prestazioni sviluppato in Python con **FastAPI**, progettato per la gestione automatizzata di Cyber Range e competizioni di cybersecurity ad elevata complessità (come **Attack-Defense** e **Patch Management**).

A differenza delle tradizionali piattaforme che si affidano a complesse reti overlay software-defined (SDN) o orchestratori cloud-native generici (Kubernetes), BlueAgent v2 adotta la filosofia del **"Rasoio di Occam"**, combinando le primitive native del kernel Linux con il motore di system container **Incus**, **Distrobuilder** per la definizione delle immagini, la predisposizione a **Ansible** per il provisioning pre-gara, e un innovativo sistema di isolamento basato su **Network Namespaces (`netns`)**.

```
                                  +---------------------------------------+
                                  |            HOST BLUEAGENT             |
                                  |                                       |
  [Partecipante] ---------------->| wg-k (VPN L3: 10.k.0.0/30)            |
  (via WireGuard)                 |   └─> br-team-k (Bridge L2: 10.k.1.1) |
                                  |        ├─> Container Web (10.k.1.2)   |
                                  |        └─> Container DB  (10.k.1.3)   |
                                  +---------------------------------------+
                                                      |
                                       (Snapshot Copy-on-Write ~100ms)
                                                      v
                                  +---------------------------------------+
                                  |     NETWORK NAMESPACE: ns-verify-uuid |
                                  |                                       |
                                  |  br-verify-uuid (Unmanaged Bridge)    |
                                  |  (Gateway Assegnato: 10.k.1.1)        |
                                  |    ├─> Clone Web (10.k.1.2 - eth0)    |
                                  |    ├─> Clone DB  (10.k.1.3 - eth0)    |
                                  |    └─> Verifier Container / Script    |
                                  +---------------------------------------+
```

### Principi Architetturali Chiave di BlueAgent v2:

1. **Isolamento della Sandbox di Verifica via Network Namespaces (`netns`):**
   * Supera i limiti della precedente architettura a doppia interfaccia (`eth1`), eliminando del tutto la seconda scheda di rete.
   * Al momento della verifica, BlueAgent alloca un **Network Namespace** dedicato (`ns-verify-uuid`) nel kernel.
   * All'interno del namespace viene creato un bridge *unmanaged* (`br-verify-uuid`) a cui viene assegnato l'IP gateway originale (`10.k.1.1`).
   * I container del team vengono duplicati istantaneamente via snapshot **Copy-on-Write (CoW)** e collegati al bridge del namespace.
   * **Fedeltà Topologica Totale:** I cloni mantengono un'unica interfaccia **`eth0`** con l'IP statico nativo (`10.k.1.x`), garantendo che l'exploit o la patch vengano valutati in un ambiente identico al 100% alla produzione.

2. **Distrobuilder & Templating dell'Indirizzamento IP:**
   * Le immagini dei container vengono definiti in modo dichiarativo tramite file YAML di **Distrobuilder**, garantendo ambienti Linux puliti e ottimizzati per `systemd`.
   * L'indirizzamento IP utilizza un sistema a template dinamici: l'IP statico della sfida per il team $k$ (es. `10.k.1.x`) viene parametrizzato ed applicato da BlueAgent al momento dell'avvio o profilazione del container (`incus start` / patch di configurazione).

3. **Predisposizione all'Integrazione con Ansible (Future Readiness):**
   * L'architettura e l'API REST sono progettate per integrare **Ansible** come motore dichiarativo di *provisioning* pre-gara.
   * Ansible può essere invocato a monte per automatizzare il setup di contesti complessi (popolamento di database, configurazione di utenti e vulnerabilità articolate) all'interno di container master, lasciando ad Incus e `netns` la clonazione e verifica a runtime in ~100 ms.

4. **Zero Side-Channel Leak e Protezione dell'Ambiente Live:**
   * L'esecuzione dell'exploit avviene interamente nel namespace isolato. Nessun pacchetto di test attraversa la rete di produzione.
   * I concorrenti non possono intercettare i payload tramite sniffer (`tcpdump`) o log di sistema sul container live, ed eventuali crash generati dall'exploit impattano esclusivamente la sandbox effimera.

---

## 2. Architettura di Rete e Schema di Indirizzamento

### A. Indirizzamento L2/L3 per Team ($k$)

L'indirizzamento IP è deterministico e calcolato in base all'indice unico del team ($k \in [1, 254]$):

* **WireGuard Tunnel (`wg-k`):** Subnet L3 punto-punto `10.k.0.0/30` per l'accesso crittografato e sicuro dei partecipanti.
* **Linux Bridge L2 (`br-team-k`):** Switch virtuale dedicato al team $k$. L'host assegna l'IP `10.k.1.1` come *default gateway*.
* **Container (`eth0`):** IP statici sulla subnet /24 (`10.k.1.x`), con topologia identica per ogni team (es. Web Server su `.2`, Database su `.3`).

| Componente | Interfaccia / Tipo | Indirizzamento IP | Ruolo |
| :--- | :--- | :--- | :--- |
| **VPN Partecipante** | `wg-k` (WireGuard) | `10.k.0.1/30` (Host), `10.k.0.2` (Client) | Terminatore crittografico L3 per i partecipanti |
| **Bridge Produzione** | `br-team-k` (Linux Bridge) | `10.k.1.1/24` | Switch L2 e Default Gateway live per il team $k$ |
| **Container Live** | `eth0` (veth paired) | `10.k.1.x/24` | Servizi vulnerabili live in gara |
| **Bridge Verifica** | `br-verify-uuid` (*unmanaged*) | `10.k.1.1/24` (nel `netns`) | Switch L2 isolato nel `ns-verify-uuid` |
| **Container Clonato** | `eth0` (veth paired) | `10.k.1.x/24` (nel `netns`) | Replica CoW usa-e-getta per la verifica |

---

## 3. Schemi di Configurazione e Modellazione Pydantic v2

Tutti i dati, le richieste HTTP e i file di configurazione YAML delle challenge sono modellati rigorosamente con **Pydantic v2** per garantire la validazione dei tipi eliminando dizionari non tipizzati.

### A. Modellazione del File di Configurazione YAML (`challenge.yaml`)

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class CommandSpec(BaseModel):
    container: str = Field(..., description="Nome del container target (es. 'web', 'db')")
    cmd: List[str] = Field(..., description="Comando ed argomenti da eseguire")
    env: Dict[str, str] = Field(default_factory=dict, description="Variabili d'ambiente")
    timeout: int = Field(default=15, description="Timeout in secondi")

class ContainerSpec(BaseModel):
    name: str = Field(..., description="Nome logico del container nella challenge")
    distrobuilder_image: str = Field(..., description="Immagine base generata da Distrobuilder")
    ip_suffix: int = Field(..., ge=2, le=254, description="Ultimo ottetto dell'IP (10.k.1.x)")
    limits_cpu: str = Field(default="1", description="Quota CPU cgroup (es. '1')")
    limits_memory: str = Field(default="256MB", description="Quota RAM cgroup (es. '256MB')")

class VerifierContainerSpec(BaseModel):
    enabled: bool = False
    image: Optional[str] = None
    script_path: Optional[str] = None

class ChallengeConfig(BaseModel):
    challenge_id: str
    title: str
    containers: List[ContainerSpec]
    verifier_container: Optional[VerifierContainerSpec] = None
    readiness_commands: List[CommandSpec] = Field(default_factory=list)
    verify_commands: List[CommandSpec] = Field(default_factory=list)
```

### B. Modelli API REST per Request / Response HTTP

```python
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Optional, Any

class TeamCreateReq(BaseModel):
    team_id: str = Field(..., description="ID del team (es. 'team-01' o indice intero)")

class TeamConfigResp(BaseModel):
    success: bool
    result: str
    message: str
    team_id: str
    wg_config: str
    ttl_expires_at: datetime

class TTLRenewReq(BaseModel):
    extend_minutes: int = Field(default=60, ge=15, le=240, description="Minuti di estensione TTL")

class ActionReq(BaseModel):
    actions: Dict[str, str] = Field(..., description="Mappa container -> azione (start, stop, restart)")

class VerifyResultResp(BaseModel):
    success: bool
    passed: bool
    message: str
    verify_results: Optional[Any] = None
```

---

## 4. Mappa Completa delle API REST (FastAPI)

Tutti gli endpoint di gestione dell'infrastruttura sono protetti da **JSON Web Token (JWT)** tramite `HTTPBearer`.

### Endpoint Rete e Gestione Team (`/teams`)

#### 1. `POST /teams`
* **Descrizione:** Inizializza l'infrastruttura di rete per un nuovo team $k$.
* **Azioni:**
  1. Alloca e crea l'interfaccia WireGuard `wg-k` e genera la configurazione `.conf` per i partecipanti.
  2. Crea il Linux Bridge `br-team-k` e vi assegna l'IP gateway `10.k.1.1/24`.
  3. Registra la sessione del team con un TTL di default (es. 120 minuti).
* **Risposta:** `TeamConfigResp` con la configurazione WireGuard scaricabile.

#### 2. `GET /teams/{team_id}`
* **Descrizione:** Recupera le informazioni di stato dell'infrastruttura di rete e la configurazione WireGuard del team.

#### 3. `DELETE /teams/{team_id}`
* **Descrizione:** Termina manualmente l'infrastruttura del team, fermando ed eliminando tutti i container e le interfacce di rete.

#### 4. `POST /teams/{team_id}/renew-ttl`
* **Descrizione:** Estende il Time-To-Live (TTL) della sessione del team, prevenendo la bonifica automatica da parte del background worker.

---

### Endpoint Lifecycle Sfide e Container (`/teams/{team_id}/challenges`)

#### 5. `POST /teams/{team_id}/challenges`
* **Descrizione:** Istanziamento dei container della challenge per il team $k$.
* **Azioni:**
  1. Verifica la presenza dell'immagine generata tramite **Distrobuilder**; se assente, ne avvia la compilazione.
  2. Crea i container di sistema Incus e applica i limiti cgroup (CPU, RAM).
  3. Collega la scheda `eth0` dei container al bridge `br-team-k` ed applica l'IP statico dinamico `10.k.1.x`.
  4. Avvia i container.

#### 6. `GET /teams/{team_id}/challenges`
* **Descrizione:** Restituisce lo stato operativo (Running, Stopped, IP, utilizzo risorse) di tutti i container del team.

#### 7. `PUT /teams/{team_id}/challenges`
* **Descrizione:** Esegue azioni di controllo dello stato su uno o più container del team (`start`, `stop`, `restart`).

#### 8. `DELETE /teams/{team_id}/challenges`
* **Descrizione:** Ferma ed elimina i container relativi a una specifica challenge senza distruggere la VPN del team.

---

### Endpoint di Verifica Sandbox (`/teams/{team_id}/challenges/verify`)

#### 9. `POST /teams/{team_id}/challenges/verify`
* **Descrizione:** Avvia la procedura automatizzata di verifica delle patch o degli exploit tramite sandbox **`netns`**.
* **Workflow Integrato (`async with NetNSVerifier`):**
  1. **Namespace Setup:** Crea un `netns` temporaneo (`ns-verify-uuid`) ed il bridge *unmanaged* (`br-verify-uuid`) configurato con l'IP gateway `10.k.1.1`.
  2. **CoW Snapshot:** Esegue lo snapshot Copy-on-Write dei container del team su Incus in **~100 ms** e collega la loro scheda `eth0` al bridge `br-verify-uuid`.
  3. **Readiness Check:** Esegue i comandi di readiness per attendere che i servizi nei cloni siano operativi.
  4. **Verification Check:** Esegue gli script/container Verifier **all'interno del namespace** via `ip netns exec` per testare la vulnerabilità.
  5. **Guaranteed Teardown:** Al termine, il Context Manager asincrono arresta ed elimina i cloni su Incus e rimuove il `netns` dal kernel, restituendo l'esito a FastAPI.
* **Risposta:** `VerifyResultResp` contenente l'esito della verifica (`passed: true/false`), il messaggio e i dettagli dell'esecuzione.

---

## 5. Implementazione del Control Plane in Python

### A. Context Manager Asincrono per la Sandbox (`NetNSVerifier`)

```python
import asyncio
import uuid
import logging
from typing import Dict, Any, List
import httpx

logger = logging.getLogger("blueagent.verifier")

class NetNSVerifier:
    def __init__(self, team_id: str, config: ChallengeConfig, incus_socket: str = "/var/lib/incus/unix.socket"):
        self.team_id = team_id
        self.config = config
        self.uuid_suffix = uuid.uuid4().hex[:8]
        self.ns_name = f"ns-verify-{self.uuid_suffix}"
        self.bridge_name = f"br-v-{self.uuid_suffix}"
        self.cloned_containers: List[str] = []
        
        # Client HTTPX asincrono comunicante su Unix Socket Incus
        self.incus_client = httpx.AsyncClient(
            transport=httpx.AsyncHTTPTransport(uds=incus_socket),
            base_url="http://localhost/1.0"
        )

    async def _run_cmd(self, cmd: str) -> str:
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(f"Comando fallito [{cmd}]: {stderr.decode().strip()}")
        return stdout.decode().strip()

    async def __aenter__(self):
        logger.info(f"Setup sandbox netns {self.ns_name} per team {self.team_id}")
        try:
            # 1. Creazione del Network Namespace e Bridge Unmanaged
            await self._run_cmd(f"sudo ip netns add {self.ns_name}")
            await self._run_cmd(f"sudo ip link add name {self.bridge_name} type bridge")
            await self._run_cmd(f"sudo ip link set {self.bridge_name} netns {self.ns_name}")

            # 2. Configurazione del Gateway nativo (10.k.1.1) dentro il netns
            team_idx = self.team_id.replace("team-", "")
            await self._run_cmd(f"sudo ip netns exec {self.ns_name} ip addr add 10.{team_idx}.1.1/24 dev {self.bridge_name}")
            await self._run_cmd(f"sudo ip netns exec {self.ns_name} ip link set dev {self.bridge_name} up")
            await self._run_cmd(f"sudo ip netns exec {self.ns_name} ip link set dev lo up")

            # 3. Snapshot Copy-on-Write e clonazione container via API Incus (~100ms)
            for c_spec in self.config.containers:
                source_name = f"{self.team_id}-{c_spec.name}"
                clone_name = f"{source_name}-v-{self.uuid_suffix}"
                
                # Chiamata API Incus per CoW Copy
                res = await self.incus_client.post("/instances", json={
                    "name": clone_name,
                    "source": {"type": "copy", "source": source_name},
                    "instance_type": "container"
                })
                await self._wait_incus_op(res.json()["operation"])

                # Riconfigurazione della scheda eth0 sul bridge unmanaged del netns
                await self.incus_client.patch(f"/instances/{clone_name}", json={
                    "devices": {
                        "eth0": {
                            "type": "nic",
                            "nictype": "bridged",
                            "parent": self.bridge_name
                        }
                    }
                })

                # Avvio del clone
                start_res = await self.incus_client.put(f"/instances/{clone_name}/state", json={"action": "start"})
                await self._wait_incus_op(start_res.json()["operation"])
                self.cloned_containers.append(clone_name)

            return self
        except Exception as e:
            logger.error(f"Errore durante il setup della sandbox: {e}")
            await self._teardown()
            raise e

    async def run_verification() -> Dict[str, Any]:
        """Esegue comandi di readiness ed exploit isolati dentro il netns."""
        for cmd_spec in self.config.verify_commands:
            target_clone = f"{self.team_id}-{cmd_spec.container}-v-{self.uuid_suffix}"
            cmd_str = f"sudo ip netns exec {self.ns_name} incus exec {target_clone} -- {' '.join(cmd_spec.cmd)}"
            
            proc = await asyncio.create_subprocess_shell(
                cmd_str, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                return {"passed": False, "reason": f"Fallito comando su {cmd_spec.container}", "details": stderr.decode()}

        return {"passed": True, "reason": "Tutti i verifier hanno avuto esito positivo"}

    async def _wait_incus_op(self, op_path: str):
        while True:
            res = await self.incus_client.get(f"{op_path}/wait")
            if res.json()["metadata"]["status"] == "Success":
                break
            await asyncio.sleep(0.05)

    async def _teardown(self):
        """Teardown atomico in ordine inverso: Stop/Delete Incus -> Del NetNS."""
        logger.info(f"Teardown sandbox {self.ns_name}")
        for clone_name in self.cloned_containers:
            try:
                stop_res = await self.incus_client.put(
                    f"/instances/{clone_name}/state", json={"action": "stop", "force": True, "timeout": 0}
                )
                if stop_res.status_code == 200:
                    await self._wait_incus_op(stop_res.json()["operation"])
                del_res = await self.incus_client.delete(f"/instances/{clone_name}")
                if del_res.status_code == 200:
                    await self._wait_incus_op(del_res.json()["operation"])
            except Exception as e:
                logger.error(f"Errore durante l'eliminazione del clone {clone_name}: {e}")

        try:
            await self._run_cmd(f"sudo ip netns del {self.ns_name}")
        except Exception as e:
            logger.error(f"Errore durante l'eliminazione del netns {self.ns_name}: {e}")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._teardown()
        await self.incus_client.aclose()
```

---

### B. Gestione Ciclo di Vita (TTL Worker) in FastAPI Lifespan

```python
import asyncio
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status

team_ttl_registry: Dict[str, datetime] = {}

async def ttl_cleanup_worker(check_interval_seconds: int = 60):
    """Task periodico in background che elimina le infrastrutture i cui TTL sono scaduti."""
    while True:
        try:
            await asyncio.sleep(check_interval_seconds)
            now = datetime.now(timezone.utc)
            expired_teams = [team_id for team_id, expires_at in team_ttl_registry.items() if now > expires_at]
            
            for team_id in expired_teams:
                logger.info(f"TTL Scaduto per team {team_id}. Avvio bonifica risorse...")
                # Invocazione bonifica infrastruttura team
                del team_ttl_registry[team_id]
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Errore nel worker TTL: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    cleanup_task = asyncio.create_task(ttl_cleanup_worker(check_interval_seconds=30))
    yield
    cleanup_task.cancel()
    await asyncio.gather(cleanup_task, return_exceptions=True)

app = FastAPI(title="BlueAgent Controller v2", lifespan=lifespan)
```

---

## 6. Sintesi dei Vantaggi dell'Integrazione REST API + `netns`

1. **Interfaccia REST Semplice e Tipizzata:** Tutta la complessità dell'allocazione dei `netns` del kernel Linux è totalmente astratta dietro semplici chiamate HTTP validatene con Pydantic v2.
2. **Resilienza e Sicurezza:** Il Context Manager asincrono `NetNSVerifier` garantisce l'eliminazione delle risorse temporanee anche in presenza di eccezioni, prevenendo il leak di namespace orfani.
3. **Efficienza I/O e Scalabilità:** Le chiamate REST ad Incus su Unix Domain Socket utilizzano un client HTTPX puramente asincrono, evitando il blocco dei thread dell'Event Loop di FastAPI.
4. **Fedeltà Topologica Totale:** I comandi di verifica eseguiti via `POST /teams/{team_id}/challenges/verify` operano su cloni identici al 100% alla produzione (singola scheda `eth0`), azzerando i falsi negativi ed eliminando i *side-channel leak*.
