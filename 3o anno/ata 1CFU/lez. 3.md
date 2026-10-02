# minimum set cover problem
**Input**: 
* set $U$ di $n$ elementi
* $\mathcal S=\{ S_{1},\dots,S_{k} \}$ collezione di sottoinsiemi
* $\forall s \in S$ c'e un costo positivo $c(S)$

**soluzione**: collezione $C \subseteq S$ che copre $U$

**minimizzare**: costo $\sum_{S\in C}c(S)$

**frequenza di un elemento** $e$: numero di insiemi a cui appartiene
$f$: frequenza dell'oggetto piu frequente

**Integer Linear Programming** per SC:
* vogliamo minimizzare $\sum_{S \in \mathcal S} c(S)x_{S}$
* **vincoli**: $\sum_{S: e \in S} x_{S} \geq 1$, $e \in U$
	* $x_{S} \in \{ 0,1 \}$
* rilassiamo $x_{S} \in \{ 0,1 \}$ con: $x_{S} \geq 0 \land x_{S} \leq 1$
	* $x_{S} \leq 1$ e' ridondante

**LP-relaxation**:
* minimizzare $\sum_{S \in \mathcal S} c(S)x_{S}$
* **vincoli**: $\sum_{S: e \in S} x_{S} \geq 1, e \in U, x_{S} \geq 0$
	* $\sum \geq 1$: *ossia ogni elemento deve essere preso almeno una volta*

**soluzione ammissibile**: e' un fractional SC.
* $OPT_{f}$: costo del minimo SC frazionale.

$$
OPT_{f} \leq OPT
$$
> l'insieme delle soluzioni frazionare ammissibili contiene quelle intere ammissibili

![[Pasted image 20260923221431.png]]
**algoritmo**:
1. trova una soluzione ottima al problema rilassato
2. seleziona gli $S$ per cui $x_{S} \geq \frac{1}{f}$ nella soluzione

**teorema**: l'algoritmo e' una $f\text{-approx}$ per SC

**proof**:
1. scegli un $e$ e considera al piu $f$ insiemi che contengono $e$
2. dato che $e$ e' coperto nella soluzione frazionaria, allora esiste $S: x_{S} \geq \frac{1}{f}$
3. sappiamo che $x_{S_{1}} + x_{S_{2}} + \dots \geq 1$ dunque almeno un'insieme prende $e$

## weighted vertex cover
**Input**: 
* grafo non diretto
* $c(v)$ costo dei vertici

**soluzione**: $U \subseteq V$ tale che ogni arco e' coperto

**misura**: minimizzare costo vertici nella soluzione

**approssimazione**: si può vedere come $LP\text{-rounding}$, dove $f=2$, dunque l'algoritmo visto prima e' $\text{2-apx}$ per Vertex Cover.

**esempio**:
* vedi una istanza di set cover come ipergrafo
	* ho dei vertici, che corrispondono agli insiemi possibili del vertex cover
	* gli archi sono gli elementi degli insiemi e collegano piu insiemi correlati tra loro
* siano $V_{1},\dots,V_{k}$ insiemi di cardinalità $n$ ognuno
	* considera $n^k$ iperarchi: ciascun'iperarco sceglie un vertice da $V_{i}$
	* tutti i vertici hanno costo 1
* $f=k$
* $\text{OPT}_{f}=n$ ossia seleziona ogni vertice ad $\frac{1}{k}$
* $OPT=n$: scegli $V_{1}$

# primale duale
**upperbound e lowerbound**: ogni soluzione ammissibile del problema duale, da un lower bound alla soluzione ottima del primale e viceversa

se le soluzioni del primale e del duale coincidono, allora ho trovato l'ottimo.

**teorema dualita LP**: un programma primale ha un ottimo finito se e solo se anche il duale lo ha. Se $x=(x_{1},\dots,x_{n})$ ed $y=(y_{1},\dots,y_{m})$ sono soluzioni ottime allora 

$$
\sum _{j=1}^n c_{j}x_{j} = \sum_{i=1}^m
 b_{i}y_{i}$$
**teorema debole**: se $x$ e $y$ sono soluzioni ammissibili per primale e duale, allora

$$
\sum _{j=1}^n c_{j}x_{j} \geq \sum_{i=1}^m
 b_{i}y_{i}
$$

**strategia greedy**: seleziona l'insieme piu cost-effective e rimuovi gli elementi coperti
![[Pasted image 20260923234335.png]]

**duale**: ogni $y_{e}$ rappresenta il contributo di ogni elemento, sotto il vincolo per cui $\forall S \in \mathcal S \sum_{e\in S}y_{e} \leq c(S)$ .

**lemma**: $\forall e \in U, y_{e}=\frac{\text{price}(e)}{H_{n}}$. allora $y$ e' una soluzione ammissibile per il duale

**teorema**: allora l'algoritmo greedy e' una $H_{n}$ approssimazione per SC.