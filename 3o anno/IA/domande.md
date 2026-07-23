
## domanda 1
![[Pasted image 20260718022407.png]]

R: e' (C) in quanto una macchina che svolga funzione che richiedono intelligenza, in quanto svolte da essere umani, indica un'IA che agisca e che pensi come un'essere umano.


## domanda 2
![[Pasted image 20260718022531.png]]
1. OK, l'agente razionale si comporta come un'umano esperto.
2. NO, l'agente razionale per essere tale non ha bisogno per forza di conoscere con completezza l'ambiente circostante.
3. NO, razionale non vuol dire per forza che agisce usando attuatori nell'ambiente
4. SI, razionale vuol dire massimizzare un vantaggio su qualcosa
5. SI, razionale vuol dire agire, con un obiettivo, usando azioni, minimizzando costi e rischi.

La 3 e' sbagliata perche': *La razionalità non si interroga sul se l'agente stia usando gli attuatori, ma sul **come** li usa. Un agente è razionale solo se le azioni che sceglie di compiere (tramite i suoi attuatori) sono quelle volte a massimizzare la misura di prestazione o a raggiungere l'obiettivo nel modo migliore possibile, dati i costi e i rischi.*


## domanda 3
![[Pasted image 20260718023045.png]]
1. SI, genera stimoli per gli agenti, dato che deve immergerli in un'ambiente.
2. SI, un'agente e' definito tramite una Performance Measure che viene misurata dal software di simulazione in modo esterno all'agente.
3. SI, il simulatore raccoglie le azioni per aggiornare la sua rappresentazione del mondo e valutare gli agenti.
4. NO, il simulatore simula l'ambiente, sono gli agenti che con le loro azioni si modificano.

## domanda 4
![[Pasted image 20260718024345.png]]
1. NO, la distanza euclidea si usa per misurare la distanza tra due punti nello spazio
2. NO, l'euristica possibile a cui si fa riferimento e' quella in cui si contano le **caselle fuori posto**
3. SI, e' un'euristica che non sovrastima mai, ed e' una versione rilassata del problema dove posso muovere i numeri come cazzo mi pare.
4. NO, la combinazione lineare di euristiche, e' un euristica valida.

## domanda 5
![[Pasted image 20260718024719.png]]
* (A) NO, dipende dall'euristica
* (B) NO, se $A^*$ e' ottimo, non dipende dal problema da risolvere.
* (D) NO, in generale applicare un'euristica vuol dire avvicinarci prima alla soluzione ignorando percorsi con euristiche peggiori ma costi migliori. Tuttavia l'euristica Non e' un criterio approssimato.
* (E) NO, non c'ha proprio senso
* (C) SI. 

## domanda aperta 1
**(D)** Discutere la relazione tra la nozione di agente e di ambiente in AI. Si esplicitino esempi di applicazioni di AI in cui distinguere le due nozioni. Si facciano esempi di applicazioni che caratterizzano i diversi tipi di ambiente e di agente

**(R)** L'agente e' l'entita che raccoglie le percezioni inviate dall'ambiente e si rapporta di conseguenza tramite gli attuatori. Invece l'ambiente rappresenta il mondo all'interno del quale l'entita vive, si evolve e cambia in base a come l'agente (o gli agenti) agisce (o agiscono).

L'agente, agendo tramite gli attutatori, comunica all'ambiente la sua azione modificando quest'ultimo. L'ambiente raccoglie le percezioni degli agenti e oltre ad apportare le modifiche allo stato del mondo, puo' dare una valutazione esterna all'agente, della sua performance: "quanto e' coerente con lo stato del mondo l'azione scelta?"

L'ambiente e' il mondo all'interno del quale l'agente viene immerso. Gli ambienti sono estremamente vari e ne possiamo studiare varie caratteristiche:
* **osservabilità**: **completamente**, **parzialmente**, **non osservabile**. Indica cosa posso osservare dell'ambiente con i sensori che l'agente ha a disposizione. Se l'ambiente non e' osservabile, l'agente deve agire per capire in che stato si trova il mondo.
* **multi-agente**: ci sono piu agenti nell'ambiente? Questi agenti collaborano o competono?
* **prevedibilita**: **deterministico**, **non deterministico** e **stocastico**. Una volta che l'agente restituisce all'ambiente un'azione, il prossimo stato del mondo e' univocamente determinato? c'e una distribuzione di probabilità sul prossimo stato? oppure e' completamente non deterministico?
* **ciclo di iterazione**: **episodico** o **non episodico**. Un ambiente episodico indica che ogni azione e' indipendente dalle precedenti, dunque non c'e' bisogno di pianificare. Non episodico indica il bisogno di pianificare, l'azione al tempo $t$ dipende dalle azioni $1,\dots,t-1$.
* **staticita**: l'ambiente puo' essere statico, dinamico o semi-dinamico. Se statico l'ambiente non cambia stato mentre decido. Se dinamico cambia stato mentre decido, se **semi-dinamico l'agente cambia il suo stato mentre decide a causa della misura di valutazione** (es: passa troppo tempo da quando ho iniziato a calcolare la prossima mossa, allora lo stato interno dell'agente cambia).
* **discreto/continuo**: se l'**ambiente** e' **discreto**, puo' essere rappresentato usando un numero finito di valori. Se continuo allora viene rappresentato usando per esempio numeri reali.
* **noto/ignoto**: se **noto**, allora l'agente sa cosa succede per ogni sua azione. se **ignoto** l'agente deve imparare cosa succede dopo ogni sua azione al mondo

Dunque le caratteristiche dell'ambiente cambiano radicalmente il modo in cui struttureremo il programma agente. Indipendente dal tipo di agente che scegliamo di utilizzare (`Reflex`, `Learning`,  `Obiettivo`, `Valutazione di utilita`) dobbiamo scegliere il giusto algoritmo per la ricerca della soluzione ed eventualmente strutturare le azioni in modo da favorire l'esplorazione e l'acquisizione di conoscenza da parte dell'agente se necessario.


**Esempi per distinguere agente/ambiente**:
* **ChatGPT**: il modello generativo e' l'agente. Il mondo che osserva e' il testo input dell'utente
* **Algoritmo che consiglia cosa acquistare**: l'algoritmo esegue calcoli per stilare una classifica di oggetti che potrebbero interessare all'utente. Il mondo che osserva e' il database degli oggetti e le preferenze dell'utente.


**Esempi di applicazioni che evidenziano le caratteristiche dell'ambiente**:
* **Robot Taxi**: l'ambiente e' 
	* Non Deterministico: lo stato del mondo non e' univocamente determinato dall'azione scelta dal Robot Taxi, molti eventi sono completamente casuali, senza una distribuzione di probabilità.
	* Noto: il taxi sa come funzionano le leggi della fisica del mondo e si comporta di conseguenza. Non deve effettuare azioni esplorative per capire come funziona l'acceleratore, e la frenata sotto le leggi della Terra
	* Non-Episodico: per arrivare a destinazione devo pianificare un percorso da attuare
	* Continuo: la velocita del taxi e' un valore continuo
	* Parzialmente osservabile:  in generale con la telecamera e il LiDar non posso vedere tutto l'ambiente che mi circonda.
	* **Dinamico**: mentre decido il mondo cambia

* **Scacchi**:
	* **Deterministico**: dopo che agisco lo stato del mondo e' univocamente determinato.
	* **Noto**: ad ogni azione l'agente sa che effetto hanno sul mondo.
	* **Sequenziale**: devo adottare una strategia per vincere
	* **Completamente osservabile**: normalmente un giocatore di scacchi quando gioca vede tutta la scacchiera.
	* **Statico**: mentre decido l'ambiente non cambia
	* **Discreto**: la scacchiera ha un numero finito di configurazioni.

## domanda aperta 1 TF3
**(D)** Discutere gli algoritmi di ricerca per gli agenti razionali. Discutere gli algoritmi di ricerca euristica, definizione e varianti, proprietà necessarie per la loro applicazione ed i vantaggi nei problemi completamente osservabili e statici. Utilizzare come esempio un problema su cui discutere e confrontare l'esito di due algoritmi euristici diversi. Discutere poi come un algoritmo di ricerca locale differisce dai precedenti discussi. Definire le caratteristiche e le metriche per la sua valutazione.

**(R)** Un'agente razionale agisce per fare la cosa giusta, ossia persegue un'obiettivo massimizzando il **valore atteso della misura delle prestazioni**. Razionale non vuol dire pensare umanamente (ossia imitare il nostro modo di pensare), ma agire in modo efficace. Un'agente razionale infine ha dei sensori e degli attuatori per comunicare con il mondo esterno.

Gli algoritmi di ricerca euristica fanno parte degli algoritmi informati, e per stabilire il costo di un nodo durante la ricerca usano una funzione di costo $f(n)$ che incorpora l'euristica $h(n)$. L'euristica $h(n)$ e' una funzione che indica la "distanza" dallo stato del nodo $n$ allo stato obiettivo.

In Greedy Best First la funzione di costo e' $f(n)=h(n)$, quindi in modo Greedy estraiamo il nodo piu promettente dalla frontiera secondo l'euristica, controlliamo se soddisfa `goal` e in caso effettuiamo l'espansione. Il costo computazionale dell'algoritmo dipende da come scegliamo $h(n)$

Un'altro algoritmo visto e' A* che utilizza come funzione di costo $f(n) = g(n) + h(n)$ con $g(n)$ il path cost. L'algoritmo e ottimo e completo se $h(n)$ rispetta le seguenti proprieta:
* $h(n)$ non sovrastima mai il costo per arrivare al goal, ossia rispetto all'euristica ottima: $h(n) \leq h^*(n) \forall n$. **condizione di ottimalita per tree search**
* $h(\text{goal}) = 0$
* $h(n) \geq 0$
* $h(n) \leq h(n')+c(n,a,n')$: ossia $h(n') \geq h(n) - c(n,a,n'). **condizione di ottimalita per graph search**

Il costo computazionale di A* e' $O(b^{h^*-h})$ con $h^*$ l'euristica ottima, mentre la complessità spaziale e' $O(b^{(h^*-h)+1})$, che e' proibitiva.

La qualita dell'euristica si misura guardando $b^* = \text{branching medio rispetto all'euristica } h$. Se $b^* \sim 1$ allora l'euristica $h$ e' vicina all'ottimo.

Se tra due euristiche occorre la seguente relazione $h < h'$ **(dominanza)** vuol dire che $h'$ porta $A^*$ ad espandere meno nodi rispetto ad $h$. $h'$ restringe meglio il campo di ricerca rispetto ad $h$.

Nei problemi completamente statici e osservabili, posso osservare lo stato del mondo e poi pianificare con $A^*$ la soluzione migliore, infine posso eseguire la soluzione.

Prendiamo come esempio una griglia 8x8 su cui vengono posizionati degli ostacoli, un gatto, un topo e delle zone piu costose da percorrere rispetto a quelle normali. Il gatto deve raggiungere il topo. Analizziamo come si comporterebbero A* ed Best First Greedy con $h(n) = \text{manatthan distance}$:
* A* si muove verso il topo, facendo attenzione ad evitare le zone più costose in quanto quanto aumentano.
* Greedy Best Search si muove esclusivamente e rapidamente verso il topo non curandosi di ostacoli ed zone costose (eventualmente la ricerca ci sbattera' contro), guarda solo l'euristica, ossia la distanza in linea d'aria.

Gli algoritmi di ricerca locale si applicano in casi in cui abbiamo una funzione obiettivo da massimizzare e non ci interessa il percorso che l'algoritmo svolge per trovare la soluzione migliore. Si utilizza in ambienti completamente osservabili, statici e noti, deterministici.

Un'algoritmo di ricerca locale e' per esempio Hill Climbing... [da finre]

## domanda aperta 2.11

Considera il problema del vacuum cleaner dove l'ambiente: i limiti e gli ostacoli sono sconosciuti.
 **(D.a)** puo' un simple reflex agent essere  razionale per questo ambiente? 
 **(R.a)** Assumendo che l'agente conosca la posizione dello sporco, il simple reflex agent deve memorizzare per ogni stato la direzione in cui muoversi, e che deve eseguire `Suck` quando si trova sopra lo sporco, ma non potendo sapere dove si trovano gli ostacoli, l'agente si incastra in un loop dove si muove verso una direzione impraticabile.

(**D.b**) Puo' un simple reflex agent randomizzato avere performance migliori del simple reflex normale? Progetta l'agente e misura la sua performance.
**(R.b)** Un simple reflex agent randomizzato potrebbe comportarsi nel seguente modo: con $p=0.75$ esegui l'azione associata allo stato, altrimenti ti muovi in una direzione a caso. Con questo approccio, anche se c'e' un'ostacolo nella direzione prevista con $p=0.25$ posso prenderne una casuale. Tuttavia la performance di questo modello potrebbe fare schifo se c'e' una sequenza lunga  di stati che mi portano in direzioni bloccate.


(**D.c**) puoi creare un'ambiente in cui l'agente preforma male?
**(R.c)** basta creare un'ambiente con ostacoli che formano un labirinto.

**(D.d)** puo' un reflex agent basato su stati performare meglio del simple reflex agent?
**(R.d)** l'agente richiesto si ricorda dopo aver eseguito un'azione di movimento se quest'ultima e' riuscita, oppure no. di conseguenza puo' assumere che in quella direzione c'e' un'ostacolo e  scegliere una direzione random in cui muoversi tra quelle ancora disponibili.


## domanda 4.1
**(D)** Dai il nome ai seguenti algoritmi:
1. Local beam search con $k=1$. R: si comporta come un DFS, per ogni strato si tiene il nodo migliore e lo espande, ma non fa backtracking. 
2. local beam search con uno stato iniziale e nessun limite sugli stati nella open list. R: si comporta come BFS
3. Simulated Annealing con $T=0$? vuol dire che se la scelta e' peggiorativa l'esponente diventa $e^{-\infty} \to 0$. Dunque l'algoritmo accetta solo mosse migliorative, ossia Hill Climbing a scalata rapida
4. Simulated Annealing con $T = \infty$? vuol dire che se la scelta e' peggiorativa la sceglie sempre, dunque e' First Choice HC


## domanda 4.12
![[Pasted image 20260719152808.png]]
(D) agente in un labirinto 3x3, l'agente si trova in $(1,1)$ ed l'obiettivo e' in $(3,3)$. Le azioni $\text{Up, Down, Left, Right}$ fanno quello che ci si aspetta a meno che non ci sia un muro. L'agente non sa dove si trovano i muri.

(D.a) Spiega come riformulare questo problema di ricerca online come una ricerca offline su stati credenza. 
(R.a) Lo stato credenza iniziale e' costituito dagli stati dove l'agente si trova in posizione $(1,1)$ per qualsiasi combinazione dei muri. A partire da questa posizione posso tentare di muovermi, se l'azione riesce vuol dire che posso passare allo stato credenza fatto da stati in cui mi trovo nella nuova posizione ed in quel punto non c'e' un muro. Altrimenti passo nello stato credenza fatto di stati in cui in quel punto c'e' un muro e mi trovo sempre in posizione (1,1). Questo modello puo' essere usato per costruire l'albero AND-OR che ritorna il piano di contingenza per la risoluzione.  

(D.b) Quante percezioni distinte sono possibili nello stato iniziale? 
(R.b) Ho un'unica percezione dato che la configurazione e' sempre uguale e non percepisco le posizioni dei muri.

(D.c) Descrivi i primi branch del piano di contingenza. Quanto e' grande piu o meno?
(R.c) A partire dalla posizione iniziale posso provare 4 mosse, da cui si sviluppano 4 nodi AND che rappresentano gli stati in cui rimango fermo, e dunque so che c'e' un'ostacolo in quella direzione, e gli stati in cui invece mi sono mosso.
* se sono rimasto fermo, il piano di contingenza dovrebbe prevedere l'esecuzione di un'altra azione e cosi via
* se mi sono mosso, allora ricomincio testando le 4 mosse, ecc...
La grandezza dell'albero esplode in combinatoriamente, so tanti!

## domanda 3.14
1. DFS espande sempre almeno tanti nodi quanti $A^*$ con un'euristica ammissibile? Falso, DFS potrebbe per puro culo potrebbe arrivare alla soluzione, mentre $A^*$ potrebbe esplorare nodi con falsa speranza.
2. $h(n) =0$ e' un'euristica ammissibile per 8-puzzle? Si, poiche $0 \leq c(s,a,s') + 0$ ed $0 \leq h^*(n)$
3. $A^*$ e' inutile in ambienti continui (robotica, taxi, movimento)? $A^*$ se gli stati sono rappresentati da valori continui, allora la ricerca di $A^*$ potrebbe non terminare mai, dunque a meno che non venga limita come in IDA* e' inutile.
4. BFS e' completa se sono ammesse azioni di costo 0? Se azioni che costano tutte 0, allora tutte le soluzioni sono uguali, dunque e' completa ed ottima, perche la soluzione comunque viene trovata. Inoltre BFS non si basa sul costo per estrarre la soluzione .