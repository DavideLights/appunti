**IR**: trovare materiale di natura **non strutturata** che soddisfa un **bisogno informativo**.

**Dove si usa IR?** Web Search, ricerca file nei sistemi operativi, classificazione email, ecc...

**Assunzioni**:
* **Staticità**: la collezione non cresce, ne diminuisce nel tempo.
* **Cosa cerchiamo**? Documenti rilevanti rispetto ad un certo bisogno informativo dell'utente.
* **Collezione**: insieme di documenti statico, ossia non cresce e non decresce mai.

**Query**: e' la richiesta utente
* **Information Need**: bisogno informativo dell'utente
* **Query e Information Need non coincidono sempre**: l'utente comunica al sistema il suo bisogno informativo attraverso la query, ma l'utente potrebbe essere un coglione.

**Dati non strutturati**: oggi ci sono molti piu dati non strutturati, rispetto a quelli strutturati. L'information retrieval ci da strumenti per manipolare questi ultimi.

**Misurare la performance di un sistema IR**: devo misurare la performance dell'intera pipeline, end-to-end e non le varie fasi.

**Performance e recall di un sistema IR**: data una query posso ritornare 10,20,100,... documenti. Ma quanti di questi sono giusti?

**Precision**: ossia la **qualita**, *frazione di documenti trovati* che rispettano la richiesta informativa. 
* **Risponde alla domanda**: *"Tra tutto quello che mi hai dato, quanto è effettivamente utile?"*
* **Massimizzare la precision**: vuol dire aumentare la qualità dei risultati rendendo il sistema selettivo.

**Recall**: frazione di documenti rilevanti nella collezione, che sono stati trovati.
* **Risponde alla domanda**: *"Tra tutto quello che esiste di utile nel database, quanto sei riuscito a trovarne?"*
* **Massimizzare la recall**: *vuol dire aumentare i falsi positivi*.

**Esempi**:
- **Alta Precision, Bassa Recall:** Il sistema è molto "timido". Restituisce solo 2 documenti, ma sono perfetti. Hai però saltato altri 100 documenti utili (es. un motore di ricerca legale che deve essere ultra-preciso).
- **Alta Recall, Bassa Precision:** Il sistema è "generoso". Ti restituisce 10.000 documenti; tra questi ci sono tutti quelli rilevanti, ma devi spulciare migliaia di risultati inutili (es. una ricerca esplorativa per una tesi di laurea).
![[Pasted image 20260306122808.png]]
**Esempio**: trovare documenti che contengono il termine $A$, $B$ e $\lnot C$.
* costruisco la matrice per righe i termini e per colonne i documenti
* e posso "facilmente" trovare i documenti che rispettano la richiesta.

**Domanda Esame**: differenza tra notazione sparsa e densa.
* **notazione densa**: **memorizzi ogni singolo valore** dell'insieme (vettore o matrice), inclusi gli zeri.
* **notazione sparsa**: in una notazione sparsa, memorizzi **solo i valori diversi da zero**, annotando la loro posizione (indice).
* **rappresentare un fenomeno in memoria**: se un dato e' per sua natura denso, allora useremo la notazione densa..
## Invertex Index
**Term-Document incidence matrices**: matrici dover per riga ho i termini, e per colonna i documenti
* **incidence vector**: ogni riga e' un vettore di incidenza
![[Pasted image 20260627155426.png]]

**(D) Quando e' sconveniente la matrice di incidenza?**
* **ipotesi**: 1 milione di documenti, 1000 parole per documento, 500 mila termini distinti tra tutte le parole nei documenti
* **come e' fatta la matrice**? ci sono almeno $500K \times 1M$ bit dove molti bit sono a 0 e pochissimi sono ad 1. L'informazione rilevante e' per quali documenti ho 1, ma ho memorizzato tanti 0 (notazione densa).
* **soluzione**: devo trovare un modo per imagazzinare solo gli 1di questa matrice per rispariarme potenzialmente un botto di spazio.
* **spazio della matrice**: $6GB$ se ho $1M$ di documenti da $1000$ parole l'uno con 

**Indice**: ad ogni query invece di scansionare i testi vado a leggere un indice creato nella fase di indicizzazione.

**Indice Inverso**: voglio vedere per ogni parola quale documento lo contiene, *ossia: per ogni termine $t$ voglio una lista di documenti che lo contiene*.
* **(D) lunghezza fissa**: puo' essere di lunghezza fissa? 
	* **No**, dovrei riallocare la memoria se devo aggiungere il documento 14 a Brutus (ref. immagine)
	* **No**, in caso di documenti con pochi termini allora spreco molto spazio.
	* **Dunque**: un Inverted Index deve essere a lunghezza variabile.
* `docID`: **numero seriale** corrispondente al documento.
![[Pasted image 20260627160614.png]]
![[Pasted image 20260420180804.png]]

**memorizzazione**:
* **su disco**: lo salvo come un unico blocco di dati
* **in memoria**: lo salvo come linked list o array a lunghezza variabile.

**Posting Lists Per Inverted Index**: 
* **struttura dati**: Linked List
* E' fatta di **posting** 
* **ordinata** per `docID`.

**document frequency**: e' utile registrare la frequenza con cui il termine compare in tutti i documenti processati.

**term frequency**: e' utile registrare la frequenza con cui un termine compare in un documento

**dizionario**: e' fatto di termini. per ogni termine ho una linked list, chiamata posting che registra in quali documenti il termine compare.
* **postings**: insieme delle postings list
* **postings list**: la singola entry della postings.

**Merge di una linked List**: avanzo su due Posting Lists in ordine, in modo da cercare i documenti che compaiono in entrambi

Costruire inverted index: 3 passaggi principali
* **Tokenizer**: trasforma il testo in token
* **Moduli linguistici**: trasforma i token applicando varie assunzioni
	* **Normalizzazione**: voglio che parole differenti abbiano lo stesso significato. Es `U.S.A` e `USA`.
	* **Stemming**: voglio tenere solo la radice della parola. Es: `authorize` ed `authorization`
	* **Lemmatizzazione**: `studentessa` diventa `studente`
	* **Stop words**: elimina parole troppo comuni come `the`, `a`, `to`, `of`
* **Indexer**: metti i token nelle posting lists

**Attenzione nella costruzione dell'inverted index**, i 3 passaggi sopra potrebbero introdurre effetti indesiderati:
* `Rossi` inteso come cognome potrebbe diventare `rosso` inteso come colore.
* Devo capire bene il ruolo di una parola del testo e decidere come modificarla per gli step successivi.
* **polisemia**: le parole hanno tanti significati.
* se rimuovo le stop words allora la band `The Who` scompare dal mio dizionario.
![[Pasted image 20260306124936.png]]



$\text{docID}$: in una collezione di documenti, assumiamo che ogni documento abbia un identificatore unico.

**indexer**: 
1. **input per indexing**: e' un insieme di coppie $(\text{term,docID})$
2. **sorting delle coppie**: data in input le coppie $(\text{term,docID})$ voglio ordinarle alfabeticamente, e poi per $\text{docID}$. Ottengo una Lista ordinata
3. **merge**: mentre costruisco la posting, faccio merge delle coppie $(\text{term, docID})$ che compaiono piu volte. OSS: i duplicati sono adiacenti
4. **document frequency**: per ogni termine salvo la frequenza con cui compare. Serve per ottimizzare le query booleane.
5. **ottengo per ogni termine la tripla**: $(\text{term}, \text{doc.freq.}, \text{*postings list})$ dove $^*\text{posting\_list}$ e' il puntatore alla struttura dati contenente i  postings.


![[Pasted image 20260318094400.png]]


**Merge algorithm** $\text{Intersect}(p_{1},p_{2})$:
1. $\text{answer} \gets \emptyset$
2. **while** $p_{1} \neq \text{NIL}$ and $p_{2} \neq \text{NIL}$:
3. **do if** $\text{docID}(p_{1}) = \text{docID}(p_{2})$
	1. **then**: $\text{Add}(\text{answer}, \text{docID}(p_{1}))$
	2. **else if** $\text{docID}(p_{1}) < \text{docID(p2)}$
		1. **then** $p_{1} \gets \text{next}(p_{1})$
		2. **else** $p_{2} \gets \text{next}(p_{2})$

**oss**: e' un semplice algoritmo di merge, nulla di complicato.