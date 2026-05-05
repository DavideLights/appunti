
* `generic-ec` crate per le curve ellittiche
* ottimizza senza oscurare lo schema originale dello pseudocodice
* non devo usare metodi o funzioni panicking
* devo scrivere dei test
* deve passare: `cargo clippy` e `cargo fmt`
* niente funzioni platform specific

![[Pasted image 20260423231620.png]]

* $\mathbb E$ e' una curva ellittica di ordine $q$, con generatore $G$. 
* $\text{encode}(X)$ e' la rappresentazione di $X$ in byte in forma compressa.
* $\mathbb B$ e' un byte, ossia un ottetto binario. $\mathbb B^*$ e' una stringa di ottetti di lunghezza arbitraria.
* $A || B$ concatena due byte
* $H$ e' `sha2-256`