
Aggiornare dalla 0.1 alla 0.1.1
===================================

Oltre a sincronizzare il proprio codice sorgente con 
https://github.com/befair/gasistafelice

nell'aggiornamento a questa versione è necessario:

1. Aggiungere il campo `gas_gasconfig` 

Esempio per il vostro sistema:

0. Commentare internamente le migrazioni in gas/migrations/ (0002 e 0003)

1. Eseguire la prima finta migrazione di south con ./manage.py migrate gas 0001 --fake
2. Eseguire le migrazioni dello schema del database con ./manage.py migrate gas --no-initial-data

enjoy !

Marko
