![[reteneurale.excalidraw]]
**note sull'architettura**:
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

## Algoritmo di classificazione
**spiegazione righe e colonne**: ogni colonna e' il vettore dei coefficienti del neurone in quello stadio.

Nell'esempio ho 2 strati, dove ognuno ha la sua matrice di pesi: $W^H$(nascosto) e $W^\text{OUT}$:
* $W^H$: le righe sono le feature, mentre ogni colonna e' un neurone
* $W^\text{OUT}$: ho $t$ classi. Ogni neurone ha un peso per ogni classe
$$
\mathbf{W}^{\text{H}} =

\begin{bmatrix}

w_{1,1}^{\text{H}} & w_{1,2}^{\text{H}} & \cdots & w_{1,h}^{\text{H}} \\

\vdots & \vdots & \ddots & \vdots \\

w_{f,1}^{\text{H}} & w_{f,2}^{\text{H}} & \cdots & w_{f,h}^{\text{H}} \\

\vdots & \vdots & \ddots & \vdots \\

w_{d,1}^{\text{H}} & w_{d,2}^{\text{H}} & \cdots & w_{d,h}^{\text{H}}

\end{bmatrix}
$$
$$

\mathbf{W}^{\text{OUT}} =

\begin{bmatrix}

w_{1,1}^{\text{OUT}} & \cdots & w_{1,e}^{\text{OUT}} & \cdots & w_{1,t}^{\text{OUT}} \\

w_{2,1}^{\text{OUT}} & \cdots & w_{2,e}^{\text{OUT}} & \cdots & w_{2,t}^{\text{OUT}} \\

\vdots & \ddots & \vdots & \ddots &\vdots\\

w_{h,1}^{\text{OUT}} & \cdots & w_{h,e}^{\text{OUT}} & \cdots & w_{h,t}^{\text{OUT}}

\end{bmatrix}

$$
1. **attivazione strato nascosto**:
	1. calcolare $z^H$ costa $O(h \cdot d)$ (ossia moltiplicazione matrice per vettore)
$$
z^H = xW^H + b^H \in \mathbb R^{1\times h}
$$
	2. calcolare le attivazioni: $O(h)$ 
$$
a^H = \sigma(z^H)
$$
2. **attivazione output:**
	1. calcolare $z^{\text{OUT}} = a^H W^\text{OUT} + b^\text{OUT} \in \mathbb R^{1 \times t}$, ossia $O(t\cdot h)$
	2. calcolare le attivazioni: $O(t)$
3. prendi il massimo!

**Costo totale per clasificare un singolo campione**: 
$$
O(h \cdot d+ h + t \cdot h + t) = O(h \cdot d + t \cdot h) = \text{numero totale di tutti i pesi } N
$$

## Addestramento
Sia:
* **training set**: di $n$ campioni
* Se $x \in \mathbb R^d$, $y=(y_{1},\dots,y_{t})$ con $y_{e} \in \{ 0,1 \}$, ed $\sum_{e} y_{e} = 1$.
	* **codifica one-hot**: se $y_{e}=1$, allora $x$ appartiene alla classe $e$.

**obiettivo**: addestrare vuol dire trovare i pesi $w^H_{f,k}$ ed $w_{i,e}^\text{{OUT}}$ che minimizzano una funzione costo.

**funzione di perdita/cost**: e' una funzione log loss **binaria**
$$
\mathcal{J}(W^{\text{H}},W^{\text{OUT}}; \mathbf{x}, \mathbf{y}) = - \sum_{e=1}^t \left[ y_e \log a_e^{\text{OUT}} + (1 - y_e) \log (1 - a_e^{\text{OUT}}) \right]
$$
* generalizzo $t$ classi in questo modo, sappiamo che possono essere 0, oppure 1
* guardando l'immagine, $\mathcal J$ dipende direttamente da come funziona la rete.

**discesa del gradiente**:
$$
\frac{\partial \mathcal{J}}{\partial w_{j,k}} \approx \frac{\mathcal{J}(w_{j,k}+\epsilon) - \mathcal{J}(w_{j,k}) }{\epsilon}
$$
* $\epsilon$: fare un aggiornamento della rete basato su propagazione in avanti, modifica un solo peso della quantità $\epsilon$, bisogna scegliere questo valore, cosi posso approssimare la derivata!
* **si osserva successivamente il comportamento della rete** mediante una nuova propagazione in avanti, che costa $O(hd+ht)$.
* devo ripetere per ogni peso, ogni campione e per il numero di iterazione: $O(n(hd+ht)^2 \cdot \text{epochs})$
* **probleba**: ogni peso e' trattato individualmente.

> gemini spiega meglio perche' devo ricalcolare ogni volta le derivate, mi sono perso
## retro propagazione
**obiettivo**: Si vuole calcolare l'errore commesso dal modello e ridistribuirlo all'indietro riutilizzando dei calcoli intermedi.
![[Pasted image 20260525150958.png]]
**dipendenze**: in giallo sono evidenziate le **dipendenze** di $w_{fk}^H$.

**applichiamo la regola della catena**, da $J$ fino a $z_{k}^H$:
$$
\frac{\partial \mathcal{J}}{\partial w^{\text{H}}_{f,k}} = \sum_{e=1}^t \frac{\partial \mathcal{J}}{\partial a_e^{\text{OUT}}} \cdot \frac{\partial a_e^{\text{OUT}}}{\partial z_e^{\text{OUT}}} \cdot \frac{\partial z_e^{\text{OUT}}}{\partial a_k^{\text{H}}} \cdot \frac{\partial a_k^{\text{H}}}{\partial z_k^{\text{H}}} \cdot \frac{\partial z_k^{\text{H}}}{\partial w_{f,k}}
$$
* **cosa vuol dire?** a partire dal nodo interessanto, faccio il prodotto delle derivate!!!!in base all'input.
## Calcolo dei singoli termini:
1. Derivata log loss rispetto a $a_j^{\text{OUT}}$:
$$

-\frac{\partial \mathcal{J}}{\partial a_e^{\text{OUT}}} = - \frac{y_e}{a_e^{\text{OUT}}} + \frac{1 - y_e}{1 - a_e^{\text{OUT}}} = \frac{a_e^{\text{OUT}} - y_e}{a_e^{\text{OUT}} (1 - a_e^{\text{OUT}})}

$$
2. Derivata della sigmoid:
$$

\frac{\partial a_e^{\text{OUT}}}{\partial z_e^{\text{OUT}}} = a_e^{\text{OUT}} (1 - a_e^{\text{OUT}})

$$
3. Derivata di $z_e^{\text{OUT}}$ rispetto a $a_k^{\text{H}}$:
$$

\frac{\partial z_e^{\text{OUT}}}{\partial a_k^{\text{H}}} = w_{e,k}^{\text{OUT}}

$$
4. Derivata di $a_k^{\text{H}}$ rispetto a $z_k^{\text{H}}$:
$$

\frac{\partial a_k^{\text{H}}}{\partial z_k^{\text{H}}} = a_k^{\text{H}} (1 - a_k^{\text{H}})

$$
5. Derivata di $z_k^{\text{H}}$ rispetto a $w_{kf}$:
$$

\frac{\partial z_k^{\text{H}}}{\partial w_{f,k}} = x_f

$$
## semplificare
Riprendendo la catena:
$$
\frac{\partial \mathcal{J}}{\partial w^{\text{H}}_{f,k}} = -\sum_{e=1}^t \frac{\partial \mathcal{J}}{\partial a_e^{\text{OUT}}} \cdot \frac{\partial a_e^{\text{OUT}}}{\partial z_e^{\text{OUT}}} \cdot \frac{\partial z_e^{\text{OUT}}}{\partial a_k^{\text{H}}} \cdot \frac{\partial a_k^{\text{H}}}{\partial z_k^{\text{H}}} \cdot \frac{\partial z_k^{\text{H}}}{\partial w_{f,k}}

$$
* **errore sullo strato di output**:  si ottiene guardando solo i primi due termini 
$$
\frac{\partial \mathcal{J}}{\partial a_e^{\text{OUT}}} \cdot \frac{\partial a_e^{\text{OUT}}}{\partial z_e^{\text{OUT}}} = (a_e^{\text{OUT}} - y_e) \overset{\mathrm{def}}{=} \delta_e^{\text{OUT}}
$$$$
\frac{\partial \mathcal{J}}{\partial w^{\text{H}}_{f,k}} = \sum_{e=1}^t \delta_e^{\text{OUT}} \cdot w_{k,e}^{\text{OUT}} \cdot a_k^{\text{H}} (1 - a_k^{\text{H}}) \cdot x_f

$$
## Notazione compatta
Definiamo l'*errore sullo strato nascosto*:
$$

\delta_k^{\text{H}} = a_k^{\text{H}} (1 - a_k^{\text{H}}) \sum_{e=1}^t w_{k,e}^{\text{OUT}} \delta_e^{\text{OUT}.} \quad\quad\quad (1)

$$
da cui:
$$

\frac{\partial \mathcal{J}(W^{\text{H}},W^{\text{OUT}}; \mathbf{x}, \mathbf{y} )}{\partial w^{H}_{f,k}} = \delta_k^{\text{H}} \cdot x_f \quad\quad\quad (2)

$$
## Notazione Vettoriale
Sia:
* $X \in \mathbb R^{n\times d}$ la matrice degli $n$ campioni
* $Y \in \{ 0,1 \}^{n \times t}$ la matrice che raccoglie tutte le echitette in formate one hot.

Per aggiornare $w_{f,k}^H$ faccio cosi:
* assegno un valore casuale **vicino a 0**
* per ogni campione $x$, ossia ogni riga $c$, di $X$:
$$

w_{f,k}^{\text{H}} \leftarrow w_{f,k}^{\text{H}} - \eta \cdot \delta^{\text{H}}_{c,k} \cdot X_{c,f}

$$
ovvero: invece che fare un aggiornamento iterativo, ne faccio un cumulativo per ogni campione.
$$
w_{f,k}^{\text{H}} =w_{f,k}^{\text{H}} - \eta \sum_{c = 1}^{n} \delta^{\text{H}}_{c,k} \cdot X_{c,f} \quad\quad\quad (3)
$$
* $\delta_{c,k}^H$ e' la componente $k$ dell'errore de layer nascosto, ottenuto a partire dal campione $c$.
* sia $A^H$ la matrice che ha per righe i vettori $a_{c}^H$ per $c=1,\dots,n$
* definiamo allora $A^\text{OUT}$
* di conseguenza:
$$
\delta^\text{OUT} = A^\text{OUT} - Y \in \mathbb R^{n \times t}
$$
* ogni riga $c$ in $\delta ^\text{OUT}$, rappresenta l'errore sul campione $c$


***addestramento con mini-batch*** ovvero si usano piccoli gruppi di dati (anziché tutto il dataset), rendendo l'apprendimento più veloce ed efficiente.

`batch_idx` è l'insieme degli indici dei campioni che fanno parte del mini-batch corrente.

| formula                                                           | codice python                                |
| ----------------------------------------------------------------- | -------------------------------------------- |
| $\delta^\text{OUT} = A^\text{OUT} - Y \in \mathbb{R}^{n\times t}$ | `delta_out = a_out - y_train_enc[batch_idx]` |

Ricordiamo che $W^\text{OUT} \in \mathbb{R}^{h\times t}$. Consideriamo il seguente prodotto
$$

\delta^\text{OUT} \cdot(W^\text{OUT})^T \in \mathbb{R}^{n\times h}

$$
La matrice risultante sulla riga $c$ e colonna $k$ contiene:
$$

\sum_{e=1}^t \delta_{c,e}^\text{OUT}w_{k,e}^\text{OUT}

$$
Se quest'ultima quantita viene moltiplicata per $A_{c,k}^\text{OUT}(1-A_{c,k}^\text{OUT})$ (ovvero per la componente $k$ del vettore $\mathbf{a}^\text{H}_c$) otteniamo
$$

\mathbf{a}^\text{H}_{c,k} (1-\mathbf{a}^\text{H}_{c,k})\sum_{e=1}^t \delta_{c,e}^\text{OUT}w_{k,e}^\text{OUT} = \delta^\text{H}_{c,k}

$$
Indicando con $\odot$ il prodotto componente per componente
$$

\delta^\text{H} = A^\text{H} \odot (1-A^\text{H}) \odot \delta^\text{OUT} \cdot(W^\text{OUT})^T \in \mathbb{R}^{n\times h}

$$

| formula                                                                                                                                         | codice python                                                      |
| ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| $\delta^\text{H} = A^\text{H} \odot (1 - A^\text{H}) \odot \left( \delta^\text{OUT} \cdot (W^\text{OUT})^T \right) \in \mathbb{R}^{n \times h}$ | `sigmoid_derivative_h = a_h * (1. - a_h)`                          |
|                                                                                                                                                 | `delta_h = np.dot(delta_out, self.w_out.T) * sigmoid_derivative_h` |

Infine consideriamo $X^T \delta^\text{H} \in \mathbb{R}^{d\times h}$. In posizione $f,k$ troviamo il prodotto scalare della colonna $f$ di $X$ per la colonna $k$ di $\delta^\text{H}$ ovvero
$$

\sum_{c=1}^{n} \delta_{c,k}^\text{H} X_{c,f}

$$
Per la (2) e la (3),

| formula                                                                  | codice python                                      | costo |
| ------------------------------------------------------------------------ | -------------------------------------------------- | ----- |
| $\frac{\partial \mathcal{J}}{\partial W^\text{H}} = X^T \delta^\text{H}$ | `grad_w_h = np.dot(X_train[batch_idx].T, delta_h)` |       |

quindi aggiorniamo $W^{H}$ nel seguente modo
$$

W^{H} \leftarrow W^{H} - \eta \frac{\partial \mathcal{J}}{\partial W^{H}}

$$
* **tasso apprendimento**: $\eta$

### Derivata $\frac{\partial \mathcal{J}}{\partial w^\text{OUT}_{k,e}}$
**Per la regola della catena**:
$$

\frac{\partial \mathcal{J}}{\partial w_{k,e}^\text{OUT}} = \frac{\partial \mathcal{J}}{\partial a_e^\text{OUT}} \frac{\partial a_e^\text{OUT}}{\partial z_e^\text{OUT}} \frac{\partial z_e^\text{OUT}}{\partial w_{k,e}^\text{OUT}}

$$
- $\frac{\partial \mathcal{J}}{\partial a_e^\text{OUT}} = \frac{a_e^{\text{OUT}} - y_e}{a_e^{\text{OUT}} (1 - a_e^{\text{OUT}})}$

- $\frac{\partial a_e^\text{OUT}}{\partial z_e^\text{OUT}} = a_e^{\text{OUT}} (1 - a_e^{\text{OUT}})$

- $\frac{\partial z_e^\text{OUT}}{\partial w_{k,e}^\text{OUT}} = \frac{\partial}{\partial w_{k,e}^\text{OUT}} \sum_{j=1}^{h} w_{j,e}^\text{OUT} a_j^\text{H} + w_{0,e}^\text{OUT} = a_k^\text{H}$

**quindi**:
$$

\frac{\partial \mathcal{J}}{\partial w^\text{OUT}_{k,e}} = (a_e^{\text{OUT}} - y_e) a^\text{H}_k = \delta_e^{\text{OUT}} \cdot a^\text{H}_k

$$
#### Notazione vettoriale
**La matrice**:
$$

\left(A^\text{H}\right)^T \cdot \delta^\text{OUT} \in \mathbb{R}^{h\times t}

$$
che in posizione $k, e$ contiene:
$$

\sum_{c = 1}^n \delta_{c,e}^{\text{OUT}} \cdot a^\text{H}_{c,k}

$$
ovvero, come detto anche sopra, la somma dei contributi all'aggiornamento del gradiente di ogni campione. Riassumendo

| formula                                                                                                  | codice python                           | costo     |
| -------------------------------------------------------------------------------------------------------- | --------------------------------------- | --------- |
| $\frac{\partial \mathcal{J}}{\partial W^\text{OUT}} = \left(A^\text{H}\right)^T \cdot \delta^\text{OUT}$ | `grad_w_out = np.dot(a_h.T, delta_out)` | $O(n hd)$ |

## Complesità
1. **Costo per il gradiente di Output ($\frac{\partial \mathcal{J}}{\partial W^{\text{OUT}}}$)**. Nel passaggio finale, dobbiamo calcolare l'aggiornamento per i pesi finali moltiplicando le attivazioni del layer nascosto ($A^{\text{H}}$) per l'errore calcolato sull'output $\delta^{\text{OUT}}$.La formula matriciale è: $(A^{\text{H}})^T \cdot \delta^{\text{OUT}}$ La matrice trasposta $(A^{\text{H}})^T$ ha dimensioni $(h \times n)$.La matrice dell'errore $\delta^{\text{OUT}}$ ha dimensioni $(n \times t)$.Costo della moltiplicazione: $(h \times n) \times (n \times t) \rightarrow \mathbf{O(n \cdot h \cdot t)}$
2. **Costo per propagare l'errore all'indietro ($\delta^{\text{H}}$)** Per trovare l'errore da assegnare allo strato nascosto, dobbiamo prendere l'errore di output e "rimandarlo indietro" moltiplicandolo per i pesi attuali.L'operazione dominante qui è: $\delta^{\text{OUT}} \cdot (W^{\text{OUT}})^T$ La matrice dell'errore $\delta^{\text{OUT}}$ ha dimensioni $(n \times t)$ .La matrice dei pesi trasposta $(W^{\text{OUT}})^T$ ha dimensioni $(t \times h)$ .Costo della moltiplicazione: $(n \times t) \times (t \times h) \rightarrow \mathbf{O(n \cdot h \cdot t)}$ (Le operazioni element-wise con la derivata della sigmoide costano solo $O(n \cdot h)$, quindi sono trascurabili).
3. **Costo per il gradiente Nascosto ($\frac{\partial \mathcal{J}}{\partial W^{\text{H}}}$)** Infine, calcoliamo l'aggiornamento per i pesi iniziali moltiplicando gli input ($X$) per l'errore dello strato nascosto ($\delta^{\text{H}}$).La formula matriciale è: $X^T \cdot \delta^{\text{H}}$ La matrice degli input trasposta $X^T$ ha dimensioni $(d \times n)$.La matrice dell'errore nascosto $\delta^{\text{H}}$ ha dimensioni $(n \times h)$.Costo della moltiplicazione: $(d \times n) \times (n \times h) \rightarrow \mathbf{O(n \cdot h \cdot d)}$
4. **costo complessivo**. $\mathbf{O(n \cdot h \cdot (t + d))}$