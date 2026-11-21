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
* exist the volume: `/srv/nfs/onboarding`


* `porta 111`: espone servizi RPC
* `nmap -sV -sC {IP} -T4`
* `nmap -sV -sT -p 111,2049 --script=nfs-showmount,nfs-ls,nfs-statfs {IP}` 
* `sudo mount -t nfs ip:/path /mount/to`
* `openssl s_client -connect ip:port -crlf` 
	* connect via POP3 and retrieve sbergz
