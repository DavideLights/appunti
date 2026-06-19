 > [!warning] studia /etc/passwd ed /etc/shadow

**password**: segreto condiviso tra utente e servizio.

**password overload**: molte persone usano la stessa password su piu siti.

**charset ristretto**: di solito uso solo i caratteri della tastiera invece di quelli possibili. 
* se la password usa in modo uniforme tutti i bit: $\frac{1}{256^8}$
* password usa solo lettere e numeri: $\frac{1}{36^8}$

password con **bassa entropia**: sono password facili da ricordare, dove una sequenza di caratteri dipende da un'altra. 

**OSINT/SOCMINT**: con tecniche di social engineering posso capire in base agli interessi di una persona che parole potrebbe usare. (conseguenza della bassa entropia)

**shannon entropy**: misura il grado di incertezza di una password.

**attacco a dizionario**: si applica facilmente a password con bassa entropia su un set di password da testare.

# wordlist: generare dizionari da usare
**wordlist**: esistono wordlist pubbliche con le password piu probabili.

**user list**: devo provare a indovinare come e' fatto il nome utente, salvo i nomi probabili da testare in un file `userlist.txt`

**password list**: ho bisogno di una lista di password. le metto in `passwordfile.txt`

**List precompilate**: in kali  ne ho gia una per le password: `/usr/share/wordlists/rockyou.txt.gz`. John the ripper ha la sua in `/usr/share/john/password.lst`.
## crunch
**crunch**: tool che crea wordlist basandosi su **combinazioni matematiche**. Tecnica di **bruteforcing**.

**quando uso crunch?** se conosco la struttura della password.

```bash
crunch 7 7 AB
```
* **lunghezza**: `7 7` genera parole di lunghezza 7.  `7 8` genera parole di lunghezza da 7 a 8
* **caratteri**: `AB` vuol dire che uso i caratteri `A` e `B`

## cewl
**cewl**: custom wordlist generator. Permette di creare wordlist **context-aware**
```bash
cewl https://www.target.xyz -w targetWL.txt
```

```bash
cewl -w bulbwords.txt -d 1 -m 5 www.bulbsecurity.com
```

* -**d**: depth per lo scraping
* -**m**: lunghezza minima della parola da generare

**quando uso cewl**? per generare password basate sulle parole dentro un sito. (utile se devo fare pentest in una azienda).

## anarchy
**username anarchy**: genera gli username potenziali usando nome e cognome.
**quando uso anarchy**?: pentest in una azienda dove di solito i nomi utente seguono un pattern.

# hydra: attacco online
**hydra**: tool con cui mando richieste di login (verso SSH, Web Login, ecc...)
* **latenza**: il server potrebbe limitare il mio troughput
* **visibilita**: ogni attempt viene loggato sulla macchina
* **lockout**
* **firewall**: puo' accorgersi di me e bloccarmi.

**con hydra**: vengo sgamato subito.

```bash
hydra -L userlist.txt -P passwordfile.txt 192.168.20.10 pop3
```

* -**l**: se conosco gia l'utente da attaccare lo posso specificare.

```bash
hydra -t 4 -l EdoMan000 -P /usr/share/wordlists/rockyou.txt -vV 10.10.10.6 ftp
```
* **-t 4**: connessioni parallele (threads)
* **-vV**: very verbose
# attacco offline con hashcat e john
**hashcat e john the ripper**: si usano quando ho il database delle password crittografate.
* **velocita**: dipende dalla mia macchina
* **invisible**: faccio tutto in locale

## nascondere le password
**hash function**: sono funzioni one-way. Nel senso che se conosco $h$ posso facilmente calcolare $h(x)=y$ ma da $y$ e' difficile risalire ad $x$.

**come attacco**? se ho le password crittografate e conosco $h$ posso calcolare $h(x)$ su un database di password in chiaro e trovare riscontri nelle password crittografate.

**salt**: una stringa random che viene aggiunta alla password. Password identiche di utenti diversi non collidono.

**cosa salvo**? nel database delle password ho `user | salt | H(password||salt)`. Devo ricordare il **sale**!

**crackstation**: sitoweb fiko
## linux password
**/etc/shadow**: `id salt hash : other-stuff : ...`
* $\text{hash} = H_{id}(\text{salt} || \text{password})$.
* $H$ e' **yescrypt** su molte distribuzioni linux. Prima si usava SHA-512
* **root**: l'unico che puo' leggerlo.

**yescrypt**: invece di essere CPU intensive, usa tanta memoria per criptare. E' piu difficile per l'attaccante perche' ha bisogno di tanta ram per decriptare.

## tool di password cracking
**john the ripper**: si basa sulla potenza computazionale del processore.

> [!warning] john the ripper
> fare le challenge su sta roba


**unshadowing**: `unshadow /etc/passwd /etc/shadow` produce un file per john the ripper.

```bash
john --single hashesFile
```
**single crack**: il comando prova per ogni utente le combinazioni di password a partire dal nome utente. hashesfile e' stato prodotto da unshadow.

`john.conf`: contiene le regole su come funziona john

`john -w=/path/to/wordlist hashesFile`: usa la wordlist data per attaccare hashesFile

**rockyou**: un esempio di wordlist da usare.

**se l'attacco fallisce?** con `-rules=All` posso applicare delle regole.

**incremental**: prova tutte le combinazioni possibili

**incremental limitato**: prova l'attacco su un insieme ristretto di combinazioni. posso specificare lunghezza minima e massima

`john --incremental:<set> hashesFile --min-length=<N> --max-length=<N>`

## custom
Uso le mie regole e la mia wordlist (presa magari dal sito dell'azienda).

**custom rules**:
* `c`: capitalize la prima lettera
* `A0`: inserisci prima
* `Az`: aggiungi alla fine
* `abc`: piazza **qui** la stringa **abc**
* `[xyz]`: prova **x**, poi **y** e poi **z**
* `@sXY`: sostituisci **X** con **Y**
![[Pasted image 20260312230831.png]]
![[Pasted image 20260312230839.png]]
![[Pasted image 20260312230850.png]]
**preprocessors**: sono i tool `[fileFormat]2john` e si occupano di
1. **strip**: dei dati inutili
2. **extract**: estrarre l'hashing crittografico o il sale
3. **format**: formatta l'hash in modo che jtr lo capisca

**hashcat**:
```bash
hashcat -m 0 -a 0 -o cracked.txt hashes.txt /usr/share/wordlists/rockyou.txt
```
* **-m 0**: MD5
* **-a 0**: attacco normale, modalita dizionario.
* **-o cracked.txt**: file di output per le password craccate

```bash
hashcat -a 6 example.dict '?d?d?d?d' --stdout
```
* **-a 6**: attacco con maschera sulle password del dizionario
* `?d?d?d?D`: maschera da applicare

```bash
hashcat -m 0 -a 1 –j ‘$_’ dict1.txt dict2.txt –stdout
```
* **-a 1**: combination mode
* **-j**: regola per la combinazione
* **dict1.txt e dict2.txt**: dizionari da combinare

## archivi e altri formati
* **fcrackzip**: `fcrackzip -u -b -v -D -p myWordlist.txt target.zip`. **Attacca un zip protetto da password**.
* `[format]2john` sono tool che attaccano il determinato `[formato]` protetto
