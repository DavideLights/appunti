## Numpy
**homogeneus multidimensional array**: e' l'array di numpy. Una tavola di elementi, tutti dello stesso tipo indicizzati da una tupla di numeri non-negativi.

**ndarray**: e' il nome della classe.

**axes**: sono le dimensioni dell'array num py. **L'array d'esempio ha 1 asse.**
```pyhton
[[1,0,0],
 [0,1,2]]
```

**variabili di ndarray**:
* `ndarray.shape`: dimensioni dell'array. Se l'array e' una matrice $n\times m$, allora `shape` ritorna `(n,m)`.
* `ndarray.size`: numero di elementi nell'array, ossia il prodotto degli interi in `shape`.
* `ndarray.data`: contiene i dati dell'array, ma non andrebbe usato. si accede ai dati indicizzandoli.

**creare un'array**: `np.array([2,3,4])`

**indexing**:
* **slicing**: `a[2:5]`
* **step**: `a[:6:2]`, ossia dall'inizio fino alla posizione 6, prendi ogni 2 elementi.
* **reverse**: `a[::-1]`
* **last row**: $b[-1]$
* **dots**: `x[1,2,...]` e' equivalente a `x[1,2,:,:,:]` dove $x$ array con **5 assi**.
	* `x[...,3]` equivale a `x[:,:,:,:,3]`

**esempi**:
* `points[3:6,1]`: dalla riga 3 alla 6, prendi l'elemento 1.
* `points[:,1]`: in tutte le righe prendi l'elemento 1.
* **attenzione** `a[[1,6,4]]`: prende da `a` le righe 1,6 e 4.

**fromfunction**: `np.fromfunction(f, (5,4), dtype=np.int_)` con `def f(x,y): ...` crea un'array passando in input $x\in[1,5]$ ed $y \in [1,4]$


