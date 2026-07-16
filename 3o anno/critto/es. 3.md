```python
def Alg(H,N,r)
	def g_r(x): ret (ax + r)%N
	def f(x): ret g_r(H(x))
	# inizializza
	x0 = random_number(1,N)
	t = h = x0
	# trova inizio del ciclo
	do:
		t = f(t)
		h = f(f(h))
	while: t != h
	
	# ora devo cercare i valori per cui ho collisione
	h = x0
	while f(t) != f(h):
		t=f(t)
		h=f(h)
	return (t,h)
```

![[Pasted image 20260414123504.png]]

**OSS**: quando nel primo ciclo ho $t=h$ non so con quale valore sono arrivato ad $h$. 

**Come rilevo dunque la collisione**? faccio ripartire $h$ dall'inizio e poi avanzo $t$ ed $h$ a step di 1.