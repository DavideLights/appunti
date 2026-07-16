
# metriche da usare per dataset sbilanciati e come bilanciare
**metodo scemo per il bilanciamento**: estraggo tanti campioni dalla classe maggioritaria quanti sono quelli nella classe minoritaria.

**metriche per la valutazione**:
* **confusion matrix, precision e recall**: calla CM posso ricavare le seguenti metriche
	* **precision**: percentuale di campioni etichettati come positivi che lo erano davvero
	* **recall**: percentuale di positivi identificati tra tutti i positivi
$$
\text{precision = } \frac{tp}{tp+fp} ;\text{ recall = } \frac{tp}{tp+fn}
$$

**accuracy**: e' definita come il numero medio di predizioni corrette. 
* **dataset sbilanciati**: non e' adatta
* **perche**? posso ottenere accuracy alta semplicemente predicendo la classe corretta.

**f1-score**: media armonica tra precision e recall
* massimizzata quando $\text{prec=recall}$
* si annulla quando una delle due vale 0
* **alta precision  + bassa recall**: identifico pochi positivi ma sono quasi tutti giusti
* **bassa precision + alta recall**: identifico molti positivi ma quasi tutti sono sbagliati
$$
F_{1} = 2 \frac{\text{precision} \cdot \text{recall}}{\text{precision }+\text{ recall}}
$$
**f1-score e dataset sbilanciati**: e' perfetta in questi casi, perche' voglio bilanciare i falsi positivi con i falsi negativi rispetto ai positivi.

## roc curve e metrica AUC
**tpr** e **fpr**:
$$
\text{TPR} =\frac{tp}{tp+fn}; \text{FPR}=\frac{fp}{fp+tn}
$$
**roc curve**: ogni modello viene addestrato fissando un valore di threshold per la classificazione, detto $t$
* **come si calcola**? per ogni possibile $t$, calcola la coppia $(TPR,FPR)$ e buttala sul grafico
* **obiettivo**: butta le coppie su un grafico, di questo grafico si vuole massimizare la AUC

**come si interpreta la roc curve**:
* **classificatore perfetto**: se c'e' un punto con $\text{TPR}=1,\text{FPR}=0$ allora il 
* **classificatore casuale**: se la roc curve, corrisponde ad una retta obliqua passante per origine
* **AUC**: massimizzare la AUC vuol dire abbassare l'FPR e massimizzare il TPR

## svm

**ottimizzare svm per dataset sbilanciati**:
$$
\frac{1}{2}\|w\|^2 + \sum_{i=1}^{N}\xi_iC_{i}
$$
* **parametro globale** $C$: sostituito nella formula da $C_{i}=C \cdot v_{i}$
* **peso del campione** $i$: $v_{i}= \frac{n}{2n_{c}}$
* **obiettivo**: voglio che la classe minoritaria abbia un peso maggiore di quella minoritaria, **dunque errori sulla classe minoritaria saranno piu pesanti**.

## bilanciare 
**sovracampionamento** con **SMOTE**:
* **per ogni campione minoritario**
	* scegli a caso un campione tra i $k$ vicini
	* traccia la retta tra i due campioni
	* crea un nuovo campione sulla retta
* **a che serve**? migliora la generalizzazione del modello

**classificare piu classi**:
* classificatore 1: allenalo a riconoscere la classe 1 dalle altre
* classificatore 2: allenalo a riconoscere la classe 2 dalle altre
* ecc...
* **come si usa?** esegui tutti i classificatori, e scegli l'output di quello con score piu alto in fase di predizione.