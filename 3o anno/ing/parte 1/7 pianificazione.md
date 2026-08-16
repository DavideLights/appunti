# Appunti di Studio: Pianificazione dei Progetti Software (Software Project 
## 1. I Fondamenti della Gestione: Le quattro "P"
La gestione efficace di un progetto software si fonda su quattro pilastri interdipendenti:
1.  **Persone (People):** L'elemento più importante per il successo di un progetto. Il *People Management - Capability Maturity Model (PM-CMM)* gestisce le **risorse umane**. Ci vuole **motivazione e competenze**
2.  **Prodotto (Product):** Identifica le caratteristiche del software da sviluppare (obiettivi commerciali, vincoli tecnici, requisiti funzionali e comportamentali).
3.  **Processo (Process):** Fornisce l'**ossatura metodologica** e le **pratiche di sviluppo** da utilizzare per raggiungere gli obiettivi.
4.  **Progetto (Project):** Definisce l'insieme operativo delle attività da svolgere, mappando tempi, costi, scadenze e compiti da allocare alle persone.
	1. organizzazione team
	2. **legge brooks**: aggiungere piu risorse non sempre accelera lo sviluppo.
		1. Alcune attività sono intrinsecamente sequenziali.
		2. L'aumento di risorse umane comporta una crescita esponenziale dei canali di comunicazione e dei tempi di coordinamento
		3. **es**: *voglio sviluppare in 3 mesi un software che richiede 1 anno di lavoro con una sola persona. Ma se uso 4 sviluppatori invece di 1, ma potrei metterci piu di un anno per completare il progetto.*

---

## 2. Organizzazione e Dinamiche dei Team di Sviluppo

#### A. Chief Programmer Team (Team del Capo-Programmatore)
Struttura altamente centralizzata volta a minimizzare i canali di comunicazione.
*   **Ruoli Chiave:**
    *  *Capo-Programmatore (Chief Programmer):* Un ***tecnico altamente esperto** responsabile della progettazione architetturale e della scrittura del codice critico*. Fa anche da **manager**.
    *  *Programmatore di Back-up:* **Sostituisce il capo-programmatore** in caso di necessità ed è responsabile delle attività di **test e integrazione**.
    *  *Segretario di Programmazione:* Cura la *documentazione tecnica, le metriche e l'archivio dei sorgenti*.
*   **Vantaggi:** Fortissimo abbattimento dei canali di comunicazione.
*   **Svantaggi:** Richiede figure di eccezionale competenza, difficili da reperire.
	* capo-programmatore: diventa il "***valutatore di se stesso***" dato che agisce sia come **progettista** che come **manager**.

#### B. Team Leader & Team Manager (Evoluzione degli Approcci)
Per superare i limiti del Chief Programmer Team, la responsabilità viene divisa in due ruoli distinti:
*   **Team Leader (Technical Management):** Gestisce gli aspetti puramente **tecnologici**, l'architettura e le scelte ingegneristiche.
*   **Team Manager (Nontechnical Management):** Gestisce l'**amministrazione**, le risorse umane, i costi e i vincoli contrattuali.
*  *Risoluzione dei Conflitti, **Project Leader**:* Nel caso in cui si verifichino frizioni decisionali (es. il Team Manager concede le ferie a uno sviluppatore indispensabile per il Team Leader), si introduce un livello superiore rappresentato dal **Project Leader** che coordina tutti.

#### C. Organizzazioni Scalabili (Contenuto Informativo delle Immagini)
Per progetti di dimensioni **medio-grandi** si adottano strutture piramidali:
*   **Struttura Scalabile Standard:** *Project Leader* coordina piu *Team Leaders*. Ogni Team Leader coordina un team di *Programmers*. **Comunicazione gerarchica**, in verticale.
	* Project Leader
		* Team Leaders
			* Programmers
*   **Struttura con Decision-Making Decentralizzato:** Simile alla precedente, ma introduce canali di comunicazione orizzontale diretta tra i Team Leader e cooperazione tra i programmatori dello stesso livello. Questo riduce i colli di bottiglia decisionali e favorisce la flessibilità.

---

## 3. L'Importanza del Project Management
Le statistiche storiche statunitensi sui progetti software (raccolte dal 1984 al 2016) rivelano che:
*   In media, solo il **50.13%** dei progetti viene completato con successo (on-time e nel budget).
*   Il **37.27%** subisce forti ritardi temporali o sforamenti di budget.
*   Il **13%** viene cancellato del tutto prima del completamento a causa di costi insostenibili o scarsa qualità.

### Obiettivo e Componenti della Pianificazione
L'obiettivo è definire un quadro di riferimento controllabile per sviluppare software nei tempi, costi e livelli di qualità stabiliti. Si compone di:
*   **Scoping:** Comprendere il problema e delimitare il lavoro da svolgere.
*   **Stime (Estimation):** Prevedere l'effort (mesi-uomo), la durata temporale e i costi finanziari. Base per la pianificazione delle risorse.
*   **Rischi (Risk Management):** Identificare, valutare e mitigare gli eventi avversi. Aiuta a prevenire problemi imprevisti.
*   **Scheduling:** Allocare le risorse umane sui task lungo l'asse temporale e stabilire **punti di controllo** (milestone). Timeline chiara, per **monitorare** l'andamento del progetto.
*   **Strategia di Controllo:** Configurare il **controllo di qualità** (un quadro di riferimento quantomeno) e la gestione sistematica dei cambiamenti.

---

## 4. Tecniche di Stima nei Progetti Software
La stima iniziale mira a ridurre l'incertezza e limitare i rischi finanziari e temporali. Si basa su tre classi di approcci:
1.  **Expert Judgment by Analisi (Stima Analogica):** Confronto sistematico con **progetti simili** precedentemente completati di cui si conoscono i dati reali.
2.  **Tecniche di Scomposizione (Approccio Bottom-Up):** Strategia "divide et impera".
	1. divisione in **task** o funzioni di cui dobbiamo stimare l'effort
	2. valuta effor usando LOC o FP.
3.  **Modelli Algoritmici Empirici:** Formule matematiche dedotte **empricamente** dai dati storici del tipo $d = f(v_i)$. *Questi modelli stabiliscono una relazione tra variabili come LOC e FP e le legano all'effort.*

---

## 5. Esempio Pratico di Stima Basata su LOC
Il calcolo di effort e costi partendo dalle Linee di Codice (LOC) stimate per ogni sottosistema si sviluppa attraverso una griglia analitica (Contenuto Informativo dell'Immagine):

*   Si stimano le LOC per ogni modulo funzionale (es. *UICF*, *2DGA*, *3DGA*, *DBM*, *CGDF*, *PCF*, *DAM*), arrivando a un totale stimato di **33.360 LOC**.
*   Si associa a ciascun modulo 
	* **indice di produttività storica** in LOC per mese/uomo (`LOC/pm`)
	* **costo unitario per** singola riga di codice (`$/LOC`).
*   **Calcolo Costo Totale:** Somma dei costi stimati per ogni singolo modulo $\rightarrow$ **$655.000**.
*   **Calcolo Effort Totale:** Somma degli effort parziali in mesi/uomo (MM) $\rightarrow$ **144.5 Mesi/Uomo**.

---

## 6. Il Modello Function Point (FP)
Proposto da Albrecht, **misura la quantità di funzionalità logica offerta all'utente basandosi unicamente sulle specifiche formali del sistema, PRIMA DELLA SCRITTURA DEL CODICE.**

### Fasi di Calcolo

#### Passo 1: Calcolo dell'UFC (Unadjusted Function Point Count)
Si identificano e contano 5 tipologie di elementi funzionali, **classificandone** la complessità (Bassa, Media, Alta) **tramite specifici pesi numerici**:
1.  **ILF (Internal Logical Files):** Archivi dati interni gestiti dal sistema (gruppi di dati, infromazioni di controllo, ..., di **proprieta del sistema software**)
2.  **EIF (External Interface Files):** Archivi dati esterni consultati ma non aggiornati.  (gruppi di dati, infromazioni di controllo, ..., di **di altre applicazioni**)
3.  **EI (External Inputs):** Dati o comandi immessi dall'esterno, dall'**utente per esempio** (es. form di inserimento).
4.  **EO (External Outputs):** Flussi di dati elaborati in uscita dal sistema (es. report, messaggi d'errore).
5.  **EQ (External Inquiries):** Interrogazioni interattive in tempo reale.
	1. Corrisponde a tutte le **combinazioni uniche di input/output, in cui un input genera un output immediato senza cambiare lo stato dei file logici interni**. 

*Esempio di conteggio (Contenuto Informativo dell'Immagine):* Assegnando pesi medi a ciascun elemento identificato (es. 1 ILF, 2 EIF, 2 EI, 3 EO, 2 EQ), si ottiene una somma pesata pari a **UFC = 55**.

#### Passo 2: Calcolo del TCF (Technical Complexity Factor)
Si valuta l'influenza di **14 fattori di complessità tecnica** ($F_j$, es. affidabilità dei backup, comunicazione dati, processamento distribuito, riusabilità del codice). Ad ogni fattore viene assegnato un punteggio da 0 (influenza nulla) a 5 (influenza essenziale).
1. Affidabile backup e ripristino
2. Comunicazione dati
3. Elaborazione dati distribuita
4. Prestazioni
5. Configurazione ad utilizzo intensivo
6. Inserimento dati online
7. Facilità operativa
8. Aggiornamento online
9. Interfaccia complessa
10. Elaborazione complessa
11. Riutilizzabilità
12. Facilità di installazione
13. Siti multipli
14. Agevolare il cambiamento

La formula per calcolare il fattore di correzione è:
$$TCF = 0.65 + 0.01 \times \sum_{j=1}^{14} F_j$$
*   Se tutti i fattori hanno valore 0 (complessità minima): $TCF = 0.65$.
*   Se tutti i fattori hanno valore 5 (complessità massima): $TCF = 1.35$.

#### Calcolo dei Function Point Finali
$$FP = UFC \times TCF$$

#### FP vs LOC
* **FP**: misurano la funzionalita e la complessita di un sistema software. Indipendenti dal linguaggio di programmazione.
* **LOC**: misurano la dimensione del software contando il numero di linee di codice. Dipende dal linguaggio di programmazione, non tiene necessariamente conto della complessita
* **Relazione tra FP e LOC**: non diretta o costante, dipende tra vari fattori.
* **Classificare i linguaggi**: alcuni linguaggi, a parita di FP richiedono un numero variabile di LOC per implementare una funzionalita. I linguaggi sono stati classificati
* **Jones' Backfiring**: situazione in cui l'uso esclusivo di LOC porta a risultati, previsioni errate in termini di sforzo di sviluppo.
---

## 7. Il Modello Algoritmico COCOMO (COnstructive COst MOdel)
Introdotto da Barry Boehm nel 1981, stima l'effort e la durata a partire dalle dimensioni del codice espresse in **KLOC** (migliaia di righe di codice).
### Modi di Sviluppo del Prodotto
*   **Organic:** **Progetti di dimensioni ridotte**, team coesi e requisiti flessibili.
*   **Semidetached:** **Progetti e team di dimensioni intermedie**, con mix di vincoli rigidi e flessibili.
*   **Embedded:** **Progetti complessi** caratterizzati da rigidi vincoli operativi e hardware (es. software di bordo aeronautici).

### I Tre Livelli del Modello
COCOMO ha 3 modelli distinti:
1.  **Basic:** Fornisce una stima rapida e approssimativa dell'effort globale. Utilizzato per stime iniziali del progetto.
2.  **Intermediate:** Applica formule correttive basate su 15 attributi di progetto (*cost drivers*). Si applica dopo aver suddiviso il sistema in sottostistemi
3.  **Advanced (o Detailed):** Applica i cost drivers a livello di singolo modulo o fase del ciclo di vita. Si applica dopo aver diviso i sottosistemi in moduli.

### Calcolo dell'Effort (Modello Intermediate, Modo Organic)
1.  **Calcolo dell'Effort Nominale:**
$$EffortNominale = 3.2 \times (KLOC)^{1.05} \text{ Mesi/Uomo (MM)}$$
    *Esempio:* Per un progetto da 33 KLOC $\rightarrow$ $3.2 \times (33)^{1.05} \approx 126 \text{ MM}$.
2.  **Applicazione dei Cost Drivers (Contenuto Informativo delle Immagini):**
    Si moltiplica l'effort nominale per un coefficiente correttivo $C$, ottenuto come produttoria di 15 fattori moltiplicativi derivanti dalle tabelle di classificazione dei **cost drivers**.
    $$Effort = EffortNominale \times C$$
    *Esempio:* Se la complessità del database è nominale (1.00) ma l'affidabilità richiesta è alta (1.15) $\rightarrow$ $C = 1.15 \rightarrow Effort = 126 \times 1.15 = 145 \text{ MM}$.

![[Pasted image 20260816225129.png]]

### Calcolo del Tempo alla Consegna (Time Schedule)
La durata temporale dello sviluppo $T$ (espressa in mesi) viene calcolata in base all'effort $E$ precedentemente stimato:
*   **Modo Organic:** $T = 2.5 \times E^{0.38}$
*   **Modo Semidetached:** $T = 2.5 \times E^{0.35}$
*   **Modo Embedded:** $T = 2.5 \times E^{0.32}$

### Stima dei Costi di Sviluppo
I costi vengono stimati ripartendo l'effort complessivo ($E$) sulle diverse fasi di sviluppo e attività di staff:
*   **Ripartizione Tipica dell'Effort per Fasi:**
    *   *Progettazione Preliminare (Preliminary Design):* **16%** dell'effort (suddiviso tra Project Manager e Analisti).
    *   *Progettazione Dettagliata, Codifica e Test (Detailed Design, Coding and Testing):* **62%** dell'effort (svolto da programmatori e analisti).
    *   *Integrazione (Integration):* **22%** dell'effort (assegnato ad analisti e programmatori).

---

## 8. Pianificazione Temporale e Controllo (Scheduling)
La pianificazione temporale organizza i compiti in una **"rete di task"** basandosi su sei principi fondamentali:
1.  **Ripartizione:** Scomposizione di processo e prodotto in task di dimensioni ragionevoli (WBS - Work Breakdown Structure).
2.  **Interdipendenza:** Identificazione delle relazioni di precedenza logica e temporale tra i task.
3.  **Allocazione di Risorse:** Assegnazione delle persone e dell'effort (date di inizio/fine).
4.  **Responsabilità Definite:** Assegnazione chiara della proprietà di ciascun task.
5.  **Risultati Previsti:** Definizione esplicita dell'output prodotto da ogni attività.
6.  **Punti di Controllo (Milestone):** Identificazione dei traguardi intermedi associati al **controllo di qualità**.

---

## 9. Strumenti di Scheduling

### A. Diagramma PERT (Program Evaluation and Review Technique)
![[Pasted image 20260816225648.png]]
*   **Rappresentazione (Contenuto Informativo dell'Immagine):** È un grafo orientato aciclico in cui ogni nodo rappresenta un task specifico ed ogni arco rappresenta un legame di precedenza (il task B non può iniziare finché il task A, collegato da una freccia, non è concluso).
*   **Funzioni Principali:**
    *   Determinazione del **Cammino Critico (Critical Path):** La sequenza di task che determina la **durata minima assoluta del progetto** (qualsiasi ritardo su un task del cammino critico ritarda l'intero progetto).
    *   Calcolo del **tempo di completamento** probabilistico tramite **modelli statistici/emprici**
    *   Calcolo delle date di inizio/fine al più presto (*Earliest*) e al più tardi (*Latest*).


### B. Carta di Gantt (Diagramma di Gantt)
![[Pasted image 20260816225839.png]]
*   **Rappresentazione (Contenuto Informativo dell'Immagine):** Diagramma a barre orizzontali in cui l'asse orizzontale rappresenta il tempo (espresso in settimane/mesi) e l'asse verticale elenca i task. **La lunghezza di ciascuna barra indica la durata prevista dell'attività**.
*   **Svantaggio:** **Non visualizza esplicitamente i legami di precedenza complessi**, per questo motivo viene quasi sempre integrata e accoppiata con un diagramma PERT.

---

## 10. Struttura del Piano di Gestione: SPMP (Software Project Management Plan)
Il documento SPMP è lo standard di riferimento per formalizzare la pianificazione. Esistono vari standard per compilare l'SPMP

**In generale l'SPMP deve parlare di**:
- **Estimates (Stime):** Questa sezione affronta le stime relative a diverse risorse del progetto, come tempo, costo e sforzo umano.
	- Stime di durata per ciascuna attività.
	- Stime di costo per risorse e attrezzature.
	- Stime di sforzo umano necessario.
- **Risks (Rischi):** Identifica e analizza i rischi potenziali che potrebbero influenzare il successo del progetto.
	- Elenco di rischi specifici e delle relative probabilità e impatti.
	- Strategie di mitigazione dei rischi.
	- Piani di risposta a situazioni di emergenza.
- **Schedule (Pianificazione):** Definisce la sequenza temporale delle attività del progetto, indicando quando ogni attività inizia e finisce.
	- Diagramma di Gantt o altro strumento di visualizzazione temporale.
	- Sequenza delle attività e delle dipendenze tra di esse.
	- Milestone (punti di controllo) critici.
- **Control strategy (Strategia di Controllo):** Indica come il progetto sarà monitorato e controllato durante la sua esecuzione.
	- Procedure di monitoraggio delle attività.
	- Strumenti e metriche di controllo.
	- Fasi di revisione e valutazione.

### A. ~~Contenuti secondo il NASA-SEL Manager's Handbook (1990)~~
Si articola in due macro-sezioni:
*   *Pagina 1/2:* **Sezione Introduzione Project Scope**: **Statement of Problem** (Requisiti chiave), **Technical Approach** (Strategie di riuso, vincoli, ambiente di sviluppo, build strategy) e **Management Approach** (Assunzioni, priorità, requisiti e allocazione delle risorse).
*   *Pagina 2/2:* **Milestones e Schedules** (Ciclo di vita, date di build/release), **Metrics** (Raccolta metriche per l'analisi storica della qualità), **Product Assurance** (Standard di Configuration Management e Quality Assurance) e **Plan Update History** (Tracciamento degli aggiornamenti apportati al piano).

### B. Contenuti secondo lo Standard IEEE 1058-1998 (Struttura in 3 Pagine)

> [!note] attenzione
> su andrea isw c'e' un mega listone di termini inutili.

1.  **Overview:** Sintesi del progetto, assunzioni, vincoli, deliverable rilasciati, schedulazione e budget sommario.
2.  **References & Definitions:** Riferimenti normativi e glossario.
3.  **Project Organization:** Interfacce esterne, struttura interna, ruoli e responsabilità.
4.  **Managerial Process Plans:**
    *   *Start-Up Plan:* Stime di effort/costi, piano di assunzione e formazione.
    *   *Work Plan:* Attività di lavoro e allocazione budget/risorse.
    *   *Control Plan:* Controllo dei requisiti, dei tempi, dei costi e della qualità.
    *   *Risk Management & Closeout Plan:* Piani di mitigazione rischi e chiusura formale del progetto.
5.  **Technical Process Plans:** Scelta del modello di processo, metodi, strumenti, infrastruttura tecnologica e criteri di accettazione del prodotto.
6.  **Supporting Process Plans:** Piani di Gestione della Configurazione (CM), Verifica & Convalida (V&V), Documentazione e Quality Assurance (QA).
7.  **Additional Plans & Annexes:** Sezioni aggiuntive opzionali.
