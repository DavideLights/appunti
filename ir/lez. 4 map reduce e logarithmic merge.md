## Distributed Indexing
**master**: assegna task ad altre macchine. E' considerata **safe** ed e' un *single point of failure*.
* **splits**: collezione di di docoumenti diviso in split.
* **split**: sottoinsieme dei documenti, la grandezza deve essere tale da poter essere gestita da un nodo.
* **pool**: insieme di macchine idle, che il master puo' estrarre.

**task paralleli**: ci sono due tipi di task da parallelizzare
* **parsers**
* **inverters**

**parser**: lo slave costruisce un indice in locale, sul sottoinsieme di documenti affidati
1. **assegnazione split**: master assegna uno split ad una macchina in idle
2. **elaborazione**: parser legge ed emette coppie $(\text{term}, \text{doc})$ in **chunk divisi per termini**.
3. **OSS**: ogni parser ha i sui chunk.

**partizionare i termini**: partiziono i termini in chunk in modo che gli stessi termini si trovino nello stesso chunk.

**inverter**: slave che costruisce le posting lists a partire da un chunk di termini.

**replicazione**: le posting lists costruite dagli slave, devono essere replicate.
![[Pasted image 20260318121849.png]]

**Esempio**:
1. Nella fase **Map** ho in input `d1: C came, C c'ed` ed `d2: C died.`
2. **Output del parser**: `<C,d1>, <came,d1>, <C,d1>, <c'ed, d1>, ...` ossia le coppie grezze.
3. Nella fase **Reduce**, colleziono per ogni termine nel chunk di interesse tutte le sue occorrenze tra i vari segment files. Ho in input `(<C,(d1,d1,d2)>, <died,(d2)>, <came,(d1)>, ...)` 
4. **Output dell'inverter**:  `(<C,(d1:2,d2:1)><died,(d2:1)>, <came,(d1:1)>,...)`

**MapReduce**: e' un paradigma figo
* $\text{map}: \text{input} \to \text{list}(k,v)$
* $\text{reduce}: (\text{k,list(v)}) \to \text{output}$ 

**document partitioned**: una macchina si occupa di collezionare termini di un sottoinsieme di documenti

**term partitioned**: una macchina si occupa di collezionare un sottoinsieme di termini.

**partition tollerance, consistency, availability**: non posso averne tutti e 3 insieme (*teorema*). Si sacrifica la consistency nell'IR.
## Dynamic Indexing
**assunzione**: i doc ID sono crescenti.
~~assunzione: la collezione e' statica~~

**eliminazione dei documenti**: uso un **vettore di bit** che indica i documenti eliminati.
**modifica dei documenti**: invalido e poi riassegno il doc id al documento.

**approccio**: 
* **main index**:
* **auxiliary/small index**: per i documenti nuovi, **interamente in RAM**
* **merge**: faccio la ricerca su entrambi gli indici e faccio il merge dei risultati.
* **re-index**: *periodicamente reindicizza dentro quello principale quando lo small index diventa troppo grande.*
* **problema**: il re-index costa troppo in memoria. Fare il merge dei due indici costa molto.

**soluzione**: ogni posting list e' un file in memoria.
* **merge**: faccio l'append scrivendo nel file della posting list corrispondente
* **assunzione**: docID crescenti.
* **problema**: troppi file, inefficiente in un sistema operativo.
## logarithmic merge
**assunzione**: lavoriamo assumendo che l'indice e' un file unico.

**obiettivo**: fondere strutture piccole, e toccare il meno possibile quelle grosse.

**schema**: sia $n=\text{grandezza indice ausiliario}$ e $T = \text{ numero di postings totale}$
* dovrei fare  $\frac{T}{n}$ merge guardando $T$ posting
* **complessita costruzione indice principale**: $\Theta(T^2 /n)$ merge al peio

**schema migliore, il logarithmic merge**:
* uso $\log_{2}\left( \frac{T}{n} \right)$ indici chiamati $I_{0}, I_{1}, \dots$ di grandezza $2^0n, 2^1n, 2^2n$ ecc...
	* **ossia**: mantieni una collezione di indici dove uno e' grande il doppio del precedente.
* $N$ elementi.
* **indice ausiliario in RAM**: $Z_{0}$ di grandezza $2^0 n$
	* **e' il piu piccolo**!
* **indici ausiliari in ROM**:
	* **indice ausiliario in ROM** $I_{0}$: viene creato quando $|Z_{0}| > n$ ed non esiste un'altro $I_{0}$ sul disco
	* **indice ausiliario in ROM** $I_{1}$: viene creato quando $|Z_{0}|>n$ ed esiste $I_{0}$ su disco. Allora $I_{1}$ e' il merge di $Z_{0}$ ed $I_{0}$
	* **indice ausiliario in** ROM $I_{2}$: viene creato facendo il merge di 2 indici $Z_{1}$ con $I_{1}$ (dove $Z_{1}$ e' il merge di $Z_{0}$ ed $I_{0}$), similmente a quanto fatto prima
	* **OSS**: $Z_{i}$ e' il nome che diamo al merge di $I_{i-1}$ con $Z_{i-1}$ 

graficamente, e' equivalente a cio:
![[Pasted image 20260702122839.png]]

**vantaggio di log merge**: faccio molti merge ma su collezioni piccole. vado a toccare quelle grandi poche volte.

**pseudo**:
![[Pasted image 20260702123054.png]]

**Costo log merge**:
* **numero di merge**: faccio al piu $O\left( \log\left( \frac{T}{n} \right) \right)$ merge per ogni posting.
* **costo totale dei merge**: faccio al piu $O\left( T \log \left( \frac{T}{n} \right) \right)$ merge.

**problema su caso reale, ossia correzione input utente**: per farlo devo sapere qual'era *probabilmente la parola che voleva inserire l'utente, ossia quella piu frequente tra i documenti.*

**calcolare frequenza parole**: con piu' indici e' difficile. Devo vedere quali documenti sono stati invalidati e ricalcolare la frequenza della parola. **E' un'operazione lenta.**

**soluzione**: uso solo l'indice principale per correggere le query.
* **ricostruzione indice**: *in parallelo ricostruisco l'indice da 0, quando e' pronto lo sostituisco con quello principale.*

# early bird su twitter
**obiettivo**: sono interessato ai tweet piu nuovi.

**multiple index segments**: segmenti piccoli che contengono fino a $2^{32}$ tweet, ogni posting e' una parola a 32 bit.
* **un segmento per volta**: posso accedere e scrivere un segmento alla volta.
* **e' piccolo**: tanto da stare in memoria.

**feature e funzionamento**:
* **parole a 32 bit**: perche' e' la dimensione di una word che un processore riesce a gestire con istruzioni native.
* **posting**: 24 bit per il tweet id e 8 per la posizione nel tweet.
* **-> aggiungere tweet alla posting list**: appendo sempre alla fine
* **-> traversal della posting list**: dalla fine, in modo da ottenere i tweet piu nuovi.

**indici read-only**: solo un indice puo' essere scritto e letto. Gli altri sono ottimizzati per essere read-only.
