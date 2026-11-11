**book**: introduction to cryptography

**owf**: $f: \{ 0,1 \}^* \to \{ 0,1 \}^*$ easy to compute and hard to invert.
* $f$ computable in polynomial time 

$$
f_{ss}(x_{1},\dots,x_{n},J) = \left(x_{1},\dots,x_{n}, \left[ \sum_{j \in J}x_{j} \text{ mod } 2^n \right]\right)
$$

**leak**: it is possible for an owf to leak informations about $x$.
* let $g$ be owf
* $f(x_{1},x_{2})=(x_{1},g(x_{2}))$
* $f$ leaks half of the input but is owf

*hardcore predicate*: is $hc$ or $h : \{ 0,1 \}^* \to \{ 0,1 \}$ in relation to a function $f$ that is hard do compute.
* we want $Pr$ better than $\frac{1}{2}$, since its only a bit and we can guess it with pr $\frac{1}{2}$
* **what it represents**: $hc$ is a *specific piece of information about $x$ that is "hidden" by $f(x)$*

**def. 7.4**: A function $hc: \{ 0,1 \}^*  \to \{ 0,1 \}$ is a hard-core predicate of a function $f$ if $hc$ can be computed in polynomial time, and for every PPT algorithm $\mathcal A$, there is a negligible function $\text{negl}$ s.t.

$$
\text{Pr}_{x\gets \{ 0,1 \}^n}\left[\mathcal A(1^n, f(x))=hc(x)\right] \leq \frac{1}{2} + \text{negl}(n)
$$

> **note**: $\text{Pr}$ is taken over $x$ choosen uniformly in $\{ 0,1 \}^n$ and the randomness of $\mathcal A$

**example of hc**. consider $hc(x) = \bigoplus_{i=1}^n x_{i}$ where $x_{1},\dots,x_{n}$ are the bits of $x$.
* one could expect it is a predicate for any owf
	* since $f$ is owf, some bit of the input is hidden
	* so it should be hard to compute all the bits of $x$!
* so take for example $f(x) = (g(x), \bigoplus_{i=1}^n x_{i})$  with $g(x)$ owf
	* $f(x)$ does not hide the value of $hc(x) = \bigoplus_{i=1}^n x_{i}$
	* **what does this mean?** Even though $f$ is still a OWF (inverting $f$ requires inverting $g$), $hc(x)$ is **explicitly leaked** as the second component of $f(x)$, so $\mathcal{A}$ can read it with probability $1 \implies hc$ is **not** a hard-core predicate for $f$ (no fixed predicate can be hard-core for *all* OWFs). #gemini
