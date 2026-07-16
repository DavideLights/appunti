
## linear apx
![[Pasted image 20260414114302.png]]

**Calcolo della tabella di approssimazione**:
* per tutte le combinazioni di input e output, ossia $\forall a,b \in \{ 0,1 \}^4$ calcolo quante stringhe $\forall X,Y \in \{ 0,1 \}^4$ mi danno $\bigoplus_{i=1}^4 a_{i}X_{i} \oplus \bigoplus_{i=1}^4b_{i}Y_{i} = 0$ 
* nel file `bias_table.csv` sono riportati i bias delle variabili

`bias_table.csv`:
![[Pasted image 20260414115051.png]]

*guardando la tabella ho cercato di formare un trail in modo da massimizzare il bias*, tenendo presente di dover scegliere combinazioni **con bias in assoluto lontane da 0**:
![[Pasted image 20260414114425.png]]
**Da qui calcolo il bias** dello XOR delle variabili scelte:
![[Pasted image 20260414115922.png]]

**il pilling up lemma** viene usato in questo modo:
* **guardando il CSV**: $e_{X_{16},V_{13}^1} = -0.25$, $e_{V^1_{13}, V_{1}^2}= -0.25$, $e_{U_{1}^3,V_{1}^3,V_{3}^3}=-0.25$
* **Per pilling up lemma**: $2^2 * (-0.25)^3 = -\frac{1}{16}$.
* **Il bias dunque e'** $\pm \frac{1}{16}$

![[Pasted image 20260414122215.png]]


**OSS**: le variabili attive potevano essere scelte meglio. Per rifare l'approssimazione le avrei scelte in questo modo.
![[Pasted image 20260414122910.png]]

![[Pasted image 20260414122237.png]]

![[Pasted image 20260414122336.png]]
![[Pasted image 20260414122354.png]]
![[Pasted image 20260414122411.png]]![[Pasted image 20260414122432.png]]