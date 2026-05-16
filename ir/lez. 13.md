## Relevance feedback e query expansion
**definire la funzione rilevanza**: 

**media armonica**:
$$
F_{1}=\frac{2PR}{P+R}
$$

**considera i sinonimi**: come recupero i sinonimi di "plane"? (es: aircraft)
* un semplice sistema di ir non recupera il documento giusto rilevante per l'utente.
* posso sfruttare il feedback dell'utente?

**due approcci**:
* locale: analisi on-deamnd
* globale

**relevance feedback**:
1. utente mette la query
2. search engine ritorna i documenti
3. l'utente seleziona quali sono rilevanti e quali non
4. il search engine calcola una query migliore

seleziono dai documenti selezionati come rilevanti le parole con idf piu alto

immaginando di essere nello spazio vettoriale, voglio modificare la query in modo da avvicinarla nello spazio ai documenti rilevanti e allontarla da quelli non rilevanti, questo vuol dire spostarmi verso altri documenti che possono piacere all'utente.

**centroide**: 
* posso spostarmi sul centroide o spostarmi verso di lui
* oppure mi avvicino, ma non troppo che e' meglio
* se ci sono documenti da cui allontarmi spero che mi avvicinano di piu ai documenti rilevanti

## rocchio e' finocchio
non so a priori a cosa devo dare importanza quando mi devo spostare, allora **parametrizzo** questi pesi
* $\alpha$: peso alla query originale
* $\beta$: peso ai documenti rilevanti, non conviene mai mettere $\beta$ a 1 e il resto a 0, i documenti giudicati rilevanti non sono esattamente quello che l'utente cercava.
* $\gamma$: peso ai documenti non rilevanti

quando e' utile? assunzioni
* A1: l'utente conosce i termini nella collezione abbastanza per impostare bene una query
* A2: i documenti rilevanti sono simili

qual'e' la fregatura? relevance feedback deve essere usato in modo cauto


....


assunzione/speranza: il mio sistema di retrieval non fa cagare, dunque i primi che ritorno non fanno veramente schifo
* i primi sono buoni
* gli ultimi fanno schifo
* sto prendendo un rischio perche' magari ho cannato forte.
* allora posso prendere documenti finiti in pagine lontane dalla 1, e le metto in top.

query drift: se i primi recuperati assumendo che saranno rilevanti potrei sbagliare contesto. `jaguar`: recupero le macchine invece che prendere l'animale!
* se lo applico piu volte diventa pericolososososososl!

fino ad ora ho usato metodi locali

globalmente: posso guardare i sinonimi nel dizionario che sto usando.

