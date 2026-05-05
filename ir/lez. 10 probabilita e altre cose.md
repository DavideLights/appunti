![[Pasted image 20260428160447.png]]![[Pasted image 20260428160525.png]]![[Pasted image 20260428160537.png]]

**random var**: $d_{t_{j} = \text{numero di occorrenze di } t_{j} \text{ nel documento } d}$
![[Pasted image 20260428160632.png]]

**distribuzione binomiale**: $p(d_{t_{j}}=k)  = \binom{l}{k}p^{-k}{1-p}^{l-k}$

**poisson**: quando $l$ e' grande e $p$ e' piccolo, allora $\text{Binomial}(l,p) \sim \text{Poisson}(\lambda)$ con $\lambda = lp$
* e' dunque simile alla distribuzione binomiale, ma e' **piu semplice da trattare**.
![[Pasted image 20260428160914.png]]

* $x$ e' il numero di occorrenze di $t_{j}$ in $d$
* $\lambda$ e' il numero di occorrenze che **mi aspetto**.
![[Pasted image 20260428161040.png]]

**come usiamo poisson**? vogliamo comparare le curve che creano i differenti termini in base al loro parametro $\lambda_{t_{j}}$

![[Pasted image 20260428161151.png]]

![[Pasted image 20260428161235.png]]
![[Pasted image 20260428161325.png]]
**Dunque**: lo score di ogni termine contribuisce come $\log \frac{\rho_{j}}{\gamma_{j}}$.
**problema**: calcolare $\rho_{j}$.
* **con collezione di documenti giudicati**: allora posso stimare $\rho_{j}$
* **a priori come faccio**?
![[Pasted image 20260428161515.png]]

![[Pasted image 20260428161650.png]]

assumo che ci siano due tipi di termini in un doucumento (derivo  dall'immagine sopra):
* termini che non caratterizzano il topic del documento
* termini che descrivono il topic del documento.

**eliteness**: e' una hidden binary variable (ossia e' elite oppure non e' elite).
* **se un termine e' elite**: se il documento parla del concetto denotato dal termine.
* **occorrenza dei termini**: dipende dalla elitness, ma la eliteness dipende dalla rilevanza.
![[Pasted image 20260428162127.png]]
![[Pasted image 20260428162309.png]]
![[Pasted image 20260428162547.png]]
**vogliamo che il contributo sia non binario rispetto a BIM**: 


... altre cose