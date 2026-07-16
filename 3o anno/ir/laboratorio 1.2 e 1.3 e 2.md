# laboratorio 1.2
**20 newsgroup**: e' il dataset

**nltk**: prima libreria opensource per sta roba.
* `nltk.download` scarica il dizionario.

**ricerca in titolo e abstract**: voglio dare importanza a **parole che stanno nel titolo** più che nel contenuto della mail.

**dataset sporco**: contiene header, indirizzi email, metadata, ecc.... Devo adattarlo al mio sistema ir.
* rimozione dell’header
- conversione in minuscolo
- normalizzazione dei numeri
- rimozione della punteggiatura
- tokenizzazione
- **rimozione delle stopwords**
- rimozione di token troppo corti
- stemming

**catena di preprocess**: devo applicare la stessa catena sia a query che documenti. `preprocess` viene usata in entrambi i contesti.

> [!error] Mini esercizio
> 

**sorted delle posting lists**: nel codice e' inutile, le posting sono gia ordinate.

# laboratorio 1.3


# laboratorio 2
**vettore**: per ogni documento costruisco vettore con tf-idf