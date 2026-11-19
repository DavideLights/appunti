* `porta 111`: espone servizi RPC
* `nmap -sV -sT -p 111,2049 --script=nfs-showmount,nfs-ls,nfs-statfs {IP}` 
* `sudo mount -t nfs ip:/path /mount/to`
* `openssl s_client -connect ip:port -crlf` 
	* connect via POP3 and retrieve sbergz
