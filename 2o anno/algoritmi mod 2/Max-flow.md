> **Input**: grafo G, pesato e diretto, dove per ogni arco e' definita $c(e)$ una funzione che definisce la quantità di flusso massima che quell'arco può' trasportare. Due nodi: $s,t$
> **Output**: $f$ max flow per il grafo G, da $s$ a $t$.
 
Per definire correttamente il problema serve sapere che:
* $val(f) = \sum_{\text{e out s}} f(e) - \sum_{\text{e in s}} f(e)$. Ossia il valore del flusso e' dato dalla capacita netta che attraversa il nodo s.
* $cap(A,B) = \sum_{\text{e in A}} c(e)$
* il **flusso netto su $(A,B)$** e' dato da: $\sum_{\text {e out A}} f(e) - \sum_{\text{e in A}} f(e)$.

La funzione di flusso deve rispettare:
* le **capacita**' degli archi: $f(e) \leq c(e) \;\; \forall e \in E$.
* **conservazione del flusso**: $\sum_{\text{e out v}}f(e) = \sum_{\text{e in v}} f(e)$.

Il problema del massimo flusso e' correlato a quello del **min cut**: ossia trovare un partizionamento dei nodi t.c. $s \in A, t \in B$ che minimizza la **capacita** tra tutti i cut.

## Algoritmo di Ford Fulkerson
E' un'algoritmo che sceglie in maniera greedy un path $s \to t$  su cui e' possibile inviare flusso. Quando tutti i path $s->t$ sono saturati l'algoritmo termina.

Il problema di questo approccio greedy e' che l'algoritmo se sbaglia **non aggiusta mai il tiro**. Per questo si crea la rete residua: $G_f$ dove per ogni arco viene creato un corrispettivo arco invertito dove $c_{f}(e)$ rappresenta il flusso della rete residua:
* $c_{f(e)} = c(e) - f(e) \; \text {se} \; e \in E$, ovvero: quanto flusso posso mandare ancora?
* $c_{f}(e) = f(e^{reverse})$, ovvero: quanto flusso posso togliere per aggiustare il tiro?

```pseudo
    \begin{algorithm}
    \caption{Ford Fulkerson}
    \begin{algorithmic}
      \Procedure{Augment}{$P, f, c$}
	    \State $\sigma \gets $ bottleneck capacity di P.
	    \For{$e \in P$}
		    \If {$e \in E$}
			    \State $f(e) \gets f(e) + \sigma$
		    \Else
			    \State $f(e^{reverse}) \gets f(e^{reverse}) - \sigma$
		    \EndIf
	    \EndFor
	    \Return {f}
      \EndProcedure
	  \Procedure{FordFulkerson}{G}
		  \ForAll {$e \in E$} \State $f(e) \gets 0$
		  \EndFor
		  \State $G_{f} \gets \text{rete residua di G con flow f}$
		  \While {$\exists P \; \text{path aumentante}$}
			  \State $f = $ Augment(P,f,c)
			  \State Aggiorna $G_f$
          \EndWhile
      \EndProcedure
      \end{algorithmic}
    \end{algorithm}
```

## Correttezza di Ford Fulkerson

> [!note] PROP. 1
> Per conservazione del flusso: dato $f: flow \text{ e } (A,B) \; \text{un qualsiasi st-cut}$ allora $val(f) = netto(A,B)$.

**Dimostrazione**: $val(f) = \sum_{\text{e out s}} f(e) - \sum_{\text{e in s}} f(e)$ che per propagazione del flusso e' $\sum\limits_{v \in A}(\sum\limits_{\text{e out v}} f(e) - \sum\limits_{\text{e in v}} f(e))$ ma dato che per conservazione del flusso i nodi più interni di $A$ hanno netto pari a 0 allora $val(f) = \sum_{\text {e out A}} f(e) - \sum_{\text{e in A}} f(e)$

> [!note] WEAK DUALITY
> con $f: \text{flusso qualsiasi}$ e $(A,B)$ un qualsiasi $\text{st-cut}$  allora $val(f) \leq cap(A,B)$ 

**Dimostrazione**: $val(f) = \sum_{\text {e out A}} f(e) - \sum_{\text{e in A}} f(e) \leq \sum_{\text {e out A}} f(e) = cap(A,B)$

> [!note] COROLLARIO
> Dalla **weak duality** segue che se $val(f) = cap(A,B)$ allora: $f$ e' **max flow** ed $(A,B)$ **min cut**.

**Dimostrazione**:
* $\forall f': val(f') \leq val(f) = cap(A,B)$.
* $\forall (A',B'): val(f) = cap(A,B) \leq cap(A',B')$.

> [!note] Max-Flow, Min-Cut Theorem
> Il valore di un Max-Flow e' la capacita di un Min-Cut, e se f: Max Flow allora non esistono cammini aumentanti in $G_f$

Si dimostra che le seguenti proposizioni sono equivalenti:
1. Esiste $(A,B)$ per cui $cap(A,B)=val(f)$.
2. $f$ e' **Max Flow**.
3. Non c'e' un augmenting path rispetto ad $f$.

**Dimostrazione**:
* $1 \to 2$: vera per **corollario**.
* $2 \to 3$: dimostrando il contrario, se $f$ non e' Max Flow allora posso ancora mandare flusso rispetto ad $f$.
* $3 \to 1$: allora vuol dire che posso creare un $\text{st-cut}$ dove $A$ e' l'insieme dei nodi raggiungibili da $s$. Gli archi che escono da $A$ sono saturati, quelli che entrano hanno flusso 0. 
## Scegliere i cammini aumentanti
Il numero di augmenting path può essere esponenziale.
* $val(f^*) \leq n C$
[[2o anno/algoritmi mod 2/Apx]]### Parametro $\Delta$
Usare un parametro di scaling $\Delta$, per cui vado a considerare il grafo $G_f(\Delta)$ fatto di archi che hanno capacita $\geq \Delta$.
Cosi ci sono: $O(m \, log C)$ augmentation e l'algoritmo esegue in $O(m^{2}\, logC)$
### BFS
Usando la visita BFS per scoprire i path, guardo prima quelli con meno archi. Quindi faccio al massimo $O(mn)$ augmentation e l'algoritmo esegue in $O(m^{2}\, n)$.

> [!note] Pseudopolinomiale
> Vuol dire che l'algoritmo esegue in $O(nmC)$ se e solo se tutti gli archi non hanno capacita massima uguale a $C$. Se cosi non fosse allora il numero di augmentation cresce esponenzialmente.

# Applicazioni Max Flow
## Matching Bipartito
Dato $G=(L \cup R, E)$ trovare matching di cardinalità massima. Un matching $M \subseteq E$ si dice **perfetto** se ogni nodo compare esattamente una volta in $M$.

> [!note] Teorema
> Esiste una corrispondenza 1-1 tra matching di cardinalita $k$ e flussi di valore $k$ in $G'$.

**Dimostrazione**: dato un matching di cardinalità $k$ posso creare un max flow di cardinalità' $k$ semplicemente immettendo flusso nei $k$ archi che partecipano al matching. Per propagazione del flusso: le $k$ unita che escono da $s$ si propagano.

Al contrario dato un flusso di cardinalità k, per ogni arco $L \to R$ questo partecipa al matching se e solo se ha flusso pari ad 1.

**Running time**: $O(nm)$, ho n nodi verso cui fare le augmentation.
## Disjoint Paths
Due path sono edge disjoint se **non condividono archi**.
> [!note] Teorema
> Esiste una corrispondenza 1-1 tra k path edge disjoint $s \to t$, e flussi di valore $k$ in $G'$.

**Dimostrazione** dati k path edge disjoint allora $f(e)=1$ se e solo se $e$ partecipa ad uno dei path edge disjoint. Dato che i path sono e.d. allora il valore del flusso e' k.

Al contrario dato ar[[2o anno/algoritmi mod 2/Programmazione Dinamica]]co con $f(e)=1$ allora per conservazione del flusso esiste un'altro $f(e')=1$ fino ad arrivare a $t$.
## Image Segmentation
* $a_{i} \geq 0, b_{j} \geq 0$
* $p_{ij} \geq 0$
* $V = \text {pixels}, E = \text {coppie di pixel adiacenti}$
* **Obiettivo**: trovare $(A,B)$ che **massimizza**: $\sum{a_{i}} + \sum\limits{b_{i}} - \sum\limits{p_ij}$

Il problema e' di massimizzazione, ma si può invertire per farlo diventare di **minimizzazione**: $\sum_{j \in B} a_{j} + \sum_{i \in A} a_{i}- \sum\limits p_{ij}$.

Per formulare come problema di Max Flow bisogna:
* aggiungere $s$ e $t$
* aggiungere $e=(s,a_{j} \;\; \forall a_j \in V$ con $c(e) = a_j$
* similmente per $e = (b_{j,}t)$ aggiungo gli archi con $c(e) = b_j$

Eseguendo ford fulkerson su questo grafo stiamo cercando $(A,B)$ che minimizza la formula obiettivo, dove $A:= \text{forground}$ e $B := \text{background}$.
