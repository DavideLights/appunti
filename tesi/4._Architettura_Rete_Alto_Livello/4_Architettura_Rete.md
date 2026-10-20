La topologia di rete di Blue Agent è suddivisa logicamente in due reti:
* **Una rete di produzione per ogni team**, dove la rete $\text{production-}k$ identifica gli oggetti di rete ed i container necessari al team $k$. 
* **Al più una rete di verifica per ogni team**, dove la rete $\text{verify-}k$ identifica gli oggetti di rete ed i container duplicati utilizzati per la verifica richiesta dal team $k$.

Lo schema di indirizzamento prevede una netta separazione tra lo spazio di gioco del team $k$, la rete WireGuard e la rete di Incus:
* `10.k.0.0/24`: è la sottorete WireGuard per i membri del team $k$.
* `10.k.1.0/24`: è la sottorete LAN per i container di produzione e per i cloni di verifica.
* `172.16.0.0/24`: è la sottorete gestita da $\text{incusbr0}$ per fornire la connettività esterna e le reti OVN tramite NAT.

## 4.1 Rete $\text{production-}k$

La rete $\text{production-}k$ (Figura \ref{fig:production-network}) è progettata per offrire un ambiente isolato e raggiungibile esclusivamente dai membri autorizzati del team. È costituita dai seguenti dispositivi di rete:
* $\text{wg-}k$: dispositivo L3 gestito da WireGuard, fa da terminazione per il tunnel del team $k$-esimo. Ha come IP gateway: `10.k.0.1/24`
* $\text{br-team-}k$: dispositivo L2 gestito dal kernel Linux. Ha come IP gateway: `10.k.1.1/24`
* $\text{eth0}$: le interfacce di rete $\text{eth0}$ dei container che vengono collegate a $\text{br-team-}k$.

$\text{wg-}k$ serve per fornire ai membri del team $k$ l'endpoint per la connessione tramite VPN, in questo modo i membri del team saranno connessi direttamente alla rete $\text{production-}k$. Ogni membro ha la sua configurazione WireGuard associata al suo peer impostato sull'interfaccia $\text{wg-}k$. Aggiungere un peer all'interfaccia WireGuard significa permettere ad un client con una certa chiave pubblica di collegarsi con un certo indirizzo ip (**cryptokey routing**), e quindi assegnare ad ogni membro del team $k$ un indirizzo nella sottorete `10.k.0.0/24`.

L'interfaccia $\text{br-team-}k$ permette di creare una rete LAN per i container del team $k$, a cui questi si collegano.

Questo collegamento avviene tramite l'utilizzo di una `veth pair` (Virtual Ethernet) per container: un'estremità è collegata a $\text{br-team-}k$, l'altra all'interfaccia del container `eth0`. 
Questa architettura comporta la creazione di un numero di `veth` pair lineare al numero di container attivi.

> `veth`: È utile per collegare interfacce che risiedono per esempio su differenti Network Namespace (ossia il modo in cui sono implementati i container). Utilizzano poca CPU e poca memoria, dato che l'implementazione è efficiente e risiede direttamente nel kernel. Dunque per centinaia di `veth` non si ha un degrado evidente delle prestazioni. [^1]

Tramite regole di forwarding del kernel e di firewall via `nftables`, il traffico dell'interfaccia $\text{wg-}k$ viene autorizzato verso $\text{br-team-}k$ e viceversa. Questa regola viene applicata aggiungendo dentro al set `team_links` (una struttura dati all'interno del kernel gestita da nftables) la coppia di interfacce interessate.

![[src/images/production-network.png]]

---

## 4.2 Rete $\text{verify-}k$

La rete $\text{verify-}k$ (Figura \ref{fig:verify-network}) è costituita dai seguenti componenti:
* $\text{verify-}k$: rete virtuale logica gestita via SDN tramite OVN e orchestrata da Incus [^2]. Non costituisce una singola interfaccia di rete convenzionale del kernel, ma una topologia virtuale isolata composta da uno switch e un router con gateway: `10.k.1.1/24`.
* $\text{incusbr0}$: bridge di rete di Incus con gateway `172.16.0.1/24`. Svolge il ruolo di interfaccia per l'instradamento verso l'esterno della rete OVN.
* $\text{eth0}$: sono le interfacce di rete dei container clonati (`10.k.1.x`) che vengono collegate a $\text{verify-}k$.

> Incus è in grado di gestire da solo il collegamento tra $\text{incusbr0}$ e $\text{verify-}k$. Questo semplifica di molto la gestione delle interfacce di verifica per BlueAgent.

Le interfacce dei container e la rete $\text{verify-}k$ sono gestite dalla SDN (*Software Defined Network*). $\text{verify-}k$ è implementata da:
1. un **Logical Switch** (denominato internamente da Incus nel DB di OVN come `incus-net<ID>-ls-int` [^2]): rappresenta la LAN su cui si agganciano le interfacce virtuali dei container di verifica.
2. un **Logical Router** (denominato `incus-net<ID>-lr` [^2]): agisce come gateway (`10.k.1.1/24`), permettendo ai container clonati di preservare l'identica configurazione IP rispetto alla produzione.

> **Tunneling Geneve e considerazioni sull'MTU:** OVN impiega il protocollo di tunneling **Geneve** (*Generic Network Virtualization Encapsulation*) [^3] per spostare i pacchetti tra più nodi della rete.

L'incapsulamento Geneve introduce tuttavia un overhead di intestazione variabile (fino a 58 byte), riducendo l'MTU effettiva della rete a $1442$ byte (rispetto ai 1500 byte dello standard Ethernet). Se pacchetti di dimensione eccedente hanno il flag *Don't Fragment* (DF) abilitato, rischiano di essere scartati generando un fenomeno di *Path MTU Blackhole*.

Bisogna notare che il tunnel Geneve non viene mai utilizzato, poiché i container di verifica risiedono tutti all'interno dello stesso nodo. Tuttavia Incus limita di default l'MTU delle interfacce di rete dei container a 1442 byte per precauzione; per risolvere il problema è possibile forzare l'MTU a 1500.

L'uso di una SDN garantisce l'assenza di conflitti di routing grazie a una netta separazione tra **spazio utente** e **spazio kernel** [^5]:
* **Spazio Utente (Control Plane):** i demoni di controllo di OVN (`ovn-northd` e l'agente locale `ovn-controller`) elaborano la topologia logica e la traducono in flussi OpenFlow concreti per Open vSwitch (`ovs-vswitchd`). Il router OVN esiste puramente a livello logico.
* **Spazio Kernel (Data Plane):** il demone `ovs-vswitchd` riceve i flussi OpenFlow e programma il modulo kernel `openvswitch.ko`, dove viene applicato l'inoltro dei frame ad alte prestazioni. 

Il collegamento tra i container e la rete OVN sfrutta sempre una coppia `veth`: un'estremità risiede all'interno del container e si attacca ad `eth0`, mentre l'altra estremità sull'host viene agganciata direttamente al bridge di Open vSwitch.

> `SDN (Software Defined Networking)`: Paradigma architetturale che separa il **piano di controllo** dal **piano dei dati**, consentendo di gestire e programmare l'infrastruttura di rete interamente via software.

> `OpenFlow`: Protocollo standard che permette al controller SDN di comunicare con lo switch e programmare le regole di matching e le azioni direttamente all'interno delle pipeline di Open vSwitch.

> `OVN (Open Virtual Network)`: Sistema SDN che opera come Control Plane per Open vSwitch. Traduce topologie logiche (Logical Switch, Logical Router, NAT e ACL) tramite `ovn-northd` e `ovn-controller` in flussi OpenFlow distribuiti, istruendo Open vSwitch su come instradare il traffico senza creare molteplici interfacce o bridge dedicati nel kernel host. È costituito da due database:
> **OVN Northbound**: memorizza la dichiarazione delle reti logiche da creare e le proprietà che devono rispettare.
> **OVN Southbound:** memorizza le tabelle di flussi logici compilate da `ovn-northd`, che `ovn-controller` traduce in regole OpenFlow concrete per il piano dei dati.


La comunicazione verso l'esterno avviene collegando il Logical Router OVN al bridge parent $\text{incusbr0}$, da cui ottiene un indirizzo IP da utilizzare. L'accesso a Internet per i container di verifica sfrutta un meccanismo di NAT a due stadi:
* **Primo Stadio (SNAT in OVN)**: quando un container di verifica (`10.k.1.x`) invia traffico all'esterno, il Logical Router riscrive l'indirizzo sorgente sostituendolo con l'IP assegnatogli da `incusbr0` (nella sottorete `172.16.0.0/24`). Se non fosse applicato, i pacchetti in uscita manterrebbero l'indirizzo sorgente `10.k.1.x`, i quali sono attestati sulle interfacce di rete dei container nella rete di produzione.
* **Secondo Stadio (SNAT su `incusbr0`)**: una volta raggiunto `incusbr0`, il sottosistema Netfilter, tramite regole `nftables`, applica la regola di **masquerade** verso l'interfaccia fisica per uscire su Internet. Viene sostituito l'indirizzo di `incusbr0` con l'indirizzo pubblico dell'host che esegue BlueAgent.

| Tratta del Pacchetto                    | Indirizzo Sorgente ($IP_{src}$)         | Indirizzo Destinazione ($IP_{dst}$) | Responsabile           |
| --------------------------------------- | --------------------------------------- | ----------------------------------- | ---------------------- |
| Dal Container ad `incusbr0`             | `10.k.1.x` *(IP duplicato)*             | $IP_{ext}$ *(Internet)*             | Container di verifica  |
| Da `incusbr0` all'interfaccia dell'host | `172.16.0.x` *(IP transito univoco)*    | $IP_{ext}$ *(Internet)*             | Incus                  |
| Dall'host verso l'esterno               | IP dell'interfaccia pubblica dell'host. | $IP_{ext}$ *(Internet)*             | `nftables` / Netfilter |

Il NAT a due stadi è necessario per evitare collisioni di routing sull'Host: il primo stadio "nasconde" gli indirizzi duplicati `10.k.1.x` traducendoli in un IP su `172.16.0.0/24`, mentre il secondo stadio permette la navigazione esterna condividendo l'IP dell'host.

> `NAT (Network Address Translation)`: Meccanismo di rete che modifica le informazioni di intestazione IP (e opzionalmente le porte di livello 4) dei pacchetti in fase di routing. [^6].

> `SNAT (Source NAT)`: Variante del NAT applicata al traffico uscente (**egress**, fase di postrouting). Modifica l'indirizzo IP sorgente del pacchetto con un indirizzo pubblico o instradabile dalla rete esterna.

> `Masquerading`: Variante dinamica di `SNAT`. Si ha quando l'indirizzo sorgente viene mappato dinamicamente sull'IP dell'interfaccia di uscita dell'host.

![[src/images/verify-network.png]]

[^1]: Linux manual page, veth(4) - Virtual Ethernet Device: https://man7.org/linux/man-pages/man4/veth.4.html
[^2]: Documentazione ufficiale Incus, OVN network driver: https://linuxcontainers.org/incus/docs/main/reference/network_ovn/
[^3]: Documentazione architetturale OVN e Geneve: https://docs.ovn.org/en/latest/topics/geneve.html
[^4]: Documentazione Netfilter, TCP MSS Clamping: https://wiki.nftables.org/wiki-nftables/index.php/Forwarding_traffic
[^5]: Documentazione Open vSwitch, architettura Datapath Kernel vs Userspace: https://docs.openvswitch.org/en/latest/intro/what-is-ovs/
[^6]: Documentazione Netfilter, Network Address Translation (NAT): https://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT)