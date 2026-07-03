**se comprimo** le postings:
* uso meno spazio in RAM e su DISCO
* meno tempo per leggere
* meno tempo per scrivere

Leggenda:
* **Set di documenti**: *Reuters-RCV1*
* $\Delta \%$ e' la riduzione in grandezza rispetto alla riga precedente.
* $\text{cumul} \%$ e' la riduzione in grandezza rispetto alla riga `unfiltered`
![[Pasted image 20260320115157.png]]
* **provo a togliere i numeri nella seconda riga**: riduce di poco la grandezza del dizionario, ma di molto gli indici
* **case folding**: accorpa parole che differiscono per maiuscole e minuscole. riduco del $17 \%$ la **grandezza del dizionario**.
* **(D) togliere 30 o 150 stopword**: **cambia poco il dizionario**.
	* **perche**: se tolgo 30/150 parole dal dizionario che rappresenta reuters (migliaia di termini) cambia poco.
* **(D)** **case folding e stemming: non cambiano la grandezza del positional index**
	* **perche**: se accorpo termini diversi in una posting, devo comunque tracciarne la loro posizione.
* **stemming**: tolgo le desinenze, i plurali ricondotti alla desinenza, riduco di un'altro $17\%$ la **grandezza del dizionario**.

**osservazioni**:
* **i numeri usati nei documenti sono generalmente pochi**, ma sono usati molte volte in Reuters, dunque ho una riduzione dell'$8 \%$.
* **case folding**: non risparmio molto, non sono parole molto frequenti.
* **rimuovere 150 stopword**: risparmio del $30\%$, sul positional index fino al $47\%$. Queste sono molto frequenti, dunque ho molto risparmio.
* **stemming**: nel dizionario ottimizzo, ma nel positional index d devo comunque ricordare dove compaiono le parole, non cambia niente.

**Nota**: in reuters ci sono poche parole che hanno alta frequenza, e tante parole con bassa frequenza. (???)

**compressione**:
* **lossy**: queste tecniche per diminuire la grandezza delle strutture dati perdono dati. Non posso ricostruire i documenti originari.
	* **OSS**: il preprocessing puo' essere visto come una compressione lossy dei dati.
* **lossless**: comprimo senza perdere dati

## heaps law
**Heaps**: la grandezza del dizionario segue il numero di token nella collezione. **E' una legge empirica**.
* **a che serve?** stimare il numero di parole nel dizionario.
* **quando funziona bene heaps**? se $T>100.000$
* $M := \text{grandezza vocabolario}$
* $T := \text{numero di token}$
* $30 \leq k \leq 500$ e $b \sim 0.5$
$$
M = kT^b \to_{\log} \log M = \log k + b \log T
$$

**logaritmo**: se andiamo a guardare il logaritmo di heaps, otteniamo la formula di una retta.
* Heaps in logaritmo, approssima bene 

**Heaps come cresce**? per documenti grandi Heaps approssima molto bene.

> [!error] Fare esercizio su heaps per esame
> 
![[Pasted image 20260702133127.png]]
## Zipf's law
* si applica quando **ho pochi fenomeni rappresentativi** e tanti **in coda, che non contano nulla**.
* **La $i^{th}$ parola piu frequente ha frequenza proporzionale ha $\frac{1}{i^{th}}$.**
* **equivalente** ad $cf_{i}= c i^k$, dove per $k=-1$ allora $cf_{i}=\frac{c}{i}$
* **logaritmo**: $\log \text{cf}_{i} = \log c - \log i$
	* ossia ho una **relazione lineare** tra $\log \text{cf}_{i} \text{ ed } \log i$
* **OSS**: si vede bene con le stopwords, infatti rimuovendole dimezzo le postings.

**conseguenza**:
* **sia la prima piu frequente**: `the` (priam piu frequente) con frequenza $\text{cf}_{1}$ ed occupa il $7 \%$ della collezione
* **sia la seconda** `of`: $\text{cf}_{2}=\frac{\text{cf}_{1}}{2}$. allora `of` occupa in proporzione circa il $3.5\%$ 
* **allora** $\text{cf}_{3} = \frac{\text{cf}_{1}}{3}$ e cosi via...

**gemini**: e quindi a che serve sto zip?

## Compressione del dizionario
**perche' comprimere il dizionario?** perche' e' grande, sta in memoria, e voglio leggerlo velocemente. 
* **dispositivi embedded**: poca memoria!

**assunzione**: usiamo **un'albero binario di ricerca** per i termini.

![[Pasted image 20260702142703.png]]
**28 byte per ogni termine**: 
* **20 byte**: il termine 
	* **problema**: non li uso tutti
* **4 byte**: frequenza
* **4 byte**: puntatore

**problema**: spreco memoria
**soluzione**: una stringa lunga con tutti i termini concatenati. Il dizionario e' fatto cosi:
* **freq**: frequenza del termine
* **postings ptr**: la sua posting list
* **string ptr**: ed il puntatore alla stringa.



![[Pasted image 20260702143115.png]]
* **dizionario**: e' una stringa composta dalla concatenazione di tutti i termini del dizionario

![[Pasted image 20260702143546.png]]
* **lunghezza del termine**: codifico all'interno della stringa la lunghezza del prossimo termine da leggere, cosi so quando fermarmi.
*  **struttura blocking**: non memorizzo tutti i puntatori. Ne tengo in memoria uno ogni $k$.
* $k$: ogni $k$ termini mi salvo il relativo puntatore sul dizionario, cosi non devo salvare il puntatore per tutti i termini.
* **problema**: piu risparmio con $k$ alto e piu e' la complessita nella ricerca della stringa.

**cosa migliora**?
* **puntatori al dizionario**: richiedono 22 bit, ossia $\log 3.2M = 22  \text{ bits} = 3 \text{bytes}$
* **osservazione**: le parola nella stringa sono ordinate, nel senso che parole vicine iniziano con una stessa sequenza di lettere.

> [!error] esercizi!
![[Pasted image 20260702144307.png]]

**front coding**:  molte parole condividono la stessa radice, allora... 
![[Pasted image 20260702144442.png]]
## compressione della posting
**compressione della posting**: devo tenere in memoria i $\text{docID}$ che su 800.000 documenti richiedono $\log_2 800.000 = 20$ bit
* **assunzione**: un posting e' un doc id.
* **posso usare meno di 20 bit?**

**termini probabili e poco probabili**:
* il termine `archnocentric` potrebbe occorrere una volta su un milione di documenti. allora mi va bene usare 20 bit per tenere in memoria quel documento
* il termine `the` occorre in tutti i documenti, non mi va bene usare 20 bit.

**bitmap vector**: **si usa quando** ho un termine denso, che compare spesso. Meglio rispetto a ricordare tutti i numeri di tutti i documenti in cui compare il termine. 

![[Pasted image 20260702145747.png]]
**delta o gap**: tengo in memoria il delta tra la posizione ed il numero precedente
* **perche funziona**? i `docID` sono incrementali
* **cosa spero**? che sia piu efficiente immagazzinare il gap rispetto al doc id. E' vero per parole molto frequenti,

## variable length encoding
**variable length encoding**: come memorizzo questi interi in memoria in modo consecutivo? ci sono varie tecniche
- **obiettivo**: utilizzare pochi bit se l'intero da memorizzare ne richiede pochi.
- **soluzione**: variable length encoding con **unary code**.

**unary code**: conto gli uni e poi metto uno 0
* e' una soluzione probabile
* ottimale se $P(n)=2^{-n}$
![[Pasted image 20260702150249.png]]

**gamma code**: vediamo come codificare `13`.
* **offset**: $13\to 1101 \to 101$. ogni numero binario inizia con 1, ottengo l'offset togliendo quell'uno.
* **length (unary):** mi devo ricordare che $101$ e' lungo 3, in unario e' $1110$
* dunque mischiando le due cose: $1110.101$. (length concatenato ad offset)
* **decodifica**: devo usare operazioni su bit!

**analisi di spazio**: $G$ viene codificato usando $2 \log G +1$ bit
* **offset**: $\log G$ bit
* **length**: $\log G + 1$ bit, il numero di uni che metto in unario e' logaritmico, a cui aggiungo il bit 0.
* **ottimale**: se $P(n) \approx \frac{1}{2n^2}$

**problema, allineamento su byte**: se il gammacode non e' allineato, allora calano le performance (devo leggere piu byte se il dato si trova a cavallo tra 2 byte)

**VB (Variable Byte) codes**:
* **obiettivo**: usare meno byte possibili. sia $G$ il gap value da codificare.
* **continuation bit** $c$: usa un bit di ogni byte per indicare se devo leggere altri byte.
* se $G \leq 127$: codifico usando 7 bit e imposto $c=1$
* se $G > 127$: codifica i 7 bit piu bassi e calcola nei successivi byte i bit rimanenti allo stesso modo.
	* **continuation bit**: l'ultimo byte ha $c=1$, gli altri hanno tutti $c=0$
* **come avviene la codifica**? scrivo i 7 bit usando la notazione binaria standard
* **tradeoff**: byte aligment consuma molto spazio se i gap sono piccoli.

![[Pasted image 20260702151818.png]]

**idee moderne usate oggi**: 
* **word aligned** a 32 o 64 bit
* codifica piu numeri in una botta sola
* introduci escape codes ed un max gap size

**google**: codifica 4 byte usandone 5-17 bytes
* **primo byte**: indica la lunghezza di ciascuno dei 4 byte usando 2 bit ciascuno.
* **pro**: decodifica del primo byte usando una *lookup table*