# traffic analysis
**sniffing**: applicazione software che acquisisce pacchetti al livello dei dati.
* **interpreta**: interpreta i dati a livello 2, 3, 4 ecc...


`tcpdump`: ascolta sul `eth0`
```bash
tcpdump -i eth0
```
https://jvns.ca/tcpdump-zine.pdf

**esempio**:
```bash
sudo tcpdump -n -i any port 53
```
* per ascoltare cosa succede al DNS!

**opzioni**:
* `-i`: seleziona l'interfaccia da scoltare. `-i any` per qualsiasi
* `-w`: scrivi in un file, con estensione per esempio `.pcap` (cosi lo puoi aprire con wireshark)
* `-c`: count, limita il numero di pacchetti da catturare.
* `-A`: stampa il contenuto dei pacchetti
* `n`: non tradurre il gli ip in hostname
* `e`: ethernet, mostra il `MAC` di origine.
* `-p`: mosra i pacchetti che vanno e vengono dal mio pc!

altre cose inutili...