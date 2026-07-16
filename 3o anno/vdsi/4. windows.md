https://www.thehacker.recipes/
## AD
**Active Directory**: sistema organizzativo. Servizio di directory centralizzato.Usa **Identity and Exclusion Management (IAM)** per verificare gli accessi.

**Domain Controller**: autentica e autorizza dispositivi in una rete windows.

**LAN Manager Hash**: LM e' un algoritmo di hashing. Ora deprecato ma ancora usato.

**SAM(Security Accounts Manager)**:  database locale di un sistema windows standalone
**NTDS.dit**: È il database di **Active Directory**. Non contiene solo password, ma l'intera struttura del dominio (oggetti, gruppi, permessi). Si trova solo sui Domain Controller (DC).
## SAM
**SAM**: file database, che contiene le password criptate. Mantiene un **lock** sul file per accederlo.

(-) **Rivest Cipher 4**: cifrario e cripta gli hash usando la `bootkey`

(-) **Windows SYSTEM file**: `C:\Windows\repair`contiene un backup del `SYSTEM`. All'interno di questa cartella trovo il file `SAM` e `system` con la `bootkey`

(-) **Conclusione sulla vulnerabilita**: se ho accesso al filesystem di windows, posso decifrare il `SAM`
**(gemini) perche e' stato introdotto il backup?** e' un compromesso tra sicurezza e usabilita. Se si corrompe il filesystem ho bisogno del backup per recuperare i dati!

**estrarre la bootkey**: 
```bash
bkhive system xpkey.txt
```
* **system**: e' il `SYSTEM` file
* **xpkey.txt**: e' la destinazione

**decriptare il sam**:
```bash
samdump2 sam xpkey.txt
```
* **sam**: destinazione.
* **xpkey.txt**: la bootkey

**backup**: dato che il sam e' un backup, potrei non avere le password degli utenti piu nuovi.

**privilegi di sistema**: posso evitare il **lock** e accedere ai dati.

**RAM**: con alcuni tool posso recuperare le password crittografate dalla RAM

**john**: con john posso attaccare il dump delle password.

## LM e NTLM
**LM (LAN Manager) e NTLM (NT LAN Manager)**: quando ottengo il sam decriptato ci sono due hashing per la stessa password.

**LM**: e' crittograficamente debole. Trovo il plaintext indipendentemente dalla lunghezza e dall'entropia.
**NTLM**: crittograficamente piu forte.
**Windows XP**: usa entrambi i metodi per retrocompatibilita (?)

### (-) LM
![[Pasted image 20260312121858.png]]

**DES**: viene usato per crittografare le due meta di plaintext.
**Come si attacca**? *Devo criptare tutte le possibli combinazioni da 1 a 7 caratteri di stringhe finche non trovo lo stesso hash che sto attaccando.*

## NTLM o  NT Hash
**LSASS** (Local Security Authority Subsystem service): recupero le credenziali in cache per sessioni attive dalla memoria processo `lsass.exe`.

**Pass-the-hash**: 
* **auth via rete**: ho bisogno solo dell'hash NT e non della password originale.
* **conseguenza**: mi basta rubare l'hash dall'avversario

**mimikatz**: tool di **post exploitation** (sono gia all'interno della macchina).
* **dump di SAM**: `lsadump::sam SystemBkup.hiv SamBkup.hiv` estrae gli hash degli utenti (similmente a come fatto prima)
* **dump di LSASS**: 
	* `privilege::debug` prova a ottenere i permessi di debug
	* `sekurlsa::logonPasswords full` estrare le credenziali in hash

# Net-NTLM
**NT Hash**: e' l'hash memorizzato e applicato nel database.
**LM, NTLMv1, NTLMv2**: sono protocolli di autenticazione.

**Net-NTLMv1**: legacy basato su **challenge-response** auth protocolo
**challenge-response**: una challenge in cui devo provare la mia identita usando NT o LM Hash.

**attacco**: devo fare un **man in the middle**. 
**vulnerabilita**: NTLMv1 e' matematicamente debole.

**Net-NTLMv2**: algoritmo piu robusto matematicamente ma si attacca come **v1**.
* **usa HMAC-MD5**
* challenge variable length
* timestamp
* algoritmo piu complesso
![[Pasted image 20260312124917.png]]

**handshake**: 
![[Pasted image 20260312101209.png]]
![[Pasted image 20260312101257.png]]
## responder
**Attacchi ad AD**: faccio affidamento su attacchi man in the middle per fare lateral movement

**Obiettivo attacchi**: redirezionare il traffico , cosi da ottenere credenziali.

**redirezionare il traffico**: inganno il client affinche provi ad autenticarsi con la macchina dell'attaccante. Se il client sbaglia a digitare il nome di una cartella condivisa avviene una richiesta DNS che su un protocollo legacy puo' **essere attaccata**

**forced authentication attacks**: costringo la vittima a connettersi al mio serve.

**responder**: fa name poisoning per **forced authentication attaccks**
* **DNS fails**: la vittima fa una richiesta DNS usando un protocollo legacy. *responder gli dice di inoltrare il traffico a me.*
* **NTLMv2 handshake**: il client inizia l'handshake con responder.
	* **invia una sfida statica**: `1122334455667788
	* mi aspetto di ricevere il valore della sfida combinato con l'hash della password dell'utente da autenticare.
	* ricevo dunque l'hash mischiato ad altri dati statici.