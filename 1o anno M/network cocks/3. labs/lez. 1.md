**obsolete**: `ifconfig, route, arp, iptunnel` and other tools are obsolete!

**commands**:
* `ip address add a.b.c.d/m dev ethX`
* `ping a.b.c.d`

**kathara**:
* `lab.conf`: contains all the containers and their network interfaces.
	* **ex**:`pc1[0]=A`: `pc1` has `eth0` on subnet `A`

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
	* `0.0.0.0/0` is the default subnet, represents the gateway


`traceroute a.b.c.d`: number of addresses and hops to reach a.b.c.d
* expose all the intermediate nodes using TTL filed in ICMP packets.
* start with TTL=1, until packets does not reach the destination
* TTL is decreased at every hop
* when TTL=0 then the router sends an ICMP packet revealing its IP to the sender.
* `traceroute` can reconstruct the list of hosts involved in a route.

`netcat`: send data over TCP and UDP

| command                  | protocol | description                          |
| ------------------------ | -------- | ------------------------------------ |
| `nc ip_addr port_num`    | TCP      | **connects** to `ip_addr:port_num`   |
| `nc -u ip_addr port_num` | UDP      | send datagrams to `ip_addr:port_num` |
| `nc -l -p port_num`      | TCP      | **listen** locally on `port_num`     |
| `nc -u -l -p port_num`   | UDP      | **listen** locally on `port_num`     |

`tcpdump`:  captures packets and stores them into a `pcap` files.
* `tcpdump -i iface_name -w filename.pcap` to caputer on `iface_name`

**excercise**:
![[Pasted image 20261120180619.png]]
1. since they are all in the same subnetwork...
	1. PC1 knows how to reach R1
	2. R1 ... R2
	3. R2 ... S1
2. but PC1 and R1 do not know how to reach S1, so we need to
	1. tell PC1 to reach S1 trough R1
	2. tell R1 to reach S1 trough R2
3. but S1 and R2 do not know how to reach PC1, as before, we'll instruct them to do so.

```bash
# PC1
ip address add 192.168.1.100/24 dev eth0
ip route add default via 192.168.1.1

# R1
ip addr add 192.168.1.1/24 dev eth1
ip addr add 10.10.10.1/30 dev eth0

# ip route add default via 10.10.10.2
ip route add 10.50.0.0/24 via 10.10.10.2

# R2
ip addr add 10.10.10.2/30 dev eth0
ip address add 10.50.0.1/24 dev eth1

# ip route add default via 10.10.10.1
ip route add 192.268.1.0/24 via 10.10.10.1

# S1
ip addr add 10.50.0.134/24 dev eth0

ip route add default via 10.50.0.1
```

**experiment**:
* `shared` is shared between the host and the containers
* **start capturing packets on R1**: `tcpdump -i eth1 -w shared/my_capture_tcp.pcap`
* **start netcat in listen mode on S1**
* **start netcat as client on pc1**, over TCP.
* also do the same using UDP and check the capture contents.
* also try to not run the nc listener and check for errors

what does the experiment show?
1. for TCP and UDP nothing interesting.
2. if we do not run the nc listener and try to send data:
	1. **TCP**: destination host answers with `RST` flag set.
	2. **UDP**: destination host answers with ICMP packet saying `Destination Unreachable (Port unreachable)`

> [!error]
> let: 
> * `eth0` on `pc1` with ip `192.168.1.100/24`
> * `eth1` on `r1` with ip `192.168.1.1/24`
> * so `route add default via 192.168.1.100` on `pc1` if we want to reach `r1` is useless.
> 
> note that `eth1` is on the same subnet of `eth0` so the route for it is trivial, just send out of `eth0`, in someway it will arrive, maybe because of a switch or a router, or because `eth1` is physically attached to it.

