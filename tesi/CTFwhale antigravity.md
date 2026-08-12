Il plugin **CTFd-Whale** è un'estensione che fornisce **ambienti dinamici e isolati (container Docker) per ogni singolo utente o squadra**. 
* permette a ogni utente di avviare, estendere (renew) o distruggere il proprio container privato con un solo clic.

### 💡 Idea di Base
* **Docker Swarm** per il deployment 
* **frp** (Fast Reverse Proxy) per il routing del traffico. 
* **Funzionamento**: quando un utente decide di affrontare una "Dynamic Docker Challenge", il plugin comunica con il demone Docker, avvia un container dedicato e usa *frp* per esporre i servizi del container tramite una porta casuale o un sottodominio univoco. 
* **iniettare flag**: possono essere generate dinamicamente e iniettate nel container al momento dell'avvio, garantendo che ogni utente abbia una flag diversa. 
* **autopulizia**:  meccanismo di auto-pulizia che distrugge i container **quando scade il tempo a disposizione dell'utente**.

### 📁 File Principali
* [`__init__.py`](file:///home/davidel/tesi/ctfd-whale/__init__.py): È il punto di ingresso del plugin. Si occupa di registrare le rotte (Blueprint), inizializzare il database, configurare i menu di amministrazione, registrare il nuovo tipo di challenge in CTFd e avviare il **demone in background** (tramite `APScheduler`) che si occupa di **distruggere i container scaduti**.
* [`models.py`](file:///home/davidel/tesi/ctfd-whale/models.py): Definisce lo schema del database. Contiene le definizioni delle tabelle per salvare le configurazioni del plugin, le informazioni specifiche delle challenge Docker e lo stato dei container attivi associati agli utenti.
* [`challenge_type.py`](file:///home/davidel/tesi/ctfd-whale/challenge_type.py): Contiene la logica di business specifica per questo nuovo tipo di challenge (chiamata `dynamic_docker`). Gestisce cosa succede quando una challenge viene creata, letta, aggiornata o quando un utente tenta di inviare una flag.
* `api.py` *(non esplorato nel dettaglio, ma fondamentale)*: ***Definisce gli endpoint RESTful*** utilizzati dal frontend (i bottoni "Start", "Renew", "Stop" premuti dagli utenti) e dal pannello di amministrazione per gestire i container.
* `utils/`: Una cartella contenente script di utilità per dialogare con le API di Docker (`docker.py`), gestire il routing frp (`routers.py`), eseguire controlli sul sistema (`checks.py`) e orchestrare la creazione/distruzione (`control.py`).

### 🧩 Costrutti, Classi e Tipi utilizzati
* **Object-Relational Mapping (ORM) con SQLAlchemy:** Il plugin estende il database di CTFd creando nuove classi che ereditano da `db.Model` o da modelli CTFd esistenti. 
  * Esempio: `DynamicDockerChallenge` eredita da `DynamicChallenge` (di CTFd) aggiungendo campi come `memory_limit`, `cpu_limit`, e `docker_image`.
  * Esempio: `WhaleContainer` tiene traccia dell'utente (`user_id`), della challenge (`challenge_id`), dell'UUID del container, della porta e della flag dinamica generata.
* **Polimorfismo (Polymorphic Identity):** La classe `DynamicDockerChallenge` usa `__mapper_args__ = {"polymorphic_identity": "dynamic_docker"}` per istruire SQLAlchemy su come integrare questo modello specifico all'interno della tabella generica delle challenge di CTFd.
* **Flask Blueprints e API Namespaces:** Utilizzati per gestire le rotte web e le API REST (es. `Blueprint("ctfd-whale", ...)` e `CTFd_API_v1.add_namespace`).
* **Jinja2 Templates (`jinja2.Template`):** Molto utilizzato in `models.py` per generare stringhe dinamiche come i sottodomini o le flag (es. rendering di una stringa con template `{{ "flag{"+uuid.uuid4()|string+"}" }}`).
* **APScheduler (`flask_apscheduler.APScheduler`):** Costrutto utilizzato per schedulare task in background (il task `whale-auto-clean` gira ogni 10 secondi).

### 💻 Accenni sul Codice
* **Validazione Dinamica della Flag:** In `challenge_type.py`, il metodo `attempt()` sovrascrive il comportamento di default. Se non ci sono flag statiche configurate dall'admin, il sistema va a cercare nella tabella `WhaleContainer` il container specifico attualmente in esecuzione per quell'utente. Se la flag inserita dall'utente (`submission`) corrisponde alla flag dinamica `container.flag` associata al *suo* container, il sistema restituisce `"Correct"`. Altrimenti, rifiuta la flag.

> [!error] CTFwhale e le flag
> Il modo in cui CTFwhale usa le flag non va bene! A noi non serve trovare la flag, ma patchare il servizio.

* **Gestione della Concorrenza:** In `__init__.py` è presente un accenno di gestione della concorrenza (lock tramite `fcntl` su `/tmp/ctfd_whale.lock`). Dato che CTFd usa spesso **Gunicorn con worker multipli**, questo lock assicura che il task in background che ripulisce i container scaduti (via `APScheduler`) venga istanziato da un solo worker e non da tutti contemporaneamente.
* **Integrazione UI:** Nel metodo `load(app)` di `__init__.py`, il plugin inietta template HTML e script JS personalizzati (`assets/create.html`, `assets/view.js`, ecc.) sostituendoli a quelli standard di CTFd tramite il dizionario `DynamicValueDockerChallenge.templates` e `.scripts`. Questo permette alla UI della challenge di mostrare i pulsanti specifici del plugin.