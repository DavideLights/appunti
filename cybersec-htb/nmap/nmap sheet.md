* `-sS`: (default) TCP SYN scan. 
* `-sC`: use default scripts when scanning.
* `-U` append to do UDP scan.
* `-p-`: scan all ports instead of default 1000 ports

## Version Scanning Examples
* `nmap -sV -sC {ip} -Tn` where $n$ is a number.
	* used to get mariadb versio in sequel