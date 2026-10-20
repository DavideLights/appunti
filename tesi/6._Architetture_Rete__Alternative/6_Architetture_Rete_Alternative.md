La sfida architetturale consiste nel duplicare l'infrastruttura di una challenge garantendo che i container clonati mantengano inalterati i loro indirizzi IP e la configurazione del gateway di default (per non alterare il comportamento dei payload dell'oracolo), senza generare conflitti di instradamento IP nell'host e garantendo la connettività Internet sia all'ambiente di verifica che di produzione.

Prima di convergere sulla soluzione adottata in BlueAgent sono state analizzate quattro architetture di rete alternative.

In questo capitolo vengono analizzate le caratteristiche tecniche, i vantaggi e i limiti operativi di ognuna.