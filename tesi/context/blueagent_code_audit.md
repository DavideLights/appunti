# Audit Architetturale e Piano di Ottimizzazione di BlueAgent

**Data Audit:** 18 Ottobre 2026  
**Target VM:** `debian@192.168.1.108` (`/home/debian/bluectfd/blueagent` & `/home/debian/bluectfd/CTFd/CTFd/plugins/blueagent`)  
**Dimensione Codebase Attuale:** ~5.717 LOC (`src/blueagent/` + `tests/`)

---

## 1. Errori Logici, Race Condition e Bug di Affidabilità

Questa sezione elenca i difetti logici reali individuati nel codice che causano perdita di stato, race condition sotto carico o fallimenti silenziosi.

| # | Modulo | Problema Identificato | Impatto | Soluzione Pianificata |
| :- | :--- | :--- | :--- | :--- |
| **L1** | `main.py`, `services/teams.py` | **Mancata riconciliazione dello stato kernel al riavvio dell'host:** i bridge `br-team-k` e le interfacce WireGuard `wg-k` sono effimeri nel kernel Linux, mentre i record di team, membri e container persistono in SQLite (`blueagent.db`). Al riavvio della VM o del demone, `main.py` applica solo le regole `nftables` base ma **non ricrea i bridge né le interfacce/peer WireGuard** presenti nel DB. Inoltre Incus lascia i container `c-{team_k}-*` in stato `STOPPED` perché il loro bridge non esiste più. | **Critico:** Dopo un riavvio della macchina host (verificato dal vivo sulla VM), tutti i team risultano registrati nel DB ma privi di VPN e bridge, causando `BridgeNotActiveError (409)` su ogni deploy/verifica. | Aggiungere nella `lifespan` di startup (`main.py`) una procedura di riconciliazione che legge i team e i membri da SQLite, ricrea in modo idempotente `br-team-k` e `wg-k`, ri-registra i peer WireGuard e riavvia i container attivi. |
| **L2** | `lifecycle/manager.py` | **Race condition distruttiva sulle reti OVN `verify-*`:** Nel ciclo di pulizia degli orfani (`_run_reconciliation_cycle`), il `LifecycleManager` controlla il `grace_period_seconds` (90s) per i container `verify-*`, ma **elimina incondizionatamente tutte le reti OVN `verify-*` senza alcun controllo di età né di lock**. | **Alto:** Se il timer del `LifecycleManager` scatta nell'istante tra la creazione dello switch `verify-{team_k}` in `OVNVerifier.__aenter__` e il collegamento del primo clone, la rete viene distrutta mentre la verifica sta partendo. | Controllare `locks.is_verify_locked(team_k)` prima di toccare qualsiasi risorsa `verify-{team_k}*` nel `LifecycleManager`, ed eliminare lo switch OVN solo se non è attivo un lock di verifica per quel team. |
| **L3** | `verifier/ovn.py` | **Leak di container "zombie" su fallimento parziale in `__aenter__`:** Il nome del clone (`verify-{team_k}-{c.name}`) viene aggiunto a `self.clones` solo *dopo* che `clone_instance`, `connect_network` e `start_instance` hanno tutte avuto successo. | **Medio-Alto:** Se `connect_network` o `start_instance` fallisce dopo che `clone_instance` ha creato il container ZFS, `_cleanup()` non elimina quel clone, lasciandolo orfano in Incus e bloccando anche la rimozione della rete OVN. | Aggiungere `clone_name` a `self.clones` immediatamente prima/dopo `clone_instance()`, così che `_cleanup()` possa sempre rimuoverlo in caso di errore successivo. |
| **L4** | `verifier/ovn.py` | **Riesecuzione cieca 3x dei `verify_commands` falliti:** In `run_checks()`, dopo che i `readiness_commands` sono già passati, ogni comando di verifica (`verify_commands`) è racchiuso in un ciclo `for attempt in range(3):` senza pausa (`sleep`) che riesegue il comando se `exit_code != 0`. | **Alto:** Quando la patch di un giocatore non è valida (`exit_code != 0`), lo script di exploit/SLA viene eseguito **3 volte di fila**, triplicando il tempo di verifica sul caso fallito e corrompendo lo stato del clone se il check non è idempotente (es. contatori DB, log, rate-limit). | Rimuovere il loop di retry sui `verify_commands` (esecuzione singola e deterministica). Mantenere il polling con backoff esclusivamente sui `readiness_commands`. |
| **L5** | `verifier/ovn.py` | **Flag `verify_internet_access` ignorato:** `ChallengeConfig` definisce `verify_internet_access: bool`, ma `OVNVerifier.__aenter__` cabla `"ipv4.nat": "true"` e `"network": "incusbr0"`, ignorando sia il flag della challenge sia `settings.incus_uplink_network`. | **Medio:** Impossibile isolare da Internet una sandbox di verifica anche quando richiesto dalla challenge (`verify_internet_access: false`). | Rispettare `self.config.verify_internet_access` e `settings.incus_uplink_network` nella creazione dello switch OVN. |
| **L6** | `locks.py`, `engine/incus.py` | **Mutazione condivisa in `LockRegistry` e `404` su operazioni Incus:** `LockRegistry.get_lock()` sovrascrive `self._locks[path].default_timeout = timeout` sull'istanza condivisa tra coroutine concorrenti; `_wait_incus_op` tratta qualsiasi HTTP `404` su `/operations/{uuid}/wait` come successo incondizionato. | **Basso-Medio:** Possibili timeout incoerenti sotto contesa e mascheramento di errori Incus se un'operazione fallisce e viene rimossa rapidamente. | Passare il timeout in fase di `acquire()` senza mutare lo stato condiviso del lock; verificare `GET /1.0/operations/{uuid}` prima di assumere il successo su `404`. |

---

## 2. Ottimizzazioni delle Prestazioni (Snellimento Latenza e I/O)

| # | Area | Collo di Bottiglia Attuale | Ottimizzazione Proposta | Guadagno Stimato |
| :- | :--- | :--- | :--- | :--- |
| **P1** | **Ciclo di vita Multi-Container** (`challenges.py`, `ovn.py`, `teams.py`) | Tutte le operazioni su più container (creazione, push file, avvio, clonazione CoW in verifica, teardown) avvengono in cicli `for` **sequenziali**. | Parallelizzare con `asyncio.gather()` la clonazione/avvio dei container target e la creazione del container `verifier` in `OVNVerifier.__aenter__`, nonché la distruzione dei cloni in `_cleanup()` e nel teardown. | **-40% / -60%** sul tempo di setup e teardown delle verifiche multi-container. |
| **P2** | **Overhead HTTP `incus exec`** (`engine/incus.py`, `challenges.py`, `ovn.py`) | Ogni chiamata `exec_command` forza `"record-output": True` ed esegue **6 chiamate HTTP** su Incus (`POST /exec`, `GET /wait`, 2x `GET logs`, 2x `DELETE logs`). Inoltre, al boot di ogni container/clone vengono lanciati 3 `exec_command` separati (`ip addr`, `ip link`, `ip route`) = **18 roundtrip HTTP per container**. | 1. Aggiungere `capture_output: bool = True` a `exec_command`: quando l'output non serve, usare `"record-output": False` (da 6 a **2 chiamate HTTP**).<br>2. Nei cloni OVN (`ovn.py`), evitare la tripla iniezione `exec_command` ridondante se il container ha già la configurazione statica nel rootfs, o eseguirla in un singolo comando combinato. | **Da 18 a 2 chiamate HTTP** per container durante la configurazione di rete. |
| **P3** | **Connessioni SQLite** (`database.py`) | `DatabaseManager._connect()` apre e chiude una nuova connessione `aiosqlite` ad **ogni singola query** e riesegue ogni volta 3 query `PRAGMA` (`journal_mode=WAL`, `foreign_keys=ON`, `busy_timeout=5000`). | Mantenere una singola connessione `aiosqlite` persistente per il ciclo di vita dell'app (inizializzata in `init_db()` e chiusa nello shutdown), configurando i `PRAGMA` una sola volta. | Eliminazione dell'overhead di apertura file/PRAGMA su ogni operazione DB. |
| **P4** | **Sottoprocessi Host e Chiavi WireGuard** (`network/_runner.py`) | `SubprocessRunner.run()` scrive il buffer `stdin` (usato per passare le **chiavi private e PSK WireGuard** a `wg set`) dentro un file temporaneo su disco (`tempfile.TemporaryFile()`) ad ogni esecuzione. | Usare `stdin=asyncio.subprocess.PIPE` e `await proc.communicate(input=stdin)` in memoria: più veloce, più semplice e non scrive mai chiavi crittografiche su `/tmp`. | Zero I/O su disco per i comandi `wg` e `nft`, maggiore sicurezza delle chiavi. |

---

## 3. Pulizia e Snellimento del Codice ("Clean-up & Debloat")

1. **Unificazione e pulizia di `models.py`:**
   - Rimuovere i modelli duplicati/legacy:
     - `TeamCreateReq` vs `TeamPutReq` $\rightarrow$ unificare in `TeamReq`.
     - `TeamMemberCreateReq` vs `TeamMemberPutReq` $\rightarrow$ unificare in `TeamMemberReq`.
     - `PeerStats` vs `PeerTelemetry` $\rightarrow$ mantenere solo `PeerTelemetry` (usato dalle API attuali).
     - Rimuovere gli alias ridondanti `ChallengeInstance = RunningContainerRecord` e `ActiveChallengeRecord = DeployResponse`.
   - Rimuovere il campo duplicato `instances` da `DeployResponse` (che oggi serializza due volte la stessa lista in `containers` e `instances`).
   - Rimuovere i campi `step_timings` dai modelli di risposta API (`TeamRecord`, `TeamMemberWG`, `DeployResponse`) o renderli opzionali/esclusi se `None` (`exclude_none=True`), evitando di sporcare i contratti JSON.
2. **Rimozione di Codice Morto (Dead Code):**
   - `services/teams.py`: rimuovere `create_team()` (alias inutilizzato) e `get_peer_stats()` (nessun endpoint API lo richiama).
   - `database.py`: rimuovere `get_connection()` (sostituito dal context manager interno) e i metodi non utilizzati.
   - `verifier/ovn.py`: rimuovere `self.session_id` (generato e mai usato).
   - `network/wireguard.py`: semplificare la logica di `generate_member_config` (dove è presente il commento `# TODO: this does not make sense`).
   - `network/commands/ip.py`: rimuovere `netns_exec` (inutilizzato).
   - `images/distrobuilder.py`: rimuovere il blocco `else:` irraggiungibile nella gestione di `proc.stdout`.
3. **Allineamento della Configurazione (`config.py`, `start_services.sh`, `README.md`):**
   - In `start_services.sh` viene passata `BLUEAGENT_DATABASE_PATH`, ma `config.py` si aspetta `BLUEAGENT_DB_PATH` (funziona solo per caso perché lo script fa `cd` nella cartella di BlueAgent). Allineare tutti i nomi delle variabili d'ambiente tra `config.py`, `start_services.sh` e `README.md`.

---

## 4. Ripensare l'Interazione Utente / Client con BlueAgent

Analizzando come l'utente (e il plugin CTFd in `/home/debian/bluectfd/CTFd/CTFd/plugins/blueagent`) interagisce con BlueAgent, emergono **4 criticità nel contratto di interazione attuale**:

### Criticità attuali nell'interazione Client $\leftrightarrow$ BlueAgent
1. **Il Template Rendering (`{{ip:web}}`, `{{subnet}}`, `{{team_k}}`) è delegato al client invece che a BlueAgent:**
   - Oggi BlueAgent non risolve i placeholder `{{ip:<container>}}`, `{{subnet}}`, `{{team_k}}`, `{{verifier_ip}}` nei `readiness_commands` e `verify_commands`. Di conseguenza, il plugin CTFd ha dovuto implementare `render_spec_for_team()` (`spec.py`) per calcolare gli IP `10.{team_k}.1.{suffix}` e fare il replace nel JSON prima di inviarlo a BlueAgent. Chiunque usi BlueAgent da CLI, script o un'altra piattaforma deve farsi i calcoli degli IP a mano.
2. **`DELETE /teams/{team_k}/machines` richiede un Body JSON in una richiesta HTTP `DELETE`:**
   - Per eliminare solo i container di una specifica challenge, l'endpoint `DELETE /teams/{team_k}/machines` accetta un intero oggetto `ChallengeConfig` nel body della `DELETE`. Molti client HTTP, proxy e standard OpenAPI scoraggiano o ignorano il body nelle richieste `DELETE`.
3. **Ripetizione continua dell'intera configurazione (`ChallengeConfig`) ad ogni verifica:**
   - Oggi BlueAgent non memorizza la definizione delle challenge: ad ogni `POST /teams/{team_k}/verificator`, il client deve rispedire l'intero YAML/JSON della challenge (inclusi i container, i limiti RAM/CPU, ecc.). Inoltre `ChallengeConfig` contiene `team_k` (già presente nell'URL!) e `challenge_id`.
4. **Provisioning manuale obbligatorio del Team prima del deploy:**
   - Se CTFd chiama `POST /teams/{team_k}/machines` ma il team non è ancora stato creato su BlueAgent, riceve `404` e deve fare `PUT /teams/{team_k}` e poi riprovare il deploy (`try ... except TeamNotFound` nel plugin CTFd).

---

### Due Proposte per l'Interazione con BlueAgent

#### Opzione A — Snellimento Conservativo (Minimo impatto sul plugin CTFd)
Mantiene gli endpoint attuali (`/teams/{team_k}/machines`, `/teams/{team_k}/verificator`), ma:
1. **Sposta il motore di templating (`{{ip:name}}`, `{{subnet}}`, `{{team_k}}`, `{{verifier_ip}}`) dentro BlueAgent**, così che qualsiasi client possa inviare i comandi con i placeholder grezzi.
2. **Supporta query parameter in `DELETE /teams/{team_k}/machines?containers=web,db`** (mantenendo il body opzionale solo per retrocompatibilità), evitando l'obbligo di inviare un body JSON sulla `DELETE`.
3. **Auto-provisioning / Auto-healing del bridge del team:** se `deploy_challenge` viene chiamato per un `team_k` il cui bridge non è attivo (o non esiste), può opzionalmente inizializzarlo/riattivarlo senza fallire con `409`.

#### Opzione B — Redesign "Challenge Catalog" (BlueAgent diventa autonomo e più pulito)
Oltre ai miglioramenti dell'Opzione A, introduce in BlueAgent il concetto di **Catalogo Challenge** (`/challenges/{challenge_id}`), speculare al catalogo `/images/{alias}`:
1. **Registrazione della Challenge una tantum (`PUT /challenges/{challenge_id}`):**
   - L'organizzatore (o CTFd quando l'admin salva la challenge) registra la configurazione YAML/JSON della challenge su BlueAgent (`PUT /challenges/web-sqli`). BlueAgent valida subito i placeholder, verifica l'assenza di collisioni di `ip_suffix` e controlla che le immagini (`containers` + `verifier`) siano `ready`.
2. **Operazioni per Team ultraleggere (senza inviare ogni volta il JSON della challenge):**
   - `POST /teams/{team_k}/challenges/{challenge_id}/deploy` $\rightarrow$ avvia i container della challenge per il team `k` (creando automaticamente il team se non esiste).
   - `POST /teams/{team_k}/challenges/{challenge_id}/verify` $\rightarrow$ esegue la verifica OVN della challenge per il team `k`.
   - `DELETE /teams/{team_k}/challenges/{challenge_id}` $\rightarrow$ spegne ed elimina solo i container di quella challenge per il team `k` (senza alcun body nella `DELETE`!).
3. **Perché l'Opzione B rende BlueAgent molto più riutilizzabile:**
   - Chiunque voglia usare BlueAgent **senza CTFd** (es. da terminale, con una dashboard custom o in un corso universitario) può caricare le immagini (`/images/{alias}`), caricare le challenge (`/challenges/{id}`) e poi lanciare deploy/verify con una singola chiamata REST senza payload!
   - È possibile mantenere attivi anche i vecchi endpoint `/teams/{team_k}/machines` e `/verificator` come wrapper interni di 5 righe per non rompere nulla nel frattempo.

---

## 5. Stato di Implementazione e Verifica (18 Ottobre 2026)

Tutte le modifiche pianificate sono state implementate, verificate e committate nel repository Git (`/home/debian/bluectfd`):

| Sezione / Punto | Descrizione | Stato | File Coinvolti |
| :--- | :--- | :--- | :--- |
| **Punto 3: Pulizia & Debloat** | Rimozione dead code, unificazione `PeerTelemetry`, deduplicazione `DeployResponse.containers`, semplificazione WireGuard keys. | **COMPLETATO** | `models.py`, `wireguard.py`, `teams.py`, `ip.py`, `ovn.py` |
| **Punto 2: Prestazioni & I/O** | `SubprocessRunner` in memoria RAM (zero disk I/O su `/tmp`), `capture_output: bool = True` su Incus exec (da 6 a 2 roundtrips HTTP), parallelizzazione deployment e verifiche OVN CoW con `asyncio.gather()`. | **COMPLETATO** | `_runner.py`, `engine/incus.py`, `services/challenges.py`, `verifier/ovn.py` |
| **Punto 1: Hardening L1–L6** | Riconciliazione automatica stato kernel/DB al boot in `main.py`, concurrency guard OVN con `is_verify_locked`, zero cloni zombie, determinismo verify, dynamic `ipv4.nat`, isolamento stato lock. | **COMPLETATO** | `main.py`, `lifecycle/manager.py`, `verifier/ovn.py`, `models.py`, `locks.py` |
| **Punto 4: Interazione Client** | 4.1 Template rendering nativo in BlueAgent (`{{team_k}}`, `{{subnet}}`, `{{verifier_ip}}`, `{{ip:<name>}}`); 4.2 Query parameter support in `DELETE /teams/{team_k}/machines?containers=web,db` e teardown completo senza body. (4.3 escluso come da vincolo utente). | **COMPLETATO** | `models.py`, `services/challenges.py`, `api/challenges.py` |
| **Infrastruttura & Servizi** | Rilevamento dinamico dell'IP da `enp0s3` in `start_services.sh`. | **COMPLETATO** | `start_services.sh` |

### Esito Test Suite
- **111 / 111 unit test passati** con successo (`pytest tests/test_*.py -v`).
- Nuovi test creati e inclusi nella suite: `tests/test_p1_bugfixes.py` e `tests/test_p4_improvements.py`.

