**radio basics**:
* $\lambda$: lunghezza d'onda
*  $\frac{c}{\lambda}$: frequenza, con $c = \text{velocita' della luce}$  
* **direzione**: di propagazione
* **ampiezza**: che varia nel tempo
![[Pasted image 20260526005653.png]]
Un'onda e':
* campo magnetico
* campo elettrico

**spettro radio**: e l'insieme finito di frequenze allocate per le comunicazioni wireless. E' gestito dalla nazione in cui mi trovo.
* **sotto licenza**: uso dedicato per qualcuno, od un gruppo di persone.
* condiviso: e' una banda condivisa tra tante persone
* non licenzata: aperta, possono trasmettere tutti.

![[Pasted image 20260526010812.png]]
**qui e' descritto il meccanismo con cui**: prendo l'informazione e la trasformo in frequenze piu alte che la mia antenna puo' trasmettere

**segnale in banda base**: $A(t)$, ossia il segnale originale che contiene l'informazione che vuoi trasmettere.
* **di cosa e' fatto**? e' un'onda centrata attorno allo zero

**oscillatore**: $\cos(2 \pi f_{c} t)$ e' l'onda generata nel tempo $t$ dall'oscillatore usando la frequenza $f_{c}$
* **carrier frequency**: e' la frequenza portante.
* $A(t) \cos(2\pi f_{c}t)$: e' il segnale risultate dalla moltiplicazione della banda base con l'oscillatore, ora posso trasmettere.

PSD (Power Spectral Density):
* **risponde alla domanda**: come e' distribuita la potenza del segnale su ogni frequenza?
* **banda passante**: questo tipo di segnale e' centrato in $f=0$, e se ha banda $W$, la sua occupazione spettrale va da $-\frac{W}{2}$ a $\frac{W}{2}$
* **cosa succede quando applico la moltiplicazione**? si divide il segnale in ampiezza e si centra in $+f_{c}$ ed in $- f_{c}$ (accade per trasformata di fourier)

**Ricevitore**: l'operazione descritta nell'imagine prende il nome di **demodulazione coerente**
![[Pasted image 20260526084458.png]]
* moltiplicare di nuovo per la portante equivale ad ottenere la banda base.

$$
\cos^2 (\Theta) = \frac{1+\cos(2 \Theta)}{2}
$$

In:
$$
\frac{A(t)}{2}[1+\cos(2 \pi 2 f_{c} t)]
$$
ho due parti, sviluppando il prodotto:
* il primo termine, ossia $\frac{A(t)}{2}$ e' il segnale originale, dimezzato in ampiezza, ed e' centrato in 0.
* il secondo termine e' una copia del segnale a frequenza $2f_{c}$, il doppio dell'originale.

**low-pass filter**: server per filtrare la parte del segnale che non mi serve, ossia il secondo termine.

![[Pasted image 20260526085011.png]]

**Segnale radio**:
* **potenza**: e' l'energia di ricezione/trasmissione per unita di tempo
	* **lineare**: si misura in watt, o milliwatt
	* **logaritmica**: si misura in decibel. 
$$
P_{dBm} = 10 \log_{10} \frac{P_{mW}}{1mW}
$$
* **larghezza di banda**: si misura in Hz di range di frequenze usate
* **codifica**: devo aggiungere ai bit un meccanismo di error correction o detection
* **digital modulation**: devo modulare i bit in modo da massimizzare la trasmissione affidabile e da codificare i bit nel segnale portante. Lo faccio cambiano ampiezza o frequenza o fase della portante
![[Pasted image 20260526085648.png]]![[Pasted image 20260526085924.png]]![[Pasted image 20260526085956.png]]
* **IQ: In-phase and Quadrature**
* **a che serve**? scompongo il segnale ricevuto in due segnali piu semplici da leggere

**per esempio**:
$$
s(t) = A(t) \cdot \cos[2 \pi f_{c}t+ \varphi(t)
]$$
* $A(t)$: ampiezza che varia nel tempo del segnale
* $f_{c}$: portante fissa
* $\varphi(t)$: fase che varia nel tempo.

**matematicamente derivo da $s(t)$, i segnali $I(t)$ e $Q(t)$:**
$$
s(t) = \underbrace {A(t) \cos[\varphi(t)]}_{I(t)} \cdot \cos(2 \pi f_{c}t) - \underbrace {A(t) \sin[\varphi(t)]}_{Q(t)} \cdot \sin(2 \pi f_{c}t)
$$
* $I(t)$: in fase, e' l'ampiezza del coseno
* $Q(t)$: in quadratura, e' l'ampiezza del seno

**Diagramma a costellazione**:
![[Pasted image 20260526091003.png]]
* **la rotazione** determina la fase
* **la distanza dal centro** determina l'ampiezza
* **in qpsk**: ho 4 segnali ad ampiezza identica, ma fasi differenti

**Teorema campionamento**: devo campionare 2 volte la frequenza massima registrabile.


... tante slide..  34-49

**SNR**:
$$
\text{SNR}(dB) = 10 \log_{10}\left( \frac{\text{received signal power}}{\text{noise power}} \right)
$$
* se $\text{SNR} = 0$, allora rumore e segnale sono uguali
* se $\text{SNR}$ alto, allora e' facile estrarre il segnale dal rumore
* se $\text{SNR}$ basso, allora e' difficile estrarre il segnale dal rumore

**Shannon capacity**: e' il tasso massimo al quale data la larghezza di banda $B$ e l'$\text{SNR}$, posso trasmettere.
$$
C = B \log_{2}\left( 1+ \frac{\text{received signal power}}{\text{noise power}} \right)
$$
* $C$ cresce linearmente in $B$ con $\text{SNR}$ costante
* $\text{SNR}$ alto: allora $C$ cresce come un logaritmo.
![[Pasted image 20260526094610.png]]
![[Pasted image 20260526094718.png]]

## MATLAB
**spectrum analyzer**: mostra un segnale nel dominio della frequenza, fa vedere come e' distribuito il segnale sulle frequenze
* **oscilloscopio**: mostra un segnale nel dominio del tempo
**span**: 
**RBW**: determina la risoluzione della frequenza nel misuramento.
* **piccolo**: poso distinguere picchi di frequenza molto vicini tra loro
* **grande**: elaborazione piu rapida, ma i dettagli vengono persi
**Istantaneous Bandwidth**: porzione di spettro massima che il sistema cattura ed elabora simultaneamente.
* **sweeping** certe frequenze non entrano in banda, allora devo sintonizzarmi su un'altra frequenza.

![[Pasted image 20260526100037.png]]
* **channel power**: e' l'integrale di tutta la potenza contenuta all'interno della banda del canale analizzato
* **OBW 99%**: ossia considero solo la parte del segnale significativa che racchiude il 99% del segnale. lascio lo 0.5% a sinistra e a destra.
* **Frequency Error:** Calcola il centro geometrico dell'OBW e lo confronta con la frequenza portante ideale che avevi impostato. Serve a capire se l'oscillatore hardware del trasmettitore è impreciso e sta trasmettendo leggermente "spostato" rispetto alla frequenza che dovrebbe usare.

**ACPR (Adjacent Channel Power Ratio)**: quanto il mio segnale sta disturbando i canali dei miei vicini?
* **perche**? a causa di filtri non perfetti, o distorsioni genero rumore sugli **Adjacent Channels** (i primi a sinistra e a destra) e sugli **alternate channels** (quelli piu esterni).

$$
\text{ACPR}(dBc) = 10 \cdot \log_{10}\left( \frac{P_\text{adj}}{P_{\text{ref}}} \right)
$$
* $P_{\text{ref}}$: potenza totale misurata nel canale principale
* $P_{\text{adj}}$: potenza dispersa nel canale adiacente.
