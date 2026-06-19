# sequel

```bash
> nmap -sC -sV 10.129.71.120
PORT     STATE SERVICE VERSION
3306/tcp open  mysql?
| mysql-info: 
|   Protocol: 10
|   Version: 5.5.5-10.3.27-MariaDB-0+deb10u1
|   Thread ID: 66
|   Capabilities flags: 63486
|   Some Capabilities: Support41Auth, IgnoreSpaceBeforeParenthesis, ConnectWithDatabase, SupportsLoadDataLocal, Speaks41ProtocolOld, FoundRows, DontAllowDatabaseTableColumn, SupportsTransactions, IgnoreSigpipes, SupportsCompression, InteractiveClient, ODBCClient, LongColumnFlag, Speaks41ProtocolNew, SupportsMultipleStatments, SupportsAuthPlugins, SupportsMultipleResults
|   Status: Autocommit
|   Salt: $=E#~rB2o^hov%QIXa\+
|_  Auth Plugin Name: mysql_native_password
```