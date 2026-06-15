**problema con adaline**: cerca di minimizzare le distanze tra i punti e l'iperpiano.

**attenzione**: nelle formule e' sempre comodo separare da $wx$ il bias $w_{0}$

**obettivo svm**: si vuole massimizzare la distanza tra l'iperpiano ed i margini.
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
\max(0, 1-y^{(i)}(w\cdot x^{(i)}+w_{0}))
$$