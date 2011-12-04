================
Optional modules
================

Askbot supports a number of optional modules, enabling certain features, not available 
in askbot by default.

.. _sphinx-search:

Sphinx search
=============
Askbot supports Sphinx search - and at this point only for MySQL.
Tested with sphinx 0.9.8.
May be a little outdated, please give your feedback if that is the case.

To enable:

* install `sphinx search package <http://sphinxsearch.com/>`_
* if necessary to support Chinese language, instead take `sphinx for Chinese <http://code.google.com/p/sphinx-for-chinese/>`_
* prepare configuration file by running command ``python manage.py get_askbot_sphinx_config > sphinx.conf``
* if necessary, modify the ``.conf`` file (may be needed for language other than English
* place the ``sphinx.conf`` file to an appropriate location, like /etc/sphinx/

Install django-sphinx python module (and follow all instructions)

    pip install django-sphinx

In ``settings.py`` add::

    SPHINX_API_VERSION = 0x113 #according to django sphinx doc
    USE_SPHINX_SEARCH = True
    ASKBOT_SPHINX_SEARCH_INDEX = 'askbot'

.. note::
    Value of SPHINX_API_VERSION may depend on the version of 
    python sphinx api installed with the django-sphinx application,
    please refer to the django-sphinx documentation.

Initialize the sphinx index (may need to log in as root)::

    indexer askbot --config /etc/sphinx/sphinx.conf

Start the sphinx search daemon::

    /usr/local/bin/searchd --config /etc/sphinx/sphinx.conf &

Also, add the line above to the file /etc/rc.d/rc.local or equivalent to start the daemon
when the server reboots.

Set up a periodic re-indexing job (using cron)::

    indexer askbot --rotate --config /etc/sphinx/sphinx.conf

Finally, add lin

.. _embedding-video:

Embedding video
===============

Want to share videos in askbot posts? It is possible, but you will have to install a forked 
version of ``markdown2`` module, here is how::

    pip uninstall markdown2
    pip install -e git+git://github.com/andryuha/python-markdown2.git#egg=markdown2

Also, for this to work you'll need to have :ref:`pip` and :ref:`git` installed on your system.

Finally, please go to your forum :ref:`live settings <live-settings>` --> 
"Settings for askbot data entry and display" and check "Enable embedding video".

Limitation: at the moment only YouTube and Veoh are supported.

.. _ldap:

LDAP authentication
===================

To enable authentication via LDAP
(Lightweight Directory Access Protocol, see more info elsewhere)
, first :ref:`install <installation-of-python-packages>`
``python-ldap`` package:

    pip install python-ldap

After that, add configuration parameters in :ref:`live settings <live-settings>`, section
"Keys to connect the site with external services ..." 
(url ``/settings/EXTERNAL_KEYS``, relative to the domain name)

.. note::
    Location of these parameters is likely to change in the future.
    When that happens, an update notice will appear in the documentation.

The parameters are:

* "Use LDAP authentication for the password login" - enable/disable the feature.
  When enabled, the user name and password will be routed to use the LDAP protocol.
  Default system password authentication will be overridden.
* "LDAP service provider name" - any string - just come up with a name for the provider service.
* "URL fro the LDAP service" - a correct url to access the service.
* "Explain how to change the LDAP password"
  - askbot does not provide a method to change LDAP passwords
  , therefore - use this field to explain users how they can change their passwords.

Uploaded avatars
================

To enable uploadable avatars (in addition to :ref:`gravatars <gravatar>`), 
please install development version of
application ``django-avatar``, with the following command::

    pip install -e git+git://github.com/ericflo/django-avatar.git#egg=django-avatar

Then add ``avatar`` to the list of ``INSTALLED_APPS`` in your ``settings.py`` file 
and run (to install database table used by the avatar app):

    python manage.py syncdb

Also, settings ``MEDIA_ROOT`` and ``MEDIA_URL`` will need to be added to your ``settings.py`` file.

.. note::

    Version of the ``avatar`` application available at pypi may not
    be up to date, so please take the development version from the 
    github repository

Wordpress Integration 
=====================

To enable authentication for self hosted wordpress sites(wordpress.com blogs will work with openid login). To enable it follow the following steps:

* Check if you have the package `"python_wordpress_xmlrpc <http://pypi.python.org/pypi/python-wordpress-xmlrpc/1.4>`_ from pypi.
* Go to your wordpress blog admin panel and serch for: Settings->Writing->Remote Publishing then check the box for XML-RPC.
* Go back to your askbot site settings and click on *Login Provider Settings* and then activate the option *Activate to allow login with self-hosted wordpress site*, 
* Input your blog url to the xmlrpc.php file it will look something like this http://yoursite.com/xmlrpc.php
* Upload an icon for display in the login area.

After doing this steps you should be able to login with your self hosted wordpress site user/password combination.
