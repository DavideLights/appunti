# geometria
**autovalore**: se $Sv = \lambda v$, vuol dire che appliccare $S$ a $v$ non ne cambia la direzione.
* $\lambda$ e' autovalore di $v$ autovettore
* **LSI**: valori di $\lambda$ grandi tali che ho autovalori sono importanti da tenere a mente.

**riscrivere autovettore**: posso riscrivere un autovettore utilizzando come coefficienti i sui autovalori

**matrici simmetriche**: $S = S^T$, ossia i numeri sono disposti in modo che se traspongo righe e colonne allora la matrice non cambia.

**ortogonalita**: $v_{1} \cdot v_{2}=0$, ossia sono indipendenti e non sovrapposti.

**matrice positiva semidefinita**: $\lambda \geq 0$
* $AA^T$ ed $A^TA$ sono positive semidefinite

**decomporre** $S$ **quadrata con abbastanza autovettori indipendenti**:
$$
S = U \Lambda U^{-1}
$$
* $U$: autovettori come colonne
* $\Lambda$: autovalori sulla diagonale, ogni componente di $U$ viene mescolata separatamente, senza mescolarsi con le altre componenti.

**decomporre** $S$ **simmetrica**:
$$
S = Q \Lambda Q^T
$$
* $Q^T=Q^{-1}$

**normalizzare** $v$:
$$
\lvert v \rvert =\sqrt{ v^2_{1} + v^2_{2} + \dots + v^2_{n} } 
$$

## LSI
**Decomposizione in autovalori**: $S = U \Lambda U^{-1}$
* $S \in \mathbb R^{m\times m}$
* $m$ autovettori linearmente indipendenti
* $U$: matrice degli autovettori di $S$
* $\Lambda$: matrice degli autovalori in diagonale di $S$
* $U^{-1}$ e' tale che: $UU^{-1}=1$
**Dividi e moltiplica per $\sqrt{ 2 }$:**
* dividi $U$ per $\sqrt{ 2 }$
* moltiplica $U^{-1}$ per $\sqrt{ 2 }$
* Allora l'inversa di $U$ coincide con $U^{-1}$

**Come si calcola $U^{-1}$?** Inverti $U$ e dividi tutto per due

**Decomposizione $S$ simmetrica**: $S = Q \Lambda Q^T$


**SVD**: **Singular Value Decomposition** $A = U \Sigma V^T$
* $U: m \times m$, autovettori di $AA^T$
	* vettori latenti associati ai termini
* $\Sigma: m \times n$, per la diagonale ho $\sigma_{i} = \sqrt{ \lambda_{i} }$
	* **valori singolari**: indicano quanta informazione cattura ciascuna dimensione latente 
* $V: n \times n$, autovettori di $A^TA$
	* vettori latenti associati ai documenti

**quantità di informazione catturata dalle prime $k$ dimensioni latenti**
$$

\frac{\sum_{i=1}^{k}\sigma_i^2}{\sum_i \sigma_i^2}

$$


**Low-Rank Approximation**: $A_{k}$ e' $X$ di rango $k$ che minimizza $|A-X|_{F}$ (norma di frobenius). Voglio trovare la SV
* $A_{k} = U diag(\sigma_{1},\dots ,\sigma_{k}, 0, \dots, 0)V^T$
* $100 < k < 300$
* **cosa fa**? Comprimo la matrice originale in modo da mantenere solo i $k$ valori singolari piu grandi e che contengono piu informazione.
* **k piccolo**: perdita di dettagli, ma catturiamo la struttura semantica principale
* **k grande**: la matrice $A_{k} \approx A$, e scende l'errore di ricostruzione

**Esempio**: $A_{2}$ rispetto ad $A$, al posto degli 0 ha dei valori leggermente positivi o negativi. LSI ha ricostruito relazioni indirette

**Convenzione per rappresentare termini e documenti**:
* $T_{k} = U_{k} \Sigma_{k}^{1/2}$ per ottenere le coordinate dei termini nello spazio latente
* $D_{k} = \Sigma_{k}^{1/2}V_{k}^T$ per ottenere le coordinate dei documenti nello spazio latente

**convenzione per Proiettare la query**:
$$
q_{k} = q^T U_{k}\Sigma_{k}^{-1}
$$
* $U_{k}$ contiene le direzioni latenti principali nello spazio dei termini
* $q^T U_{k}$: esprimo $q$ in base alle direzioni latenti, nello spazio dei termini
* ora posso fare cosine similarity tra query e documento nello spazio latente.

**Rappresentazione simmetrica**: la abbiamo quando facciamo il quadrato, ossia $\Sigma_{k}^{1/2}$.
$$
A_{k}(t,d) \approx <T_{k}(t), D_{k}(d)>
$$

**Dimensioni latenti**: posso rappresentare termini e documenti all'interno dello spazio latente come se fossero fossero la stessa cosa.


**Polisemia**: parole che hanno molti significati
**Sinonimi**: parole che hanno lo stesso significato

**Che cosa abbiamo fatto**? se tengo solo $k$ autovalori in $\Sigma$ ed azzero il resto, allora ho ottenuto la decomposizione in  $A_{k}$ che fa molte cose interessanti.
* mappare documenti e termini verso uno spazio a bassa dimensionalità
* le dimensioni riflettono associazioni semantiche.
* riduzione del rumore.

**Recall**: aumenta, catturo meglio i significati delle parole
**Precision**: invariata, o peggiora. Posso attribuire falsi significati alle parole se $k$ non ottimo.