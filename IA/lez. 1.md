**IA forte**: ha come obiettivo riprodurre il pensiero umano ed i suoi processi cognitivi.
**IA debole**: vuole risolvere problemi specifici in modo intelligente.

**Cosa e' una IA**?
* puo' essere **umana** o **razionale**
* puo' **pensare** o **agire**.

**IA che agisce umanamente**: per essere tale deve passare il test di turing
1. un'uomo parla con una macchina ed un umano
2. l'uomo fa le domande e riceve  delle risposte
3. se l'uomo non riesce a decidere chi e' la macchina allora questa ha passato il test.

**cosa serve per passare il test di turing**?
* computer vision e robotica
* language processing, automated reasoning, machine learning.

**IA che pensa umanamente**:
* bisogna capire come l'uomo pensa
* capire il processo decisionale, di risoluzione dei problemi e di apprendimento

**IA che pensa razionalmente**:
* bisogna capire cosa e' un ragionamento logico
* si basa sulla rappresentazione di fatti in modo formale
* **fare la cosa giusta**: la cosa giusta da fare potrebbe non esistere.

## agenti
**agente**: entità che interagisce con l'ambiente usando **attuatori** e **sensori**
* **percezioni**: permettono di ricevere **input** dall'ambiente, attraverso i **sensori**
* **azioni**: l'azione dipende dalla **sequenza delle percezioni** e si manifesta con gli **attuatori**
* **funzione agente**: associa ad ogni sequenza di percezioni, un'azione
	* $f: P^* \to A$
* **programma agente**: implementa la funzione, esegue sull'architettura dell'agente.
* e' fatto da **architettura** + **programma agente**

**storia dell'agente**: e' la sequenza di percezioni
**conoscere le percezioni a priori**: cosa faccio se non mi aspetto che succeda qualcosa nell'ambiente?

**agente razionale**: fa la cosa giusta. 
* **tabella funzione agente**: e' corretta.
* **efficacia**: agisce in modo efficace
* **preferenze**: deve decidere cosa fare quando non esiste una scelta "migliore"
* **razionale e onniscenza**: razionalità non vuol dire onniscenza quando bisogna scegliere la cosa giusta.
* **obiettivo**: massimizzare la misura di prestazione

**misura di prestazione**: devo valutare la **sequenza di stati assunti** dall'agente.
* **oggettivita**: e' una misura oggettiva e paragonabile

**scegliere misura di prestazione**: teniamo conto di due cose
* **natura della misura esterna**: la misura guarda gli effetti delle azioni sull'ambiente
* **scopo della misura**: e' uno strumen

## PEAS
**PEAS**:
* **performance**: devo scegliere la misura di performance
* **environment**: devo definire cosa mi interessa dell'ambiente che mi circonda.
* actuators
* sensors

**Razonalita**: dipende da 4 fattori
* **misura di prestazione**: agiamo per massimizzare la misura scelta
* **conoscenza a priori dell'ambiente**: cosa so dell'ambiente? come si comporta in base a cosa faccio?
	* **imparare**: nel caso in cui l'agente non ha conoscenza a priori dell'ambiente.
	* **non autonomo**: se l'agente razionale dipende da conoscenza a priori, allora non e' autonoma.
* azioni che posso fare
* **sequenza delle percezioni**: le percezioni cambiano la visione che l'agente ha del mondo.

**onniscenza**: e' la configurazione per cui, per ogni azione, so cosa succede nell'ambiente.
* **quando si applica**? in contesti reali quasi mai, bisogna sempre dunque effettuare azioni per esplorare l'ambiente.

**agente autonomo**: non dipende da conoscenza a priori
* "*si comporta in misura dell'esperienza che ha*"

## ambiente
**osservabilita**:
* **completamente**: con le percezioni posso conoscere per intero lo stato dell'ambiente.
* **parzialmente**: alcuni aspetti posso non conoscerli e devono essere dedotti se possibile
* **non osservabile**: non ho sensori, lo stato e' totalmente incerto.


**multi-agente**: piu' agenti interagiscono con lo stesso ambiente.
* collaborazione/competizione
* comunicazione

**prevedibilita**:
* **deterministico**: lo stato successivo e' univocamente determinato dall'azione dell'agente selezionata.
* **stocastico**: ho una distribuzione di probabilità sugli stati.
* **non deterministico**: non c'e' una distribuzione di probabilità sugli stati.

**ciclo di iterazione**:
* **episodico**: *Non c'e' bisogno di pianificare*, l'esperienza agente e' divisa in episodi indipendenti tra loro. Le azioni di un'episodio non influenzano l'episodio successivo. 
* **non episodico**: bisogna pianificare, le azioni di un'episodio influenzano quello dopo.

**statico/dinamico**:
* **statico**: il mondo non cambia mentre decido
* **dinamico**: il mondo cambia
* **semi-dinamico**: l'agente cambia percezione del mondo mentre elabora, per esempio varia la misura di prestazione col passare del tempo.

**discreto/continuo**: riguardo alle variabili dell'ambiente...
* **discreto**: enumerabile
* **continuo**: non enumerabile

**noto/ignoto**: riferito all'agente
* **noto**: so cosa succede ad ogni azione, conosco le regole del mondo
* **ignoto**: devo imparare cosa fanno le mie azioni, esplorare e ragionare.
	* **azioni esplorative**: devo capire!!!

**environment generator**: devo generare ambiente che interagiscono con gli agenti per valutare le performance in piu casi.
* **l'ambiente non e' reale**: simulato via software, per testare il programma agente.
* **software ambiente**: deve emulare il ciclo PERCEZIONE-AZIONE-VALUTAZIONE

## agenti

**table driven agent**:
1. `percepts.append(percept)`
2. `return lookup(percept, Table)`
3. **autonomia**: non e' autonomo, dipende da conoscenza pregressa.
4. **estensibilità**: non e' facile da implementare ed estendere.

**skeleton-agent**:
1. **static**: `memory`
2. `mem = UpdateMem(mem, percept)`
3. `act = ChooseBestAct(mem)`
4. `mem = UpdateMem(mem, act)`
5. `return act`
6. **mem**: e' la memoria interna dello stato del mondo
7. e' la base degli agenti!

### agenti reattivi
**simple reflex agent**: seleziona azione in base alla **percezione corrente** tramite **regole condizione**.
1. `state = interpret-input(percept)`
2. `rule = rule-match(state, regole)`
3. `azione = regola.azione()`
4. **randomizzare**: il processo va randomizzato, evitiamo che si incastri il modello in un loop.

![[Pasted image 20260716142953.png]]
* **sensore**: mi dice com'e' il mondo
* **attuatori**.

**model based reflex agents**: introduciamo lo **stato interno**. E' utile per ambienti non completamente osservabili.
![[Pasted image 20260716143601.png]]
* "*com'e' ora il mondo?*": modella lo stato interno per rappresentare l'evoluzione del mondo. L'**agente si chiede come le proprie azioni modificano l'ambiente**.
	* "*what the world is like now*"
* **regole**: mi dicono come agire in base allo stato interno
1. `stato = AggiornaStato(percept, modello)`
2. `regole = RuleMatch(stato)`
3. `action = regola.action()`



## agenti con obiettivo
**goal based agent**: introduciamo oltre a stati e percezioni, un goal da raggiungere.
* **pianificare**: l'agente deve necessariamente pianificare per raggiungere un goal generico.
* **stato interno**: hanno uno stato interno come prima.
* **interrogazione del modello**: un'agente model based e' interessato a capire, *"cosa succederebbe se eseguissi $A$"*?
* **previsione**: controllo il risultato previsto con il goal, scegliendo l'azione che mi avvicina di piu all'obiettivo.
* *Guidati da un obiettivo, Pianificano, richiedono necessariamente piu calcoli.*

## agenti con valutazione di utilita
**valutazione di utilita**: oltre a massimizzare il goal, mi chiedo quanto e' buona/vantaggioso ciascun stato del mondo.
* **utility function**: misura quanto e' utile uno stato per perseguire l'obiettivo

**obiettivi alternativi**: un'agente puo' avere piu' obiettivi possibili, devo capire verso quale obiettivo muovermi.
* **funzione di utilita**: qual'e' il migliore stato finale?

**funzione di utilita**: assegna ad ogni stato un valore numerico, "quanto l'agente e' soddisfatto" in quello stato, indipendentemente dal goal scelto da perseguire.
* **a che serve**? a confrontare obiettivi diversi.

**obiettivi con probabilita diverse**: l'agente deve penalizzare ottimi obiettivi ma quasi impossibili da perseguire, o molto costosi.

## learning agent
**learning agent**:
![[Pasted image 20260716145925.png]]
* **ambienti sconosciuti**: deve scoprirli e migliorare nel tempo la sua prestazione.
* **esperienza**: devo fare esperienza del mondo per capire come e' fatto.
* **CRITIC**: fornisce **feedback** al modulo di apprendimento, analizza i risultati e interpreta il comportamento dell'agente.
* **LEARNING ELEMENT**: produce modifiche al programma agente in base al feedback ricevuto dal CRITIC, ossia modifica il PERFORMANCE ELEMENT
* **PERFORMANCE ELEMENT**: e' l'agente vero e proprio che opera. in base al mondo esterno, calcola la performance corrente e se necessario modifica il learning element in caso di previsioni errate.
* **PROBLEM GENERATOR**: crea e suggerisce problemi o scenari ipotetici per migliorare l'apprendimento, genera dati ed esperienze.misura


esempio taxi:
* **PERFORMANCE ELEMENT**: guida il taxi
* **CRITIC**: misura quanto si lamenta il cliente
* **LEARNING ELEMENT**: modifica le regole per frenata e velocita nel PE in base al feedback
* **PROBLEM GENERATOR**: suggerisci una strada secondaria da provare

## tipi di rapresentazione
**atomica**:
* ogni stato e' un **blocco unico e indivisibile**, a cui non posso accedere alla sua **struttura interna**
* ho dunque delle transizioni tra stati

**fattorizzato**: ogni stato e' un'insieme di variabili
* **vettore**: posso vedere uno stato come un vettore di variabili

**strutturata**: ricco e complesso
*  oggetti sono entita con relazioni tra loro
* **descrivo**: relazioni, gerarchie, dipendenze.

