**problema con adaline**: cerca di minimizzare le distanze tra i punti e l'iperpiano.

**attenzione**: nelle formule e' sempre comodo separare da $wx$ il bias $w_{0}$

**obiettivo svm**: si vuole massimizzare la distanza tra l'iperpiano ed i margini.
* $H^+ : wx^+ = 1$, margine destro
* $H^-: wx^-1 = -1$, margine sinistro

**la funzione da massimizzare/minimizzare e':**
$$
\frac{2}{\|w\|} \equiv_{min} \frac{\|w\|}{2} 
$$

passaggi per ottenerla:
$$
\frac{wx^+}{\|w\|} - \frac{wx^-}{\|w\|} = \frac{1-w_{0}}{\|w\|} - \frac{-1-w_{0}}{\|w\|} = \frac{2}{\|w\|}
$$
* $wx^+ = 1-w_{0}$ ed $wx^- = -1 -w_{0}$

**vincoli**: vogliamo minimizzare la funzione ma mantenendo dei vincoli
$$
y^{(i)}(wx^{(i)}+w_{0})\geq 1
$$
* **significato**: devo classificare tutti bene, si comporta come il perceptron.

**problema vincoli**: spesso le istanze non sono linearmente separabili, dunque introduciamo gli slack per permettere degli errori
* se $y^{(i)} = 1$ allora la **formula sopra diventa** $wx^{(i)} + w_{0} \geq 1 - \xi^{(i)}$
* se $y^{(i)} = -1$ allora la formula sopra diventa $wx^{(i)}+w_{0} \leq -1 + \xi^{(i)}$

**riscriviamo la funzione obiettivo**: vogliamo aggiungere come errore il valore degli slack, e li pesiamo con $C$
$$
\frac{\|w\|}{2}  + C \sum_{i=1}^n \xi^i
$$

**problema**: la funzione non e' derivabile! presenta un punto angoloso
**hinge loss**:
$$
\xi^{(i)}=\max(0, 1-y^{(i)}(w\cdot x^{(i)}+w_{0}))
$$


**ridefinisco la funzione obiettivo**:
$$
J(w) = \frac{1}{2}\|w\|^2 + C \sum_{i=1}^n \max(0, 1-y^{(i)}(wx^{(i)} + w_{0}))
$$

**ho due casi dunque**:
* classifico correttamente, ossia $1-y^{(i)}(wx^{(i)} + w_{0}) < 0$
* classifico male, ossia $1-y^{(i)}(wx^{(i)} + w_{0}) \geq 0$

$J(w)= \begin{cases} w-\eta w \text{ se classifico correttamente} \\ w- \eta(w-Cy^{(i)}x^{(i)}) \end{cases}$

**iperparametro** $C$:
1. **se $C$ elevato con istanze separabili**: *il margine si restringe, voglio classificare meglio piuttosto che avere un margine ampio*
	1. **overfitting**: ho basso bias ma alta varianza, ossia rischio di adattarmi troppo
2. **se $C$ basso**: ho un margine piu largo poiche permetto piu errori ma generalizzo meglio
	1. **overfitting**: alto bias e bassa varianza, ossia rischio di non catturare la vera distribuzione dei dati

## istanze non separabili
**calcolare una nuova feature**: posso estrarre dai dati una feature che renda l'istanza separabile

**problema**: lavorare in $d+1$ dimensioni e' costoso computazionalmente.
**soluzione, kernel trick**: usare una funzione kernel per fare i calcoli in piu dimensioni utilizzando campioni con meno dimensioni.

**funzione kernel**: e tale che mi permette di calcolare il prodotto di $\phi(x_{1})\cdot \phi(x_{2})$ senza calcolare esplicitamente $\phi(x)$:
$$
K(x_{1},x_{2}) = \phi(x_{1}) \cdot \phi(x_{2})
$$

**quale kernel usare?**
$$
K(x_{1},x_{2})=e^{(-\lambda \| x_{1}-x_{2}\|^2)}
$$
* $\gamma>0$ controlla l'influenza dei singoli punti di addestramento
* $\gamma$ alto: allora do più peso alle distanze tra i campioni
* $\gamma$ basso: allora do meno peso alle distanze tra i campioni.

$K$ **espande su un numero potenzialmente infinito di dimensioni**:
$$
e^t = \sum_{n=0}^\infty \frac{t^n}{n!}
$$

# valutare un modello
**bias elevato**: il modello e' troppo semplice, e non e' abbastanza preciso nel catturare la complessità del dataset.

**varianza elevata**: indica overfitting, ossia modello troppo legato alle peculiarita del dataset di addestramento

**evitare overfitting nella svm**:
$$
\min_{w,b,\xi} \frac{1}{2} \|w\|^2_{2} + C \sum_{i=1}^n \xi_{i}
$$
* con $\|w\|^2$ si vuole penalizzare l'uso di $w_{i}$ troppo grandi, distribuendo il suo valore tra gli altri $w_{j}$.
* vuol dire che il rumore si distribuisce su tutti i pesi.
* $\|w\|_{2} =\sqrt{ w^2_{1} + \dots }$
* $\|w\|^2_{2} = w_{1}^2 + \dots$ 

**valutazione con metodo holdout**: 
* **training set**: estrailo dal data set
* **test set e validation set**: dividi il resto
* **come si usa**? addestro il modello sul training set, e valuto i parametri sul validation set (lo uso come fosse il test set, ma piu volte). alla fine verifico come performa sul test set
* **problema**: e' un'approccio abbastanza casuale, dipende da come sono stati tagliati i due insiemi.

**valutazione cross validation**:
* **fold**: si suddivide il dataset in $k\text{-fold}$, con $k=5,10$
* **per $i=1,\dots,k$ iterazioni**:
	* il fold $i\text{-esimo}$ viene usato come validation
	* il resto come training set
	* produci un punteggio per la valutazione
* **fai la media dei punteggi**
* **come si usa**? addestro $k$ volte il modello e lo valuto, ogni volta utilizzando sottoinsiemi differenti. Questo metodo

**matrice confusione**: la matrice mostra i seguenti valori
* `tp`: n. valori identificati come positivi, che lo sono veramente
* `fp`: n. valori identificati come positivi, ma che non lo sono
* `tn`: n. valori identificati come negativi, che lo sono veramente
* `fn`: n. valori identificati come negativi, che non lo sono veramente