# Learning Harness

## Step 2 — Learning Method & Workflow

## Step 3 — System Structure & Functional Architecture

**Versione:** 1.0 — Documento di progettazione concettuale  
**Target iniziale:** Studenti universitari STEM, con particolare attenzione alla preparazione di esami scritti e orali.  
**Obiettivo:** Definire il processo di apprendimento e la struttura funzionale del sistema prima di procedere alle specifiche tecniche e al prototipo.

---

# 1. Visione generale del progetto

## 1.1 Il problema

Gli assistenti AI generalisti, come ChatGPT o Claude, sono particolarmente efficaci nel produrre spiegazioni, riassunti e risposte a domande. Tuttavia, non sono progettati specificamente per accompagnare uno studente durante l'intero processo di apprendimento.

Uno studente può caricare slide, PDF, trascrizioni e appunti, richiedere una spiegazione e ricevere una risposta accurata. Questo processo presenta però diversi limiti:

- **Apprendimento passivo:** leggere una spiegazione non significa necessariamente averla compresa o essere capaci di ricostruirla.
    
- **Perdita di attenzione:** durante le generazioni o tra un contenuto e l'altro lo studente può distrarsi, cambiare applicazione o utilizzare lo smartphone.
    
- **Scarsa continuità:** le conversazioni non costituiscono necessariamente un percorso coerente che collega prerequisiti, spiegazioni, esercitazioni e ripassi.
    
- **Informazioni mal calibrate:** l'AI può approfondire eccessivamente argomenti secondari o essere troppo sintetica su concetti complessi.
    
- **Falsa sensazione di competenza:** comprendere una spiegazione mentre la si legge è diverso dal riuscire a ricostruirla autonomamente.
    
- **Mancanza di organizzazione:** lo studente deve spesso gestire autonomamente fonti, pianificazione, avanzamento, esercizi e appunti.
    
- **Materiali finali frammentati:** spiegazioni, chiarimenti e correzioni restano dispersi tra differenti conversazioni.
    

Il progetto nasce per affrontare questi problemi attraverso un ambiente di studio dedicato.

## 1.2 La soluzione proposta

Realizzare un **AI Learning Harness**, un software in cui intelligenza artificiale e studente collaborano attraverso un metodo di studio strutturato, senza ridurre l'esperienza a un chatbot affiancato a un editor.

L'harness organizza le fonti, costruisce le spiegazioni, guida l'elaborazione personale, identifica possibili incomprensioni, supporta le correzioni e pianifica il consolidamento delle conoscenze.

L'interfaccia centrale è costituita da due pannelli:

- **Sinistra — AI Explanation:** una spiegazione strutturata e interattiva, costruita sulle fonti del corso.
    
- **Destra — Student Notes:** uno spazio in cui lo studente deve organizzare e scrivere autonomamente ciò che ha compreso.
    

Durante il percorso il sistema integra verifiche mirate, feedback e possibilità di approfondimento. Al termine, la rielaborazione dello studente viene corretta e integrata per produrre appunti completi, riutilizzabili e collegati alle fonti.

## 1.3 Principio fondamentale

> Non dobbiamo ottimizzare la quantità di informazioni che l'AI riesce a trasferire allo studente. Dobbiamo ottimizzare quanto lo studente riesce a comprendere, ricordare e utilizzare autonomamente.

Il successo del prodotto non coincide con il numero di pagine elaborate, di spiegazioni generate o di appunti completati.

Il risultato principale è lo sviluppo di conoscenze che lo studente può utilizzare anche senza l'assistenza dell'AI.

## 1.4 Le tre responsabilità dell'harness

**Organizzatore**

Raccoglie e organizza il materiale, riconosce le dipendenze tra gli argomenti, definisce priorità e pianifica studio e ripassi.

**Tutor cognitivo**

Produce spiegazioni adattate, sostiene il ragionamento, propone chiarimenti, riconosce potenziali errori e aiuta lo studente a correggerli.

**Valutatore formativo**

Osserva le conoscenze dimostrate, conserva le lacune emerse, pianifica verifiche e distingue la semplice familiarità con il materiale dalla capacità di utilizzarlo autonomamente.

Queste tre responsabilità operano in modo coordinato, non come funzionalità scollegate.

---

# 2. Principi pedagogici e vincoli di prodotto

La ricerca dello Step 1 ha individuato diversi riferimenti: Self-Regulated Learning, Cognitive Load Theory, ICAP, Self-Explanation, Retrieval Practice, Distributed Practice, Worked Examples, Feedback Formativo e Guidance Fading.

Questi riferimenti costituiscono la base scientifica del metodo, senza imporre regole numeriche arbitrarie.

## 2.1 Apprendimento attivo

Lo studente non deve limitarsi a leggere una spiegazione generata dall'AI.

Durante il processo deve rielaborare personalmente le informazioni attraverso scrittura, ragionamento, esempi e successiva verifica.

La scrittura degli appunti costituisce quindi un'attività centrale e necessaria del percorso ordinario.

L'obiettivo non è semplicemente produrre testo, ma rendere esplicita l'interpretazione personale di ciò che viene studiato.

## 2.2 Supporto proporzionato alle conoscenze

Bisogna distinguere tra due condizioni:

1. Lo studente affronta un argomento che non conosce.
    
2. Lo studente affronta un argomento che ha già studiato.
    

Nel primo caso sono necessarie spiegazioni, esempi e collegamenti con i prerequisiti. Non avrebbe senso richiedere una ricostruzione autonoma di conoscenze mai acquisite.

Nel secondo caso diventa maggiormente utile promuovere il recupero dalla memoria, gli esercizi, l'individuazione degli errori e l'applicazione pratica.

Il sistema deve progressivamente ridurre l'assistenza quando lo studente dimostra maggiore padronanza, mantenendo sempre la possibilità di richiedere chiarimenti.

Questo principio è riconducibile al _Guidance Fading_ e all'_Expertise Reversal Effect_.

## 2.3 Centralità dello studente

L'AI non deve sostituirsi allo studente nelle attività cognitive essenziali.

Può automatizzare organizzazione, ricerca nelle fonti, preparazione delle spiegazioni, confronto delle risposte e programmazione dei ripassi.

La comprensione, la rielaborazione e il ragionamento devono invece rimanere attività dello studente.

Il sistema può facilitare l'inizio di una sessione e aiutare chi incontra difficoltà, ma non può garantire l'apprendimento in assenza di partecipazione attiva.

## 2.4 Semplicità dell'interfaccia

La complessità pedagogica deve essere gestita principalmente dall'harness.

Lo studente non dovrebbe dover selezionare continuamente tra numerose metodologie, modalità di feedback, agenti o strumenti.

L'esperienza deve rimanere comprensibile, coerente e concentrata sulle attività di studio.

L'obiettivo è avere **un'interfaccia semplice con un metodo di apprendimento sofisticato**, non un insieme di funzionalità AI presentate attraverso decine di pulsanti.

## 2.5 Interventi di qualità

L'AI non deve interrompere continuamente lo studente.

Le domande devono essere giustificate dal contenuto, dal momento della sessione e dalle possibili incomprensioni.

Il feedback dovrebbe essere concentrato in una fase coerente del lavoro, evitando commenti invasivi durante la scrittura.

Una fase di feedback può contenere più domande, qualora necessario, ma non deve trasformarsi in una sequenza indefinita di interrogazioni.

## 2.6 Separazione tra appunti e apprendimento

Il sistema mantiene due risultati distinti:

**Knowledge Artifact:** gli appunti finali prodotti dallo studente e consolidati con l'assistenza dell'AI.

**Learning State:** le evidenze disponibili sulla comprensione dello studente, sugli errori commessi e sugli argomenti che richiedono ripasso.

Gli appunti possono essere completi e corretti anche quando lo studente presenta ancora lacune.

Il miglioramento del documento finale non deve quindi essere confuso con l'avvenuta acquisizione delle conoscenze.

---

# STEP 2 — DEFINIZIONE DEL METODO DI STUDIO

# 3. Struttura generale: due percorsi

Il metodo prevede due percorsi principali.

## Percorso A — Lecture by Lecture

Dedicato a studenti che stanno affrontando una materia per la prima volta o che vogliono seguirla progressivamente, lezione dopo lezione.

La priorità è acquisire conoscenze nuove, costruire modelli mentali corretti e sviluppare appunti personali.

## Percorso B — Exam Preparation

Dedicato a studenti che hanno già affrontato almeno parte della materia e vogliono prepararsi per l'esame.

La priorità è valutare le conoscenze esistenti, individuare lacune, consolidare la memoria e sviluppare la capacità di risolvere problemi o rispondere autonomamente.

I due percorsi condividono lo stesso ambiente di studio e lo stesso metodo di elaborazione attiva.

Non rappresentano due applicazioni separate.

Un argomento completamente sconosciuto può richiedere una spiegazione guidata anche durante Exam Preparation. Analogamente, un argomento già conosciuto può essere trattato con un recupero rapido durante Lecture by Lecture.

**La modalità definisce l'obiettivo generale; il livello di conoscenza determina il supporto necessario per il singolo argomento.**

---

# 4. Onboarding e creazione del percorso

Il primo contatto deve richiedere poche informazioni essenziali.

## 4.1 Selezione dell'obiettivo

Lo studente indica se desidera:

- Studiare progressivamente una materia.
    
- Prepararsi per un esame.
    

In seguito può fornire informazioni rilevanti come nome del corso, programma, data dell'esame e modalità di valutazione.

La raccolta dei dettagli deve essere progressiva, evitando questionari iniziali eccessivamente lunghi.

## 4.2 Disponibilità del materiale

Il sistema chiede esplicitamente:

**Hai già il materiale del corso?**

Sono previste tre condizioni.

**Materiale completo:** lo studente carica PDF, slide, dispense, trascrizioni, appunti, registrazioni o altri materiali pertinenti.

**Materiale parziale:** lo studente carica quanto disponibile e il sistema identifica le sezioni apparentemente mancanti.

**Nessun materiale:** si parte dal programma del corso, dagli argomenti indicati o da fonti accademiche attendibili reperibili. Il sistema deve chiarire quando non può ricostruire fedelmente i contenuti specifici del professore.

La disponibilità delle fonti è indipendente dalla conoscenza effettiva dello studente.

## 4.3 Informazioni per la pianificazione

Quando disponibili, possono essere considerate:

- Data e tipologia dell'esame.
    
- Disponibilità settimanale.
    
- Calendario accademico e impegni personali.
    
- Priorità tra diverse materie.
    
- Livello di preparazione iniziale.
    
- Eventuali vincoli o preferenze già emerse durante lo studio.
    

Le informazioni non devono necessariamente essere richieste tutte all'inizio.

Il sistema dovrebbe essere in grado di proporre un primo percorso anche con dati incompleti, segnalandone i limiti.

---

# 5. Preparazione delle fonti e organizzazione della materia

Questa fase è comune ai due percorsi.

## 5.1 Acquisizione delle informazioni

L'harness analizza le fonti disponibili e identifica:

- Struttura generale del corso.
    
- Argomenti e sottoargomenti.
    
- Concetti fondamentali.
    
- Prerequisiti e relazioni tra i concetti.
    
- Definizioni, teoremi, formule, esempi e dimostrazioni.
    
- Esercizi presenti nel materiale.
    
- Eventuali indicazioni del professore sulle modalità d'esame.
    

Per i materiali molto grandi, il sistema deve costruire una rappresentazione strutturata e ricercabile, evitando di dipendere dalla presenza di tutti i documenti contemporaneamente nel contesto del modello.

## 5.2 Gerarchia delle fonti

La fonte principale del percorso universitario dovrebbe essere il materiale specifico del corso, quando disponibile.

Le fonti esterne svolgono un ruolo di integrazione, chiarimento e controllo.

In caso di discrepanze tra slide, trascrizioni, appunti e riferimenti esterni, il sistema deve segnalarle anziché correggerle silenziosamente.

Bisogna poter distinguere una formulazione adottata dal professore da una spiegazione aggiuntiva introdotta dall'AI.

## 5.3 Mappa concettuale

Il materiale viene organizzato secondo una gerarchia:

**Materia → Moduli → Lezioni → Sottomoduli → Concetti**

Le dipendenze concettuali possono attraversare questa gerarchia.

Per esempio:

_Distributed Systems → Logical Clocks → Happened-Before → Lamport Clocks_

Un concetto può richiedere conoscenze appartenenti a lezioni precedenti o ad altri corsi.

Questa mappa sostiene la pianificazione, le spiegazioni, il recupero attivo e la successiva individuazione delle lacune.

## 5.4 Suddivisione in blocchi didattici

Le lezioni vengono suddivise in unità concettualmente coerenti.

La suddivisione non deve dipendere rigidamente dal numero di parole o dai minuti di lettura.

Un blocco può essere breve quando presenta una definizione semplice, oppure articolato quando affronta un teorema, una dimostrazione o un problema complesso.

Ogni unità dovrebbe possedere:

- Un obiettivo di comprensione.
    
- Un insieme identificabile di concetti.
    
- Le fonti necessarie.
    
- Eventuali prerequisiti.
    
- Una spiegazione o attività principale.
    
- Un punto naturale di completamento.
    

Il passaggio tra spiegazione, elaborazione e verifica segue principalmente **confini concettuali**, non timer prestabiliti.

---

# 6. Il ciclo centrale di apprendimento

Questo ciclo rappresenta il cuore dell'applicazione e viene riutilizzato in entrambi i percorsi.

**Preparazione → Spiegazione → Self Notes → Feedback → Revisione → Merge → Consolidamento**

## 6.1 Preparazione del blocco

Prima di iniziare, il sistema identifica l'obiettivo didattico e valuta le informazioni disponibili sulla preparazione dello studente.

Se emergono prerequisiti fondamentali non ancora verificati, può proporre un controllo breve e mirato.

Il pretesting deve essere utilizzato quando è didatticamente appropriato, non come requisito rigido prima di ogni contenuto.

Le domande sui prerequisiti servono a comprendere come spiegare l'argomento, non a impedire automaticamente l'accesso allo studio.

## 6.2 First Comprehension Node — Spiegazione

Nel pannello sinistro viene presentata una spiegazione generata a partire dalle fonti.

La spiegazione deve:

- Rispettare il programma e il materiale del corso.
    
- Adattarsi alle conoscenze pregresse.
    
- Essere sufficientemente completa.
    
- Utilizzare esempi, formule, immagini e schemi quando utili.
    
- Evidenziare relazioni tra concetti.
    
- Evitare introduzioni superflue e dettagli non pertinenti.
    
- Permettere approfondimenti contestuali.
    

Lo studente deve poter selezionare un passaggio della spiegazione e chiedere:

- Un chiarimento.
    
- Un esempio alternativo.
    
- Una spiegazione più dettagliata.
    
- Una riformulazione più semplice.
    
- Un collegamento con un argomento precedente.
    
- Una verifica rispetto alla fonte originale.
    

Le risposte devono apparire all'interno dell'esperienza di studio, senza obbligare lo studente a spostarsi in una chat indipendente.

Durante il primo apprendimento, la spiegazione deve essere sufficientemente guidata. Non si devono nascondere informazioni necessarie a comprendere un argomento mai visto.

## 6.3 Self Notes — Elaborazione personale

Contemporaneamente alla spiegazione, nel pannello destro lo studente costruisce i propri appunti.

Questa è una fase obbligatoria del percorso ordinario.

Lo studente non deve limitarsi a copiare il testo dell'AI, ma costruire una rielaborazione personale che possa comprendere:

- Definizioni con parole proprie.
    
- Spiegazioni causali.
    
- Esempi.
    
- Collegamenti con argomenti precedenti.
    
- Formule e loro interpretazione.
    
- Ragionamenti e passaggi di esercizi.
    
- Dubbi o aspetti non ancora compresi.
    

Lo studente è libero di organizzare titoli, sottotitoli e struttura degli appunti.

Il pannello sinistro fornisce il riferimento didattico, mentre quello destro rappresenta il lavoro personale.

La scrittura non deve essere trasformata in un esercizio di trascrizione.

Se lo studente non riesce a procedere, può richiedere una spiegazione aggiuntiva, un indizio o un esempio, per poi riprendere la rielaborazione.

L'AI non deve completare automaticamente gli appunti mentre lo studente sta ancora costruendo il proprio ragionamento.

## 6.4 Completamento della prima elaborazione

Quando lo studente considera conclusa la propria rielaborazione, avvia una fase di feedback.

Il sistema analizza il testo confrontandolo con:

- Le fonti di riferimento.
    
- Gli obiettivi del blocco.
    
- I concetti fondamentali.
    
- Le precedenti conoscenze dimostrate.
    
- Gli eventuali dubbi emersi durante la spiegazione.
    

Il sistema non interpreta automaticamente un testo corretto come prova definitiva di comprensione.

## 6.5 Feedback Node — Iterazione di domande

Viene eseguita una **singola fase di revisione mirata** sul blocco studiato.

Durante questa fase possono essere proposte una o più domande, selezionate in base alle lacune effettivamente rilevate e alla rilevanza didattica.

Le domande possono servire a:

- Verificare un passaggio non sufficientemente spiegato.
    
- Evidenziare una contraddizione.
    
- Chiarire un errore concettuale.
    
- Richiedere un esempio concreto.
    
- Controllare la comprensione di una formula.
    
- Far emergere un collegamento non compreso.
    
- Verificare se una conclusione deriva correttamente dalle premesse.
    

Le domande devono essere prevalentemente aperte e richiedere ragionamento, evitando che lo studente possa superare la verifica semplicemente indovinando.

**Il sistema non deve porre domande banali soltanto per mantenere attiva l'interazione.**

Se la rielaborazione è soddisfacente e non emergono lacune rilevanti, la revisione può essere minima.

### Gestione delle risposte errate

Quando una risposta è sbagliata, il sistema dovrebbe:

1. Identificare la natura dell'errore.
    
2. Offrire, se utile, un indizio o una domanda di chiarimento.
    
3. Consentire un nuovo tentativo.
    
4. Fornire una spiegazione esplicita quando il supporto indiretto non è sufficiente.
    

L'obiettivo non è trattenere indefinitamente la risposta corretta.

La procedura socratica è uno strumento pedagogico, non un obbligo universale.

Tutta l'interazione rimane parte della stessa fase di revisione; non viene avviato un nuovo ciclo completo per ogni errore.

## 6.6 Note Revision & Merge

Al termine della verifica, il sistema utilizza:

- Appunti iniziali dello studente.
    
- Domande poste dal tutor.
    
- Risposte dello studente.
    
- Errori e chiarimenti emersi.
    
- Fonti originali.
    
- Eventuali approfondimenti effettuati.
    

Su questa base propone una versione consolidata degli appunti.

Il merge deve:

- Conservare la struttura e le formulazioni valide dello studente.
    
- Correggere gli errori effettivi.
    
- Completare le lacune importanti.
    
- Integrare informazioni emerse durante il feedback.
    
- Evitare ripetizioni inutili.
    
- Mantenere riferimenti alle fonti.
    
- Consentire allo studente di rivedere e accettare le modifiche.
    

Il risultato deve essere un documento completo e utilizzabile per i ripassi successivi.

**Il merge non deve cancellare la storia dell'apprendimento.**

Un errore corretto negli appunti rimane un'informazione utile per il sistema di valutazione e ripasso.

## 6.7 Consolidamento e passaggio successivo

Dopo il merge, l'unità viene registrata come studiata e il sistema aggiorna il profilo di apprendimento.

Non significa necessariamente che il concetto sia già padroneggiato.

Il sistema può programmare una verifica successiva, collegarla a un altro argomento o inserirla nelle attività di ripasso.

La transizione alla lezione seguente deve essere fluida.

Eventuali lacune non critiche possono essere conservate e riprese successivamente, mentre quelle che compromettono direttamente i prerequisiti della lezione successiva richiedono particolare attenzione.

---

# 7. Percorso A — Lecture by Lecture

## 7.1 Obiettivo

Accompagnare uno studente nell'apprendimento progressivo di un corso universitario, anche quando non possiede una conoscenza iniziale della materia.

Il percorso deve favorire la costruzione graduale delle conoscenze e la produzione di appunti completi durante lo studio.

## 7.2 Pipeline

**A1 — Acquisizione delle fonti**

Lo studente carica i materiali disponibili e indica il corso da affrontare.

**A2 — Analisi dei prerequisiti**

Il sistema identifica conoscenze fondamentali richieste dal programma.

Per esempio, prima di affrontare determinati algoritmi può verificare concetti relativi a grafi e strutture dati.

Si utilizzano brevi verifiche diagnostiche, limitate agli aspetti rilevanti.

**A3 — Organizzazione e pianificazione**

L'harness costruisce la struttura del corso, divide le lezioni in sottomoduli e propone un piano compatibile con la disponibilità dello studente.

Lo studente può consultare una panoramica degli argomenti e del progresso.

**A4 — Spiegazione guidata**

Si avvia il primo blocco concettuale.

L'AI utilizza spiegazioni sufficientemente approfondite, esempi guidati e collegamenti con i prerequisiti.

**A5 — Self Notes**

Lo studente scrive la propria rielaborazione nel pannello destro.

Può approfondire il testo di sinistra, fare domande e richiedere chiarimenti.

**A6 — Feedback**

Conclusa la prima elaborazione, il sistema identifica potenziali incomprensioni e propone domande mirate.

**A7 — Merge**

Gli appunti vengono revisionati, integrati e consolidati.

**A8 — Progress Tracking**

Il sistema registra i contenuti studiati, le lacune, il progresso e le informazioni utili alla pianificazione futura.

**A9 — Lezione successiva e ripassi**

Si prosegue con i contenuti successivi, inserendo opportunamente verifiche su argomenti già affrontati.

## 7.3 Caratteristiche distintive

Il percorso Lecture by Lecture privilegia:

- Acquisizione iniziale delle conoscenze.
    
- Spiegazioni più guidate.
    
- Costruzione progressiva della struttura della materia.
    
- Connessioni con i prerequisiti.
    
- Creazione di appunti personali da zero.
    
- Consolidamento distribuito nel tempo.
    

La difficoltà delle attività deve crescere insieme alla preparazione.

---

# 8. Percorso B — Exam Preparation

## 8.1 Obiettivo

Supportare uno studente che deve sostenere un esame e possiede già una conoscenza almeno parziale della materia.

Il sistema non deve presumere che tutti gli argomenti siano noti, ma nemmeno obbligare lo studente a ripetere integralmente contenuti già padroneggiati.

## 8.2 Pipeline

**B1 — Acquisizione del programma d'esame**

Il sistema raccoglie programma, materiale, appunti, esercizi e, quando disponibili, prove o indicazioni del professore.

Viene identificato il formato dell'esame: scritto, orale, pratico o misto.

**B2 — Diagnosi delle conoscenze**

Si propone una valutazione iniziale, adattata al programma e possibilmente costituita da domande aperte, esercizi o richieste di spiegazione.

Le prove non devono essere necessariamente lunghe, ma sufficientemente rappresentative per orientare il percorso.

La diagnosi permette di individuare:

- Argomenti già conosciuti.
    
- Argomenti ricordati in modo incompleto.
    
- Errori ricorrenti.
    
- Argomenti mai studiati.
    
- Abilità richieste dall'esame ma non ancora dimostrate.
    

L'autovalutazione può integrare, ma non sostituire, le prestazioni osservate.

**B3 — Pianificazione per priorità**

L'harness organizza gli argomenti in funzione di lacune, importanza, dipendenze concettuali e tempo disponibile.

La priorità non coincide necessariamente con l'ordine originale delle lezioni.

**B4 — Studio e consolidamento mirato**

Lo studente utilizza la consueta interfaccia a due pannelli.

A sinistra trova una spiegazione calibrata rispetto alle conoscenze già possedute: può essere sintetica, approfondita oppure completamente guidata.

A destra produce una rielaborazione personale.

Se possiede appunti precedenti, può consultarli o importarli come materiale di riferimento. Non è necessario riscrivere meccanicamente ciò che conosce già, ma deve comunque produrre un contributo attivo quando un argomento viene affrontato.

Per esempio, può ricostruire una definizione, spiegare un meccanismo, risolvere un problema o motivare un passaggio.

**B5 — Feedback e merge**

Il sistema applica il medesimo ciclo di revisione e consolidamento utilizzato nel percorso Lecture by Lecture.

**B6 — Esercitazione e recupero attivo**

Questa fase assume un peso maggiore rispetto al primo percorso.

Le attività includono:

- Domande aperte.
    
- Esercizi simili a quelli del professore.
    
- Problemi che richiedono più passaggi.
    
- Collegamenti tra argomenti.
    
- Ricostruzioni di formule e dimostrazioni.
    
- Domande di ragionamento.
    
- Simulazioni di esame orale.
    

Gli esercizi ufficiali forniti dal professore dovrebbero avere una priorità particolare.

Gli esercizi aggiuntivi generati dall'AI devono essere riconoscibili come tali.

**B7 — Ripasso distribuito**

Gli argomenti precedentemente studiati vengono riproposti secondo una pianificazione di recupero attivo.

Le verifiche possono combinare concetti appartenenti a moduli differenti, soprattutto quando è importante distinguere tra procedure o principi simili.

**B8 — Simulazione dell'esame**

Il sistema propone prove coerenti con la modalità di valutazione.

Durante una simulazione lo studente dovrebbe poter lavorare senza il normale supporto esplicativo dell'AI.

Terminata la prova, l'harness analizza gli errori e aggiorna le priorità di ripasso.

## 8.3 Caratteristiche distintive

Il percorso Exam Preparation privilegia:

- Diagnosi iniziale più approfondita.
    
- Studio delle lacune.
    
- Recupero dalla memoria.
    
- Minore quantità di spiegazioni ridondanti.
    
- Esercitazioni basate sull'esame.
    
- Verifiche cumulative.
    
- Simulazioni e preparazione all'autonomia.
    

Se un argomento è completamente sconosciuto, viene affrontato con il livello di guida necessario per il primo apprendimento.

---

# 9. Pianificazione e organizzazione nel tempo

## 9.1 Organizzazione settimanale

La pianificazione dovrebbe essere costruita principalmente su obiettivi settimanali, suddivisibili in attività giornaliere.

Questo permette di evitare programmi eccessivamente rigidi, nei quali una singola giornata saltata compromette il resto del calendario.

Il sistema deve considerare la disponibilità effettiva dello studente e la difficoltà prevista delle attività.

## 9.2 Pianificazione dinamica

Dopo ogni sessione, l'harness può aggiornare il piano sulla base di:

- Argomenti completati.
    
- Difficoltà effettivamente incontrate.
    
- Tempo impiegato.
    
- Errori e lacune.
    
- Verifiche superate o non superate.
    
- Disponibilità residua.
    
- Avvicinamento dell'esame.
    

Le attività non completate devono poter essere redistribuite senza accumulare automaticamente una quantità ingestibile di lavoro arretrato.

La ripianificazione rimane una proposta del sistema, non un vincolo imposto allo studente.

## 9.3 Supporto all'inizio delle sessioni

Un ulteriore obiettivo è ridurre la difficoltà di iniziare a studiare.

L'harness può proporre un'attività iniziale chiara e di dimensioni contenute, indicando quale argomento affrontare e quale risultato raggiungere.

Può anche conservare il punto esatto in cui la sessione precedente è stata interrotta.

Lo studente non dovrebbe ogni volta dover ricostruire manualmente cosa stava facendo.

## 9.4 Retention e ripasso

Il sistema integra una pianificazione del recupero attivo distribuito nel tempo.

Non deve limitarsi a ricordare che un argomento è stato letto.

Dovrebbe considerare quando è stato verificato, quali errori sono emersi e come lo studente ha risposto in assenza di suggerimenti.

Le attività possono comprendere:

- Richiamo di definizioni e concetti.
    
- Ricostruzione di spiegazioni.
    
- Domande su errori precedenti.
    
- Esercizi applicativi.
    
- Collegamenti tra argomenti.
    
- Problemi misti.
    

Algoritmi di scheduling della memoria come FSRS possono essere valutati come possibile soluzione tecnica, ma non costituiscono un requisito obbligatorio del metodo.

---

# 10. Attenzione e gestione della continuità

## 10.1 Riduzione dei tempi morti

Uno dei problemi che il progetto intende affrontare riguarda la perdita di attenzione durante l'attesa di generazioni AI.

L'harness dovrebbe minimizzare le situazioni in cui lo studente rimane inattivo aspettando che venga preparato il materiale successivo.

È possibile organizzare anticipatamente i blocchi e predisporre i contenuti successivi mentre lo studente lavora.

Questo deve ridurre le attese senza introdurre continuamente nuove attività.

## 10.2 Cambi di attività strutturali

Lo studio può alternare:

**Spiegazione → Rielaborazione → Ragionamento → Revisione**

Queste transizioni devono dipendere dalla struttura didattica.

Un teorema complesso può richiedere una spiegazione lunga e continuativa. Una definizione semplice può essere seguita da un esempio o da una breve verifica.

Non è necessario interrompere lo studente ogni dieci minuti.

## 10.3 Interruzioni e feedback

Il tutor dovrebbe evitare di intervenire durante una fase di scrittura produttiva, salvo necessità particolari.

La maggior parte degli interventi automatici viene concentrata nelle fasi di revisione previste.

Le richieste volontarie dello studente rimangono disponibili durante tutta la sessione.

## 10.4 Pause

L'harness può suggerire pause nei punti di completamento naturale.

La durata deve essere flessibile e non dipendere da una presunta soglia universale dell'attenzione.

Le pause dovrebbero essere proposte in modo discreto e non invasivo.

Un esempio potrebbe essere:

_Hai completato un blocco impegnativo. Vuoi fare una breve pausa prima del prossimo?_

La decisione rimane allo studente.

## 10.5 Ripresa della sessione

Dopo una pausa o un'interruzione, il sistema può presentare una breve contestualizzazione:

- Cosa è stato affrontato.
    
- Cosa è stato compreso o resta da chiarire.
    
- Qual è la prossima attività.
    

Lo scopo è facilitare la ripresa senza costringere lo studente a ricominciare.

Non bisogna presumere di poter misurare direttamente l'attenzione attraverso semplici segnali come tempo di inattività, velocità di scrittura o cambi di finestra.

Questi segnali possono indicare problemi, ma non dimostrano autonomamente la perdita di concentrazione.

---

# 11. Come misurare l'apprendimento

Il sistema deve distinguere le attività svolte dalle competenze dimostrate.

## 11.1 Indicatori di progresso

Gli indicatori possono comprendere:

- Unità studiate.
    
- Appunti completati.
    
- Verifiche effettuate.
    
- Errori concettuali rilevati.
    
- Miglioramento nelle successive verifiche.
    
- Capacità di recuperare informazioni senza assistenza.
    
- Capacità di applicare concetti a situazioni nuove.
    
- Mantenimento delle conoscenze a distanza di tempo.
    

## 11.2 Stati concettuali

Ogni concetto può essere rappresentato attraverso stati descrittivi, per esempio:

- Non affrontato.
    
- In apprendimento.
    
- Studiato, ma non verificato.
    
- Comprensione iniziale dimostrata.
    
- Richiede consolidamento.
    
- Padronanza sostenuta da verifiche ripetute.
    

Questi stati sono indicazioni operative, non giudizi definitivi sulla conoscenza dello studente.

Il sistema deve conservarne le evidenze.

## 11.3 Non introdurre blocchi artificiali

Un modello estremamente rigido, che impedisca sempre di passare al modulo successivo senza superare un test, rischia di compromettere il flusso di studio.

È preferibile distinguere tra:

- Lacune critiche per la comprensione dei contenuti successivi.
    
- Lacune non critiche che possono essere affrontate durante i ripassi.
    

Le prime richiedono maggiore attenzione immediata. Le seconde possono essere registrate e recuperate successivamente.

---

# STEP 3 — STRUTTURA DELL'HARNESS

# 12. Obiettivo dello Step 3

Lo Step 3 traduce il metodo definito nello Step 2 in una struttura funzionale.

Non ha ancora lo scopo di scegliere framework, database, servizi cloud o protocolli specifici.

Deve invece chiarire:

1. Quali componenti logici servono.
    
2. Quali informazioni utilizzano.
    
3. Quali risultati producono.
    
4. Come comunicano.
    
5. Quali condizioni determinano il passaggio tra le fasi.
    
6. Come queste funzionalità vengono integrate nell'esperienza dello studente.
    

La struttura deve rimanere modulare, affinché il metodo pedagogico possa evolvere senza richiedere una riprogettazione totale dell'applicazione.

---

# 13. Struttura generale del sistema

L'architettura concettuale viene divisa in quattro macrocomponenti, ispirati alla struttura degli Intelligent Tutoring Systems.

## 13.1 Domain Model — Modello della materia

Rappresenta ciò che deve essere studiato.

Comprende:

- Fonti e relativi riferimenti.
    
- Organizzazione del corso.
    
- Gerarchia degli argomenti.
    
- Dipendenze tra concetti.
    
- Prerequisiti.
    
- Definizioni ed esempi.
    
- Esercizi disponibili.
    
- Relazioni tra contenuti e obiettivi d'esame.
    

Il Domain Model permette al sistema di costruire spiegazioni coerenti e di recuperare le informazioni necessarie.

## 13.2 Student Model — Modello dello studente

Rappresenta le informazioni disponibili sul processo di apprendimento.

Comprende:

- Conoscenze iniziali.
    
- Progressi.
    
- Appunti e revisioni.
    
- Risposte alle verifiche.
    
- Errori ricorrenti.
    
- Evidenze di padronanza.
    
- Argomenti da ripassare.
    
- Calendario e disponibilità.
    
- Preferenze esplicite di studio.
    

Non dovrebbe costruire diagnosi cognitive o psicologiche arbitrarie.

Le informazioni devono essere comprensibili, modificabili quando opportuno e collegate a osservazioni verificabili.

## 13.3 Pedagogical Engine — Motore pedagogico

È il componente che coordina le decisioni didattiche.

Sulla base del Domain Model e dello Student Model determina:

- Quale argomento proporre.
    
- Quale livello di spiegazione utilizzare.
    
- Se servono chiarimenti sui prerequisiti.
    
- Quando proporre una verifica.
    
- Quali domande selezionare.
    
- Quale feedback fornire.
    
- Quando ridurre l'assistenza.
    
- Quali argomenti riproporre.
    
- Come aggiornare la pianificazione.
    

Questo componente rappresenta la differenza principale rispetto a un chatbot generalista.

Non è un semplice prompt che chiede al modello di comportarsi da professore: è un insieme coerente di regole, informazioni e decisioni didattiche.

## 13.4 Interaction Layer — Ambiente di studio

È il livello attraverso il quale lo studente interagisce con l'harness.

Comprende:

- Interfaccia a due pannelli.
    
- Navigazione tra lezioni e blocchi.
    
- Editor personale.
    
- Approfondimenti contestuali.
    
- Feedback.
    
- Revisione del merge.
    
- Verifiche.
    
- Visualizzazione del progresso.
    
- Pianificazione.
    

L'interfaccia presenta soltanto le funzionalità pertinenti al momento della sessione, evitando di esporre tutta la complessità del sistema.

---

# 14. Nodi funzionali dell'harness

Le macrocomponenti vengono articolate in nodi con responsabilità definite.

I nodi rappresentano funzioni logiche, non necessariamente processi, agenti o servizi software separati.

|Nodo|Responsabilità|Output principale|
|---|---|---|
|N1 — Course Setup|Raccoglie obiettivo, percorso e informazioni iniziali|Profilo del percorso|
|N2 — Source Manager|Acquisisce, organizza e indicizza le fonti|Libreria delle fonti|
|N3 — Knowledge Mapper|Ricostruisce argomenti, lezioni e prerequisiti|Mappa della materia|
|N4 — Diagnostic Engine|Valuta le conoscenze iniziali e le lacune|Profilo diagnostico|
|N5 — Study Planner|Organizza attività, priorità e ripassi|Piano di studio|
|N6 — Explanation Engine|Produce spiegazioni adattate e verificabili|Blocchi didattici|
|N7 — Student Workspace|Gestisce la rielaborazione personale|Appunti dello studente|
|N8 — Feedback Engine|Esamina gli appunti e guida la revisione|Domande, risposte ed errori|
|N9 — Notes Consolidator|Integra le correzioni e crea gli appunti finali|Appunti consolidati|
|N10 — Assessment Engine|Gestisce verifiche, esercizi e simulazioni|Evidenze di apprendimento|
|N11 — Progress & Retention|Registra progressi e pianifica recuperi|Stato di apprendimento|
|N12 — Session Coordinator|Gestisce continuità, transizioni e pause|Stato della sessione|

Questa divisione ha lo scopo di chiarire le responsabilità. Nello Step 4 alcune funzioni potranno essere accorpate.

---

# 15. Approfondimento dei nodi principali

## 15.1 Source Manager

Il Source Manager gestisce il materiale.

Deve supportare concettualmente documenti, slide, trascrizioni, appunti ed eventuali contenuti audiovisivi.

Quando un'informazione viene estratta da una fonte, deve mantenere un collegamento al documento e, ove possibile, alla posizione originale.

Le slide possono fornire immagini, schemi e formule da riutilizzare nelle spiegazioni.

Il sistema può anche produrre autonomamente schemi, diagrammi SVG o altri supporti visivi, purché siano pertinenti al contenuto.

Quando vengono utilizzate informazioni esterne, deve esserne mantenuta la provenienza.

### Organizzazione gerarchica della conoscenza

Per gestire materiali di grandi dimensioni, la conoscenza può essere organizzata su più livelli:

**Livello 1 — Contesto essenziale**

Obiettivo del percorso, vincoli pedagogici, unità corrente e informazioni indispensabili per l'interazione.

**Livello 2 — Contesto del modulo**

Riepilogo strutturato della lezione, concetti, prerequisiti e informazioni pertinenti.

**Livello 3 — Fonti di dettaglio**

Documenti originali e contenuti specialistici recuperabili quando necessari.

Questa organizzazione limita la duplicazione e riduce la dipendenza da contesti eccessivamente grandi.

Non deve però sostituire il controllo delle fonti originali nei passaggi importanti.

## 15.2 Knowledge Mapper

Il Knowledge Mapper produce una rappresentazione coerente della materia.

Deve riconoscere:

- Struttura delle lezioni.
    
- Dipendenze.
    
- Concetti fondamentali.
    
- Concetti secondari.
    
- Relazioni tra argomenti.
    
- Obiettivi didattici.
    

Il risultato permette di evitare che le spiegazioni vengano generate come sezioni isolate.

Quando un concetto richiede conoscenze precedenti, l'harness può richiamarle o verificarle.

## 15.3 Explanation Engine

L'Explanation Engine genera e adatta il contenuto visibile nel pannello sinistro.

Utilizza:

- Contenuto delle fonti.
    
- Obiettivo didattico.
    
- Conoscenze pregresse dello studente.
    
- Eventuali errori già osservati.
    
- Caratteristiche della disciplina.
    

Può generare spiegazioni di diversa profondità, esempi guidati, confronti, visualizzazioni e approfondimenti.

### Gestione delle discipline STEM

La struttura generale rimane invariata, ma la spiegazione cambia in base al contenuto.

Per matematica può comprendere formule, dimostrazioni e procedimenti.

Per algoritmi può utilizzare pseudocodice, diagrammi ed esempi di esecuzione.

Per sistemi operativi può presentare sequenze di eventi e scenari concorrenti.

Per cybersecurity può introdurre configurazioni, meccanismi e casi applicativi.

L'adattamento della spiegazione non richiede necessariamente la sostituzione del pannello destro degli appunti.

## 15.4 Student Workspace

Lo Student Workspace rappresenta il luogo principale dell'elaborazione personale.

Deve garantire:

- Scrittura libera.
    
- Organizzazione autonoma delle note.
    
- Possibilità di creare strutture gerarchiche.
    
- Supporto ai contenuti necessari per le discipline STEM.
    
- Conservazione dello stato.
    
- Revisione delle modifiche.
    

Lo studente deve rimanere proprietario della propria rielaborazione.

La presenza del tutor non deve trasformare l'editor in una superficie continuamente riscritta dall'AI.

## 15.5 Feedback Engine

Il Feedback Engine viene attivato quando lo studente conclude una prima fase di rielaborazione oppure richiede esplicitamente un controllo.

Analizza:

- Correttezza concettuale.
    
- Completezza rispetto agli obiettivi.
    
- Coerenza del ragionamento.
    
- Possibili confusioni.
    
- Collegamenti non esplicitati.
    
- Informazioni emerse da precedenti verifiche.
    

L'analisi interna può essere articolata, ma l'interfaccia deve mostrare un feedback semplice e naturale.

Il sistema deve selezionare le questioni più significative, non presentare automaticamente tutti i possibili commenti.

Le domande vengono gestite come un unico episodio di revisione del blocco.

Le risposte prodotte in questo episodio costituiscono informazioni utili per il merge e per il modello dello studente.

## 15.6 Notes Consolidator

Il Notes Consolidator trasforma la rielaborazione iniziale in un documento finale.

Non deve limitarsi a un riassunto della spiegazione AI.

Deve combinare:

**Student Draft + Feedback Dialogue + Verified Sources → Consolidated Notes**

Il risultato deve rispettare la struttura personale dello studente e integrare soprattutto le informazioni necessarie per correggere o chiarire i concetti.

È opportuno conservare:

- Versione originale.
    
- Proposta di revisione.
    
- Modifiche accettate.
    
- Riferimenti alle fonti.
    
- Eventuali lacune non ancora risolte.
    

Il consolidamento degli appunti non aggiorna automaticamente le conoscenze come padroneggiate.

## 15.7 Assessment Engine

Il sistema di verifica è particolarmente rilevante durante Exam Preparation.

Deve supportare attività differenti in funzione della disciplina e della modalità di valutazione.

Per esempio:

- Domande teoriche aperte.
    
- Esercizi numerici.
    
- Dimostrazioni.
    
- Problemi algoritmici.
    
- Analisi di codice.
    
- Esercizi del professore.
    
- Simulazioni orali.
    

Quando possibile, la valutazione dovrebbe considerare anche il procedimento e non soltanto la risposta finale.

Le correzioni generate dall'AI devono essere considerate fallibili: per contenuti formali e risultati oggettivamente verificabili dovrebbero essere impiegati controlli appropriati.

## 15.8 Progress & Retention

Questo componente mantiene lo storico dell'apprendimento.

Per ogni concetto può conservare:

- Data del primo studio.
    
- Verifiche effettuate.
    
- Esiti.
    
- Errori ricorrenti.
    
- Ultimo recupero autonomo.
    
- Eventuali difficoltà ancora aperte.
    
- Prossima attività proposta.
    

Queste informazioni vengono utilizzate dal planner per distribuire i ripassi e adattare il percorso.

## 15.9 Session Coordinator

Il Session Coordinator gestisce il flusso complessivo.

Determina quale attività è in corso e quali transizioni sono disponibili.

Si occupa anche di mantenere la continuità tra sessioni, supportare pause e riprese e ridurre le attese inutili.

Non deve misurare la concentrazione attraverso un singolo indicatore comportamentale.

---

# 16. Interfaccia principale: Dual-Pane Study Workspace

## 16.1 Struttura

Il workspace centrale presenta stabilmente due aree.

### Pannello sinistro — AI Explanation

Contiene:

- Lezione corrente.
    
- Spiegazione strutturata in blocchi.
    
- Definizioni ed esempi.
    
- Formule e schemi.
    
- Immagini tratte dalle fonti.
    
- Diagrammi generati quando utili.
    
- Riferimenti ai materiali originali.
    

Lo studente può selezionare una parte del testo e richiedere un approfondimento contestuale.

L'esperienza non deve comportarsi come una conversazione continua separata dallo studio.

### Pannello destro — Student Notes

Contiene gli appunti costruiti dallo studente.

Durante la prima fase è uno spazio di elaborazione personale.

Al termine, diventa il luogo in cui visualizzare e approvare le integrazioni proposte.

La struttura delle note è definita principalmente dallo studente e può essere diversa da quella del testo esplicativo.

## 16.2 Navigazione

L'interfaccia deve fornire una percezione chiara della posizione all'interno del corso:

**Corso → Modulo → Lezione → Blocco corrente**

Non è necessario che l'intera gerarchia sia sempre visibile.

Un sistema di navigazione discreto può mostrare il contesto e consentire di accedere alle altre sezioni.

## 16.3 Modalità contestuali

Le due aree rimangono il riferimento centrale, mentre le attività possono modificare temporaneamente l'interazione.

**Study:** spiegazione e scrittura.

**Review:** domande e correzione del ragionamento.

**Merge:** proposta di integrazione degli appunti.

**Recall:** verifica autonoma, con riduzione temporanea dell'accesso alle risposte.

**Exam Simulation:** attività di valutazione senza assistenza ordinaria.

Queste sono modalità logiche interne, non necessariamente pulsanti o schermate differenti.

## 16.4 Design dell'interazione

Il principio generale è la _progressive disclosure_: mostrare soltanto gli strumenti necessari nel momento in cui servono.

Le domande del tutor devono comparire in modo contestuale.

Il feedback non deve utilizzare una tassonomia complessa visibile allo studente.

L'interfaccia deve evitare elementi decorativi, notifiche inutili e componenti che competono per l'attenzione.

---

# 17. Orchestrazione dei nodi

## 17.1 Percorso generale

**Course Setup → Source Manager → Knowledge Mapper → Diagnostic Engine → Study Planner**

Dopo la preparazione, il percorso passa all'esperienza di studio.

## 17.2 Ciclo di una singola unità

**Explanation Engine → Student Workspace → Feedback Engine → Notes Consolidator → Progress & Retention**

Il Session Coordinator gestisce gli stati e le transizioni tra queste attività.

## 17.3 Comportamento adattivo

Il Pedagogical Engine decide come affrontare un blocco considerando il suo obiettivo e le conoscenze disponibili.

Esempi:

**Concetto nuovo:** spiegazione completa, esempio guidato e rielaborazione personale.

**Concetto parzialmente noto:** spiegazione concentrata sulle difficoltà, rielaborazione e successiva verifica.

**Concetto consolidato:** maggiore attenzione a recupero attivo e applicazione.

**Errore importante:** feedback specifico e chiarimento prima di proseguire.

**Errore non critico:** registrazione per revisione o ripasso successivo.

Non esiste una regola unica applicabile a ogni argomento.

---

# 18. Modello informativo minimo

Lo Step 3 richiede di identificare le entità principali, senza definire ancora lo schema del database.

|Entità|Contenuto|
|---|---|
|Course|Materia, programma, obiettivi, modalità d'esame|
|Source|File, metadati, riferimenti e provenienza|
|Concept|Argomento, prerequisiti, dipendenze|
|Learning Unit|Blocco didattico con obiettivo e fonti|
|Study Plan|Attività, priorità e scadenze|
|Study Session|Stato corrente e attività svolte|
|Explanation|Spiegazione prodotta per l'unità|
|Student Draft|Appunti originali dello studente|
|Feedback Session|Domande, risposte e chiarimenti|
|Consolidated Notes|Versione revisionata degli appunti|
|Learning Evidence|Risultati delle verifiche e osservazioni|
|Student Progress|Stato delle conoscenze e cronologia|
|Review Task|Attività di recupero o ripasso programmata|

Il sistema dovrebbe mantenere relazioni tra questi elementi.

Per esempio, una domanda di verifica dovrebbe essere collegabile al concetto, alla fonte e all'eventuale errore che l'ha motivata.

---

# 19. Gestione della memoria e continuità dell'harness

Il sistema deve conservare informazioni sufficienti a riprendere il percorso senza ricostruirlo ogni volta.

È utile distinguere tre forme di memoria.

## 19.1 Memoria della materia

Contiene la struttura del corso, le fonti, i concetti e le relazioni.

## 19.2 Memoria dello studente

Contiene progressi, lacune, risposte, errori e informazioni pertinenti alla personalizzazione.

## 19.3 Memoria della sessione

Contiene il blocco corrente, lo stato degli appunti, le interazioni recenti e la prossima attività.

Queste informazioni devono essere gestite in maniera selettiva.

Non serve fornire al modello ogni volta l'intera cronologia di tutte le sessioni. Devono essere recuperate le informazioni pertinenti all'attività corrente.

La distinzione tra informazioni essenziali, contesto del modulo e documenti recuperabili permette di ridurre ridondanza e costi, preservando la continuità.

---

# 20. Affidabilità e salvaguardie pedagogiche

## 20.1 Grounding sulle fonti

Le spiegazioni devono essere basate principalmente sui materiali disponibili.

Le integrazioni esterne devono essere distinguibili e, quando rilevante, accompagnate da riferimenti verificabili.

Una discrepanza tra fonti non deve essere nascosta.

## 20.2 Evitare l'eccessiva dipendenza dall'AI

Il tutor dovrebbe preferire indizi e richieste di ragionamento quando lo studente ha già le conoscenze necessarie per rispondere.

Deve però poter fornire spiegazioni complete quando queste sono indispensabili.

La disponibilità delle risposte non deve trasformarsi in un meccanismo che impedisce sistematicamente lo sforzo personale.

## 20.3 Conservare l'autonomia

Lo studente può richiedere chiarimenti, modificare il percorso, riorganizzare gli appunti e consultare le fonti.

Il sistema non deve imporre un metodo talmente rigido da rendere frustrante lo studio.

L'harness propone e accompagna; non sostituisce la responsabilità dello studente.

## 20.4 Valutazione prudente delle competenze

Il sistema può formulare valutazioni formative basate sulle evidenze disponibili.

Non può assumere di conoscere perfettamente lo stato mentale dello studente.

Un testo corretto, un quiz superato o una sessione lunga non sono, isolatamente, dimostrazioni definitive di apprendimento.

---

# 21. Esempi di funzionamento

## 21.1 Studente che affronta per la prima volta Distributed Systems

Lo studente crea il corso e carica slide e trascrizioni.

Il sistema identifica gli argomenti, propone una struttura delle lezioni e verifica alcuni prerequisiti rilevanti.

Viene avviata una lezione sugli orologi logici.

A sinistra compare una spiegazione dei concetti di causalità e _happened-before_.

Lo studente legge e scrive a destra la propria interpretazione, includendo un esempio.

Seleziona un passaggio della spiegazione e chiede un chiarimento su eventi concorrenti.

Dopo aver completato la propria rielaborazione, avvia la revisione.

Il tutor individua una possibile confusione tra ordine logico e ordine temporale reale e pone una domanda mirata.

Lo studente prova a rispondere, riceve un chiarimento e modifica la propria spiegazione.

L'AI propone il merge degli appunti.

Il sistema registra la difficoltà incontrata e programma una verifica successiva.

Lo studente passa al blocco seguente.

## 21.2 Studente che prepara un esame di Algorithms

Lo studente carica programma, slide, appunti e prove d'esame.

Indica la data e la modalità della valutazione.

Il sistema propone una diagnosi iniziale su grafi, strutture dati, complessità e principali algoritmi.

Emergono difficoltà sugli algoritmi di cammino minimo.

Il percorso assegna priorità a quell'argomento.

A sinistra viene proposta una spiegazione focalizzata sulle differenze tra gli algoritmi e sulle condizioni di applicabilità.

A destra lo studente ricostruisce il ragionamento e svolge un esempio.

Durante la revisione emerge una confusione relativa ai pesi negativi.

Il tutor propone una domanda di ragionamento.

Dopo la correzione e il merge, il sistema propone un esercizio simile a quelli del professore.

In una sessione successiva, lo studente affronta un problema misto senza indicazioni su quale algoritmo utilizzare.

Il risultato contribuisce all'aggiornamento del percorso di ripasso e preparazione all'esame.

---

# 22. Prima delimitazione del prototipo

La struttura descritta contiene molte funzionalità, ma il prototipo non deve necessariamente implementarle tutte.

Per testare l'idea pedagogica fondamentale, il primo prototipo dovrebbe concentrarsi su:

1. Creazione di un corso e caricamento di materiale.
    
2. Suddivisione delle fonti in lezioni e blocchi concettuali.
    
3. Interfaccia a due pannelli.
    
4. Spiegazioni fondate sulle fonti.
    
5. Scrittura autonoma degli appunti.
    
6. Approfondimenti contestuali.
    
7. Una fase mirata di feedback.
    
8. Revisione e merge degli appunti.
    
9. Conservazione delle versioni e dei progressi essenziali.
    
10. Una prima verifica dell'apprendimento senza assistenza.
    

Queste funzionalità consentono di verificare la principale ipotesi del prodotto: che un processo integrato di spiegazione, rielaborazione e feedback possa essere più efficace di un utilizzo prevalentemente passivo di un chatbot.

Pianificazione avanzata, simulazioni orali, algoritmi di ripasso sofisticati, integrazione con calendari e personalizzazione comportamentale possono essere sviluppati progressivamente.

La priorità è validare il nucleo dell'esperienza prima di aumentare la complessità.

---

# 23. Decisioni consolidate e ipotesi da validare

## Decisioni di prodotto

Sono considerati elementi centrali della progettazione:

- Target iniziale universitario STEM.
    
- Due percorsi principali: Lecture by Lecture ed Exam Preparation.
    
- Un'unica esperienza di studio basata su due pannelli.
    
- Spiegazione interattiva a sinistra e rielaborazione personale a destra.
    
- Scrittura autonoma come componente obbligatoria del ciclo ordinario.
    
- Un episodio di feedback mirato dopo la prima elaborazione del blocco.
    
- Consolidamento degli appunti attraverso merge.
    
- Distinzione tra qualità degli appunti e apprendimento dimostrato.
    
- Adattamento delle spiegazioni alle conoscenze pregresse.
    
- Organizzazione delle fonti e delle dipendenze concettuali.
    
- Progress tracking e recupero attivo.
    
- Interfaccia semplice e controllo delle interruzioni.
    

## Ipotesi da validare

Restano questioni sperimentali:

- Quanto debba essere lungo un blocco didattico nelle diverse discipline.
    
- Quante domande siano appropriate durante una revisione.
    
- Quale politica di feedback produca migliori risultati.
    
- Quanto l'obbligo di scrittura migliori l'apprendimento rispetto ad altre forme di elaborazione.
    
- Quale livello di assistenza sia ottimale per diverse conoscenze iniziali.
    
- Come distribuire ripassi ed esercitazioni.
    
- Come proporre pause senza interrompere il ragionamento.
    
- Quali segnali siano realmente utili per personalizzare il percorso.
    
- Se e quando la correzione guidata degli appunti migliori la ritenzione a lungo termine.
    

Queste ipotesi non devono essere trasformate prematuramente in vincoli rigidi.

---

# 24. Confini dello Step 4

Il documento definisce il comportamento desiderato, ma non decide ancora:

- Stack tecnologico.
    
- Framework dell'interfaccia.
    
- Modelli LLM da utilizzare.
    
- Architettura di deployment.
    
- Database e struttura delle tabelle.
    
- Protocollo di orchestrazione.
    
- Formati interni di rappresentazione.
    
- Implementazione della ricerca nelle fonti.
    
- Algoritmi specifici di scheduling.
    
- Meccanismi di sicurezza e autorizzazione.
    
- API e contratti tra moduli.
    
- Metriche tecniche di prestazione.
    

Queste scelte appartengono al documento di specifica dello Step 4.

---

# 25. Sintesi finale

Il Learning Harness non nasce per rendere più veloce la generazione di spiegazioni, ma per trasformare l'uso dell'intelligenza artificiale in un processo di apprendimento organizzato, attivo e continuativo.

Il metodo si basa su due percorsi distinti per obiettivo, ma unificati da un ciclo centrale:

**Comprendere → Rielaborare → Ragionare → Correggere → Consolidare → Recuperare**

L'ambiente di studio mantiene la spiegazione AI a sinistra e gli appunti dello studente a destra.

L'AI fornisce la struttura della materia, le spiegazioni e il supporto necessario. Lo studente costruisce personalmente la propria comprensione.

Al termine di un'unità, il sistema analizza gli appunti e avvia una revisione mirata, finalizzata a individuare e chiarire le incomprensioni più importanti.

Il merge produce un documento di studio completo, ma non viene confuso con una certificazione dell'apprendimento.

Nel tempo, l'harness conserva le evidenze raccolte, aggiorna la pianificazione, ripropone gli argomenti necessari e riduce l'assistenza quando lo studente dimostra maggiore autonomia.

**Il valore del prodotto non è avere un'AI che studia per lo studente, ma creare un ambiente in cui l'AI rende più efficace il lavoro cognitivo che soltanto lo studente può svolgere.**