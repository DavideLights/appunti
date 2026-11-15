**private network**: made of computers owned by a single organization.
* **Traffic**: in a private network is trusted and shared only among participants. #gemini

**what if**: 
* corporation has multiple geograph. locations? how can i extend it?
* you are abroad and cannot access the local network?

**solution**: you can use a **VPN (Viva il Pisello Nero)**.
* **goal**: build a secure private network
* **restriction**: over an insecure public network
* **mechanisms**: encryption, authentication, packet tunneling, and firewalls (not a single defense mechanism; subject to public internet reliability). #gemini

**tunnel**: 
* **ssh port forwarding**: same concept, we tunnel a packet encapsulating it and sending towards someone.

**configurations**:
* **vpn client on the gateways (GW):** *GW2GW*
	* **use case**: connection over vpn is transparent to clients
	* **transparent**: all of the clients do not know about the vpn.
* **vpn end to end**: no gateway involved in encryption and decryption
	* **use case**: a VPN shared only between 2 endpoints, and not between gateways (can also mix GW2GW and end-to-end). #gemini

## OpenVPN
**OpenVPN**: implementation for a VPN.
* **based on**: TLS

### TLS
**public key certificate**:
* **certificate**: is my **public key** concatenated in some way with my **identity** ($\text{CERT}_{id} \leftarrow \langle id, \text{PUB KEY}_{id} \rangle$, plus metadata like CN, expiration). #gemini
* **identity**: IP Address or Domain name (Common Name / Subject).
* **sign**: yes, the certificate must be signed by a Certification Authority (CA); the signature is embedded in the certificate. #gemini
* **CA**: a certification authority just checks and signs certificate.
	* **trusting**: we trust CA server. if he signs it i assume everything is ok.
* **how do i trust a CA?**: it has a certificate that can be signed by **ANOTHER CA**.
	* **root**: is the one that self signs a certificate.

**browser example**:
* **gerarchia certificati**: its the chain of certifications for a certificate (**chain of trust**).
* during the TLS handshake the server sends its certificate chain up to an intermediate CA (X.509 AIA extensions may also link intermediate issuers, never the root CA). #gemini
* **folder**: on every host there is a folder with the trusted `certs`.
	* **linux**: `/etc/ssl/certs`
	* **TLS Man In the Middle**: i can create a fake certificate authority and add it in `/etc/ssl/certs`
	* **how do you trust a root cert**? yes, via the local copy in the trust store (`/etc/ssl/certs` or browser store): root CA certs are pre-installed locally, never fetched dynamically during TLS. #gemini
	* **why i do not need a local copy of a certificate for every website?** the website sends its certificate (and intermediates) in the handshake, and you verify the signature chain up to the local root CA certificate. #gemini


> TE FIDI O NUN TE FIDI AO.


**key concept**: 
1. clients trust **root** CAs #gemini
2. no need to use the CA **private key** during verification: the CA signs with its private key, so clients/servers verify signatures using only the CA's **public key** (inside `ca.crt`); the CA itself can stay offline. #gemini

**certificates**: have a lot of info and follow a standard X.509


```bash
openssl x509 -in file.pem -text   # add -inform der if DER-encoded
```

### now openvpn (OpenViva il Pisello Nero)

**PKI**: Public Key Infrastructure, is composed of:
* a master Certificate Authority (root CA certificate + key) used to sign server and client certificates #gemini
* a separate certificate **and private key** for the server and each client #gemini

**how do server and client authenticate**? each peer presents its certificate and proves ownership using its **own private key** (`server.key` / `client.key`); the other peer verifies the CA signature using only `ca.crt` (no **CA private key** is needed). #gemini

> **note**: authentication is bidirectional (mutual TLS): client authenticates to server and server authenticates to client. #gemini

**server**:
* does not need all the certificates for every user (only `ca.crt`, `server.crt`, `server.key`). #gemini
* compromised keys can be selectively disabled via a **CRL** (Certificate Revocation List) without rebuilding the whole PKI. #gemini

### how to create a PKI
`easy-rsa`: wrapper scripts around `openssl` (in `/usr/share/easy-rsa` in Kathara): #gemini
```bash
cd /usr/share/easy-rsa
./easyrsa init-pki                      # init PKI folder structure
./easyrsa build-ca                      # build root CA (ca.crt, ca.key)
./easyrsa build-server-full SERVER_NAME # server cert & key
./easyrsa build-client-full CLIENT_NAME # client cert & key
openssl dhparam -out dh2048.pem 2048    # Diffie-Hellman params (server only)
```
*(sample DH params also at `/usr/share/doc/openvpn/examples/sample-keys/dh2048.pem`)* #gemini

* **generated files** (in `/usr/share/easy-rsa/pki`, named by Common Name): #gemini
	* `ca.crt` (server + all clients, public) / `ca.key` (CA signing machine only, **secret**) #gemini
	* `dh{n}.pem` (server only, public) #gemini
	* `server.crt` (public) / `server.key` (**secret**) → server only #gemini
	* `client1.crt` (public) / `client1.key` (**secret**) → `client1` only #gemini

`openssl`: security library, the most important thing in the world. if you break this you break your mom's ass.

### OpenVPN Architecture
creates a virtual network interface:
* **TUN L3**: virtual network iface for IP tunneling 
* **TAP L2**: is a virtual network iface for Ethernet tunneling / bridging.

**data flow in linux os** (received packet): #gemini
* NIC → Real NIC driver (kernel space) → OpenVPN (user space, decrypts) → TUN/TAP driver (kernel space) → App TX/RX (user space). *(Reverse path when sending).* #gemini

**encapsulation**:
* traffic is encapsulated inside TCP or UDP (NAT-friendly: outer IP & L4 ports can be NATted). #gemini
* **default**: openvpn works on UDP, because tunneling TCP over TCP doubles overhead and causes duplicate retransmissions / congestion-control conflicts (TCP meltdown). #gemini

**TUN**: layer 3, easy to setup, less overhead. Create `tun0`.

**TAP**: layer 2, create an interface with a mac address (supports non-IP protocols like ARP). #gemini

## Client/Server config
```bash
cat server.conf
```
* `port/protocol`
* `dev tun`
* `server`: this line decides the subnet we are creating.
	* its a pool, from this we assign ip addresses to clients connecting.
	* be careful to not cause conflicts.
* `ca`: path to Root CA certificate (`ca.crt`), used to verify peer certificates. #gemini
* `cert`: path to this host's own signed public certificate (`server.crt` or `client.crt`). #gemini
* `key`: path to this host's own **private key** (`server.key` or `client.key`), kept secret and used to prove identity in the TLS handshake. #gemini
* `dh` *(server only)*: path to Diffie-Hellman parameters (`dh2048.pem`) for key exchange. #gemini

```bash
cat client.conf
```
* `remote`: vpn address and port (plus `client`, `dev tun`, `proto`, `ca/cert/key`). #gemini

### Kathara setup (`lab_vpn`) #gemini
Due to Kathara container limitations, `.startup` files must manually create `/dev/net/tun`: #gemini
```bash
mkdir -p /dev/net
mknod /dev/net/tun c 10 200
chmod 600 /dev/net/tun
```
* Launch OpenVPN with `openvpn server.conf` (on `s1`) then `openvpn client.conf` (on `pc1`, `pc2`; key password `"password"`), and open another shell via `kathara connect <node>`. #gemini

## Push routes (`lab_vpn_pushroute`) #gemini
* Running the OpenVPN server on a **gateway** (`r_server_vpn`) lets a VPN client (`client1_vpn`) reach a host (`p_host`) in the server's private LAN without `p_host` running OpenVPN. #gemini
* In `server.conf`: #gemini
```text
push "route 192.168.0.0 255.255.255.0"
```
* Adds the `192.168.0.0/24` route to `client1_vpn`'s routing table via the VPN tunnel (otherwise packets go to its default gateway `r1`, which drops them). #gemini

### Security considerations #gemini
* Non-VPN hosts (e.g., `p_host`) can reach VPN clients (`client1_vpn`) if routing allows it. #gemini
* VPNs by default do **not** isolate untrusted networks / the Internet from the VPN → isolation must be configured manually with **firewalls**. #gemini

## Client-specific configuration (`CCD`) #gemini
* In `server.conf`: #gemini
```text
client-config-dir /root/ccd
```
* Create a file `/root/ccd/<CN>` named after the client's certificate **Common Name (CN)** (e.g., `/root/ccd/client1`) to assign a static VPN IP: #gemini
```text
ifconfig-push 192.168.100.101 255.255.255.0
```
