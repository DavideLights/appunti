**come funziona early bird**?
1. i tweet sono memorizzati in segmenti di memoria ordinati in word da 32 bit, in modo da rendere efficiente la lettura per il processore.
2. lettura read-only: una volta che l'indice attivo si riempie viene congelato e tenuto in modalita solo lettura. solo l'indice corrente puo' essere modificato.