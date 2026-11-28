# 04. Network Security, TLS & Forensics

> [!abstract] Triage `.pcap` / `.pcapng` (Primi 60 Secondi)
> 1. **Statistiche generali**: `Statistics → Protocol Hierarchy` e `Statistics → Conversations` (scopri subito quali protocolli e IP parlano).
> 2. **Ricerca testuale veloce**: filtro `frame contains "flag"` o regex case-insensitive `frame matches "(?i)flag\\{"`.
> 3. **Commenti nascosti**: `pkt_comment` per commenti sui singoli pacchetti, oppure `Statistics → Capture File Properties` per commenti globali del file.
> 4. **File trasferiti**: `File → Export Objects → HTTP` (o `SMB` / `TFTP` / `IMF`).
> 5. **Ricostruzione flussi**: Tasto destro su un pacchetto → `Follow → TCP Stream` (o `UDP` / `HTTP` / `TLS Stream`).

---

## 1. Wireshark: Filtri e Ispezione

**Trigger**: Analisi di un file `.pcap` / `.pcapng` per estrarre credenziali, file, comandi o flag nascoste in header/payload/DNS.

### Tabella Filtri Essenziali (Display Filters)

| Obiettivo | Filtro Wireshark | Note operative |
| :--- | :--- | :--- |
| **Solo traffico HTTP** | `http` | Vedi richieste `GET`/`POST`, URI, User-Agent e risposte. |
| **Solo POST HTTP** | `http.request.method == "POST"` | Utile per trovare login form o upload di file. |
| **DNS per sorgente** | `dns && ip.src == 192.168.100.3` | Oppure `ip.src_host == ...`; controlla query anomale (DNS exfiltration nei sottodomini). |
| **Commenti nei pacchetti** | `pkt_comment` | Mostra solo i pacchetti con commento allegato. |
| **Contenuto esatto (case-sensitive)** | `frame contains "Pwn all the things!!!"` | Cerca byte/stringa ovunque nel frame (header + payload). |
| **Ricerca Regex (case-insensitive)** | `frame matches "(?i)(flag\|ctf)\\{"` | Ideale se non sai maiuscole/minuscole o formato esatto. |
| **Isolare uno stream TCP/UDP** | `tcp.stream eq 1` / `udp.stream eq 0` | Usa le frecce nella finestra `Follow Stream` per scorrere tutte le conversazioni. |
| **Traffico ICMP (Ping exfil)** | `icmp && icmp.type == 8` | Controlla `data.data` dentro i pacchetti Echo Request (spesso contengono flag 1 byte alla volta). |
| **Tastiera/Mouse USB (CTF Misc/Net)** | `usb.capdata` oppure `usbhid.data` | Keystroke injection o keylogger su bus USB (`HID` interrupt). |
| **Escludere rumore** | `!(arp || mdns || ssdp || nbns)` | Pulisce la vista dal traffico di broadcast locale. |

### Azioni Rapide nell'Interfaccia
- **Convertire byte grezzi (`Data`) in testo leggibile**:
  - Nel pannello centrale (Packet Details), espandi `Data (...)` → guarda il campo `Text:` oppure fai **tasto destro su `Data` → `Show Packet Bytes...` → seleziona `Show data as: ASCII`** (oppure `YAML` / `Hex Dump` / `Raw` per salvare).
- **Follow Stream con formato giusto**:
  - Tasto destro sul pacchetto → `Follow → TCP Stream` (o `UDP Stream`). In basso a destra cambia `Show data as` tra `ASCII`, `Hex Dump`, `Raw` (per salvare binari) o `C Arrays`.
  - Per estrarre solo un lato della comunicazione (es. solo risposta server), usa il menu a tendina `Entire conversation` in basso.

---

## 2. Automazione da Terminale: `tshark` & `scapy`

**Trigger**: Il `.pcap` ha decine di migliaia di pacchetti, oppure la flag è spezzettata (un carattere per pacchetto DNS, ICMP, porta TCP o byte in campi custom).

### `tshark` (Wireshark da CLI)

```bash
# 1. Cerca flag in tutto il pcap (ASCII / Hex)
tshark -r capture.pcapng -Y 'frame matches "(?i)flag"'

# 2. Estrai tutte le query DNS (tipico per DNS exfiltration)
tshark -r capture.pcapng -Y "dns.flags.response == 0" -T fields -e dns.qry.name

# 3. Estrai payload HTTP POST o User-Agent
tshark -r capture.pcapng -Y "http.request" -T fields -e http.request.method -e http.request.uri -e http.user_agent

# 4. Estrai payload dati TCP/UDP in esadecimale (uno per riga)
tshark -r capture.pcapng -Y "udp.port == 9000" -T fields -e data.data | xxd -r -p

# 5. Segui uno stream TCP direttamente da terminale
tshark -r capture.pcapng -q -z follow,tcp,ascii,0
```

### `scapy` (Python per parsing custom)

```python
from scapy.all import rdpcap, TCP, UDP, ICMP, DNSQR, Raw

pkts = rdpcap("capture.pcapng")

# Esempio: estrai payload Raw da pacchetti TCP verso porta 9001
out = b""
for p in pkts:
    if p.haslayer(TCP) and p[TCP].dport == 9001 and p.haslayer(Raw):
        out += p[Raw].load
print(out)

# Esempio: estrai nomi query DNS
for p in pkts:
    if p.haslayer(DNSQR):
        print(p[DNSQR].qname.decode())
```

---

## 3. TLS 1.3: Handshake e Decifratura Traffico

**Trigger**: Traffico cifrato (`TLSv1.2` / `TLSv1.3`) in un `.pcap` accompagnato da un file `keylog.txt` (SSLKEYLOGFILE) o da una chiave privata RSA (`server.key`), oppure domande di protocollo su `ClientHello` / `SNI` / `ALPN` / certificati.

### Come funziona l'Handshake TLS 1.3 (con Perfect Forward Secrecy)
1. **Step 1 — Negoziazione & Random**:
   - Client (`C`) e Server (`S`) generano ciascuno un valore `Random` (32 byte) e se li inviano in chiaro (`ClientHello` / `ServerHello`), insieme a cipher suite, `SNI` (dominio richiesto) e `ALPN` (protocollo applicativo, es. `h2`, `http/1.1`).
2. **Step 2 — Scambio chiavi effimere (`key_share`)**:
   - `C` e `S` generano ciascuno una coppia **(chiave pubblica, chiave privata)** effimera per **ECDHE** (Elliptic Curve Diffie-Hellman Ephemeral).
   - Il campo `key_share` inviato in chiaro contiene la **chiave pubblica**; la chiave privata resta esclusivamente in RAM.
3. **Step 3 — Shared Secret & Forward Secrecy**:
   - Combinando la propria chiave privata con la `key_share` pubblica ricevuta, `C` e `S` ottengono lo stesso **shared secret**.
   - Subito dopo eliminano la chiave privata effimera dalla RAM (per questo anche rubando in futuro la chiave del certificato del server non si può decifrare il traffico passato).
4. **Step 4 — Key Schedule (HKDF) e Cifratura AEAD**:
   - L'algoritmo **HKDF** (*HMAC-based Key Derivation Function*) deriva dallo shared secret le chiavi di sessione (per handshake e traffico applicativo).
   - Il traffico applicativo viene cifrato con cifrari simmetrici **AEAD** (es. **AES-GCM** o **ChaCha20-Poly1305**), **non** con RSA.
   - *(Nota: la chiave asimmetrica RSA/ECDSA del certificato serve solo in `CertificateVerify` per firmare l'handshake e **autenticare** l'identità del server, non per cifrare i dati).*

### Decifrare TLS catturato in Wireshark
Apri `Edit → Preferences → Protocols → TLS`:
- **Caso A — Hai un file `keylog` (`SSLKEYLOGFILE`, funziona per TLS 1.2 e TLS 1.3)**:
  - Imposta il path del file in **`(Pre)-Master-Secret log filename`**.
  - Un keylog standard contiene righe come `CLIENT_RANDOM <hex> <hex>` (TLS 1.2) o `CLIENT_HANDSHAKE_TRAFFIC_SECRET` / `CLIENT_TRAFFIC_SECRET_0` (TLS 1.3).
  - Wireshark decifrerà automaticamente tutti i pacchetti e mostrerà il protocollo interno (es. `HTTP` / `HTTP2`).
- **Caso B — TLS 1.2 con scambio chiavi RSA statico (no ECDHE) e hai la chiave privata del server (`server.key`)**:
  - Aggiungi IP, porta, protocollo (`http`) e path del `.pem`/`.key` in **`RSA keys list`**.

> [!warning] Trappola comune TLS
> Se la cipher suite negoziata usa `ECDHE` (es. `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` o qualsiasi TLS 1.3), la sola chiave privata RSA del server **non basta** a decifrare il traffico: serve per forza il `SSLKEYLOGFILE` (oppure uno scambio TLS 1.2 `TLS_RSA_*` senza `ECDHE`/`DHE`).

### Ispezione certificati e connessioni TLS da terminale
```bash
# Connettiti a un servizio TLS e vedi certificato, SNI e output raw
openssl s_client -connect host:443 -servername target.domain -crlf

# Ispeziona un certificato locale .pem / .crt
openssl x509 -in cert.pem -text -noout
```

---

## 4. Estrazione Oggetti & File Carving (Forensics Base)

**Trigger**: File estratto da HTTP (`upload.html`, dump raw, immagini sospette), file senza estensione, o dati concatenati in un singolo blob binario.

### Procedura di Carving
1. **Identifica il tipo reale**: `file oggetto` (non fidarti dell'estensione!).
2. **Estrai oggetti direttamente da Wireshark**: `File → Export Objects → HTTP` (salva immagini, ZIP, script trasferiti).
3. **Carving automatico da file binari o HTML esportati**:
   ```bash
   # Foremost: estrae PNG, JPG, PDF, ZIP da qualsiasi file (es. upload.html)
   # ATTENZIONE: -o vuole una CARTELLA di output, non il nome del file!
   foremost -i upload.html -o extracted_out/
   # Troverai i file in extracted_out/png/00000000.png

   # Binwalk: trova e estrae file/archivi annidati (es. PNG + ZIP appeso in coda)
   binwalk -e suspicious.png
   ```

### Magic Bytes & Strumenti Rapidi Forensics

| Tipo File | Magic Bytes (Hex) | ASCII / Note |
| :--- | :--- | :--- |
| **PNG** | `89 50 4E 47 0D 0A 1A 0A` | `.PNG....` (termina con chunk `IEND`: `49 45 4E 44 AE 42 60 82`) |
| **JPEG** | `FF D8 FF` | Termina con `FF D9` |
| **GIF** | `47 49 46 38 39 61` | `GIF89a` (o `GIF87a`) |
| **PDF** | `25 50 44 46 2D` | `%PDF-` |
| **ZIP** | `50 4B 03 04` | `PK..` |
| **GZIP** | `1F 8B 08` | Compresso `.gz` |
| **ELF** | `7F 45 4C 46` | `.ELF` (eseguibile Linux) |
| **PCAP / PCAPNG** | `D4 C3 B2 A1` / `0A 0D 0D 0A` | Catture di rete |

```bash
# Metadati (commenti EXIF, autore, coordinate)
exiftool image.png

# Stringhe leggibili (anche UTF-16LE con -e l per binari Windows)
strings -n 6 file.bin | grep -iE "flag|pass|key"

# Steganografia base su PNG/BMP (LSB, palette, chunk nascosti)
zsteg -a image.png
pngcheck -v image.png

# Steganografia JPEG/WAV con eventuale passphrase
steghide extract -sf image.jpg
```
