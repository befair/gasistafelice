Install development version - 2nd february 2012
-----------------------------------------------

0. Prepare with your system with required software:

  * Git
  * PostgreSQL

  for Debian/Ubuntu --> apt-get install postgresql git-core
  other requirements are installed via pip install. Such as...

  * Django >= 1.3.1

  Create locale for your sytem 
  * sudo locale-gen it_IT.UTF-8

  We suggest you to make a local deploy in virtualenv, not a big virtual machine!
  but a virtual python environment in order to keep your system clean.

  Search for virtualenvwrapper 

1. Clone project GASISTA FELICE from GitHub repository

  * git clone https://github.com/feroda/gasistafelice.git

2. Install package requirements and submodules

  * git submodule update --init
  * pip install -r requirements.txt

3. Set your local settings

  * cd gasistafelice
  * gasistafelice/gasistafelice$ cp settings.py.dist settings.py --> copy the file to customize
  * /gasistafelice/gasistafelice$ gedit settings.py

  The main thing is to set the database connection
  ADMINS = (('xxxxx', 'a@a.it'),)
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gasdb',           
        'USER': 'utente',         
        'PASSWORD': 'xxxx',      
        'HOST': '',             
        'PORT': '',            
    }
  }

  INIT_OPTIONS = {
    'domain' : "ordini.desmacerata.it",
    'sitename' : "DES Macerata",
    'sitedescription' : "Gestione degli ordini per il Distretto di Economia Solidale della Provincia di Macerata (DES-MC)",
    'su_username' : "admin",
    'su_name'   : "Referente informatico",
    'su_surname': "del DES-MC",
    'su_email'  : "",
    'su_passwd' : "admin",
  }


4. Initialize data:

  * python manage.py syncdb --noinput
  * python manage.py init_superuser


5. (Optional) Load some data for testing

  * gasistafelice/gasistafelice$ python manage.py loaddata fixtures/auth/test_data.json

6. Running

  * gasistafelice/gasistafelice$ python manage.py runserver

  From your preferred browser (GF works with Firefox but you can try others...) 
  use the follwing links reguardless of your customization:

  http://localhost:8000/

  you could use also the admin interface to do some tests...:

  http://localhost:8000/admin/  --> Admin interface for Django 


Use PostgreSQL database
[-----------------------

If you want to set up a PostgreSQL db follow these steps:

.. sourcecode:: python

    (desmacerata1)fero@archgugu:~/src/gasistafelice/gasistafelice$ psql -U postgres
    psql (9.1.1)
    Type "help" for help.

    postgres=# create role desadmin  login password '';
    CREATE ROLE
    postgres=# create database desmc owner desadmin encoding 'utf8' template template0;
    CREATE DATABASE
    postgres=# grant all privileges on database desmc to desadmin;
    GRANT
    postgres=# \q


Setup cron for automatic order open and close
---------------------------------------------

Check every two minutes if there are orders to be opened or closed

.. sourcecode:: crontab

   \*/2 * * * * root /usr/local/gasistafelice/extra/sh_manage_wrapper.sh order_fix_state


WAS: OLD GUIDE
--------------

1/7 download project code for GASISTA FELICE project from git repository
You must have your github account, set your public SSH ley on github and set localy your API Token
(gasdev)$ git clone git@github.com:feroda/gasistafelice.git

2/7 Install sub modules
(gasdev)$ cd gasistafelice
(gasdev)/gasistafelice$ git submodule update --init

3/7 Install requirements
(gasdev)$ pip install -r requirements.txt`

4/7 Set your local settings
(gasdev)$ cd gasistafelice
(gasdev)/gasistafelice/gasistafelice$ cp settings.py.dist settings.py --> copy the file to customize
(gasdev)/gasistafelice/gasistafelice$ gedit settings.py
The main thing is to set the database connection
ADMINS = (('xxxxx', 'a@a.it'),)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
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
create your empty database first
(gasdev)/gasistafelice/gasistafelice$ python manage.py syncdb  --> Create tables but SAY NO when asked to create the super user (!)
(gasdev)/gasistafelice/gasistafelice$ python manage.py init_superuser --> Create DES base object and the super user following settings.py 
Note: (gasdev)/gasistafelice/gasistafelice$ python manage.py loaddata initial_data.json --> Initial data are loaded automaticaly with the syncdb operation

6/7 (optional) Load some data for testing
(gasdev)/gasistafelice/gasistafelice$ python manage.py loaddata test_data.json

7/7 Running
(gasdev)/gasistafelice/gasistafelice$ python manage.py runserver
From your preferred browser use the follwing links reguardless of your customizzation:
http://127.0.0.1:8000/admin/  --> Admin interface for Django 
http://127.0.0.1:8000/gas-admin/   --> Advancded Django admin interface
http://127.0.0.1:8000/gasistafelice/rest/   --> SANET interface customization for Gassista use



