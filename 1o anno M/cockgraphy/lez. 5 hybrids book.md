**book**: Introduction to Modern Cryptography 7.4.2

**theorem 7.20**: if there exists a pseudorandom generator $G$ with expansion factor $n+1$ (from $n$ to $n+1$), then 
* for any polynomial $\text{poly}$ 
* there exists a pseudorandom generator $\hat{G}$ 
* with expansion factor $\text{poly}(n)$

**proof**: consider constructing a pseudorandom generator $\hat G$ that outputs $n+2$ bits. Lets describe how $\hat{G}$ works:
1. **step 1:**
	1. given $s \in \{ 0,1 \}^n$
	2. compute $t_{1} := G(s)$
	3. we obtained $n+1$ bits (because $G$ has an expansion factor of $n+1$)
2. **step 2**:
	1. the initial $n$ bits of $t_{1}$ are used **again** as seed for $G$
	2. concatenate the resulting $n+1$ bits with the final bit of $t_{1}$
3. **step 3**: return the $(n+2)\text{-bit}$ string

![[Pasted image 20261107150640.png]]


**now we have to prove that its secure**:
* define three sequences of distributions $\{ H_{n}^0 \}_{n=1,\dots}$, $\{ H_{n}^1 \}_{n=1,\dots}$, and $\{ H_{n}^2 \}_{n=1,\dots}$
* each is a distribution on strings of length $n+2$ (because $\hat{G}: \{0,1\}^n \to \{0,1\}^{n+2}$ stretches by $2$ bits, so $H_n^0 \equiv \hat{G}(U_n)$, $H_n^2 \equiv U_{n+2}$, and every intermediate hybrid $H_n^1$ bridging them must be defined over the same output space $\{0,1\}^{n+2}$) #gemini
* in distribution $H_{n}^0$ 
	* we choose (**input**) a uniform string $t_{0}\in \{ 0,1 \}^n$
	* the **output** for distribution $H_{n}^0$ is $t_{2}=\hat{G}(t_{0})$
* in distribution $H_{n}^1$ 
	* choose uniform string $t_{1} \in \{ 0,1 \}^{n+1}$
	* parse it as $s_{1}|| \sigma_{1}$
		* $s_{1}$: the initial $n$ bits
		* $\sigma_{1}$ the last bit
	* the output for $H^1_{n}$ is $t_{2}=G(s_{1})|| \sigma_{1}$
* in distribution $H^2_{n}$
	* the output is a uniform string $t_{2} \in \{ 0,1 \}^{n+2}$
	* $t_{2}\gets H_{n}^2$ describes the process above for $H^1_{n}$, this time generating $n+2$ uniform bits

**hybrid argument**: tool for proving indistinguishability when a primitive is applied multiple times.
* we define a series of intermediate "hybrid distributions"
* those distributions act as a bridge between "extreme distributions"
* the main condition to follow is that there is a polynomial number of hybrids when applying the hybrid argument