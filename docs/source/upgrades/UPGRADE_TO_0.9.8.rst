
Aggiornare dalla 0.9.7 alla 0.9.8
=================================

Oltre a sincronizzare il proprio codice sorgente con 
https://github.com/feroda/gasistafelice

# git clone https://github.com/feroda/gasistafelice.git

nell'aggiornamento a questa versione è necessario:

1. Eseguire la prima finta migrazione di south dell'applicazione users con ./manage.py migrate users 0001 --fake
2. Eseguire le migrazioni dello schema del database con ./manage.py migrate users --no-initial-data

buon divertimento!
Luca `fero` Ferroni
