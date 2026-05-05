**approccio probabilistico**: otterremo un sistema che performa bene tanto quanto l'approccio vettoriale utilizzando le probabilità.
* permette di ragionare su eventi incerti esprimendoli come probabilita.

**domanda da studiare**: quanto e' rilevante $d$ rispetto alla query $q$ fatta da un utente $u$?

**sorgenti di incertezza**:
* **utenti differenti** giudicano differentemente la rilevanza di $d$ rispetto a $q$
* **seconda del contesto**: un utente giudica differentemente $d$ rispetto a $q$ a seconda del contesto.
* **rappresentazione di** $d$: un utente giudica in base a come $d$ e' rappresentato. 
* **approssimazione del sistema ir**: per stimare la rilevanza di $d$ si fanno errori di approssimazione.

**probabilita**: voglio studiare $P(\text{relevant} | d,q) = \text{probabilita che il documento e' buono dati } d,q$.

**come lo calcolo la rilevanza**?
* **modelli probabilistici**: *binary independence model e bestmatch25.*
* **language model**: che si applica anche all'information retrieval.

**oss. su vector space model (VSM)**: in questo modello, il documento piu simile potrebbe essere totalmente irrilevante per l'utente. 

> [!note] gemini
> Il Vector Space Model (VSM) si basa sulla **somiglianza sintattica** (coseno tra i vettori). Se la tua query è "panca" e il documento parla di "panca" intesa come attrezzo da palestra, ma tu cercavi un elemento d'arredo, il VSM ti darà un'alta similarità perché le parole coincidono, ma la **rilevanza** per te è zero. L'approccio probabilistico cerca di modellare proprio questa incertezza dell'utente.

**formule varie**:
* $P(A,B) = P(A \cap B) = P(A|B)P(B) = P(B|A)P(A)$.
* $P(B) = P(A,B) \cdot P(\bar A, B)$.

**bayes e p. totali**:
$$
p(A|B) = \frac{p(B|A) p(A)}{p(B)} = \left[ \frac{p(B|A)}{p(B|A)p(A) + p(B| \bar A)p(\bar{ A})} \right] p(A)
$$
* **priori**: $P(A) = \text{priorita a priori}$
* **posteriori**: $P(A|B) = \text{probabilita a posteriori}$
* **ossia**: posso trovare la probabilità a posteriori di $A$ usando quella a priori.

**odds**: $O(A) = \frac{P(A)}{P(\bar{A})} = \frac{P(A)}{1-P(A)}$
* **ordinamento**: permette di ordinare i risultati, e' indicatore della rilevanza di un documento.
* se $O(A) > 1$ allora e' più probabile che il documento sia rilevante
* se $O(A) = 1$ allora non si sa
* se $O(A) < 1$ allora e' più probabile che il documento non rilevante. 

**rilevanza di un documento**: sia $p(R_{d,q})=p(R|d,q)$, usiamo **p. totali** per calcolare...
$$p(R|d,q) = \sum_{u\in U} p(R|d,q,u)p(u)$$
* $p(R|d,q) = \text{probabilita che il documento sia rilevante per il documento}$ dove $R_{d,q}$ e' una v.a. aleatoria.
	* $R_{d,q} = 1$ se il documento $d$ e' rilevante per $q$
	* $R_{d,q} = 0$ altrimenti
* $p(R|d,q,u)= \text{probabilita che l'utente } u \text{ giudica } d \text{ rilevante alla query } q$
* $p(u) = \text{ probabilita che l'utente } u \text{ e' chiamato a giudicare la rilevanza}$

**utenti**: nella formula non servono, omettere $p(u)$ non cambia l'ordinamento dei documenti.

>[!note] gemini
> Il professore intende che, in un sistema IR generico, **noi vogliamo un ranking che vada bene "in media" per tutti**. Siccome $p(u)$ (la probabilità che arrivi l'utente $u$) o la specifica opinione dell'utente non dipendono dal documento $d$ che stiamo analizzando, ai fini del **ranking** (ovvero decidere se $d_1$ sta sopra $d_2$) quel valore è una costante. ==Se moltiplichi tutti i punteggi per la stessa costante, l'ordine non cambia.==

**odds sulla rilevanza**. un documento e' rilevante se $p(R|d,q) > p(\bar{R}|d,q)$, ossia:
$$ O(R|d,q) = \frac{p(R|d,q)}{p(\bar{ R} | d,q)} > 1$$

**decomporre $p(R|d,q)$ usando bayes:** ci sono due modi
1. $p(R|d,q) = \frac{p(d|R,q)p(R|q)}{p(d|q)}$, ed $p(\bar{ R}| d,q)$ si ricava similmente
2. $p(R|d,q) = \frac{p(q|R,d)p(R|d)}{p(q|d)}$, ed $p(\bar{R}|d,q)$ si ricava similmente

**ranking**: faccio il ranking dei documenti osservando dunque $O(R|d,q)$ (odds).

**probabilistic ranking**: devo ordinare in base a $p(R_{d,q}) = p(R|d,q)$ e devo stimare questi valori. Calcolarlo e' complicato, devo fare delle **assunzioni**.

**assunzione**:
* **indipendenza**: assumiamo $d$ e $q$  indipendenti $\forall d,q$
* **uniformita documenti**: $\forall d,d': p(d) = p(d')$ (questa assunzione non vale per altri contesti, es: pagerank)
* **ignorare**: $p(R|q)$ puo essere ignorato. e' un valore costante per tutti i documenti.
$$
p(R|d,q) = \frac{p(d|R,q)p(R|q)}{p(d|q)} = \frac{p(d|R,q)p(R|q)}{p(d)}
$$
**definizioni**:
* $p(d|R,q) = \text{p. che } d \text{ venga scelto u.a.r dai documenti rilevanti per } q$.
* $p(R|q) = \text{p. che un documento scelto dalla collezione sia rilevante per } q$
* $p(d|q) = p(d) = \text{la probabilita che } d \text{ sia pescato dalla collezione}$, si assumono $d,q$  indipendenti $\forall d,q$.

## PRP e calcolo del rischio
**PRP (Probability Ranking Principle)**:  
> [!note] PRP (Probability Ranking Principle)
>  *If the retrieved documents (w.r.t a query) are ranked decreasingly on their probability of relevance, then the effectiveness of the system will be the best that is obtainable.*
* **come dicevano ad oxford**: *se i documenti sono ordinati in ordine decrscente in base alla probabilita di rilevanza, allora abbiamo ottenuto il miglior sistema di ir possibile*. **e grazie al cazzo**.
>[!note] gemini
>Il PRP dice che se non hai altre informazioni, ==l'ordine basato sulla probabilità di rilevanza decrescente è quello che ti garantisce, statisticamente, il minor numero di documenti irrilevanti nelle prime posizioni==. È l'ottimo teorico ==sotto l'ipotesi che la rilevanza di un documento sia indipendente da quella degli altri.==


~~**PRP esteso**:~~
>[!note] ~~PRP esteso~~
> ~~If *the IR* system’s response to each *query* is a ranking of the documents ... in order of decreasing probability of relevance to the *query*, where the probabilities are estimated as accurately as possible on the basis of whatever data have been made available to the system for this purpose, the overall effectiveness of the system to its user will be the best that is obtainable on the basis of those data~~

**Voglio calcolare il rischio**. siano:
* $C(d,q) = \text{ costo quando }d \text{ e' rilevante rispetto a } q \text{ e non e' stato recuperato}$
* $C'(d,q) = \text{ costo quando }d \text{ non e' rilevante rispetto a } q \text{ ed e' stato recuperato}$
* $D = D(q)$ insieme di documenti ritornati dal sistema.
* **allora il rischio** e' $R(D(q)) = \sum_{d\in D} C'(d,q)p(\bar{R}|d,q) + \sum_{d \not \in D} C(d,q) p(R|d,q)$
* **ossia**: $R(D(q)) = \sum_{d \in D} C'(d,q)(1-p(R|d,q)) + \sum_{d \not \in D} C(d,q) p(R|d,q)$

**A che serve il rischio**? si puo' usare come misura inversa rispetto alla qualita di un risultato.

**assunzioni sul rischio**:
* $D(q) = k$ e' n valore costante.
* $C,C'$ sono variabili binarie.

**calcolare il rischio**:
$$
R(D(q)) = \sum_{d \in D(q)}(1-p(R|d,q)) + \sum_{d \notin D(q) }p(R|d,q) = |D(q)| + \sum_{d \notin D(q)} p(R|d,q) - \sum_{d \in D(q)} p(R|d,q)
$$
* $\forall d\in D$ voglio ottenere la probabilita che $d$ **non venga restituito** come parte del risultato
* $\forall d\notin D$ voglio ottenere la probabilita che $d$ **venga restituito** come parte del risultato

**minimizzare** $R(D(q))$: vuol dire che $D(q)$ e' tale che da **massimizzare** 
$$
\star:\sum_{d \in D(q)} p(R|d,q) - \sum_{d \notin D(q)} p(R|d,q)
$$
**massimizzare** $\star$: vuol dire che $D(q)$ contiene i $k$ documenti con $p(R|d,q)$ piu alta.
* assumendo che $|D(q)| = k$

**Teorema**: assumendo 0/1 loss, allora **PRP** e' ottimo e minimizza gli errori, ossia il costo per gli errori.
* gemini vuol dire che con $C,C'$ variabili binarie allora prp e' ottimo?

## fare effettivamente i calcoli con BIM
**Binary Independence Model**: e' il modello piu' semplice. faccio le seguenti assunzioni
* **indipendenza**: le rilevanze dei documenti sono indipendenti l'une dalle altre.
* **rilevanza binaria**: il documento e' rilevante oppure no.
* il documento e' un **set di features** che costituiscono la **rappresentazione**: $d$ e' il vettore $(f_{1},\dots,f_{n})$ di features. allora consideriamo la probabilita che le feature $f_{1},\dots,f_{n}$ siano rilevanti rispetto a $q$:
$$
p(R|f_{1},\dots,f_n,q) = \frac{p(f_{1},\dots,fn| R,q)p(R|q)}{p(f_{1},\dots,f_n|q)} =_{rank} p(f_{1},\dots,f_{n}|R,q)
$$
* $=_{rank}$: ==simbolo di equivalenza ai fini del ranking==
* **indipendenza feature**: $p(f_{1},\dots,f_{n}|R,q) = \prod_{i} p(f_{i}|R,q)$, dunque le features sono indipendenti tra loro $\forall \in [1,n]$.

**in BIM, ogni feture di un documento**:
1. e' associata ad un termine
2. e' binario: vale 1 se occorre nel documento, 0 altrimenti.
3. **il documento e'** $v_{d}= (x_{1},\dots,x_{m})$ con $x_{i} = 1$ se $t_{i} \in d$.
4. **la query e** '$v_{q} = (y_{1},\dots,y_{m})$ dove $y_{i} = 1$ se $t_{i} \in q$.
5. **collisioni**: *query e documenti differenti potrebbero essere rappresentati dallo stesso vettore*.

**rimodelliamo** $p(R|d,q)$ **usando i vettori**:
* $p(R|v_{d},v_{q}) = \frac{p(v_{d}|R,v_{q})p(R|v_{q})}{p(v_{d}|v_{q})} =_{rank} p(v_{d}|R,v_{q})$
* **similmente**: $p(\bar{R}|v_{d},v_{q}) = p(v_{d}| \bar{R}, v_{q})$
* $p(v_{d}|R,v_{q})$ e' la probabilita che se un documento rilevante e' stato selezionato, allora $v_{d}$ e' la sua rappresentazione.

**fare il ranking in BIM**: data la query $q$ faccio il ranking guardando $p(R|v_{d},v_{q})$ per ogni documento rispetto alla query. ossia:![[Pasted image 20260427174833.png]]
$$
O(R|v_{d},v_{q}) =_{rank} \prod_{t_{i}:x_{i}=y_{i}} \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})}
$$

**split dei termini**: dato che $x_{i}$ puo' essere 0 o 1, allora:
$$\
O(R|v_{d},v_{q}) =_{rank} \prod_{t_{i}:x_{i}=1} \frac{p(x_{i}=1|R,v_{q})}{p(x_{i}=1| \bar{R}, v_{q})} \cdot \prod_{t_{i}:x_{i}=0} \frac{p(x_{i}=0|R,v_{q})}{p(x_{i}=0| \bar{R}, v_{q})}
$$

**tabella sulle probabilità rispetto ai termini**:

|                            | relevant document $(R)$ | nonrelevant doucment ($\bar{R}$) |
| -------------------------- | ----------------------- | -------------------------------- |
| term present ($x_{t} = 1$) | $p_{t}$                 | $u_{t}$                          |
| term absent ($x_{t} = 0$)  | $1-p_{t}$               | $1-u_{t}$                        |
dove:
* $p_{t} = p(x_{t}=1|R,v_{q})$ e' la probabilità che un **termine appaia** in un **documento rilevante** per $q$.
* $u_{t} = p(x_{t} = 1| \bar{R},v_{q})$ e' la probabilità che un **termine appaia** in un **documento non rilevante** per $q$.

$$
\
O(R|v_{d},v_{q}) =_{rank} \prod_{t_{i}:x_{i}=1} \frac{p_{i}}{u_{i}} \cdot \prod_{t_{i}:x_{i}=0} \frac{1-p_{i}}{1-u_{i}}
$$
**e' equivalente a** (==attenzione ai pedici delle produttorie==):
$$
\
O(R|v_{d},v_{q}) =_{rank} \prod_{t_{i}:x_{i}=y_{i}=1} \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})} \cdot \prod_{t_{i}:y_{i}=1} \frac{1-p_{i}}{1-u_{i}}
$$

**si semplifica in**:
$$
O(R|v_{d},v_{q}) =_{rank} \prod_{t_{i}:x_{i}=y_{i}=1} \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})} 
$$

> [!note] gemini
> Nella formula originale, ==noi abbiamo termini che appaiono nel documento ($x_i=1$) e termini che NON appaiono ($x_i=0$)==.
> Per renderlo calcolabile solo sui termini presenti, moltiplichiamo e dividiamo per $\frac{1-p_i}{1-u_i}$ per i termini dove $x_i=1$. Così otteniamo una parte che dipende solo dalla query (costante) e una parte che dipende solo dai termini presenti nel documento. **Risultato:** l'RSV (Retrieval Status Value) diventa una somma di pesi solo sui termini presenti.
> 

**RSV (Retrieval Status Value)**: passiamo ai logaritmi, e' piu comodo.
1. $c_{i} = \log \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})} = \log \frac{p_{i}}{1-p_{i}} - \log \frac{u_{i}}{1-u_{i}}$
	1. $\frac{p_{i}}{1-p_{i}}$ e' odds per $t_{i}$ che appare in un documento rilevante.
	2. $\frac{u_{i}}{1-u_{i}}$ e' odds per $t_{i}$ che appare in un documento non rilevante.
2. $RSV_{d} = \sum_{t_{i}:x_{i}=y_{i}=1} \log_{} c_{i}$

**peso**: $c_{i}$ si comporta come un peso.
* $c_{i} > 0$: allora $t_{i}$ compare per lo piu in documenti **rilevanti**
* $c_{i} < 0$: allora $t_{i}$ compare per lo piu in documenti **non rilevanti**

## stimare le probabilita: con set di giudizi disponibili
**due scenari**:
* **pseudo-relevance feedback**: *a training set of relevance judgements given by users is available*. *Relevance judgements may derive by a pseudo-relevance feedback method*
* **nessuna informazione**

**dati da usare**: nel primo caso ho dei giudizi disponibili
* $N$ = numero di documenti totali
* $R$ = numero di documenti rilevanti segnalati da un'utente
* $r_{i}$ numero di documenti rilevanti in cui compare $t_{i}$
* $df_{t_{i}}$ numero di documenti che contengono $t_{i}$
![[Pasted image 20260428135931.png]]

**evitare gli zeri**: faccio smoothing aggiungendo $\alpha=0.5$, voglio evitare valori pari a 0 nella formula.

![[Pasted image 20260428140101.png]]

**assunzioni**: i documenti rilevanti sono pochissimi rispetto al numero di documenti nella collezione
* allora posso dire che $u_{i} = \frac{df_{t_{i}}}{N}$
* $\log \frac{1-u_{i}}{u_{i}} = \frac{\log N-df_{t_{i}}}{df_{t_{I}}} \sim \log \frac{N}{df_{t_{i}}}$

possiamo concludere che:
$$
c_{i} = \log \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})} \sim \log \frac{p_{i}}{(1-p_{i})} + \log \frac{N}{df_{t_{i}}}
$$

## stimare senza giudizi
**assunzione**: $p_{i}$ costante su tutti i termini $x_{i}$ e fissato $p_{i}=0.5$

**conseguenza**: ogni termine potrebbe o no comparire in un documento rilevante con probabilità $0.5$. *Si cancellano i fattori nell'espressione dell'RSV*

**similmente a prima**: 
$$
RSV_{d} = \sum_{t_{i}:x_{i}=y_{i}=1} \log \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})} \sim \sum_{t_{i}:x_{i}=y_{i}=1} \log \frac{N}{df_{t_{i}}}
$$

**quando va bene questo RSV**? per pochi documenti ci sta.

## differenze tra vector space ed BIM
1. non sono piu di tanto differenti
2. **gemini** che vuol dire? In either case you build an information retrieval scheme in the exact same way.
3. la formula di BIM e' simile a vector space ma e' molto approssimata.

**limitazioni di BIM**: e' stato creato per fare retrieval su titoli e abstract. Non andrebbe usato per la ricerca su interi documenti, dovremmo porre attenzione alla term frequency e alla lunghezza dei documenti.
* BIM non analizza term frequency e doc length.


>[!warning] per martedi
> me se rompe la stampante un giorno. come faccio a dire la probabilita che si rompe di nuovo al giorno $x$? che distribuzione si usa? poisson


