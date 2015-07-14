GUIDA DI RIPRISTINO DI GASISTAFELICE
====================================

Ripristino in locale del database
---------------------------------

Questa guida elenca i passi necessari a rispristinare il database di GF all'ultima versione valida disponibile.

Prima di seguire questa guida è necessario avere un file di backup, per convenzione chiamato backup_gf.tar.gz.
Per ulteriori informazioni su come è costruito il file si veda lo script `extra/backup_db.sh`

L'archivio backup_gf.tar.gz contiene due file:

* un file (META) con il riferimento alla versione del software al momento dell'ultimo backup valido del database;
* un file (backup_gf.dump) contenente l'ultimo backup valido del database di GF.
 
Per ripristinare il database si dovrà:

1. scompattare il file backup_gf.tar.gz, 
2. aprire il file backuo_gf/META e copiare il codice alfanumerico identificato da "hash: "
3. portare il codice all'ultima versione funzionante con il comando: 

    git checkout <hash>

4. aprire il file settings.py presente nella cartella d'installazione di GF e modificare il campo 'NAME' dentro 'DATABASES' inserendo un nome diverso per il DB. Il vecchio database rimarrà così non sovrascritto.

5. eseguire i comandi:

    NOTA: è necessaria un'installazione di django perchè il comando ./wipe_postgres_db.sh funzioni. Se si utilizza un virtualenviroment, caricarlo con il comando workon <nome_virtualenv> 

    - export GF_HOME=<cartella di installazione di GF>

    - cd $GF_HOME/extra

    - ./wipe_postgres_db.sh

  per creare un nuovo database su cui installare il backup

6. ripristinare il DB:

    psql -U postgres <nuovo_nome_db> <  backup_gf.dump

  oppure, entrare nella shell di postgres:
    
    psql -d <nuovo_nome_db> -U <nomte_utente>

  quindi eseguire il comando:

    \i backup_gf.dump

    (ci saranno diversi warning, possono essere ignorati)
 
