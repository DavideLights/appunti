# domande
![[Pasted image 20260617150927.png]]
## Domanda 2.1
![[Pasted image 20260518172724.png]]

**la media**: $-0.000414638830\dots$ e' la potenza media del segnale in output dall'Ideal Rectangular pulse filter block. 
**RMS**: matlab riporta $\text{RMS}=1$,dunque $P=1^2=1$
## Domanda 2.2

![[Pasted image 20260617213440.png]]
**primo grafico, rectangular pulse filter**: i numeri generati casualmente vengono convertito in un segnale rettangolare. La porzione del segnale pari ad 1 in ampiezza indica la trasmissione di un bit accesso, e viceversa per ampiezza pari a -1.

**secondo grafico, awgn channel**: viene introdotto del rumore, sul segnale originale.

**terzo grafico, integrate and dump**: vediamo la ricostruzione del segnale originale attraverso il campionamento del segnale in output dall'awgn channel. Bene o male i segni delle ampiezza tra primo e terzo grafico corrispondono, nonostante il rumore di fondo inserito artificialmente.

![[Pasted image 20260617150947.png]]

## Domanda 2.3
$\text{Eb/No} = 12\text{dB}$:
![[Pasted image 20260617214648.png]]
$\text{Eb/No} = 6\text{dB}$:
![[Pasted image 20260617214730.png]]
$\text{Eb/No} = 0\text{dB}$:
![[Pasted image 20260617214816.png]]

Il parametro $\text{Eb/No}$ misura **il rapporto segnale-rumore normalizzato per singolo bit**.
* $\text{No}$ e' la potenza del rumore di fondo. 
* **Se questo parametro tende a 0**, allora il rumore di fondoe' piu forte del segnale originale.
* Di conseguenza: **il diagramma ad occhio si fa sempre piu stretto**, poiche' e' difficile distinguere un tipo di simbolo dall'altro.

## Domanda 2.4
Come ci si aspetterebbe secondo quanto detto in **2.3**, l'error rate diminuisce all'aumentare di $\text{Eb/No}$. Inoltre l'error rate e' molto basso ($0.07835$) per $\text{Eb/No} = 0$ 

## Esperimenti guidati
![[Pasted image 20260617151028.png]]
**DSSS BPSK**: con questo sistema di trasmissione, ogni singolo bit, codificato con bpsk viene moltiplicato per una sequenza detta **chips** di lunghezza arbitraria. Dunque, quando voglio trasmettere un bit 1 trasmetto l'intera sequenza di chips, se trasmetto -1 trasmetto la sequenza chips invertita.

1. **D1**) In ogni bit originale che volevo trasmettere, ci entrano 20 simboli della sequenza di chipping. Pero noto che la sequenza di chipping contiene solo 16 simboli ![[Pasted image 20260617230110.png]]
2. **D3**) Nonostante il rumore, si riesce a riconoscere il segnale originale
![[Pasted image 20260617230005.png]]


![[Pasted image 20260617151053.png]]
* **D1) Check the Standard BPSK Dots**: 
* ![[Pasted image 20260617235002.png]]
* **D2) Check the DSSS Dots Before and After**: la prima immagine mostra la costellazione per `var=.05`, la seconda per `var=1`
![[Pasted image 20260617230958.png]]
![[Pasted image 20260617231128.png]]
![[Pasted image 20260617235445.png]]
![[Pasted image 20260617235403.png]]
**lato trasmettitore**:
* **D1)** la banda si e' allargata da $-500 \text{Hz}$ a $500\text{Hz}$, rispetto ai $-100, 100$ originali.
* **D2)** inoltre il prodotto ha fatto abbassare il picco (ossia onda blu rispetto alla gialla)
![[Pasted image 20260618000650.png]]

**lato ricevente**: 
* **D3)** il segnale giallo viene trasformato in quello blu
* **D4)** un picco di un jammer riceve lo stesso trattamento del segnale legittimo, ossia viene spalmato su tutta la larghezza di banda.
