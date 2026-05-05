**contesto**: una volta identificata una rete, devo capire cosa ci gira sopra.

**network exploits**: si applicano quando conosco sistema operativo e applicazioni di rete in esecuzione sull'host da attaccare.

**active OS discovery**: manda vari pacchetti e analizza le risposte dell'host. I sistemi operativi piu comunemente usati rispondono con firme riconoscibili.

**passive OS discovery**: monitora il traffico e cerca pattern nella rete che sono caratteristici di un sistema operativo.
* **stealth**: osservo la rete e mando pochi pacchetti
* **ideale quando**: sono connesso direttamente alla rete da attaccare.

**os fingerprinting $\not\equiv$  port scan**: sono due attacchi diversi ma che usano processi e tecniche simili.
* `nmap` fa os finegprinting mandando una serie di **pacchetti specifici**.
* `TCP ACK` **su porta chiusa**: i sistemi operativi reagiscono differentemente ad un `ACK` su porta chiusa, dunque guardo la risposta!
* *queste differenze tra sistemi permettono ad nmap di creare un fingerprint del sistema operativo in base alla risposta.*

**gemini**: differenza tra os fingerprint e version detection scan (-sV)

**os fingerprinting operation**:
1. **ping e scan**: prima di iniziare con il fingerprinting dei sistemi operativi, **nmap fa uno scan normale** per determinare la disponibilita del sistema e categorizza le porte da sfruttare, identificando quelle chiuse.
2. **fingerprinting vero e proprio**:
	1. manda un **OS probe**
	2. **TCP handshakes**: misura `uptime`, predici le sequenze, ip identification sequence generation (gemini: che uvol dire sta roba???)
![[Pasted image 20260429122451.png]]

**sequenze**: posso provare a **predire** i numeri di sequenza TCP.
* **hikacking**: se so come si comportano i numeri di sequenza, l'attaccante puo' mascherarsi come uno dei due partecipanti alla comunicazione.