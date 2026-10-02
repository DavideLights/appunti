# min steiner tree
**Input**: grafo $G=(V,E)$ non diretto, con archi non negativi.
* **required**: $R$ set di vertici richiesti
* **steiner vertices**: $V-R$

**Soluzione**: albero $T$, che contiene i vertici richiesti ed un sottoinsieme arbitrario degli steiner (eventualmente nessuno, oppure tutti)
$$
T: \sum_{e \in E(T)}c(e)
$$

**metric Steiner tree problem**: $G$ completo ed **triangle inequalty** $c(u,v) \leq c(u,w)+c(w,v)$

**teorema**: in termini di approssimazione lo stainer tree problem si riduce al metric steiner tree problem

**proof**: 
* sia $I$ istanza per Stainer **Tree**********
* in tempo polinomiale ottengo $I'$
* sia $I'$ istanza per metric Stainer Tree con
	* $G'=(V,E')$
	* $c'(u,v)=\text{costo shortest path } u-v$
	* $R'=R$
* $c'(u,v) \leq c(u,v) \to \text{OPT}(I') \leq \text{OPT}(i)$
	* quindi il costo di un nodo e' il costo per arrivarci e non il suo costo originale
* **convertire**: da $T'$ soluzione per $I'$, posso passare a $T$ soluzione per $I$ utilizzando al massimo lo stesso costo.
	1. rimpiazza ogni arco in $T'$ con lo shortest path in $G$
	2. scegli un qualsiasi spanning tree
1. allora $\text{cost}(T) \leq \text{cost(T')}$

**spanning tree**: ritorna una soluzione ammissibile.

**teorema**: algoritmo per MST  e' $2\text{-apx}$ per il problema metric ST.

**proof**:
* sia $T$ steiner tree di costo OPT ed $M$ un MST per $R$
* raddoppia gli archi di $T$, ossia un **grafo Euleriano**, ottengo costo $2 \text{OPT}$
* considera il tour Euleriano a partire dal graf oEuleriano
* ottieni il ciclo Hemiltoniano $C$ su $R$
	* utilizza il tour euleriano
	* salta i nodi steiner

![[Pasted image 20260921233050.png]]

* per triangle inequalty: $\text{cost}(C) \leq 2\text{OPT}$
* $C$ e' spanning subpgrah per $G[R]$ ed $\text{cost}(M) \leq \text{cost}(C)$

> ossia, sappiamo che un ciclo hamiltoniano completo ha costo $2\text{OPT}$, e che un minimum spanning tree costa meno di un ciclo hamiltoniano. dunque il minimum spanning tree trova una soluzione che costa mendo di 2OPT


# traveling salesman

**Input**: grafo non diretto, completo, archi non negativi

**soluzione ammissibile**: un ciclo $C$ che visita **ogni arco** una sola volta.

**misura**: somma dei costi degli archi nel ciclo.

**metric tsp**: versione del traveling salesman dove ogni arco soddisfa la triangle inequalty


**teorema**: per ogni funzione calcolabile in tempo polinomiale $\alpha(n)$, TSP non puo' essere approssimato di un fattore $\alpha(n)$, altrimenti $P=NP$.

**proof**: sia A algoritmo $\alpha(n)\text{-apx}$ per tsp
1. sia $G$ un ciclo hamiltoniano
2. sia $G'$ costruito su G
3. $c(u,v)=1$ se $(u,v)\in E(G)$ ed $c(u,v)=n \alpha(n)$ altrimenti.
4. **se** $G$ ha ciclo hamiltoniano allora TSP tour in $G'$ costa $n$
5. **altrimenti** il TSp costa $> n \alpha(n)$
6. **ossia**: $G$ ha ciclo hamiltoniano se e solo se A ritorna un tour di costo $n$

**algoritmo per metric tsp**:
1. calcola MST
2. ottieni grafo euleriano
3. ottieni tour euleriano
4. ritorna C tour che visita i nodi nell'ordine in cui lo fa il tour euleriano

**teorema**: l'algoritmo e' $2\text{apx}$

**proof**: 
* rimuovere un'arco dall'ottimo per TSP ci da uno spanning tree.
* allora $\text{cost}(T) \leq \text{OPT}$
* dunque $\text{cost(C)} \leq \text{2cost}(T) \leq 2\text{OPT}$

**algoritmo migliore**:
* un grafo e' euleriano se e solo se i vertici hanno grado pari
* in ogni grafo non diretto, il numero di arci **con degree dispari e' pari.**

1. trova mst di G
2. calcola il minimum cost perfect matching M, sull'mst di G considerando gli archi con degree dispari.
3. trova tour euleriano
4. output del tour in ordine di apparizione nel tour