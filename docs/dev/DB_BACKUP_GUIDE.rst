
GUIDA DI BACKUP DEL DATABASE DI GASISTA FELICE TRAMITE SCRIPT
=============================================================

Questa guida spiega come utilizzare lo script di backup del database per produrre un archivio contentente:

* un backup di Gasista Felice;
* un file contenente informazioni circa la data del backup e l'HEAD del branch a cui l'installazione di Gasista Felice puntava al momento del backup.

Inoltre, lo script ruoterà i vecchi archivi di backup di Gasista Felice precedentemente creati, se presenti.

Il file backup_db.sh è localizzato nella cartella extra della root di Gasista Felice.

1. Per eseguire lo script è necessario che alcune variabili d'ambiente vengano settate, nello specifico:

  * GF_HOME: path assoluto alla cartella di Gasista Felice contenente il file manage.py;
  * DIR: indica la cartella nella quale si vuole che l'archivio venga salvato e ruotato.

NOTA: nel caso le variabile di cui sopra non venissero settate, lo script utilizzerà i seguenti valori di deafult:

  * GF_HOME: /usr/local/gasistafelice
  * DIR: /var/backups 

Quindi, una volta eseguito lo script sarà possibile localizzare l'archivio appena creato nella cartella DIR. 
