Aggiornare dalla 0.11 alla 0.12
===============================

Oltre a sincronizzare il proprio codice sorgente con
 
https://github.com/befair/gasistafelice

nell'aggiornamento a questa versione è necessario:

0. installare django-reversion:

   `$ pip install -r requirements/base.py`

#. Aggiungere il campo `GASConfig.digest_days_interval`:
   
   **OPZIONALE**: rimuovere le tabelle relative a django-pro-history, decommentando le righe relative alla cancellazione della history nel file    
   `gas/migrations/0004_auto__del_historicalgasmemberorder__del_historicalgasconfig__del_histo.py`
       
       **ATTENZIONE**: questo rimuoverà tutti dati esistenti relativi alla history.

   `$ ./manage.py migrate gas 0001 --fake`
   
   `$ ./manage.py migrate gas --no-initial-data`

enjoy!

Marko
