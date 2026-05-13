**modello client-server**:
![[Pasted image 20260511233337.png]]
**come accedo al servizio in client-server**? devo conoscere ip del server e porta del servizio.

**http**:
![[Pasted image 20260511233542.png]]
* `cookie`: con `Set-Cookie` il server mi dice qual'e' il mio identificativo. Alla richiesta successiva, specifico quel cookie.
* `POST`: con post invio i dati al server, in questo caso i dati di login e specifico a quale risorsa inviare i dati.
* `javascript`: il web browser del client esegue solo codice javascript
* `codice server`: il server puo' eseguire il cazzo che gli pare basta che risponde al client con codice `javascript`

## OWASP top ten
**cos'e**'? un documento con gli standard di sicurezza per sviluppatori e la sicurezza per le web app

## Di chi mi devo fidare?
**client**: posso fidarmi del client, questo potrebbe eseguire programmi malevoli che aggirano controlli che il server impone sulla pagina web che costruisce in risposta. **il server deve sempre controllare l'input utente!**
* `header fields` e `cookie`: vanno controllati!
* `query`: i valori nelle query `HTTP` devono essere controllati!

## enumerazione di un folder
**GET**: posso usarlo per ottenere in risposta i contenuti di una directory o di un file (gemini controlla che dico)
* **risposta positiva**: esiste il file o la directory
* **forbidden**: esiste ma non posso accederci

## codici HTTP
* **continue 100**: vuol dire che la richiesta e' stata interrotta lato server e deve continuarla il client. 
* **successful 200**: vuol dire che la richiesta e' soddisfatta con successo
* **multiple choices 300**: tanti significati, in generale la richiesta non e' stata completata, ma non c'e' un vero e proprio errore
* **bad request 400**: vuol dire che la richiesta e' scritta male o il server non l'ha capita proprio
* **internal server error 500**: il client non ha fatto nulla di sbagliato, ma il server ha incontrato un'errore inaspettato, dunque non ha completato la richiesta

## robots
**che pagine dovrebbe non visitare un web-crawler**? su `/robots.txt` e' descritto tutto!
```robots.txt
User-agent: *
Disallow: /private-directory/
```
* `User-agent` e' verso chi applicare la regola
* `Disallow`: indica su quale directory applico la regola!

## Enumerare file e cartelle
```bash
dirbuster -u http://example.com/ -l /usr/share/wordlists/your_wordlist -e php,txt
```


```bash
dirsearch -r -f -u http://example.com/ -w
/usr/share/wordlists/your_wordlist -e php,txt
```

```bash
gobuster dir -u http://example.com/ -w
/usr/share/wordlists/your_wordlist -x php,txt
```


# enumerare parametri
**parametri generici inline**:
```bash
wfuzz -c -z file,/usr/share/wordlists/your_wordlist --hh 92
"http://example.com/admin.php?FUZZ='"
```


**login forms**:
```bash
hydra -t 16 -l user -P /usr/share/wordlists/your_wordlist http-form-post://example.com/admin:username=^USER^&password=^PASS^
```


## host virtuali
**cos'e'?** stesso indirizzo ip, ma domini diversi
* `http://subdomain1.example.com` su `160.151.102.30`
* `http://subdomain2.example.com` su `160.151.102.30`

**e cosa fanno**? nonostante l'ip sia lo stesso, il servizio offerto in `http` e' differente. potrebbero dunque rispondermi con pagine totalmente differenti.


**enumare host**:
```bash
gobuster vhost -u http://example.com/ -w
/usr/share/wordlists/your_wordlist
```

```bash
wfuzz -w /usr/share/wordlists/your_wordlist --hh 92
-u http://example.com/ -H “HOST: FUZZ.example.com”
```


## git
`git-dumper`: script python che fa il dump di un repo git.
**perche?** nella storia del repo potrebbero esserci informazioni utili sulla struttura di un sito web.