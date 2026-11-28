# introduzione al problema
```c
codice qui
```

con `gdb` ora vogliamo analizzare cosa succede ai registri della prima della chiamata. 
* `b &main+103`
* `r`
* `info reg`

**stato dei registri** for a `printf`: how are arguments passed to a printf?
* `rdi` contiene la stringa da formattare, in particolare ne contiene il puntatore.
* `rsi,rdx,rcx,r8,r9` gli altri 5 argomenti passati  in ordine
* i restanti vanno nello stack, passati tramite push

**infatti**:
* `x/s 0x555555556004`
* `x/4gx $rsp`
![[Pasted image 20261126130929.png]]


> [!note] `x/4gx $rsp` syntax
> * `x`: examine
> * `4`: quantity, numero consecutivo di oggetti da leggere
> * `g`: giant, oggetti sono parole a 64 bit, ossia 8 byte.
> * `x`: hex, scrivi in esadecimale.
> Dunque: legge 4 parole a 64 bit a partire dal valore del registro $rsp$

# passing wrong types

**printf**: does not actually check what you pass, and if it matches the type specified in the format string.


**how to leak memory**:
* `%c`: read a char off the stack
* `%d, %i, %x`: to leak an integer, 4 bytes
	* `%x`: **read data from the stack**
* `%s`: dereference a string and read its byte until the null byte (a string).

**Size parameters for printf**:
* `%x` leaks 4 bytes
* `%hx` is 2 bytes
* `%hhx` is 1 bytes
* `%lx` is 8 bytes

> [!note] intuition
> `h` stands for half and `l` for longer by doubling

```c
char fmt_str[256];
char *secret_value = "this is my secret";

strcpy(fmt_str, argv[1]);
strcat(fmt_str, "\n"); 
printf(fmt_str, 0xBEEF1337)
```

> [!note] `strcpy` and `strcat`
> * `strcpy(dest, src)` copies src into dest
> * `strcat` concatenates `src` into `dest`

`./a.out "leak: %c"`: outputs the least significant byte of `0xBEEF1337`
* **console output interpretation**: the byte `37` is the code for the character `7`
* **why that happens**? we are basically calling `printf("leak: %c", 0xBEEF1337)`

`./a.out "leak: 0x%x"`: outputs `0xbeef1337`, were `%x` is the escape code to ouput a value using its hex representation.

`./a.out "leak: 0x%lx"`: does not output more bytes that just `%x` in this case.
does
`./a.out "leak: %p"`: does not do something more interesting than `%x`.

`./a.out "leak: %p %p %p %p"`: this does something strange!
![[Pasted image 20261126143421.png]]

can we use this behaviour to leak `secret_value`? YES.
![[Pasted image 20261126144832.png]]
* the missing arguments are automatically retrieved from the registers
* if we have more arguments (`%p`) than register, the we'll end up reading the stack.
* In the stack resides the secret.

**we can do it better**: 
* `%7$x`: prints the t7h paramether
* `./a.out 'leak: %9$s'`: will print out just the secret. 

**why this works**?
* **who does printf trust**? we exploit the fact that `printf` trusts the format string it has given as first parameter.
* **who does printf rely on to work correctly and format the data?** on the caller, he trusts that the caller setup correctly stack and registesr to provide all the data to be formatted.
* **it works because**:  if we can attack the format string, then we can tell printf to read registers and stack values for us.

```c
printf("%s", argv[1]); // is safe
printf(argv[1]); // this is not
```

# writing memory

`%n`: dereferences a value, and writes there the number of bytes written so far.

```c
int namelength;
printf("%s%n", name, &namelength);
printf("The name is %d bytes long!", namelength);
```

now look at this example: 
```c
code here
```

run with gdb:
* `b *main`
* `x/6i $rip`: disassembles the next 6 instructions starting from the RIP
	* `RIP` points at the instruction to execute.
* `disass main`: disassembles the whole main and shows you were we are.

in the assembly:
* `test %eax, %eax` corrisponde ad `if(*print_flag)`
	* dove `eax` contiene il valore di `print_flag`
	* **cosa fa**? `AND` logico, bit a bit di `%eax`
		* **Zero Flag**: viene impostata a 0, se `%eax AND %eax` ha tutti i bit a 0, ossia se `%eax` ha tutti i bit a 0.
* `je`: esegue il salto se la Zero Flag e' stata impostata, quindi se `%eax==0`
* `mov -0x220(%rbp),%rax`: vuol dire che `rax` contiene il valore contenuto in `-0x220(%rbp)`
	* **note**: its just before `test` instruction.
	* **RBP**: punta alla base del frame della memoria della procedura corrente
	* quindi RBP punta in alto
	* sottrarre un valore ad RBP vuol dire indirizzare l'area di memoria dello stack.
	* o in generale accedere all'heap del processo.

let's look what's the index of `print_flag` inside the stack, so we can give it to the `printf` function:
![[Pasted image 20261126171256.png]]

So `print_flag` is the 4th element in the stack, via `printf` we can write on it like this (remember, that the first 6th arguments of `printf` are registers so we will pass it the value `%10` instead of `%4`) .

Run the binary using: `./a.out 'a%10$n'` to read the flag! (just create a fake `/flag` file with some text inside)

> [!error] initialize `rbp` and `rsp`
> To actually calculate at wich offset `print_flag` is located at, using `gdb`, you have to execute the first main's instructions that are used to initialize the stack of the function, so try executing for example `ni 7`. 
> **Otherwise the steps above will return random data.**

**so what we did**?
* used `a%10$n` to write 1 inside `print_flag`
* so we redirected the code's flow taking a different branch than the one expected.
# other writing strategies

**controlling how many byte to write**:
* `%ln`
* `%hn`
* `%hhn`

**padding**: 
```c
char buf[4];
printf("%1145258561x%1$n");
```
* we pad the value to print using `0x1145258561` characters
* so the length of the string written into the screen is actually `0x1145258561`
* **goal**: we write `0x1145258561` into the first argument.
* **note**: `0x1145258561` corresponds to the string `ABCD`

look at this example:
```c
asd
```

**problem**: executing this code implies waiting the console to print all this large amount of spaces into the screen

**solution**:
```c
char buf[4];
printf("%65x%1$hhn")
```