# 1.0
**context**:
* the stack contains a 15-character secret password
* secret is at `0x7fffc1171680`
* stack pointer is at `0x7fffc1171620`
* the difference is: `0x60 = dec(96)`
* divide by 8: `dec(12)` 

**how to take the flag**:
* just pass `%18$s` to the `printf`

**were is the string**? maybe on another section of the program since `s` tells `printf` to dereference the pointer and start reading the string from that address. So on the stack resides only the pointer to the string.

> [!note] referring to printf man.
> syntax for printf conversions:  `%[argument$][flags][width][.precision][length modifier]conversion`
> * so we specified `[argument$]` 
> * and the conversion

# 1.1
passed for the first time the string: 
```c
%p %p %p %p %p %p %p %p %p %p %p %p %p %p
```

It returned something like:
```c
0x76ce8955e723 (nil) 0x76ce8947f297 0xa 0x25 0x53564f5552465053 0x53585841475351 (nil) (nil) (nil) (nil) (nil) (nil) 0x7ffc80e5e660
```

the last address returned, looks like an address referring to a stack (since it starts with `0x7ff...`, and the stack pointer has a similar value).

So replacing last `p` with an `s` returned the secret password.