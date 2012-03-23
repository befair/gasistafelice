****************************************************************************
***********************   PREPARAZIONE SISTEMA   ***************************
****************************************************************************

Questo file contiene istruzione su come preparare l'ambiente di lavoro nel 
caso in cui ci si avvicini per la prima volta agli strumenti necessari 
all'installazione di Gasista Felice.


***** Python

1.	Controllare se python è installato sul proprio Sistema con:
	
	$ python --version -->  versione di python installata 
	
	se ritrona errore (python non è installato) saltare alla prossima sezione, 
	altrimenti continuare. 

2.	Installazione python:

	$ sudo apt-get install python



********** SQLITE

SQLite è una libreria che implementa un DBMS SQL che permette la creazione e la
gestione di una base di dati (comprese tabelle, query, form, report).

$ sudo apt-get install sqlite3 python-sqlite



********** POSTGRESQL

PostgeSQL è un database relazionale. In particolare, psycop2 è un PostgreSQL 
adapter per Python.
	
1.	Installare i seguenti pacchetti:
	
	$ sudo apt-get install postgresql python-psycopg2
	$ sudo apt-get install postgresql-client subversion pgadmin3 pgadmin3-data

2.	Creazione di un utente e di un DB associato all'utente creato:

	2.1	prima di procedere, controllare di avere il permesso per autenticarsi
		controllando nel file di configurazione di postgresql:
		
		$ sudo gedit /etc/postgresql/versione/main/pg_hba.conf
		
		("versione" indica la versione di postgresql, tipicamente un valore
		del tipo 8.4 )
		
		controllare che il valore METHOD nella linea
		
		# TYPE  DATABASE    USER        CIDR-ADDRESS          METHOD

		 local   all         all                           		   
		 
		 sia un valore che permetta l'autenitcazione con password, ad esempio 
		 TRUST (vedere manuale postgresql), ed eventualmente modificare tale 
		 valore.
		
		
	2.2	quindi:
		$ sudo -u postgres createuser -D -A -P nome_utente 
		$ sudo -u postgres createdb -O nome_utente nome_DB
	
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
 
	$ sudo apt-get install python-setuptools python-dev build-essential
	$ sudo easy_install -U pip
	$ pip --version --> verificare l'installazione

2.1	Installare virtualenv e virtualencwrapper:

	$ sudo pip install -U virtualenv --> installare virtualenv
	$ virtualenv --version--> verificare l'installazione
	
	$ sudo pip install virtualenvwrapper --> installare virtualenvwrapper

2.2 Aggiungere le seguenti linee al proprio shell startup file (es. ~/.bashrc):

	-export WORKON_HOME=$HOME/.virtualenvs
	-export PROJECT_HOME=$HOME/Development_folder --> sostituire con la cartella
	che si vuole
	-source /usr/local/bin/virtualenvwrapper.sh --> script 
	



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


******** Installare gasista felice come developer (DA RIVEDERE)

1.	Creazione chiave SSH per stabilire una connessione sicura tra GitHub e il 
	proprio computer:
	
	nota: Per inserire la propria chiave SSH nel sito GitHUb è necessario 
	possedere un account nel suddetto sito.
	
	1.1	Controllare se già esiste una chiave SSH nel prorio computer:
		
		$ cd ~/.ssh
		
		quindi
		
		$ ls -a
		
		se la cartella non esiste, o se non contiene due file chiamati id_rsa e 
		id_rsa.pub, saltare al opunto 1.3, altrimenti continuare con il prossimo 
		punto.
	
	1.2	Backup e rimozione della chiave SSH esistente:
	
		$ mkdir key_backup (crea una sottocartella in ~/.ssh)
		$ cp id_rsa* key_backup (copia id_rsa e id_rsa.pub nella sottocartella)	 
		$ rm id_rsa* (rimuove i file copiati per premettere la creazione della 
					  nuova chiave)
					  
	1.3	Generazione chiave SSH:
	
		$ ssh-keygen -t rsa -C "indirizzo_email@dominio.com"
		
		verrà richiesto dove salvare la chiave, premere invio senza inserire 
		nulla per salvarla nella cartella predefinita(indicata nella richiesta).
		Quindi, scegliere una password e inserirla quando richiesto.
		
	1.4 Aggiungere la propria chiave SSH sul sito GitHub:
	
		1.4.1 Sul sito GitHub cliccare su “Account Settings” > “SSH Public Keys” > 
			  “Add another public key”
		1.4.2 Aprire il file id_rsa.pub creato precedentemente e copiarne il 
			  contenuto ESATTAMENTE COME E'SCRITTO NEL FILE nel campo "key" 
			  della pagina del sito.
		1.4.3 Premere il bottone "Add Key"
		1.4.4 Per testare il tutto, esguire da terminale
			
			  $ ssh -T git@github.com
			  
			  e rispondere "yes" alla richiesta di connessione al sito GitHub

2.	Clonare il repository in locale:
	
	(gasdev)$ git clone git@github.com:feroda/gasistafelice.git

3.	Richiedere l'autorizzazione alla scrittura nel repository (INCOMPLETO)		

