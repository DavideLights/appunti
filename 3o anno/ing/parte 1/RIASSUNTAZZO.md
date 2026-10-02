# 2 processo software

**processo software**: bisogna decidere sotto quali operazioni sottoporre il ciclo di vita del software a partire dall'analisi dei requisiti, fino allo stato operativo.
* artefatti: prodotti intermedi del software, come documentazione
* codice: sorgente associato alle varie build
* manutenzione: bisogna specificare le tecniche di manutenzione
	* perfettiva, adattiva, preventiva, correttiva
* cosa definisce? cosa bisogna fare, per guidare la fase dove si decide come lo si fa.
* test, verifica e validazione: alla fine di ogni fase dello sviluppo si verifica/test. alla fine dello sviluppo si fa la validazione
	* verifica: lo stiamo facendo  nel modo giusto?
	* validazione: stiamo costruendo il prodotto giusto? (match con User goals)

**build and fix**: assenza di struttura, si fa una sola build e la si migliora di continuo. fa schifo

**waterfall**: ogni fase e' succeduta dalla verifica. globalmente si fa la validazione. Se verifica o validazione non hanno successo si torna indietro e si ripete la cascata da una fase specifica.
* analisi requisiti
* analisi specifiche
* design
* codifica
* integrazione
* modalita operativa

**rapid prototyping**: per ridurre i rischi legati alle specifiche utente, si sviluppa un prototipo velocemente da presentare al cliente e agli stakeholder

**sviluppo prototipo**: determinare obiettivi, determinare funzionalita, sviluppo e valutazione.

**throw away prototyping**: si sviluppano piu prototipi finche non soddisfiamo il cliente, successivamente si va nella fase di sviluppo vera e propria.

**problemi della prototipazione**: 
* no legale
* sicurezza/performance
* destrutturato

**programmazione visuale**: ottimo per la prototipiazione ma problemi di teaming, e troppe dipendenze software, architettura non chiara e immediata.

**modello incrementale**: in progetti grandi, si reiterano i passaggi di sviluppo piu volte per ridurre il rischio di errori. in particolare si vuole iterare piu volte le fasi di specifica per evitare costi enormi per riparare gli errori in fasi avanzate di sviluppo.

**modell con/senza overall**: con architettura overall viene definita un'architettura che devono eseguire tutte le build. una build sussegue l'altra. senza, ogni build puo' essere tratta l'una indipendentemente dall'altra.

 **cosa vuol dire incrementale**: si sviluppano piu build differenti, fino ad arrivare ad una build finale

**numero di build**: costruire tante build, vuol dire avere un costo alto di integrazione e viceversa.

**incrementale vs waterfall**: piu feedback, e reiterazione della validazione. piu team, piccoli, che lavorano contemporaneamente. 

**modello a spirale**: e' simile a waterfall ma
* introduce prototipazione
* introduce analisi del rischio prima di ogni fase
* si fa pianficazione
* rotazione: sadfdsaf
* asse verticale: costo

**modello a spirale dettagliato**: prototipazione, analisi, identificare alternative, valutare alternative, gestione dei rischi prima di ogni step


**gestione del rischio**: 
* rischio: probabilita che un evento accada con effetti avversi sullo sviluppo
* posso classificarli in base alla probabilita che avvegano
* posso classificarli in base al tipo
	* progetto
	* business
	* prodotto
* come si gestisce? identificazione -> analisi -> pianificazione -> monitoraggio

**modello ad oggetti**: modulare, pianificazione basata su oggetti.

**sync and stabilize**: 
* **synch**: periodo dove ogni giorno viene rilasciata una build sincronizzando il lavoro di tutti i team
* **stabilize**: periodo in cui ci si concentra per rilasciare una build funzionanate, milestone
* ogni team, task semplici
* lavoro parallelo
* test continuo 

**sas vs waterfall**: sas permette di
* parallelizzare il lavoro
* dividere il lavoro in team
* scalabile per organizzazioni grandi

**modello netscape**:
* basato su sync and stabilyze
* ogni 3 dev, 1 tester.
* **fase sync**: nuove funzionalita
* **fase stabilize**: debuging, testing, fix, prestazioi
* **problemi**: effort, review, teaming

**step netscape**:
1. **definizione e approvazione**: vengono analizzati i requisiti utente e di sistema. executive approva il progetto
2. **sviluppo**: design e sviluppo -> interim executive -> rilascio alpha interna
	1. alpha interna possibilmente feature complete
3. **beta**: rilascio prima beta pubblica -> rilascio seconda beta pubblica con UI freeze e feature complete
4. si raggiunge lo stato code complete, si fa debug e ci si prepara al rilascio finale

**agile**: le tecniche agile hanno come principi
* rapporti umani, comunicazione
* comunicazione con cliente
* scrittura software funzionante e documentazione
* resistenza ai cambiamenti
* ed altri 12 principi

**scrum**: e' un framework agile
* **scrum master**: facilita implementare scrum
* **developer team**: chi lavora all'interno dello sprint
* **product owner**: detiene il backlog
* **spirnt**: e' un'iterazione all'interno di scrum, 2/4 settimane
	* prima riunione: product lo sprint backlog
	* development: si lavora sulle feature/problemi/ottimizzaizoni nel backlog
	* sprint review: riunione su cosa si e' fatto nello sprint corrente
	* **sprint retro-spective: si decide come migliorare lo sviluppo nel prossimo sprint**

**user stories**: tecnica agile per descrivere i requisiti utente
* as `<role> i want <goal> so that <benefit>`
* **epic**: se una user story puo' essere decomposta, poiche' grande

CCM: 5 livelli di maturita
* caotico
* limitare costi e tempi
* applicazione modello
* monitoraggio valori sullo sviluppo software
* miglioramento processi produttivi

# 3 requisiti
requisito software: rappresenta un vincolo sul sistema software oppure un bisogno dell'utente che il sistema deve risolvere. i vincoli rappresentano un vero e proprio contratto tra azienda e cliente da rispettare.
* vincoli astratti: utili per l'appalto
* vincoli utente: scritti usando linguaggio comprensibili
* a chi sono destinati i requisiti? agli ingegneri per la fase OOA e OOD
	* gli ingegneri
	* utenti finali: sanno cosa offrira il software

tipi di requisiti:
* funzionali: req. utente
* non funzionali: req. sistema
* domino: dipendono dal dominio applicativo (leggi, norme)

clasificazione:
* requisiti esterni: dipendono da altri sistemi software 
* performance: in quanto tempo mi aspetto una risposta dal sistema
* affidabilita: quanto deve essere disponibile il servizio sul totale del tempo
* sicurezza: quanto deve essere sicuro
* conformita
* manutenibilita
* usabilita: misurare facilita di utilizzo

problemi possibili:
* inconsistenza
* incompletezza
* ambigui

**verificabilita**: requisiti ben scritti dovrebbero anche essere verificabili tramite misurazioni, in termini di spazio, di performance, robustezza, facilita di uso, complessita

**comprensione degli use case**: verbi consistenti, no termini generali, no termini ambigui, linguaggio semplice e diretto.

**requisiti di sistema**: PDL, UML, o linguaggi alto livello
* matematiche

**SRS**: IEEE ha definito un standard per il system requirements specification.
* introduzione
* glossario dei termini
* requisisti utente
* specifiche di sistema
* architettura di sistema
* modelli di sistema
* **evolution**

# 4. ingegneria dei requisiti
**ingegneria dei requisiti**: e' il processo di raccolta, analisi e convalida dei requisiti.
* studio fattibilita
* raccolta e analisi
* convalida
* gestione
* pianificazione e controlo

**studio di fattiblita**: varie riunioni con exectuive, ecc per produrre un report di fattibilita. 
* ritorno investiemtno
* verifica processi aziendali
* verifica compatibilita con strategia per utente finale
* verifica budget / tecnolgie disponibili
* verifica compatibilita con servizi esterni

**identificazione e analsi**:
* identificazione: 
	* etnografia con stakeholder
	* casi d'uso
	* prototipazione
* analisi: modelli formali e semi-formali
* capire il domino applicativo, raccolta, classifica, priorita, compatiblita, ecc....

**convalida**: ci sono varie teniche
* formali: check list
* informali: walktrough
* generazione test cases
* bisogna verificare: compatibilita, verificabilita, validita, completezza, coerenza, verificabilita

**gestione dei requisiti**: evoluzione probaiblistica dei requisiti:
* cambiabili
* emergenti
* derivanti dal software
* consequenziali

**pianificazione e controllo**: associare id al requisito, ed identficare una misura per monitorarlo. pianificare la gestione del requisito

**analisi formale e semi-formale**: per l'analisi semi-formale si usano l'analisi strutturata, oppure l'analisi OOA.

petri net: semplice

linguaggio z

semi-formali: PDL, java

**modelli e punti di vista**: bisogna studiare i requisiti utente sotto 3 punti di vista:
* statico: ERD, rappresentare come sono organizzati i dati e le relazioni
* comportamentale: DFD, rappresentare come vengono scambiati i dati
* dinamico: diagramma di stato

**DFD**: permette di rappresentare
* sorgenti dati esterne/interne
* flusso di azioni sui dati
* **iterativo**: un flusso dati puo' essere espanso per aggiungere dettagli

**SSA**:
1. DFD embrionale
2. si selezonano quali aree computerizzare: batch o realtime?
3. si identificano sorgenti esterne/interne
4. determinare logica dei processi
5. determinare input/output dei processi
6. determinare grandezza storage e hardware requirements

# 5. OOA
**OOA**: descrive cosa bisogna fare. mentre OOD il come.
* analisi e design devono essere fatti sotto tre punti di vista
	* modello dati: modello statico/logico. come sono divise le entita e le informazioni. class diagram
	* modello comportamentale: che messaggi si scambiano gli oggetti tra loro. collaboration diagram
	* modello dinamico: come si comportano gli oggetti a livello operativo., il cilco di vita del software e come occorrono gl ieventi nel tempo. component diagram

UML: 9 formalismi per OOA ed OOD
* class diagram
* state diagram
* activity diagram
* component diagram
* deployment diagram
* use case diagram
* collaboration diagram
* object diagram
* sequence diagram

**modello dei dati**: 
* organizzazione statica e logica del sistema, come sono organizzati i dati
* iterativo: 
	* preliminare: contiene solo Entita, ossia classi derivate dal dominio applicativo
	* avanzata: aggiungo interfacce e controller
* class diagram

**identificare classi**
* **noun phrases**: sono quelle frasi che fatte di entita nominali, ossia parole che decrivono il contesto/significato di una parola centrale nel discorso
	* rilevanti: sono le entita
	* non rilevanti
	* fuzzy: sono quelle parole generali/equivocabili/specifiche che non capiamo per il momento, ma fondamentali nel sistema.
* **CRC**: riunioni dove per ogni entita identificata si identificano responsabilita e collaboratori sotto-forma di card
* **use case diagram**: dagli use case si capisce cosa deve fare una entita identificata
* **common class patterns**: un termine diventa classe se denota un evento, una persona, un luogo, un concetto.
* di solito si mischiano tutti i pattern e si usano uno dopo l'altro.

**linee guida per definire entity classes:**
* ogni classe ha uno scopo ben preciso
* molteplicita di attributi
* interfaccia esposta
* singleton oppure statica

**naming**:
* camel case: nomi classi
* snake case: nomi attributi

**associazioni**: quando un'attributo non e' primitivo si ha un'associazione tra due classi
* ruolo: a che serve l'associazione?
* moleplicita: da entrambi i lati quante istanze partecipano?

**aggergazione**: associazioni che indicano un'appartenenza tra le parti
* **forte**: per valore
	* exclusive owns: se il padre muore allora stira il figlio
	* owns: il figlio puo' essere riassegnato
* **debole**: per riferimento
	* has: appartenenza debole
	* member: la classe e' membra del padre ma non c'e' un forte legame di appartenenza

**UML**:
* aggregazione semplice: rombo vuoto.
* appartenenza: rombo pieno

**ereditarieta**: si manifesta tramite


**object diagram**: relazioni complessed ed interazioni tra oggetti

**modello comportamentale**: e' modellato tra vari diagrammi
* activity diagram: le sequenze di azioni per portare a termine un'obiettivo
* use case diagram: modella per ogni attore i casi d'uso a lui correlat
	* extend: quando un use case e' facoltativo per portare a termine un'altro use case
	* include: quando un use case e' obbligatorio per un'altro

**activity diagram**: 
* ha piu livelli di astrazione
* **iterativo**: posso espandere ogni azione a piacimento
* guard conditions: per le condizioni sul flusso
* fork e join: per le parallele
* rombo: if

**diagrammi interazione**:
* OOA -> sequence diagram
* OOD -> collaboration diagram
* $\text{seq} \equiv \text{col}$

**identificare operazini da esporre**: ad almeno un messaggio corrisponde una operazione da ep

# 7 pianificazione
4 p:
* persone: risorse umane, CMM
* progettazione: **insieme operativo delle attivita da svolgere**
* processo: processi aziendali
* prodoto: vincoli, caratteristiche, requisiti

mancano un po de cose...

**COCOMO**: si adatta a 3 tipi di sviluppo
* aziende piccole
* team intermedi
* sistemi realtime/tanti vincoli

**3 modelli**:
* calcolo solo effort nominale, overview globale del tempo di sviluppo
* calcolo effort con cost drivers
* divido cost drivers per modulo


**step**:
* effort nominal: si calcola elevando e moltiplicando LOC per due costanti
* effort: si calcola moltiplicando effort nominale per cost drivers
	* cost drivers: produttoria dei punteggi assegnati ai cost drivers
* tempo consegna: moltiplico effort per costante ed elevo per una costante $k$
	* $k$ varia a seconda del tipo di azienda, es $k=0.38,0.35,0.32$

**cosa ottengo?** tempo consegna, ossia mesi perima della consegna.

**che ci faccio coi mesi**: ripartisco il tmepo di sviluppo
* 16: requisiti e progettazione 
* 62: sviluppo
* 22: integrazione e testing

**pianificazione temporale**: si suddivide il progetto in task semplici. si identificano le dipendenze tra questi, si stima l'effort, tempo di completamento e costo. cosa ci si aspetta da un task, quanto personale assegnare.
* i task dovrebbero essere piu indipendenti possibili

grafo di PERT: le frecce rappresentano dipendenze
* cammino minimo: tempo minimo per prototipo funzionante
* tempo di completamento: viene stabilito con metodi empirici oppure statistici

**SPMP**: software project management plan
* gestione dei rischi
* stime
*  control strategu