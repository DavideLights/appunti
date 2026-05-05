* `findmnt`: trova se sono montate certe partizioni
* `mount | grep '^/'`: mostra tutte le partizioni montate
* `ls /var/mail` e `ls /var/www` per informazioni su webserver e mail server.
* `ls /var/spool/{mail,www}`
* `find / -writable 2> /dev/null | cut -d "/" -f 2,3 | sort -u`.
	* `sort -u`: toglie i duplicati
	* `cut -d "/" -f 2,3` toglie `/` dal path ed estrae seconda e terza colonna dall'output.
* `find / -type f -mtime -1 2>/dev/null`: trova ciò che e' stato modificato nell'ultima ora.
	* `-mmin 30`: l'ultima mezz'ora.
* `find / -type f -newermt "9:00:00" 2>/dev/null`: cosa e' stato modificato dalle 9 (gemini conferma te)
* `sudo -V`: controllare la versione perche' potrebbe essere exploitabile.
## logging
* `who`: mostra le sessioni attive per l'utente corrente.
* `watch`: esegue comando periodicamente.
* `last`: mostra le ultime sessioni di login.
	* `last root | head`.
	* gemini: differenza tra head e less
* `tail -n 1`: prende l'ultima riga.
* `lastlog`: oltre agli utenti normali fa vedere anche gli utenti senza login.
* `lastb`: lastb is the same as last, except that by default it shows  a  log  of  the  /var/log/btmp file, which contains all the bad login attempts.
* `cat /var/log/auth.log | grep chpasswd` **tutte le informazioni di login** che riguardano il cambio password
	* `| grep root`: le cose relative a **root**.
	* `string ... | grep ...` mi da solo testo human readable.
* `tail -f /var/syslog`: il comando rimane attaccato alla macchina e posso vedere le cose nuove che succedono. (`watchdog`).
* `sudo -l`: mi fa vedere cosa puo' fare l'utente secondo a cosa c'e' scritto in `cat /etc/sudoers`
* `cat /etc/sudoers` e `cat /etc/sudoers.d/usergroup`: informazioni sui permessi sudo degli utenti.
* `find -type f \{-perm -u+s -o -perm -g+s \} -exec ls -l {} \; 2>/dev/null`: trova file eseguibili con **SUID**.
## processi
* `ps aux`: da informazioni su tutti i processi.
	* **oss**: se l'output fa schifo e viene tagliato allora faccio `ps aux | cat`. Lo passo a cat prima di fare il grep.
* `ps -ef` quasi equivalente ad `ps aux`.
* `echo $$`: dammi il PID del processo corrente.
* `pidof /bin/zsh`: dammi il PID delle istanze di `/bin/zsh`
* `lsof`: lista le risorse usate da un processo.
* `lsof -i -n -P`: mostra le socket usate da un applicativo. 
	*  `-n`: non risolve l'indirizzo ip con DNS. potrebbe essere utile o no. crea traffico DNS ed e' piu lento.
* `netstat -tulpn`
* `top`, `htop`: sono interattivi.
* `cat /etc/services`
* `apt list --upgradable`

## enumerazione su applicazioni installate
* `ls -lah /usr/bin`
* `dkpg -l`, `rpm -qa` ecc...
* `ls -lah /var/cache/apt/archives`
* `ls -lah /var/cache/yum`

## enumerazione su rete 
* `ip a`, `ifconfig`, `arp -a`
* `ip r`, `route`
* `iptables -L -v -n`: utile se ho un firewall, per vedere le regole del firewall. In verita non serve a un cazzo!
* `tcpdump -i lo -A`: il dump di cosa passa sull'interfaccia.

## enumerazione ssh
* `cat /etc/ssh/ssh_config` (**client**)
* `cat /etc/ssh/sshd_config` (**server**)
	* `cat /etc/ssh/sshd_config | grep Permit` per vedere se per esempio posso accedere come root, ecc...
	* `| grep Port` me ottenere la porta.
* `find / -name id_rsa 2> /dev/null`: gemini che minchia trova?
*  `find / -name authorized_keys 2> /dev/null`: gemini che minchia trova?
* `cat /ghome/*/.ssh/id_rsa`: ottieni tutte le chiavi RSA

## enumerazione MySQL
* cerca i file di configurazione per sborrare
* se trovo delle credenziali posso usarle per trovare altre password porka madonna.

## enumerazione cronjobs
* `crontab -l` o `crontab -l uzzo`. 
	* `-l`: listone del crontab.
	* https://crontab.guru per decifrare le regole che sono complicate porcodio

## enumerazione capabilities
* posso creare un **sottoinsieme di privilegi** da assegnare a dei processi.
* `CapInh` (**Inherited**): quando un nuovo processo e' creato, eredita tutte le capabilities del padre e potrei exploitarlo.
* `CapEff` (**Effective**): capabilities effettivamente usate dal processo. Il kernel fa il controllo dei privilegi da qua.
* `CapPrm` (**Permitted**): ho un limite alle capabilities del processo. da qui elevo ad effective
* `CapBnd` (**Bounding**): mette un limite alle capabilities che un processo non puo' mai utilizzare. Previene passaggi di capabilities non permessi.
* `CapAmb` (**Ambiente**): capabilities che sono mantenute tra chiamate di sistema. (gemini aiutami te)

gemini: spiegamele meglio a che servono

* `cat /proc/<PID>/status | grep Cap`
* `capsh --decode= 00001fffff` mi fa il decode della capability come esadecimale. E' una maschera.
* `getcap` e' piu semplice. 
	* `getcap -r / 2>/dev/null` me lo fa su tutti i file in `/`. Ed e' utile porcoddio!


## linpeas
**linpeas**: e' uno script che cerca automaticamente e fa enumeration.
* **e' un tool oneline**: faccio il `curl` del file e lo do in pasto ad `sh` senza nemmeno salvarlo.
* l'output giallo-rosso e' al 95% un vettore d'attacco
* l'output rosso e' da controllare.

## pspy


## attenzione ai tool automatici
* linpeas e pspy sono troppo rumorosi
* ti sgamano
* devi imparare a mano ad usarli
* cosi sai leggere l'output.


