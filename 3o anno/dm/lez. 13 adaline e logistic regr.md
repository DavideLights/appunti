
**perceptron**: se classifica in modo errato, aggiorna i pesi. se non sbaglia, smette con l'addestramento.

**adaline**: si vuole minimizzare l'errore nella classificazione, si usa dunque una funzione di costo
* **attenzione**: a differenza della regressione lineare vogliamo classificare e non predire il valore di una funzione.

**differenze ed analogie tra adaline e perceptron**:
* **funzione di attivazione**: 
	* **adaline**: e' la funzione identità
	* **perceptron**: non c'e'
* **funzione treshold**:
	* **adaline**: corrisponde all'output e serve per la classificazione
	* **perceptron**: e' l'unico nodo presente
* **calcolo dell'errore**:
	* **adaline**: prende l'output della funzione di attivazione
	* **perceptron**: prende l'output della funzione di treshold
* **f. errore**: utilizzano entrambi la somma degli errori quadrati

**problema**: il miglior separatore potrebbe essere pero' un $w$ con errore grande, mentre qui si cerca di minimizzarlo.
* **oss**: la funzione di errore guarda le distanze tra il target e quello che ho predetto! non corrisponde necessariamente al miglior piano separatore
$$
\frac{\partial J}{\partial w_j} = \frac{\partial}{\partial w_j} \frac{1}{2}\sum_{i=1}^n \left( y^{(i)} - w\cdot x^{(i)} \right)^2
$$

## regole aggiornamento
**perceptron**:
$$
w_{j} \gets w_{j} + \eta(y^{(i)}-\hat{y}^{(i)})x_{j}^{(i)}
$$
**adaline**:
$$w_j \leftarrow w_j + \eta \sum_{i=1}^{n} (y^{(i)} - w\cdot x^{(i)}) x_j^{(i)}$$

**oss**: 
* **errore globale**: aggiorno il peso guardando tutti i campioni
* **valore continuo**: quando misuro l'errore per ogni campione guardo la distanza come **valore continuo** tra $y^{(i)}$ e $w \cdot x^{(i)}$ 
	* **perceptron**: l'errore e' $y^{(i)} - \hat{y}^{(i)}$, ossia la differenza tra le etichette delle due classi, ossia dove $- \hat y^{(i)}$ e' **discreto**
* **sbagliare il meno possible**: adaline vuole trovare l'iperpiano che sbaglia il meno possible, anche se l'istanza non e' separabile da alcun piano


## logistic regression

**vogliamo utilizzare la seguente funzione di attivazione**:
$$
\phi (z) = \frac{1}{1+e^{-z}}
$$
* classifico con $+1$ se $\phi(z) \geq 0.5$

**idea**: lavorare con misure di proabilita
* $p = \text{probabilita di classificare correttamente l'esempio}$
* usiamo odds per combinare $p$ col suo complemento
* usiamo il logaritmo perche' e' comodo (valori piu piccoli ecc...)

$$
\text{Odds}(p) = \frac{p}{1-p}
$$
$$
\text{logit}(p) = \log \left(  \frac{p}{1-p} \right) = z
$$
come trovo $\phi(z)$? essenzialmente, voglio riscrivere $p$ assumendo che 
$$
\text{logit}(p) = \log \left(  \frac{p}{1-p} \right) = w \cdot x =z
$$

**nuova funzione di errore**: log-verosimiglianza, ed e' da massimizzare
$$\prod_{i=1}^{n} \phi(w\cdot x^{(i)})^{y^{(i)}}(1-\phi(w\cdot x^{(i)}))^{1-y^{(i)}} \to 
\sum_{i=1}^n (y^{(i)}\log \phi(z) 
+ (1-y^{(i)})\log(1-\phi(z) ))
$$
* **segno**: cambio segno per trasformarlo in problema di minimizzazione

**aggiornamento pesi**: calcolando le derivate, magicamente
$$w_j \leftarrow w_j + \eta \sum_{i=1}^{n} (y^{(i)} - \phi(z)) x_j^{(i)}$$
## standardizzazione
Nota: invece di calcolare `mu` e `std` sull'intero dataset, li ho caclcolati solo sul `train set`. Questo perche' devo standardizzare rispetto a deviazione e media della fase di addestramento, altrimenti starei applicando sui dati la media del test set, ed e' concettualemente sbagliato.

## Domanda esame: Perche' la versione stocastica converge prima?
Perche' anche se fatto su piccoli batch, la versione stocastica fa piu aggiornamenti in un'iterazione.
Praticamente faccio $N / \text{batch\_size}$ aggiornamenti:

* i batch sono scelti in modo casuale, dunque c'e' molto rumore

* pero' la somma di tutti i pesi e' molto vantaggiosa rispetto al rumore

* il rumore e' vantaggioso: permette di uscire da minimi locali poco profondi, o dai punti di sella, li dove il normale Gradient Descent calcolerebbe una valore vicino a 0

  

Attenzione:

> gradiente calcolato sull'intero dataset (Batch Gradient Descent) è la "direzione vera" verso il minimo globale (o locale) della funzione di costo. È preciso, ma lento e costoso. Quando usi un mini-batch, stai calcolando il gradiente su un campione. Poiché quel campione potrebbe non rappresentare perfettamente l'intera distribuzione (es. il batch contiene troppi dati "facili" o troppi dati "outlier"), la direzione che ottieni non è quella ottimale.