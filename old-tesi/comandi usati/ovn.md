```bash
debian@debian13:~$ sudo ovs-vsctl set open_vswitch . \
   external_ids:ovn-remote=unix:/run/ovn/ovnsb_db.sock \
   external_ids:ovn-encap-type=geneve \
   external_ids:ovn-encap-ip=127.0.0.1
```


```bash
sudo incus network set incusbr0 ipv4.dhcp.ranges=172.16.0.0-172.16.0.99 ipv4.ovn.ranges=172.16.0.100-172.16.0.199
```