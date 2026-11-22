
**example**: $h_{a,b}(m)=am+b \mod p$ with $p$ large prime number

**lemma**: $h_{a,b}$ is pairwise independent family.
* because $\Pr[h_{a,b}(m)=\tau \land h_{a,b}(m')=\tau']$ is satisfied only with a unique combination of $a,b$ over $\mathbb Z_{b}^2$
* so $\Pr = \frac{1}{p^2}$

**thm**: every pairwise independent $\mathcal H$ is a one time $\mathcal E$ stat with $\mathcal E=\frac{1}{|\mathcal T|}$

**proof thm**: 
$$
\Pr[h_{a,b}(m)=\tau | h_{a,b}(m')=\tau'] = \frac{\Pr[h_{a,b}(m)=\tau \land h_{a,b}(m')=\tau']}{\Pr[h_{a,b}(m')=\tau']} = \frac{1}{|\mathcal T|}
$$

**bad news** to have a $t$ times $2^{-\lambda}$ statistical resistance MAC, then you need a key long $(t+1) \lambda$ bits.

# randomness extraction

How to generate random numbers?
* we need a source of randomness $X$
* and a deterministic function that a machine can use to extract more randomness from $X$
* why? if $X$ is not random and we have $\text{Ext}$ deterministic extraction algorithm, then at the worst case it could be that $\Pr[X=c]=1=\Pr[\text{Ext}(X) = \text{Ext}(c)]$
* we need the source to be almost random at least.

How to measure the randomness?
* min entropy: $H_\infty(X) = -\log \max_{x} \Pr[X=x] =\min_{x} \log \frac{1}{\Pr[X=x]}$
* examples, $X=0^n$, so basically from $X$ you'll always extract 0
	* then: $H_{\infty}(X)=0$, its the worst case
* examples, $X$ uniformly random on $\{ 0,1 \}^n$
	* then: $H_{\infty}(X)=n=-\log 2^{-n}$ 

what does min entropy mean? we want to understand at the worst case how many bits are predictable.

why do we need entropy? for randomness extraction we want to bound $X$:
$$
H_{\infty}(X) \geq k \iff p_{max} \leq 2^{-k}
$$


**thm**: $\text{Ext}: \{ 0,1 \}^n \to \{ 0,1 \}$ does not exists, even if we bound with $k=n-1$, so that at the worst case, only one bit leaks information on $n$.
* so, even if $X$ has min entropy n-1 over $n$ bits

**proof for thm**: 
* assume exists $\text{Ext}: \{ 0,1 \}^n \to \{ 0,1 \}$
* take $b\in \{ 0,1 \}$ maximizing $|\text{Ext}^{-1}(b)|$
* then $|\text{Ext}^{-1}(b)| \geq 2^{n-1}$, its at least bigger than the half
* but then an adversary could choose $X_{\text{bad}}$ s.t its a uniform distribution over $\text{Ext}^{-1}(b)$
* and so $\text{Ext}^{-1}(X_{bad})$ gets always mapped to $b$ with Pr 1. But also $H_{\infty}(X_{bad}) = k-1$, contraddiction $\square$.

so an adversary can choose $\text{X}_{bad}$ so that we break you mom's ass hole.

**solution**: seeded extractor.
$$
\text{Ext}: \{ 0,1 \}^d \times \{ 0,1 \}^n \to \{ 0,1 \}^\ell
$$

**def**. $\text{Ext}$ is $(k, \mathcal E )$ seeded extractor iff
* $\forall X: H_{\infty}(X) \geq k$
* $(S,\text{Ext}(S,X)) \approx_{\mathcal E} (S, U_{\ell}) \equiv U_{\ell+d}$
* $\approx_{\mathcal E} \equiv SD(X,Y) \leq \mathcal E$
* where $s \gets S$ is completly know to the adversary, and we would like for $\approx_{\mathcal E}$ to still hold


**thm**: left-over hash lemma
* let $\mathcal H = \{ h_{s}: \{ 0,1 \}^n \to \{ 0,1 \}^\ell \}$
* let $\mathcal H$ be pairwised independent
* theb $\text{Ext}(s,x) = h_{s}(x)$ is a $(k,\mathcal E)$seeded extractor for

$$
k \geq \ell + 2\log \frac{1}{\mathcal E} -2
$$

to prove this we need to probe that:
* assume $Y$ over $\mathcal Y$
* assume $\text{Col}(Y) \leq \frac{1}{|\mathcal Y|}(1+4 \mathcal E^2)$
* then $\text{SD}(Y,U) \leq \frac{1}{\mathcal E}$