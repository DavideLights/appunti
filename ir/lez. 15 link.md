**Good/Unkown/Bad**:
* nodo puntato da nodi **good**: allora e' good
* nodo puntato da nodi **bad**: allora e' bad
* **good non punta mai a bad**
* **se punti a bad, se bad.**

**Link nel web**:
* link $\equiv$ anchor text
* ipotesi 1: un link da $A$ a $B$ conferisce autorita da $B$
* ipotesi 2: il testo del link da $A$ a $B$ descrive $B$


**indicizzare anchor text**:
* sto indicizzando $D$
* prendi tutti gli anchor text, verso $D$ e indicizzali
* **problema spam**: se gli anchor text non sono affidabili? 
* **soluzione**: se ho giudizi sui documenti, posso pesare gli anchor text in modo da aumentare/diminuire il peso dei termini nell'anchor text

**rappresentare il web**:
* **liste di adiacenza**: per ogni URL, devo tenere in memoria gli **outlink** ed gli **inlink**
* Algoritmo Boldi e Vigna: fa la compressione degli URL/hyprlink (normalmente richiedono 64 bit) verso 2/3 bit per link.

**compresisone liste di adiacenza**:
* **proprieta utilizzate**: similarita, localita (ossia i link vanno verso "pagine vicine"), gap encoding, distribuzione dei gap values
* **modifiche**: posso definire una lista come modifica di un'altra lista!
* **gamma code**: usa $1+2\log x$ bit.

**proprieta**:
* **le liste definite come modifiche di un'altra sono poche**, e sono concentrate all'interno della stessa area.
* duqnue, la lista di modifiche da seguire e' corta.

## page rank
**link farm**: i vecchi browser assegnavano autorita in base ai link

**page rank**:
* **random walk**: prendi ogni arco di un nodo in modo equiprobabile
	* **variante**: analizza testo e link per calcolare la probabilita di seguire il link
* **dead ends**: la random walk potrebbe incastrarsi in vicoli cechi
* **teleporting**: salta ad una pagina casuale 
	* con una probabilita per esempio del 10%, in un qualsiasi momento teletrasportati.
	*  **a che serve?** imita un utente che naviga a cazzo di cane, ed ogni tanto segue i link
	* **conseguenza**: non posso incastrarmi localmente

**catene di markov**:
* $P_{ij}$ e' la probabilita di passare allo stato $j$ a partire da $i$ 
* **random walk**: e' esattamente un'implementazione di markov
* **long-term visit rate**: per ogni catena di markov questo valore e' unico

**probability vectors**: $x=(x_{1},\dots,x_{n})$ mi dice con codifica one-hot, in che stato mi trovo.
* sia $P$ matrice di transizione
* $xP$ e' il prossimo stato
* $xP^2, xP^3$ sono i successivi...
* **converge**?

**convergenza**:
* converge ad $a$ autovettore di $P$, con gli autovalori piu grandi
* $a: aP=a$
* **ossia**: la catena di markov comincia a stabilizarsi dopo molte iterazioni che applico le transizioni.

## hits
cosa ritorno come risultato per una query? due tipi di pagine...
* **hub pages**: liste di link su un certo tema
	* **good hub page**: vuol dire che punta a molte pagine autoritative.
* **authority pages**: liste di pagine che occorrono in hub marcati come good
* **a che serve**? utile per broad topi queries

![[Pasted image 20260713015511.png]]

schema:
* estrai il base set: pagine che potrebbero essere good hub, o autorita
* dal base set ricava un small set di top hub e top authority pages
* itera questo algoritmo descritto piu volte

**uso**:
* `query=browser`
* **root set**: composto da tutte le pagine che contengono `browser`
* **aggiungi al root set**: chi punta/e puntato ad/da una pagina nel root set 
* ho ottenuto il base set
![[Pasted image 20260713015842.png]]

**algoritmo iterativo**:
* per ogni pagina nel base set aggiorna $h(x) = \text{ hub score}$ ed $a(x) = \text{authority score}$
* $h(x) = \sum_{x \to y} a(y)$
* $a(x) = \sum_{y \to x} h(x)$
![[Pasted image 20260713020054.png]]**convergenza**: l'algoritmo converge dopo 5 iterazioni tipo.