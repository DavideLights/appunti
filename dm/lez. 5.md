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
