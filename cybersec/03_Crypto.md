# 03. Cryptography

> [!abstract] Triage Crittografia
> 1. **Riconosci il formato**: Hex (`[0-9a-f]`), Base64 (`A-Za-z0-9+/=`), interi grandi (`long_to_bytes`), lista di decimali (`chr`).
> 2. **Identifica lo schema**:
>    - **Simmetrica a flusso / XOR**: chiave corta ripetuta, nonce riutilizzato (CTR/ChaCha20).
>    - **Simmetrica a blocchi (AES/DES)**: blocchi da 8 byte (DES) o 16 byte (AES). ECB (blocchi identici) vs CBC (IV + padding).
>    - **Aritmetica modulare / CRT**: più moduli $n_i$ e resti $a_i$ → Teorema Cinese del Resto.
>    - **Asimmetrica (RSA / DH)**: interi enormi ($n, e, c$ oppure $p, g, A, B$).

---

## 1. Encoding, Conversioni e Endianness

**Trigger**: Devi convertire tra stringhe, `bytes`, esadecimale, Base64 e interi giganti (tipico di RSA e PyCryptodome).

```python
from base64 import b64encode, b64decode
from Crypto.Util.number import long_to_bytes, bytes_to_long

# 1. Interi ASCII <-> Stringhe (chr / ord)
lst = [102, 108, 97, 103]
s = "".join(chr(y) for y in lst)       # "flag"
nums = [ord(c) for c in s]             # [102, 108, 97, 103]

# 2. Hex <-> Bytes
b = bytes.fromhex("666c6167")          # b"flag"
h = b.hex()                            # "666c6167"

# 3. Base64 <-> Bytes
raw = b64decode("ZmxhZw==")            # b"flag"
b64 = b64encode(b"flag").decode()      # "ZmxhZw=="

# 4. Interi <-> Bytes (nativo Python + Endianness)
n = int.from_bytes(b"flag", "big")     # 1718378855 (sinistra -> destra, standard rete/RSA)
b_big = n.to_bytes(4, "big")           # b"flag"
n_lit = int.from_bytes(b"flag", "little") # 1734437990 (destra -> sinistra, x86/x64)

# 5. Interi giganti <-> Bytes (senza dover calcolare la lunghezza n)
b_auto = long_to_bytes(n)              # b"flag"
n_auto = bytes_to_long(b"flag")        # 1718378855
```

> [!warning] Trappole comuni
> - Non chiamare `b.decode()` su byte arbitrari (es. ciphertext crudo): usa `b.decode('utf-8', errors='replace')` o lavora sempre con `bytes`.
> - In Python `int.to_bytes(length, byteorder)` richiede la lunghezza esatta: per numeri di dimensione ignota usa `long_to_bytes(n)` oppure `(n.bit_length() + 7) // 8`.

---

## 2. XOR & One-Time Pad (OTP)

**Trigger**: Ciphertext in hex/bytes, cifrari custom basati su `^`, oppure riutilizzo della stessa chiave su più messaggi (Many-Time Pad).

### Concetti chiave
- **Proprietà fondamentali**: $A \oplus A = 0$, $A \oplus 0 = A$, $(A \oplus B) \oplus B = A$.
- **Perché l'OTP con chiave ripetuta è rotto**: se ripeti una chiave corta $k$ su un messaggio lungo, puoi fare brute-force byte-per-byte (o per posizioni modulo $|k|$).
- **Riutilizzo della chiave OTP (Two-Time Pad)**: se cifri $M_1$ e $M_2$ con la **stessa** chiave $K$:
  $$C_1 \oplus C_2 = (M_1 \oplus K) \oplus (M_2 \oplus K) = M_1 \oplus M_2$$
  Se conosci una porzione di $M_1$ (es. `flag{`), fai `C1 ^ C2 ^ b"flag{"` per leggere i primi byte di $M_2$ (*crib dragging*).

### Snippet pronti

```python
# 1. Single-byte XOR brute-force (256 possibili chiavi: 0x00..0xFF)
cbytes = bytes.fromhex("104e137f425954137f74107f525511457f5468134d7f146c4c")

for k in range(256):
    m = bytes(b ^ k for b in cbytes)
    if all(32 <= x < 127 for x in m):  # Solo ASCII stampabile
        print(f"Key {k:#04x}: {m.decode()}")

# 2. Known-Plaintext Attack (recupera chiave ripetuta conoscendo il prefisso "flag{")
crib = b"flag{"
key_prefix = bytes(c ^ p for c, p in zip(cbytes, crib))
print("Prefisso chiave:", key_prefix)

# 3. XOR tra due buffer di lunghezza diversa (repeating-key XOR)
def xor_repeat(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
```

> [!warning] Trappola `range(255)` vs `range(256)`
> Un byte assume valori `0..255`: in Python `range(255)` si ferma a `254` e salta `0xFF`. Usa sempre `range(256)`.

---

## 3. Cifrari Simmetrici (DES, AES, ChaCha20) e Modalità

**Trigger**: Script Python con `Crypto.Cipher` (`DES`, `AES`, `ChaCha20`), errori di padding, blocchi ripetuti o modifica controllata di ciphertext (bit-flipping).

### Confronto rapido

| Caratteristica | DES | AES | ChaCha20 |
| :--- | :--- | :--- | :--- |
| **Tipo** | Cifrario a blocchi (rete Feistel) | Cifrario a blocchi (rete SPN) | Stream cipher (ARX: Add-Rot-XOR, 20 round) |
| **Blocco / Stato** | Blocco 64 bit (**8 byte**) | Blocco 128 bit (**16 byte**) | Stato 512 bit (**64 byte**, matrice $4\times 4$ word 32-bit) |
| **Chiave** | 64 bit (56 bit effettivi) | **128 / 192 / 256 bit** | **256 bit** (32 byte) + Nonce (64 o 96 bit) |
| **Padding** | Necessario (su multipli di 8B) | Necessario (su multipli di 16B) | **Non serve** (keystream troncato alla lunghezza di $P$) |
| **Side-channel** | S-Box (vulnerabile a cache-timing) | S-Box software (in hardware usa AES-NI) | **Cache-timing resistant** (solo ops ARX a tempo costante) |

### Padding Standard
- **PKCS#7** (default in PyCryptodome): se mancano $N$ byte, aggiunge $N$ volte il byte `N` (`data\x02\x02`, se già multiplo aggiunge un intero blocco `\x10`×16).
- **ANSI X.923**: riempie i primi $N-1$ byte con `\x00` e mette $N$ nell'ultimo byte (`data\x00\x02`).
- **ISO 7816-4**: aggiunge `\x80` seguito da `N-1` byte `\x00` (`data\x80\x00`).

### Modalità Operative e Vulnerabilità CTF

| Modalità | Equazione | Vulnerabilità tipica in CTF |
| :--- | :--- | :--- |
| **ECB** | $C_i = E_K(P_i)$ | **Senza IV, deterministico**: blocchi uguali danno ciphertext uguali; puoi riordinare/incollare blocchi. Attacco *Byte-at-a-Time* se c'è un prefisso controllato dall'utente. |
| **CBC** | $C_i = E_K(P_i \oplus C_{i-1})$, $C_0 = \text{IV}$<br>$P_i = D_K(C_i) \oplus C_{i-1}$ | **IV mancante**: senza IV non decifri $P_1$.<br>**CBC Bit-Flipping**: modificando $C_{i-1}$ in $C'_{i-1} = C_{i-1} \oplus P_i \oplus P'_i$, forzi $P_i \to P'_i$ (corrompendo $P_{i-1}$).<br>**Padding Oracle**: se il server rivela errori di padding, decifri tutto senza chiave. |
| **CTR** | $C_i = P_i \oplus E_K(\text{Nonce} \parallel i)$ | **Nonce Reuse**: se lo stesso `(key, nonce)` cifra due messaggi, $C_1 \oplus C_2 = P_1 \oplus P_2$ (identico a Two-Time Pad). |

### Snippet PyCryptodome pronto

```python
from Crypto.Cipher import AES, DES, ChaCha20
from Crypto.Util.Padding import pad, unpad

# DES in CBC (blocco 8 byte, padding X923)
key_des = bytes.fromhex("0123456789abcdef")
cipher = DES.new(key_des, DES.MODE_CBC)       # genera IV casuale (8 byte)
ct = cipher.encrypt(pad(b"text to encrypt", 8, style="x923"))
iv = cipher.iv                                # VA SALVATO/INVIATO per decifrare P_1!

# Decifratura DES-CBC
dec = DES.new(key_des, DES.MODE_CBC, iv=iv)
pt = unpad(dec.decrypt(ct), 8, style="x923")

# AES-CBC Bit-Flipping: cambia "user=bob" in "user=adm" nel blocco i usando il blocco i-1
# c_prev_mod = bytes(a ^ b ^ c for a, b, c in zip(c_prev, b"user=bob", b"user=adm"))
```

> [!warning] Regola d'oro per CBC e CTR
> - In **CBC**, chi decifra conosce $K$ e $C_1$, ma per ottenere $P_1 = D_K(C_1) \oplus \text{IV}$ **deve** ricevere anche `cipher.iv` (spesso prepended ai primi 8/16 byte del ciphertext: `iv = data[:16]; ct = data[16:]`).
> - In **ChaCha20**, mai riutilizzare lo stesso `nonce` con la stessa `key`.

---

## 4. Aritmetica Modulare: GCD, Euclide Esteso e Inversa

**Trigger**: Devi calcolare $a^{-1} \bmod n$ (es. chiave privata RSA $d$, cifrario Affine, Common Modulus Attack) o verificare se due numeri sono coprimi.

### Concetti chiave
- **GCD & Identità di Bézout**: per ogni $a, b \in \mathbb{Z}$, esistono $x, y \in \mathbb{Z}$ tali che:
  $$ax + by = \gcd(a, b)$$
- **Inversa Modulare**: $x$ è l'inversa di $a$ modulo $n$ ($ax \equiv 1 \pmod n$) **se e solo se** $\gcd(a, n) = 1$ ($a$ e $n$ sono coprimi).
- **Come trovarla a mano / con Bézout**: applica l'algoritmo euclideo esteso a $(a, n)$ per trovare $ax + ny = 1$. Riducendo modulo $n$, il termine $ny \equiv 0 \pmod n$ si annulla, quindi $ax \equiv 1 \pmod n \implies x \equiv a^{-1} \pmod n$.

### Applicazioni crittografiche principali
1. **RSA Key Generation**: dato $e$ coprimo con $\phi(n)$, calcoli $d = e^{-1} \bmod \phi(n)$.
2. **RSA Common Modulus Attack**: stesso messaggio $m$ cifrato con lo stesso $n$ e due esponenti coprimi $e_1, e_2$: trovi $s_1 e_1 + s_2 e_2 = 1$ con `egcd` e recuperi $m = c_1^{s_1} \cdot c_2^{s_2} \bmod n$.
3. **Cifrario Affine**: cifratura $E(x) = (ax + b) \bmod 26$, decifratura $D(y) = a^{-1}(y - b) \bmod 26$.
4. **CRT**: calcolo di $y_i = N_i^{-1} \bmod n_i$.

### Snippet pronto

```python
import math

# Built-in Python 3.8+ (veloce e gestisce moduli arbitrari)
g = math.gcd(a, n)
inv = pow(a, -1, n)   # Lancia ValueError se gcd(a, n) != 1

# Algoritmo Euclideo Esteso manuale: ritorna (g, x, y) t.c. a*x + b*y = g
def egcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

# Verifica: g, x, y = egcd(e, phi); d = x % phi
```

---

## 5. Teorema Cinese del Resto (CRT)

**Trigger**: Hai un sistema di congruenze con moduli coprimi a coppie $n_1, \dots, n_k$, oppure in RSA lo stesso messaggio $m$ è stato cifrato verso più destinatari con stesso esponente piccolo $e$ (es. $e=3$) e moduli diversi $n_i$.

### Enunciato & Intuizione
Siano $n_1, n_2, \dots, n_k$ interi positivi **coprimi a coppie** ($\gcd(n_i, n_j) = 1 \;\forall i \neq j$) e $N = \prod_{i=1}^k n_i$. Per qualsiasi $a_1, \dots, a_k$, il sistema:
$$\begin{cases} x \equiv a_1 \pmod{n_1} \\ \vdots \\ x \equiv a_k \pmod{n_k} \end{cases}$$
ammette **una ed una sola soluzione** $x \bmod N$.

- **Formula risolutiva**: per ogni $i$, definisci $N_i = \frac{N}{n_i}$ e risolvi $N_i y_i \equiv 1 \pmod{n_i}$ (cioè $y_i = N_i^{-1} \bmod n_i$):
  $$x \equiv \sum_{i=1}^k a_i \cdot N_i \cdot y_i \pmod N$$
- **Due letture pratiche**:
  1. **Ricostruzione**: conoscendo solo i resti $(r_1, r_2)$ di $x$ rispetto a moduli piccoli $(n_1, n_2)$, ricostruisci univocamente $x \bmod (n_1 n_2)$ (es. $7 \equiv 1 \pmod 3$ e $7 \equiv 2 \pmod 5 \leftrightarrow (1, 2) \bmod 15$).
  2. **Parallelizzazione / RSA-CRT**: in informatica puoi eseguire calcoli pesanti separatamente modulo $p$ e modulo $q$ (numeri grandi la metà) e poi ricombinare il risultato modulo $N = pq$ (usato da RSA per velocizzare la decifratura di ~4x).

### Snippet pronto (CRT + Hastad Broadcast)

```python
import math

def crt(remainders: list[int], moduli: list[int]) -> int:
    N = math.prod(moduli)
    x = 0
    for n_i, a_i in zip(moduli, remainders):
        N_i = N // n_i
        y_i = pow(N_i, -1, n_i)
        x = (x + a_i * N_i * y_i) % N
    return x

# Esempio Hastad's Broadcast Attack (RSA con e=3, 3 ciphertext c1,c2,c3 su n1,n2,n3)
# import gmpy2
# m_cubed = crt([c1, c2, c3], [n1, n2, n3])
# m, exact = gmpy2.iroot(m_cubed, 3)
```

---

## 6. RSA Step-by-Step e Attacchi Classici

**Trigger**: Vengono forniti $n, e, c$ (e talvolta $p, q$, hint su $\phi(n)$ o multipli cifrati).

### Funzionamento RSA
1. **Generazione chiavi**:
   - Scegli due primi grandi $p, q$ e calcola il modulo $n = p \cdot q$.
   - Calcola la funzione toziente di Eulero: $\phi(n) = (p - 1)(q - 1)$ (conta gli invertibili in $\mathbb{Z}_n^*$: tutti i numeri da $1$ a $n$ esclusi i multipli di $p$ e $q$).
   - Scegli esponente pubblico $e$ tale che $\gcd(e, \phi(n)) = 1$ (tipicamente `65537`).
   - Calcola esponente privato: $d \equiv e^{-1} \pmod{\phi(n)}$, quindi **$ed \equiv 1 \pmod{\phi(n)}$** (cioè $ed = 1 + k\phi(n)$).
2. **Cifratura**: $c \equiv m^e \pmod n$.
3. **Decifratura** (per il **Teorema di Eulero**: se $\gcd(a, n)=1$, allora $a^{\phi(n)} \equiv 1 \pmod n$):
   $$c^d \equiv (m^e)^d = m^{1 + k\phi(n)} = m \cdot (m^{\phi(n)})^k \equiv m \cdot 1^k \equiv m \pmod n$$

```python
from Crypto.Util.number import long_to_bytes, bytes_to_long

# Esempio completo RSA
p, q = 11, 7
n = p * q
phi = (p - 1) * (q - 1)
e = 7
d = pow(e, -1, phi)

m = 5
c = pow(m, e, n)
decrypted = pow(c, d, n)
```

> [!warning] Usa sempre `pow(base, exp, mod)`!
> Non scrivere mai `(base ** exp) % mod`: calcola prima un numero gigantesco in RAM bloccando il programma. `pow(a, b, n)` usa l'esponenziazione modulare veloce (*square-and-multiply*) in $O(\log b)$.

### Checklist Attacchi RSA in CTF

| Condizione osservata | Attacco | Soluzione rapida |
| :--- | :--- | :--- |
| $n$ piccolo (< 100 cifre) o noto | **Fattorizzazione diretta** | Cerca $n$ su [FactorDB](https://factordb.com) o usa `yafu` / `sympy.factorint(n)`. |
| $e$ piccolo (es. `3`) e $m^e < n$ | **Small Public Exponent** | Non c'è riduzione modulo $n$: calcola la radice $e$-esima intera `gmpy2.iroot(c, e)[0]`. |
| $p$ e $q$ molto vicini ($\|p-q\|$ piccolo) | **Fattorizzazione di Fermat** | Partendo da $a = \lceil\sqrt{n}\rceil$, incrementa $a$ finché $a^2 - n = b^2$ è quadrato perfetto; poi $p = a+b, q = a-b$. |
| Stesso $m$, stesso $e$ piccolo, $e$ moduli $n_i$ diversi | **Hastad's Broadcast Attack** | Risolvi CRT sui $(c_i, n_i)$ per avere $m^e$, poi estrai la radice $e$-esima. |
| Stesso $m$, stesso $n$, due esponenti $e_1, e_2$ coprimi | **Common Modulus Attack** | Trova $s_1 e_1 + s_2 e_2 = 1$ con `egcd`; $m = (c_1^{s_1} \cdot c_2^{s_2}) \bmod n$ (se $s_i < 0$, inverti prima $c_i$). |
| $n$ è primo ($p$) o potenza ($p^k$) | **$\phi(n)$ degenere** | Se $n=p$ primo: $\phi(p)=p-1$. Se $n=p^2$: $\phi(p^2)=p(p-1)$. Se multi-prime: $\phi(n)=\prod(p_i-1)$. |
| $e$ enorme e $d$ molto piccolo ($d < \frac{1}{3} n^{1/4}$) | **Wiener's Attack** | Frazioni continue su $\frac{e}{n}$ (libreria `owiener`). |
| Ti danno un oracolo di decifratura (es. non decifra $c$) | **RSA Malleability (Blinding)** | Chiedi di decifrare $c' = (c \cdot 2^e) \bmod n$, ottieni $m' = 2m \bmod n$, poi $m = m' \cdot 2^{-1} \bmod n$. |

### Snippet Fermat & Common Modulus

```python
import math
from Crypto.Util.number import long_to_bytes

# Fermat Factorization (quando p e q sono vicini)
def fermat_factor(n: int) -> tuple[int, int]:
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    while True:
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            return a - b, a + b
        a += 1

# Common Modulus Attack
def common_modulus(n: int, e1: int, e2: int, c1: int, c2: int) -> int:
    g, s1, s2 = egcd(e1, e2)
    assert g == 1
    part1 = pow(c1, s1, n) if s1 >= 0 else pow(pow(c1, -1, n), -s1, n)
    part2 = pow(c2, s2, n) if s2 >= 0 else pow(pow(c2, -1, n), -s2, n)
    return (part1 * part2) % n
```

---

## 7. Diffie-Hellman (DH) & Hashing / PRNG

### Diffie-Hellman
**Trigger**: Parametri pubblici $(p, g)$ e chiavi scambiate $A = g^a \bmod p$, $B = g^b \bmod p$. Il segreto condiviso è $S = B^a \bmod p = A^b \bmod p = g^{ab} \bmod p$.
- **Attacchi comuni**:
  - $p$ piccolo o $p-1$ composto da fattori piccoli (*Pohlig-Hellman* / BSGS in SageMath `discrete_log()`).
  - **Parameter tampering / MitM**: se puoi forzare $A=1$ o $A=p$ o $A=0$, il segreto condiviso diventa prevedibile ($1$ o $0$).

### Hashing & PRNG Python
- **Hash per carattere / password deboli**: se trovi una lista di hash SHA-256/MD5 di singoli caratteri o parole comuni, genera una lookup table in Python:
  ```python
  import hashlib, string
  lut = {hashlib.sha256(c.encode()).hexdigest(): c for c in string.printable}
  ```
- **`random` di Python (`Mersenne Twister MT19937`)**: **NON è crittograficamente sicuro**.
  - Se il seed deriva da `int(time.time())`, fai brute-force sui secondi attorno all'orario della challenge.
  - Con `624` output consecutivi a 32-bit di `random.getrandbits(32)` puoi ricostruire lo stato interno e predire il futuro (libreria `randcrack`).
