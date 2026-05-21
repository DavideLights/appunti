## Relevance feedback e query expansion
**definire la funzione rilevanza**: 

**media armonica**:
$$
F_{1}=\frac{2PR}{P+R}
$$
* tende a peggiorare quando uno dei due e' sbilanciato rispetto all'altro
* si tiene bassa se $P$ ed $R$ sono bilanciati

**come miglioro la recall**?
**considera i sinonimi**: come recupero i sinonimi di "plane"? (es: aircraft)
* un semplice sistema di ir non recupera il documento giusto rilevante per l'utente, anche se $d$ che contiene solo *aircraft* sarebbe il piu rilevante.
* **osservazione**: devo capire quali documenti sono rilevanti in base al feedback utente, dato che non posso sapere che plane e' sinonimo di aircraft nel mio sistema.

**due approcci**:
* **locale**: analisi on-demand per una query utente.
* **global**: fai un analisi globale per la query expansion.

**relevance feedback**:
1. utente mette la query
2. search engine ritorna i documenti
3. l'utente seleziona quali sono rilevanti e quali non
4. il search engine calcola una query migliore

**cosa ci faccio**? con i documenti rilevanti, mi ricavo i pesi dei termini
![[Pasted image 20260519150931.png]]
* combino questi valori con le frequenze della query e ripeto la ricerca con la nuova query.

**concetto chiave per il feedback**: centroide
$$
\vec{\mu}(D) = \frac{1}{|D|} \sum_{d\in D}\vec{v}(d)
$$

* $\vec{v}(d)=  \vec{d}$, ossia il vettore di $d$

**query ottimale**: $\vec{q}_{opt}$
* **assumendo di conscere**: $C_{r}$ e $C_{nr}$ documenti rilevanti e non rilevanti 
$$
S(\vec{q}, C_{r}, C_{nr}) = s(\vec{q}, \vec{\mu}(C_{r})) - s(\vec{q}, \vec{\mu}(C_{nr}))
$$
* con $s$ la misura di similarità
* $\vec{q}_{opt}$ e' la query che separa meglio documenti rilevanti e non rilevanti.

il $\vec{q}_{opt}$ e' tale da massimizzare:
$$
\vec{q} \cdot \vec{\mu}(C_{r})- \vec{q} \vec{\mu}(C_{nr})
$$
* **un cazz'e tutt'uno**: $\vec{q}$ e' costante puo' essere eliminato!
**dunque, l'ottimo e' il vettore differenza tra i due centroidi**:
$$
\vec{q}_{opt} = \vec{\mu}(C_{r}) - \vec{\mu}(C_{nr})
$$

**problema**: non conosco $C_{r}$, $C_{nr}$, ma ho dei suggerimenti dall'utente.

**Rocchio**: 
$$
\vec{q}_{m} = \alpha  \vec{q}_{0} + \beta \mu(D_{r}) - \gamma \mu(D_{nr})
$$
$$
= \alpha  \vec{q}_{0} + \beta    \frac{1}{D_{r}} \sum_{\vec{d}_{j} \in D_{r}} \vec{d}_{j}  - \gamma     \frac{1}{|D_{nr}|} \sum_{\vec{d}_{j} \in D_{nr}} \vec{d}_{j}
$$
con $\alpha, \beta, \gamma$ parametri

**obiettivo**: immaginando di essere nello spazio vettoriale, voglio modificare la query in modo da avvicinarla nello spazio ai documenti rilevanti e allontarla da quelli non rilevanti, questo vuol dire spostarmi verso altri documenti che possono piacere all'utente.

**come funziona rocchio**: 
* posso spostarmi sul centroide o spostarmi verso di lui
* oppure mi avvicino, ma non troppo che e' meglio
* se ci sono documenti da cui allontarmi spero che mi avvicinano di piu ai documenti rilevanti


**non so a priori a cosa devo dare importanza**: quando mi devo spostare, allora **parametrizzo** questi pesi
* $\alpha$: peso alla query originale
* $\beta$: peso ai documenti rilevanti, non conviene mai mettere $\beta$ a 1 e il resto a 0, i documenti giudicati rilevanti non sono esattamente quello che l'utente cercava.
* $\gamma$: peso ai documenti non rilevanti

**quando e' utile? assunzioni**
* **A1**: l'utente conosce i termini nella collezione abbastanza per impostare bene una query. 
	* **dunque se l'utente sbaglia parole**, es: `cosmonaut/astronaut` si viola l'assunzione.
* **A2**: i documenti rilevanti sono simili
	* ho documenti che parlano di tabacco lavorato e allo stesso tempo documenti su campagne anti-fumo.

**qual'e' la fregatura**? relevance feedback deve essere usato in modo cauto

**problemi in generale**:
* **query lunghe**: relevance feedback crea query lunghe, costose da processare.
* **utenti**: non tutti lasciano un feedback
* come capisco quando applico relevance feedback perche' e' stato recuperato un documento?

**pseudo-relevance feedback**: automatizza la parte manuale del true relevance feedback
* **algoritmo**: ottieni una ranked list in base agli hit della query utente
* assumi che il mio sistema di retrieval non fa schifo, dunque i primi $k$ sono marcati come rilevanti.
* **in media**: funziona bene.

**query-expansion**: sistema in cui aggiungo risorse che non dipendono dalla query alla query di ricerca. per esempio aggiungo i sinonimi



query drift: se i primi recuperati assumendo che saranno rilevanti potrei sbagliare contesto. `jaguar`: recupero le macchine invece che prendere l'animale!
* se lo applico piu volte diventa pericolososososososl!

fino ad ora ho usato metodi locali

globalmente: posso guardare i sinonimi nel dizionario che sto usando.

