# 06. Recon, Enumerazione & Servizi

> [!abstract] Workflow Recon Macchina / Servizio
> 1. **Scansione porte**: `nmap -sV -sC -T4 <IP>` (poi `-p-` per tutte le 65535 porte, `-sU` per UDP).
> 2. **Virtual Host (`/etc/hosts`)**: se scopri domini `.htb`/`.local` (da redirect HTTP, certificati TLS, email), aggiungili subito a `/etc/hosts`.
> 3. **Enumerazione Web**: `gobuster` / `ffuf` su directory, estensioni (`.php`, `.bak`, `.txt`) e vhost.
> 4. **Servizi esposti**: NFS (`2049`), SMB (`445`), MySQL/MariaDB (`3306`), POP3/IMAP (`110/995`, `143/993`).

---

## 1. `nmap` (Port Scanning & Script NSE)

**Trigger**: Hai un IP target e devi scoprire porte aperte, servizi, versioni e misconfigurazioni note.

| Flag | Significato | Quando usarla |
| :--- | :--- | :--- |
| `-sS` | TCP SYN scan (default con `sudo`) | Scansione veloce senza completare l'handshake TCP. |
| `-sV` | Service/Version detection | Identifica software e versione esatta (es. `MariaDB 10.x`, `OpenSSH`). |
| `-sC` | Script NSE di default | Controlla accesso anonimo FTP/SMB, titoli HTTP, certificati TLS. |
| `-p-` | Tutte le porte (`1..65535`) | Indispensabile se i servizi girano su porte alte non standard. |
| `-sU` | UDP scan | Lento, ma necessario per DNS (`53`), SNMP (`161`), TFTP (`69`). |
| `-T4` / `-Tn` | Timing template ($n \in [0..5]$) | Velocizza (`-T4` su LAN/VPN) o rallenta (`-T2` se c'è rate-limit/IDS). |

```bash
# 1. Scansione iniziale rapida con versioni e script default
nmap -sV -sC -T4 <IP> -oN nmap_init.txt

# 2. Scansione completa di tutte le porte TCP
nmap -p- --min-rate 3000 -T4 <IP>

# 3. Scansione UDP sulle porte principali
sudo nmap -sU --top-ports 50 <IP>

# 4. Script NSE mirati (es. NFS)
nmap -p 111,2049 --script=nfs-showmount,nfs-ls,nfs-statfs <IP>
```

---

## 2. Web Fuzzing (`gobuster`, `ffuf`) & `curl`

**Trigger**: C'è un server HTTP/HTTPS e vuoi trovare endpoint nascosti, file di backup o sottodomini/VHost.

### `gobuster` & `ffuf`
```bash
# Directory & file busting con estensioni (-x)
gobuster dir -u http://10.129.108.9/ \
  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -x php,txt,html,bak

# Alternativa più veloce con ffuf (filtra codici o dimensioni pagina ripetitive con -fc / -fs)
ffuf -u http://TARGET/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -fc 404

# Virtual Host / Subdomain fuzzing (fondamentale quando vedi un dominio tipo target.htb)
ffuf -u http://target.htb -H "Host: FUZZ.target.htb" \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -fs <SIZE_DEFAULT>
```

### `curl` Avanzato (Cookie, Header, Redirect)
```bash
# Segui redirect (-L), mostra header di risposta (-i), silenzioso (-s)
curl -i -s -L http://TARGET/

# Salva i cookie ricevuti (-c) durante un login POST e riutilizzali (-b)
curl -c cookies.txt -X POST "http://TARGET/login" -d "username=admin&password=Password1"
curl -b cookies.txt "http://TARGET/dashboard"

# Invia JSON o header custom
curl -s -X POST "http://TARGET/api" -H "Content-Type: application/json" -d '{"id":1}'
```

---

## 3. Database: MariaDB / MySQL Client

**Trigger**: Porta `3306` esposta o accesso al DB da terminale dopo aver ottenuto credenziali.

```bash
# Connessione (ATTENZIONE: nessuno spazio tra -p e la password!)
mysql -h <IP_O_HOST> -u root -p'password'

# Se il server non supporta TLS/SSL o fallisce la verifica certificato:
mysql -h <IP_O_HOST> -u root -p'password' --skip-ssl
```

### Comandi SQL Essenziali dopo il Login
```sql
SHOW DATABASES;             -- Lista tutti i DB (plurale!)
USE nome_db;                -- Entra nel database target
SHOW TABLES;                -- Lista le tabelle nel DB corrente
DESCRIBE nome_tabella;      -- Mostra colonne e tipi (equivale a SHOW COLUMNS FROM tbl;)
SELECT * FROM nome_tabella; -- Legge i dati
```

> [!note] Database di sistema sempre presenti in MariaDB / MySQL
> `information_schema` (metadati su tutte le tabelle/colonne), `mysql` (utenti e hash password), `performance_schema` (metriche runtime), `sys` (nelle versioni recenti).

---

## 4. Network Shares: SMB (`445`) & NFS (`2049`)

### SMB (`microsoft-ds`, porta `445`)
**Trigger**: Porta `445` aperta su Windows o Samba Linux.

```bash
# Elenca le share disponibili senza password (null session)
smbclient -L //<IP> -N

# Connettiti a una share specifica (fornisce shell stile FTP: ls, cd, get, mget)
smbclient //<IP>/WorkShares -N
# Con utente specifico:
smbclient //<IP>/WorkShares -U username
```

### NFS (`rpcbind 111`, `nfs 2049`)
**Trigger**: Porta `2049` esposta su Linux.

```bash
# 1. Lista i volumi esportati dal server
showmount -e <IP>

# 2. Monta in locale (ATTENZIONE ai due punti ":" tra IP e path remoto!)
sudo mkdir -p /mnt/nfs
sudo mount -t nfs <IP>:/srv/nfs/onboarding /mnt/nfs

# 3. Smonta a fine analisi
sudo umount /mnt/nfs
```

---

## 5. Mail & Servizi TLS Raw (`openssl s_client`)

**Trigger**: Porte POP3S (`995`), IMAPS (`993`), SMTPS (`465`) o servizi custom cifrati via TLS.

```bash
# Connessione interattiva TLS (usa -crlf per inviare \r\n richiesto da POP3/SMTP/HTTP!)
openssl s_client -connect <IP>:995 -crlf -quiet
```

### Comandi POP3 essenziali (una volta connesso)
```text
USER kevin
PASS Enigma2024!
LIST          # Elenca ID e dimensione in byte dei messaggi
retr 1        # Scarica il messaggio 1 (alcuni server accettano solo lowercase o uppercase)
QUIT
```

---

## 6. Listener & Gestione Shell Interattiva (PTY Upgrade)

**Trigger**: Sessione interattiva grezza ottenuta su terminale remoto (es. netcat/socket) priva di tab-completion, `Ctrl+C` sicuro o editor funzionanti.

```bash
# 1. Listener in ascolto sulla porta locale 4444
nc -lvnp 4444

# 2. Upgrade a TTY completa sulla sessione remota (eseguire dentro la sessione remota)
python3 -c 'import pty; pty.spawn("/bin/bash")'

# 3. Sospendi la sessione (Ctrl+Z), imposta il terminale locale in raw mode e riprendi (fg):
#    stty raw -echo; fg
#    export TERM=xterm-256color
```
