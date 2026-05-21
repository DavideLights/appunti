### `array-test.c`

```c
int a[10] = {1,2,3,4,5,6,7,8,9,10};

int main(...){
	char *p;
	int i;
	
	// andare all'indirizzo piu alto dell'array
	// p = (char*)a + sizeof(a)
	p = a + sizeof(a); // Domanda: e' corretto?
	
	for(i = 1; i<=10; i++){
		printf("%d", ((int *)p)[-i]);
	}
}
```
* **indici negativi**: sono permessi se $p$ punta verso l'ultimo indirizzo dell'array.
* **casting**: `(int *)p`

1. voglio accedere a degli interi, ma ho a disposizione `char *p`.
2. per accedere correttamente attraverso l'operatore `[]` devo fare il casting!

> [!error] prof
> `p = a +sizeof(a)` da errore compilazione, e comunque dovrebbe funzionare.


### `basic-buffer-overflow.c`
```c
int main(...){
	int index, value;
#ifdef IN_STACK
	int control_variable;
	int v[10];
#endif


	control_variable = 1;
	while (control_variable == 1){
		scanf("%d%d", &index, &value);
		v[index] = value;
		printf("array elem at position %d has been set to value %d\n",index,v[index]);
		
	}
	
	printf("exited\n");
	return 0;
}
```

![[Pasted image 20260519165651.png]]![[Pasted image 20260519165804.png]]
Questo vuol dire che c'e' una differenza di `0x20` byte, ossia 32 byte.

> [!error] prof
> **Problema**: provando a dare in input `-32 0` non si ferma il loop
 **Ma**: se metto `define IN_STACK` con input `-1 0` si ferma il loop.

## `busy-loop.c`
**compilare**: `-nostartfiles`
![[Pasted image 20260519171244.png]]

**attenzione**: nella sezione del testo, `f` e' l'unica funzione trovata. Dunque per come funziona Linux, e' la prima procedura che viene chiamata all'esecuzione.

**infatti**: se rimuovo `-nostartfiles`