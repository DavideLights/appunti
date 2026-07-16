## BW e spacing
**Qual'e' la frequenza centrale della stazione?**
* Nel progetto la frequenza portante impostata e' $91.7 \text{MHz}$, ed il gain e' pari a $40$.
* Dunque la frequenza e' $91.7 \text{MHz}$

**Osserva lo spettro attorno alla stazione.**
**Qual'e' la larghezza di banda approssimativamente?**
![[Pasted image 20260526112219.png]]
* approssimativamente vale,: $\Delta \text{ kHz} = 49.3904 \text{ kHz}$
* e' stato calcolato posizionando i due cursori dello span.

**Identifica due stazioni FM vicine.**
**Qual'e' lo spacing tra le due stazioni?** in base agli screenshot che ho a disposizione non riesco ad individuarlo.
## OBW: non visto

## RBW: non visto

## Noise Level
**Stimare l'average noise level**:
![[Pasted image 20260526114452.png]]**Il noise level vale circa**: $0.506 \text{ dBm}$
## sampling frequency
**aprendo le impostazioni del ricevitore RTL-SDR**: la sampling frequency e' $240e3 \text{Hz}$.

**ipotizzando di ridurre la sampling frequency**: si ridurrebbe la banda catturata.

## Signal to noise ratio
siano:
* **noise level circa**: $0.506 \text{ dBm}$, l'ho preso posizionando i cursori sulla zona del rumore.
* **il segnale ha picco**: $32.8149 \text{ dBm}$, l'ho preso utilizzando il tool che rileva i picchi nel segnale.
* **allora**: $$\text{SNR} = 32.8149 - 0.506 = 32.3089 \text{ dB}$$
Il valore e' alto, questo vuol dire che e' facile estrarre il segnale dal rumore.
* se cresce la potenza del rumore l'SNR tenderebbe a 0
* se cresce la potenza del segnale l'SNR e' lontano positivamente da 0.
# Altri dettagli 
**picco a 0**: negli screenshot si nota un picco sullo 0. Questo dipende da errori hardware e non dovrebbe essere considerato.

**jamming**: applicando un jammer e' possibile aumentare il noise floor, se si aumenta abbastanza e' impossibile ricostruire il segnale trasmesso.
