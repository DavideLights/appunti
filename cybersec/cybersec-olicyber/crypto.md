## 1. `chr`

```python
lst = [...]
# chr: da intero a char
x = [chr(y) for y in lst]
print(''.join(x))
```

`join` example:
```python
myTuple = ("John", "Peter", "Vicky")
x = "#".join(myTuple)
# John#Peter#Vicky
```

## 3. base 64

```python

int.from_bytes(b, endianess)

(z).to_bytes(n, endianess)
# n: numero di bytes
```
* `endianess='big'`: sinistra verso destra
* `endianess='little'`: viceversa

```python
from base54 import b64decode

part1 = b64decode('hex64string')
part2 = (integer goes here).to_bytes(20, 'big')
print(part1.decode(''))
```

# 4. bruteforce
questo script e' il motivo per cui non si puo prendere una chiave corta, ripeterla per generare una chiave da usare per OTP su un messaggio lungo.

```python
ciphertext = '104e137f425954137f74107f525511457f5468134d7f146c4c'
cbytes = bytes.fromhex(ciphertext)
clen = len(cbytes)


for i in range(255):
    m = ''.join([chr(b^i) for b in cbytes])
    if m.isascii():
        print(m)
    

```


## 07. DES

```python
import Crypto.Cipher
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

text = "text to encrypt"
key = bytes.fromhex('here goes the key in hex format')
cipher = DES.new(key, DES.MODE_CBC)

padded_text = pad(text.encode(), 8, style='x923')

ciphertext = cipher.encrypt(padded_text)
```

* DES: e' una rete Feistel
* `CBC`: $C_i = E_K(P_i \oplus C_{i-1})$
* `X923`: riempie i primi $N-1$ byte mancanti con `\x00`, e scrive nell'ultimo byte il numero $N$ di byte mancanti.
	* es con padding di 1 byte: `data\x01`
	* es con padding di 2 byte: `data\x00\0x02`

> [!error] `cipher.iv`
> Per decifrare il primo byte bisogna inviare insieme a `cipher.encrypt` il valore `cipher.iv` scelto randomicamente dalla classe `DES`. Nella modalita CBC si ha che
> * $P_1 = D_K(C_1) \oplus \text{IV}$
> * dunque chi decifra conosce $K$ e $C_1$ ma ha bisogna anche di $IV$


**ChaCha20**:
* **cifrario a blocchi**: fa passare il plaintext dentro la rete feistel per manipolarlo
* **stream cipher**: combina il plaintext tramite XOR con un flusso di byte pseudo-casuali.



|                   | cifrario a blocchi (es: AES)                                                   | chacha20                                                                                                                    |
| ----------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| **padding**       | **padding necessario**: poiche elaborano messaggi a blocchi di lunghezza fissa | **non serve**: sebbene le chiavi sono calcolate a blocchi, queste possono essere **troncate** alla lunghezza del messaggio. |
| **non linearita** | Tramite l'uso di SBOX, vulnerabile ad attacchi sulla cache della CPU.          | 3 operazioni (ADD, ROT, XOR) da applicare su **20 round**, su una matrice 4x4 di parole a 32-bit.                           |
| **efficienza**    | **alta**, uso di istruzioni CPU dedicate per le operazioni di AES.             | **ancora meglio di AES**: usa esclusivamente operazioni ARX a 32-bit e su registri standard per le CPU.                     |
| **chiave**        | dimensione variabile                                                           | 256-bit                                                                                                                     |
| **stato**         | matrice da 16 byte                                                             | matrice di 64 byte                                                                                                          |

> **cache timing resistance**: chacha20 non utilizza la SBOX ma una matrice di numeri molto piu piccola. Inoltre utilizza esclusivamente operazioni che sulla CPU impiegano sempre lo stesso tempo per essere eseguite. Dunque attacchi sulla cache o basati sul tempo di risposta non rivelano informazioni.


# 09 inversa e gcd

> [!note] fare gli appunti qui e farsi spiegare da gemini le applicazioni crittografiche piu importanti 


# 10 teorema cinese del resto

**Teorema cinese del resto**: 
* siano $n_1,n_2, \dots, n_k$ interi positivi, coprimi a coppie.
	* $\gcd(n_i, n_j) = 1 \forall i \neq j$
* sia $N$ il prodotto di questi $n_i$
* allora per qualsiasi $a_1, a_2, ..., a_k$
* il sistema di congruenze lineari:

$$\begin{cases} x \equiv a_1 \pmod{n_1} \\ x \equiv a_2 \pmod{n_2} \\ \vdots \\ x \equiv a_k \pmod{n_k} \end{cases}$$
* ammette una ed una sola soluzione $x \mod N$

**Come si risolve il sistema**?
* prendi tutti gli $N_i = \frac{N}{n_i}$
	* **es**: sia $N=n_1 n_2 n_3$
	* $N_1 = n_2 n_3$
	* $N_2 = n_1 n_3$
	* $N_3 = n_1 n_2$
* risolvi tutte le congruenze $N_i y_i \equiv 1 \mod n_i$ per $y_i$ incognita
* allora $x = \sum_i N_i \cdot y_i \cdot a_i$

ragionando a ritroso, il teorema cinese del resto ci da due idee potenti, la prima:
* prendi $x \in N$ e assumiamo $N=n_1 \cdot n_2$
* allora posso esprimere ed identificare unicamente $x$ come la tupla $(r1,r2)$ dei resti di $x$ rispettivamente in $n_1$ ed $n_2$.
* **es**: $N=15$ con $n_1=3$ ed $n_2=5$
	* sia $x=7$, allora $7 \equiv 1 \mod 3$ ed $7 \equiv 2 \mod 5$. dunque posso rappresentarlo come $(1,2)$, 
	* **significato 1**: il resto della divisione per 3 ed il resto per la divisione per 5
* **significato 1**? se so che $x$ ha resto $r1$ in mod $n1$ ed resto $r2$ in mod $n2$, allora posso facilmente capire chi e' $x \mod N$.
* **significato 2**: ogni resto per $N$ corrisponde una tupla di resti per i numeri $n1,n2,n3,...$ t.c. $N=n1\cdot n2\cdot n3\cdot...$ e siano comprimi tra loro. 

A cosa serve nei computer? posso parallelizzare i calcoli in $\mod N$ lavorando indipendentemente su $\mod n1, \mod n2, ...$ unendo alla fine i risultati.


**Challenge**: si risolve applicando la procedura per risolvere il sistema mostrato sopra.
```python
n = [lista dei moduli]
N = prod(n)
a = [lista delle soluzioni delle congruenze]

x = 0
for h,k in zip(n,a):
	hinv = pow(N//h, -1, h)
	x = (x + (hinv * N//h * k)) % N
```


## 11 RSA step by step
* `p=11, q=7`
* allora $n=77$
* scelgo $m=5$
* $\phi(n)=60= \phi(11)\phi(7)= 10\cdot 6$
* infatti in mod 77 gli invertibili sono gli interi da 1 a 77 esclusi i multipli di 7 e di 11
	* ossia: `7, 14, 21, ..`
	* ossia: `11,22,33, ..`
	* quindi, 60 numeri.
* **chiave pubblica**: ora vogliamo scegliere $e: \phi(n) \text{ coprimo con } e$
* **chiave privata**: di conseguenza scegliamo $d \equiv e^{-1} \mod \phi(N)$
* **cifriamo il messaggio**: $m^e \mod n$
* **teorema di eulero**: siano $a,n$ coprimi, allora $a^{\phi(n)} =1 \mod n$
	* **nota**: vogliamo $e$ coprimo con $\phi(n)$ per poterlo invertire. 
* **decifrare il mesaggio**: riceviamo $c=m^e$, allora $c^d = m^{ed}$, ed $m^{ed} \mod N$  e' $m$.
	* nota $d \equiv e^{-1} \mod \phi(N)$, quindi $ed\equiv0 \mod \phi(N)$


> [!error] `pow`
> Quando si calcolano le potenze enormi in modulo in python conviene usare `pow` invece di `a ^^ b % c`. `pow` utilizza un'algoritmo molto piu efficiente

come si trova l'inversa a mano l'inversa di $x \mod n$? fai algoritmo euclideo esteso e trova la soluzione $ax + by$, dove $x$ e l'incognita originale. allora l'inversa e' $a$ mentre $by$ si annulla in $\mod n$ poiche $y=n$.f