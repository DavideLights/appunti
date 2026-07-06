
# wildcard queries
**spell correction**: *molti utenti sbagliano a scrivere / non sanno la parola precisa*

**wildcard**: `*`. permette cercare parole se ne si conosce solo una porzione.

**cercare le parole**: ho bisogno di una struttura dati che mi permetta di farlo. Per esempio un'albero binario ben bilanciato.

**albero binario**: se i termini sono ordinati in un albero binario, allora posso facilmente recuperare le parole corrispondenti alla query `mon*` per cui fare le query, ossia tutte le foglie di un certo sotto-albero.
![[Pasted image 20260421114206.png]]

**come faccio a processare la query**: `se*ate AND fil*er`?
* **pero come processo `se*ate`**? faccio l'AND tra `se*` ed `*ate`.
* **problema**: troppi `AND` se ho tante wildcard di questo tipo. Costa troppo anche se uso un albero binario.

**soluzione definitiva**: *Permuterm Index*
* **gestisce** le wildcard query dove `*` si trova in varie posizioni.
* **che cos'e'?**: indice di tutte le permutazioni possibili di una parola.
* **puntatore**: ogni rotazione punta al termine originale.
* **perché**? ruotando trasformo tutte le wild-card nella forma standard con `*` solo alla fine. 
* **struttura dati per le rotazioni**: `B-tree`.
* **carattere aggiuntivo**: `$` indica la fine del termine
* **come cerco queste permutazioni?** le metto tutte nel dizionario, e nell'albero di ricerca, risalendo il puntatore ottengo la parola originale.
![[Pasted image 20260327110215.png]]

![[Pasted image 20260327110556.png]]
**come si usa**? ottenuta una query del tipo `m*n`, questa diventa `n$m*` e cerco nell'albero binario le possibili alternative che continuano la parola. 
* **nota**: l'albero binario contiene tutte le permutazioni
* **da permutazione a originale**: devo leggere il permuterm index per ottenere la parola originale che ho completato.
## bigram (k-gram) indexes
**permuterm, problema di spazio**: il permuterm cresce molto velocemente in spazio con un dizionario di termini lunghi.

**k-gram**: enumera i $\text{k-grammi}$, ossia le sequenze di $k$ caratteri che occorrono in un termine.

**esempio**: i $2\text{-grammi}$ sono tutte le sequenze di 2 caratteri.
![[Pasted image 20260327111113.png]]

**inverted index dei k-gram**: devo mantenerne uno per andare dai bigrammi ai termini nel dizionario.
![[Pasted image 20260327111246.png]]

**processare una query**: se devo risolvere `mon*` allora devo fare `$m AND mo AND on`.
* **falsi positivi**: devo applicare un **post filter**, il sistema trova anche `moon` che contiene `$m`, `mo` ed `on`.
* **meglio del permuterm**: piu' efficiente.
# spelling error detection and correction
* spelling error **detection**
* spelling error **correction**: 
	* **correggi** `hte` in `the`
	* **suggerisci** correzione o una **lista** di correzioni.

**probabilita**: l'errore di spelling varia in base all'applicativo. Su telefonino ho un'errore del $7\%$. (TODO: sta robba e' vera???)


| tipo errore     | non o real? | context sensitive? | descrizione                                                                                  |
| --------------- | ----------- | ------------------ | -------------------------------------------------------------------------------------------- |
| `non-word`      | `non-word`  | no                 | Si ha quando **il termine non appartiene al dizionario**. Facile da individuare come errore. |
| `typographical` | `real-word` | si                 | **errore di battitura**, *ho scritto male la parola*.                                        |
| `cognitive`     | `real-word` | si                 | **errore di pronuncia**, dovuto a parole con suono simile. es `peace -> piece`, `two -> too` |

**rimediare ad** `non-word spelling`: ogni parola che non sta nel dizionario e' un errore di questo tipo.
* **dizionario enorme**: equivale a piu precisione.
* **edit distance**: la parola con cui correggere minimizza la edit distance
* **noisy channel probability**: considera il rumore. Ossia la tastiera del telefono ha rumore piu' alto rispetto alla tastiera del telefono.

**candidate set**: genera per la parola $w$ un set di parole con
* **pronuncia** simile
* **spelling** simile
* che contiene $w$ **stesso**.

**scegliere il candidato**: 
* **context-sensitive**: quali dei candidati hanno senso nella query?
* **i candidati hanno edit-distance bassa**, dove gli edits possibili sono: *insertion, deletion, substitution e transposition of two adjacent letters.*
* **probabilita**: 80% degli errori con edit distance pari a 1
	* **edit distance pari a 1**, ossia basta fare una di queste azioni a partire dall'errore: inserimento, eliminazione, trasposizione, sostituzione.
* **spazi e trattini**: `thisidea` $\to$ `this idea`. `inlaw` $\to$ `in-law`.
* **merge**: `data base` $\to$ `database`.

## Noisy channel model
**obiettivo**: correggere le `non-words`.

**noisy channel model**: $\hat w = \text{argmax}_{w\in V}P(w|x) = \text{argmax}_{w\in V}\frac{P(x|w)P(w)}{P(x)} = \text{argmax}_{w \in V}P(x|w)P(w)$
* **oss**: se voglio trovare il massimo, allora il denominatore e' trascurabile dato che e' costante $\forall w \in V$
* **parola corretta**: $w$, un termine.
* **errore**: $x$, un termine.
* **frazione costante**: dunque si toglie quando applico bayes.

**modelli**, mi servono per calcolare $P(x|w)$ ed $P(w)$, sono i miei stimatori:
* **CHANNEL MODEL PROBABILITY**: $P(x|w)$ e' la probabilità che scrivo $x$ volendo scrivere $w$. si basa sulla confusion matrix e sulla edit distance.

*  **UNIGRAM PRIOR PROBABILITY**: $P(w) := \text{quanto e' comune la parola } w = \frac{C(w)}{T}$
	* $C(w) = \text{numero occorrenze}$
	* $T$ numero totale di termini nel corpus.

**computing error probability confusion matrix**: dice quante volte avviene ogni tipo di errore.
![[Pasted image 20260421142227.png]]

**channel model**: il modello per $P(x|w)$ funziona cosi
![[Pasted image 20260421142456.png]]
*  **ATTENZIONE**: dove $\text{count[...]}$ e' il **numero di occorrenze per $w_{i}$ la lettera corretta all'interno dell'intero corpus**

**edit distance**: e' il **numero minimo** di operazioni per trasformare una parola in un'altra. Si calcola usando programmazione dinamica.
* **edit distance 1**: costituisce l'80% degli errori
* **edit distance 2**: comprende edit distance 1, ed arriva a circa il 90%.

**come generare i candidati**: 
1. **soluzione scema, brute force**: confronto `x` con tutte le parole del dizionario, e' costoso.
2. **genero** tutte le parole con **edit dist** $\leq k$: costoso.
3. **k-gram index**: e' più efficiente, utilizzo l'indice invertito per recuperare parole che condividono $\text{k-grammi}$ simili
 4. **automa a stati finiti**: avanzato.
5. **liste precomputate**: veloce ma poco flessibile.

**problema confusion matrix**: alcune probabilità sono pari a 0, dunque si *azzera il prodotto* $P(x|w)P(w)=0$. 

**soluzione. Smoothing LaPlace**: aggiungi +1. *Nella confusion matrix faccio cosi*: $$P(x|w)=\frac{\text{sub}[x,w]+1}{\text{count}[w]+A}$$
## Context-sensitive spell correction
**contesto**: dobbiamo correggere le *real words* ed abbiamo bisogno di un contesto per decidere la parola giusta.

**noisy channel**: il modello precedente si basa solo su una parola alla volta. non ha una finestra sull'intera frase per decidere.
* **frase osservata**: $X = (x_{1},x_{2},\dots,x_{n})$ dove ogni $x_{i}$ e' una **parola**.
* **frase candidata**: $W$

**Insiemi candidati**: sia la sentence costituita da $x_{1},\dots,x_{n}$, per ogni $x_{i}$ genero $\text{Candidate}(x_{i}) = \{ x_i, w_{1}^i, w_{2}^i, \dots , w_{k}^i \}$
* ogni parola ha il suo insieme dei candidati

**Come scelgo la sequenza $W$ di candidati che massimizza** $P(W|x_{1},\dots,x_{n})$? uso un **language model**:
* **idealmente**: $\hat{W} = \text{argmax}P(W|X) = \text{argmax} P(X|W)P(W)$
* $P(X|W)$ e' facile da calcolare, ma $P(W)$ e' difficile. Come calcolo la probabilità $W$ tenendo conto che $W$ potrei non averla mai osservata per intera?

**Come calcolo $P(X|W)P(W)$**? che **modelli** uso?
* $P(X|W) = \prod_{i=1}P(x_{i}|w_{i}) = \text{probabilita di emissione}$ (**Hidden Markov Model**)
* $P(W)= \text{bigram model}$
	* dove $P_{\text{bigram}}(w_{k} | w_{k-1}) =\text{ probabilita di transizione}$ (**Hidden Markov Model**)

**BIGRAM MODEL (per context-sensitive)**: per calcolare $P(W)$ vedo **quanto ogni parola e' coerente con la precedente**, non guardo tutta la frase insieme.
* a differenza di **UNIGRAM MODEL** guardo la parola precedente.
* **modello markoviano**: bigram model e' markoviano, metto un limite alla storia di parole che guardo.
* $P(w_{1}, \dots, w_{n})=P(w_{1})P(w_{2}|w_{1})\dots P(w_{n}|w_{n-1}) = \text{prodotto delle p. di transizione}$. (**Hidden Markov Model**)

**smoothing**: devo includere fenomeni che potrei non aver visto, **alcuni bigram compaiono 0 volte**, dunque $P(w_{1},\dots,w_{n})$ si azzera.
* $P(w_{i}|w_{i-1})=(1-\lambda)P_{\text{bigram}}(w_{i}|w_{i-1}) + \lambda P_{\text{unigram}}(w_{i})$
	* $P_{\text{bigram}}(w_{k}|w_{k-1})=\frac{C(w_{k-1},w_{k})}{C(w_{k-1})}$
	* $P_{\text{unigram}}(w_{i})= \frac{C(w_{i})}{C(W)}$
* **interpolazione** tra **bigram** e **unigram**, se il bigramma non mi da informazione (ossia vale 0), magari l'unigram mi da un po' di informazioone.
* **parametro**: $\lambda$ va scelto tramite esperimenti per bilanciare unigram e bigram.

**log**: vogliamo lavorare con i logaritmi, dato che abbiamo tanti prodotti di probabilità nella formula dello smoothing.
![[Pasted image 20260327120750.png]]
* **underflow**: se non uso i logaritmi potrei sottostimare i valori.
	* **perche?** Dato che lavoro con numeri tra $0$ e $1$, i valori molto vicini a 0 vengono arrotondati e perdo informazione, non va bene!
* **log risolve underflow**: $\log P (w_{1} \dots w_{n}) = \log P(w_{1})  +\log P(w_{2}|w_{1}) + \dots$ 


> [!note] Markov
> Modello probabilistico utilizzato per descrivere una sequenza di eventi (o stati) in cui la probabilità che si verifichi un determinato evento futuro **dipende esclusivamente dallo stato immediatamente precedente**.
> * **Stati e Transizioni:** Il sistema si muove all'interno di un insieme di stati possibili. Il passaggio da uno stato all'altro è regolato da **probabilità di transizione**.
> * **A che serve?** Serve a scoprire informazioni nascoste, *modella la frase come sequenze di stati/simboli nel tempo*.

**hidden markov model**: 
* **osservazioni**, $X$: i simboli che vedo
* **hidden**, $W$: i simboli che devo scoprire, candidate ad essere sostituzioni corrette per lo spelling correction.
* **transizioni**: $P(w_{i}|w_{i-1})$, ossia le successioni possibili di parole.
* **emissioni**: $P(x_{i} |w_{i})$, le parole possibili da scegliere.


![[Pasted image 20260327121733.png]]

**grafo**:
* **layer**: posizione nella frase
* **nodo**: possibile parola candidata
* **complessita**: costruire il grafo e trovare la migliore combinazione richiede tempo esponenziale.
* **programmazione dinamica**: risolve il problema, in particolare nasce l'algoritmo di vitebri. **viterbi** e' troppo pesante e "preciso" per IR. 
* **1/2 errori per frase**: si assume che si facciano pochi errori. genero alcune frasi candidate, calcolo le loro probabilità e scelgo la migliore.

**semplificazione**: do un limite a quanti errori (1 o 2) potrei aver fat to, altrimenti l'**algoritmo di viterbi** potrebbe cambiare tutte le parole.

**language model**: usa statistica di unigrammi, bigrammi e costo delle sostituzioni per tirare fuori le parole giuste.

**problema**: *se la mia parola e' corretta ma molto rara*?
* **penalita**: le parole rare sono le piu penalizzate in questo sistema.
* **conseguenza**: se voglio correggere, lo faccio male in alcuni casi. Addirittura potrei correggere quando non serve.
* introduco la probabilita che l'utente sbagli la parola in input, a seconda del metodo di input.

**soluzione**: introduco $P(w|w)$, stimati, ossia probabilita che la parola osservata sia corretta. Devono essere valori abbastanza alti, da pesare successivamente.

**peso** $\beta$: $P(W)^\beta$ e' il peso da applicare a $P(W) = \text{probabilita che la parola osservata sia corretta}$ nella formula 
$$
\hat{w} = \text{argmax}_{w\in V}P(x|w)P(w)^{\beta}
$$


