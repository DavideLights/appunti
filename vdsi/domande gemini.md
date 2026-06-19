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


