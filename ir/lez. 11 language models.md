**BM25 e language models**:
* **BM25**: $p(R | d,q) = \text{ quanto e' rilevante } d \text{ rispetto a } q$
* **Language Models**: $p(q|M_{d}) = \text{quanto e' probabile che } q \text{ sia stato generato dal modello } M_{d}$?
* **differenza**: entrambi hanno un'approccio probabilistico. Ma usano idee diverse.

**document language model**: $M_{d}$ e' il modello  probabilistico del documento $d$.
* $M_{d}$ cambia da documento a documento
* **attenzione**: non intendiamo che $M_{d}$  (dunque il documento) generi letteralmente la query. e' un'assunzione per modellare il problema.

**modello generativo**: ogni documento e' una base per un modello generativo che genera la query.
* che modello vogliamo usare? con che parametri?

**come si usa**?
1. arriva la query
2. ottengo documenti candidati
3. per ogni documento ho un modello generativo per misurarlo su una query.

**cos'e' un modello generativo**?
* **genera sequenze di termini**, uno per volta.
* $M_{d}$ associato a $d$, assegna una probabilità al **prossimo termine** generato.
* **finite state automata**: le transizioni sono i termini generati.

**Da cosa dipendono le probabilita**?
* **in generale da una storia**: $p(w_{i}| w_{1},\dots,w_{i-1})$
* **assunzione**: $p(w_{i}| w_{1},\dots,w_{i-1},M_{d}) = p(w_{i}|M_{d})$, ossia la probabilità di generare una parola dipende soltanto da quello che mi dice il modello, non mi interessa guardare l'intera frase.

**Modello come distribuzione di probabilita sui termini**: $$M_{d} = \{ p(t|M_{d}): t\in V \}$$
**automi probabilistici**: sono gli automi che generano le query. una certa transizione viene presa con una certa probabilita.
![[Pasted image 20260507120455.png]]

**bagof words e modello unigram**: considero automi **con un solo stato**, dunque $p(t|s) = p(t)$ per ogni termine.
![[Pasted image 20260507120716.png]]

**probabilistic state automation (??)**: per astrarre le generazione di linguaggi, probabilistici (??)

**prodotto**: $p(q|M_{d})$ e' il prodotto delle probabilita dei termini in $q$ secondo il modello $M_{d}$
* attenzione! si passera poi ovviamente a somme dei logaritmi.

**ranking**: viene fatto applicando bayes e approssimando come detto prima. La formula di partenza e':
$$
p(d|q) = \frac{p(q|d)p(d)}{p(q)}
$$
dove approssimiamo: $$
p(q|d) \approx p(q|M_{d})
$$
ed ai fini del rank, $p(q)$ e' una costante su tutti i documenti, dunque  si elimina:
$$
p(d|q) =_{\text{rank}} p(q|M_{d})p(d)
$$
## stimare le probabilita
**modello unigram independence** assumption:
$$
p(q|M_{d}) = p(<w_{1},\dots,w_{|q|}>|M_{d}) = \prod_{i=1}^{|q|} p(w_{i}|M_{d})
$$
* **query**: la vediamo come una bag di termini indipendenti gli uni dagli altri.
* **count**: devo tenere il conto di quante volte compare ogni termine! $tf_{t_{i}, q} = k_{i}$
* **in questo modello:** $p(t_{i}|M_{d}) = p_{i}$

**modello multinomiale**:
* mi chiedo qual'e' la probabilita di osservare $k$ occorrenze del termine $t$ nella query $q$.
$$
p(q|M_{d}) = \frac{|q|!}{\prod_{t\in V} tf_{t,q}!} \prod_{t\in V} p(t|M_{d})^{tf_{t,q}} =_{\text{rank}} \prod_{t \in V} p(t|M_{d})^{t_,q}
$$

$$
= \prod_{t: tf_{t,q}>0} p(t|M_{d})^{tf_{t,q}}
$$
* $|q|!$ e' comune a tutti i documenti ordinati sulla stessa query
* e non mi interessa nemmeno il denominatore
* **coefficiente multinomiale**: dipende solo dalla query.
* ottengo dunque una formula piu semplice come al solito

$M_{d}$ **nel modello multinomiale e' un vettore**: 
$$
M_{d} = [p(t_{1}|M_{d}),\dots,p(t_{|V||M_{d}})]
$$
* con $\sum p(t_{i} | M_{d}) =1$


**probabilita del termine nel documento**: 
$$
\hat p_{i} = \hat{p}(t_{i}|M_{d}) = \frac{tf_{t,d}}{|d|}
$$

**smoothing**: un termine con probabilità 0, porta il prodotto a 0. Applico lo **smoothing di laplace**. **Questo vuol dire che il nuovo conteggio totale dei termini conta ogni intermine una volta in piu!** quindi devo normalizzare le formule aggiungendo $|V|$
* **problema**: altero il peso del conteggio dei termini!!! 
$$
\sum_{t\in V} (tf_{t,d}+1) = |d| + |V|
$$
$$
p_{lap}(t|d) = \frac{tf_{t,d}+1}{|d|+|V|}
$$

**modello della collezione**: posso allo stesso modo stimare le probabilita guardando la collezione intera.
$$
\hat p(t|M_{c}) = \frac{cf_{t}}{T}
$$
* $cf_{t}$: occorrenze di $t$ nella collezione.
* $T$: e' il numero di termini $t$

**Jelinek-Mercer smoothing** sui termini:
$$
p_{JM}(t|d) = \lambda\frac{ tf_{t,d}}{|d|} + (1-\lambda)\frac{c f_{t}}{T}
$$
$$
p_{JM}(q|d) = \prod_{k=1}^{|q|} p_{JM}(w_{k}|d)
$$


* $\lambda$ e' un iperparametro, da stimare dunque tramite benchmark. serve a definire il peso rispetto alla collezione.
* $\lambda$ **alto** $\to$ ricerca di tipo congiuntivo, tende a ritornare i documenti contenenti le parole nella query
* $\lambda$ **basso** $\to$ ricerca di tipo disgiuntivo, performa bene su query lunghe.

> [!warning] esercizio scemo

> [!warning] esercizio esame

## dirichelet
**problema di jelinek**: non tiene conto della lunghezza del documento. 
* **goal** combinazione delle evidenze del documento e della collezione, ma deve dipendere dalla lunghezza!!@#!$

**pseudotoken**: immagino di concatenare un'altro documento che e' l'unione di tutte le parole del dizionario, dunque i termini hanno sicuramente la distribuzione di $M_{c}$.
* **smoothing di dirichlet**: uso un peso $\mu$ arbitrario.
* **token virtuale**: con $\mu$ aggiungo token virtuali al conteggio.
* **a che serve dirichlet**: aggiungo al documento da sortare uno pseudo-documento di lungheza $\mu$ i cui termini sono distribuiti secondo il modello del documento.

$$
\mu p(t|M_{c}) = \frac{\mu cf_{t}}{T}
$$
**combina la term frequency con lo smoothing**:
$$
tf_{t,d} + \mu p(t|M_{c})
$$

**normalizzo con il totale**!
$$
p_{Dir}(t_{i}|d) = \frac{tf_{t_{i},d} + \mu p(t_{i}|M_{c})}{\sum_{t_{k} \in V}(\textcolor{red}{tf_{t_{k},d}} + \textcolor{blue}{\mu p(t_{k}|M_{c})})}
$$
**nota** in $M_{c}$ la somma delle sue probabilita e' 1:
$$
\sum_{k} \textcolor{blue}{\mu p(t_{k}|M_{c})} = \mu \sum_{k}p (t_{k}| M_{c}) = \mu
$$
**mentre**: 
$$
\sum_{t_{k} \in V} \textcolor{red}{tf_{t_k,d}}
 = |d|$$
**dunque**:
$$
p_{Dir}(t_{i}|d) = \frac{tf_{t,d} + \mu p(t|M_{c})}{\textcolor{red}{|d|}+\textcolor{blue}{\mu}}
$$

#### interpolazione
$$
p_{Dir}(t|d) = \textcolor{red}{\frac{tf_{t,d}}{|d|+\mu}} + \frac{\mu}{|d| + \mu} p (t |M_{c})
$$
$$
\textcolor{red}{\frac{tf_{t,d}}{|d|+\mu}} = \frac{|d|}{|d|+\mu} \textcolor{blue}{\frac{tf_{t,d}}{|d|}}
$$
$$
\hat{p}(t|M_{d}) = \textcolor{blue}{\frac{tf_{t,d}}{|d|}}
$$
$$
p_{Dir}(t|d) = \frac{|d|}{|d|+\mu} \hat{p}(t| M_{d}) + \frac{\mu}{|d| + \mu} \hat{p}(t|M_{c})
$$

$$
p_{\text{Dir}}(t|d) = \lambda_{d}\hat{p}(t|M_{d}) + (1-\lambda_{d})\hat{p}(t|M_{c})
$$
$$
\lambda_d = \frac{|d|}{|d| + \mu}
$$
**ossia dirchelet e' jelinek-mercer:** ma usa un $\lambda_{d}$ differente per ogni documento.
* $d$ **lungo** $\to \lambda_{d}$ **e' grande**: ci fidiamo di piu del modello del documento.
* $d$ **corto** $\to$ $\lambda_{d}$ **e' piccolo**: ci fidiamo di piu della collezione
* $\mu$ **aumenta** $\to$ **c'e' piu smoothing verso la collezione**.
* $\mu$: viene fatto il tuning sulla collezione.

## usare dirichlet per retrieval
$$
p_{Dir}(q|d) = \prod_{k=1}^np_{Dir}(w_{k}|d)
$$
$$
p_{Dir}(w_{k}|d) = \frac{tf_{w_{k},d} + \mu p(w_{k}|M_{c})}{|d| + \mu}
$$
$$
\log p_{Dir}(q|d) = \sum_{k=1}^n \log \frac{tf_{w_{k},d} + \mu p(w_{k}|M_{c})}{|d| + \mu}
$$

* **jelinek-mercer**: si usa per query verbose
* **dirichlet**: fa interpolazione sulla lunghezza del documento, funziona meglio per query con parole chiave.

**[ESERCITAZIONE] Perche' dirichlet pesa correttamente parole frequenti come** `the`?

Nel caso di Dirichlet smoothing:

$$

p_{\mathrm{Dir}}(t \mid d)

=

\frac{tf_{t,d}+\mu p(t \mid C)}

{|d|+\mu}

$$
dove:
- $tf_{t,d}$ è il numero di occorrenze di $t$ nel documento $d$;
- $p(t\mid C)$ è la probabilità del termine nella collezione;
- $\mu$ controlla la forza dello smoothing.

Riscriviamo la formula mettendo in evidenza il contributo del background:
$$

p_{\mathrm{Dir}}(t \mid d)

=

\frac{\mu p(t\mid C)}{|d|+\mu}

\left(

1+

\frac{tf_{t,d}}{\mu p(t\mid C)}

\right)

$$
Passando ai logaritmi:
$$

\log p_{\mathrm{Dir}}(t \mid d)

=

\log

\frac{\mu p(t\mid C)}{|d|+\mu}

+

\log

\left(

1+

\frac{tf_{t,d}}{\mu p(t\mid C)}

\right)

$$

Il secondo termine:

$$

\log

\left(

1+

\frac{tf_{t,d}}{\mu p(t\mid C)}

\right)

$$


* **RISPOSTA**: il fattore $\mu p(t|C)$ pesa il contributo di $\text{tf}_{t,d}$ dividendolo

Quindi il ranking non dipende solo dai termini presenti nel documento.
Dipende da due effetti:
1. un termine raro dà un guadagno maggiore quando compare nel documento;
2. il denominatore |d|+μ introduce una normalizzazione legata alla lunghezza del documento.

In sintesi:
- i termini comuni hanno probabilità alta nel background, quindi aggiungono poca evidenza specifica;
- i termini rari hanno probabilità bassa nel background, quindi quando compaiono nel documento sono più informativi;
- Dirichlet smoothing introduce anche una normalizzazione rispetto alla lunghezza del documento.

Per questo motivo, nei Language Model non serve necessariamente un IDF esplicito: parte del comportamento dell'IDF emerge dal confronto tra documento e collezione.
# pro e contro
con i language model lo score più alto potrebbe essere negativo dovuto al fatto che utilizziamo il logaritmo e tra 0 e 1 il logaritmo vale valori negativi cerchiamo un valore vicino allo 0 comunque invece con BM25 otteniamo sempre valori positivi

- i language model hanno idf non esplicita ma tramite la collection frequency otteniamo un risultato simile, invece BM25 la ha in modo esplicito
- con BM25 riusciamo ad avere più controllo dei fenomeni grazie ai parametri di saturazione e di normalizzazione $k_1$ e $B$