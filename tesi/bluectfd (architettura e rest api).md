
**Scenario macchine**: posso spawnare **una macchina per utente**. Ogni challenge ha la sua macchina docker
* **interfaccia Patch Challenge**: esegui/ferma la macchina per la challenge corrente

![[bluectfd.excalidraw]]

**ASSUNZIONE, scenario semplificato**: la configurazione della challenge indica il Verification Agent con cui parlo

* `PatchChallenge`: e' la classe della challenge
* `PatchChallengeModel`: e' il modello che rappresenta la patch challenge nel suo database
	* `config`: e' una stringa che rappresenta il JSON
* `PatchFlag`: e' la flag, il metodo `compare` si occupa di validare la flag.
	* `compare`: contatta il verification agent fornito nel config della challenge per determinare se la challenge e' stata superata.
* `CLIENT BROWSER`: e' in grado di inoltrare via API REST, delle richieste al Verification Controller
	* **bypass del verification controller**: non e' possibile. Assumiamo che il verification controller e' l'oracolo  per qualsiasi richiesta

# glossario rest api
* **Verification Agent**: e' l'agente che gestisce la comunicazione il container (o macchina) vulnerabile
* **Macchina Target**: e' la macchina gestita dal suo Verification Agent di riferimento

**GET**: recuparea la rappresentazione della risorsa nell'URI
**POST**: creare la risorsa identificata dall'URI. oppure invia dati ad una risorsa esistente
* **non idempotente**
**PUT**: aggiornare una risorsa se esistente, o creare una risorsa se non esiste.
* corpo: rappresentazione della risorsa
* sostituisce la risorsa se gia esiste.
* **idempotenza**: inviare piu volta la stessa PUT non cambia il server.
**PATCH**: richiesta di aggiornamento parziale di una risorsa esistente.
* corpo: modifiche da effettuare.

**DELETE**: rimuove la risorsa

# Verifcation Controller API 
**cosa rapresenta**: l'API esposta dal Verification Controller agli admin e gli utenti di CTFd. Essenzialemente prende una richiesta, e la scompone in piu richieste per il Verification Target per 

## PatchChallengeTarget `/patch_challenges/id
**cosa rappresenta**: l'interfaccia verso la macchina target della patch `id`.
* **GET**: richiesta dello stato della macchina target. E' in esecuzione?
* **POST**: per avviare la macchina
* **PUT**: per avviare la macchina o fare il restore o il reset.
* **~~PATCH~~**: estendi lifetime e altre cose???
* **DELETE**: ferma la macchina

## PatchChallengeFlag `/patch_challenges/id/flag`
**cosa rappresenta**: la flag, relativa alla patch.
* **GET**: invia tutte le azioni necessarie al verification agent, ed aspetta i risultati per determinare se la flag e' stata ottenuta

## PatchChallengeSLA
`patch_challenges/id/sla`
**cosa rappresenta**: l'SLA della macchina target.
* **GET**: richiedi l'SLA della macchina target

# verification agent

## Container `/containers/id`
**cosa rappresenta**: l'interfaccia verso il container della patch `id`.
* **GET**: ritorna lo stato del container (es: e' in esecuzione)
* **POST**: per avviare il container
* **PUT**: per avviare il container, fare il restore o il reset.
* **DELETE**: ferma il container
## ContainerBatch `/containers/id/batch`
**cosa rappresenta**: un batch di operazioni orchestrate dal verification agent, da eseguire in ordine sul container `id`. L'output quando disponibile viene inviato tramite API REST ad `/patch_challenges/id/batch`
* **POST**: richiedi l'esecuzione di un'batch di azioni specificato nel corpo

# blueagent architettura secondo antigravity

**Raccomandato: FastAPI (Python)**

| Aspetto               | FastAPI                          | Flask                             |
| --------------------- | -------------------------------- | --------------------------------- |
| Async nativo          | ✅ `async/await` built-in         | ❌ sincrono, serve gevent/eventlet |
| Validazione           | ✅ Pydantic automatico            | ❌ manuale                         |
| API docs              | ✅ Swagger/OpenAPI auto-generati  | ❌ da aggiungere                   |
| Consistenza con CTFd  | ⚠️ diverso ma sempre Python      | ✅ stesso framework                |
| Performance I/O-bound | ✅ eccellente per chiamate Docker | ⚠️ blocking                       |

FastAPI è la scelta migliore perché:
- Le operazioni del BlueAgent sono **I/O-bound** (attesa Docker, rete, file) → l'async nativo fa una differenza reale.
- La **validazione Pydantic** ti permette di definire i modelli di richiesta/risposta una volta e avere validazione + documentazione gratis. Si sposa bene con lo schema `PatchChallengeExample.json`.
- Rimani in **Python**, quindi puoi riutilizzare conoscenze e potenzialmente condividere modelli/schemi con il plugin CTFd.

Struttura minimale:
```
blueagent/
├── main.py              # FastAPI app + routes
├── models.py            # Pydantic schemas (request/response)
├── container_manager.py # Logica Docker
├── config.py            # Configurazione agente
└── requirements.txt
```

---

## Gestione Container

**Raccomandato: `docker-py`** (SDK ufficiale Python per Docker)

```python
import docker
client = docker.from_env()  # connessione via socket

# Operazioni che ti servono
container = client.containers.run("challenge-image", detach=True)
container.stop()
container.restart()  # ← per il "Restore"
container.logs()
container.attrs["NetworkSettings"]["IPAddress"]  # ← IP da ritornare al frontend
```

Perché `docker-py`:
- **SDK ufficiale**, ben mantenuto, documenta tutte le API Docker.
- Copre tutto ciò che ti serve: `run`, `stop`, `restart`, `exec_run` (per eseguire test dentro il container), `logs`, inspect rete.
- Evita di fare `subprocess.call(["docker", ..."])` che è fragile e meno sicuro.

### Alternative da valutare solo se servono:

| Tecnologia | Quando usarla |
|---|---|
| **Podman + `podman-py`** | Se vuoi rootless containers (più sicuro in ambiente CTF) |
| **Docker Compose** (via `docker compose` CLI) | Se ogni challenge ha più container (es. web + db) |
| **containerd / nerdctl** | Overkill per questo caso |

---

## Sicurezza (importante per un CTF!)

- **Autenticazione**: token condiviso tra CTFd e BlueAgent (header `Authorization: Bearer <token>`), configurato in entrambi.
- **Bind**: il BlueAgent dovrebbe ascoltare solo sull'interfaccia di rete interna, non su `0.0.0.0`.
- **Rate limiting**: i partecipanti non devono poter spammare start/stop.
- **Isolamento container**: usa `--network=none` o reti dedicate per evitare che i container challenge comunichino tra loro.

---

## Riassunto scelta consigliata

| Componente | Tecnologia |
|---|---|
| **Linguaggio** | Python 3.11+ |
| **Framework API** | FastAPI + uvicorn |
| **Container runtime** | Docker |
| **SDK container** | `docker-py` |
| **Validazione** | Pydantic |
| **Comunicazione CTFd ↔ Agent** | REST + Bearer token |








