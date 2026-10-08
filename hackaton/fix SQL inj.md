**Vulnerabilita**: Facendo l'accesso inserendo come nome utente `'=' 'or'` si accede alla dashboard. 

fix:
1. accedo con ssh con utente `snowadmin`
2. `sudo docker exec -t allyoucansnow bash`
3. il file interessato e' `/var/www/allyoucansnow/admin/login.php`
4. 

