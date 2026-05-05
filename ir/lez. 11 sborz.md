**cosa simile a lez 9 e 10, ma apparentemente folle**! $p(q|M_d) = \text{p. che la query } q \text{ sia stata generata da dal modello linguistico } M_d \text{ del documento } d$.
* supponi una query $q$ in input. questa e' legata a documenti con topic simili alle parole della query.
* per ogni query: $q$ e' fissato.
* cambia: $M_{d}$ il modello del documento $d$.
* voglio fare il rank con questa probabilita.


**modello generativo**: ogni documento e' una base per un modello generativo.

**come si usa**?
1. arriva la query
2. ottengo documenti candidati
3. per ogni documento ho un modello generativo per misurarlo su una query.

**modello generativo**: probabilita di tirar fuori una determinata parola avendone osservate gia altre.

**bagof words**: vedo le parole in isolamento nel modello generativo, ognuna isolata dalle altre.

>[!note] astrazione immagine



**finite state automation**: per astrarre la generazione di linguaggio

**probabilistic state automation (??)**: per astrarre le generazione di linguaggi, probabilistici (??)

**assunzione**: $p(w_{i}| w_{1}, \dots, w_{i-1}, M_{d}) = p()$ (bagof words)

**stop**: non e' una parola ma indica la fine della generazione.
**dato un'automa a stati finiti**: posso determinare la probabilita di generare quella frase tramite il prodotto delle probabilita.

**prodotto**: attenzione! si passera poi ovviamente a somme dei logaritmi.

**semplificazione**: consideriamo automi ad un solo stato, dunque per ogni termine ho solo una probabilita. **Ma dovrei conoscere queste probabilita**.

**dunque**: $p(\text{query}|M_{d_{1}}) = \prod_{t_{i} \in q} p(t_{i})$ (????)

**assunzioni**: $p(q|d) \approx p(q|M_{d})$  RIVEDIIIasidifdsaf

**ranking**: viene fatto in base a $p(q|M_{d})$. ossia il prodotto delle probabilità dei termini nella query.

## stimare le probabilita
**modello unigram**: $p(t_{i} | M_{d}) = p_{i}$
* query: bad di item.
* count: contare quante volte ogni termine compare.

**modello multinomiale**: VEDI FORMULONA
* $|q|!$ e' comune a tutti i documenti ordinati sulla stessa query
* e non mi interessa nemmeno il denominatore
* ottengo dunque una formula piu semplice come al solito dio canefafa

Cosa e' $M_{d}$: e' un vettore di robe...

**probabilita del termine nel documento**: e' il rapporto tra term frequency e lunghezza del documento.
* termini che non compaiono mai portano la likelihood della query a 0

**smoothing**: uso la tecnica di laplace come al solito. faccio + 1
* aggiungo 1 per ogni termine, dunque devo dividere per $|V|$ nella formula!!

**slide 25 non ho capito**:

**Jelinek-Mercer smoothing**:
* $\lambda$ e' un iperparametro, da stimare dunque tramite benchmark

> [!warning] esercizio scemo

> [!warning] esercizio esame

**problema di jelinek**: non tiene conto della lunghezza del documento. 
* **goal** combinazione delle evidenze del documento e della collezione, ma deve dipendere dalla lunghezza!!@#!$

**pseudotoken**: immaginando di concatenare un'altro documento che e' l'unione di tutte le parole del dizionario non ne tenevamo in considerazione la lunghezza. 
* smoothing di dirichlet, uso un peso $\mu$ arbitrario.
* **token virtuale**: con $\mu$ aggiungo token virtuali al conteggio.
* **a che serve dirichlet**: aggiungo al documento da sortare uno pseudo-documento di lungheza $\mu$ i cui termini sono distribuiti secondo il modello del documento.

ALTRE FORMULE!@!$!@#


$\lambda_{d}$: in dirichlet l'interpolazione viene fatta per documento e abbiamo ottenuto $\lambda_{d} = \frac{|d|}{|d|+\mu}$
* l'interpolazione dipende dal documento!!!!

dirichlet funziona bene per keywords queries
quell'altro su query lunghe!


**debolezza della baracca**: problemi con le frequenze dei termini, non ne tengo conto!

**che c'ha di figo**: e' semplice ma non competitivo.
