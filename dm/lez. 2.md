* **NumPy**: gestione di array e calcoli numerici
* **Matplotlib**: librerie per la creazione di grafici e disegno di forme.

## KNN
**che cos'e'?** un'algoritmo che impara in modo supervisionato.
* **classifica**: in base al tag piu frequente nei k oggetti piu vicini
* **fitting**: `fit` implementa l'apprendimento, consiste nella *memorizzazione dei dati*.
* **predict**: `predict` guarda i $k$ piu vicini, con *distanza euclidea* per assegnare il tag.
* **efficienza**: selection sort (*ad ogni iterazione identifica il piu piccolo*), oppure albero binario per la ricerca dei $k$ piu vicini.
* **moda**: l'elemento piu frequente in una lista.

**vantaggio**: man mano che colleziono dati e li aggiungo, il classificatore si adatta subito ai nuovi dati di training.

**svantaggio**: il costo computazionale cresce linearmente nel dataset a meno che
* **feature**: sono poche
* **implementazione**: inefficiente, a meno che non uso k-d tree.
* **storage**: non posso scartare nessun elemento del dataset.

**standardizzare**: bisogna standardizzare, in modo che ogni feature contribuisca allo stesso modo.

**curse of dimensionality**: se lo spazio delle features e' molto sparso, allora la distanza tra i punti perde di significato. bisogna selezionare le features oppure ridurre le dimensioni.
## numpy e pandas
* `np.array()`: definisce array e matrici per essere usati da numpy.
* `np.arange`: genera un intervallo di numeri per numpy.
* Sia `y=[...]` una lista numpy e `t in y`. Allora `y == t` e' la lista dove un `true` in i-esima posizione indica la presenza di t in y in posizione i-esima.
* Sia `y=[a,b,a,c]` e `t=a`, allora `np.where(y==t)` ritorna gli indici in cui si trova `t`
* `np.unique` ritorna l'array senza duplicati e con `return_counts=True`, ritorna il numero di occorrenze per ogni oggetto. Utile per identificare il massimo.
* `np.concatenate`: concatena le liste
* `np.setdiff1d`: differenza tra liste (come insiemi???)
* `df.iloc`: `iloc` contiene i valori del data frame a cui posso accedere con posizioni integer based.
## modellazione
* suddivisione data set in `X_train` , `y_train` ed `X_test` ed `y_test`.



