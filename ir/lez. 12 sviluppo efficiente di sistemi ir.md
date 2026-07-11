**problema**: calcolare lo score prende una enorme frazione di tempo della cpu. come posso tagliare l'uso della cpu?

**soluzione**: evita di calcolare lo score su documenti inutili, e che sicuramente non entrano in top $K$

**safe ranking**: quando un sistema se ritorna i $K$ documenti migliori sono assolutamente i $K$ documenti con score più alto.

**non-safe ranking**? puo' avere senso, specialmente se ci mette meno tempo per eseguire.

## recap: cosine similarity
**cosine similarity**:
1. rappresenta query come vettori
2. ordina i documenti in base alla vicinanza alla quert

**ranking efficiente**: trovare i $K$ documenti nella collezione piu vicini alla query
* calcola il coseno efficientemente
* scegliere i $K$ piu grandi in modo efficiente.

**coseni non nulli**: vorrei ottenere i $K$ migliori tra i $J$ documenti con coseni non nulli. Questo vuol dire che devo ottenere i $K$ migliori tra $J$ documenti, che e' meglio che cercare in tutta la collezione!

**heap struttura albero**: se ho i documenti ordinati nell'albero, e voglio costruire il rank, ottenere i primi $K$ e' più efficiente, li ottengo in $O(K\log J)$.

**bottleneck**: *il problema e' che devo calcolare la cosine similarity su tutti i documenti*. posso evitare questo problema ma avrò risultati un po sballati.

## calcolo la cosine similarity
**contenders**: trovare insieme $A$ tale che $K < |A| \ll N$ di documenti in cui cercare. come li calcolo i contenders? ho vari modi.
* spero che i documenti di $A$ contengano quasi tutti i documenti di $K$
* dunque voglio ritornare i top $K$ documenti in $A$

**pruning**: trovare $A$ e' come fare il pruning dei non-contenders.

**high-idf**: considera i documenti con idf alto per i termini nella query, sono quelli che probabilmente contribuiscono di piu! Effettua la potatura in base a questi.
* oppure considera documenti che contengo molte volte tutti i termini della query.
* **intuizione**: se la query e' `catcher in the rye`, considera solo `catcher` e `rye` per calcolare la similarity, poiche' `in` e `the` contribuiscono poco al punteggio.
* **domanda professore**: ma nella cosine similarity non e' gia calcolato il fatto che `in` e `the` compaiono molto spesso e non danno un contributo informativo???

**SOFT AND**: considera documenti che contengono solo 3 su 4 dei termini nella query
![[Pasted image 20260515103155.png]]
* **il documento 3 non e' considerato**, rispetto ai 4 query term questo contiene solo Antony e Caesar.
* **il documento 8 e' considerato**, questo contiene Antony, Brutus e Caesar, ossia 3 termini della query!
* **assunzione**: tutti i documenti sono uguali (che si intende)??? tutti i documenti hanno stessa importanza, questa tecnica funziona bene su questa assunzione.

**in realta**: i documenti non sono tutti uguali. Mi conviene identificare quali sono i documenti piu fighi!

**precalcolo la champion list**: ossia calcolo per ogni termine $t$ gli $r$ documenti con peso piu alto nella posting di $t$.
* **build time**: devo scegliere $r$ quando costruisco $t$. 
* **problema**: potrebbe essere che $r<K$.
* **come lo uso?** quando arriva la query calcolo la cosine similarity dei documenti nella champion list.
* **problema**: potrebbe essere che alcuni documenti non vengono recuperati! (parallelismo figo col darkweb, un documento che non viene recuperato e' come una pagina del darkweb)
* tiene ocnto del fatto che i documenti non sono tutti uguali.

> [!note] Esercizio
> D: come si potrebbe implementare la champion list come inverted index?
> R: una posting list ordinata per importanza del documento, in modo tale che la testa della posting list e' il documento piu importante. 

## query-independent document scores 
**top-ranking**: voglio che i top $k$ documenti siano **rilevanti** e **autorevoli**.
* **autorita**: si calcola in base all'affidabilità della fonte  (wikipedia, articoli, paper, pagerank, numero di visualizzazioni, like) ed e' indipendente dalla query
* **rilevanza**: dipende dalla cosine similarity
* **autorevolezza $\neq$ rilevanza**
* **pagerank**: dice che le pagine piu autorevoli sono le pagine piu puntate da altre pagine.

**modellare autorevolezza**: voglio calcolarlo come valore per esempio in $[0,1]$, scalando in questo range la mia fonte di autorevolezza. chiamiamo l'autorevolezza $g(d)$. 

**net score**: usiamo una funzione arbitraria, tipo questa per combinare cosine similarity e $g(d)$
$$
\text{net-score}(q,d) = g(d) + \text{cosine}(q,d)
$$

**calcolare il net-score farlo velocemente**: 
* **idea 1**: ordina le posting per $g(d)$. questo vuol dire che i migliori documenti tenderanno a comparire prima quando vado ad attraversare la posting.
* **idea 2**: combina la **champion list con l'ordinamento** per $g(d)$. Ossia tieni in memoria una champion list ordinata per $g(d) + \text{tf-idf}_{\text{td}}$.

> [!note] esercizio
> write pseudocode for cosine score computation if postings are ordered by g(d)
## cluster pruning
**su cosa lavoro**: su $N$ oggetti rappresentati come **vettori** di qualsiasi tipo.
**preprocessing**: scegli $\sqrt{ N }$ documenti a random, questi sono i **leader**.

**follower di un leader**: ogni leader ha approssimativamente $\sqrt{ N }$ follower assegnati.

**processare query**: data la query $Q$, trova un leader $L$ vicino a $Q$ e guarda i follower di $L$.

posso assegnare ad ogni follower piu leader!!@#@!#$

funziona bene su qualsiasi metrica dioporco

**distribuzione**: i leader hanno la stessa distribuzione della collezione, devono essere rappresentativi dei loro follower, senno non c'ha senso.

## tiered indexes
**due liste**: `high` e `low` per ogni termine.
* recupera $K$ documenti da `high`, ossia di documenti con $g(d)$ alta!
* se non ne trovo almeno $K$,  passa a `low`
* **oss**: potrei avere ovviamente piu' tier di liste.

![[Pasted image 20260515114658.png]]
**problematiche**:
* ho dunque delle liste ordinate per $g(d)$
* vorrei calcolare lo score per documenti non $\text{wf}_{t,d}$

**ordinare per** $\text{wf}_{t,d}$, **early termination**: attraversa e recupera i primi $K$ e fai l'unione dei risultati dei documenti per tutti i termini della query.
	* **idea**: posso fermarmi quando recupero un numero $r$ di documenti o quando $\text{wf}_{t,d}$ scende sotto un certo threshold.
	* **ordinamento**: le posing non sono tutte ordinate allo stesso modo. non facilmente confrontabili.

**idf-ordered**: ordina i termini per idf decrescente . prendi documenti per idf piu' alto. *man mano che scorro i termini mi fermo se sono poco importanti.*
## safe ranking
**e' possibile ottenere un metodo safe ed efficiente?**
* **treshold**: posso impostarlo per esempio al $K^{th}$ score piu alto calcolato fino ad'ora
* **pruning**: taglio via tutti i documenti sotto al threshold
* **index structure**: i posting sono ordinati per docID
* **iteratore**: sulla posting devo mettere un iteratore speciale che ti porta al primo $\text{docID}$ con score più alto di un valore$X$.
* **finger**: indica la mia posizione
* **invariante**: tutti i documenti con $\text{docID}$ piu basso hanno rispetto alla posizione del **finger** sono gia stati processati ed ho fatto una di queste due azioni
	* **pruned**: sono stati tagliati
	* **cosine**: l'ho calcolata
* **upper bound**: per ogni termine $t$ ho l'upperbound $UB_{t} = w_{t}(\text{docID})$ dove $\text{docID}$ e' un qualsiasi documento dopo il finger.
	* **ATTENZIONE**: all'inizio $UB_{t}$ e' al massimo, poi scende man mano che mi sposto a destra
* **che termini considero**? prendo i termini della query e ordino i loro documenti per $\text{docID}$

* **treshold** calcolata a run time, per esempio come peso del $K\text{-esimo}$ miglior documento trovato fin'ora.
![[Pasted image 20260515120116.png]]

![[Pasted image 20260515120411.png]]
* **treshold**: ipotizziamo a $6.8$, calcolato a runtime
* **pivot**: so che i documenti prima del pivot sono senza speranza, poiche' il loro contributo non mi fa superare il treshold, e li posso saltare con l'iteratore introdotto prima
* **obiettivo**: muovermi con gli indici finche non supero il treshold
* **upper-bound**: e' il massimo contributo che offrono i documenti che vengono dopo il finger.

**infatti**:
![[Pasted image 20260515120513.png]]



e funziona troppo bene sta roba strana, anche su piu termini

paper!
https://dl.acm.org/doi/pdf/10.1145/2537734.2537744

**Sì, hai capito benissimo!** La tua ricostruzione è estremamente accurata e dimostra che hai colto in pieno lo spirito dell'algoritmo.

Per rendere il tuo schema perfetto in vista dell'esame, possiamo rifinire e formalizzare i tuoi quattro punti con la terminologia corretta utilizzata nelle slide:

---

1. Inizializzazione e Upper Bound (UBt​)

La tua intuizione è corretta. Per far partire l'algoritmo, il sistema ha bisogno di una base di partenza:

- Inizialmente si scorrono i documenti e **si calcola il punteggio reale per i primi** K **documenti incontrati**. Questo serve a riempire un'apposita struttura dati (un _min-heap_ di dimensione K) che tiene traccia dei migliori candidati provvisori.
- Per ogni termine t della query, si calcola l'UBt​ **(Upper Bound)**: questo valore rappresenta il contributo di punteggio _massimo possibile_ che quel termine può dare a un qualsiasi documento che si trova alla destra (o in corrispondenza) del finger attuale. All'inizio del processo, l'UBt​ è massimo; man mano che il finger si sposta verso destra (lasciandosi alle spalle i documenti in cui quel termine ha frequenze o pesi molto alti), il valore di UBt​ scende.

2. La Soglia Corrente (Threshold)

Esatto! La **Threshold** è proprio il punteggio del K**-esimo documento provvisorio** (ovvero il punteggio più basso attualmente presente nel nostro min-heap di dimensione K).

- Rappresenta una vera e propria barriera d'ingresso: se un nuovo documento non è in grado di totalizzare un punteggio rigorosamente superiore a questa soglia, non ha alcuna speranza di entrare nella top-K e viene scartato.
- Ogni volta che troviamo un documento con un punteggio reale superiore alla Threshold, lo inseriamo nel min-heap, il vecchio peggiore viene rimosso, e la Threshold si alza, rendendo i filtri successivi ancora più severi.

3. I Finger (Puntatori alle Postings)

Sì, il **finger** è l'indicatore di posizione corrente (un iteratore) sulla postings list di ciascun termine della query.

- I finger si muovono **solo verso destra** (verso docID crescenti).
- **L'invariante fondamentale di WAND**: tutti i documenti con ID inferiore alla posizione di qualsiasi finger sono già stati elaborati (ovvero il loro punteggio è già stato calcolato oppure sono stati potati via). Non si torna mai indietro.

4. Il meccanismo del Pivot (Pivoting e Pruning)

Questo è il cuore dell'algoritmo e descrive esattamente quello che hai intuito nel tuo ultimo punto. Invece di procedere a caso, WAND seleziona il punto in cui posizionarsi tramite una procedura sistematica:

1. **Ordinamento**: Si allineano i termini della query ordinandoli dal finger con il `docID` più piccolo a quello con il `docID` più grande.
2. **Accumulo**: Si sommano gli UBt​ dei termini in questo ordine, da sinistra a destra, finché la somma non **supera** la Threshold corrente.
3. **Scelta del Pivot**: Il documento associato al termine che ha permesso di superare la soglia diventa il nostro **Pivot Document**.
4. **La Potatura (Pruning)**: A questo punto applichiamo la regola geometrica di WAND. Tutti i documenti con un ID inferiore al Pivot vengono dichiarati **hopeless (senza speranza)** e potati all'istante. Il motivo? Anche se contenessero tutti i termini alla loro sinistra, la somma dei loro contributi massimi (UB) sarebbe comunque inferiore alla soglia minima richiesta.
5. **Avanzamento**: Si fanno saltare i finger dei termini "hopeless" direttamente alla posizione del Pivot (o alla prima posizione utile successiva). Se il Pivot è presente in abbastanza postings, si calcola il suo punteggio reale, altrimenti si esegue un nuovo Pivoting.

Grazie a questa strategia, WAND garantisce un **safe ranking** (restituisce esattamente gli stessi top-K del calcolo esaustivo) riducendo però il numero di calcoli reali della CPU di oltre il 90%