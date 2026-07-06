## `fflush-example.c`

`fflush`: il funzionamento non e' definito per lo standard input. 
`fscanf`: quando non riesce a prendere l'input e a convertirlo nel formato richiesto, l'input rimane nel buffer utente e non viene svuotato.

**caso 1, nel codice inserisco una stringa (o qualcosa di diverso da un intero)**: 
* `scanf` fallisce a convertire ad intero, l'input utente rimane nel buffer della libreria.
* `fflush` viene eseguito su `stdin`, ma non fa niente (comportamento non definito dallo standard)
* `scanf` non ho tempo per iniziare a scrivere, `scanf` prova immediatamente a leggere il buffer della libreria (`scanf` non aveva consumato nessun caratter!), e fallisce a convertire ad intero, di nuovo.
* **cosa vedo?** viene stampato due volte 0

**caso 2, nel codice inserisco un numero**:
* `scanf` converte la stringa in numero ed il buffer della libreria viene svuotato
* `fflush` non serve a niente
* `scanf` ho tempo per scrivere, il buffer e vuoto,  e la stringa viene convertita in intero
* **cosa vedo?** viene stampato due volte 1, e dato che ad ogni chiamata di `scanf` il buffer viene svuotato, riesco a scrivere quando mi e' richiesto.



