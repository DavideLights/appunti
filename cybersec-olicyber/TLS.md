1. step 1, random:
	1. C e S generano `Random`
	2. C e S si inviano `Random` a vicenda, in chiaro
2. step 2, generazione pub e priv
	1. C e S generano chiavi pub e priv
	2. `key_share` corrisponde alla chiave pubblica
	3. la privata esiste solo in ram.
3. step 3,
	1. generare shared secret a partire dalle corrispettive chiavi pubbliche.
	2. C e S avranno lo stesso shared secret.
	3. C e S eliminano la chiave privata, non serve piu.
4. step 4,
	1. L'algoritmo HKDF genera lo schedule delle chiavi a partire da shared secret
	2. Con lo schedule delle chiavi si cifra usando tipo RSA

* Come decifrare comunicazione TLS catturata con wireshark? se il file delle chiavi e' formattato come richiede lo standard TLS puoi passarlo a wireshark e fa tutto lui.