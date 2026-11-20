* **obsolete**: `ifconfig, route, arp, iptunnel` are obsolete!

**commands**:
* `ip address add a.b.c.d/m dev ethX`
* `ping a.b.c.d`


| command                             | desc.                                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `ip link show`                      | show all interfaces                                                                                                            |
| `ip link set eth0 up/down`          | set up/down flag on the NIC driver (but the interface is still on). **simply**: control whatever the device is running or not. |
| `ip address show`                   | show protocol addresses for each interface                                                                                     |
| `ip address add a.b.c.d/m dev ethX` | add an ip address to a device                                                                                                  |
| `ping a.b.c.d`                      | send ICMP packets                                                                                                              |

**how to solve network unreachable in lab 1**?
* define a default route or gateway
* specify how to reach pc2 from pc1

**def. static route**: routes for packets that should not or must not go trough the default gateway.
* `ip route add 192.0.2.1 via 10.0.0.1 [dev ifname]`
* `ip route add 192.0.2.0/24 via 10.0.0.1 [dev ifname]` 
* **file**: `/etc/sysconfig/network-scripts/route-[dev ifname]` is the file sotring routes.

**def. default gateway**: 
* for traffic which is not destined for the local network
* and for wich **no preferred route is specified** in the routing talbe
* **file**: `/etc/sysconfig/network`

**managing routes**:
* `ip route show`
* `ip route add a.b.c.d/m via next_hop_ip`
* `ip route add default via next_hop_ip`
* `ip route add 0.0.0.0/0 via next_hop_ip`
	* `0.0.0.0/0` is the default gateway