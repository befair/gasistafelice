Istruzioni per installare Gasista Felice (9 marzo 2012)
---------------------------------------------------------


0/7

	E' consigliato installare gasista felice in un virtual environment (se 
	necessario consultare il file "preINSTALL.ita.rst" per informazioni sui 
	virtual environment):

	$ mkvirtualenv gasdev  --> creare ambiente di lavoro

	('gasdev' è un esempio di nome per il virtual environment da creare, ma
	 è possibile scegliere un nome qualsiasi).

	I prossimi passi dell'installazione avranno come ambiente il virtual 
	environment creato. 
	
	Per accedere in seguito al virtual environment, eseguire:
	
	$ workon gasdev  



1/7 Scaricare il codice del progetto GASISTA FELICE dal repository pubblico:

	(gasdev)$ git clone https://github.com/feroda/gasistafelice.git


2/7 Installare i sottomoduli:

	(gasdev)$ cd gasistafelice
	(gasdev)/gasistafelice$ git submodule update --init


3/7 Installare i requisiti del progetto:

	(gasdev)$ cd gasistafelice
	(gasdev)/gasistafelice$ pip install -r requirements.txt
	
	-nota: 
	
	 prima di procedere con l'installazione dei requisiti, assicurarsi che 
	 il proprio sistema soddisfi i requisiti necessari all'installazione dei 	 requisiti di gasista felice.
	 
		-In un sistema di derivazione debian, assiurarsi di avere instal		lati i seguenti pacchetti:

		- python-dev (PYTHON)
		- libpq-dev (PostgreSQL)
		- libsqlite3-dev (SQLite)

		-In un sistema windows, scaricare ed installare:
		
		- python (versione 2.6.5)
		- postgresql
		- sqlite



4/7 Configurare Gasista Felice:

1.	Creare il file delle impostazioni in gasistafelice/gasistafelice/ e 
	chiamarlo "settings.py", quindi copiarvi il contenuto del file 
	"settings.py.dist" sito nella stessa directory:
	
	(gasdev)/gasistafelice$ cd gasistafelice
	(gasdev)/gasistafelice/gasistafelice$ cp settings.py.dist settings.py
	
2.	aprire il file "settings.py": 
	
	quindi decommentare i setting relativi a "DATABASES" e "INIT_OPTIONS".



5/7 Sincronizzare il database:

1.	Creazione delle tabelle:

	E' necessario disporre di un database già creato ed associato ad un utente.
	Il nome del database, insieme all'username e ala password dell'utente a cui 
	è associato, vanno inseriti nei campi corrispondenti della struttura 
	DATABASES nel file "settings.py" in gasistafelice/gasistafelice/.
	
	(gasdev)/gasistafelice/gasistafelice$ python manage.py syncdb --noinput

    e poi applicare le migrazioni con:

	(gasdev)/gasistafelice/gasistafelice$ python manage.py migrate

2.	Creare l'utente amministratore di gasistafelice:

	(gasdev)/gasistafelice/gasistafelice$ python manage.py init_superuser
	
	l'username e la password di amministrazione verrano lette dai campi 
	corrispondenti della struttura INIT_OPTIONS nel file "settings.py".

6/7 Far partire il server:

	(gasdev)/gasistafelice/gasistafelice$ python manage.py runserver

	In seguito, sarà possibile accedere ai seguenti link tramite browser:
	
	- http://127.0.0.1:8000/


7/7	(punto facoltativo) Caricare dei dati di prova:

	(gasdev)/gasistafelice/gasistafelice$ python manage.py loaddata 
		test_data.json
