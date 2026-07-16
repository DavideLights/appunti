**obiettivo della privilege escalation**: una volta ottenuto l'accesso come utente non privilegiato devo diventare utente root, o comunque eseguire comandi come `uid=0, per a`

**fasi della privilege scalation**:

**restricted shell**: e' una shell che non permette di muoversi liberamente all'interno del sistema. potrebbe non permettere l'inserimento di spazi o di eseguire particolari programmi.

**come capisco su che shell mi trovo?** `echo $0`

**in una shell ristretta**: posso tentare di eseguire una shell completa con `/bin/bash`, ma per farlo devo raggirarne i limiti se ci sono

**vi**: `:!/bin/bash` 

**bypassare restrizione sui nomi dei binari usando wildcard**: se non posso eseguire `/bin/bash`, magari posso provare con `/bin/b*sh` e la wildcard probabilmente fara match solo con `bash`


**quale variabile d'ambiente sostituisce lo spazio per bypassare le shell ristrette**? `${IFS}`

**leggere `/etc/passwd` se spazio proibito**: `cat${IFS}/etc/passwd`

**come visualizzare kernel e architettura del sistema**? `uname -a`
**come visualizzare informazioni sulla distribuzione?** `cat /etc/*release`
**quale comando mostra id utente, e gruppi**? `id

**quale comando permette di vedere le variabili ambiente**? `env`

**cosa fa `sudo -l`**? fa vedere le regole sudo per l'utente corrente

**come monitoro i processi in tempo reale**? `htop` o `top`

**perche' e' utile controllare** `.bash_history` **in enumerazione**? potrebbe contenere password scritte in chiaro (passate come argomento ai comandi), o comandi sensibili

**linux capabilities, cosa sono**? meccanismo con il quale posso concedere ad un file eseguibile, un'insieme ristretto di permessi speciali, invece di concedere tutti insieme i privilegi di root. 

**effective capability**: e' la capability che raccoglie i permessi effettivamente concessi in un determinante istante di tempo al processo

**cosa indica il bit suid**? che chiunque puo' eseguire il programma usando come `uid` quello del proprietario del file.

**come si visualizzano le porte di rete aperte e i relativi proc**? `netstat -tulpn`

**le chiavi ssh private dove si trovano**? `~/.ssh/id_rsa/`

**quale comando elenca i cronjob**? `crontab -l`

**qual'e' lo scopo di permitted cap**? imposta un insieme massimale di capabilities che il processo puo usare

**cos'e' LinPEAS?** linpeas serve per controllare i vettori
**pspy**: serve a visualizzare i processi in esecuzione, alcuni potrebbero essere stati lanciati con password in chiaro

**come avvio una bash ristretta**? con `rbash`

**cosa fa `find / - perm -u+s`**: cerca file con suid attivo per l'utente proprietario.

**quale comando elenca i processi in esecuzione**? `ps aux`

**a cosa server** `netstat -tulpn`: mostra le socket attive ed i relativi processi in esecuzione. 

**dove si trovano le chiavi private ssh**? `~/.ssh/id_rsa`

**quale file contiene i mount point del filesystem**: `/etc/fstab`
**cosa fa `crontab -l`**? mostra i cronjob per l'utente corrente

**a che serve pspy**:  mostra tutti i processi in esecuzione sulla macchina con i relativi comandi d'esecuzione.

**perche' i kernel exploit sono l'ultima scelta per un pentester**? il kernel exploit sono rumorosi, e potrebbero rendere il sistema instabile. Dunque si cercano modi piu creativi per bucare il sistema.

**formato di `/etc/passwd`**: `nomeutente:hash:uid:gid:nomedescrittivo:homedir:/bin/bash`

cosa vuol dire `NOPASSWD:ALL`? che tutti i comandi (`ALL`) possono essere eseguiti senza richiedere la password con sudo.

**path hijacking**: si applica quando script o risorse del sistema vengono accedute utilizzando percorsi relativi. questi possono essere attaccati rimpiazzando il file con uno malevolo, che viene eseguito quando richiamato da un programma con permessi piu alti. inoltre linguaggi come python possono essere indotti a caricare moduli contraffatti piuttosto che altri.

**sudoers path traversal**: quando in sudoers ho permessi di esecuzione su un'intera cartella, posso navigarla al contrario ed eseguire quello che mi pare.

**7z**: se ha permessi speciali, posso usarlo per fare il backup per conto del mio utente di file sensibili

# seminari
**Quale livello di precisione offre il tracciamento della posizione 5g?** precisione sulla scala dei centimetri

**In quali contesti risulta utile il 5g?** Le aree dove il gps e' disturbato o non arriva, ossia in molte zone, anche stadi ed eventi affollati.

**Che cosa offre il 5g in termini di prestazioni rispetto a gps?**

**SDR**: si intende una radio dove la conversione del segnale in digitale viene effettuata immediatamente dopo il processamento nel front-end RF (che puo' essere pilotato via software).
* permette di definire il comportamento della radio via software e di manipolare il segnale di conseguenza.

**Quali sono le principali funzione del core network?**  autenticazione e connessione alla rete

**cellulari definiti come blackbox**: l'hardware dei comuni cellulari permette di accedere al 5g attraverso un'interfaccia standardizzata che non permette di manipolare direttamente il segnale radio, non permette nemmeno l'ispezione della ret.

**obiettivo del 5gMap**: strumento per sviluppatori e ricercatori per studiare vulnerabilita ed efficienza del 5g.

**cifratura nel canale radio**: serve a rendere il messaggio illeggibile, dato che il 5g e' un canale condiviso

**protezione dell'integrita**: si vuole garantire che i dati arrivino integri a destinazione contro un potenziale attaccante usando MAC

**come scopro quali algoritmi sono supportati dalla rete?** una volta che trovo l'antenna, usando 5gmap posso richiedere di instaurare una connessione al Network Core utilizzando un particolare protocollo. Mi basta chiedere se il protocollo x e' supportato iniziare il meccanismo di connessione.

**tmsi**: temporary mobile subscriber identity che cose? e' un codice identificativo assegnato in maniera temporanea e dunque cambio quando mi sposto da una base station ad un'altra. impedisce il tracciamento della mia identita nello spostamento

**imsi catcher**: un'attaccante si finge una base station autorevole ed annuncia la sua presenza utilizzando un segnale molto piu potente di quello della stazione autorevole. dunque l'utente si collega all'attaccante e gli manda l'imsi
* sono rumoroso e sgamabile e causo problemi di servizio alla vittima che si accorge che qualcosa non va

**attacco man in the middle**: mi fingo una base station che inoltra i pacchetti all'implementazione di un finto UE che inoltra i dati alla vera base station

**vulnerabilita AES per bit flipping**: se conosco una porzione del testo in chiaro e del cifrato (per esempio nel campo di una connessione DNS so qual'e' il server di default contattato), allora posso recuperare la chiave AES usata

**cosa succede alla fine dell'attacco imsi catcher**?