# Revisione Accademica della Tesi di Laurea Magistrale

**Candidato:** Davide L.  
**Oggetto:** Revisione strutturale, contenutistica e stilistica della tesi su *BlueAgent*  
**Ruolo:** Relatore di Tesi  
**Data:** 17 Ottobre 2026  
**Stato del Documento:** Bozza di Revisione Completa  

---

## 1. Valutazione Generale del Relatore (Executive Summary)

Caro Davide,

ho esaminato con molta attenzione l'intero manoscritto della tua tesi capitolo per capitolo, confrontandolo con la base di codice e i test operativi eseguiti sulla piattaforma.

### I Punti di Forza (La Qualità Ingegneristica)
L'impianto tecnico della tesi è di **altissimo livello ingegneristico**. La scelta di coniugare system containers via **Incus**, **ZFS** con Copy-on-Write (CoW) a basso costo per il provisioning istantaneo, **OVN** per creare una rete di verifica trasparente priva di conflitti di routing L3 con la produzione, e il firewalling deterministico tramite **nftables** dimostra una profonda padronanza dei sistemi operativi e del networking Linux. Il lavoro su **BlueAgent** e la sua integrazione nativa con **CTFd** costituiscono un contributo originale e concreto nel panorama dei Cyber Range per competizioni difensive.

### Le Criticità Principali da Risolvere
Sul piano della **stesura della tesi accademica**, tuttavia, emergono lacune e disomogeneità che rischierebbero di penalizzare severamente il tuo voto di laurea se presentate alla commissione:

1. **Disomogeneità marcata tra i capitoli:**
   - Alcune parti sono scritte con grande perizia tecnica (es. il Capitolo 4 e la sezione 5.2).
   - Altre sezioni fondamentali sono purtroppo ridotte a meri appunti o risultano letteralmente vuote:
     - Il **Capitolo 1 (Introduzione)** è lungo appena 11 righe e termina con un appunto in maiuscolo.
     - La sezione **5.3 (Plugin CTFd)** contiene unicamente la parola `TODO` (mentre nel codice hai sviluppato un plugin completo ed eccellente!).
     - La sottosezione **5.4.4 (Filesystem alternativi BTRFS)** è priva di testo.
     - La sezione **2.5 (CyberPatriot)** è un frammento di sole 6 righe con il titolo errato (*CyberPatrion*).
2. **Residui di bozza e placeholder inaccettabili in commissione:**
   - Nel testo sono rimaste tracce palesi di appunti interni, come *«Nella figura sborgz viene analizzato...»* (sezione 2.3), *«Di seguito, nell'immagine sburgoz, viene mostrata...»* (sezione 2.4), e promemoria di sviluppo in linea come `REVISION OBIETTIVO` o `ATTENZIONE: anche la generazione delle immagini...`.
3. **Numerazione dei capitoli e delle sezioni disallineata:**
   - Nel Capitolo 3 le intestazioni Markdown riportano ancora la numerazione precedente (es. `# 2.3 Use Cases...`, `# 2.4 Requisiti...`, `# 1.2 Oracoli...`).
   - Nell'Appendice (Capitolo 7) i file sono intitolati `5.1`, `5.2`, `5.3`, `5.4` con salti di numerazione interni (mancano 5.1.3 e 5.3.2).
   - Nei casi d'uso (UC) sono state commentate intere sezioni generando salti numerici (da UC-03 si salta a UC-06, poi a UC-08, poi a UC-12).
4. **Registro linguistico ed errori ortografici ricorrenti:**
   - **Accenti ed apostrofi:** l'uso sistematico dell'apostrofo al posto dell'accento grave (`e'` invece di `è`, `piu'` invece di `più`, `poiche'` invece di `poiché`, `perche'` invece di `perché`). Nelle tesi universitarie italiane questo è considerato un grave errore di forma tipografica.
   - **Troncamenti con apostrofo indebito:** frequente apostrofo davanti a sostantivi maschili (es. *un'orchestratore*, *un'ambiente*, *un'insieme*, *un'ottimo*, *un'indirizzo*, *un'altro*). L'articolo indeterminativo maschile *un* non vuole MAI l'apostrofo.
   - **Tono colloquiale:** espressioni gergali da eliminare (*«La rete production-k e' fatta cosi»*, *«ci pensa il kernel»*, *«appesantiamo il carico»*, *«banalmente»*).

Di seguito trovi l'analisi chirurgica capitolo per capitolo, con le indicazioni puntuali e gli esempi pratici "Prima / Dopo" da applicare per portare il testo all'eccellenza accademica.

---

## 2. Tabella di Priorità degli Interventi

| Priorità | File / Sezione | Natura del Problema | Azione Correttiva Richiesta |
| :--- | :--- | :--- | :--- |
| **P1 - Bloccante** | `5.3_CTFd.md` | Sezione `TODO` (3 righe) | Redigere l'intero capitolo sul plugin CTFd (architettura, blueprint, API, WireGuard sync). |
| **P1 - Bloccante** | `1_Introduzione.md` | Abbozzo incompiuto (11 righe) | Espandere a 3-5 pagine secondo la struttura standard accademica (schema fornito sotto). |
| **P1 - Bloccante** | `2.3_CyTrONE.md`, `2.4_CyberRangeCZ.md` | Placeholder `sborgz` e `sburgoz` | Sostituire con riferimenti formali a figure numerate o schemi architetturali. |
| **P1 - Bloccante** | `2.5_CR_CyberPatrion.md` | Titolo errato (*CyberPatrion*), 6 righe, frase tronca | Rinominare in *CyberPatriot*, completare l'analisi con citazione e tabella comparativa. |
| **P2 - Strutturale** | `3.2_Use_Cases.md`, `3.3_Requisiti.md`, `3.4_Meccanismi.md` | Titoli numerati erroneamente (`2.3`, `2.4`, `1.2`) | Rinumerare coerentemente (`3.2`, `3.3`, `3.4`) e riordinare la sequenza UC. |
| **P2 - Strutturale** | `2.2_CR_Alternativi_CTFBox.md` | Mancanza della tabella comparativa | Aggiungere la tabella di confronto con BlueAgent (uniformità con kCTF, CyTrONE, CR-CZ). |
| **P2 - Strutturale** | `2.1_CR_Alternativi_kctf.md` | Didascalia errata a riga 75 | Correggere: la tabella confronta *kCTF e BlueAgent*, non *NsJail*. |
| **P2 - Strutturale** | `5.4.4` (in `5.4_Validazione.md`) | Sottosezione vuota su BTRFS | Scrivere l'analisi comparativa tra ZFS CoW e BTRFS snapshot. |
| **P2 - Strutturale** | `6._Architetture...` | Capitolo privo di introduzione e tabella di sintesi | Introdurre il razionale delle alternative scartate e inserire matrice comparativa finale. |
| **P2 - Strutturale** | `7._Appendice/` | Numerazione file `5.x`, salti numerici, link rotto `![[Pasted...]]` | Rinumerare in `7.x` (o Appendice A), correggere salti e sostituire immagine mancante. |
| **P3 - Formale** | Tutti i file | Refusi ortografici, accenti (`e'` -> `è`), troncamenti errati | Revisione globale dell'italiano formale e bibliografia BibTeX. |

---

## 3. Revisione Dettagliata Capitolo per Capitolo

### Capitolo 1: Introduzione (`1._Introduzione/1_Introduzione.md`)

#### Diagnosi
Il testo attuale conta solo 11 righe e si interrompe con:
> `INSERIRE RISULTATI OTTENUTI e METODOLOGIA USATA`

In una tesi di laurea magistrale, l'Introduzione è il capitolo più letto dai membri della commissione e dai controrelatori. Deve presentare in modo ineccepibile il problema scientifico, le sfide tecnologiche, i contributi originali e l'organizzazione dell'opera.

#### Struttura Accademica Obbligatoria da Adottare
1. **1.1 Scenario e Motivazione:** L'evoluzione degli attacchi cyber; transizione dalle CTF puramente offensive (Jeopardy/Attack-Only) alle competizioni realistiche di difesa e Blue Teaming; importanza della formazione pratica con Cyber Range.
2. **1.2 La Definizione del Problema:** I Cyber Range attuali basati su VM complete (OpenStack, VirtualBox) sono pesanti, lenti nel deployment e scalano difficilmente su hardware modesto. Le soluzioni basate su container tradizionali (Docker/kCTF) sono orientate a singoli processi isolati (NsJail) e mal si adattano a sistemi complessi multi-servizio (system container con init system completo).
3. **1.3 La Sfida dell'Oracolo di Verifica:** Come testare la presenza di una vulnerabilità o la validità di una patch senza permettere ai partecipanti di catturare il traffico di verifica dell'Oracolo (sniffing) e senza causare collisioni di routing L3 tra ambienti duplicati.
4. **1.4 La Soluzione Proposta: BlueAgent:** Presentazione dell'architettura (Debian 13, Incus, ZFS CoW, OVN SDN, nftables, plugin CTFd).
5. **1.5 Risultati Chiave Ottenuti:** Tempi di provisioning quasi istantanei grazie agli snapshot ZFS CoW, isolamento crittografico via WireGuard con un tunnel dedicato per team, trasparenza totale della rete di verifica.
6. **1.6 Organizzazione della Tesi:** Breve roadmap capitolo per capitolo.

#### Esempio Concreto di Miglioramento

*Prima (dal tuo testo):*
> Nel lavoro di tesi vogliamo gestire una competizione CTF (Capture The Flag).
> [...] Abbiamo dunque sviluppato *BlueAgent*, un'orchestratore di sistemi vulnerabili basato sulla tecnologia dei container che implementa il meccanismo di verifica...

*Dopo (Proposta per la tesi):*
> Il presente lavoro di tesi affronta la progettazione e la realizzazione di un'infrastruttura Cyber Range avanzata orientata a competizioni di sicurezza informatica di tipo *Defensive* Capture The Flag (CTF). Nelle tradizionali competizioni CTF di stampo offensivo, l'obiettivo dei partecipanti consiste nello sfruttare vulnerabilità al fine di sottrarre sequenze segrete (*flag*). Al contrario, negli scenari difensivi (*Blue Teaming*), i team sono chiamati a identificare falle di sicurezza, applicare contromisure efficaci (*patching*) e garantire contemporaneamente la disponibilità e l'integrità dei servizi applicativi simulati.
> 
> Per soddisfare tali requisiti, è stato sviluppato **BlueAgent**, un orchestratore specializzato di ambienti vulnerabili che impiega *system container* orchestrati tramite Incus, uno storage pool ZFS basato su semantica Copy-on-Write (CoW) per il provisioning rapido delle istanze, e una Software-Defined Network (SDN) gestita mediante Open Virtual Network (OVN). L'architettura assicura l'invisibilità totale degli oracoli di verifica rispetto al traffico dei concorrenti e previene conflitti di instradamento dovuti alla sovrapposizione degli indirizzi IP tra gli ambienti di produzione e di verifica.

---

### Capitolo 2: Contesto e Confronto con lo Stato dell'Arte (`2._Contesto...`)

#### 2.0 Introduzione allo Stato dell'Arte (`2_Cyber_Range_Lo_Stato_Dell_Arte.md`)
- **Criticità:** La riga 1 contiene un'annotazione di bozza:
  `REVISION OBIETTIVO: le comparazioni non devono essere superficiali, ma precise! Spiegare in cosa differiscono sia al livello architetturale ma anche applicativo.`
- **Azione:** Eliminare la riga e trasformarla in un paragrafo che definisce le dimensioni di benchmarking utilizzate per confrontare le soluzioni:
  1. *Unità di isolamento:* Full VM vs Application Container vs System Container.
  2. *Tipo di scenario:* Jeopardy offensiva vs Blue Team difensivo.
  3. *Meccanismo di verifica:* statico vs dinamico/oracolo trasparente.
  4. *Overhead computazionale e provisioning time.*

#### 2.1 kCTF (`2.1_CR_Alternativi_kctf.md`)
- **Criticità 1:** A riga 75 la didascalia recita:
  `Tabella comparativa tra kCTF ed NsJail`
  Questo è un errore materiale: la tabella confronta chiaramente **kCTF** e **BlueAgent**!
  *Correzione:* Sostituire con `Tabella comparativa tra kCTF e BlueAgent`.
- **Criticità 2:** Refuso a riga 60: `Tutta via` -> correggere in `Tuttavia`.

#### 2.2 CTFBox (`2.2_CR_Alternativi_CTFBox.md`)
- **Criticità:** È descritto molto bene, ma è l'unico sistema dello stato dell'arte a **non avere una tabella comparativa finale**.
- **Azione:** Aggiungere in fondo alla sezione la seguente tabella strutturata:

```markdown
### Tabella Comparativa: CTFBox vs BlueAgent

| Caratteristica | CTFBox | BlueAgent |
| :--- | :--- | :--- |
| **Modello di Esecuzione** | Application Container (Docker) | System Container (Incus) |
| **Init System nel Container** | Assente (singolo processo) | Completo (PID 1 con systemd reale) |
| **Ambiente di Gioco** | Single-container isolato | Multi-container collegati in LAN virtuale |
| **Meccanismo di Verifica** | Container di verifica condiviso | Rete OVN isolata con cloni CoW atomici |
| **Protezione dell'Oracolo** | Esposto a intercettazione L2 | Totalmente invisibile (SDN L3 separata) |
| **Accesso Partecipanti** | Port mapping / Reverse Proxy | Tunnel cifrato WireGuard deterministico |
| **Target Competitivo** | Attack & Defense tradizionale | Defensive Blue Teaming & Patch Verification |
```

- **Refusi nel testo:**
  - `conettersi` -> `connettersi`
  - `un'indirizzo` -> `un indirizzo` (maschile!)
  - `si rileva essere un'ottimo` -> `si rivela essere un ottimo` (maschile!)

#### 2.3 CyTrONE (`2.3_CR_Alternativi_CyTrONE.md`)
- **Criticità Bloccante:** A riga 61 compare:
  `Nella figura sborgz viene analizzato...`
  Questo termine inventato come segnaposto è una svista critica.
- **Azione:** Sostituire la frase con un riferimento formale:
  *Prima:* `Nella figura sborgz viene analizzato il flusso di deploy di CyTrONE.`
  *Dopo:* `Nella Figura \ref{fig:cytrone_arch} viene illustrato il flusso di deployment e instradamento delle risorse adottato da CyTrONE.`
- **Refusi nel testo:**
  - `d icaricare` -> `di caricare`
  - `conentra` -> `concentra`
  - `vulnearbilita` -> `vulnerabilità`
  - `traninig` -> `training`

#### 2.4 CyberRangeCZ (`2.4_CR_CyberRangeCZ.md`)
- **Criticità Bloccante:** A riga 31 compare:
  `Di seguito, nell'immagine sburgoz, viene mostrata...`
  Altra occorrenza di segnaposto provvisorio.
- **Azione:** Sostituire con `Nella Figura \ref{fig:cyberrangecz_arch} viene schematizzata l'infrastruttura a microservizi di CyberRangeCZ.`
- **Refusi nel testo:**
  - `decsrive` -> `descrive`
  - `instanze` -> `istanze`
  - `distirbuzione` -> `distribuzione`
  - `Sandobx` -> `Sandbox`
  - `microservizzi` -> `microservizi`

#### 2.5 CyberPatriot (`2.5_CR_CyberPatrion.md`)
- **Criticità Bloccante:** 
  1. Il nome nel titolo e nel file è sbagliato: `CyberPatrion` anziché **CyberPatriot**.
  2. Il testo consta di sole 6 righe ed è palesemente incompleto.
  3. A riga 3 compare una frase sconnessa: *«I team assumono giocano il ruolo...»*.
  4. Manca qualsiasi citazione formale e manca la tabella comparativa.
- **Azione:** Correggere e ampliare.
- **Bozza raccomandata per la riscrittura:**

```markdown
# 2.5 CyberPatriot

**CyberPatriot** [^cyberpatriot_ref] è un programma di formazione e competizione cyber difensiva ideato dall'Air & Space Forces Association (AFA) statunitense, rivolto primariamente a studenti delle scuole superiori e università. A differenza dei formati CTF convenzionali orientati allo sfruttamento offensivo, CyberPatriot è interamente focalizzato sulla sicurezza difensiva (*hardening* dei sistemi operativi e mitigazione delle vulnerabilità).

Nello scenario tipico di CyberPatriot, ciascun team riceve una o più macchine virtuali complete pre-configurate (basate su distribuzioni Windows Server/Desktop o Linux), volutamente affette da molteplici difetti di sicurezza: account non autorizzati, policy di password permissive, servizi di rete non necessari in esecuzione, permessi errati sul filesystem e malware dormiente. I partecipanti operano come amministratori di sistema ("Blue Team"), con il compito di individuare e correggere tali falle entro una finestra temporale prefissata, mantenendo al contempo operativi i servizi critici per il business.

La valutazione delle prestazioni avviene mediante un motore di scoring proprietario (denominato *CyberPatriot Scoring Engine*), installato localmente all'interno di ciascuna immagine virtuale sotto forma di servizio o demone. Il motore interroga periodicamente lo stato del sistema (registro di sistema, file di configurazione, utenti attivi) e attribuisce punti non appena una specifica contromisura viene applicata, inviando il punteggio a un server centrale.

### Tabella Comparativa: CyberPatriot vs BlueAgent

| Caratteristica | CyberPatriot | BlueAgent |
| :--- | :--- | :--- |
| **Unità di Virtualizzazione** | Macchine Virtuali complete (VMware / VirtualBox) | System Container leggeri (Incus) |
| **Consumo di Risorse** | Elevato (diversi GB di RAM per istanza VM) | Minimo (poche centinaia di MB per team) |
| **Ambiente di Rete** | VM isolata singola (raramente multi-nodo) | Topologia multi-container realistica in LAN |
| **Motore di Valutazione** | Agente locale dentro la macchina del giocatore | Oracolo esterno non rilevabile in rete SDN |
| **Resistenza al Manomissione** | Bassa (il partecipante può tentare il reverse dell'engine locale) | Totale (l'oracolo esegue in una rete OVN clonata) |
| **Integrazione Piattaforme** | Software client/server proprietario dedicato | Plugin nativo e open-source per CTFd |

[^cyberpatriot_ref]: Air & Space Forces Association, "CyberPatriot: The National Youth Cyber Education Program", https://www.uscyberpatriot.org
```

---

### Capitolo 3: BlueAgent (`3._BlueAgent/`)

#### 3.2 Casi d'Uso (`3.2_Use_Cases.md`)
- **Titolo da correggere:** L'intestazione è `# 2.3 Use Cases per CTF Manager`. Deve diventare:
  `# 3.2 Casi d'Uso di BlueAgent`
- **Casi d'Uso commentati e salti numerici:**
  Nel file sono presenti blocchi commentati con tag HTML:
  - `<!-- ## UC-04: Modifica Flag -->`
  - `<!-- ## UC-05: Modifica Configurazione di Rete -->`
  - `<!-- ## UC-07: Accesso ai Log di Verifica -->`
  - `<!-- ## UC-09 ... UC-11 ... UC-13 -->`
  Di conseguenza la sequenza dei casi d'uso visibili diventa: **UC-01, UC-02, UC-03, UC-06, UC-08, UC-12**.
- **Azione:** In una tesi non devono esserci salti arbitrari nei diagrammi o nelle tabelle di specifica dei requisiti. Se i casi d'uso sono stati scartati, eliminali definitivamente dal sorgente e **rinumera sequenzialmente da UC-01 a UC-06**; se invece descrivono funzionalità del sistema BlueAgent/CTFd (come l'accesso ai log di verifica o la gestione delle chiavi), de-commentali e integrali pienamente.

#### 3.3 Requisiti di Sistema (`3.3_Requisiti_Di_Sistema.md`)
- **Titolo da correggere:** L'intestazione è `# 2.4 Requisiti di Sistema` e `## 2.4.1 ...`. Deve diventare:
  `# 3.3 Requisiti di Sistema` e `## 3.3.1 ...`
- **Formalizzazione dei requisiti:** In Ingegneria del Software i requisiti si formalizzano mediante tabelle recanti un codice univoco, una descrizione succinta e il livello di priorità (MoSCoW: Must have, Should have, Could have).
- **Esempio pratico da inserire:**

```markdown
### Tabella 3.1: Requisiti Funzionali del Sistema

| ID | Nome Requisito | Descrizione | Priorità |
| :--- | :--- | :--- | :--- |
| **REQ-F-01** | Provisioning Istantaneo | Clonazione CoW dei container di challenge mediante ZFS in meno di 2 secondi. | *Must* |
| **REQ-F-02** | Accesso VPN Cifrato | Generazione e configurazione automatica di un'interfaccia WireGuard dedicata per team. | *Must* |
| **REQ-F-03** | Isolamento Multi-Tenant | Totale segregazione L2/L3 e di firewall tra le reti di team distinti. | *Must* |
| **REQ-F-04** | Verifica Atomica Non Invasiva | Replicazione dell'ambiente in una rete OVN effimera per l'esecuzione dell'exploit oracolo. | *Must* |
| **REQ-F-05** | Integrazione CTFd | Plugin con blueprint web per download config VPN e sottomissione verifica. | *Should* |
| **REQ-F-06** | Cleanup Automatico | Rilascio deterministico di container, storage e regole di rete alla scadenza o al termine. | *Must* |

### Tabella 3.2: Requisiti Non Funzionali

| ID | Ambito | Descrizione | Metrica di Riferimento |
| :--- | :--- | :--- | :--- |
| **REQ-NF-01** | Prestazioni | Basso overhead di storage e memoria host | Overhead storage CoW < 50MB per clone |
| **REQ-NF-02** | Trasparenza | Impossibilità per i partecipanti di rilevare il traffico dell'oracolo | 0 pacchetti dell'oracolo visibili su `wg-k` |
| **REQ-NF-03** | Fedeltà | Ambienti compatibili con standard Linux completi | Supporto nativo a `systemd` nei container |
| **REQ-NF-04** | Sicurezza Host | Nessuna concessione di permessi di root sull'host ai concorrenti | Esecuzione container in namespace unprivileged |
```

#### 3.4 Meccanismi di Verifica ed Oracoli (`3.4_Meccanismi_di_Verifica.md`)
- **Titolo da correggere:** L'intestazione attuale è `# 1.2 Oracoli e Meccanismi di Verifica`. Deve diventare:
  `# 3.4 Meccanismi di Verifica ed Oracoli`
- **Refusi:**
  - `orcehstratore` -> `orchestratore`
  - `deve sia completamente trasparente` -> `deve essere completamente trasparente`
- **Miglioramento concettuale:** Aggiungere un diagramma di flusso logico o una sequenza numerata precisa che descriva il ciclo di vita della verifica:
  1. *Richiesta:* Il giocatore richiede la verifica tramite l'interfaccia web di CTFd.
  2. *Snapshot & Clone:* BlueAgent crea un clone CoW ZFS dello stato attuale dei container del team $k$.
  3. *Attestazione di Rete:* I cloni vengono connessi allo switch logico OVN della rete $\text{verify-}k$.
  4. *Esecuzione dell'Oracolo:* Il container/script dell'oracolo esegue l'exploit di test contro il clone.
  5. *Valutazione Verdetto:* Se l'exploit fallisce (la vulnerabilità è mitigata) e i controlli di integrità di servizio (*Service Health Check*) hanno successo, la flag viene rilasciata; altrimenti viene restituito errore.
  6. *Teardown:* Distruzione immediata della rete OVN e distruzione dei cloni ZFS.

---

### Capitolo 4: Architettura di Rete ad Alto Livello (`4._Architettura_Rete...`)

#### 4.1 Rete di Produzione e 4.2 Rete di Verifica (`4_Architettura_Rete.md`)
- **Organizzazione file:** Nel repository hai `4_Architettura_Rete.md` (che contiene internamente i paragrafi 4.1 e 4.2) e poi `4.3_Struttura_Challenge.md`. Questa struttura è corretta purché le intestazioni interne rimangano allineate.
- **Miglioramento del Registro Linguistico:**
  *Prima (riga 12):*
  > La rete production-k e' fatta cosi, contiene:
  > * wg-k: dispositivo L3 gestito da WireGuard...
  > * br-team-k: dispositivo L2 gestito dal kernel Linux...

  *Dopo (formale):*
  > La rete di produzione associata al team $k$-esimo ($\text{production-}k$) è progettata per offrire un ambiente isolato e raggiungibile esclusivamente dai membri autorizzati del team. Essa comprende le seguenti entità architetturali:
  > * **Interfaccia $\text{wg-}k$:** dispositivo virtuale di livello 3 gestito dal modulo kernel di WireGuard, che funge da punto di terminazione per il tunnel VPN cifrato dei concorrenti del team $k$, attestato con indirizzo gateway `10.k.0.1/24`.
  > * **Bridge $\text{br-team-}k$:** dispositivo di commutazione di livello 2 istanziato nel kernel Linux dell'host, che implementa il dominio di broadcast locale per i container della challenge del team, attestato su `10.k.1.1/24`.

  *Prima (riga 21):*
  > Dunque all'interno del kernel appesantiamo il carico nella gestione delle interfacce, infatti avremmo oltre ad eth0, una coppia veth per ogni container.

  *Dopo (formale):*
  > Questa architettura comporta la creazione di un numero di interfacce virtuali proporzionale al numero di container attivi: per ciascuna istanza, oltre all'interfaccia logica interna `eth0`, il kernel mantiene in memoria una coppia `veth`. Come documentato in letteratura [^1], l'overhead in termini di cicli CPU e consumo di memoria per la gestione delle strutture `net_device` delle coppie `veth` è trascurabile, consentendo la coesistenza di centinaia di link attivi senza degradazione percepibile del throughput.

- **Dettaglio essenziale da evidenziare:** La sezione 4.2 sul **doppio stadio di NAT** (SNAT OVN verso `incusbr0` a `172.16.0.x` + Masquerading nftables verso l'esterno) è **uno dei passaggi più brillanti della tesi**. Spiegalo con estrema chiarezza, perché risolve l'annoso problema dei pacchetti di risposta WAN che altrimenti verrebbero instradati erroneamente sulla rete di produzione anziché su quella di verifica.

---

### Capitolo 5: Architettura nel Dettaglio e Validazione (`5._Architettura...`)

#### 5.1 Architettura del Codice (`5.1_Architettura_Codice.md`)
- **Avviso interno da rimuovere (riga 17):**
  `> **ATTENZIONE: anche la generazione delle immagini dovrebbe avvenire tramite interfaccia**`
  Questo è un promemoria di sviluppo e non deve assolutamente comparire nella tesi finale.
- **Componente commentato (righe 78-86):**
  Nel markdown la riga del `LifecycleManager` è stata commentata all'interno della tabella dei moduli.
  Il `LifecycleManager` gestisce compiti vitali (scadenza ambienti, timeout verifiche, bonifica zombie). Rimuovi il commento e documentane formalmente il ruolo.

#### 5.3 Il Plugin CTFd (`5.3_CTFd.md`)
- **Criticità Massima:** Il file contiene letteralmente:
  ```markdown
  # 5.3 Plugin CTFd
  
  TODO
  ```
  Questo è un vuoto inaccettabile, soprattutto considerando che hai già scritto il codice funzionante del plugin in `CTFd/CTFd/plugins/blueagent/`!
- **Azione:** Inserire la trattazione approfondita del plugin CTFd.
- **Bozza completa pronta per essere integrata:**

```markdown
# 5.3 Il Plugin di Integrazione per CTFd

Per consentire ai partecipanti e agli amministratori della competizione di interagire in modo intuitivo e trasparente con le funzionalità di BlueAgent, è stato sviluppato un plugin nativo per la piattaforma **CTFd** (il framework open-source di riferimento per l'organizzazione di competizioni CTF).

Il plugin, integrato nella directory `CTFd/plugins/blueagent`, estende sia il pannello di controllo per gli organizzatori sia l'interfaccia utente visibile ai concorrenti durante la gara.

### 5.3.1 Architettura del Plugin e Blueprint Flask
CTFd è basato sul microframework web Flask e sull'ORM SQLAlchemy. Il plugin BlueAgent sfrutta il sistema di estensioni modulari di CTFd registrando un apposito **Flask Blueprint**:

1. **Gestione del Modello Dati:** Vengono introdotte tabelle dedicate nel database relazionale di CTFd per mappare le associazioni tra `team_id`, chiavi pubbliche WireGuard, stato dell'ambiente (`STOPPED`, `STARTING`, `RUNNING`, `VERIFYING`) e storico delle sottomissioni di verifica.
2. **Comunicazione con l'Agente:** Il plugin agisce come client REST asincrono nei confronti di BlueAgent (in esecuzione su porta locale o su nodo dedicato all'indirizzo `:8000`). La comunicazione è autenticata tramite bearer token condiviso per prevenire accessi non autorizzati all'API di orchestrazione.

### 5.3.2 Funzionalità per i Partecipanti
Nella vista di ciascuna challenge difensiva, il plugin inietta dinamicamente componenti d'interfaccia dedicati:
* **Download della Configurazione VPN:** Il giocatore può scaricare con un singolo clic il proprio file di configurazione WireGuard (`bluectfd_team_K.conf`), contenente la chiave privata generata, l'indirizzo IP assegnato nella subnet `10.k.0.0/24` e l'endpoint pubblico del server.
* **Stato dell'Infrastruttura:** Viene esposto lo stato di salute dei container assegnati al team (indirizzi IP interni della LAN `10.k.1.0/24` e porte dei servizi).
* **Pulsante di Verifica della Patch ("Verifica Difesa"):** Quando il team ritiene di aver mitigato con successo la vulnerabilità senza compromettere l'erogazione del servizio, inoltra una richiesta di verifica. L'interfaccia disabilita il pulsante per prevenire race conditions o tentativi di flood (rate limiting) e notifica l'avvio della pipeline di collaudo.
* **Polling e Visualizzazione del Verdetto:** Il browser effettua interrogazioni periodiche sullo stato del job di verifica. Al termine dell'oracolo:
  - In caso di esito positivo (vulnerabilità non più sfruttabile e check funzionali superati), il server accredita automaticamente i punti e visualizza la flag ottenuta.
  - In caso di fallimento, viene mostrato un messaggio diagnostico conciso (es. *"Servizio inaccessibile"* o *"Vulnerabilità ancora sfruttabile"*), evitando di fornire dettagli che possano fungere da oracolo informativo indesiderato per i concorrenti.

### 5.3.3 Funzionalità di Amministrazione
Dall'interfaccia di amministrazione di CTFd, i manager della gara possono:
* Monitorare il carico del server e il numero di container Incus attivi in tempo reale.
* Forzare il riavvio o la terminazione delle istanze di un team in caso di stallo.
* Visualizzare i log di esecuzione degli oracoli per verificare eventuali contestazioni durante o dopo la competizione.
```

#### 5.4 Validazione (`5.4_Validazione.md`)
- **Sezione 5.4.4 vuota:** L'intestazione `5.4.4 Considerazioni su Filesystem Alternativi (BTRFS)` non contiene testo.
- **Azione:** Inserire un'analisi comparativa chiara tra ZFS e BTRFS:
  - *Perché BTRFS è stato valutato:* filesystem Copy-on-Write nativo nel mainline Linux Kernel (non richiede moduli out-of-tree / DKMS come ZFS).
  - *Perché ZFS è stato preferito per BlueAgent:* ZFS vanta una maturità notevolmente superiore nella gestione di storage pool complessi con quote e I/O concorrente; il supporto ZFS in Incus/LXD è di primo livello; i comandi di snapshot e clone (`zfs clone`, `zfs snapshot`) sono rigorosamente O(1) e non soffrono dei noti problemi di frammentazione estrema dello spazio libero e degradazione dei metadati tipici di BTRFS in scenari ad alto tasso di allocazione/cancellazione rapida.

#### 5.5 Difesa e Validazione di BlueAgent (`5.5_Difesa_Architettura.md`)
- **Tono e prospettiva:** Il capitolo si focalizza sui compromessi dell'architettura (MTU Blackhole UDP, limite a 254 team per singolo byte `10.k.x.x`, lock `flock` confinato al singolo nodo). Questo è un ottimo punto di maturità scientifica, ma il titolo "Difesa" suona improprio.
- **Miglioramento del Titolo:** Rinominare in:
  `# 5.5 Analisi dei Limiti Architetturali e Lavori Futuri`
- **Refusi nel testo:**
  - `un'ottima compatibilita tra` -> `un'ottima compatibilità tra`
  - `Si benefica da CoW` -> `Si beneficia del CoW`
  - `L'adozione di Incus e' dovuto` -> `L'adozione di Incus è dovuta`
  - `Il vantaggio piu grande che porta BlueAgent` -> `Il principale vantaggio introdotto da BlueAgent`
  - `notevoilmente` -> `notevolmente`
  - `renderelo` -> `renderlo`

---

### Capitolo 6: Architetture di Rete Alternative (`6._Architetture...`)

#### Diagnosi Complessiva del Capitolo
Questo capitolo dimostra un eccellente approccio ingegneristico: non ti sei limitato a presentare la soluzione scelta (OVN con Incus), ma hai analizzato sistematicamente quattro alternative scartate:
1. *Bridge L2 senza gateway* (`6.1`)
2. *Interfaccia wan1 aggiuntiva* (`6.2`)
3. *Network namespace separato per la verifica* (`6.3`)
4. *Router intermedio* (`6.4`)

Tuttavia, le quattro sezioni sono estremamente sintetiche (circa 10-15 righe ciascuna) e **mancano sia di un'introduzione generale sia di una tabella di confronto conclusiva**.

#### Azioni da Intraprendere:
1. **Creare un'introduzione al capitolo:** Spiegare chiaramente il vincolo fondamentale di design:
   > *«La sfida architetturale consiste nel duplicare l'infrastruttura di una challenge garantendo che i container clonati mantengano inalterati i loro indirizzi IP e la configurazione del gateway di default (per non alterare il comportamento dei payload dell'oracolo), senza generare conflitti di instradamento ARP e IP nell'host con la rete di produzione già attiva, e garantendo la connettività Internet per l'accesso a repository e servizi esterni.»*
2. **Inserire la Tabella Sinottica delle Alternative al termine del capitolo:**

```markdown
### Tabella Comparativa: Architetture di Rete a Confronto

| Criterio | 6.1 Bridge L2 senza GW | 6.2 Interfaccia wan1 | 6.3 NetNS Separato | 6.4 Router Intermedio | **BlueAgent (OVN SDN)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Fedeltà di Rete** | Bassa (nessun default GW) | Scadente (aggiunta interfaccia anomala) | Ottima (topologia identica) | Ottima (topologia identica) | **Eccellente (fedele al 100%)** |
| **Accesso WAN per l'Oracolo** | Assente | Presente (via wan1) | Presente (coppia veth verso root) | Presente (SNAT su router ausiliario) | **Presente (SNAT OVN a 2 stadi)** |
| **Collisioni IP con Produzione** | Nessuna | Nessuna | Nessuna | Nessuna | **Nessuna (SDN isolata)** |
| **Complessità Software** | Minima | Moderata (modifica routing container) | Elevata (gestione veth manuale e bypass Incus) | Medio-alta (orchestrazione container router) | **Minima in BlueAgent (delegata a Incus/OVN)** |
| **Overhead Risorse** | Quasi nullo | Basso | Basso | Medio (un container router per team) | **Basso (demoni OVN condivisi)** |
| **Verdetto Finale** | *Scartata* | *Scartata* | *Scartata* | *Scartata* | **Adottata come Soluzione Ottimale** |
```

- **Refusi nel testo del capitolo 6:**
  - `tutta via` (scritto staccato in 6.1 e 6.3) -> `tuttavia`
  - `solo un'unico bridge` -> `un unico bridge` (maschile!)
  - `poiche riesiedono` -> `poiché risiedono`
  - `tracciarene` -> `tracciarne`
  - `Questo perche' il motore di Incus esegue sul namespace root` -> `Questo perché il demone di Incus è eseguito nel namespace di rete root`

---

### Capitolo 7: Appendice (`7._Appendice/`)

#### Diagnosi Complessiva
L'Appendice contiene nozioni teoriche fondamentali (Networking Linux, WireGuard, ZFS, NsJail e Namespaces) che supportano la comprensione dei capitoli 4 e 5. Tuttavia presenta gravi disallineamenti di numerazione e impaginazione:

1. **Numerazione dei file e titoli errata:**
   - Il file `5.1_LinuxNetworking.md` ha titolo `# 5.1 Linux Networking`. Deve diventare:
     `# A.1 Linux Networking e Sottosistema Netfilter` (oppure `7.1`)
   - All'interno di `5.1_LinuxNetworking.md` si salta da `5.1.2 Bridge` direttamente a `# 5.1.4 Netfilter` (manca completamente il paragrafo 5.1.3!).
   - Il file `5.2_VPN_e_OVN.md` ha come titolo interno `# 7.2 WireGuard` e non contiene una sola riga su OVN!
   - Il file `5.3_ZFS.md` ha titolo `# 5.3 ZFS` e salta da `5.3.1` a `5.3.3` (manca il paragrafo 5.3.2!).
   - Il file `5.4_NsJail.md` ha titolo `# 5.4 NsJail e Container`.
2. **Link a immagini Obsidian non compilabili in LaTeX:**
   In `5.2_VPN_e_OVN.md` a riga 17 compare il tag grezzo di Obsidian:
   `![[Pasted image 20261001214515.png]]`
   Se questo file non esiste o non viene convertito da `convert_thesis.py`, la generazione del PDF finale fallisce o produce un box vuoto.
   *Azione:* Sostituire con un'immagine correttamente denominata in `src/images/wireguard_cryptokey.png` oppure con una tabella testuale/Mermaid della tabella cryptokey routing.
3. **Refusi nell'Appendice:**
   - In `5.4_NsJail.md`:
     - `un'altro insieme` -> `un altro insieme` (maschile!)
     - `isolazione` -> `isolamento`
   - In `5.1_LinuxNetworking.md`:
     - `cpnntrack` -> `conntrack`
     - `accountig` -> `accounting`
     - `effettaure` -> `effettuare`
     - `passagio da user spa ce a kernel space` -> `passaggio da user space a kernel space`

---

## 4. Guida di Stile e Tipografia Accademica

Per evitare penalizzazioni formali da parte della commissione di laurea, attieniti rigorosamente a queste tre regole fondamentali della lingua italiana scritta:

### 1. La Regola degli Accenti (No all'Apostrofo per gli Accenti)
In ambiente accademico, l'uso dell'apostrofo al posto dell'accento è considerato inaccettabile:
* **Sbagliato:** `e'`, `piu'`, `poiche'`, `perche'`, `gia'`, `puo'`, `affinche'`
* **Corretto:** `è`, `più`, `poiché`, `perché`, `già`, `può`, `affinché`

### 2. La Regola dell'Apostrofo: Troncamento vs Elisione
* **Troncamento (al maschile, MAI l'apostrofo):** L'articolo indeterminativo maschile è *un*. Non si apostrofa mai, nemmeno davanti a vocale!
  - **Sbagliato:** *un'orchestratore, un'ambiente, un'insieme, un'ottimo, un'indirizzo, un'altro, un'approccio.*
  - **Corretto:** *un orchestratore, un ambiente, un insieme, un ottimo, un indirizzo, un altro, un approccio.*
* **Elisione (al femminile, SEMPRE l'apostrofo):** L'articolo indeterminativo femminile è *una*, che davanti a vocale si elide in *un'*.
  - **Corretto:** *un'interfaccia, un'architettura, un'applicazione, un'estremità.*

### 3. Registro Linguistico Impersonale
Sostituisci la prima persona plurale (*«abbiamo sviluppato»*, *«vogliamo gestire»*, *«ci siamo chiesti»*) o le forme discorsive (*«fatta così»*, *«banalmente»*) con la terza persona impersonale e il passivo scientifico (*«è stato sviluppato»*, *«si propone di gestire»*, *«è opportuno osservare»*).

---

## 5. Piano Operativo di Revisione (Checklist)

Segui questo piano di lavoro ordinato per completare la tesi:

- [ ] **Fase 1: Eliminazione Segnaposto e Refusi Critici (30 min)**
  - [ ] Rimuovere `sborgz` da `2.3_CR_Alternativi_CyTrONE.md`.
  - [ ] Rimuovere `sburgoz` da `2.4_CR_CyberRangeCZ.md`.
  - [ ] Rimuovere `REVISION OBIETTIVO` da `2_Cyber_Range_Lo_Stato_Dell_Arte.md`.
  - [ ] Rimuovere il warning `ATTENZIONE:...` da `5.1_Architettura_Codice.md`.
  - [ ] Sostituire l'immagine incollata `Pasted image...` in `7._Appendice/5.2_VPN_e_OVN.md`.

- [ ] **Fase 2: Redazione delle Sezioni Mancanti (Priorità Assoluta) (2-3 ore)**
  - [ ] Scrivere interamente **Capitolo 1 (Introduzione)** partendo dalla traccia fornita nella Sezione 3.
  - [ ] Scrivere interamente la sezione **5.3 (Plugin CTFd)** utilizzando il codice in `CTFd/CTFd/plugins/blueagent/` e la bozza fornita.
  - [ ] Espandere la sezione **2.5** correggendo il titolo in **CyberPatriot**.
  - [ ] Completare la sottosezione **5.4.4 (Confronto ZFS vs BTRFS)** in `5.4_Validazione.md`.

- [ ] **Fase 3: Riorganizzazione Numerazione e Casi d'Uso (1 ora)**
  - [ ] Correggere le intestazioni nel Capitolo 3 (`3.2`, `3.3`, `3.4`).
  - [ ] Risolvere i casi d'uso commentati in `3.2_Use_Cases.md` e riordinare la numerazione sequenziale (UC-01 .. UC-06).
  - [ ] Rinumerare le sezioni dell'Appendice (Capitolo 7 / Appendice A) sanando i salti di numerazione interni.

- [ ] **Fase 4: Tabelle di Sintesi e Correzione Formale (1-2 ore)**
  - [ ] Inserire la tabella comparativa per CTFBox (`2.2`).
  - [ ] Correggere la didascalia della tabella in `2.1` (kCTF vs BlueAgent).
  - [ ] Inserire l'introduzione e la matrice comparativa finale nel Capitolo 6.
  - [ ] Eseguire una ricerca e sostituzione globale dei refusi ortografici (`e'` -> `è`, troncamenti maschili errati).

- [ ] **Fase 5: Compilazione e Verifica Finale**
  - [ ] Eseguire `./compile.sh` per verificare che la pipeline LaTeX generi il PDF senza errori né warning di collegamenti orfani.
  - [ ] Controllare l'indice generale (*Table of Contents*) nel PDF finale per assicurarsi della perfetta continuità gerarchica.

---
*Buon lavoro, Davide. L'architettura software e di rete che hai realizzato ha un valore ingegneristico notevole: con questi interventi redazionali, la tua tesi rifletterà appieno l'eccellenza del lavoro pratico svolto.*
