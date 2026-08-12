**CTFBox ha troppe funzionalita**: non conviene usarlo, le logiche sono gia in CTFd sarebbe ridondante.

**Studiare CTFBox**: 
* Incus LXD
* `config.json` per la limitazione delle risorse
* gestione rete: il meccanismo freeze/lock/unlock di CTFBox limita dinamicamente l'accesso alle macchine.

**CTFd-Whale**: fa esattamente quello che voglio io.
* **sfide Jeopardy**: isolamento per singolo utente

# CTFBox
## rete
* **sottorete**: `10.0.0.0/8`
* **assegnazione ip**: `10.80.team_id.0/24`
* **cloud router**: gestisce il traffico, e applica regole SNAT. I pachetti verso le VM hanno ip S(NAT)orgente `10.254.0.1`
* **~~stati della rete~~**: 
	* **freeze**: posso solo comunicare col Game Server
	* **lock**: rete bloccata verso l'esterno, posso accedere alla VM per configurare le difese
	* **unlock**: rete aperta, posso attaccare

## vm
* **incus (LXD)**: dentro l'immagine docker. mitiga il container escape.
* **accesso**: tramite `root` con password token assegnato al team
* `config.json`: limiti hardware per il container

## scoring
**tick**: ogni 2 minuti, il game system fa queste azioni per verificare se il servizio e' UP
* Check SLA: ossia verifica disponibilita
* Put Flag: inserisci flag
* Get Flag: recupera flag

**punteggio finale**: e' calcolato
* sommando i punti ottenuti per ogni servizio
* moltiplicare il totale per il SLA
	* **ossia**: sul totale dei **tick**, quante volte il servizio era online?

**Inviare flag**: posso inviare una flag per tick (una flag ogni 2 minuti)


# codice
## `/router`
`entry.sh`: e' l'entry point, eseguito all'avvio del container docker.
* iptables: gestione routing/nat.
* **http**: intercetta il traffico per la gestione della socreboard.
* `TEAM_IDS`: variabile d'ambiente con i team. Per ogni team inizializza la sottorete.
* `confgen.py`: genera i certificati WireGuard per tutti i giocatori. Avvia `wg0` ed assegna gli ip necessari.
* `tc`: **traffic control**. Usa la variabile globale `RATE_NET` per impostare la larghezza di banda verso le VM vulnerabili.

`ctfroute.sh`: e' un binario installato come `/usr/sbin/ctfroute`.
* applica le regole `lock`, `unlock` e `freeze`

`ctroute-handle.sh`: viene chiamato ad ogni socket creata per leggere i comandi `lock`, `unlock` e `freeze`

`confgen.py`: genera i file configurazione WireGuard per ogni squadra e la configurazione `wg0.conf` del router
* `pins.json` : file con le credenziali per la distribuzione.

`docker file`: descrive la crezione del **docker del router**
* usa `apline:latest`
* installa le dipendenze
* copia gli script al suo interno.

## `/vm`
Contiene il necessario per avviare le macchine vulnerabili, la costruzione avviene in due fasi:
* `pre-build`: comune a tutti
* `entry`

`entry.sh`: script principale di avvio della `vm`, opera in due modalita
* `prebuild`: invocata alla creazione dell'immagine.Avvia il demone docker

> *Avvia il demone Docker interno, cerca tutte le sottocartelle nella directory `/root/` (dove si trovano i servizi vulnerabili) e, se trova un file `compose.yml`, esegue `docker compose build`. In questo modo, le immagini Docker dei servizi vengono create e memorizzate all'interno dell'immagine base della VM, risparmiando tempo prezioso.*

* `entry`: momento in cui parte la vm per i team nella gara.
	* esegue `predeploy.sh` per generare password e SECRET_KEY
	* `docker compose up -d` avviare effettivamente i servizi vulnerabili

`build.sh`: installa i pacchetti di sistema necessari. configura ssh, configura sudoers
* crea il file di servizio `systemd` che lancia `entry.sh`, rinominato in `_entry_vm_init

> [!error] `entry.sh` ed `_entry_vm_init`
> `entry.sh` viene rinominato in `_entry_vm_init` all'esecuzione.

`dockerfile.prebuilder`: cre l'immagine base, indipendentemente dal team.
* Ubuntu
* Esegue `build.sh` per installare i servizi e i pacchetti essenziali
* Copia `services` in `/root/`
* `ENTRYPOINY` e' `entry.sh` con agomento `prebuild` *innescando così la compilazione di tutte le immagini Docker dei servizi, rendendo questa immagine "pesante" ma pronta all'uso.*

`Dockerfile`: definisce l'immagine finale per ogni team, pre-costruita a parira da `Dockerfile.prebuilder`.
* inserisce la configurazione WireGuard per quel team e la abilita all'avvio
* rigenera chiavi ssh, ogni team ha le sue, uniche.
* utilizza docker secrets per impostare password `root` 
* avvia `/sbin/init -> systemd`

`services/`: contiene le ***applicazioni vulnerabili***
* `compose.yml`: ogni servizio ha il suo `compose.yml`, **indica come deve essere avviato**.


## `/incus`
**demone incus**: e' un fork di LXD, crea ambiente isolato dentro docker per eseguire in sicurezza le  "macchine virtuali" dei giocatori.
* ambiente isolato 
* **docker privilegiati**: sono vulnerabili, e' possibile uscire dall'ambiente sandbox.

`start.sh`: script principale che svolge
* **Gestione ciclo di vita**: registra i segnali (es: `SIGTERM`) per spegnere **"dolcemente" (graceful shutdown)** tutte le macchine virtuali dei team e il demone Incus stesso prima che il container venga arrestato
* **Avvio Demoni**: lancia in background `lxcfs` (virtualizzazione filesystem), `system-udevd` (gestione device) e `incusd`
* **Rete e NAT**: forwarding tra container e `incusbr0` ossia la rete interna della VM
* **Setup e ripristino**: per inizializzare `incus`
	* `/var/lib/incus/ready`: inizializza `incus` leggendo `incus.yml` e crea la VM
> *Se è la prima esecuzione (cioè non esiste il file `/var/lib/incus/ready`), inizializza Incus iniettando il file di configurazione `incus.yml` ed esegue lo script Python per la creazione delle VM. Se il container era già stato avviato in passato, fa partire direttamente le VM preesistenti.*

`customize-vm.py`:
1. **creazione** `base-vm`:  Genera una singola macchina virtuale di partenza (basata su un'immagine `ubuntu:noble`). Una volta avviata, tramite i comandi API di incus (`incus file push` e `incus exec`), le inietta dentro gli script `build.sh`, `entry.sh` e la cartella con le applicazioni vulnerabili (`services/`). Lancia quindi la modalità _prebuild_ (che compila le app), spegne la VM e la prepara per la clonazione.
2. **Clonazione Parallela**: Sfruttando un pool multi-processo, crea "cloni" rapidi (grazie al filesystem BTRFS) della `base-vm`, uno per ogni team partecipante. A ciascun clone (es. `vm1`, `vm2`...):
    - Assegna precisi limiti di RAM, CPU e un pool di archiviazione disco dedicato (per evitare che i team esauriscano le risorse degli altri o del server).
    - Inserisce all'interno le configurazioni WireGuard personali, rigenera le chiavi SSH e imposta la password di root di quel team.
3. Avvia le macchine in parallelo.

`Dockerifle`: definisce l'immagine docker per incus.
- Usa `debian:stable-slim` come base.
- Configura variabili d'ambiente per localizzare i binari e le librerie corrette di Incus.
- Finge la presenza del comando `systemctl` (creando un file fittizio che risponde sempre 0) per ingannare alcune dipendenze.
- Installa le repository ufficiali di "Zabbly" (chi fornisce le build stabili per Incus su Debian/Ubuntu).
- Scarica tutti gli strumenti necessari per la virtualizzazione e lo storage: `incus`, `btrfs-progs`, utilità di rete, `nftables` / `iptables`, e Python 3 (per lo script di automazione visto sopra).
- Imposta `/start.sh` come Entrypoint.