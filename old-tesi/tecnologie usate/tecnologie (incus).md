```bash
usermod -a -G incus-admin arch
incus admin init --minimal
usermod -v 1000000-1000999999 -w 1000000-1000999999 root
```


## pull/push file
```bash
incus file pull first/etc/hosts
incus file push hosts first/etc/hosts
incus file pull first/var/log/syslog - | less
```


## snapshot
```bash
incus snapshot create first clean

# rompi il container
incus exec first -- rm /usr/bin/bash
incus exec first -- bash

# restore
incus snapshot restore first clean

# delete
incus snapshot delete first clean
```

## sicurezza 
**socket unix**: chiunque ha accesso al socket unix `/var/lib/incus/unix.socket` ha privilegi root sul sitema ospitante.

# reti
**External Network**: usano interfacce che gia esistono, dunque incus non ha molto controllo. Il traffico passa per una **parent interface**.

**Macvlan network**: e' una virtual LAN che posso usare per assegnare vari indirizzi IP alla stessa network interface. Si divide l'interfaccia in sotto interfaccie a cui assegnare gli IP, basandosi sul MAC address generato randomicamente.