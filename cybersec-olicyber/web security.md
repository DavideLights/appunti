## `requests`: ottenere il testo
```python
r = requests.get("URL HERE")
print(r.text)
```

`r.text`: HTTP response content.

##  `requests`: get parametrizzata

```python
r = requests.get("URL HERE", params={"id": "flag"})
print(r.text)
```

## `requests`: get con campi custom nell'header

```python
r = requests.get("URL HERE", headers={"X-Password": "admin"})
```

## `requests`: cookie

```python
r = requests.get("URL HERE", cookies={"password": "admin"})
```

> we send a cookie wich name is password and value admin.


## `requests`: Session cookie
> session e cookie: nella challenge viene richiesto utilizzare l'oggetto Session, per gestire lo stato della connessione.

> stato della connessione: in questa challenge e' necessario perche' vogliamo che `Session` gestisca per noi il cookie inviato dal server tramite `URL/cookie` e che alla successiva get lo specifichi per noi. 

```python
s = requests.Session()
r = s.get("URL HERE/cookie")
r = s.get("URL HERE/flag")
```

# `requests`, HEAD.
**perche sfruttarlo**? il metodo HEAD teoricamente dovrebbe comportarsi come GET per tutte le risorse. In pratica il server potrebbe essere configurato male e rilevare qualcosa.

**a cosa serve nei server**? a scaricare l'header per una risorsa grossa svariati gigabyte invece di fare direttamente il GET dell'intera risorsa.

## `requests`: POST
**Main Technical Terms:**
- **POST Request:** An HTTP method used to send data to a server inside the "body" of the request (unlike a GET request, which puts data visibly in the URL).
    
- **MIME (Multipurpose Internet Mail Extensions):** A standard used to identify the format of data sent over the internet, usually specified in an HTTP request's `Content-Type` header.
    
- **`application/x-www-form-urlencoded`:** The default MIME format browsers use when submitting HTML forms. It formats data into key-value pairs separated by `&` symbols (specifically `username=admin&password=admin` for this challenge) and converts spaces or special characters into URL-safe codes.

```python
r = requests.post("URL", data={"username": "admin", "password": "admin"})
```

## JSON post
```python
r = requests.post("URL", json={"username": "admin", "password": "admin"})
```

## OPTIONS
> Talvolta può essere interessante cercare di utilizzare intenzionalmente un verbo non supportato. Normalmente un server dovrebbe gestire richieste non supportate in maniera pulita, ma in presenza di configurazioni errate o errori di programmazione, utilizzare un metodo imprevisto può indurre un crash. I crash e più in generale le operazioni non anticipate possono rivelare informazioni interessanti che nell'utilizzo normale di un servizio web sono nascoste.

```python
r = requests.options("URL")

# now try unsupported methods, not shown in options header.
rput = requests.put("...")
rpatch = requests.patch("...")
print(rput.text, rput.headers)
print(tpatch.text, rpatch.headers)
```

# CSRF (Cross-site request forgery)
**scenario**: siti web dinamici che non sanno come controllare se una richiesta di autenticazione sia stata inviata intenzionalmente oppure no.

**cosa sfrutta**? la fiducia di un sito rispetto ad un'utente. (gemini: explain this better)

**esempio tipico in 4 passaggi**:
1. l'attaccante crea una richiesta contraffatta alla banca
	1. es: trasferisci da utente `A` a me `10.000$`.
2. l'attaccante invia la richiesta contraffatta come **collegamento ipertestuale** alla vittima, per esempio tramite mail.
3. la vittima apre la mail, clicca il link ed effettua la richiesta creata dall'attaccante.
4. il server della banca riceve la richiesta per conto della vittima. Per il server la vittima sara eventualmente autorizzatta ad effettuare la richiesta di trasferimento.
5. l'attaccante si piglia li sordi.
![Una richiesta falsificata](https://www.cloudflare.com/img/learning/security/threats/cross-site-request-forgery/forged-request.png "Una richiesta falsificata")

**cosa sfruttano le CSRF**?
1. siti web che autorizzano operazioni in base all'identita dell'utente.
2. sfruttano il browser della vittima che invia le richieste al server. Il server contiene eventualmente risorse sensibili da sfruttare.

**CSRF e GET**: una GET e' un'operazione che non cambia lo stato del server, quindi e' possibile al massimo solo carpire dati sensibili se autorizzati.

**CSRF e POST**: una POST invece cambia lo stato del server, queste operazioni devono essere adeguatamente prottete dal CSRF

**come difendersi**? usare token anti-CSRF
* SOP: consente richieste solo dalla stessa origine
* CORS: consente solo determinati tipi di richieste da un'origine diversa.
* Syncrhronizer token pattern: il server invia 
* Token cookie-to-header

## CSFR  challenge

```python
# because CSRF depends on cookie
s = requests.Session()
r = s.post("URL/login", json={"username":"admin", "password":"admin"})

csrf = r.json()['csrf']
for i in range(4):
print(csrf)
   r = s.get("URL/flag_piece", params={"index": i, "csrf"=csrf})
   print(r.text)
   csrf = r.json()['csrf']
```

> note: `r.json` is a method and not a member.