**algoritmo alto livello**:
* **inizia con una soluzione** per il primale e per il duale
* **iterativamente**: migliora la soluzione duale ed migliora quella primale

**analisi**: dimostrare l'approssimazione usando il valore del duale come lowerbound.

**riprendendo minimum set cover**:

$$
\text{minimizzare} \sum_{S\in \mathcal S} c(S) x_{S} \equiv \text{massimizzare} \sum_{e \in U} y_{e}
$$
* $\sum_{S\varepsilon \in S}x_{s} \geq 1$ ed $x_{s} \geq 0$
* $\sum_{e: e\in S} y_{e} \leq c(S)$ con $y_{e} \geq 0$

**tight**: dato $y$, $S$ e' tight se $\sum_{e\in S} y_{e} = c(S)$

**idea**: seleziona solo insiemi tight

**algoritmo**:
1. inizializza: $x \gets 0; y \gets 0$
2. finche non copro tutti gli elementi
	1. scegli un elemento non coperto, e alza $y_{e}$ finche qualche insieme non diventa tight
	2. scegli tutti gli insiemi tight e calcola $x$
	3. dichiara gli elementi presi come covered
3. ritorna $x$

**teorema**: l'algoritmo e' $f\text{-approx}$

**proof**: il cover calcolato e' compatibile. alzo il prezzo degli $y_{e}$ finche non copro il costo degli insiemi.
* **claim**: $\sum_{S \in \mathcal S}c(S)x_{S} \leq f \sum_{e\in U}y_{e}$
* ogni elemento si trova in al piu $f$ insiemi
* $y$ rappresenta il problema duale: dunque $\sum_{e\in U} y_{e} \leq \text{OPT}$

# minimum steiner forest
**Input**: 
* grafo non diretto, con archi non negativi
* collezione di insiemi disgiunti di $V$: $S_{1}, \dots, S_{k}$

**soluzione**:
* foresta dove ogni coppia di vertici appartenenti allo stesso insieme $S_{i}$ sono connessi.

![[Pasted image 20260924013734.png]]

**minimizzare**: costo archi della foresta.

**metric**:
* $G$ completo
* costi soddisfano triangle inequalty

**connectivity requirement function**
$$
r(u,v) = 1 \text{ iff } u \text{ and } v \text{ appartengon allo stesso } S_{i} \text{ altrimenti } 0
$$

**funzione $f$ su tutti i cut in** $G$: $\forall S \subseteq V, S'=V \setminus S$
$$
f(S) = 1 \text{ iff } \exists u \in S \text{ and } v \in S' \text{ tale che } r(u,v)=1 
$$

linear programming:
* minimizzare $\sum_{e\in E} c_{e}x_{e}$
	* $\sum_{e: e \in \sigma(S)}x_{e} \geq f(s)$
	* $x_{e} \in \{ 0,1 \}$
	* rilassato $x_{e} \geq 0$
	* $\sigma(S) =\text{ archi che attraversano il cut su } S$ e $V \setminus S$
* massimizzare $\sum_{S \subseteq V} f(S) y_{S}$
	* $\sum_{S: e \in \sigma(S)} y_{S} \leq c_{e}$

![[Pasted image 20260924020742.png]]