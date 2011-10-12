Install development version (04 jully 2011)
-------------------------------------------

1/7 download project code for GASISTA FELICE project from git repository
You must have your github account, set your public SSH ley on github and set localy your API Token
(gasdev)$ git clone git@github.com:feroda/gasistafelice.git

2/7 Install sub modules
(gasdev)$ cd gasistafelice
(gasdev)/gasistafelice$ git submodule update --init

3/7 Install requirements
(gasdev)$ pip install -r gasistafelice/requirements.txt`

4/7 Set your local settings
(gasdev)$ cd gasistafelice
(gasdev)/gasistafelice/gasistafelice$ cp default_settings.py settings.py --> copy the file to customize
(gasdev)/gasistafelice/gasistafelice$ gedit settings.py
The main thing is to set the database connexion
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
create your empty database first
(gasdev)/gasistafelice/gasistafelice$ python manage.py syncdb  --> Create tables and the super user
Note: (gasdev)/gasistafelice/gasistafelice$ python manage.py loaddata initial_data.json --> Initial data are loaded automaticaly with the syncdb operation

6/7 (optional) Load some data for testing
(gasdev)/gasistafelice/gasistafelice$ python manage.py loaddata test_data.json

7/7 Running
(gasdev)/gasistafelice/gasistafelice$ python manage.py runserver
From your preferred browser use the follwing links reguardless of your customizzation:
http://127.0.0.1:8000/admin/  --> Admin interface for Django 
http://127.0.0.1:8000/gas-admin/   --> Advancded Django admin interface
http://127.0.0.1:8000/gasistafelice/rest/   --> SANET interface customization for Gassista use
