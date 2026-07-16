> [!note] attenzione all'overfitting
> Quando ho overfitting, il modo in cui il modello funziona dipende troppo dai dati in input per l'allenamento ed e' dunque poco flessibile.
> * funziona bene sul training set
> * funziona male su altri dati
> * Le features dovrebbero essere dati che mi dicono qualcosa anche su oggetti che non ho visto.

> [!note] troppe feature? allora...
> * troppa memoria
> * troppa complessita temporale
> * overfitting
> * funzioni di distanza degradano

> [!note] normalizzazione
> alcune feature potrebbero aver bisogno di essere normalizzate

## regressione lineare

![[regressione_lineare.excalidraw]]
**obiettivo**: cercare i coefficienti di un'iperpiano che approssimano meglio la funzione obiettivo.
$$
y = w_0 + \sum_{i=1}^d w_{i}x_{i}
$$
**assumiamo**: $x_{0} = 1 \to x=(1,x_{1},\dots,x_{d})$

$$
y = \sum_{i=0}^d w_{i}x_{i} = w \cdot x
$$

**matrice di addestramento ed output**: rispettivamente $X \in R^{n \times d} \text{ e } y \in R^d$, segue che $x^{(i)}\in R^d$ ed $y^{(i)} \in R$.
* $x^{(i)}$ e' la riga i-esima in $X$
* $y^{(i)}$ e' l'output di $f$ per $x^{(i)}$

**intercetta**: e' il punto in cui la retta della regressione intercetta l'asse delle ordinate $y$, ossia con le $x$.

**ho trasformato la formula standardizzata in una formula del tipo** $y= x_{0} + a_{1}x_{1} + a_{2}x_{2} + \dots$ dove:
* $x_{0}=\text{valore intercetta}$ (==ref.==)
* ed il resto corrisponde alla parte $\text{coefficienti di } x$
* ***cosa ho fatto**: ho evidenziato chi sono i coefficienti di $x$.
* **intercetta**: per definizione e' proprio $\text{valore intercetta}$, ossia $x_{0}$  (==ref.==)
## funzione errore e discesa del gradiente
**Somma degli errori quadrati**:
$$
J(w) = \frac{1}{2} \sum_{i=1}^n \left( y^{(i)} - w\cdot x^{(i)}\right)^2
$$
**obiettivo**: minimizzare $J(w)$, ci sono due modi
* calcolare $(X^T X)^{-1}X^T y$ con costo $O(n^3)$
* fare discesa del gradiente: voglio cercare $w^*$ che minimizza $J(w)$ aggiornando $w$ in direzione opposta al gradiente

**gradiente**: indica la direzione di massima pendenza positiva, dunque devo andare in direzione opposta. 

$$
w \gets w - \eta \nabla J(w)
$$
* $\nabla J(w)$ e' il vettore delle derivate parziali
* **tasso apprendimento**: $\eta$

### derivare sta funzione
$$
\frac{\partial J}{\partial w_j} = \frac{\partial}{\partial w_j} \frac{1}{2}\sum_{i=1}^n \left( y^{(i)} - w\cdot x^{(i)} \right)^2
$$
**derivata del quadrato**:
$$
 \frac{2}{2}\sum_{i=1}^n \left(( y^{(i)} - w\cdot x^{(i)} ) \cdot \frac{\partial}{\partial w_j}(y^{(i)} - w\cdot x^{(i)})\right)
$$
**sviluppo del prodotto tra vettori** $w \cdot x^{(i)}$:
$$
\sum_{i=1}^n \left(( y^{(i)} - w\cdot x^{(i)} ) \cdot \frac{\partial}{\partial w_j} (y^{(i)} -\sum_{k=1}^d w_{k}x_{k}^{(i)}) \right)
$$
**nella sommatoria sopravvive solo** $x_{j}^{(i)}$:
$$
\sum_{i=1}^n \left(( y^{(i)} - w\cdot x^{(i)} )(-w_{j})\right) = -\sum_{i=1}^n w_{j} \left( y^{(i)} - w\cdot x^{(i)} \right)
$$

> [!note] attenzione bro!
> * la derivata ha segno meno, dunque $w_{j} \gets w_{j} - \dots$ diventa $w_{j} \gets w_{j} + \dots$
> * dato che uso somma degli errori quadrati, l'aggiornamento di ogni peso e' influenzato dall'errore di tutti i pesi.

**vettore degli errori**:
$$
\texttt{errors} = \left(

\begin{array}{c}

y^{(1)}-w\cdot x^{(1)}\\

\vdots\\

y^{(n)}-w\cdot x^{(n)}

\end{array}

\right)
$$
**allora**:
$$
\nabla J(w) = -X^T \times \text{errors}
$$


## valutazione errrori
Per valutare l'errore su tutti i campioni usiamo il **MAE** (Mean Absolute Error)
$$
\frac{1}{n} \sum _{i=1}^n |y_{i} - z_{i}|
$$
## standardizzazione
**a che serve**? fa convergere prima l'algoritmo, ho bisogno di meno step per ottenere la soluzione ottima.
* in un dataset con varianza elevata e media non 0, la discesa del gradiente si muove in modo strano

![[Pasted image 20260606020722.png]]

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

## discesa del gradiente stocastica
**problema memoria**: su dataset enormi non posso fare discesa del gradiente, tenere in memoria $X$ potrebbe non essere fattibile.

**discesa stocastica**: aggiorno i pesi guardando una porzione della matrice $X$ ottenuta selezionando casualmente un numero fissato di righe.
* ossia: partiziono il dataset in blocchi casuali.
* **SGD puro**: se $X_{b}$ contiene un solo campione.
* **numero di aggiornamenti per epoca**: tanti quanti sono i blocchi
 
$$
\nabla J(w) = -X^T_{b} \times \text{errors}
$$

**formula**:
$$
w_{j} \gets w_{j}+ \frac{1}{|X_{b}|} \sum_{i\in X_{b}} w_{j} \left( y^{(i)} - w\cdot x^{(i)} \right)
$$