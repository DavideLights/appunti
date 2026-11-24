**def. pseudorandomness**: $f$ is pseudorand iff it is indistinguishable from a random string, with **negligible probability**.

> [!note] $\{ X_{\lambda} \}_{\lambda \in \mathbb N}$
> It is family of probability distributions, indexed by $\lambda \in \mathbb N$.
> * **infinite**: its a infinite sequence of distributions.
> * $\{ G(U) \}$
> 

**computationally indistinguishable**: 
* $X = \{ X_{\lambda} \}_{\lambda \in \mathbb N}$
* $Y = \{ Y_{\lambda} \}_{\lambda \in \mathbb N}$
* Then $X \approx_{C} Y$ iff
* $|\Pr[\mathcal A(X) =1] - \Pr[\mathcal A(Y)=1]| \leq \text{negl}(\lambda)$

**it means**: two distributions are indistinguishable if $\forall \mathcal A$ we cannot distinguish them.

**game attack**: as shown, $\{ \text{GAME}(\lambda,0) \} \approx_{C} \{ \text{GAME}(\lambda,1) \}$. 


**pseudorandom generators**: 
* **GOAL**: extract and amplify recorded random sources.
* what 