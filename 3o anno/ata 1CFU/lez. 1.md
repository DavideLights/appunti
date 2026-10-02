$\alpha$ **approx**: algoritmo che produce una soluzione all'istanza il cui valore, al caso peggiore, e' ha come distanza il **fattore** $\alpha$ dall'ottimo
* $\alpha$: approx ratio.
* $\alpha \geq 1$: minimizzazione
	* $\text{cost}(s) \leq \alpha \text{OPT}(x)$
* $\alpha \leq 1$: minimizzazione
	* $\text{value}(s) \geq \alpha \text{OPT}(x)$

# minimum vertex cover
* **Input**: grafo non diretto $G=(V,E)$
* **Soluzione**: $U \subseteq V$ tale che $(u,v) \in E$ e' coperto da $U$, ossia $u\in U$ oppure $v \in U$
* **Misura**: $|U|$ e' da **minimizzare**

**def**: $M \subseteq E$ e' **matching** se non ci sono archi in $M$ che condividono nodi

**def**: $M$ matching e' massimale se per ogni $e\in E \setminus M$, allora $M \cup  \{ e \}$ non e' matching.

**algoritmo. trovare vertex cover**:
1. parti da $G=(V,E)$
	1. rimuovi un arco $e=(u,v)$ a caso, da $G$, e tienilo da parte.
	2. rimuovi gli archi incidenti in $u$ e $v$
	3. ripeti se $G$ ha ancora archi.

**lemma**: i nodi degli archi trovati formano un VC ammissibile

**proof**: sia $M \subseteq E$ **maximal matching**, calcolato dall'algoritmo.
* **copertura**: l'algoritmo trova un Maximal Matching
	* **dunque**: i nodi del matching coprono tutti i nodi.
* **allora**: qualsiasi altro arco condivide nodi in $M$, e allora  e' coperto

**algoritmo e'** $\text{2-apx}$:
* sappiamo che l'algoritmo ritorna una soluzione ammissibile.
* sia $M$ maximal matching calcolato dall'algoritmo
* sia $U$ il vertex cover corrispondente
* allora una soluzione ottima ha almeno $|M|$ nodi
* ma $|U|=2|M| \leq 2 \text{OPT}$.

**lower bounding scheme**: $|U|=2|M| \leq 2 \text{OPT}$
* la grandezza di un maximal matching e' lower bound per VC

**D1: puo' l'approssimazione essere migliorata**?
1. sia $K_{n,n}$ un **grafo bipartito**
2. l'algoritmo seleziona tutti i $2n$ vertici
3. ma il vertex cover ottimale prende solo un lato del gravo bipartito.

![[Pasted image 20260921213805.png]]

**D2: si puo' trovare un'algoritmo con migliore apx usando il lower bounding scheme $|U|=2|M| \leq \text{OPT}$?**
* sia $K_{n}$ un **grafo completo**, ossia il caso peggiore su cui eseguire l'algoritmo.
* il maximal matching ha $(n-1)/2$ archi
* ed il vertex cover migliore e' fatto di $n-1$ nodi
* quindi il maximal matching non puo' essere usato per migliorare l'approsimazione

**D3: esiste un lower bounding scheme che porta ad un'approssimazione migliore per VC?** 
* e' domanda aperta

**Risposta parziale**:
* assumendo **unique games conjecture**
* se esiste una $\alpha \text{-approx}$ con $\alpha <2$, allora $P=NP$

# minimum set cover 
**Input**:
* $U$, universo di $n$ elementi
* $S=\{ S_{1},\dots,S_{k} \}$ collezione di sottoinsiemi di $U$.
* ogni $s\in S$ ha un costo

**Soluzione ammissibile**: $C \subseteq S$ che copre $U$

**misura**: $\sum_{S\in C}c(S)$.

**soluzione greedy**: seleziona l'insieme piu `cost-effective`.
* $\alpha = \frac{\text{cost}(S)}{|S-C|}$ con $S-C$ differenza tra $S$ l'insieme di nodi da inserire e $C$ nodi gia coperti.
* sia $\text{price}(s\in S)=\alpha_{S}$, ossia la cost effectiness dell'insieme utilizzato per prendere quell'oggetto.
* si vuole selezionare l'insieme il cui rapporto tra costo e nodi nuovi scoperti e' migliore.

Siano $e_{1},\dots,e_{n}$ l'ordine con cui ho preso gli elementi di $U$
* **Lemma**: $\forall k=1,\dots,n: \text{price}(e_{k}) \leq \frac{\text{OPT}}{(n-k+1)}$
* **dimostrazione**: 
	1. In un qualsiasi punto dell'iterazione, gli elementi non selezionati coprono $U$ con un costo peggiore di $\text{OPT}$
	2. sia $C'=U-C$ con $C$ ottimo, il costo per coprire gli oggetti non selezionati
	3. allora $\frac{\text{OPT}}{|C'|}$ spalma l'ottimo sui nodi non coperti
	4. quindi $\text{price}(e_{k}) \leq \frac{OPT}{|C'|} \leq \frac{OPT}{n-k+1}$

**teorema**: l'algoritmo greedy ha $\alpha=H_{n}=1+\frac{1}{2} + \dots + \frac{1}{n}$
* $\text{costo del cover} = \sum_{k=1}^n \text{price}(e_{k}) \leq \sum_{k=1}^n \frac{OPT}{(n-k+1)} \leq H_{n} OPT$
* $H_{n} = \text{serie armonica} \leq \ln n + 1$

**teorema**: esiste una costa $c>0$ per cui se esiste un algoritmo $(c \ln n)\text{-apx}$ per Set Cover, allora $P=NP$

**teorema**: se esiste una algoritmo con $c<1$, allora  tutti i problemi in NP si risolvono in $O(n^{O(\log \log n)})$
