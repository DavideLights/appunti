# enumeration
* **nmap**: `nmap -sS -sV -sT [ipaddr]`
* **comandi per bypass shell ristretta**: `https://www.verylazytech.com/linux/bypassing-bash-restrictions-rbash`
* `find / -writable 2>/dev/null | cut -d "/" -f 2,3 | sort -u`: **mi dice le cartelle in cui ci sono file in cui posso scrivere** 
* `find`: puo' essere usata per trovare file modificati entro un certo lasso di tempo
* `tcpdump`: per vedere cosa passa sull'interfaccia di rete, ascoltare su una specifica porta, ecc...
* https://crontab.guru/
* **trovare setuid**: `find /usr/bin /usr/lib -perm /4000 -user root`
* **trovare setgid**: `find /usr/bin /usr/lib -perm /2000 -group root`
* **cerca tutte le capabilities**: `getcap -r / 2>/dev/null` me lo fa su tutti i file in `/`. 
* https://github.com/peass-ng/PEASS-ng/tree/master/linPEAS: *LinPEAS is a script that search for possible paths to escalate privileges on Linux/Unix*/MacOS hosts.*
* https://github.com/DominicBreuker/pspy: *pspy is a command line tool designed to snoop on processes without need for root permissions. It allows you to see commands run by other users, cron jobs, etc. as they execute. Great for enumeration of Linux systems in CTFs. Also great to demonstrate your colleagues why passing secrets as arguments on the command line is a bad idea.*


**reverse shell**: https://www.revshells.com/