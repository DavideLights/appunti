## introduzione
**approccio probabilistico**: otterremo un sistema che performa bene tanto quanto l'approccio vettoriale utilizzando le probabilità.
* permette di ragionare su eventi incerti esprimendoli come probabilita.
* **eventi incerti** riguardano il sistema e la rilevanza di un documento per **l'utente**

**cosa studiamo e quali sono i problemi**? quanto e' rilevante $d$ rispetto alla query $q$ fatta da un utente $u$? ma ci sono tante approssimazioni da fare poiché:
* **utenti differenti** giudicano differentemente la rilevanza di $d$ rispetto a $q$
* **a seconda del contesto**: un utente giudica differentemente $d$ rispetto a $q$ a seconda del contesto.
* **in base alla rappresentazione di** $d$: un utente giudica in base a come $d$ e' rappresentato. 
* **in base approssimazione del sistema ir**: per stimare la rilevanza di un documento si fanno errori di approssimazione.

**domanda fondamentale**: come calcolo la rilevanza di un documento in base alla query? ho due modi:
* **modelli probabilistici**: *binary independence model e bestmatch25.*
* **language model**: che si applica anche all'information retrieval.

**in formula**:
$$
P(\text{relevant} | d,q) = \text{probabilita che il documento e' buono dati } d,q
$$
**irrilevanza per vector space model (VSM)**: in questo modello, il documento piu simile potrebbe essere totalmente irrilevante per l'utente. 

**perche puo' sbagliare VSM**?
* **somiglianza**: si basa esclusivamente sulla somiglianza sintattica (cosine similarity)
* **contesto**: non guarda il contesto delle parole, ossia come vengono intese e che significato assumono.

## Probabilita
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

**odds**: usiamo $O(A)$ per ordinare i documenti, questo sono le proprieta di **odds**
* **ordinamento**: permette di ordinare i risultati, *possiamo usarlo come indicatore della rilevanza di un documento*.
* se $O(A) > 1$ allora e' più probabile che il documento sia rilevante.
* se $O(A) = 1$ allora sono equiprobabili i due eventi.
* se $O(A) < 1$ allora e' più probabile che il documento non rilevante.

$$O(A) = \frac{P(A)}{P(\bar{A})} = \frac{P(A)}{1-P(A)}$$

## rilevanza di un documento
**rilevanza di un documento**: sia $p(R_{d,q})=p(R|d,q)$, la calcoliamo usando le **probabilità totali** rispetto agli **utenti**.
$$p(R|d,q) = \sum_{u\in U} p(R|d,q,u)p(u)$$
* **interpretazione**: $p(R|d,q)$ e' intesa come la *probabilità che **un utente** giudica $d$ rilevante in base alla query $q$*
* $p(R|d,q) = \text{probabilita che il documento sia rilevante per il documento}$ dove $R_{d,q}$ e' una v.a. aleatoria.
	* $R_{d,q} = 1$ se il documento $d$ e' rilevante per $q$
	* $R_{d,q} = 0$ altrimenti
* $p(R|d,q,u)= \text{probabilita che l'utente } u \text{ giudica } d \text{ rilevante alla query } q$
* $p(u) = \text{ probabilita che l'utente } u \text{ e' chiamato a giudicare la rilevanza}$

**$p(u)$ non ci interessa**: omettere $p(u)$ non cambia l'ordinamento dei documenti, assumiamo sia un **valore costante**, dunque uguale per tutti gli utenti.
* **perche**: moltiplicare i punteggio di ranking per la stessa costante non cambia l'ordinamento.

**applichiamo odds sulla rilevanza**: otteniamo dunque una formula che calcolata per tutti i documenti ci permette di effettuare il ranking.
* **un documento e' rilevante se**: $p(R|d,q) > p(\bar{R}|d,q)$
* **ossia se**:
$$ O(R|d,q) = \frac{p(R|d,q)}{p(\bar{ R} | d,q)} > 1$$

## calcolare le probabilita!
**obiettivo**: ora dobbiamo capire cosa sono $p(R|d,q)$ ed $p(\bar{R}|d,q)$, cosi posso calcolare **odds** e fare il ranking.

**posso decomporre $p(R|d,q)$ usando bayes**: ci sono due modi.
* il primo e':
$$p(R|d,q) = \frac{p(d|R,q)p(R|q)}{p(d|q)}$$ 
* il secondo e':
$$
p(R|d,q) = \frac{p(q|R,d)p(R|d)}{p(q|d)}
$$

* per $p(\bar{R}|d,q)$ si fa similmente in entrambi i modi.

**assunzioni**: calcolare queste probabilità e' difficile, dunque facciamo varie assunzioni.
* **indipendenza**: assumiamo $d$ e $q$  indipendenti $\forall d,q$
* **uniformita documenti**: $\forall d,d': p(d) = p(d')$ 
	* *questa assunzione non vale per page rank pero'!!!!*
* **ignorare**: $p(R|q)$ puo essere ignorato. e' un valore costante per tutti i documenti.

**dunque la formula diventa**: si semplifica $p(d|q)$ in $p(d)$
$$
p(R|d,q) = \frac{p(d|R,q)p(R|q)}{p(d|q)} = \frac{p(d|R,q)p(R|q)}{p(d)}
$$
* $p(d|R,q) = \text{p. che } d \text{ venga scelto u.a.r dai documenti rilevanti per } q$.
* $p(R|q) = \text{p. che un documento scelto dalla collezione sia rilevante per } q$, ed e' **costante per tutti i documenti che vengono confrontati con la query** $q$.
* $p(d|q) = p(d) = \text{la probabilita che } d \text{ sia pescato dalla collezione}$, si assumono $d,q$  indipendenti $\forall d,q$.

## PRP
**PRP (Probability Ranking Principle)**:  
> [!note] PRP (Probability Ranking Principle)
>  *If the retrieved documents (w.r.t a query) are ranked decreasingly on their probability of relevance, then the effectiveness of the system will be the best that is obtainable.*
* **come dicevano ad oxford**: *se i documenti sono ordinati in ordine decrscente in base alla probabilita di rilevanza, allora abbiamo ottenuto il miglior sistema di ir possibile*. **e grazie al cazzo**.
* **a che serve?** ottimizzare i risultati per l'utente finale che legge.
* **funzione di costo errore**: sono $C, C'$, le assumiamo binarie. Allora PRP e' ottimo.
* **assunzione indipendenza**: la rilevanza di un documento e' indipendente dalla rilevanza degli altri.

>[!note] gemini
>Il PRP dice che se non hai altre informazioni, ==l'ordine basato sulla probabilità di rilevanza decrescente è quello che ti garantisce, statisticamente, il minor numero di documenti irrilevanti nelle prime posizioni==. È l'ottimo teorico ==sotto l'ipotesi che la rilevanza di un documento sia indipendente da quella degli altri.==

## errore e rischio
**obiettivo**: per ottenere il miglior sistema ir possibile, bisogna calcolare l'errore che questo commette.
**perche?**: il miglior sistema ir e' quello che minimizza l'errore.

**definiamo il rischio**:  il sistema ir sbaglia in **2 casi**.
* quando il documento $d$  e' rilevante rispetto a $q$, ma non e' stato recuperato.
* quando il documento $d$ non e' rilevante rispetto a $q$, ma e' stato recuperato.

**in formule:**
* $C(d,q) = \text{ costo quando }d \text{ e' rilevante rispetto a } q \text{ e non e' stato recuperato}$
* $C'(d,q) = \text{ costo quando }d \text{ non e' rilevante rispetto a } q \text{ ed e' stato recuperato}$
* $D = D(q)$ insieme di documenti ritornati dal sistema

**assunzioni sul rischio**:
* $D(q) = k$ e' n valore costante.
* $C,C'$ sono variabili binarie.

**allora il rischio**:
$$R(D(q)) = \sum_{d\in D} C'(d,q)p(\bar{R}|d,q) + \sum_{d \not \in D} C(d,q) p(R|d,q)$$
$$R(D(q)) = \sum_{d \in D} C'(d,q)(1-p(R|d,q)) + \sum_{d \not \in D} C(d,q) p(R|d,q)$$
* **lol**: abbiamo introdotto $C', C$ ma sono superflui all'interno delle sommatorie.
$$
R(D(q)) = \sum_{d \in D(q)}(1-p(R|d,q)) + \sum_{d \notin D(q) }p(R|d,q)$$
* maneggiamo le sommatorie: sposto l'uno fuori e metto la parte negativa a destra.
$$ = |D(q)| + \sum_{d \notin D(q)} p(R|d,q) - \sum_{d \in D(q)} p(R|d,q)
$$**misura inversa**: il rischio e' una misura inversa **rispetto alla qualita** di un risultato.

**minimizzare** $R(D(q))$: vuol dire che $D(q)$ e' tale che da **massimizzare**.Dopo tante formule l'obiettivo era questo.
$$
\star:\sum_{d \in D(q)} p(R|d,q) - \sum_{d \notin D(q)} p(R|d,q)
$$

* $|D(q)|$ **omesso**: assumendo sia un parametro costante, allora minimizzare la formula sopra e' equivalente a minimizzare $\star$.

**Teorema**: assumendo 0/1 loss, allora **PRP** e' ottimo e minimizza gli errori, ossia il costo per gli errori.
* gemini vuol dire che con $C,C'$ variabili binarie allora prp e' ottimo?

## BIM e features
**Binary Independence Model**: e' il modello piu' semplice. faccio le seguenti assunzioni
* **indipendenza**: le rilevanze dei documenti sono indipendenti l'une dalle altre.
* **rilevanza binaria**: il documento e' rilevante oppure no. 
**features**: il documento e' un **set di features** che costituiscono la **rappresentazione**.
* $d$ e' il vettore $(f_{1},\dots,f_{n})$ di features. allora consideriamo la probabilità che le feature $f_{1},\dots,f_{n}$ siano rilevanti rispetto a $q$.
* ***indipendenza feature**: $p(f_{1},\dots,f_{n}|R,q) = \prod_{i} p(f_{i}|R,q)$, dunque le features sono indipendenti tra loro $\forall \in [1,n]$.

**formulona**:
$$
p(R|f_{1},\dots,f_n,q) = \frac{p(f_{1},\dots,fn| R,q)p(R|q)}{p(f_{1},\dots,f_n|q)} =_{rank} p(f_{1},\dots,f_{n}|R,q)
$$
* $=_{rank}$: ==simbolo di equivalenza ai fini del ranking==

**features**: cosa sono?
1. ogni feature e' associata ad un termine
2. e' binario: vale 1 se occorre nel documento, 0 altrimenti.
3. **il documento e'** $v_{d}= (x_{1},\dots,x_{m})$ con $x_{i} = 1$ se $t_{i} \in d$.
4. **la query e** '$v_{q} = (y_{1},\dots,y_{m})$ dove $y_{i} = 1$ se $t_{i} \in q$.
5. **collisioni**: *query e documenti differenti potrebbero essere rappresentati dallo stesso vettore*.

## calcolare la rilevanza e ottenere $RSV$
**rimodelliamo la rilevanza (vista prima) in termini di features**:
*passiamo da:*
$$
p(R|d,q) = \frac{p(d|R,q)p(R|q)}{p(d|q)} = \frac{p(d|R,q)p(R|q)}{p(d)}
$$
*a questa roba qua:*
$$p(R|v_{d},v_{q}) = \frac{p(v_{d}|R,v_{q})p(R|v_{q})}{p(v_{d}|v_{q})} =_{rank} p(v_{d}|R,v_{q})$$
 * **similmente**: $p(\bar{R}|v_{d},v_{q}) = p(v_{d}| \bar{R}, v_{q})$
* **nota**: $p(v_{d}|R,v_{q})$ e' la probabilità che se un documento rilevante per $q$ e' stato selezionato, allora $v_{d}$ e' la sua rappresentazione


**applichiamo odds**:  
$$
O(R|v_{d}, v_{q}) = \frac{p (R|v_{d}, v_{q})}{p(\bar{R}|v_{d},v_{q})} =_{\text{rank}} \frac{p(v_{d}|R,v_{q})}{p(v_{d}| \bar{R}, v_{q})}
$$
*dato che le feature sono indipendenti per assunzione, la presenza o l'assenza di qualsiasi parola sono eventi indipendenti tra loro*:
$$
 \frac{p(v_{d}|R,v_{q})}{p(v_{d}| \bar{R}, v_{q})} = \prod_{i=1}^M \frac{p(x_{i}|R,v_{q})}{p(x_{i}|\bar{R}, v_{q})}
$$

*ogni $x_{i}$ puo' essere 0 oppure 1, dunque faccio lo split dei termini*:
$$O(R|v_{d},v_{q})=_{\text{rank}} \prod_{t_{i}: x_{i}=1} \frac{p(x_{i}=1|R,v_{q})}{p(x_{i}=1|\bar{R}, v_{q})} \cdot \prod_{t_{i}: x_{i}=0} \frac{p(x_{i}=0|R,v_{q})}{p(x_{i}=0|\bar{R}, v_{q})}$$
**semplifichiamo**: *i termini che non compaiono nella query hanno stessa probabilita di comparire in documento rilevanti e non rilevanti.* ossia non mi interessano i termini che non sono nella query.
* **ossia**: se $y_{i}=0$ allora $p(x_{i}=1|R,v_{q}) = p(x_{i}=1|\bar{R}, v_{q})$

*dunque voglio guardare i termini che compaiono nella query e nel documento, e d i documenti che non compaiono nel documento, ma nella query*:
$$
O(R|v_{d},v_{q})=_{\text{rank}} \prod_{t_{i}: x_{i}=y_{i}=1} \frac{p(x_{i}=1|R,v_{q})}{p(x_{i}=1|\bar{R}, v_{q})} \cdot \prod_{t_{i}: x_{i}=0, y_{i}=1} \frac{p(x_{i}=0|R,v_{q})}{p(x_{i}=0|\bar{R}, v_{q})}
$$
**ora siano**: 
* $p_t = p(x_{t}=1 | R,v_{q}) = \text{ probabilita che il termine compaia in un documento rilevante per } q$
* $u_{t}=p(x_{t}=1 | \bar{R}, v_{q}) = \text{probabilita che il termine compaia in un documento non rilevante per } q$
![[Pasted image 20260506124451.png]]

$$
O(R|v_{d},v_{q})=_{\text{rank}} \prod_{t_{i}: x_{i}=y_{i}=1} \frac{p_{i}}{u_{i}} \cdot \prod_{t_{i}: x_{i}=0, y_{i}=1} \frac{1-p_{i}}{1-u_{i}}
$$
*spostando dalla parte destra alla sinistra*:
$$
O(R|v_{d},v_{q})=_{\text{rank}} \prod_{t_{i}: x_{i}=y_{i}=1} \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})} \cdot \prod_{t_{i}: y_{i}=1} \frac{1-p_{i}}{1-u_{i}}
$$
* **che succ?** togliere $x_{i}=0$ nella seconda produttoria, vuol dire che conto tutte le $x_{i}$ che hanno $y_{i}=1$.
* **se tolgo $x_{i=0}$ devo dividere la produttoria per la parte in piu, in modo da annullarla**
* ossia devo dividere la formula per $\frac{1-p_{i}}{1-u_{i}}$ per tutti le $t_{i}: x_{i}=1, y_{i}=1$
* **equivale a moltiplicare per $\frac{1-u_{i}}{1-p_{i}}$ e lo posso accorpare nella prima produttoria.** che ha come iteratore  $t_{i}: x_{i}=1, y_{i}=1$

*la parte destra e' costante per tutti i documenti rispetto alla query* $q$ (poiché ha come iteratore $t_{i}: y_{i} =1$), ed ai fini del ranking si puo' ignorare.
$$
O(R|v_{d},v_{q}) =_{rank} \prod_{t_{i}:x_{i}=y_{i}} \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})}
$$
**posso finalmente definire il Retrieval Status Value (RSV$_{d}$)**:
* prendo $O(R|v_{d}, v_{q})$ e ne faccio il logaritmo.

$$
RSV_{d} = \sum_{t_{i}:x_{i}=y_{i}=1} \log \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})} = \sum_{t_{i}:x_{i}=y_{i}=1} c_{i}
$$

*l'input del logaritmo puo' essere visto come il peso del termine nell'RSV*, lo chiamiamo $c_{i}$ e si comporta come odds:
$$
c_{i} = \log \frac{p_{i}(1-u_{i})}{u_{i}(1-p_{i})} = \log \frac{p_{i}}{1-p_{i}} - \log \frac{u_{i}}{1-u_{i}}
$$
- $( c_i > 0 ):$ il termine è più tipico dei documenti rilevanti;
- $( c_i = 0 ):$ il termine non distingue rilevanti e non rilevanti;
- $( c_i < 0 )$: il termine è più tipico dei documenti non rilevanti. 
- Quindi $c_{i}$ misura quanto un termine aiuta a distinguere documenti rilevanti da documenti non rilevanti. 

**$p_{i}$ e $u_{i}$ rispettivamente con feedback di rilevanza o senza valgono**:
$$p_i=\frac{r_i}{R}$$ $$u_i=\frac{df_i-r_i}{N-R}$$ con

- ($N$): numero totale di documenti nella collezione;
- ($R$): numero di documenti rilevanti;
- ($r_i$): numero di documenti rilevanti che contengono il termine ($t_i$);
- ($df_i$): numero totale di documenti che contengono ($t_i$). 
- **senza conoscere $r_i$ e $R$ allora approssimiamo** questi calcoli assumendo che i documenti rilevanti siano decisamente inferiori della collezione totale quindi:
$$u_i \approx \frac{df_i}{N}; p_i=0.5$$

con queste assunzioni $RSV_{d}$
$$
RSV_{d} = \sum_{t_{i}: x_{i} = y_{i}=1} \log \frac{N}{\text{df}_{t_{i}}}
$$

**osservazione**: BIM e VSM sono simili ma usano pesi diversi. possiamo usare le stesse strutture dati per implementare entrambi. ma quali informazioni usiamo?
* BIM e' usato per titoli ed abstract, non usa term frequency o inverse document frequency ed usa rilevanza binaria
* non e' dunque adatto per documenti troppo enormi.

