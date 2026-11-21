# converti dati generci in testo
![[Pasted image 20261121102412.png]]

# filtrare

**mostrare solo pacchetti HTTP**
![[Pasted image 20261121103703.png]]

**mostrare dns e filtrare per sorgente**:
![[Pasted image 20261121104340.png]]

**filter comments**: usa il filtro `pkt_comment` nel campo di wireshark.

**filter for content**: usa il filtro `frame contains "Pwn all the things!!!"` nel campo di wireshark
# estrazione oggetti / png
**png**: per leggere un png dentro ad un file .html estratto con wireshark usare `foremost -i upload.html -o file.png`