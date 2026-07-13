**Costruzione index**: ordino i termini in $O(n\log n)$
* ***Problema**: troppa memoria e tempo. I dati sono tanti.
* **indexer**: e' la macchina o il processo che costruisce l'indice.

**RCV1**: collezione usata fine anni 90, vecchia e piccola. Collezione di notizie di reuters.
* **formattazione RCV1**: titolo, data e body.
* $N = \text{numero documenti} = 800.000$
* $L = \text{numero medio di token} = 200$
* $M = \text{termini (= tipi di parole)} = 400.000$. Numero di parole differenti tra gli $N$ documenti.

```
cat file.txt | tr " " "\n" | sort | uniq | wc
```

**sort-based index construction**: 
* **problema**: devo caricare tutti i documenti in memoria per farne il `sort`
* Ogni coppia $(\text{termID}, \text{docID})$ costa 8 byte di memoria
* Se la  collezione e' grande occupo facilmente tutta la ram.
* **soluzione**: tengo in memoria soluzioni intermedie sul disco e ordino altre porzioni di dati.

**average bytes per term**:
* **token**: sono le parole che vedo nel testo
* **term**: sono le parole nel dizionario. Queste vengono trasformate!

**(D) byte per token e per termini in RCV1**:
 * **avg. # bytes per token 4.5**
 * **avg. # bytes per term 7.5**
 * *abbiamo questa differenza per token si intendono anche tutte le occorrenze di parole come `the`, `in`, `of`, ecc... che abbassano di molto la media.* 

**non-positional postings**: **100.000.000** contro i **160.000.000** di token stimati nei testi. 
* **perche?** molte parole  sono ripetute o stopword rimosse.

**problema grande**: il sort-based index construction  non scala ed non e' fault tollerant. Cerchiamo una soluzione migliore...
* **block size**: ogni disco scrive a blocchi da 8 fino a 256 KB.
* **trasferimento**: e' piu' efficiente trasferire grandi quantita di dati dal disco.
* **che famo???**
## BSBI (Block sort-based indexing)
**assunzioni**:
* $(\text{termID}, \text{docID})$ usa 8 byte e sono generate man mano che faccio il parsing.
* **ATTENZIONE**: la coppia contiene un `termID`, e non il `term`. Questo ci serve per l'ordinamento dei termini.
* ho 100M di coppie da 8 byte di cui fare il sort.

**obiettivo**: sorting con pochi accessi sul disco

**Voglio fare il sort di `100MB` di dati**:
* **blocco**: stabilisco che posso fare il sort in memoria di`10MB` per volta, per esempio. Ogni blocco potrebbe contenere uno o piu documenti
* **per ogni blocco**:  faccio sorting $O(n \log n)$ e creo l'inverted index list. Ricorda che $n=10M \text{ di postings}$
* **merge**: *una volta che li ho sul disco mi basta fare il merge* di questi, tanto sono tutti ordinati.

`BSBIndexConstruction`:
1. $n \gets 0$
2. **while** non ho finito di processare tutti i documenti
3. **do** $n \gets n+1$
	1. **ottieni il blocco**: $\text{block} \gets \text{ParseNextBlock()}$
	2. **crea l'indice per quel blocco**: $\text{BSBI-Invert}(\text{block})$
	3. **scrivi su disco**: $\text{WriteBlockToDisk}(\text{block}, f_{n})$**avg. # bytes per token 4.5**
4. $\text{MergeBlocks}(f_{1},\dots,f_{n}; f_{\text{merged}})$


**AVL**: se i blocchi sono alberi bilanciati, allora il merge di blocchi costa $O(\log N)$.
* **merge delle posting list**: per ogni termine in ogni blocco, il merge viene fatto concatenando le posting list
* **assunzione**: assegno i documenti da parsare in ogni blocco in modo incrementale.

**merge dei blocchi**
![[Pasted image 20260629170643.png]]
* **la procedura e' la seguente**: leggo, concateno e riscrivo su disco
* **merge binari**: faccio il merge di "blocchi adiacenti" per "termId", e faccio la concatenazione delle posting list

**documenti per blocco**:
* **b1**: per ogni termine ha un range da 1-10 doc per esempio
* **b2**: per ogni termine ha un range da 11-20..
* ecc...
* **dunque**: mi basta fare la **concatenazione** delle posting lists.

**Multi-way merge**: 
* **apri i file simultaneamente**: mantieni dei buffer in lettura e scrittura per ogni blocco.
* **apri il file di output**: un buffer per scrivere.
* **ad ogni iterazione**: *estrai dalla coda con priorita il blocco con $\text{termID}$ piu basso e fai il merge della posting lists per quel $\text{termID}$ con il file di output, e modifica la chiave per quel blocco.*
* **coda priorita**: *serve per ottenere ad ogni iterazione il blocco con il term id piu basso.*

**Problema**: assumo che io possa mantenere il dizionario che mappa termini (**stringhe**) a `termID` (**numeri**).

## SPIMI
* **idea 1**: genera dizionari separati per blocco per ogni termine
* **idea 2**: non fare il sort. non ce n'e' bisogno
* **token**: coppia $(\text{term}, \text{docID})$. non uso piu il $\text{termID}$
![[Pasted image 20260318114401.png]]
* **riga 6**: aggiungi il nuovo termine al dizionario (implementato con hashing)
* **riga 7**: dal dizionario recupera la posting list
* **riga 9**: raddoppia lo spazio allocato **se** (**riga 8**) non basta.


**piu veloce di BSBI**:
* costruisco la posting list senza dover collezionare prima i token per poi farne il sort.
* ogni chiamata `SPIMI-Invert` scrive un blocco.
* L'algoritmo `SPIMI` fa il merge del prodotto delle chiamate a `SPIMI-Invert`, **come visto prima**
* **duplicati**: l'uso del dizionario implica che coppie identiche $(\text{term}, \text{docID})$ vengano mappate allo stesso posto nel dizionario. In **BSBI** avrei allocato spazio inutilmente!
* **compressione**: se so comprimere i dati, posso leggere e scrivere velocmenete.
* **complessita temporale**: $O(T) \in O(M \log M)$ assumendo $M \ll T$, $M=\text{numero di termi unici}$ ed $T=\text{numero di token totali}$

**lettura e scrittura su disco**: in questi contesti faccio tantissime scritture e letture. Devo cercare di ridurre

**compressione**: se riesco a comprimere i termini e i postings riesco a mettere piu roba in memoria, quindi SPIMI e' molto piu efficiente

## distributed indexing
* **single point of failure**: non deve esserci
* gemini che vantaggi ha rispetto a singola macchina? perche' e necessario in information retrieval?

**error prone**: tendenzialmente, con 1000 server con SLA pari a $99.9$. 63 giorni l'anno ho un guasto e devo chiamare un cristiano a ripararlo.

**master machine**: decide che deve fare lo slave. assegna indexing job alle macchine in idle da una pool


