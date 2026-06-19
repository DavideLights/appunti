### **Regressione Lineare**

- **Modello**: $y = w_0 + \sum_{i=1}^{d} w_i x_i = w \cdot x$
- **Standardizzazione feature**: $x_i^{\texttt{std}} = \frac{x_i - \mu_i}{\sigma_i}$
- **Errore Quadratico Medio (Cost Function $J$)**: $$J(w) = \frac{1}{2}\sum_{i=1}^n \left( y^{(i)} - w\cdot x^{(i)} \right)^2$$
- **Gradiente**: $\nabla J(w) = - X^T\times \texttt{errors}$ dove l'errore è $y^{(i)}-w\cdot x^{(i)}$
$$
w_{j} = w_{j} - \left( -w_{j}\sum_{i=1}^n(y^{(i)}-wx^{(i)}) \right)
$$
- **Discesa del Gradiente (Aggiornamento Pesi)**: $w \leftarrow w -\eta \nabla J(w)$
- **Errore Medio Assoluto (MAE)**: $\frac{1}{n}\sum_{i=1}^{n} |y_i - z_i|$
- **discesa gradiente a mini batch**: *e' la via di mezzo tra SGD e batch gradient descent*
$$
w_{j} \gets w_{j}+ \frac{1}{|X_{b}|} \sum_{i\in X_{b}} w_{j} \left( y^{(i)} - w\cdot x^{(i)} \right)
$$
### **Alberi di Decisione**
- **Indice di Gini (Impurità)**: $$I_G(D_p) = 1-\sum_{c}\left(\frac{n_c}{n} \right)^2$$
- **massimo con due classi** $(c=2)$: $1-\sum_{i=1}^c 0.5^2 = 0.5$, ossia quando le due classi sono **perfettamente mischiate**.
* $D_p$: insieme di esempi relativi al nodo $p$.
* $n = |D_p|$
* $n_c = \text{numero di esempi in } D_p \text{ appartenenti alla classe } c$.
* $n_c/n$: probabilita di assegnare un esempio alla classe $c$
* $n_c \to 0$: allora $I_G \to 0$
* se $I_G(D_p) =0$: se ho solo due classi ,vuol dire che una delle due prevale sull'altra

- **Entropia (Impurità)**: $$I_H(D_p) = - \sum_{c} \frac{n_c}{n}\log_2 \frac{n_c}{n}$$
- **Guadagno Informativo ($IG$)**: $$IG(D_p) = I_G(D_p) - \left( \frac{|D_L|}{n} I_G(D_L) + \frac{n-|D_L|}{n} I_G(D_R) \right)$$
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
### **Perceptron**
- **Funzione Attivazione**: $\phi(w\cdot x) = +1$ se $w\cdot x \geq 0$, altrimenti $-1$
- **Regola di Aggiornamento Pesi (solo in caso di errore)**: $$w = w+ \eta y^{(i)} x^{(i)} \text{(nota: voglio spostare w verso x)}$$
- **Distanza Punto-Iperpiano**: $d = \frac{w\cdot p + w_0}{|w|}$
$$
\gamma = \min y^{(i)} \frac{w^* x^{(i)}}{\|w^*\|} = \text{distanza minima tra miglior piano sep e campione}
$$
$$
U \geq \max \|x^{(i)}\|
$$
$$
k = \text{numero iterazioni} = \frac{U^2}{\gamma^2}
$$

### **Adaline e Regressione Logistica**

- **Adaline - Aggiornamento pesi**: $w_j \leftarrow w_j + \eta \sum_{i=1}^{n} (y^{(i)} - w\cdot x^{(i)}) x_j^{(i)}$
- **Funzione Sigmoide**: $\phi(z) = \frac{1}{1+e^{-z}}$
- **Regressione Logistica - Cost Function (Log Loss)**: $J(w) = -\sum_{i=1}^{n}\left( y^{(i)}\log\left(\phi(w\cdot x^{(i)})\right) + (1-y^{(i)})\log\left( 1-\phi(w\cdot x^{(i)})\right) \right)$
- **Regressione Logistica - Aggiornamento Pesi**: $w_j \leftarrow w_j +\eta \sum_{i=1}^{n} x_j^{(i)} \left( y^{(i)} - \phi(w\cdot x^{(i)}) \right)$

### **Reti Neurali (Backpropagation)**

- **Forward Pass - Strato Nascosto**: $z_k^{\text{H}} = \sum_{f=1}^d w_{k,f}^{\text{H}} x_f + b_k^{\text{H}}$, $a_k^{\text{H}} = \sigma(z_k^{\text{H}})$
- **Errore Strato Output ($\delta^{\text{OUT}}$)**: $\delta_e^{\text{OUT}} = a_e^{\text{OUT}} - y_e$
- **Errore Strato Nascosto ($\delta^{\text{H}}$)**: $\delta_k^{\text{H}} = a_k^{\text{H}} (1 - a_k^{\text{H}}) \sum_{e=1}^t w_{k,e}^{\text{OUT}} \delta_e^{\text{OUT}}$
- **Derivata Sigmoide**: $a(1-a)$ (es. $\frac{\partial a_e^{\text{OUT}}}{\partial z_e^{\text{OUT}}} = a_e^{\text{OUT}} (1 - a_e^{\text{OUT}})$)
- _Forma vettoriale_: $\mathbf{z}^{\text{H}} = \mathbf{x} W^{\text{H}} + \mathbf{b}^{\text{H}}$.
- _Forma vettoriale_: $\mathbf{z}^{\text{OUT}} = \mathbf{a}^{\text{H}} W^{\text{OUT}} + \mathbf{b}^{\text{OUT}}$.
- **Output di Predizione**: $\text{argmax}_{e=1}^t { a_e^{\text{OUT}}}$.
- **Funzione di Costo (Log Loss Generalizzata)**: $\mathcal{J} = - \sum_{e=1}^t \left[ y_e \log a_e^{\text{OUT}} + (1 - y_e) \log (1 - a_e^{\text{OUT}}) \right]$.

### **Retro-Propagazione (Backpropagation)**

- **Errore Strato Output ($\delta^{\text{OUT}}$)**: $\delta_e^{\text{OUT}} = a_e^{\text{OUT}} - y_e$.
    - _Forma matriciale_: $\delta^\text{OUT} = A^\text{OUT} - Y$.
- **Errore Strato Nascosto ($\delta^{\text{H}}$)**: $\delta_k^{\text{H}} = a_k^{\text{H}} (1 - a_k^{\text{H}}) \sum_{e=1}^t w_{k,e}^{\text{OUT}} \delta_e^{\text{OUT}}$.
    - _Forma matriciale_: $\delta^\text{H} = A^\text{H} \odot (1-A^\text{H}) \odot \left(\delta^\text{OUT} \cdot(W^\text{OUT})^T\right)$.
- **Calcolo dei Gradienti (Derivate dei Pesi)**:
    - _Pesi Output_: $\frac{\partial \mathcal{J}}{\partial w^\text{OUT}_{k,e}} = \delta_e^{\text{OUT}} \cdot a^\text{H}_k$. Matriciale: $\frac{\partial \mathcal{J}}{\partial W^\text{OUT}} = \left(A^\text{H}\right)^T \cdot \delta^\text{OUT}$.
    - _Pesi Nascosti_: $\frac{\partial \mathcal{J}}{\partial w^{H}_{f,k}} = \delta_k^{\text{H}} \cdot x_f$. Matriciale: $\frac{\partial \mathcal{J}}{\partial W^\text{H}} = X^T \delta^\text{H}$.
- **Aggiornamento dei Pesi (Discesa del Gradiente)**: $W \leftarrow W - \eta \frac{\partial \mathcal{J}}{\partial W}$.

### **Costo Computazionale (Complessità)**

- **Forward Pass (singolo campione)**: $O(h \cdot d + t \cdot h)$.
- **Addestramento (singola epoca su $n$ campioni)**: $O(n\cdot h \cdot (t+d))$. Includendo il metodo di forza bruta senza backpropagation il calcolo della derivata scalerebbe malissimo a $O(n(hd+ht)^2)$.

### **Macchine a Vettori di Supporto (SVM)**

- **Distanza tra i Margini**: $d = \frac{2}{|w|}$
- **cerniera, hinge loss, SVM**:
$$
\xi^{(i)} : \begin{cases}
wx^{(i)}+w_{0} \geq 1 - \xi^{(i)} \text{ se } y^{(i)} =1 \\
wx^{(i)}+w_{0} < -1 + \xi^{(i)} \text{ se } y^{(i)} =-1
\end{cases}
$$
$$
\xi^{(i)} = \max(0, 1-y^{(i)}(wx^{(i)}+w_{0}))
$$

- **Funzione Obiettivo (Hinge Loss + Margine)**: $J(w) = \frac{1}{2}|w|^2 + C\sum_{i=1}^{n} \max\left(0, 1 - y^{(i)}(w\cdot x^{(i)} + w_0) \right)$
- **aggiornamento**: $$
w_{j} \gets \begin{cases}
w_{j} - \eta w_{j} \text{ se classifico correttamente } \\ \\
w_{j} - \eta(w_{j} - Cy^{(i)}x^{(i)})
\end{cases}
$$
- **Pesi classi sbilanciate**: $v_c = \frac{n}{2n_c}$ e $C_i = C \cdot v_i$
- **Kernel Trick (Gaussiano RBF)**: $K(x_1, x_2) = e^{\left(-\gamma |x_1 - x_2|^2\right)}$

### **Valutazione e Dati Sbilanciati**

- **F1-Score**: $F1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$
- **TPR (True Positive Rate/Recall)**: $TPR = \frac{TP}{TP+FN}$
- **FPR (False Positive Rate)**: $FPR = \frac{FP}{FP+TN}$

### **PCA (Riduzione Dimensionalità)**

- **Centratura Dati**: $x_{i,j}^{\text{(centrato)}} = x_{i,j} - \mu_j$
- **Matrice di Covarianza ($X$ centrata)**: $C = \frac{1}{n-1}X^T X$
- **Varianza di proiezione sull'autovettore $v$**: $\mathrm{Var}(X\cdot v) = v^T C v$
- **Equazione Autovalori**: $C w = \lambda w$ da cui la varianza massima è $\lambda$ (autovalore)