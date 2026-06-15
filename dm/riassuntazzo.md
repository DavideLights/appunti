## regressione lineare
* usa le stesse regole di adaline

**regressione lineare stocastica**:
* sia $b=\frac{n}{\text{batch\_size}}$
$$
	w_{j} \gets w_{j} + \frac{1}{b} \sum_{i=1}^n (y^{(i)}-wx^{(i)})x^{(i)}
$$

## perceptron
**perceptron**: e' un classificatore lineare. 
* **classificazione**: $w_{1}x_{1} + \dots + w_{n}x_{n} \geq \Theta$ allora classifica come $+1$, altrimenti $-1$.
* **alternativamente**: con $x_{1}=1$ ed $w_{1} = -\Theta$ (unita bias), allora classifichiamo in base a $wx \geq 0$
* **piano separatore**: l'obiettivo e' trovare un piano separatore che classifica correttamente tutti gli esempi.

**regola di aggiornamento**:
$$
w_{j} \gets w_{j} - \eta (y^{(i)} - \hat{y}^{(i)})x_{j} 
$$
* la formula guarda se viene commesso l'errore'
* l'errore e' calcolato differenza di due valori discreti

**convergenza**: l'algoritmo trova un'piano separatore se e solo se l'istanza e' linearmente separabile.

**algoritmo di apprendimento**:
* per ogni esempio $x\in X$
	* calcola classifica con la regola $wx \geq 0$
	* se ho sbagliato $w_{j} \gets w_{j} - \eta (y^{(i)} - \hat{y}^{(i)})x_{j}$
* se non ho mai  sbagliato posso terminare, altrimenti ricomincia da capo

**classificare correttamente**: ho classificato correttamente $wx$ 

**prodotto scalare**: $xw = x_{1}w_{1} + \dots + x_{n} w_{n}$

**numero iterazioni massime**: 
$$
k = \frac{U^2}{\gamma^2}
$$
* $U \geq \max |x^{(i)}|$
* $\gamma = \max_{i} y^{(i)}{\frac{w^*x^{(i)}}{\|w^{(k)}\|}}$

**poiche**:
$$
1 \geq \cos(\beta) \geq \frac{k \eta \gamma}{n U \sqrt{ k }} > 0
$$

## adaline
**rispetto al perceptron**:
* **abbiamo funzione di attivazione**: $\phi(z)=z$
* **treshold**: la funzione a soglia per la classificazione $\phi(xw)\geq 0$ allora classifico come $+1$ con $w_{1}=-\Theta$ ed $x=1$.
* **obiettivo**: trovare il miglior piano separatore possibile, anche se l'istanza non e' linearmente separabile.

**funzione di aggiornamento di adaline**:
$$
w_{j} \gets w_{j} + \eta\sum_{i=1}^n(y^{(i)}-wx^{(i)})x_{j}
$$
* rispetto a prima, guardo l'errore globale ed aggiorno il peso di conseguenza
* l'errore e' calcolato su $wx^{(i)}$ che assume un valore continuo

**attenzione**: stiamo cercando il piano che minimizza al distanza tra il valore predetto ed l'etichetta reale, tuttavia il miglior piano potrebbe essere quello con distanze altissime!


## logistic regresison


**regressione logistica**:
$$
\phi(z) = \frac{1}{1+e^{-z}}
$$

**obiettivo**: voglio classificare usando una misura di probabilita. $P(y=1|x)=\text{probabilita di classificare come uno avendo visto } x$

**come arriviamo alla formula**? si vuole restringere il valore $wx \in [-\infty, +\infty]$.
* $\text{Odds}(p) = \frac{p}{1-p}$
* $\text{logit} = \log \frac{p}{1-p}$
* imponiamo $\log \frac{p}{1-p} = z \to \frac{p}{1-p} = e^z$ e cosi via

**funzione di errore**:
$$
\prod_{i=1}^n \phi(z)^{y^{(i)}}(1-\phi(z))^{1-y^{(i)}} =_{\text{log}} \sum_{i=1}^n y^{(i)}\log \phi(z)+(1-y^{(i)})\log(1-\phi(z)^{})
$$


**regola di aggiornamento**:
$$
w_{j} \gets w_{j } - \eta\sum_{i=1}^n(y^{(i)}-\phi(z))x_{j}
$$

# reti neurali
**architettura**:
* **input**: $d$ nodi, non sono i neuroni attivi, uno per feature che la processano l'input relativo e la passano al neurone nel layer nascosto.
* **ogni neurone ha il suo vettore di pesi**
* **output del neurone**: dipende dalla combinazione lineare del vettore delle feature del campione, con il suo vettore dei pesi. su questa applico la funzione di attivazione.
* **input del neurone**: ogni neurone prende in input $d$ feature su cui esegue il calcolo precedente.
* $e$ e' il pedice che indica un'etichetta
* **classificazione**: per maggioranza sull'output dei neuroni in output.
* **neuroni in output**: il neurone $e$ usa il vettore $W_{e}^\text{OUT}$ ed il vettore composto dai risultati nel layer precedente.  
* **classificazione**: $x$ e' $\text{argmax}^t_{e=1}\{a_{e}^\text{OUT}\}$
* **termini noti**: sono $b^H = (b_{1}^H, b_{2}^H, \dots, b_{h}^H) = (w_{1,0}^H, \dots, w_{h,0}^H)$
* **etichette**: dove ho $1,..,t$ etichette