
Aggiornare dalla 0.9.8 alla 0.9.9.9
===================================

Oltre a sincronizzare il proprio codice sorgente con 
https://github.com/feroda/gasistafelice

# git clone https://github.com/feroda/gasistafelice.git

nell'aggiornamento a questa versione è necessario:

1. Aggiungere il campo `balance_current` 
2. Popolare il campo `balance_current` per tutte le voci del registro registrate

Esempio per il vostro sistema:

Punto 0:

./manage.py syncdb

Punto 1:

- sqlite3
# echo 'ALTER TABLE simple_accounting_ledgerentry ADD COLUMN "balance_current" DECIMAL' | ./manage.py dbshell

- postgresql
# echo 'ALTER TABLE simple_accounting_ledgerentry ADD COLUMN "balance_current" numeric(10, 4)' | ./manage.py dbshell

Punto 2:

# ./manage.py shell


from simple_accounting.models import LedgerEntry, Account
for ac in Account.objects.all():
    prev_balance_current = 0
    for ledger_entry in ac.ledger_entries.order_by('entry_id'):
        ledger_entry.balance_current = prev_balance_current + ledger_entry.amount 
        prev_balance_current = ledger_entry.balance_current
        super(LedgerEntry, ledger_entry).save()
    print("account=%s, balance=%s" % (ac, ac.balance))


buon divertimento!
Luca `fero` Ferroni
