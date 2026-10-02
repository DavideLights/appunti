Viewed incus_client.py:1-100
Viewed containers.py:1-160
Viewed containers.py:161-337
Viewed main.py:1-100
Viewed main.py:100-150
Viewed verifiers.py:1-89
Ran command: `python3 -m py_compile src/blueagent/services/verifiers.py`
Viewed incus_client.py:150-250

Se intendi scalare l'architettura verso **molti utenti e molte challenge** adottando il pattern **"1 container dedicato per utente per challenge"** ($N_{\text{utenti}} \times M_{\text{challenge}}$), BlueAgent e l'infrastruttura sottostante incontreranno diversi colli di bottiglia critici. 

Ecco un'analisi dettagliata dei problemi suddivisi per area, con le relative soluzioni architetturali:

---

### 1. Colli di bottiglia nel codice di BlueAgent (Concorrenza & I/O)

* **I/O sincrono bloccante nel Threadpool di FastAPI:**
  * **Problema:** Gli endpoint di [routers/containers.py](file:///home/debian/blueagent/src/blueagent/routers/containers.py) usano `def` standard anziché funzioni asincrone pure (`async def`). FastAPI li delega al threadpool di AnyIO (default limitato a 40 thread). 
  * In [services/incus_client.py](file:///home/debian/blueagent/src/blueagent/services/incus_client.py#L205), le chiamate a `_wait_for_operation` eseguono una GET di long-polling bloccante verso `/1.0/operations/<uuid>/wait` (con timeout fino a 600s).
  * **Impatto:** Se 40 utenti avviano una challenge in contemporanea, l'intero threadpool si satura in attesa delle risposte da Incus. L'agente smette di rispondere a qualsiasi richiesta (inclusi `/health` o interrogazioni di stato).
  * **Soluzione:** Rendere l'Incus Client nativamente asincrono usando `httpx.AsyncClient` e endpoint `async def`. In questo modo le attese delle operazioni Incus non occupano thread del SO.

* **Singleton `IncusClient` e Connessione Unix Socket condivisa:**
  * **Problema:** Un'unica istanza di `httpx.Client` viene condivisa da tutti i thread ([routers/containers.py#L48-L65](file:///home/debian/blueagent/src/blueagent/routers/containers.py#L48-L65)). `httpx` ha pool limitati di connessioni keep-alive concorrenti verso il socket UDS. Sotto picchi di carico concorrenti, questo può causare timeout o lock interni del pool di trasporto.

---

### 2. Gestione del Ciclo di Vita (Orphan Containers & Mancanza di TTL)

* **Nessun Garbage Collector o scadenza temporale (TTL):**
  * **Problema:** Attualmente i container vengono creati su richiesta e distrutti solo se il controller CTFd invia esplicitamente una `DELETE /containers/{name}`.
  * **Impatto:** Se un utente chiude il browser, abbandona la challenge, o se una richiesta HTTP va persa, il container rimane attivo indefinitamente. Con 50 utenti che provano 5 challenge, ti ritrovi rapidamente con 250 container attivi anche se nessuno li sta usando, esaurendo RAM e CPU dell'host.
  * **Soluzione:** 
    1. Aggiungere un campo `created_at` / `last_active_at` o impostare un TTL per container (es. 1 ora).
    2. Implementare un task di background in BlueAgent (o cron job) che distrugge automaticamente i container inattivi o scaduti.

---

### 3. Limiti di Rete e Allocazione IP

* **Esaurimento del pool DHCP su `incusbr0`:**
  * **Problema:** Il bridge di default di Incus (`incusbr0`) assegna generalmente una subnet IPv4 `/24` (circa 253 indirizzi IP disponibili).
  * **Impatto:** Se $N \times M > 250$, i nuovi container non riceveranno alcun indirizzo IPv4. Le chiamate a `get_instance_state(name).extract_ipv4()` falliranno o restituiranno `None`, bloccando le verifiche di rete ([services/resources.py](file:///home/debian/blueagent/src/blueagent/services/resources.py)).
  * **Soluzione:** Configurare una subnet più ampia (es. `/20` o `/16`) sul bridge di Incus (`incus network set incusbr0 ipv4.address 10.10.0.1/16`).

* **Esposizione delle porte e connettività utente:**
  * **Problema:** Come raggiungono gli utenti i container?
    * Se le porte vengono esposte sull'host tramite proxy device (`incus config device add ... proxy listen=tcp:0.0.0.0:PORT`), due utenti sulla stessa challenge richiedono la stessa porta interna (es. 22 o 80), costringendoti a gestire un complicato port mapping dinamico.
    * Se gli utenti accedono direttamente all'IP del container, è necessaria una VPN (es. WireGuard verso il bridge Incus) o un reverse proxy dinamico (es. Traefik/Envoy basato su sub-domain/SNI).

---

### 4. Limiti Risorse Host & Noisy Neighbor (Quote Incus)

* **Assenza di limiti di CPU, RAM e Disco:**
  * **Problema:** In [routers/containers.py#L122-L128](file:///home/debian/blueagent/src/blueagent/routers/containers.py#L122-L128), i container vengono avviati con il profilo `default` senza specificare quote o limiti di cgroup.
  * **Impatto:** 
    * Un singolo utente che lancia un fork bomb, alloca troppa memoria o genera log infiniti può mandare in kernel OOM (Out Of Memory) l'intero host, abbattendo tutti gli altri container e BlueAgent stesso.
    * Anche a riposo, 300 container Debian/Alpine consumano tra i 15 e i 30 GB di RAM solo per i processi di base (`systemd`/`init`, `rsyslog`, ecc.).
  * **Soluzione:** Definire profili Incus dedicati o configurare config con limiti stretti:
    ```python
    config = {
        "limits.cpu": "1",
        "limits.memory": "256MB",
        "limits.processes": "100",
        "root": {"size": "2GiB"}  # se su ZFS/btrfs
    }
    ```

* **Storage Driver dell'Incus Host:**
  * Se il pool di Incus usa il driver `dir`, ogni container viene copiato per intero (lentissimo e ad alto consumo di disco). È imperativo usare un backend CoW (**ZFS** o **Btrfs**) per creare e distruggere istanze istantaneamente tramite snapshot senza duplicare i file.

---

### 5. Race Conditions e Mancanza di Locking per Istanza

* **Stato concorrente non sincronizzato:**
  * **Problema:** Non esiste alcun lock per nome di container.
  * **Impatto:** Se l'interfaccia CTFd invia richieste ravvicinate (es. doppio clic su "Riavvia" o "Verifica" mentre è in corso un'operazione di start/stop), Incus restituirà un errore `409 Conflict` ("Instance is already starting" o "Operation in progress"). BlueAgent attualmente propaga questi errori come `500` o `502` ([main.py](file:///home/debian/blueagent/src/blueagent/main.py#L80-L97)).
  * **Soluzione:** Implementare un meccanismo di locking in memoria per container (es. `asyncio.Lock()` per chiave `container_name`) o una coda di operazioni serializzate per istanza.

---

### 6. Sicurezza ed Esecuzione del Verifier (`/verify`)

* **Esecuzione di codice arbitrario nel processo di BlueAgent:**
  * **Problema:** In [routers/containers.py#L248-L265](file:///home/debian/blueagent/src/blueagent/routers/containers.py#L248-L265), lo script `.py` caricato via HTTP viene importato dinamicamente con `importlib.util` ed eseguito direttamente **all'interno del processo Python di BlueAgent**.
  * **Impatto:** 
    * **Sicurezza:** Uno script di verifica con codice malevolo o buggato ha accesso a tutta la memoria di BlueAgent, alle sue variabili d'ambiente, al socket di Incus (`/var/lib/incus/unix.socket`), e può chiamare `sys.exit()`, consumare tutta la memoria o mandare in crash il servizio.
    * **GIL & Blocco thread:** Se 30 verifiche girano in contemporanea, si contendono il GIL di Python e il pool di thread.
  * **Soluzione:** Eseguire i verifier in sottoprocessi isolati con permessi minimi (o dentro un container effimero "runner" di verifica), anziché importarli nel core dell'agente.

---

### 7. Scalabilità Orizzontale (Single Node vs Multi Node)

* **Vincolo a singolo host:**
  * **Problema:** BlueAgent è attualmente pensato per gestire una singola istanza Incus locale tramite Unix socket.
  * **Impatto:** Un singolo server fisico/VM ha un limite rigido di container eseguibili (tipicamente 100-300 leggeri su hardware standard).
  * **Soluzione futura:** 
    * Sfruttare le capacità di **Incus Cluster**: configurare Incus in modalità cluster nativa su più nodi fisici; Incus distribuirà i container sui nodi tramite `target` o scheduler.
    * In alternativa, distribuire più istanze di BlueAgent (una per nodo fisico) coordinate a monte da CTFd o da un load balancer con routing basato sull'assegnazione utente-nodo.

---

### Riepilogo delle Priorità di Intervento

| Priorità       | Area                      | Azione Consigliata                                                                 |
| -------------- | ------------------------- | ---------------------------------------------------------------------------------- |
| 🔴 **Critica** | **TTL & Cleanup**         | Evitare che i container dimenticati saturino RAM e disco dell'host.                |
| 🔴 **Critica** | **Subnet Incus**          | Allargare la subnet di `incusbr0` oltre la `/24`.                                  |
| 🟠 **Alta**    | **I/O Asincrono**         | Convertire `IncusClient` in `httpx.AsyncClient` per sbloccare la concorrenza HTTP. |
| 🟠 **Alta**    | **Resource Quotas**       | Limitare CPU, RAM e processi massimi nei profili Incus delle challenge.            |
| 🟡 **Media**   | **Isolamento Verifier**   | Eseguire gli script di verifica fuori dal processo principale di BlueAgent.        |
| 🟡 **Media**   | **Locking per Container** | Gestire la mutua esclusione sulle transizioni di stato (`start`/`stop`/`delete`).  |