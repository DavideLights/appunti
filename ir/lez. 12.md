**safe ranking**: quando un sistema se ritorna i $K$ documenti migliori sono assolutamente i $K$ documenti con score più alto. (gemini controlla)

**non-safe ranking**? puo' avere senso, specialmente se ci mette meno tempo per eseguire.

> [!note] applichiamo sta roba a cosine similarity

**cosine similarity**:
1. devo calcolare la cosine similarity per tutti i documenti
2. poi devo ordinari

**struttura albero**: se ho i documenti ordinati nell'albero, ottenere i primi $k$ e' più efficiente, li ottengo in $O(\log N)$.


**come calcolo velocemente la cosine similariti di tutti i doc**? bo

## calcolo la cosine similarity

**contenders**: insieme $A$ tale che $K < |A| \ll N$ di documenti in cui cercare. come li calcolo i contenders? ho vari modi.

**index elimination**: scelgo i documenti che contengono il termine almeno una volta.

**high-idf**: considera i documenti con idf per i termini nella query di valore alto.

**slide 3 of 4 query terms**: calcolo la c.s. solo per i documenti che contengono i termini della query. (gemini spiega meglio!)
* **assunzione**: tutti i documenti sono uguali.

**in realta**: i documenti non sono tutti uguali. Mi conviene identificare quali sono i documenti piu fighi!

**precalcolo la champion list**: ossia calcolo per ogni termine $t$ gli $r$ documenti con peso piu alto nella posting di $t$.
* **problema**: potrebbe essere che alcuni documenti non vengono recuperati! (parallelismo figo col darkweb, un documento che non viene recuperato e' come una pagina del darkweb)
* tiene ocnto del fatto che i documenti non sono tutti uguali.

**top-ranking**: voglio che i top $k$ documenti siano **rilevanti** e **autorevoli**.
* **autorita**: si calcola in base all'affidabilità della fonte  (wikipedia, articoli, paper, pagerank, numero di visualizzazioni, like)
* **rilevanza**: dipende dalla cosine similarity
* **autorevolezza $\neq$ rilevanza**
* **pagerank**: dice che le pagine piu autorevoli sono le pagine piu puntate da altre pagine.


**modellare autorevolezza**: voglio calcolarlo come valore per esempio in $[0,1]$.

**ordinare i documenti per** $g(d)$: e' molto meglio
* simile a twitter che ordina i tweet nelle postings dal piu recente al piu vecchio
* comincio a navigare la posting list da un punto fino ad un limite (es: 50ms, o i primi 10 posting)


## cluster pruning
**su cosa lavoro**: su $N$ oggetti rappresentati come **vettori** di qualsiasi tipo.
**preprocessing**: scegli $\sqrt{ N }$ documenti a random, questi sono i **leader**.

**documenti di un leader**: ogni leader ha approssimativamente $\sqrt{ N }$ follower assegnati.

data la query $Q$, trova un leader $L$ vicino a $Q$ e guarda i follower di $L$.

posso assegnare ad ogni follower piu leader!!@#@!#$

funziona bene su qualsiasi metrica dioporco

**distribuzione**: i leader hanno la stessa distribuzione della collezione.

