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