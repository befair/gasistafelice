Istruzioni per installare Gasista Felice (04 luglio 2011)
---------------------------------------------------------

1/7 scaricare il codice del progetto GASISTA FELICE dal repository pubblico
se non avete impostato la vostra chiave pubblica sul sito di GITHUB ed registrato la vostra API TOKEN in locale usare le note in fondo a questo docummento.
(gasdev)$ git clone git@github.com:feroda/gasistafelice.git

2/7 Installare gli sotti moduli
(gasdev)$ cd gasistafelice
(gasdev)/gasistafelice$ git submodule update --init

3/7 Installare i requisity del progetto
(gasdev)$ pip install -r gasistafelice/requirements.txt

4/7 Impostare gli vostri settings locale
(gasdev)$ cd gasistafelice
(gasdev)/gasistafelice/gasistafelice$ cp default_settings.py settings.py --> copia il file generale da personalizzare (nota usare from default_settings.py import *?)
(gasdev)/gasistafelice/gasistafelice$ gedit settings.py
In sostanza personnalizzare la connessione al vostro database. 
ADMINS = (('xxxxx', 'a@a.it'),)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gasdb',                      # Or path to database file if using sqlite3.
        'USER': 'utente',                     # Not used with sqlite3.
        'PASSWORD': 'xxxx',                   # Not used with sqlite3.
        'HOST': '',                           # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
    }
}
$ export DJANGO_SETTINGS_MODULE=gasistafelice.settings
(optional)$ export PYTHONPATH=/www
$ sudo locale-gen it_IT.UTF-8
$ django-admin.py runserver
Validating models...
0 errors found

5/7 Sincronizzare database
creare la vostra bancadati prima
(gasdev)/gasistafelice/gasistafelice$ python manage.py syncdb  --> Creazione delle tabelle ed impostare un utente amministartore
(gasdev)/gasistafelice/gasistafelice$ python manage.py loaddata initial_data.json --> vengono caricati in automatico con il SyncDB

6/7 (facoltativo) Caricare dei dati di prova
(gasdev)/gasistafelice/gasistafelice$ python manage.py loaddata test_data.json

7/7 Eseguire 
(gasdev)/gasistafelice/gasistafelice$ python manage.py runserver
dal browser navigare usando i varie link di partenza (al riguardo delle vostre impostazioni):
http://127.0.0.1:8000/admin/  --> Interfaccia amministratore di default di django
http://127.0.0.1:8000/gas-admin/   --> Interfaccia amministratore evoluta
http://127.0.0.1:8000/gasistafelice/rest/   --> Con l'interffacia SANET per l'accesso gassista










****************************************************************************
***********************   Allegato Preparazione PC   ***********************
****************************************************************************



Potete preparare il vostro ambiante di lavoro. Cui sotto alcune note per guidarvi
***** Install Python
Python 2.7 va bene (kappao per python 3.2 django non lo fa girare adesso che scriviamo queste note)
$ sudo apt-get install python
-- set LD_LIBRARY_PATH and PYTHON_PATH enviroment vars conveniently 
-- or 
-- to specify /usr as install prefix by setting the CMAKE_INSTALL_PREFIX cmake option. 
-- ./configure --prefix=$HOME/usr-64/python-2.7.1
$ python  --> avviare la console di python 
Python 2.7.1+ (r271:86832, Apr 11 2011, 18:05:24)  ... [GCC 4.5.2] on ...
$ which python --> /usr/bin/python
$ python --version  --> Python 2.7.1+

***** Install server
APACHE
$ httpd -v --> Installato?
$ sudo apt-get install apache2 python-setuptools libapache2-mod-python libapache2-mod-wsgi
__configurare apache per python
$ sudo gedit /etc/apache2/sites-available/default   --> se usate la cartella di default
OR
$ sudo gedit /etc/apache2/apache2.conf  --> se usate una cartella specifica
<Directory /var/www/>
    Options Indexes FollowSymLinks MultiViews
    AllowOverride None
    Order allow,deny
    allow from all
++  AddHandler mod_python .py
++  PythonHandler mod_python.publisher
++  PythonDebug On
</Directory>
Salvare, chiudere e testare 
$ sudo gedit /var/www/test.py
$ sudo gedit /your_configured_path/test.py
def index(req):
  return "Test successful";
Dal browser puntare a http://localhost/test.py --> Test successful

***** Install dababase
********** MYSQL
$ sudo apt-get install mysql-server python-mysqldb  --> definire la password amministratore
$ sudo apt-get install mysql-client
$ sudo mysqladmin -u root -h localhost password 'mypassword' 
$ sudo mysqladmin -u root -h myhostname password 'mypassword' 
$ sudo apt-get install php5-mysql
Potete accedere a MySQL server cosi:
mysql -u root -p
password: lnx
mysql> 
\c clear
\h help
\q quit
Installare un query browser
$ sudo apt-get update && apt-get install mysql-admin
$ sudo apt-get install phpmyadmin --> durante l'installazione scegliere APACHE > lighttpd 
Settare per girare su Apache
$ sudo gedit /etc/apache2/apache2.conf
++ #phpmyadmin for mySqlserver
++ Include /etc/phpmyadmin/apache.conf
Salvare, chiudere, riavviare APACHE e testare 
$ sudo /etc/init.d/apache2 stop
$ sudo /etc/init.d/apache2 start
   or
$ sudo /etc/init.d/apache2 restart
http://localhost/phpmyadmin --> Ok
$ sudo netstat -tap | grep mysql
tcp        0      0 localhost.localdo:mysql *:*                     LISTEN      1054/mysqld    
$ sudo netstat -tap all 

********** SQLLITE
$ sudo apt-get install sqlite3 python-sqlite

********** POSTGRESQL
Module psycop2: Psycopg is PostgreSQL adapter for Python programming language.
$ sudo apt-get install postgresql python-psycopg2
$ sudo apt-get install postgresql-client subversion pgadmin3 pgadmin3-data
Sostituire la password dell'utente amministratore ‘postgres’
$ sudo su postgres -c psql template1
psql (8.4.8)
template1=# ALTER USER postgres WITH PASSWORD ‘new_password’;
template1=# \q
$ sudo passwd -d postgres
passwd: password expiry information changed.
$ sudo su postgres -c passwd
Enter new UNIX password: new_password
Retype new UNIX password: new_password
dalla shell creare un utente con tutti privilege e creare una bancadati 'gasdb'
$ sudo -u postgres createuser -D -A -P utente 
$ sudo -u postgres createdb -O utente gasdb

***** Installare virtualenv, easy_install, pip, virtualenvwrapper
$ sudo apt-get install python-setuptools python-dev build-essential  --> easy_install
$ sudo easy_install -U pip  --> pip
$ pip --> verificare l'installazione
Usage: pip COMMAND [OPTIONS] ...
$ sudo pip install -U virtualenv --> installare virtualenv
$ virtualenv --> verificare l'installazione
... Usage: virtualenv [OPTIONS] DEST_DIR ...
$ sudo pip install virtualenvwrapper --> installare virtualenvwrapper
$ export WORKON_HOME=~/Envs  --> sostiuire la cartella Envs con quello che vi piace 
$ mkdir -p $WORKON_HOME
$ mkvirtualenv gasdev  --> creare ambiente di lavoro
$ source Envs/gasdev/bin activate --> activare l'ambiante di lavoro
$ workon gasdev --> activare l'ambiante di lavoro
--> lavorare
(gasdev)$ deactivate  --> uscire dall'ambiante di lavoro


Installare alcuni software nell'ambiante di lavoro

***** Install DJANGO
(gasdev)$ pip install django

***** Install SPHINX
(gasdev)$ pip install sphinx

***** Install DJANGO-PERMISSIONS
(gasdev)$ pip install django-permissions

***** Install DJANGO-WORKFLOW
(gasdev)$ pip install django-workflows

***** validare il codice
$ pip install configobj   
$ sudo apt-get install pychecker 
$ pip install validate

***** verificare l'installazione
(gasdev)$ pip freeze  --> lista dei pacchetti installati
(gasdev)$ python --> avviare la console
Python 2.7.1+ (r271:86832, Apr 11 2011, 18:05:24) 
[GCC 4.5.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import django  --> No error = good
>>> print django.get_version() --> 1.3
>>> CTRL+D to exit
(gasdev)$ django-admin.py --version   -->  1.3
(gasdev)$ python -c "import django; print django.get_version()" --> 1.3

***** Installare GIT
$ sudo apt-get install git-core git-svn
$ git version --> 1.7.4.1
$ git config --list
$ ssh-keygen -t rsa -C "your_email@youremail.com" --> generare le chiave SSH
La vostra identificazione salvata dentro /home/vostro_pc/.ssh/id_rsa  e   la chiave pubblica dentro /home/lnx/.ssh/id_rsa.pub.
The key fingerprint is: fc:06:72:d2:45:a2:7d:e4:27:87:7b:1b:8d:fe your_email@youremail.com
$ cd ~/.ssh
~/.ssh$ gedit id_rsa.pub
copiare e andare sul vostro profillo nel sito di github (creare una account se non l'avete già): https://github.com/account#profile_bucket
Aggiugnere una chiave pubblica -->impostare un titolo e incollare 
$ cd ~
Dal sito di github reccuperare la vostra API token (Edit profile > Account admin) e inserirla nel vostro computer
$ git config --global github.user you_github_account
$ git config --global github.token f2fb6446f9dasdfbfb2df44c96692e
$ git config --list   --> verificare le vostre informazioni
$ gedit ~/.gitconfig
github connect
$ ssh git@github.com
... Permanently added 'github.com,207.97.227.239' (RSA) to the list of known hosts ...

