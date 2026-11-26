* command sheet: https://www.mysqltutorial.org/mysql-cheat-sheet/
# connecting to the DB
* `mysql -h {ip/hostname} -u root -ppassword`
* `--skip-ssl`: when server does not support TLS.
# interacting with the DB
1.  `SHOW DATABASE`: show all db  in the server. The following are always present on a mariadb.
2.  `USE htb`: enter into `htb` database
3. `SHOW TABLES`: after being in a db (`USE`), display all the tables.
4. `SHOW COLUMNS FROM table` or `DESCRIBE table`
5. 

```sql
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
```