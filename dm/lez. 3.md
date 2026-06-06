* `np.unique(y_train, return_counts=True)` ritorna una lista dove ogni termine compare una ed una sola volta. `return_counts=True` ritorna anche per ogni item l'occorrenza

## k-d tree
**albero binario**.
**nodo**: fa riferimento ad una dimensione di un particolare  punto su `d` dimensioni.
**dimensione**: ad ogni livello dell'albero si alternano le dimensioni a cui i nodi fanno riferimento.

**esempio**: con `d=2`, ci troviamo per esempio nel piano cartesiano.
* **radice (ascisse)**: il nodo radice ha come dimensione quella delle ascisse e si riferisce al punto `a`
	* **sottoalbero sinistro**: nodi con ascisse minore.
	* **sottoalbero destro**: nodi con ascisse maggiore uguale.
* **livello successivo (ordinate)**: uso le ordinate come dimensione di riferimento per ordinare i sottoalberi, sul figlio sinistro usero il punto `b`, sul destro il punto `c`.
* **ecc...**
* fino alle **foglie!**


**costruzione**: costosa.
* **identificare il mediano**: ogni nodo dovrebbe essere il mediano del sottoinsieme che rappresenta, dunque devo ordinare i punti del sottoinsieme in $O(n \log n)$
* **partizionare** i punti in due sottoinsiemi per ogni nodo

**costo della costruzione**: l'altezza dell'albero e' bilanciata, ad ogni livello devo ordinare $n$ punti, dunque $O(n \log^2 n)$

**ricerca dei vicini**: si cercano in media in $O(k log n)$
* **parto**: dalla radice dell'albero vado al nodo di cui voglio cercare i vicini
* **backtracking**: proseguo la ricerca, oppure torno indietro. In media ci metto $\log(n)$ a cercare i vicini.

# Liste python e ndarray

| python           | numpy                                  | costo python | costo numpy             |
| ---------------- | -------------------------------------- | ------------ | ----------------------- |
| `append`         | `np.append`                            | `O(1)`       | `O(n)`: copia           |
| `pop`            | non supportato                         | `O(1)`       | --                      |
| concatenazione   | `np.concatenate`                       | `O(n+m)`     | `O(n+m)`                |
| ripetizione      | `np.tile`                              | `O(k*n)`     | `O(k*n)`                |
| **slicing**      | ritorna una vista sull'array originale | `O(k)`       | `O(1)` in **lettura**   |
| somma vettoriale | ...                                    | `O(n)`       | `O(n)` ma e' piu veloce |
| moltiplicazione  | ...                                    | `arr * 3`    | `O(n)`                  |
* **copia**: costa in numpy costa $O(n)$
* **slicing**: costa solo $O(1)$, ritorno una **vista** sull'originale.
* **somma e moltiplicazione vettoriale**: sono efficienti in numpy con tempo $O(n)$ molto efficiente.