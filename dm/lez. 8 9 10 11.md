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
IG(D_p) = I_G(D_{p}) - (\frac{n_{L}}{n} I_G(D_{L}) + \frac{n_{R}}{n}I_G(D_{R}))
$$
$$
I_{G}(D) = 1-\sum_{c}\left( \frac{n_{c}}{n} \right)^2= \sum_{c} \frac{1}{n}\left( 1-\frac{1}{n} \right)
$$
* **massimo con due classi** $(c=2)$: $1-\sum_{i=1}^c 0.5^2 = 0.5$, ossia quando le due classi sono **perfettamente mischiate**.
$$
I_{H} = -\sum_{c}\frac{n_{c}}{n}\log_{2} \frac{n_{c}}{n}
$$
**misure di impurità**: $I_{G}$ ed $I_{H}$

**addestramento**: per ogni nodi si calcola la feature e la dimensione migliore da usare, ossia quella che massimizza $IG(D_{i})$. La foglia e' il nodo che determina la classe da assegnare all'esempio.

**iperparametri**: impurità,  depth massima albero, dimensione minima del dataset.
* **depth**: determina il rischio di overfitting

## Implementazione
Un *nodo interno* è un dizionario con i seguenti campi:
- `'index'`: l'indice della colonna di `X` corrispondente alla caratteristica usata per il test;
- `'value'`: il valore con cui confrontare la caratteristica
- `'groups'`: una coppia che contiene $D_L$ e $D_R$
- `'left`, `'right'`: i riferimenti ai due figli

Un *nodo foglia* è semplicemente un valore, il nome della classe.


## complessita temporale
* `_get_best_split`: $O((nd)^2)$. Trova feature e valore che massimizzano il guadagno informativo.
* `_split_dataset`: $O(nd)$. Fai lo split in base a feature e valore.

# foresta
* $k$ alberi decisionali, variegati.
* **classificazione**: avviene prendendo l'etichetta piu frequente
* **iperparametri**: dimensione della foresta, dimensione insiemi di addestramento per ogni albero e numero di features usate

## varieta negli alberi
**bootstrap**: faccio una serie di estrazioni con reinserimento dal dataset per popolare gli insiemi di addestramento di ogni singolo albero.
* **features**: ogni albero viene addestrato su $d'=\sqrt{ d }$ features
* **campioni**: in totale addestro su $n' \equiv n$ campioni

**proprieta bootstrap**: in media
* un'albero viene addestrato sul $63\%$ dei nodi
* due alberi condividono il $37\%$ dei nodi