
```bash
# Base64 encode / decode
echo -n "testo" | base64
echo "dGVzdG8=" | base64 -d

# Hex encode / decode
echo -n "flag" | xxd -p
echo "666c6167" | xxd -r -p

# Cercare una flag ovunque in una cartella
grep -rnI -E "flag\{|CTF\{" .

# Server HTTP rapido (per ricevere file o ospitare payload XSS/CSRF)
python3 -m http.server 8000

# Listener rapido (reverse shell / exfiltration)
nc -lvnp 4444
```
