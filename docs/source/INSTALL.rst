.. _installationguide:


Installation guide for developers
=================================

This guide is intended for modern Debian/Ubuntu-based and Arch-based GNU/Linux distributions.

    Note: we'll use ``gf_dev`` as reference name for this guide.  Of course, you can change it as you wish.


System Requirements
-------------------

Generate Italian locale for your system::

    $ sudo locale-gen it_IT.UTF-8

We need to install common development packages, Git, Python and related packages, SQLite and PostgreSQL databases.

On Debian/Ubuntu::

    $ sudo apt-get install build-essential git-core \
        python python-{dev,imaging,pip,setuptools,virtualenv} virtualenvwrapper \
        sqlite3 libsqlite3-dev python-sqlite \
        postgresql postgresql-client libpq-dev python-psycopg2

On Arch::

    $ sudo pacman -S base-devel git \
        python2 python2-pip python-virtualenvwrapper \
        sqlite \
        postgresql postgresql-libs python2-psycopg2


Database
--------

Only on Arch, first of all initialize ``postgres`` user::

    $ sudo -u postgres initdb --locale en_US.UTF-8 -E UTF8 -D '/var/lib/postgres/data'

Now start PostgreSQL daemon::

    # On Debian/Ubuntu
    $ sudo service postgresql start

    # On Arch (and Debian Jessie?)
    $ sudo systemctl start postgresql

Then, open the file::

    # On Debian/Ubuntu  (if necessary, replace "9.3" accordingly to your version of PostgreSQL)
    $ sudo vim /etc/postgresql/9.3/main/pg_hba.conf

    # On Arch
    $ sudo vim /var/lib/postgres/data/pg_hba.conf

Add the last line::
		
    # TYPE  DATABASE    USER        CIDR-ADDRESS          METHOD

    local   all         postgres                          peer
    local   all         gf_dev                            trust

Reload PostgreSQL::

    # On Debian/Ubuntu
    $ sudo service postgresql reload

    # On Arch (and Debian Jessie?)
    $ sudo systemctl reload postgresql

Create ``gf_dev`` PostgreSQL user::

    $ sudo -u postgres createuser -D -A gf_dev

Create ``gf_dev`` PostgreSQL database::

    $ sudo -u postgres createdb -O gf_dev -E utf-8 -T template0 gf_dev

Test access to the new database (then, exit with ``\q`` or ``CTRL+d``)::

    $ psql -d gf_dev -U gf_dev
    psql (9.3.5)
    Type "help" for help.

    gf_dev=#


Virtual Environment
-------------------

    Note: we'll assume your virtualenvs root is ``~/.config/venvs``.

Set the virtualenv root to your ``.bashrc`` (or ``.zshrc``) and reload it::

    $ echo 'export WORKON_HOME=$HOME/.config/venvs' >> ~/.bashrc
    $ source ~/.bashrc

Create your virtualenv::

    $ mkvirtualenv -p `which python2` gf_dev

Now, you've enabled the virtualenv and you'll see something like::

    (gf_dev)$

..

    For deactivate it use ``deactivate``, for enable it again ``workon gf_dev``.


Web Application
---------------

    Note: we'll assume your repositories root is ``~/src``.

Clone the Gasista Felice repository::

    (gf_dev)$ cd ~/src
    (gf_dev)$ git clone git://github.com/befair/gasistafelice.git gf_dev

..

    Alternatively, if you've a Github account::

        (gf_dev)$ git clone git@github.com:befair/gasistafelice.git gf_dev

Go inside new directory and install submodules::

    (gf_dev)$ cd gf_dev
    (gf_dev)$ git submodule update --init

Install Python requirements inside your virtualenv::

    (gf_dev)$ pip install -r gasistafelice/deps/dev.txt

Edit ``settings.py`` accordingly to your needs::

    (gf_dev)$ cd gasistafelice
    (gf_dev)$ vim gf/settings.py

Initialize the database::

    (gf_dev)$ ./manage.py makemigrations --noinput
    (gf_dev)$ ./manage.py migrate

Create the admin user::

    (gf_dev)$ ./manage.py init_superuser

Optionally, you could load some example data::

    (gf_dev)$ ./manage.py loaddata fixtures/auth/test_data.json

Now let's run the web server::

    (gf_dev)$ ./manage.py runserver

Go to http://localhost:8000/ and enjoy Gasista Felice!!

You could use also the Django admin interface to do some tests at http://localhost:8000/gasistafelice/admin/.


Next time
---------

Next time you'll run Gasista Felice, you've to:

Go to project root, inside ``gasistafelice`` directory::

    $ cd ~/src/gf_dev/gasistafelice

Enable virtualenv and export the following environment variables::

    $ workon gf_dev

Run the web server::

    (gf_dev)$ ./manage.py runserver


Next steps
----------

Now you can see next guides:

* configure mail
* use GitHub account
* forking model
