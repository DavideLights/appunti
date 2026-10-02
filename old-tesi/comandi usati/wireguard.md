
```
sudo sysctl -w net.ipv4.ip_forward=1
```

```
# Generazione chiavi Server Host
wg genkey | tee wg-0-private.key | wg pubkey > wg-0-public.key

# Generazione chiavi Client Partecipante
wg genkey | tee client-0-private.key | wg pubkey > client-0-public.key
```

```
# Creazione dell'interfaccia virtuale WireGuard
sudo ip link add dev wg-0 type wireguard

# Assegnazione dell'IP host sulla subnet 10.0.0.0/30
sudo ip addr add 10.0.0.1/30 dev wg-0

# Configurazione della porta UDP e della chiave privata
sudo wg set wg-0 listen-port 51820 private-key wg-0-private.key

# Attivazione dell'interfaccia
sudo ip link set dev wg-0 up
```


> [!error] dns e ip
> non c'e' un server dhcp e il dns non viene risolto. ogni container deve ottenere per ora staticamente l'ip e avere un dns server impostato.
> dunque bisogna riavviare `systemd-resolved` dopo aver impostato un dns

 