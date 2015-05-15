
Aggiornare dalla 0.9.9.9 alla 0.10
===================================

Oltre a sincronizzare il proprio codice sorgente con 
https://github.com/befair/gasistafelice

nell'aggiornamento a questa versione è necessario:

0. installare django-reversion:

$ pip install -r requirements/base.py

1. Aggiungere il campo `GASConfig.digest_days_interval` (se si desidera anche cancellare i dai della history, andare al punto 2.):

1-1. Eseguire la prima finta migrazione di south con ./manage.py migrate gas 0001 --fake
1-2. Eseguire le migrazioni dello schema del database con ./manage.py migrate gas --no-initial-data

2.Opzionale; rimuovere le tabelle relative a django-pro-history.
ATTENZIONE: questo rimuoverà tutti dati esistenti relativi alla history.

1-1. Eseguire la prima finta migrazione di south con ./manage.py migrate gas 0001 --fake
1-2. Decommentare la parte relativa alla cancellazione della history nel file `gas/migrations/0004_auto__del_historicalgasmemberorder__del_historicalgasconfig__del_histo.py`
1-2. Eseguire le migrazioni dello schema del database con ./manage.py migrate gas --no-initial-data


enjoy !

Marko
