
Aggiornare dalla 0.6 alla 0.7
=============================

Oltre a sincronizzare il proprio codice sorgente con 
https://github.com/feroda/gasistafelice

# git clone https://github.com/feroda/gasistafelice.git

nell'aggiornamento a questa versione è necessario:

1. Eliminare dal database tutte le relazioni temporali
2. Rieffettuare la sincronizzazione del database

Eliminare dal database tutte le relazioni temporali
---------------------------------------------------

Per chi è fortunano come me (fero) e dispone di un sistema GNU/Linux
con una shell moderna (bash/dash), può effettuare i seguenti semplici
comandi per eseguire quasi automaticamente tutte le operazioni.

Dico quasi perché consiglio di effettuare una verifica delle tabelle che
si stanno rimuovendo prima di eseguire le operazioni `DROP TABLE` vere e proprie.

Dal vostro amico terminale eseguite:

# cd <directory del default_settings.py>
# echo '\dt *_historical*' | python manage.py dbshell | grep table | awk '{print $3 }'

e verificate di avere un output a:

    base_historicalcontact
    base_historicaldefaulttransition
    base_historicalperson
    base_historicalplace
    gas_historicaldelivery
    gas_historicalgas
    gas_historicalgasactivist
    gas_historicalgasconfig
    gas_historicalgasmember
    gas_historicalgasmemberorder
    gas_historicalgassupplierorder
    gas_historicalgassupplierorderproduct
    gas_historicalgassuppliersolidalpact
    gas_historicalgassupplierstock
    gas_historicalwithdrawal
    supplier_historicalcertification
    supplier_historicalproduct
    supplier_historicalproductcategory
    supplier_historicalproductmu
    supplier_historicalproductpu
    supplier_historicalsupplier
    supplier_historicalsupplieragent
    supplier_historicalsupplierstock

questa è la lista delle tabelle che verranno eliminate. A questo punto potete eseguire:

# for t in $(echo '\dt *_historical*' | python manage.py dbshell | grep table | awk '{print $3 }'); do echo DROP TABLE $t | python manage.py dbshell ; done

e successivamente sincronizzare il database:

# python manage.py syncdb

Buon divertimento!
Luca `fero` Ferroni
