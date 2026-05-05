**porte socket**:
* **HTTP**: 80
* **HTTPS**: 443
* **SSH**: 22

**la porta dipende dal protocollo**: esiste la porta `80/TCP` e la `80/UDP`, costituiscono due canali separati. 

**NAT**: piu device possono condividere un singolo ip pubblico. 
* **source address**: il router lo modifica quando inoltra il pacchetto in internet.
* **porta sorgente**: modifica anche questa!
* **home e corporate networks**: utilizzato spesso.

**Firewalls**: controlla quale traffico puo' entrare/uscire dalla rete.
* **allow/deny** del traffico pacchetti, basandosi su regole.
* **criteri**: *source ip, dest ip, source port, dest port, protocol, ecc...*

**DNS**: traduce i nomi in ip

**URL**:![[Pasted image 20260423012215.png]]
* **protocollo**: indica come la risorsa dovrebbe essere acceduta
* `[<username>:<password>@]`: sono opzionali, e permettono di connettersi per conto di un'utenza. Pero' questo vuol dire che la password potrebbe passare in chiaro nel traffico di rete.

**basic connectivity**
* `ping`: controlla se host raggiungibile e la latenza
* `traceroute`: mostra il path dei pacchetti verso la destinazione.
* `arp / ip neigh`: tabella arp
* `ip / ifconfig`: mostra interfacce network e la configurazione
* `route / ip route`:  mostra le tabelle di routing

**netcat**:
*  **TCP**: `nc <target> <port>` (connettiti) ed `nc -l -p <port>` (ascolta)
* **UDP**: `nc -u <target> <port>` (connettiti) ed `nc -l -p <port>` (ascolta)
* **disable DNS**: `-n`
* **esegui programma e ridireziona IO**: `nc -l -p <port> -e <program>`

## DNS
**DNS**: distribuito su server, gearchico,
* **delegazione**: ogni livello delega al successivo la risoluzione.
* **zone**: i dati di un dominio e un sottoinsieme dei suoi sotto-domini costituiscono una zona
* **es**: `dns.uniroma2.it`, `www.uniroma2.it`, `mail.uniroma2.it` si trovano nella zona di `uniroma2.it` nell'immagine, sotto il dominio `.it`
![[Pasted image 20260423013837.png]]

gemini spiega: Uniroma2 could have separate nameservers on each 
department, each responsible for their own 
subdomain
The parent domain would delegate responsibility for 
a subdomain to each department, making many 
zones

**attori DNS**:
* **client**: un programma che usa un dominio.
* **server**: database di dati DNS
* **resolver**: software che accetta query da un client e interroga uno o piu server DNS. ritorna al cliente una risposta alla query.

**query ricorsiva**: il server a cui faccio richiesta se ne ha bisogno manda query ad altri server per risolvere il nome.
* **no referral**: non mi viene ritornato nessun referral, ci pensa il server!

**query iterativa**: se il server a cui faccio richiesta non ha la risposta, mi da il referral ad un'altro DNS server.

**record types**:  rispondono ad una domanda specifica.
* `A`: `IPv4`; `AAAA`: `IPv6`.
* `MX`: Mail Exchange
* `PTR`: Host name corresponding to IP address. **e' l'opposto di `A`**
* `NS`: Host name del server autoritativo per il nome dato.
* `CNAME`: nome canonico del nome da risolvere.
* `SOA`: identifica il server responsabile per l'informazione del dominio.
* `TXT`: testo generico.

**risoluzione in linux**, ordine delle fonti per la traduzione:
* `/etc/hosts`: permette di fare mapping manuali.
	* `127.0.0.1 localhost`, `192.168.1.10`
* **cache**
* **DNS resolver**

`dig`: "interroga dns server"
* `dig hostname`
* `dig hostname record-name`
* `dig @dns-server hostname record-name`
* `dig @dns-server hostname any`

`dig` vs `host`: `host` e' piu semplice da leggere rispetto ad `host`

**discovering host**:
1. **forward lookup bruteforce**: prova liste di potenziali hostname per identitifcare sottodomini che espongono certi servizi.
2. **reverse lookup bruteforce**: scansiona ip e trova i `PTR` che rivelano gli hostname e le naming conventions interne alla societa.
3. **DNS zone transfer**: fai il dump della DNS zone al server autoritativo.
![[Pasted image 20260424100127.png]]
## forward lookup bruteforce
```bash
for ip in $(cat list.txt); do host $ip.megacorpone.com; done
```

## reverse lookup bruteforce
```bash
for ip in $(seq 1 255);do host 38.100.192.$ip;done | grep -v "not found"
```

## dns zone transfer
**dns zone**: processo in cui un dns server passa una copia di parte del database (ossia una zona) ad un'altro server DNS.

**a che serve?** cosi posso avere piu server DNS che rispondono alla stessa zona. ne servono almeno 2.

**come si richiede la copia**? uno slave server fa una richiesta al master server.

**attacco**:
1. pretendi di essere uno slave che vuole rispondere in modo lecito alle query dns
2. il master mi rivela tante informazioni topologiche sulla rete che voglio attaccare.
3. **gemini spiega:** In particular, if someone plans to subvert your DNS, by poisoning or spoofing it, for example, they'll find having a copy of the real data very useful.

**soluzione**: il master ha una lista di slave fidati a cui trasferire i dati.


```bash
host -t ns megacorpone.com | cut -d " " -f 4
```

**zone transfer**: usa il protocollo **AXFR** ed e' una client-initiated request.
```bash
dig axfr @nsztm1.digi.ninja zonetransfer.me
```

**script per zone transfer**
```bash
if [-z "$1"]; then
	echo "[*] Simple Zone transfer script"
	echo "[*] Usage: $0 <domain name> "
	exit 0
fi
for server in $(host -t ns $1 | cut -d" " -f4); do
	host -l $1 $server | grep "has address"
done
```

### dns recon
**dns recon**:
* **zone transfer**:`dnsrecon -d <domain> -a` or `dnsrecon -d <domain> -t axfr`
* **reverse lookup**: `dnsrecon -r <startIP-endIP>`
* **reverse lookup** su record `SPF`:`dnsrecon -d <domain> -s`

**record SPF** (Sender Policy Framework): e' un record TXT che elenga i server autorizzati ad inviare mail dal dominio di interesse.

**caso uso SPF**: un server di posta che riceve un messaggio per certificare che l'indirizzo sia valido controlla se esiste un record col suo nome nel dns server della zona.

**dns recon bruteforce**: `dnsrecon.py -d <domain> -D <namelist> -t brt`.
* **namelist**: nomi che uso per provare a risolvere
* **cosa fa**? fa una richiesta dns per ogni dominio da provare.

### altri tool e mitigazione
**dnsenum**: `dnsenum zonetransfer.me`
**fierce**: trova spazi di indirizzi ip e hostname dentro domini. Fa zone transfer, reverse lookup e brute force

**mitigare**: l'attacco zone transfer puo' essere facilmente bloccato configurando una lista di ip che possono fare il zone transfer

# host discovery
**DNS Enumeration**: non mi trova tutti gli host attivi in rete, alcuni potrebbero non avere un nome associato.

**arp scan**: funziona solo se ti trovi nella stessa sottorete degli host da attaccare.
![[Pasted image 20260428210518.png]]

**ping scan**: si fa con `nmap`
* **ICMP echo request**: uso ICMP per interrogare i probabili host
* **remote networks**: ICMP puo' attraversare le reti
* **firewall**: potrebbe bloccare i messaggi ICMP.
![[Pasted image 20260428210536.png]]

**identificare il servizio**: una volta trovato con ping scan un host bisogna capire che servizi esegue sulle porte.
 
**port scanning**: devo testare quali porte sono aperte, chiuse o filtrate sull'host da attaccare.
* **porte standard**: ricorda che molti servizi eseguono su porte fissate.
* **offensive/defensive secuirity**: in entrambi gli ambiti bisogna fare port scanning.

**port binding**: il sistema operativo per esporre un servizio alla rete lega il processo ad una specifica coppia (IP adress, port)

**servizi diversi, ip diversi, su stesso host**, per esempio:
* web app viene esposta legandola **all'ip address pubblico** della macchina
* una web app interna, per esempio di controllo della macchina, viene legata all'ip address locale, per esempio all'interfaccia di **loopback** `127.0.0.1`

**ogni porta ha il suo linguaggio**: quando interrogo una porta devo farlo usando il suo protocollo.
1. **identificare il protocollo di trasporto**: `TCP, UPD, ...`
2. **identificare il protocollo a livello di applicazione**: `HTTP, SSH, FTP, ...`
# TCP
![[Pasted image 20260428152305.png]]
**durante il three-way-handshake**:
* **negoziazione parametri**: parametri di rete, della connessione TCP.
* **se l'handshake viene completato**: allora la porta e' aperta.

```bash
nc -n -vv -w 1 -z <ip addr> <port range>
```

## UDP scan
**a differenza di TCP**:
* **niente three-way handshake**
* **stateless**
* `nc -nv -u -z -w 1 <ip address> <port range>`
* guardare 

**come si fa lo scan udp**? viene mandato un pacchetto udp vuoto alla porta.
* **se porta aperta**: non ricevo niente dalla target machine
* **se la porta e' chiusa**: ricevo messaggio ICMP di errore

**falsi positivi**: avviene se un firewall blocca il messaggio ICMP.
**list**: spesso scansiono solo una lista predeterminata di porte interessanti, dove so che ci sara qualcosa di interessante.


## nmap
**default**: scansiona le 1000 porte TCP piu popolari su un target in input
**port states**:
![[Pasted image 20260428215407.png]]


**-p**: specifica un range di porte. `nmap <ip address> -p25-150`
**CIDR**: per specificare un range di indirizzi

**identita**: vogliamo nascondere il nostro ip da cui parte la scansione
* **-S: spoof**, qualsiasi risposta viene re-direzionato allo spoofed ip.
* **-D**: posso offuscare l'indirizzo ip scegliendolo randomicamente da una lista. `nmap <ip address> -D <fake ip list>`

**icmp**: nmap usa icmp di default, ma molti firewall lo bloccano.
* `ping`: nmap di default scansiona mandando una **echo request** ed aspettando una **echo reply** via icmp.
* **a che serve ping**? serve a controllare se il target e' acceso (up)
* **-P0**: sopprime icmp.

**nmap, scan e porte default**: quando una porta e' attiva, e nmap la trova, viene ritornato il servizio di default su quella porta.

**servizio**: non sappiamo dunque che servizio viene eseguito su quella porta.
* sulla 22 c'e' ssh?
* sulla 80 che tipo di server http c'e'?
