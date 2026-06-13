**Obiettivo**: classificare in due classi. $-1$ e $1$

**Neurone**: 
* **input**: $x = (x_{1},\dots,x_{d}) \in R^d$.
* **output**: $1$ o $-1$.
* **cosa e'**? implementazione di una funzione decisionale di tipo lineare.
* **funzione lineare di riferimento**: $x_{1}w_{1} + \dots + x_{d}w_{d}$
* **classificazione**: con $\Theta$ fissato, se $x_{1}w_{1} + \dots + x_{d}w_{d} \geq \Theta$, allora $x$ e' classificato come 1, altrimenti -1.
* $w_{0}= -\Theta, x_{0} = 1$, allora: $x_{0}w_{0} + x_{1},w_{1} + \dots + x_{d}w_{d} \geq 0 \to x \text{ classificato come } + 1 \text{, altrimenti } 0$
	* $w_{0}$: **bias unit**, unita di polarizzazione.

**prodotto scalare**:
$$
w  \cdot x^T = x_{0}w_{0} + x_{1}w_{1} + \dots + x_{d}w_{d}
$$
**notazione per il neurone**: 
$$
\phi(w\cdot x^T) = 1 \text{ se } w\cdot x^T \geq 0 \text{, altrimenti }-1 
$$
* **input di rete**: $w \cdot x$
* **addestramento**: serve a trovare $w$.

> [!note] $x^T$
> Il vettore $x^T$ in riga, va trasposto e portato in colonna per effettuare la moltiplicazione con $w$.

**iperpiano**: con $x \in R^d$, allora $w \cdot x = 0$ e' iperpiano.
* **addestrare**: voglio trovare l'iperpiano che separa meglio gli esempi.

> Se gli $n$ esempi sono linearmente separabili, allora l'algoritmo trova l'iperpiano che li separa

![[Pasted image 20260612122659.png]]

**Algoritmo**:
1. **Inizializza** $w$
2. **Per $n$ epoche**:
	1. **test**: di $w$ su tutti gli esempi
	2. **se non ho errori**: stop.
	3. **altrimenti**: aggiorna $w$

**classificare** $x^{(i)}$: $x^{(i)}$ e' classificato correttamente se e solo se $y^{(i)}(w\cdot x^{(i)})> 0$ 
**altrimenti, aggiorno**:
$$
w = w + \eta y^{(i)} x^{(i)}
$$
* **$\eta$ eta**: tasso di apprendimento


**preliminari**:
* **prodotto scalare**: $a,b$ due vettori, allora: $a \cdot b = a_{1}b_{1}+\dots + a_{d} b_{d}$
* **modulo o lunghezza**: $||a|| = \sqrt{ a_{1}^2 + \dots + a_{d}^2 }$

**prop. 1**: con $\beta$ angolo tra $a,b$.
$$
a \cdot b= ||a||\; ||b|| \cos(\beta)
$$
* **perpendicolari**: $a,b$ sono perpendicolari se e solo se $a \cdot b = ||a|| \; ||b|| \cos(\beta) = 0$.

**prop. 2**: sia $H$ l'iperpiano
$$
H: w_0 + w_1 x_{1} + \dots + w_{d} x_{d} = 0
$$
* $(w_{1},\dots,w_{d})$ e' perpendicolare ad $H$.

**dim prop. 2**:  sia $H'$ l'iperpiano
$$
H': w_{1} x_{1} + \dots + w_{d}x_{d} = 0
$$
* $H'$ e' parallelo ad $H$
* sia il punto $p \in H'$, **allora il vettore direzione che dall'origine va in $p$ e' vettore direzione per $H'$, ma lo e' anche per** $H$.
* dato che $p\in H'$, allora vale  $w \cdot p = 0$. 
* sia $\beta$ l'angolo tra $p$ e $w$
$$
||w||\; ||p|| \cos(\beta) = 0
$$
* **soluzione**: deve essere che $\cos(\beta)=0 \iff \beta=\pm 90$.

**prop. 3 (distanza da $p$ ad $H$ piano)**:
$$
\frac{w \cdot p + w_{0}}{||w||}
$$

**Dim.** 
* sia $u \in H$
* $w \cdot u = -w_{0}$
* sia $\beta$ angolo tra $H$ e $p-u$

Allora, la distanza $d_{pH}$ da $p$ a $H$ è
$$

d_{pH} = \|p-u\| \sin(\beta).

$$

Applichiamo la Proprietà 1 ai vettori $p-u$ e $w$ (il vettore perpendicolare ad $H$, Proprietà 2):
$$

\cos(90-\beta) = \frac{w\cdot (p-u)}{\|w\| \|p-u\|} = \frac{||w||  \;||(p-u)||}{\|w\| \|p-u\|} \sin (\beta) = \sin(\beta)

$$
* $a \cdot b= ||a||\; ||b|| \cos(\beta) \to \frac{a \cdot b}{||a||\; ||b||}=  \cos(\beta)$
* $90-\beta$: il vettore $(p-u)$ e' "sollevato" di $\beta$ rispetto al  piano $H$, ma sappiamo anche che $w$ e' perpendicolare ad $H$

Sostituendo $\sin(\beta)$ nella formula per $d_{pH}$:
$$

d_{pH} = \frac{w\cdot (p-u)}{\|w\|} = \frac{w\cdot p - w\cdot u}{\|w\|} =

\frac{w\cdot p + w_0}{\|w\|}

$$

---

**Sia**: $H$ iperpiano che separa gli esempi di $X \in R^{m \times d}$.
* assumiamo che $H$ passi per l'origine, dunque $w \cdot x = 0$
* **se cosi non fosse**: posso estendere $X$ aggiungendo la dimensione $d+1$, con $x^{d+1}_{i} =1$ 
* **dunque ora**: abbiamo sempre un iperpiano che passa per l'origine.

**Obiettivo**: voglio trovare $w^*$ vettore dei coefficienti.
* **sia**: $w^{(k)}$ l'iperpiano generato al passo $k$
* **allora**: l'angolo tra $w^*$ e $w^{(k)}$ decresce, al crescere di $k$.

**margine** di $w^*$:
* e' il minimo tra le distanze degli esempi $x^{(i)}$ ed il piano $w^* \cdot x=0
* **se vale < 0**: vuol dire che $w^*$ non e' separatore!
* **altrimenti**: ho piano separatore.
$$

\gamma = \min_i \left\{ y^{i}\frac{w^*\cdot x^{(i)}}{\|w^*\|} \right\}.

$$
**limite superiore della norma**, e' $U$ tale che:
$$

U \geq \max_i \| x^{(i)} \|

$$
---
## analisi algoritmo
**algoritmo**:
* sia $w^{(0)} = (0,\dots,0)$
* $w^{(k)} = w^{(k-1)} + \eta y^{(i)}x^{(i)}$
* assumiamo che al passo $k$ aggiorno l'iperpiano, allora...
$$

y^{(i)} w^{(k-1)}\cdot x^{(i)} \leq 0 < \gamma \leq y^{(i)}\frac{w^* \cdot x^{(i)}}{\| w^* \| }

$$
Dalla proprietà del prodotto scalare:

$$

\cos(\beta) = \frac{w^* \cdot w^{(k)} }{\|w^*\|

\|w^{(k)}\|} = \frac{w^* \cdot w^{(k)} }{\|w^*\|} \frac{1}{\|w^{(k)}\|}

$$

### 1o fattore
**Ricordando la regola di aggiornamento:**
$$

\frac{w^* \cdot w^{(k)} }{\|w^*\|} = \frac{w^* \cdot w^{(k-1)} + \eta y^{(i)}x^{(i)}\cdot w^* }{\|w^*\|}

= \frac{w^* w^{(k-1)}}{\|w^*\|} + \eta\frac{y^{(i)}x^{(i)}\cdot w^* }{\|w^*\|}\geq \frac{w^* w^{(k-1)}}{\|w^*\|} +\eta \gamma

$$
ossia:
$$
\frac{w^* \cdot w^{(k)}}{\| w^*\|} \geq \frac{w^* \cdot w^{(k-1)}}{\|w^*\|} + \eta \gamma
$$


**Ripetendo per tutti i $k$:**
$$

\frac{w^* \cdot w^{(k)} }{\|w^*\|} \geq \frac{w^* w^{(k-1)}}{\|w^*\|} +\eta \gamma \geq \frac{w ^* w^{(k-2)}}{\|w^*\|} +2\eta \gamma \geq \ldots \geq \frac{w^* w^{(0)}}{\|w^*\|} + k\eta \gamma

$$
ossia:
$$
\frac{w^* \cdot w^{(k)}}{\|w^*\|} \geq \frac{w^* w^{(0)}}{\|w^*\|} k \eta \gamma
$$
ma $w^{(0)} = (0,\ldots, 0)$, dunque:
$$

\frac{w^* \cdot w^{(k)} }{\|w^*\|} \geq k\eta\gamma > 0.

$$
### 2o fattore
Passiamo al secondo fattore che definisce $\cos(\beta)$ ovvero $1/\|w^{(k)}\|$. Dalla regola di aggiornamento
$$

\|w^{(k)}\|^2 = \|w^{(k-1)} + \eta y^{(i)} x^{(i)}\|^2

$$
Se $a$ e $b$ sono due vettori di pari dimensione $d$, si ha $\|a+b\|^2 = \|a\|^2 + 2a\cdot b + \|b\|^2$. La dimostrazione è immediata:
$$
\|a+b\|^2 = (a_1 + b_1)^2 +\ldots + (a_d + b_d)^2
$$
$$
= a_1^2+\ldots+a_d^2 + 2a_1b_1 +\ldots+2a_d b_d + b_1^2+\ldots+b_d^2

$$
$$

= \|a\|^2 + 2 a\cdot b + \|b\|^2

$$
Quindi:
$$
\|w^{(k)}\|^2 = \|w^{(k-1)}\|^2 + 2 \eta y^{(i)} x^{(i)}\cdot w^{(k-1)} + \| \eta y^{(i)} x^{(i)} \|^2
$$
* **secondo termine**: e' $\leq 0$ (per via della regola di aggiornamento dei pesi)
* **terzo termine**: e' $\leq (\eta U)^2$
Tornando a $\|w^{(k)}\|^2$
$$

\|w^{(k)}\|^2 \leq \|w^{(k-1)}\|^2 + \eta^2 U^2 \leq \|w^{(k-2)}\|^2 + 2\eta^2 U^2 \leq \ldots \leq \|w^{(0)}\|^2 + k\eta^2 U^2 = k\eta^2 U^2.

$$

### Mettendo insieme primo e secondo fattore
* **oss**: al denominatore trovo la radice di $k \eta^2 U^2$
$$

1 \geq \cos(\beta) \geq \frac{k\eta\gamma}{\eta U\sqrt{k}} = \frac{\gamma\sqrt{k}}{U} > 0

$$
* **se $k$ cresce**, allora la relazione tende a 1
* **se tende a 1**, allora $\cos(\beta) \to 1$, ossia $\beta \to 0$
* **convergenza**: algoritmo converge in  $\sqrt{ k }= \frac{U}{\gamma}$ passi, dunque $k = \frac{U^2}{\gamma^2}$


## codice
![[Pasted image 20260522010802.png]]
Questa separazione trovata e' pericolosa! Ma il perceptron non trova la divisione migliore, trova la prima che separa 1 e -1! 


Cambiando feature, a con epoca massima 1000
![[Pasted image 20260522011533.png]]
![[Pasted image 20260522011542.png]]