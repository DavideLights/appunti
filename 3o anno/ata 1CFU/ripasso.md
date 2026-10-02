**minimum set cover**:
* **Input**: $U$ ed $S = \{  S_{1}, \dots \}$ sottoinsiemi di $U$
* **Soluzione**: $S \subseteq \mathcal S$ tale che $S$ copre tutto $U$
* costo: $\sum_{s \in S}c(s)$

**algoritmo greedy**:
* seleziona gli insiemi piu cost effective.
* $\alpha = \frac{c(S)}{|C-S|}$ ossia l'insieme che permette di recuperare piu oggetti al prezzo migliore
* itero finche non copro tutto $U$.

Siano $e_{1},\dots,e_{n}$ gli elementi presi dall'algoritmo in ordine da $U$:
1. $e_{1}$ viene preso con $\frac{c(S)}{n-k+1} \leq \frac{\text{OPT}}{n-k+1}$
2. Il costo totale della soluzione e' $\leq \sum_{k}^n \frac{\text{OPT}}{n-k+1} \leq H_{n }\text{OPT}$

dunque l'algoritmo greedy e' $H_{n} \text{-apx}$.

# min steiner tree

**Input**: $G$ grafo pesato ed $R$ sottoinsieme di $V$
**Soluzione**: $T$ albero che contiene i nodi $R$ ed opzionalmente i nodi $V-R$ detti steiner

**Min**: minimizzare il costo dell'albero $T$

metric steiner: grafo $G$ completo e triangle inequalty.

**metric steiner problem**: per passare da $I$ istanza per steiner ad $I'$ istanza per metric steiner
* in $T'$ l'arco $u,v$ ha come costo lo shortest path in $G$ per andare da $u$ a $v$
* per andare da $T'$ in $T$ allora sostituisco l'arco $u,v$ in $T'$ con lo shortest path in $G$  e ripristino i costi originali.

in generale vale che $OPT(I') \leq OPT(I)$

il problema viene risolto da MST ed e' $2\text{-apx}$:
* MST indotto su $R$, genera effettivamente un'albero che contiene tutti gli $R$ nodi

**proof**: costruisco tour euleriano su $T'$, e ricavo ciclo hamilton $C$ da $T'$
* $\text{cost}(M) \leq \text{ cost}(C) \leq 2\text{OPT}$
* dove $M$ e' l'albero generato dall'MST
* perche' un MST costa meno di un ciclo hamiltoniano che costa almeno meno di 2OPT

# traveling sales man

**Input**: grafo non diretto, completo, archi non negativi
* **soluzione ammissibile**: $C$ che visita ogni arco una sola volta.
* **misura**: somma dei costi de

**teorema**: per ogni funzione calcolabile in tempo polinomiale $\alpha(n)$ allora TSP non puo' essere approssimato di un fattore $\alpha(n)$.

sia $A$ algoritmo per $\text{TSP}$ $\alpha(n)\text{-apx}$
* sia $G$ istanza di un ciclo hamiltoniano
* sia $G'$ completo costruito su $G$
	* $c(u,v)=1$ se l'arco appartiene a $G$ altrimenti costa $n\alpha(n)$
* cerco un ciclo hamiltoniano in $G$
	* se costa piu di $n\alpha(n)$ allora non ho trovato soluzione TSP
	* se costa $n$ allora top.


# minimu set cover LP
vogliamo minimizzare set cover:
* $\sum_{S\in\mathcal S} c(S)x_{S}$ con $x_{S}\in \{ 0,1 \}$
* **vincolo**: $\sum_{S: e\in S} x_{S} \geq 1$ per ogni $e\in U$

versione rilassata:
* $\sum_{S \in \mathcal S} c(S) x_{S}$ con $x_{S}\geq 0$
* stesso vincolo, devo prendere ogni oggetto almeno una volta

risolvendo la versione rialssata otteniamo $\text{OPT}_{f}$, ossia la soluzione frazionaria che include tutte le soluzioni intere.


La soluzione intera si ottiene prendendo tutti gli insiemi che hanno $x_{S}\geq \frac{1}{f}$ con $f$ frequenza.

questo
