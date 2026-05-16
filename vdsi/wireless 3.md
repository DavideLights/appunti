
## recap wireless 2
**frequenza portante**: e' modellata come una sinusoide di cui posso modellare ampiezza, frequenza e fase

**PSD**: power spectral density

**banda passante**: e' la banda assegnata per la comunicazione (???)
* da banda base si passa alla passante attraverso la moltiplicazione per il coseno ad una certa frequenza.

**modulazione**: ad una coppia di simboli corrisponde un tipo di segnale
*  `QPSK`: codifica 4 simboli con 4 fasi
* modulazione con meno simboli ha prestazioni migliori, vuol dire che ho meno errori possibili.

**segnale e rumore**: 
* **SNR**: rapporto segnale rumore, ossia ampiezza del rumore rispetto al segnale.

**importante**: banda base e passate, e conversione di frequenza
## wireless 3
**spoofing**: attacco a livello fisico, l'attaccante trasmette un segnale radio che e' piu forte a quello del segnale da attaccare.
* chi riceve si sincronizza al segnale dell'attaccante, quello falso ignorando il segnale autentico piu debole.

### software defined radio
**data source**: sorgente
**source encoder**: aggiungi/rimuovi bit in base a come mi servono
**channel encoder**:
**symbol mod**: fino a qui operiamo a livello di bit
**d/a**: convertitore digitale analogico, passiamo  al segnale anale!
**rf chain**: catena radio frequenza, qui viene fatta la moltiplicazione col coseno.


**al contrario, nel ricevente:** la rf chain mi porta dalla banda portante a quella base attraverso il campionamento

> [!note] gemini: spiega il campionamento meglio
**campionamento**: devo spezzettare il segnale in campioni, devo avere un numero finito di oggetti da analizzare
> * **tempo di campionamento**: quanti campioni prendo ogni secondo???

**a che tempo**? devo avere una frequenza che mi permette di recuperare i picchi della sinusoide. Il teorema del campionamento dice che:
$$
f_{\text{sample}} > 2 B
$$
* $B = \text{banda del segnale}$


**front-end analogico**: parte piu' esterna dell'antenna.
* oscillatore: sposta dalla frequenza portante alla banda base

**front-end digitale**: 

**cosa c'e' nella RF**? architetture Zero Intermediate Frequency, cerca di ridurre i passaggi tra i cambi di frequenze. $I$ e $Q$ sono le due componenti della mia onda, dunque un'onda si puo' sempre scomporre.
* $I = \text{in fase}$
* $Q = \text{quadratura}$

**software defined radio**: cerca di processare il segnale dalla radio frequenza in un solo step.
* tutto cio che avviene dopo la conversione in radio frequenza e' programmabile.
* dispositivo radio dove una o piu funzioni (demodulazione, conversione in frequenza, encoding) sono programmabili via software, ho flessibilita su tutte le operazioni hardware.

ho perso un po di slide

**slide sull'architettura della SDR**: ...


**modulazione fm**: modula la frequenza in base al segnale audio
* **demulatore**: dalla variazione delle frequenze ottiene il segnale audio!
* **sottocampionare**: devo campionare il segnale alla velocita del lettore


**pilot tone**: serve a sincronizzarsi, e' un picco ad una frequenza centrale


**che succ**? ogni radio trasmette ad una determinata frequenza. Frequency Division multiple acces
* dunque ogni stazione prende una fetta di frequenza
* tra una stazione e l'altra esiste una **guard band**, evita interferimenti tra stazioni
* nelle guard band c'e' solo rumore, il **noise floor**, un rumore randomico che e' attorno ad una costante (si comporta come rumore bianco)
* quando qualcuno trasmette emerge un segnale dal noise floor.

**potenza del segnale**: si misura come il picco nella trasmissione, e dipende chiaramente da cosa si sta trasmettendo
* **potenza del rumore**: devo ascoltare il noise floor e ottenere il picco minimo.

**banda**: nella banda assegnata alla trasmittente, la trasmissione avviene in una banda che emerge rispetto al noise floor

**come misurare la banda**: devo cercare dove inizia il segnale che si discosta significativamente dal rumore e dove questo finisce. La distanza tra questi due "tempi" indica la banda.

come misurare le frequenze centrali


## reporting!
number stations: websdr.