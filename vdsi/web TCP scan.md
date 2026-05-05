## banner
**banner**: e' un messaggio che viene mandato immediatamente dopo una connessione, *o in risposta ad una richiesta*. e contiene:
* service type (HTTP, FTP, SSH)
* software (apache, openssh, ...)
* version information
* os details

**netcat**: `nc [-u] <addr> <port>` (dove **-u** sta per **udp**)
**nmap**: `nmap -sV [-sU] [-p<ports>] <ipaddress>`


## TCP connect scan `-sT`
![[Pasted image 20260429092308.png]]
**tpc connect scan**: tento di aprire una connessione, successivamente la chiudo. Si fa con `-sT`
**closed port**: mando `SYN` e ricevo `RST`
**open port**: mando `SYN` e ricevo `ACK+SYN`. Devo mandare `ACK` rispetto al `SYN` del server, e `RST` per chiudere la connessione.

**problemi**: e' un approccio **rumoroso**.
* **logs**: compaio nei log del server!
* `connect()`: la connessione `TCP` e' completa quando mando `SYN`, dunque il server alloca risorse per gestirla.

> [!note] gemini: spiega meglio cosa c'e' scritto qua sotto
> ◦ Since the TCP connect() scan is completing a TCP connection, normal application processes immediately 
follow
◦ These applications are immediately met with a RST packet
◦ but the application has already provided the appropriate login screen or introductory page
◦ By the time the RST is received
◦ the application initiation process is already well underway and additional system resources are used

**dunque**: il `tcp` scan e' l'ultima risorsa se non ho accesso aprivilegi elevati.

## TCP SYN Scan `-sS`
**obiettivo**: rispetto al connect scan, voglio fare il **reset** della connessione prima che il *TCP handshake sia completato*.

![[Pasted image 20260429112021.png]]

`ACK`: rispetto a prima, non mando `ACK` rispetto a `SYN/ACK` che ricevo dal server, in caso di porta aperta.

**vantaggi**:
* **sessione TCP**: non viene mai creata lato server. dunque ho piu chance di non rimanere nei log del server.
* **quiet**: dunque questo tipo di scan e' meno rumorosa.
* **stressful**: dato che non creo sessioni, lato server e' meno stressante questo tipo di scan.

## stealth scan
**stealth scan**: e' un tipo di scan in cui mando un singolo frame ad una porta `TCP` senza fare handshaking. Mi aspetto di ricevere un qualche tipo di risposta.

**header**: devo manipolare l'header TCP in modo da ottenere una risposta. usiamo combinazioni irrealistiche dei bit nell'header.

**protocollo tcp**: dice che, quando una porta riceve dati
* se la **porta e' chiusa**: risponde con `RST`
* se la **porta e' aperta**: non risponde.

**nasce un problema**: non posso capire quando ho una **porta aperta**, o semplicemente la rete ha **droppato il frame** che ho inviato.

**pacchetti custom**: dunque nmap usa frame `TCP` creati ad-hoc per attaccare. Per crearli ha bisogno dei privilegi di sistema.
**3 tipi di scan stealth**: `fin scan`, `xmas scan`, `null scan`

**fin scan**:
![[Pasted image 20260429113249.png]]

**xmas scan**:
![[Pasted image 20260429113328.png]]
**null scan**:
![[Pasted image 20260429113402.png]]

**sono stealth perche**: non creano connessioni
* **rispetto al server**: silenziose.
* **log**: non dovrebbero comparire nei log i frame inviati.

**quanti frame devo inviare**?
* **porta chiusa**: 2 pacchetti per identificarla
* **porta aperta**: 1 solo pacchetto.

> [!note] gemini spiega
> On a Windows-based computer
◦ All ports will appear to be closed regardless of their actual state
◦ Any device showing open ports must not be a Windows-based device
The user running stealth scans needs to have root privilege

**perche usare le stealth scan**?  usano meno banda di rete rispetto a `TCP SYN` scan e mi da molte informazioni su sistemi non-Windows.

**version detection**: `nmap -sV` gemini spiega!!!!

## udp scan `-sU`
**handshaking**: `udp` non lo fa, dunque non ci sono `SYN`, `FIN` da gestire o da sfruttare. dunque lo scanning `udp` e' più semplice.

![[Pasted image 20260429114601.png]]**overhead**: non c'e' l'overhead dovuto a header e handshake tcp.
**overhead icmp**: se ho molti tentativi falliti (**porte chiuse**), ho un traffico `icmp` elevato sulla rete.

**windows**: posso attaccarlo con scan udp, *non c'e' un limite ai messaggi icmp che posso inviare*.

> [!note] gemini spiega perche'
> The UDP scan provides port information only
◦ If additional version information is needed
◦ The scan must be supplemented with a version detection scan (-sV) or the operating system fingerprinting option (-O).

**gemini**: perche' con TCP ottengo anche informazioni sul servizio in esecuzione.

## ack scan `-sA`
**porte aperte**: `ack scan` trova solo porte filtrate o non filtrate.

**connessione**: non viene mai effettuata una connessione per trovare porte effettivamente aperte.

**gemini**: spiega meglio `ack scan`.
![[Pasted image 20260429115506.png]]

**vantaggio di** `ack scan`: se sulla rete c'e' traffico di dati, allora e' difficile accorgersi dello scan.

**a cosa serve `ack scan`**: ad identificare porte filtrate da un firewall!

![[Pasted image 20260429115836.png]]