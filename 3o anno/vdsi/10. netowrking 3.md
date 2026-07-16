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
## OS fingerprinting process -O
**Test**: il processo e' suddiviso in 7 test. A questi segue il test della porta chiusa **UDP**.

![[Pasted image 20260511221605.png]]
**TEST TCP**: sono 6 e i risultanti `SYN/ACK` sono usati per:
* **initial values**: comparare i valori di sequenza iniziali.
* **ip values**: comparare i valori di identificazioni ip
* **timestamp**: comparare i timestamp TCP

**esatta versione dell'os**: in alcuni casi azzecco la versione del sistema operativo!

**svantaggi di `-O`**: 
* **root**: `nmap`  ha bisogno di scrivere i byte direttamente sulla scheda di rete, o comunque sui layer di rete molto bassi.
* **perche devo bypassare il sistema operativo**? solo in questo modo posso generare frame strani con le flag `SYN, FIN, PSH, URG` accese allo stesso tempo.
* **attenzione**: queste flag accese insieme contemporaneamente sono inusuali, dunque uno stronzo potrebbe sgamarmi.

**quando e' accurato**? deve esserci almeno 1 porta aperta ed 1 una chiusa, entrambe di tipo TCP.

gemini cosa e' un ISN graph?

# host discovery con nmap
**host discovery** tramite `ping` si fa con:
```bash
nmap -sn <target_network>
```

**arp scan**: anche questo e' supportato insieme ad altre tecniche.

## NMAP Scripting Engine
**dove si trovano gli script?** `/usr/share/nmap/scripts`

**a che servono**? banalmente, estendono le funzionalita di `nmap`.
* **information gathering**: enumerazione servizi, enumerazione vulnerabilita, ecc...

**default**: l'esempio esegue script di default
```bash
nmap -sC <target>
```

**script specifico**:
```bash
nmap --script=<script-name> <taraget>
```

**categoria di script**:
```bash
nmap --script=<script-category> <target>
```
* **default**
* **safe**
* **intrusive**
* **not intrusive**

**come scrivo il mio script**?
* **linguaggio**: lua
* **prototipo**: la funzione accetta in input host e porte identificate in fase di scanning e ritorna un'output generico.

## SMB
* **SMB**: server message block, permette di condividere file, stampanti e porte seriali. Si attacca facilmente, fa schifo!
* **porte SMB**: 139, 445 in TCP, e altre UDP

**comandi**:
* `nmap -v -p 139,445 -oG smb.txt <ip range>`: gemini che fa?
* `nbtscan -r <subnet o ip address>`: gemini che fa?

**nmap**:
```bash
nmap -p445,139 --script=smb-os-discovery <ipaddr>
```

**cosa ottengo in output**? il sistema operativo che sta eseguendo il server smb.

## `SMPT`

* **telnet**: uso telnet per connettermi al server
* `VRFY`: chiedo di verificare l'esistenza di un'utente
* `EXPN`: chiedo al server se l'utente appartiene ad una maling list.