
**obiettivo**: proiettare una matrice di campioni su uno spazio con molte feature, verso uno con poche feature. voglio massimizzare:
* la varianza dei dati, ossia feature ortogonali tra loro
* media pari a 0


1. centrare la matrice, sottraendo la media feature per feature
2. calcolare la matrice di covarianza: $C=\frac{1}{n-1}X^T X \in R^{d \times d}$


di questa matrice voglio trovare:
* $k$ autovettori che massimizzano l'autovalore in $C$
* li seleziono e creo la matrice $W \in R^{d \times k}$
* $X \times W \in R^{n\times k}$

**matrice di covarianza**:
* sulla diagonale: $\text{var}$
* sul resto le covarianze: $\text{cov}$

la **coviarianza**: $cov(x_{1},x_{2})$
* se vale 0: allora $x_{1},x_{2}$ non sono correlati tra loro
* se vale > 0: allora al crescere di $x_{1}$, l'altro diminuisce
* viceversa se vale $<0$

proiettare la matrice: $Xv$
* $var(Xv) = v^T Cv$

