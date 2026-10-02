**Architettura**: macchina virtuale con all'interno incus e blueagent
* **vantaggi**: 
	* non devo esporre la socket di incus
	* figo e funzionale
* **svantaggi**: una challenge che richiede una macchina virtuale potrebbe essere difficile da generare e con prestazioni scadenti.

**Architettura alternativa**: vpn che gestisce le connessioni
* **forwarding pacchetti**: instrado pacchetti per i container nella macchina virtuale con incus, la macchina inoltra al container il pacchetto.

**Bridge L2 e MACVLAN**:
* **Bridge L2**: o Linux Bridge, agisce come uno switch di rete (L2)
	* crea coppie di interfacce virtuali **veth pair**, che collegano container con il bridge dell'host
	* **MAC learning**: esendo uno switch di rete, impara le associazioni tra MAC e IP.
	* interfaccia in modalita promiscua
	* **comunicazione host-container**: host e container possono comunicare tra di loro
	* **overhead**: rispetto a macvlan, lo stack veth usa code di scheduling, apprendimento e inoltro.
* **macvlan**: non e' uno switch, crea interfacce virtuali figlie che si agganciano all'interfaccia parent.
	* **MAC univoco**: ogni interfaccia ha il suo mac
	* **veth**: non esistono veth intermedie
	* **inoltro**: viene fatto guardando il MAC di destinazione.
	* **problema**: l'interfaccia parent non puo' comunicare con le sotto-interfacce
	* **overhead**: non c'e', e' molto piu semplice di Bridge L2

**Bridged Adapter per la vm**: per esporre la macchina virtuale alla rete.
* la macchina ottiene un ip dalla stessa rete del computer host

**Bridge L2 per i container**: anche se ha alto overhead, e' semplice da implementare e personalizzabile.

**oppure, macvlan per i container**: si puo' fare ma devo mettere blueagent su un container


## creare il bridge L2
> [!error] impostare i MAC address
> per qualche motivo da approfondire `eth0`  ed `br0` devono avere stesso mac address, altrimenti non si riesce ad instradare verso il router.
Il metodo più pulito e nativo per configurare un bridge L2 su Arch Linux è utilizzare `systemd-networkd`.
  
> [!error] Fondamentale: Ethernet vs Wi-Fi
Il bridging L2 standard **non funziona in modo affidabile su schede Wi-Fi** a causa delle limitazioni dell'intestazione 802.11 (che gestisce di norma 3 indirizzi MAC e rifiuta frame con MAC virtuali multipli senza WDS/4-address mode). Assicurati di usare un'interfaccia **cablata (Ethernet)** sull'host (es. `eth0` o `enp3s0`).

## incusbr0 vs br0
Abbiamo dovuto creare il nostro bridge `br0`, perche `incusbr0` e' una rete NAT:
* sottorete privata e isolata
* ha un suo dhcp server
* la rete esterna dunque non vede i container 

`br0` invece:
* usa `eth0` per creare uno switch di rete
* i container si collegano a `eth0`, dunque bypasso la rete nat predisposta da incus