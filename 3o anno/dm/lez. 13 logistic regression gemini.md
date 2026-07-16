Certamente, ecco un'analisi più approfondita che entra nel merito delle derivazioni matematiche e delle scelte implementative presenti nel notebook:

### 1. Adaline: Passaggi Matematici e Codice
**Sviluppo Matematico del Gradiente**
Il cuore di Adaline è la minimizzazione della funzione di costo (somma degli errori quadratici) $J(w) = \frac{1}{2}\sum_{i=1}^n \left( y^{(i)} - w\cdot x^{(i)} \right)^2$ tramite la discesa del gradiente.

Per trovare la direzione in cui scendere, si calcola la derivata parziale di $J(w)$ rispetto a ogni peso $w_j$. 
1. Applicando la regola della catena: $\frac{\partial J}{\partial w_j} = \sum_{i=1}^n \left( y^{(i)} - w\cdot x^{(i)} \right) \frac{\partial}{\partial w_j}\left( y^{(i)} - \sum_{k=1}^{d}w_k\cdot x^{(i)}_k \right)$.
2. La derivata interna rispetto a $w_j$ restituisce semplicemente $-x^{(i)}_j$.
3. Ottenendo infine: $\frac{\partial J}{\partial w_j} = -\sum_{i=1}^n x^{(i)}_j \left( y^{(i)} - w\cdot x^{(i)} \right)$.
    

**In forma vettoriale**, il gradiente diventa un elegante prodotto matrice-vettore:
$$\nabla J(w) = - X^T \times \text{errors}$$
* $\text{errors}$ è il vettore colonna delle differenze $(y^{(i)}-w\cdot x^{(i)})$.

**Osservazioni sul Codice (Classe `AdalineGD`)**
- **Vettorizzazione pura:** L'aggiornamento dei pesi delle features avviene con l'istruzione `self.w_[1:] += self.eta * X.T.dot(errors)`.
- **Gestione del Bias (`w[0]`):** Nel codice, l'aggiornamento dell'intercetta è separato: `self.w_[0] += self.eta * errors.sum()`. 
	- `w[0]` è associato a una "*variabile fittizia*" con valore costantemente pari a $1$, il che induce una riga di $1$ nella matrice trasposta $X^T$.
- **Funzione di Attivazione:** Per Adaline viene esplicitamente definita `def activation(self, X): return X`, ovvero una funzione identità. Nel fit, l'output non viene alterato prima del calcolo dell'errore.

### 2. Regressione Logistica: Passaggi Matematici e Codice
**Sviluppo Matematico dalla Sigmoide alla Log-Verosimiglianza**
La regressione logistica estende il modello lineare per restituire probabilità, effettuando passaggi molto precisi:
1. **Dagli Odds alla Sigmoide:** 
	1. Si parte dal concetto statistico di **Odd** $\frac{p}{1-p}$ 
	2. se ne prende il **logaritmo** per mappare le probabilità sull'intero asse reale: $\text{logit}(p) = \log\left(\frac{p}{1-p}\right) = w \cdot x = z$.
	3. Invertendo questa equazione rispetto a $p$, si ricava la formula della funzione sigmoide logistica: $p = \frac{1}{1+e^{-z}}$.
    
2. **Funzione di Costo:** A differenza di Adaline, qui l'obiettivo è massimizzare la probabilità congiunta (verosimiglianza) che tutti gli esempi siano classificati correttamente. Per poterla minimizzare con la discesa del gradiente, le si cambia di segno e si usa il logaritmo, arrivando alla funzione "Log-Verosimiglianza":    $$J(w) = -\sum_{i=1}^{n}\left( y^{(i)}\log\left(\phi(w\cdot x^{(i)})\right) + (1-y^{(i)})\log\left( 1-\phi(w\cdot x^{(i)})\right) \right)$$
3. **Derivata del Costo:** Il notebook mostra un risultato matematico sorprendente: calcolando la complessa derivata parziale della log-verosimiglianza, i termini si semplificano restituendo un'equazione identica a quella trovata per Adaline: $\frac{d}{d w_j} J(w) = - \sum_{i=1}^{n} x_j^{(i)} \left( y^{(i)} - \phi(w\cdot x^{(i)}) \right)$. L'unica differenza algebrica è che ora $\phi$ rappresenta la sigmoide e non l'identità.

**Osservazioni sul Codice (Classe `LogisticRegressionGD`)**
L'implementazione in Python dimostra quanto la regressione logistica sia parente stretta di Adaline. La classe è quasi la copia carbone della precedente, ma con le seguenti cruciali modifiche per accomodare la nuova matematica:
- **La Sigmoide prende vita:** Il metodo di attivazione viene modificato per implementare la formula ricavata: `def activation(self, z): return 1. / (1. + np.exp(-z))`.
- **Calcolo del Costo:** Nel loop di addestramento (`fit`), l'aggiornamento matriciale dei pesi rimane identico ad Adaline. Tuttavia, l'istruzione per il calcolo del costo cambia radicalmente per implementare la formula della log-verosimiglianza:
    `cost = -y.dot(np.log(output)) - ((1 - y).dot(np.log(1 - output)))`.
- **Predizione basata su Soglia:** Nel metodo `predict`, essendoci di mezzo delle probabilità, l'etichetta di classe viene stabilita se l'input di rete è maggiore di $0$ (il che equivale matematicamente a una probabilità del $50\%$ uscita dalla sigmoide): `np.where(self.net_input(X) >= 0.0, 1, 0)`.

# tutti i passaggi per funzione di log-verosimiglinza:
* Equivalentemente massimizzeremo il suo logaritmo naturale, ovvero la funzione
* L'obbiettivo è trovare $w$ che massimizzi la precedente espressione.
$$

\sum_{i=1}^{n}\left( y^{(i)}\log\left(\phi(w\cdot x^{(i)})\right) + (1-y^{(i)})\log\left( 1-\phi(w\cdot x^{(i)})\right) \right)

$$
Cambiando di segno la precedente diventa una funzione di costo differenziabile e che può essere minimizzata con discesa del gradiente.
$$

J(w) = -\sum_{i=1}^{n}\left( y^{(i)}\log\left(\phi(w\cdot x^{(i)})\right) + (1-y^{(i)})\log\left( 1-\phi(w\cdot x^{(i)})\right) \right) = -\sum_{i=1}^{n} \ell_i(w)

$$

dove abbiamo indicato con $\ell_i(w)$ la $i$-esima funzione nella sommatoria.
$$

\frac{d}{d w_j}\ell_i(w) = \frac{y^{(i)}}{\phi(w\cdot x^{(i)})} \frac{d}{d w_j} \phi(w\cdot x^{(i)})+

\frac{1-y^{(i)}}{1-\phi(w\cdot x^{(i)})} \left(0 - \frac{d}{d w_j}\phi(w\cdot x^{(i)}) \right)

$$
$$

= \left( \frac{y^{(i)}}{\phi(w\cdot x^{(i)})} - \frac{1-y^{(i)}}{1-\phi(w\cdot x^{(i)})}\right) \frac{d}{d w_j}\phi(w\cdot x^{(i)})

$$
$$

= \frac{y^{(i)} - \phi(w\cdot x^{(i)}) }{\phi(w\cdot x^{(i)}) \left(1-\phi(w\cdot x^{(i)})\right)} \frac{d}{d w_j}\phi(w\cdot x^{(i)})

$$
L'aggiornamento dei pesi $w_j$ segue il verso opposto del gradiente ovvero

$$
w_j \leftarrow w_j -\eta \frac{d}{d w_j} J(w)
$$
$$
\frac{d}{d w_j} J(w) = - \sum_{i=1}^{n} x_j^{(i)} \left( y^{(i)} - \phi(w\cdot x^{(i)})  \right)
$$
$$
w_j \leftarrow w_j +\eta \sum_{i=1}^{n} x_j^{(i)} \left( y^{(i)} - \phi(w\cdot x^{(i)})  \right)
$$
Usando le stesse considerazioni atte per Adaline
$$
w \leftarrow X^T \times \texttt{errors}
$$

Dove il vettore `errors` ha per componenti $y^{(i)} - \phi(w\cdot x^{(i)})$. Notare che quest'ultimo ha la stessa forma dell'analogo di Adaline, la differenza è nella definizione della funzione $\phi$ che nel caso di Adaline è la funzione identità mentre ora è la funzione sigmoid e logistica.


## logistic regression
Siano:
* $p$: classifico con classe 1
* $p=P(y=1|x)$: sapendo che $x$ sono le feature, la classe e' 1

**Usiamo Odd**: $\frac{p}{1-p}\in[0,+\infty]$
**in logaritmo**:
$$
\text{logit}(p) = \log\left( \frac{p}{1-p} \right)
$$
voglio riscrivere $p$ in funzione di $z=w \cdot x$:

$$\log\left( \frac{p}{1-p} \right) = z \to (*) \frac{p}{1-p} = e^z$$
![[Pasted image 20260525121627.png]]
![[Pasted image 20260525121645.png]]