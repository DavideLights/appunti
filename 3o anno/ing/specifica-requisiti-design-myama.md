# Documento di Specifica dei Requisiti e Progettazione Software - Sistema "MyAma"
*Derivante dalla mappatura sistematica del database "MyAma" sul template di Ingegneria del Software (`guida-compilazione-isw.md`)*

Questo documento costituisce la specifica e la progettazione di dettaglio del sistema **MyAma**, la piattaforma per la gestione centralizzata della raccolta dei rifiuti ingombranti a Roma Capitale. Il design qui esposto traduce fedelmente lo schema logico e i vincoli fisici del database d'origine in requisiti funzionali, modelli di casi d'uso, requisiti di sistema e architettura dei dati orientata agli oggetti.

---

## 1. INTRODUZIONE

### 1.1 Obiettivi del Sistema
Il sistema **MyAma** nasce per sostituire i sistemi aziendali legacy frammentati dell'Azienda Municipale Ambiente (AMA) di Roma Capitale. Gli obiettivi primari sono:
* **Centralizzazione logistica:** Coordinare in un'unica piattaforma le richieste di smaltimento dei cittadini, la disponibilità dei veicoli aziendali, i turni del personale operativo e la capienza delle sedi (centri di raccolta).
* **Tracciabilità dei flussi:** Monitorare l'intero ciclo di vita di un rifiuto ingombrante, dalla prenotazione iniziale al conferimento o ritiro effettivo, fino alla pesatura finale e al ricalcolo delle tariffe.
* **Prevenzione del degrado urbano:** Ridurre i conferimenti illeciti fornendo ai cittadini uno strumento self-service immediato per prenotare ritiri a domicilio o registrare consegne dirette presso i centri di raccolta comunali.

### 1.2 Contesto d'Uso e Ambito del Prodotto
Il software opera come una piattaforma client-server ad alta disponibilità.
* **Canali di Accesso:** Il sistema prevede un portale web per i clienti (cittadini) e gli amministratori, e un modulo client (ad es. per dispositivi mobili o terminali rugged) dedicato agli operatori sul campo `[TODO: Da definire a livello di implementazione software lo stack tecnologico di frontend (es. React/Angular, Flutter) e i protocolli di comunicazione client-server]`.
* **Ambiente Operativo:** Funzionamento previsto h24 per 365 giorni all'anno, con picchi di carico stimati per una popolazione potenziale di circa 2 milioni di utenti (Roma Capitale).

---

## 2. GLOSSARIO

Il glossario definisce in modo non ambiguo i concetti chiave utilizzati in tutto il progetto, garantendo la coerenza interna tra requisiti, casi d'uso e modelli.

| Termine | Categoria | Definizione |
| :--- | :--- | :--- |
| **Cliente** | Attore | Cittadino maggiorenne, residente a Roma, registrato al sistema tramite SPID o credenziali tradizionali, che richiede servizi di smaltimento. |
| **Lavoratore AMA** | Attore | Dipendente operativo dell'azienda AMA, specializzato nel ruolo di "Autista (Corriere)" o "Operatore di Sede". |
| **Autista (Corriere)** | Attore | Lavoratore AMA incaricato di effettuare i ritiri dei rifiuti a domicilio guidando un veicolo aziendale assegnato. |
| **Operatore di Sede** | Attore | Lavoratore AMA che opera fisicamente all'interno di un centro di raccolta (Sede AMA) e gestisce l'accoglienza e i conferimenti dei cittadini. |
| **Amministratore** | Attore | Utente con permessi di livello massimo, preposto alla configurazione di sedi, CAP, tariffe e turni. |
| **Prenotazione** | Entità | Richiesta formale di smaltimento rifiuto, caratterizzata da un codice univoco, foto, descrizione, tipologia (a domicilio o in sede), data, ora, peso stimato/effettivo, costo e stato. |
| **Sede AMA** | Entità | Centro fisico di raccolta e stoccaggio rifiuti ingombranti, identificato da un codice univoco e associato a un elenco di CAP serviti. |
| **Veicolo** | Entità | Mezzo di trasporto aziendale (identificato da targa) con uno specifico carico massimo e stato logico, associato a un autista per i ritiri a domicilio. |
| **Stato Prenotazione** | Stato | Ciclo di vita logico di una richiesta di smaltimento, i cui valori ammissibili sono `'attiva'`, `'completata'` e `'cancellata'`. |
| **Valutazione (Feedback)** | Entità | Giudizio opzionale (voto da 1 a 5 e commento) che un cliente può associare a una prenotazione, inseribile esclusivamente in stato `'completata'`. |

---

## 3. USER REQUIREMENTS DEFINITION (CASI D'USO)

La specifica dei requisiti utente è strutturata in base agli attori del sistema. Vengono qui dettagliati i tre casi d'uso primari del sistema MyAma tramite tabelle standardizzate.

```
                      ┌──────────────────────────────────────────────┐
                      │                SISTEMA MyAma                 │
                      │                                              │
      ( Cliente ) ───┼───> [UC1: Effettua Prenotazione Ritiro]      │
                      │                                              │
                      │                                              │
 ( Amministratore ) ──┼───> [UC2: Gestisci e Assegna Turni/Veicoli]  │
                      │                                              │
                      │                                              │
      ( Autista ) ───┼───> [UC3: Registra Completamento Ritiro]      │
                      └──────────────────────────────────────────────┘
```

### 3.1 Use Case Cliente (Cittadino)

#### UC1: Effettua Prenotazione Ritiro Rifiuto

| Elemento | Descrizione Operativa |
| :--- | :--- |
| **Nome Caso d'Uso** | Effettua Prenotazione Ritiro Rifiuto |
| **Attori** | Cliente (Primario) |
| **Precondizioni** | Il Cliente è registrato, ha effettuato con successo l'accesso ed è maggiorenne (requisito verificato all'atto della registrazione tramite controllo della data di nascita). |
| **Passi Azione (Scenario Principale)** | 1. Il Cliente richiede l'inserimento di una nuova prenotazione.<br>2. Il sistema recupera l'indirizzo e il CAP registrati nel profilo del Cliente.<br>3. Il sistema interroga il database per individuare le sedi AMA che coprono quel CAP (tramite l'associazione `LISTA_CAP`).<br>4. Il sistema presenta le sedi compatibili e chiede di selezionare la tipologia di servizio (`'a domicilio'` o `'in sede'`).<br>5. Il Cliente compila i dati della prenotazione inserendo: descrizione del rifiuto, peso stimato (maggiore di zero), data e orario preferito, e carica una fotografia del materiale.<br>6. Il sistema convalida i dati, calcola la tariffa provvisoria (Formula: $Costo = TipologiaRifiuto \times Peso$) e (se il servizio è a domicilio) verifica la disponibilità di un veicolo idoneo e di un autista per il turno selezionato.<br>7. Il Cliente conferma i dettagli e la tariffa stimata.<br>8. Il sistema registra la prenotazione con stato `'attiva'` e associa la chiave esterna del cliente (`codice_fiscale`), della sede (`codice_sede`) e (se a domicilio) del lavoratore assegnato (`CID_lavoratore`). |
| **Scenari Alternativi** | **3.a Nessuna sede copre il CAP inserito:**<br>&nbsp;&nbsp;&nbsp;&nbsp;1. Il sistema rileva che il CAP del cliente non è presente nell'elenco `LISTA_CAP` di alcuna sede.<br>&nbsp;&nbsp;&nbsp;&nbsp;2. Il sistema mostra un errore di incompatibilità geografica e interrompe la procedura.<br>**6.a Peso non valido:**<br>&nbsp;&nbsp;&nbsp;&nbsp;1. Il sistema rileva che il peso inserito è $\le 0$.<br>&nbsp;&nbsp;&nbsp;&nbsp;2. Il sistema blocca la procedura, evidenzia il campo in rosso e richiede di inserire un peso positivo.<br>**6.b Mancanza di risorse logistiche (ritiro a domicilio):**<br>&nbsp;&nbsp;&nbsp;&nbsp;1. Il sistema verifica che non vi sono veicoli con capacità di carico residua sufficiente o autisti liberi nel turno selezionato.<br>&nbsp;&nbsp;&nbsp;&nbsp;2. Il sistema propone date o turni alternativi, invitando il Cliente a selezionarne un altro. |
| **Post-condizioni** | La prenotazione viene salvata con successo nel database in stato `'attiva'`. |

---

### 3.2 Use Case Amministratore (Staff Tecnico)

#### UC2: Gestisci e Assegna Turni e Veicoli

| Elemento | Descrizione Operativa |
| :--- | :--- |
| **Nome Caso d'Uso** | Gestisci e Assegna Turni e Veicoli |
| **Attori** | Amministratore (Primario) |
| **Precondizioni** | L'Amministratore è autenticato e ha accesso alla console di amministrazione. |
| **Passi Azione (Scenario Principale)** | 1. L'Amministratore accede alla sezione logistica e richiede l'inserimento di un nuovo turno settimanale.<br>2. Il sistema mostra l'elenco dei lavoratori registrati con ruolo `'corriere'` (Autisti) o `'in_sede'` (Operatori).<br>3. L'Amministratore seleziona il lavoratore (`CID_lavoratore`), inserisce le specifiche del turno (data, orario d'inizio, orario di fine, pausa pranzo) e associa un veicolo (identificato da `targa`) qualora il lavoratore sia un autista.<br>4. Il sistema effettua un controllo di consistenza: verifica che il lavoratore non abbia turni sovrapposti nello stesso giorno e che il veicolo sia in stato `'disponibile'`.<br>5. L'Amministratore conferma l'assegnazione.<br>6. Il sistema registra il record nella tabella di associazione `TURNO_SETTIMANALE`, imposta il lavoratore come assegnatario primario del veicolo e aggiorna lo stato del veicolo su `'occupato'`. |
| **Scenari Alternativi** | **4.a Conflitto di orari per il lavoratore:**<br>&nbsp;&nbsp;&nbsp;&nbsp;1. Il sistema rileva un overlapping temporale con un turno preesistente per lo stesso dipendente.<br>&nbsp;&nbsp;&nbsp;&nbsp;2. Il sistema notifica il conflitto evidenziando l'orario bloccante e impedisce l'inserimento.<br>**4.b Veicolo non disponibile:**<br>&nbsp;&nbsp;&nbsp;&nbsp;1. Il sistema rileva che il veicolo selezionato è in manutenzione o già assegnato ad un altro autista per quel turno.<br>&nbsp;&nbsp;&nbsp;&nbsp;2. Il sistema mostra un avviso, blocca il salvataggio e richiede di selezionare un veicolo differente. |
| **Post-condizioni** | Il turno settimanale e l'associazione veicolo-autista sono salvati nel database. Lo stato del veicolo viene aggiornato coerentemente. |

---

### 3.3 Use Case Autista (Corriere)

#### UC3: Registra Completamento Ritiro con Ricalcolo Peso

| Elemento | Descrizione Operativa |
| :--- | :--- |
| **Nome Caso d'Uso** | Registra Completamento Ritiro con Ricalcolo Peso |
| **Attori** | Autista (Primario) |
| **Precondizioni** | L'Autista è autenticato sul proprio terminale mobile, è in servizio e ha una prenotazione nello stato `'attiva'` a lui assegnata per il turno corrente. |
| **Passi Azione (Scenario Principale)** | 1. L'Autista seleziona la prenotazione in carico dall'elenco del proprio turno.<br>2. Al momento del ritiro fisico, l'Autista esegue la pesatura effettiva del rifiuto ingombrante.<br>3. L'Autista inserisce nel sistema il peso reale riscontrato (sovrascrivendo l'attributo `peso_rifiuto`).<br>4. Il sistema esegue un trigger di controllo interno per verificare che il nuovo peso non superi il limite residuo di portata del veicolo aziendale associato per quel turno.<br>5. Il sistema ricalcola dinamicamente la tariffa finale (`costo_prenotazione`) basandosi sul peso effettivo.<br>6. L'Autista richiede la chiusura dell'intervento.<br>7. Il sistema aggiorna lo stato della prenotazione in `'completata'` e memorizza il peso definitivo e la tariffa finale calcolata. |
| **Scenari Alternativi** | **4.a Sovraccarico del veicolo:**<br>&nbsp;&nbsp;&nbsp;&nbsp;1. Il sistema rileva che l'aggiunta del peso reale del rifiuto fa superare il `carico_massimo` tollerato dal veicolo.<br>&nbsp;&nbsp;&nbsp;&nbsp;2. Il sistema solleva un warning critico sul terminale dell'Autista. L'Autista deve confermare manualmente la presa in carico eccezionale o richiedere l'intervento di un mezzo di supporto `[TODO: Da definire a livello di implementazione software come gestire il flusso di eccezione logistica di sovraccarico (es. smistamento automatico di un secondo veicolo)]`. |
| **Post-condizioni** | La prenotazione transita definitivamente in stato `'completata'`. Il peso effettivo e la tariffa ricalcolata sono memorizzati a sistema, sbloccando la possibilità per il Cliente di inserire una valutazione. |

---

## 4. SYSTEM REQUIREMENTS

### 4.1 Requisiti Funzionali (RF)
I requisiti funzionali del sistema sono formulati in maniera assertiva ed impersonale:

* **RF_01 (Registrazione & SPID):** Il sistema software deve consentire la registrazione dei cittadini fornendo i propri dati anagrafici e convalidando la maggiore età (18 anni compiuti). Deve inoltre supportare l'integrazione di un token SPID per l'autenticazione certificata.
* **RF_02 (Incompatibilità CAP):** Il sistema software deve impedire la registrazione di una prenotazione se l'indirizzo di domicilio specificato non presenta un CAP coperto da almeno una Sede AMA (intervallo CAP ammesso per Roma Capitale: `[00010 - 00199]`).
* **RF_03 (Calcolo Tariffe):** Il sistema software deve calcolare in modo automatico e dinamico il costo della prenotazione moltiplicando il peso del rifiuto (che deve essere rigorosamente maggiore di zero) per la tariffa associata alla specifica tipologia di rifiuto ingombrante.
* **RF_04 (Filtro Geolocalizzato):** Il sistema software deve presentare al cliente, durante la compilazione della prenotazione, esclusivamente le sedi AMA che servono il CAP del domicilio dell'utente.
* **RF_05 (Gestione Logistica):** Il sistema software deve consentire agli amministratori l'assegnazione dei dipendenti a turni orari settimanali e (per i lavoratori con ruolo `'corriere'`) ad uno specifico veicolo disponibile.
* **RF_06 (Verifica Carico):** Il sistema software deve impedire l'assegnazione di un veicolo a un servizio di ritiro se il peso stimato o reale del rifiuto supera la portata utile residua del veicolo stesso (`carico_massimo`).
* **RF_07 (Aggiornamento Stato & Valutazione):** Il sistema software deve consentire l'inserimento di una valutazione (voto numerico da 1 a 5 e commento facoltativo) da parte del cliente solo ed esclusivamente se la prenotazione associata si trova in stato `'completata'`. Il sistema deve rifiutare qualsiasi tentativo di sottomissione del feedback per prenotazioni attive o annullate.
* **RF_08 (Anonimizzazione & GDPR):** Il sistema software deve effettuare un'eliminazione in cascata (`ON DELETE CASCADE`) dei dati del cliente in caso di cancellazione del suo account, garantendo la rimozione immediata delle informazioni sensibili e identificative, conservando i record delle prenotazioni storiche in forma strettamente anonimizzata per soli fini statistici interni.

---

### 4.2 Requisiti Non Funzionali (RNF)

I requisiti qualitativi sono organizzati seguendo le linee guida dello standard **ISO/IEC 25010** e focalizzandosi sui vincoli di persistenza, sicurezza e integrità emersi dal progetto di basi di dati.

#### 1. Sicurezza (Security)
* **RNF_SEC_01 (Autenticazione):** Il sistema deve memorizzare le password degli utenti (Clienti e Lavoratori) all'interno del database esclusivamente in forma cifrata (hashing) `[TODO: Da definire a livello di implementazione software l'algoritmo di hashing (es. bcrypt o Argon2) e le librerie di sicurezza]`.
* **RNF_SEC_02 (Privacy e Accesso ai Dati):** Il sistema non deve rivelare ai Lavoratori AMA in servizio le informazioni personali del Cliente non strettamente necessarie allo svolgimento del ritiro. Ai corrieri deve essere mostrato solo il recapito telefonico minimo e l'indirizzo di ritiro, escludendo email, password e dati di nascita.
* **RNF_SEC_03 (Audit):** Tutte le operazioni di inserimento, modifica o cancellazione effettuate sulla tabella `PRENOTAZIONE` devono essere loggate a fini di auditing.

#### 2. Efficienza delle Prestazioni (Performance Efficiency)
* **RNF_PER_01 (Tempo di Risposta):** Il ricalcolo automatico della tariffa e la verifica di disponibilità di veicoli/autisti durante l'inserimento di una prenotazione devono richiedere un tempo di elaborazione inferiore a 2 secondi.
* **RNF_PER_02 (Capacità):** Il backend deve essere dimensionato per supportare la gestione concorrente di almeno 10.000 prenotazioni attive contemporaneamente senza degradazione delle performance.

#### 3. Affidabilità e Disponibilità (Reliability & Availability)
* **RNF_REL_01 (Integrità Transazionale):** Le operazioni che coinvolgono più tabelle (es. registrazione prenotazione, assegnazione turno e aggiornamento stato veicolo) devono essere eseguite all'interno di transazioni ACID native per prevenire stati incoerenti del database.
* **RNF_REL_02 (Disponibilità):** Il sistema deve garantire un uptime del 99.9% h24, strutturando politiche di backup automatico del database a caldo `[TODO: Da definire a livello di implementazione software la strategia di backup e replica del database (es. replica master-slave, backup incrementali giornalieri)]`.

#### 4. Usabilità (Usability)
* **RNF_USA_01 (Accessibilità Mobile):** Il client per i lavoratori deve essere fruibile su dispositivi mobili con un'interfaccia responsive ad alto contrasto per facilitare l'uso all'aperto da parte dei corrieri.

#### 5. Manutenibilità (Maintainability)
* **RNF_MNT_01 (Modularità):** La logica di business relativa ai vincoli e alle tariffe deve essere disaccoppiata dall'interfaccia utente (Boundary) implementando l'architettura MVC/ECB, facilitando l'estensione o la modifica delle tariffe senza riscrivere i client UI.

---

### 4.3 Requisiti di Dominio (RD)
* **RD_01 (Limiti CAP di Roma):** Il sistema deve convalidare l'inserimento di CAP accettando unicamente i valori numerici compresi nell'intervallo `00010` - `00199`, corrispondenti al territorio comunale di Roma Capitale.
* **RD_02 (Proprietà Rifiuto):** Un cittadino può smaltire esclusivamente rifiuti che rientrano nelle tabelle dei codici CER (Catalogo Europeo dei Rifiuti) per i rifiuti ingombranti e speciali assimilati gestiti da AMA.

---

## 5. MODELLO DI DOMINIO (ENTITÀ E RELAZIONI)

Il modello di dominio sottostante descrive la struttura statica delle entità logiche di MyAma. Sostituisce l'unrefined class diagram, catturando classi e molteplicità delle associazioni derivate direttamente dal database relazionale normalizzato.

### 5.1 Diagramma delle Classi di Dominio (UML Concettuale)

```
   ┌───────────────┐                  1..* ┌───────────────┐
   │   Cliente     ├──────────────────────>│    SedeAMA    │
   └───────┬───────┘                       └───────┬───────┘
           │ 1                                     │ 1
           │                                       │
           │ 0..*                                  │ 0..*
   ┌───────▼───────┐                       ┌───────▼───────┐
   │  Prenotazione │<──────────────────────┤   Lista_CAP   │
   └───────┬───────┘ 0..*             1..* └───────────────┘
           │ 1
           │
           ├───────────────────────────────┐
           │ 0..1                          │ 0..*
   ┌───────▼───────┐               ┌───────▼───────┐
   │  Valutazione  │               │  Lavoratore   │
   └───────────────┘               └───────┬───────┘
                                           │ 1 (Eredità: ruolo ENUM)
                                    ┌──────┴──────┐
                                    ▼             ▼
                                ┌───────┐     ┌───────┐
                                │Autista│     │Operat.│
                                └───────┘     └───────┘
                                    │ 1
                                    │ 0..1
                                ┌───▼───┐
                                │Veicolo│
                                └───┘───┘
```

### 5.2 Descrizione delle Entità e Cardinalità
Le associazioni riflettono fedelmente i vincoli di integrità del database di provenienza:

1. **Cliente - Prenotazione ($1 \to 0..*$):** Un cliente può inserire nel tempo molteplici prenotazioni nel sistema. Ciascuna prenotazione deve essere imperativamente legata a un unico cliente (`codice_fiscale`).
2. **Prenotazione - Valutazione ($1 \to 0..1$):** Una singola prenotazione può ricevere al massimo un feedback. Questo vincolo di unicità è garantito dal fatto che la chiave primaria di `Valutazione` coincide con la chiave esterna della prenotazione stessa.
3. **SedeAMA - Prenotazione ($1 \to 0..*$):** Ogni prenotazione viene instradata e gestita da un'unica sede AMA competente per territorio.
4. **SedeAMA - Lista_CAP ($1..* \to 1..*$):** Relazione molti-a-molti. Una sede serve una lista di più CAP e lo stesso CAP può essere coperto da più sedi. Nel database, questa relazione è normalizzata tramite la tabella ponte `LISTA_CAP`.
5. **Lavoratore - Prenotazione ($1 \to 0..*$):** Ogni operazione di ritiro viene assegnata a un dipendente AMA di servizio.
6. **Lavoratore - Veicolo ($0..1 \to 1$):** Un autista (lavoratore specializzato) è associato a un veicolo aziendale specifico per il suo turno lavorativo di ritiro a domicilio. Un veicolo in servizio deve avere un unico autista.

---

## 6. PROGETTAZIONE ARCHITECTTURALE DEI DATI

Questa sezione formalizza le decisioni di design relative a come i dati persistenti del dominio vengono gestiti dal software e memorizzati nel DBMS relazionale MyAma.

### 6.1 Mappatura Object-Relational (O/R Mapping)
Per garantire una corrispondenza esatta tra la modellazione a oggetti del Class Diagram e lo schema relazionale in Terza Forma Normale (3NF), si applicano i seguenti criteri di traduzione:

1. **Risoluzione delle Chiavi Esterne (Foreign Keys):** 
   Nel Class Diagram di Dominio e nel successivo Class Diagram Refined, le chiavi esterne SQL (come `codice_fiscale` o `codice_sede` all'interno della tabella `PRENOTAZIONE`) vengono **completamente eliminate**. Al loro posto si utilizzano le **associazioni direzionali UML** (frecce di navigabilità). Ad esempio, la classe `Prenotazione` conterrà un attributo privato di tipo oggetto referenziato:
   * Codice SQL: `codice_fiscale VARCHAR(16) REFERENCES CLIENTE`
   * Codice Refined UML: `-cliente: Cliente` (visibilità privata, tipo classe)
2. **Normalizzazione delle Tabelle di Associazione (Molti-a-Molti):**
   Le tabelle associative del database come `TURNO_SETTIMANALE` e `LISTA_CAP` vengono modellate in UML come associazioni dirette tra le due classi partecipanti, con molteplicità `*` su entrambi i lati. Nella raffinazione del codice, verranno implementate tramite collezioni dinamiche (es. `List<Turno>` all'interno della classe `Lavoratore` e `List<Lavoratore>` in `Turno`) `[TODO: Da definire a livello di implementazione software l'uso di un framework ORM specifico come Hibernate/JPA o l'utilizzo di query SQL native tramite JDBC/DAO]`.
3. **Mappatura dell'Ereditarietà (Specializzazione Lavoratore):**
   Nel database d'origine, i ruoli operativi dei dipendenti sono distinti attraverso un attributo `ruolo` di tipo ENUM (`'in_sede'`, `'corriere'`). A livello di Ingegneria del Software, per supportare l'estensibilità ed evitare istruzioni condizionali complesse nel calcolo dei turni, questa relazione viene idealmente tradotta tramite **ereditarietà di classe** (Classe astratta `Lavoratore` e sottoclassi concrete `Autista` e `OperatoreSede`).

### 6.2 Vincoli Fisici di Integrità e Persistenza
Il sistema software demanda al DBMS la protezione finale dei dati sensibili e la consistenza delle relazioni, ma i controller di business (classi `<<control>>` in ECB) devono intercettare questi vincoli prima della sottomissione fisica per migliorare l'esperienza utente ed evitare eccezioni a livello di database:

* **Integrità Referenziale in Cascata (`ON DELETE CASCADE`):** 
  In ossequio al GDPR, se un `Cliente` cancella il proprio account, il DBMS esegue l'eliminazione automatica in cascata di tutte le sue prenotazioni. Per non alterare la reportistica storica aziendale, il controller applicativo deve invocare una routine di anonimizzazione che clona i dati statistici delle prenotazioni in una tabella di storicizzazione de-identificata (priva di CF) prima di confermare la cancellazione sul database `[TODO: Da definire a livello di implementazione software la logica di anonimizzazione statistica]`.
* **Integrità dei Dati e Validazione Preventiva:**
  * **Verifica Maggiore Età:** La validazione dei 18 anni compiuti deve essere controllata sia dal controller di registrazione client-side sia dal trigger nativo sul DB (`verifica_eta_cliente`), garantendo un doppio livello di sicurezza.
  * **Range Voti:** Il feedback deve essere limitato dal controller in un range intero `[1, 5]`, mapparne la visualizzazione grafica con una scala a stelle (UML Boundary) e applicare il vincolo di `CHECK` SQL a livello fisico di colonna.
  * **Integrità dei CAP:** Il sistema blocca preventivamente l'inserimento di qualsiasi indirizzo che non contenga un CAP valido per il territorio di Roma Capitale (`00010` - `00199`).
