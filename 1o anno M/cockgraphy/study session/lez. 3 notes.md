We want to prove that $h_{a,b}(m)=am+b \mod p$ with $p$ a large prime using $\lambda$ bits.

**fix**: $m,m',\tau,\tau'$. in terms of probability and linear algebra we want to state this problem: when $am+b=\tau$ and $am'+b=\tau'$?

$$
Pr\left[\left(\begin{matrix}
m & 1  \\
m' & 1
\end{matrix}\right) \left(\begin{matrix} a \\ b

\end{matrix}\right) = \left(\begin{matrix}
\tau \\ \tau'
\end{matrix}\right)\right]
$$

but fixed $m,m', \tau, \tau'$, with $a,b$ uniformly random then this has only one solution, so:
$$
= \frac{1}{p^2}
$$

> having $a,b$ large depends on having $p$ large.

Now that we found an hash family with this property, can we use it for MAC and say it is $\mathcal E$ stat. secure with $\mathcal E = \frac{1}{|\mathcal T|}$?

**thm**: every pairwise $\mathcal H$ is also a MAC with $\mathcal E=\frac{1}{|\mathcal T|}$.

$$
\mathcal H = \{ h_{k}: \mathcal M \to \mathcal T\}_{k\in \mathcal K}
$$

if $\mathcal H$ is pairwise independent, then it is uniform over $\mathcal T^2$.