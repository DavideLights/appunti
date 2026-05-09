> [!note] attenzione all'overfitting
> Quando ho overfitting, il modo in cui il modello funziona dipende troppo dai dati in input per l'allenamento ed e' dunque poco flessibile.
> * funziona bene sul training set
> * funziona male su altri dati
> * 
>Le features dovrebbero essere dati che mi dicono qualcosa anche su oggetti che non ho visto, e che quindi generalizzi bene

> [!note] troppe feature? allora...
> * troppa memoria
> * troppa complessita temporale
> * overfitting

> [!note] normalizzazione
> alcune feature potrebbero aver bisogno di essere normalizzate
> gemini spiegami quando!

## regressione lineare

![[regressione_lineare.excalidraw]]

$$
y = w_0 + \sum_{i=1}^d w_{i}x_{i}
$$
**assumiamo**: $x_{0} = 1 \to x=(1,x_{1},\dots,x_{d})$

$$
y = \sum_{i=1}^d w_{i}x_{i} = w \cdot x
$$
**poiche**: $x_{0}w_{0}=1 \cdot w_{0} = w_{0}$

**matrice di addestramento**: se ho $n$ campioni da $d$ feature, allora $x\in R^{n \times d}$ e' la mia matrice per l'addestramento.

**output**: per ogni campione ho un valore $y_{i}$ in output, questi costituiscono dunque il vettore  $y \in R^n$.


**intercetta**: e' il punto in cui la retta della regressione intercetta l'asse delle ordinate $y$, sossia con le $x_{i}$.

**intercetta a partire dai dati standardizzati**:
$$
x_{i}^\text{std}=  \frac{x_{i} - \mu_{i}}{\sigma_{i}}
$$
$$
y = w_{0}^{std} + \sum_{i=1}^d w_{i}^{\text{std}}x_{i}^{\text{std}}
$$
$$
y = w_{0}^{\text{std}} + \sum_{i=1}^d w_{i}^{\text{std}}\frac{x_{i} - \mu_{i}}{\sigma_{i}}
$$
$$
y = \underbrace{w_{0}^{std} + \sum_{i=1}^d\frac{w_{i}^\text{std} \mu_{i}}{\sigma_{i}}}_{\text{valore intercetta}} + \underbrace{\sum_{i=1}^d \frac{w_{i}^\text{std}}{\sigma_{i}} x_{i}}_{\text{ coefficienti di } x}
$$
**ho trasformato la formula standardizzata in una formula del tipo** $y= x_{0} + a_{1}x_{1} + a_{2}x_{2} + \dots$ dove:
* $x_{0}=\text{valore intercetta}$ (==ref.==)
* ed il resto corrisponde alla parte $\text{coefficienti di } x$

**cosa ho fatto**: ho evidenziato chi sono i coefficienti di $x$.

**intercetta**: per definizione e' proprio $\text{valore intercetta}$, ossia $x_{0}$  (==ref.==)

## valutazione errore
$$
\frac{1}{n} \sum _{i=1}^n |y_{i} - z_{i}|
$$