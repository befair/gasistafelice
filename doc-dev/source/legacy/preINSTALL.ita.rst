****************************************************************************
***********************   PREPARAZIONE SISTEMA   ***************************
****************************************************************************

Questo file contiene istruzione su come preparare l'ambiente di lavoro nel 
caso in cui ci si avvicini per la prima volta agli strumenti necessari 
all'installazione di Gasista Felice.

NOTA: se non altrimenti specificato, tutti i comandi in questa guida vanno eeseguiti come utenti con permessi di amministratore.


***** Python

1. Installare python eseguendo:

	$ apt-get install python python-dev


********** SQLITE


SQLite è una libreria che implementa un DBMS SQL che permette la creazione e la
gestione di una base di dati (comprese tabelle, query, form, report).

1. Installare SQLITE:

$ apt-get install sqlite3 python-sqlite libsqlite3-dev


********** POSTGRESQL

PostgeSQL è un database relazionale. In particolare, psycop2 è un PostgreSQL 
adapter per Python.
	
1.	Installare i seguenti pacchetti:
	
	$ apt-get install postgresql python-psycopg2 libpq-dev postgresql-client

2.	Creazione di un utente e di un DB associato all'utente creato:

	2.1	prima di procedere, controllare di avere il permesso per autenticarsi
		controllando nel file di configurazione di postgresql:
		
		$ gedit /etc/postgresql/versione/main/pg_hba.conf
		
		("versione" indica la versione di postgresql, tipicamente un valore
		del tipo 8.4 )
		
		controllare che il valore METHOD nella linea
		
		# TYPE  DATABASE    USER        CIDR-ADDRESS          METHOD

		 local   all         all                           		   
		 
		sia un valore che permetta l'autenticazione senza password, ad esempio 
		TRUST (vedere manuale postgresql), ed eventualmente modificare tale 
		valore.

        Alternativamente, è possibile specificare l'autenticazione dell'utente postgres 
        come peer (quindi permettere solo all'utente di sistema postgres di accedere come 
        utente postgres), e considerare sicura (trust) l'autenticazione dall'utente che 
        andremo a creare da parte di qualsiasi utente di sistema. Quindi ad esempio:

		# TYPE  DATABASE    USER        CIDR-ADDRESS          METHOD

		 local   all         postgres                          peer 		   
		 local   all         nome_utente                       trust 		   
		
	2.2	quindi:
		$ createuser -D -P -U postgres nome_utente
		$ createdb -U postgres -O nome_utente -E 'utf8' -T 'template0' nome_DB
	
3.	Log-in al database creato e associato all'utente:

	$ psql -d nome_DB -U nome_utente -W


***** Installare virtualenv, easy_install, pip, virtualenvwrapper

Virtualenv è un pacchetto utilizzato per creare ambienti di sviluppo Python 
isolati. Questo è molto utile nel caso si voglia testare il comportamento di un 
programma usando, appunto, diverse versioni di Python. Virtualenvwrapper 
semplifica l'uso di virtualenv, la gestione dei virtual environment e il
passaggio tra diversi virtual environment.
Pip è un tool per installare e gestire pacchetti Python contenuti nel Python 
Package Index. Rimpiazza easy_install (utile comunque per l'installazione di 
pip).
 
1.	Installare pip:
 
	$ sudo apt-get install python-pip
	###### $ sudo apt-get install python-setuptools python-dev build-essential
	###### $ sudo easy_install -U pip
	$ pip --version --> verificare l'installazione

2.1	Installare virtualenv e virtualencwrapper:

	######### $ sudo pip install -U virtualenv --> installare virtualenv
	######### $ virtualenv --version--> verificare l'installazione
	
	######### $ sudo pip install virtualenvwrapper --> installare virtualenvwrapper
	$ apt-get install virtualenvwrapper --> installare virtualenvwrapper

2.2 Inizializzare l'ambiente per virtualenvwrapper:

    NOTA: percorso_cartella indica il persorso alla cartella dove i virtualenvironment verranno installati

    -mkdir -p percorso_cartella/envs
	-source /etc/bash_completion.d/virtualenvwrapper --> script 

    In seguito aggiungere la seguenti linea al proprio shell startup file (es. ~/.bashrc):

    -export WORKON_HOME=percorso_cartella/envs


***** Installare GIT

GIT è un sistema di versioning.

1.	Installare i pacchetti:

	$ sudo apt-get install git-core git-svn
	$ git version --> per controllare la versione
	
2.	Alcuni comandi utili:

	$ git submodule init --> agiunge le URL dei repository dei sottomoduli al 
							 file .git/config leggendo da ".gitmodules"
	$ git submodule update --> clona i repositroy e controlla i commit per 
							   controllare eventuali modifiche da apportare in 
							   locale
	$ git submodule sync --> aggiorna il file .git/config, sincronizzando i 
							 sottomoduli
	$ git pull --> controlla se in un repository master sono presenti modifiche
				   non presenti nella copia locale del codice, sincronizzando, 
				   eventualmente, le due versioni. 

