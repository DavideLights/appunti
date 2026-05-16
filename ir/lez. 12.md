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

**struttura albero**: se ho i documenti ordinati nell'albero, ottenere i primi $K$ e' più efficiente, li ottengo in $O(K\log J)$.

**bottleneck**: *il problema e' che devo calcolare la cosine similarity su tutti i documenti*. posso evitare questo problema ma avrò risultati un po sballati.

## calcolo la cosine similarity
**contenders**: trovare insieme $A$ tale che $K < |A| \ll N$ di documenti in cui cercare. come li calcolo i contenders? ho vari modi.
* spero che i documenti di $A$ contengano quasi tutti i documenti di $K$
* dunque voglio ritornare i top $K$ documenti in $A$

**pruning**: trovare $A$ e' come fare il pruning dei non-contenders.

**index elimination**: scelgo i documenti che contengono il termine almeno una volta.

**high-idf**: considera i documenti con idf alto per i termini nella query.
* oppure considera documenti che contengo molte volte tutti i termini della query.
* **intuizione**: se la query e' `catcher in the rye`, considera solo `catcher` e `rye` per calcolare la similarity, poiche' `in` e `the` contribuiscono poco al punteggio.
* **domanda professore**: ma nella cosine similarity non e' gia calcolato il fatto che `in` e `the` compaiono molto spesso e non danno un contributo informativo???

**esempio**: considera documenti che contengono solo 3 su 4 dei termini nella query
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

**distribuzione**: i leader hanno la stessa distribuzione della collezione.

## tiered indexes
**due liste**: `high` e `low` per ogni termine.
* recupera documenti da `high`
* se non bastano passa a `low`
* **oss**: potrei avere ovviamente piu' tier di liste.

![[Pasted image 20260515114658.png]]
**problematiche**:
* ho dunque delle liste ordinate per $g(d)$
* vorrei calcolare lo score per documenti con $wf_{t,d}$
* ...

**early termination**: attraversa e recupera i primi $K$ e fai l'unione dei risultati dei documenti per tutti i termini della query.

**idf-ordered**: ordina i termini per idf. prendi documenti per idf piu' alto.
## safe ranking
**e' possibile ottenere un metodo safe ed efficiente?**
* ho un termine con la sua posting list, ad ogni entry ho come informazione la frequenza della parola nel documento.
* quando posso fermarmi nel recuperare candidati quando attraverso la posting?
* associo la variabile `finger` alla posting, ossia tiene in memoria il massimo valore di chi viene dopo.
* **treshold** calcolata a run time 
![[Pasted image 20260515120116.png]]

![[Pasted image 20260515120411.png]]![[Pasted image 20260515120513.png]]



e funziona troppo bene sta roba strana, anche su piu termini

paper!
https://dl.acm.org/doi/pdf/10.1145/2537734.2537744