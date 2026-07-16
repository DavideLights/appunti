* **bandit11**: cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'*

### bandit 13 - SSH
https://help.ubuntu.com/community/SSH/OpenSSH/Keys

**private key**: si trova nel computer da cui faccio login, non deve essere mai condivisa. 

**Sfida SSH**: il protocollo prevede una sfida, che si puo risolvere solo se sono in possesso della private key, in modo da dimostrare la mia identita.

**public key**: si trova in `.ssh/authorized_keys` sul server di destinazione

**Perche' SSH usa crittografia pubblica**? Comunico al server la mia chiave pubblica cosi sa come criptare i messaggi per me. Ho una sola chiave per piu server, sono io che devo ricordare quella loro.

**Creare Chiavi RSA**:
```bash
mkdir ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t rsa
```
* **location**: path
* **passphrase**: password che protegge la chiave in caso venga rubata. Deve essere forte e immagazzinata in un password manager.
* `.ssh/id_rsa.pub` contiene la chiave pubbliche

**encryption level**: puo' essere di `2048 bit` (default) oppure `4096` usando l'opzione `-b 4096`

## connettermi a bandit14 usando la sua chiave privata
**generare chiave pubblica**: `ssh-keygen`

**ottieni la chiave privata**:
```bash
scp -P 2220 bandit13@bandit.labs.overthewire.org:/home/bandit13/sshkey.private b14sshkey.private
```

**permessi**:
```bash
chmod 600 b14sshkey.private
```

**login**:
```bash
ssh -i b14sshkey.private -p 2220 bandit14@bandit.labs.overthewire.org
```

# bandit 14
Per ottenere che tipo di socket ho su `30000`
```bash
ss -tulpn | grep 30000
```

Per inviare la richiesta:
```bash
nc localhost 30000
CTRL+V della password
```

# bandit 15
```bash
openssl s_client -connect localhost:30001
```

# bandit 16
```bash
nmap -p 31000-32000 -v -A -T4 localhost
```
* `-p 31000-32000`: range di porte
* `-v`: verboso
* `-A`: aggressive text
* `-T4`: timing stretto, non attendere troppo

# bandit 19-20
**setuid e setgid**: permette gli utenti di avviare un eseguibile con i permessi su file system del proprietario o del gruppo. Permette di elevare temporaneamente i permessi ad un utente nel contesto di esecuzione di un programma.

**chmod ricorsivamente**:
```bash
`find /path/to/directory -type d -exec chmod g+s '{}' '\'`
```


