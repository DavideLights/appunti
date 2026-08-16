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
  

Questo approccio trasforma la VM in un vero e proprio switch virtuale: la sua interfaccia di rete principale diventa una "porta" dello switch, perdendo il proprio IP diretto, che viene invece assegnato al bridge stesso. I container Incus si collegheranno a questo bridge ottenendo un IP dalla stessa rete della VM.

  

**1.Identifica l'interfaccia fisica della VM:**

Esegui `ip link` per trovare il nome dell'interfaccia principale della tua macchina virtuale (ad esempio `eth0`, `ens3` o `enp1s0`). Annota questo nome, ti servirà nei passaggi successivi.

  

**2.Crea il device virtuale del bridge (br0):**Crea un file .netdev per definire il bridge.

Crea il file `/etc/systemd/network/10-br0.netdev` e inserisci questa configurazione per dire al kernel di creare il bridge:

  

Ini, TOML

```
[NetDev]
Name=br0
Kind=bridge
```

**3.Collega l'interfaccia fisica al bridge:**Sostituisci 'eth0' con il nome reale della tua interfaccia.

Crea il file `/etc/systemd/network/10-br0-bind.network`. Questo file dice a `systemd-networkd` di prendere la tua scheda di rete e agganciarla al bridge, togliendole la gestione diretta dell'IP.

  

Ini, TOML

```
[Match]
Name=eth0

[Network]
Bridge=br0
```

**4.Configura la rete sul bridge:**Il bridge eredita l'indirizzo IP che prima aveva la VM.

Crea il file `/etc/systemd/network/11-br0.network`. Se la tua VM riceveva l'IP in DHCP dalla rete esterna, usa questa configurazione:

  

Ini, TOML

```
[Match]
Name=br0

[Network]
DHCP=ipv4
```

Se usavi un IP statico, configuralo qui (es. `Address=192.168.1.10/24`, `Gateway=192.168.1.1`). Assicurati di disabilitare o eliminare eventuali vecchi file `.network` che configuravano l'IP direttamente sull'interfaccia fisica.

  

**5.Applica la configurazione di rete:**

Riavvia il demone di rete per applicare i cambiamenti. **Attenzione**: se sei connesso in SSH e hai sbagliato la configurazione al passaggio 4, potresti perdere la connessione.

  

Bash

```
sudo systemctl restart systemd-networkd
```

Verifica con `ip a` che l'interfaccia `br0` sia UP e abbia ottenuto l'indirizzo IP, mentre l'interfaccia fisica dovrebbe essere UP ma senza IP.

  

**6.Configura Incus per utilizzare il bridge L2:**

Ora che il sistema operativo ha il suo bridge, devi dire a Incus di collegarci i container. Puoi creare un profilo dedicato (consigliato) oppure modificare quello di default:

```
# Crea un nuovo profilo chiamato 'l2-bridge'
incus profile create l2-bridge

# Aggiungi un'interfaccia di rete collegata a br0
incus profile device add l2-bridge eth0 nic nictype=bridged parent=br0
```

**7.Lancia il container e verifica:**

Lancia un container applicando il nuovo profilo. Il container farà una richiesta DHCP che attraverserà il bridge e arriverà direttamente al router della rete esterna.

```
incus launch images:ubuntu/24.04 mio-container --profile default --profile l2-bridge
```

```bash
# Assegna IP statico al container
incus network set incusbr0 ipv4.address 10.0.3.1/24
incus config device set <container_name> eth0 ipv4.address 10.0.3.10
```


## incusbr0 vs br0
Abbiamo dovuto creare il nostro bridge `br0`, perche `incusbr0` e' una rete NAT:
* sottorete privata e isolata
* ha un suo dhcp server
* la rete esterna dunque non vede i container 

`br0` invece:
* usa `eth0` per creare uno switch di rete
* i container si collegano a `eth0`, dunque bypasso la rete nat predisposta da incus