# clustering
**parametri**:
* `min_pts`: numero minimo di punti a distanza al massimo `eps` per considerare un punto cluster.
* `eps`: distanza entro la quale due punti sono "vicini".

**definizioni**:
* `core point`: punto con almeno `min_pts` punti a distanza `eps`
* `border point`: non `core` ma a distanza `eps` da un core
* `noise point`: ne `core` e ne `border`

**raggiungibilità**:
* $p$ **raggiungibile direttamente per densità** da $q$: se $p$ distanza $\leq \text{eps}$ da $q$ core
* $p$ **raggiungibile per densità da** $q$: $\exists$ catena di core point da $q$ core, verso $p$
* $p$ connesso a $q$: se $\exists r$ tale che $p,q$ raggiungibili per densita da $r$

**cluster**: un cluster $C$ rispetta le seguenti proprieta
* se $p \in C$ ed $u$ raggiungibile per densita da $p$, allora $u \in C$
* se $p, u \in C$, allora $u,q$ connessi per densita.

**border**: puo' appartenere a piu cluster

### algoritmo `dbscan` per il clustering
1. per ogni nodo $x\in X$
2. se `label[x] != None`: `continue`
3. sia $V = \{ \text{vicini di } x \}$
4. **se** $|V| \leq \text{min\_pts}$, allora `label[x] = Noise`
5. **altrimenti**: `label[x]= str(x)` ed **espandi** $x$

**espansione** di $x$:
1. sia $S = \{ \text{ vicini di } x \}$
2. per ogni $s \in S$ : 
		1. se `label[s]==Noise`: `label[s]=str(x)`
		2. se `label[s]!=None`: **continua**, allora e' gia stato assegnato a qualcuno.
		3. se $|\{ \text{ vicini di } s\}| \geq \text{min\_pts}$: aggiungi ad $S$ i vicini di $s$


**Complessita**: 
$$
O(n \cdot(\log n + c \log n))
$$
* per ogni nodo devo estrarre i vicini: $n \log n$
* ipotizzando di aver estratto $c$ vicini, ogni nodo in $n$ deve essere eventualmente espanso, ossia per ogni vicino devo vedere se questo e' cluster mediante l'estrazione dei vicini $c$, dunque $O(nc\log n)$
* dunque il costo e' $n \log n$

## stimare eps migliore per il parametro $\text{min\_pts=k}$
per stimare eps si utilizza il metodo del **gomito**:
1. **ottieni per ogni nodo la distanza dal $k\text{-esimo}$ punto**
2. **ordina i punti**, per la distanza calcolata prima, dalla piu piccola alla piu grande.
3. **etichetta i punti e buttali su un grafico**, ottengo una curva che tende a crescere
4. **sia $AB$ la retta che unisce il primo punto con l'ultimo** punto ossia quello con distanza minima a quello con distanza massima
5. voglio trovare $P$ che massimizza la distanza con la retta: $\frac{AB \times AP}{\|AB\|}$

# albero di decisione
**obiettivo**: trovare una sequenza di test ottimi per la classificazione. ossia si vuole costruire un'albero di decisione ogni nodo vuol massimizzare il guadagno informativo

$$
I_{G}(D_p) = I_{G}
$$