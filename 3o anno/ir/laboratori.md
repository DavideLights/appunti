## laboratorio 1.1
**Bisogno informativo vs query**:
Un utente potrebbe avere questo bisogno informativo:
> “Voglio trovare un modo per catturare un topo senza ucciderlo.”

Ma potrebbe formulare la query come:
> `how to trap a mouse alive`

**tokenizzazione**: cioè nella suddivisione del testo in unità elementari chiamate **token**. 
- rimozione della punteggiatura
- gestione di apostrofi e forme contratte
- normalizzazione
- stemming o lemmatizzazione
- rimozione delle stopwords

**matrice sparsa**: La term-document matrix è molto utile dal punto di vista concettuale, ma non è adatta a collezioni grandi: nella pratica, quasi tutte le celle sono 0, quindi la matrice è molto **sparsa**.


**osservazione didattica**: Non c'è ancora nessun concetto di ranking.
- i documenti non vengono ordinati per importanza
- non esiste una nozione di "più rilevante" o "meno rilevante"
- il match è semplicemente **esatto**
- può essere troppo rigido
- non gestisce bene query vaghe o incomplete
- non ordina i risultati per utilità

**osservazione didattica**: spesso i termini con $df_{t_{i}}$ piu bassa sono quelli che nelle query booleane con un and restringono di molto il campo di ricerca.


```python
def intersect(postings1, postings2):
    """
    Restituisce l'intersezione tra due postings lists ordinate.
    """
    answer = []
    i = 0
    j = 0

    while i < len(postings1) and j < len(postings2):
        if postings1[i] == postings2[j]:
            answer.append(postings1[i])
            i += 1
            j += 1
        elif postings1[i] < postings2[j]:
            i += 1
        else:
            j += 1

    return answer
```

## laboratorio 1.2
**preprocessing**: nell'esempio vediamo una mail di richiesta di aiuto in merito a dei driver video. *Pero' insieme a questa informazione ci sono vari indirizzi email, numeri di telefono, mittente, destinatario che potrebbero non interessarci*. Dunque:
- rimozione dell’header
- conversione in minuscolo
- normalizzazione dei numeri
- rimozione della punteggiatura
- tokenizzazione
- rimozione delle stopwords
- rimozione di token troppo corti
- stemming

**stemming**: riduzione in radice!

**processare phrase queries ed term queries booleane**: tengo in memoria tutti e due i tipi di indici (posizionale e non)

## laboratorio 1.3
**query non valide**:
- `NOT graphic`
- `imag OR NOT graphic`
- `NOT "file format"`
- perche' non escludono documenti.
- **NOT**: voglio che si comporti come un'operatore di sottrazione, piuttosto che: "dammi tutto cio che non e' `X`".

## laboratorio 2

**bag of words model**: attenzione, le seguenti frasi in bag of words model sono molto simili.
- `john is quicker than mary`
- `mary is quicker than john`

Nel ranked retrieval è importante distinguere tra:
- **term frequency (tf)**: quante volte un termine compare in un documento
- **document frequency (df)**: in quanti documenti compare il termine

**peso logaritmico**: pesare la term frequency con il logaritmo e' utile perche
* se $tf_{t,d}$ passa da 1 a 2 occorrenze, allora il logaritmo cambia molto
* se $tf_{t,d}$ passa da 100 a 101 occorrenze, allora cambia poco.

**titolo e body**: conviene dare pesi diversi a parole nel titolo rispetto che nel body.


## laboratorio 3

In BM25 la crescita non e' lineare: 
* la prime occorrenze sono molto importanti
* ma dopo un po statura e lo score aumenta sempre di meno.
* passare da 10 occorrenze a 20, non raddoppia lo score, ma molto di meno.
* **oss**: la ripetizione dei termini puo' essere ridondante e non informativa.

**Length Normalization**: sia $B_{d}$ la normalizzazione della lunghezza con parametro $b=1$:
* se la lunghezza aumenta rispetto alla media, allora il denominatore in BIM25 e' piu grande.
* se il denominatore e' piu grande, il termine perde di importanza
* **perche**? evito di dare a importanza a documenti lunghi, solo perche' contengono piu parole!

![[Pasted image 20260714015821.png]]
A parita di $\text{tf}_{t,d}$:
* documenti corti hanno punteggio migliore
* documenti lunghi hanno punteggio minore
* **assunzione**: un documento lungo, statisticamente ha piu parole!

$k_{1}$:
* **valori piccoli**: saturazione rapida, vuol dire che dopo poche occorrenze le ripetizioni conatano poco
* **valori grandi**: saturazione lenta, vuol dire che dopo tanto occorrenze le ripetizioni contano di piu

$b$: se facciamo scorrere il parametro da 0 fino ad 1, notiamo che sono privilegiati i documenti piu corti nel ranking 


## language model
Il parametro $\mu$ controlla la forza dello smoothing:
* $\mu$ piccolo: il modello privilegia lo score del documento
* $\mu$ grande: il modello privilegia il comportamento nella collezione.