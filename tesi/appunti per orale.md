**Linux Gateway**: e' un dispositivo di rete, tipicamente uno switch L3, che instrada il traffico dalla rete locale alle reti esterne.

Rete verify $k$:
* **Perche' non esiste l'overlapping degli indirizzi ip in verifica**? Perche il logical switch ed il logical router non esistono nel kernel, sono solo un'astrazione. Il Bridge Open vSwitch invece esiste lato kernel ed esegue la topologia logica per determinare le regole OpenFlow, senza coinvolgere lo stack TCP/IP dell'host. Prima di raggiungere `incusbr0` lo SNAT traduce gli IP sorgenti per evitare conflitti.

* **Perche dall'esterno non posso instradare verso la rete OVN**? Non esistono rotte per instradare qui container senza indirizzare a br-team-k
* Chi gestisce le regole per il NAT? ovn ed Incus.