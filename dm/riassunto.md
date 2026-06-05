# lez 1. 2. 3. 4.

## numpy
```python
# es 1: ritorna la lista l sezna duplciati, insieme ad una lista delle occorrenze
np.unique(l, return_counts=True)

# es 2: disegnare un punto
fig, ax = plt.subplots(figsize=(8,8))
ax.scatter(x,y,color='red', marker='*')

# es 3: estrarre i campioni da X etichettati come lab
z = X[np.where(ym == lab)]

# es 4: estrarre la moda 
uq, counts = np.unique(l, return_counts=True)
moda = uq[np.argmax(counts)] 
```
**cosa fa** `y==lab`?: ritorna lista di booleani, dove compare `True` se la condizione e' rispettata.
### tabella costi
| python           | numpy                                  | costo python | costo numpy             |
| ---------------- | -------------------------------------- | ------------ | ----------------------- |
| `append`         | `np.append`                            | `O(1)`       | `O(n)`: copia           |
| `pop`            | non supportato                         | `O(1)`       | --                      |
| concatenazione   | `np.concatenate`                       | `O(n+m)`     | `O(n+m)`                |
| ripetizione      | `np.tile`                              | `O(k*n)`     | `O(k*n)`                |
| **slicing**      | ritorna una vista sull'array originale | `O(k)`       | `O(1)` in **lettura**   |
| somma vettoriale | ...                                    | `O(n)`       | `O(n)` ma e' piu veloce |
| moltiplicazione  | ...                                    | `arr * 3`    | `O(n)`                  |
## KNN:

**struttura della classe**:
* `fit`: consiste nella **memorizzazione** del data set
* `predict`: 
	* **insertion sort**: esegue in $\Theta(kn)$.
	* **kd tree**: esegue in $\Theta(k \log n)$

al variare di $k$:
* **se troppo grande**: il modello e' generalista, molti campioni contribuiscono all'etichetta di un campione.
* **se e' troppo piccolo**: allora il modello fa overfitting, la classificazione dipende molto dal training set.
## k-d tree
* **costo ricerca**: $O(\log n)$ in media, al caso peggiore $O(n)$
* **costo di costruzione**: $O(d n \log n)$ per costruire un albero bilanciato, per farlo devo ordinare i termini, ==per ogni dimensione==.

**a che serve?** permette di cercare efficientemente campioni su $d$ dimensioni. La ricerca e' strutturata ad albero, ad ogni nodo corrisponde un campione di riferimento su cui applicare il test. La dimensione di riferimento su cui applicare il test si alterna di livello in livello

**nodi**: i nodi dell'albero rappresentano un campione, dove a sinistra e a destra si trovano i campioni con coordinata minore o maggiore rispetto ad un certo valore

**foglia**: e' il risultato della ricerca (???)

**Mediano**: ogni nodo dell'albero dovrebbe rappresentare il mediano, in modo da dividere bene il sottoinsieme che quel nodo rappresenta.

**perche' al caso peggiore** la ricerca costa $\Theta(n)$? L'algoritmo di ricerca fa backtraking, al caso peggiore sbaglia sempre.

**perche' all'aumentare di $d$ la ricerca degrada**? il numero di nodi cresce esponenzialmente.
## IRIS e quadrati
**identificare la feature piu inutile**: e' stato fatto escludendo a turno una feature, ed identifichiamo il sottoinsieme di feature che performa meglio.
* **oppure**: approccio incrementale, ossia piano piano aggiungo features e vedo come varia l'accuracy (in meglio o in peggio)

**effettuare lo split del dataset correttamente**: devo ritornare dei sottoinsiemi bilanciati di dati. sia `train_size` la grandezza del train che voglio ottenere.
1. prendi la cardinalità delle classi che compaiono nel dataset
2. per ogni classe `c`: prendi a caso `train_size%` campioni dalla classe `c` e mettili nel train set, gli altri vanno nel test 

```python
for e in labs:
	a = np.where(y==e)
	# scegli randomicamente e butta in train_idxs!
	np.random.choice(a, size=int(n0*train_size), replace=False)
# fai append degli indici
# ...
np.setdiff1d(np.arange(n), train_idxs)
```

**classificazione quadrati**: sono state scelte le seguenti features per una corretta classificazione
* varianza della **distanza dal bounding** box
* varianza della **distanza dal centroide** del poligono.
# lez 5. 6. 7. 8.
## standardizzazione
**standardizzazione**: serve a ridurre il peso che hanno campioni con valori molto grandi, rispetto a campioni con valori piu piccoli, poiche in fase di addestramento potrebbero modificare pesantemente i pesi del classificatore. *si porta inoltre*:
* **deviazione standard a** 1
* **media a** 0

per **standardizzare** il data-set $X$ si applica: 
$$
X^{\text{std}} = \frac{X -\mu}{\sigma}
$$
**ottenere intercetta dai dati standardizzati**:
$$
w_{0}^{\text{std}} + w^{\text{std}}x^{\text{std}}=  w_{0}^{\text{std}} + \sum_{i=1}^d w^{\text{std}}_{i}\frac{x_{i} - \mu_{i}}{\sigma_{i}} 
$$
$$
= \underbrace{w_{0}^{\text{std}} - \sum_{i=1}^d w^{\text{std}} _{i}\frac{\mu_{i}}{\sigma_{i}}}_{\text{la nuova intercetta } w_{0}} + \sum_{i=1}^d  \frac{w^{\text{std}}_{i}}{\sigma_{i}} x_{i}
$$

**MAE**: Mean Absolute Error. Per calcolare quanto sbaglia il modello in media.
$$
\frac{1}{n} \sum_{i=1}^n|y_{i} - z_{i}|
$$
## Regressione Lineare con discesa gradiente
**costo addestramento**:$O(\text{epoche} \cdot nd)$

**trovare** $w^*$. ci sono due metodi:
* $(X^T X)^{-1} X^T y$: fare questa moltiplicazione costa $O(n^3)$, e la matrice potrebbe non essere invertibile
* discesa del gradiente.

**funzione di errore** $J$:
$$
J(w) = \frac{1}{2} \sum_{i=1}^n(y^{(i)} - w_{i} \cdot x^{(i)})^2
$$ 
**come aggiorno i pesi**?
$$
w \gets w -\eta \nabla J(w)
$$
* **significato**: voglio andare in direzione opposta rispetto alla derivata del gradiente, ossia il vettore che indica dove cresce la funzione, io voglio scovare il minimo.
* **tasso apprendimento**: $\eta$. Moltiplica il vettore direzione per la discesa del gradiente. piu' e' grande e' piu scendo velocemente verso il minimo.
	* **troppo grande**: non converge mai, potrei sempre saltare il minimo, o potrebbe addirittura aumentare l'errore
	* **troppo piccolo**: ci mette troppo a converge, rischio di overfitting.


**gradiente di** $J$:
> [!attenzione] derivata di funzione composta
> $f(g(x))$ diventa $f'(x)g(x)$ o qualcosa del genere.

$$
\frac{\partial J(w)}{\partial w_{j}} = \frac{1}{2}\left(\sum_{i=1}^n (y^{(i)} - wx^{(i)}) \frac{\partial}{\partial w_{j}}(y^{(i)} - wx^{(i)})^2 \right)
$$
$$
\frac{1}{2} \left(\sum_{i=1}^n (-2x_{j}^{(i)})(y^{(i)} - wx^{(i)}) \right)
$$
$$
\sum_{i=1}^n \left( x_{j}^{(i)}(y^{(i)}-wx^{(i)})\right)
$$
* **nota**: $wx^{(i)}$ e' prodotto di due vettori, dunque diventa $\sum_{i=1}^d w_{i}x_{i}$ da **derivare rispetto** ad $w_{j}$.

**vettore errori**:
$$
\texttt{errors} = \left(
\begin{array}{c}
y^{(1)}-w\cdot x^{(1)}\\
\vdots\\
y^{(n)}-w\cdot x^{(n)}
\end{array}
\right)
$$

**dunque**:
$$
\nabla J(w) = -X^T \times \text{errors}
$$

**come inizializzo i pesi**? valori random vicino a 0

**implementazione**:
```python
def fit(self, X, y):
	# standardizzazione e init pesi
	...
	
	for _ in range(self.n_iter):
		output = self.net_input(x_std)
		errors = y - output
		self.w[1:]-= self.eta * X.T.dot(errors)
		self.w[0] -= self.eta * errors.sum()
	
def net_input(self, X): return np.dot(X, self.w_[1:]) + self.w_[0]
```
**discesa del gradiente minibatch**: l'approccio minibatch divide in blocchi il dataset per l'allenamento. son o formati da **campioni scelti u.a.r.** Ad ogni epoca aggiorno applicando la funzione di errore guardando un blocco per volta. E' fantastico perche'
* **introduce rumore**: permette di uscire dai minimi locali
* **converge prima**: ad ogni epoca aggiorno più volte i pesi.
* **memoria**: devo tenere solo un blocco di memoria per volta.

**validation set**: viene utilizzato per implementare **early stopping**
* ad ogni iterazione uso una misura per vedere la qualita del modello sul validation set.
* se questa misura smette di migliorare di un tasso `tol` aumento `patience_count` di 1
* se `patience_count >= patience` allora non mi conviene piu continuare e interrompo


# lez 8. 9. 10. 11.

## alberi
**nodo**: valore, feature, insiemi $L \text{ e }R$, puntatori figli
* **foglia**: la classe per la classificazione si trova in **valore**
* **cosa rappresentano**? un test del tipo $\text{valore} \leq \text{feature}$.

**iperparametri**: numero minimo di nodi, indice di gini, altezza massima albero

**indice di gini**:
$$
I_{G}(D_{p}) = \sum_{c} \frac{n_{c}}{n}\left(1- \frac{n_{c}}{n}\right) = 1 - \sum_{c}\left(\frac{n_{c}}{n}\right)^2
$$
* $\frac{n_{c}}{n} = \text{ proporzione di }$
* se $n_{c}$ tende a 0 ed ho due classi 

> [!note] attenzione al **meno**!
$$
-I_{G(D_{p})} = \sum_{c} \frac{n_{c}}{n} \log \frac{n_{c}}{n}
$$

**costo predict**: $O(h)$

## cluster e db scan
**core point**: punto con almeno `min_pts` punti a distanza $\leq \text{eps}$
**border point**: se non e' core point ed e' vicino ad un core. possono essere in piu cluster
**noise point**: ne core e ne border.

**raggiungibilità**, $p$ raggiungibile da $q$ ...
* **direttamente**: se $p$ a distanza $\leq q$ con q **core**
* **direttamente per densità**: se $p$ e' raggiungibile attraverso una catena di core da $q$ **core**.
* **connesso per densità**: se $\exists r$ tale che $p,q$ connessi per densità ad $r$, con $r$ **core point**.

**cluster**: 
* $\forall p,q \in C$ allora $p$ e connesso a $q$
* se $p \in C$ ed $q$ raggiungibile per densita da $q$, allora $q \in C$ 

**costo db scan**:
* **ricerca puntia distanza $\leq \text{eps}$**: degrada facilmente, la ricerca da $O(\log n)$ passa ad $O(n)$ quando le **dimensioni sono elevate** (anche solo con $d\geq{10}$) e se ho **troppi** **campioni nel raggio** $\text{eps}$
  * **db scan completo**: per ogni punto devo cercare i punti a distanza $\leq eps$. assumendo questi siano in numero costante, devo vedere se sono cluster da espandere. **Costo** $O(n c\log n)$ in media

**algoritmo db scan**:
1. per ogni punto $p \in X$
2. se `label[p] != None`: continue
3. Ottieni i punti a distanza $\leq \text{eps}$ da $p$, mettili in $C$
4. se $|C| \geq \text{min\_pts}$: allora ho un cluster, espandilo.
5. altrimenti: `label[p] = Nosie`
6. ripeti.

**espansione**:
* per ogni nodo s $\in S$
* se `label[s] == Noise`: `label[s] = c`
* se `label[s] != None` return
* `label[s] = c`
* se s ha almeno `min_pts` nodi vicini, aggiungili ad $S$
* ripeti

**gomito**: per stimare epsilon si utilizza il gomito,
* $\frac{AP + AB}{A}$

## foresta
**a che serve**? costruisce $k$ alberi variegati, e su ognuno di questi classifica un campione. L'output e' l'etichetta che compare piu spesso in output.

**cosa implica/sostituisce l'uso di una forsta**? una foresta implementa un validation set per ogni albero. Ogni albero e' addestrato su un sottoinsieme del training set, il resto viene utilizzato come validation.

**bootstrap**: assegno ad un albero i campioni con questa tecnica. ossia estrazione casuale con reinserimento dal training set. Si dimostra che permette di lasciare il $66\%$ dei campioni fuori dall'albero, ed ogni coppia di alberi differisce per il $37\%$ dei campioni.

**quante feature**? seleziono $\sqrt{ d }$ features, con $d$ numero di feature nel dataset.

`oob_valutation`: serve per valutare i singoli alberi sui campioni sui cui non sono stati addestrati.
# lez 12. 13
## perceptron
**obiettivo**: classificare campioni in due classi. +1 e -1.

$$
w_{0} + w \cdot x = \Theta \to w \cdot x = 0 \text{ con } w_{0} = -\Theta \text{ ed } x_{0}=1
$$
* classifico con $+1$ se: $w\cdot x \geq 0$
* classifico con -1 se: $w \cdot < 0$
* $w_{0} = -\Theta$ e' il **bias** della rete.

**algoritmo**:
1. per ogni epoca, per ogni campione
	1. prova a classificare
	2. aggiorna i pesi ad ogni errore
2. se non ho mai sbagliato ritorna

**aggiornamento pesi**:
$$
w \gets w + \eta x^{(i)} y^{(i)}
$$
**prodotto vettori:** $a\cdot b$
**modulo**: $\|a\| =\sqrt{ a_{1}^2 + \dots + a_{d}^2 }$
**coseno**: $a \cdot b=\|a\|b\|\|\cos(\beta)$ con $\beta$ l'angolo tra $a,b$

**prop. 1**: $H: w_{0} + w_{1}x_{1} + \dots + w_{n}x_{n}$ e' perpendicolare a $w$.
dim...
**prop. 2**: la distanza di un vettore $v$ dal piano $w\cdot x$ e' 
$$
\frac {w \cdot p + w_{0}}{\|w\|}
$$
dim...

**H passa per l'origine**: si puo' **assumere** che $H$ passi sempre per l'origine, infatti se cosi non fosse si puo' aggiongere una **coordinata costante per tutti i punti** e passare in $d+1$ dimensioni

**convergenza dell'algoritmo**: si dimostra facendo vedere che $\cos(\beta) \to 0$ al cresce delle iterazioni $k$.

$$
\gamma = \min_{i}\left \{ y^{(i)} \frac{wx^{(i)}}{\|w\|} \right\}
$$
.
$$U \geq \max \{ \|x^{(i)}\| \}$$Dunque l'aggiornamento viene fatto in questo modo:
$$w^{(k)} = w^{(k-1)} + \eta y^{(i)}x^{(i)}$$
ed e' vero che:
$$y^{(i)}wx^{(i)} \leq 0 < \gamma < \min_{i}\left \{ y^{(i)} \frac{w x^{(i)}}{\|w\|} \right\}$$

analizziamo l'angolo tra $w$ e $w^*$:
$$\cos(\beta) = \frac{w^*w}{\|w^*\|\|w\|} = \frac{w^* w}{\|w^*\|} \frac{1}{\|w\|}$$**il primo termine**:
$$\frac{w^* w^{(k)}}{\|w^*\|} = \frac{w^{*}(w^{(k-1)} + \eta y^{(i)}x^{(i)})}{\|w^*\|} \geq \frac{w^* w^{(k-1)}}{\|w^*\|} + \gamma \eta$$
**applicandolo altre $k-1$ volte**:
$$\frac{w^{*}w^{(k)}}{\|w^*\|} \geq k \eta \gamma$$

**ora il secondo termine**: $\frac{1}{\|w\|^2}$
$$\|w^{(k)}\|^2 = \|w^{(k-1)} + \eta y^{(i)}x^{(i)}\|^2 \geq \|w^{(k-1)}\| +  \| \eta y^{(i)}x^{(i)}\|^2$$
$$\| \eta y^{(i)} x^{(i)}\|^2 = \|\eta x^{(i)}\| \leq \eta^2 U^2$$
applicando il tutto $k$ volte:
$$\|w^{(k)}\|^2 \leq \|w^{(k+1)}\| + n^2U^2 \leq \dots \leq kn^2U^2 \leq_{\sqrt{  }} \sqrt{ k }nU $$

dunque:
$$\frac{k\eta \gamma}{\sqrt{ k } nU} =\frac{\sqrt{ k } \gamma}{U} \to k = \frac{U^2}{\gamma^2}$$

## adaline
**obiettivo**: trovare il migliore piano separatore usando 
$$
J(w) = \frac{1}{2} \sum_{i=1}^n(y^{i} - wx)^2
$$
* $\phi(z)$ e' la funzione identita
* l'errore viene calcolato sempre, a differenza del perceptron

**aggiornamento pesi**:
$$
w_{j} \gets w_{j} - \sum_{i=1}^n(y^{(i)} - wx^{(i)})w_{j}
$$
* la funzione di errore spinge troppo in una direzione anche se la predizione e' corretta, ma la distanza tra predizione ed etichetta e' pesante.
* errore globale: guarda tutti i campioni

## regressione logistica
**obiettivo**: usare una misura di probabilita per descrivere quanto e' probabile che un campione sia classificato come $+1$ piuttosto che come $-1$

$$\frac{p}{1-p} = z \to \log\left(\frac{p}{1-p}\right)  = e^z \to p = \frac{1}{1+e^z}$$
**sigmoide logistica**: si deriva da sopra
$$\phi(z) =p = \frac{1}{1+e^z}$$

* **logaritmo**: incapsula il valore in $[0,+\infty]$
* **esponenziale nella frazione**: incapsula il valore in $[0,1]$

**funzione attivazione**: $\hat y(w\cdot x) = 1 \iff \phi(w\cdot x) > 0.5$ 

**nuova funzione di apprendimento**:
$$
\prod_{i=1}^n \phi(z)^{y_{i}}(1-\phi(z))^{1-y_{i}}
$$
$$\to_{\text{log}} \sum_{i=1}^n  \log(\phi(z))y_{i} + \log(1-\phi(z))(1-y_{i})$$
**derivata diventa**:
$$\frac{\partial}{\partial w_{j}} J = w_{j}(y_{i} - \phi(z))$$
**domanda esame**: perche' la versione stocastica converge prima?
1. fa piu aggiornamenti per epoca
2. il rumore permette di uscire dai minimi locali prima

# lez 15. 16.
## rete neurale
**struttura rete neurale**:
* **Layer input**: $x \in R^d$
* **Layer nascosto**: pesi $w_{f,h}$, $W^H \in R^{d\times h}$, attivazione in $a^H \in R^h$
* **Layer output**: pesi $w_{h,t}$, $W^{OUT} \in R^{h\times t}$, attivazione in $a^{OUT} \in R^t$
* $\sigma$: funzione logistica
* $b^H$ e $b^{OUT}$ sono i termini noti.

**propagazione in avanti**: 
* **strato nascosto**: $x \times W^H + b^H$, ossia $R^d \times R^{d\times h}$ 
* **strato output**: $a^H W^{OUT} + b^{OUT}$, ossia $R^h \times R^{h\times d}$
* **costo**: $O(dh+hd)$

**codifica one hot**: in $y = (y_{1},\dots,y_{t})$ solo una classe e' accesa, gli altri sono spenti.

> [!note] ricorda!

**backpropagation**:
$$J(w) = - \sum_{e=1}^t y_{e} \log(a_{e}^{OUT}) + (1-y_{e})\log(1-a_{e}^{OUT})$$

**discesa del gradiente su $J$**: quando devo aggiornare un un peso, devo derivare rispetto a tutti gli altri pesi. dunque costa $O(\text{epoche } n (dh + ht))$ che e' tantissimo

**chaining rule**: 
$$\frac{\partial \mathcal{J}}{\partial w^{\text{H}}_{f,k}} = -\sum_{e=1}^t \frac{\partial \mathcal{J}}{\partial a_e^{\text{OUT}}} \cdot \frac{\partial a_e^{\text{OUT}}}{\partial z_e^{\text{OUT}}} \cdot \frac{\partial z_e^{\text{OUT}}}{\partial a_k^{\text{H}}} \cdot \frac{\partial a_k^{\text{H}}}{\partial z_k^{\text{H}}} \cdot \frac{\partial z_k^{\text{H}}}{\partial w_{f,k}}$$

$$\frac{\partial J}{\partial w_{f,k}^H} = w_{f,k} \cdot a^H(1-a^H) \sum_{e} w_{k,e}^{OUT} \cdot (a_{e}^{OUT}-y_{e})$$
 **in vettori** (per il calcolo del costo computazionale dell'algoritmo)
$$a^H \odot (1-a^H) \odot ((a^{OUT}-y)(W^{OUT})) = \delta^H$$
* $a^H \cdot(1-a^H) \in R^{n \times h}$: $O(nh)$
* $a^{OUT} -y = t_{1} \in R^{n\times t}$: $O(nt)$
* $t_{1} \times W^{OUT} \equiv R^{n\times t} \times R^{t \times h}= R^{n \times h}$ $O(nth)$
* il prodotto componente per componente da in output $R^{n \times h}$
$$(\delta^H)^T X$$
* con $\delta^H \in R^{n \times h}$, allora $(\delta^H)^T \in R^{h \times n}$.
* $X \in R^{n \times d}$
* allora: $R^{h \times n} \times R^{n \times d} = R^{h  \times d}$ $O(hnd)$

**dunque il costo** e': $O(\text{epoche } nh(t+d))$

# lez 17. 18. 19
## svm
**obiettivo**: si vuole massimizzare la distanza tra $H^+$ ed $H^-$
* $H: w_{0} + w\cdot x = 0$
* mentre per le x tali che la classificazione e' = 1 si ottiene $H^{+}: w_{0} + w\cdot x = 1$
* mentre ... la classificazione e' = -1 si ottiene $H^{-}: w_{0} +w \cdot x = -1$.

**spacing**: si vuole massimizzare distanza tra $H^{+}$ ed $H^{-}$
$$d = \frac{w\cdot x^+}{\|w\|} - \frac{w \cdot x^-}{\|w\|} = \frac{1-w_{0}}{\|w\|}- \frac{-1-w_{0}}{\|w\|}= \frac{2}{|w|}$$
$$ \to_{\text{min}} \frac{\|w\|}{2} \equiv \frac{\|w\|^2}{2}$$abbiamo ricavato un **problema di minimizzazione** che deve sottostare al **vincolo**:
$$
y^{(i)} wx^{(i)} + w_{0} \geq 1
$$

**quando non separabili linearmente**:
$$\begin{cases}
w_{0} + wx^{(i)} \geq 1- \xi^{(i)} \text{ se } y^{(i)} = 1 \\ \\
w_{0} + wx^{(i)} \leq -1 +\xi^{(i)} \text{ se } y^{(i)}= -1
\end{cases}$$
* variabili slack aggiunte ai vincoli per ammorbidire il problema.

**ora dobbiamo penalizzare l'uso di queste variabili**, definisco la funzione di errore:
$$J(w) = \frac{\|w\|^2}{2} + C\sum_{i=1}^n \xi^{(i)}$$
**problema**: non posso derivare i vincoli!

**funzioni a cerniera**:
$$\max(0, 1-y^{(i)}(wx^{(i)} + w_{0}))$$
* ha un **punto angoloso**, dunque non e' derivabile, ma bisogna spezzarla in due casi

$$
J(w) = \frac{\|w\|^2}{2} + C\sum_{i=1}^n \max(0,1-y^{(i)}(wx^{(i)})+w_{0})
$$

**derivata di ** $J(w)$:
$$w \leftarrow \left\{

\begin{array}{lcl}

w - \eta w & & \text{se $y^{(i)}( w\cdot x^{(i)} + w_0 ) > 1$}\\

w - \eta \left(w - C y^{(i)} x^{(i)} \right) & & \text{altrimenti}

\end{array}

\right.$$
* $C$ controlla quanto dare peso a classificazioni errate, valori bassi penalizzano poco predizioni errate, e do priorita' alla massimizzazione del margine.
* se $C$ alto allora do priorita agli errori

## kernel tricks
**quando si usano**? quando non e' possibile classificare in $d$ dimensioni. magari aggiungere una dimensione aiuta.

**problema**: lavorare in piu dimensioni aiuta molto per la separabilita, tuttavia, lavorare esplicitamente in questi spazi può essere **molto costoso** dal punto di vista computazionale, *soprattutto quando il numero di feature è elevato o quando si considerano trasformazioni polinomiali di grado alto.*
* ***kernel trick**: risolve questo problema **evitando di calcolare esplicitamente la trasformazione** $\phi(x)$, che mappa i dati dallo spazio originale a uno spazio di dimensione più alta $\mathcal{H}$.

**funzione kernel $K$** permette di calcolare **direttamente, nello spazio di partenza, il prodotto scalare tra le immagini di due vettori nello spazio trasformato**:
$$ K(x_1, x_2) = \phi(x_1) \cdot \phi(x_2)$$
* posso calcolare di rettamente il prodotto di due vettori nello spazio di destinazione usando $K$
* funziona se il modello **si basa su moltiplicazioni tra vettori**
* risparimo notevole computazionale

**che kernel uso?** Un kernel molto diffuso è il kernel gaussiano o Radial Basis Function (RBF), definito come

$$K(x_1, x_2) =e^{\left(-\gamma \|x_1 - x_2\|^2\right)}$$
dove $\gamma > 0$ controlla l'influenza dei singoli punti di addestramento:
* **cosa fa?** *modera il problema dell'overfitting dovuto all'eccessivo aumento delle dimensioni nella proiezione*.
* tanto più gamma sarà grande tanto più **si da enfasi alle singole distanze tra i campioni**, ossia il margine si adatta di piu ai campioni
* **al diminuire di gamma**: il margine si allarga.

  
**$K$ espande su un numero potenzialmente infinito di dimensioni**: questa funzione può essere espansa tramite lo sviluppo in serie dell’esponenziale:
$$e^t = \sum_{n=0}^{\infty} \frac{t^n}{n!}$$
- prodotto scalare di un numero infinito di termini all'interno di uno spazio infinito.

## valutazione
* **bias elevato**: modello molto generico sui dati
* **alta varianza**: overfitting alto

**overfitting sul test set**: nel caso io voglia cercare i migliori parametri $C, \gamma$ devo 