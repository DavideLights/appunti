
**cos'e'**? *tecnica di riduzione della dimensionalità delle caratteristiche*.
* **come**? proietta il dataset su uno spazio a dimensionalita inferiore con variabili non correlate tra loro e dimensioni informative.
* **cosa sto cercando**?  *gli assi perpendicolari alla direzione in cui c'e' massima varianza tra i campioni*
* le feature sono vettori ortogonali tra loro

**come si fa?**
* **centra la matrice**: $x_{i,j}- \mu_{j}$
* **matrice di covarianza**: $C = \frac{1}{n-1}X^T X \in R^{d \times d}$
* **autovalori e autovettori**: gli autovettori sono sono le direzioni principali mentre gli autovalori indicano quanta varianza hanno ciascuna
* **massimizzare**: selezionare gli autovettori che massimizzano l'autovalore.

**perche solo sul training set**?
* l'obiettivo del PCA e' ridurre la dimensionalita per l'allenamento
* **non si applica sul test set perche'**: altrimenti **inquino con media e varianza globali i valori del test set**, ed il modello risultera stranamente molto performante.

**matrice di covarianza**:
* sulla diagonale: $\text{var(x\_i)}$
* sul resto le covarianze: $\text{cov(xj,xi)}$

la **coviarianza**: $cov(x_{1},x_{2})$
* se vale 0: allora $x_{1},x_{2}$ non sono correlati tra loro
* se vale > 0: allora al crescere di $x_{1}$, l'altro diminuisce
* viceversa se vale $<0$

**che cos'e' l'autovalore**? e' la varianza lungo la direzione dell'autovettore

**massimizzare la varianza**: voglio ottenere una base di autovettori che massimizzano gli autovalori.

**cosa garantisce questa matrice**? grazie al teorema spettrale
* no ridondanza sulle features, quindi 2 o piu feature non rappresentano lo stesso dato
* fornendo in input 

## matrice simmetrica
**proiezione di $X$ su $v$:** $X \cdot v$

**voglio trovare**: $v$ che massimizza $Var(X\cdot v) = v^T C v$
* con $\|v\|=1$


proiettare la matrice: $Xv$
* $var(Xv) = v^T Cv$

