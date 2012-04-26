.. Gasista Felice documentation master file, created by
   sphinx-quickstart on Thu Mar 29 07:53:14 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Benvenuti nella documentazione di Gasista Felice!
=================================================

Contenuti:
==========

.. toctree::
   :maxdepth: 2
   
   base
   gas
   supplier
   des
   des_notification
   rest


Overview
========

* **Base:**
  É l'app che contiene tutte le funzionalità di base estese da tutte le altre applicazioni. 

* **Gas:**
  L'applicazione principale di Gasista Felice, qui vengono gestite principalmente le informazioni dei Gasisti (account, conti ecc.) e gli ordini ai fornitori. 

* **Supplier:**
  Contiene gli elementi per la gestione dei fornitori oltre ad informazioni su prodotti, fornitori e produttori.

* **Des:**
  API per la gestione del DES e delle relazioni tra questo e altri soggetti economici. Controlla anche l'autenticazione degli utenti del DES.

* **Des_notification:**
  Tiene traccia ed informa sulle modifiche all'interno del DES.

* **Rest:**
  Intyerfaccia Utente. É composta da diversi blocchi, dove ogni blocco raggruppa funzionalità analoghe.


Struttura delle cartelle del programma
======================================
::

  base
    base/templatetags
    base/management
    base/management/commands
    base/migrations
    base/forms
  supplier - 
    supplier/management
    supplier/management/commands
    supplier/migrations
  lib
    lib/fields
  locale
    fixtures
    fixtures/supplier
    fixtures/base
    fixtures/gas
    fixtures/auth
    fixtures/des
  gas
  gas/models
    gas/management
    gas/management/commands
    gas/migrations
    gas/forms
    gas/forms/order
  static/nui
    static/nui/images
    static/nui/blocks
    static/nui/style
    static/nui/scripts
    static/nui/img
    templates
    templates/registration
    comments
  des
    des/management
    des/management/commands
    des_notification
    des_notification/templates
    des_notification/templates/notification
    des_notification/management
    des_notification/management/commands
    log
  admin
    admin/templatetags
    admin/templates
    admin/templates/admin
  rest
    rest/views
    rest/views/blocks
    rest/models
    rest/templates
    rest/templates/blocks
    rest/templates/blocks/transactions
    rest/templates/blocks/basket_sent
    rest/templates/blocks/base
    rest/templates/blocks/gas_users
    rest/templates/blocks/prepared_orders
    rest/templates/blocks/recharge
    rest/templates/blocks/suppliers_report
    rest/templates/blocks/supplier_users
    rest/templates/blocks/order_report
    rest/templates/blocks/fee
    rest/templates/blocks/stored_orders
    rest/templates/blocks/users
    rest/templates/blocks/basket
    rest/templates/blocks/order
    rest/templates/blocks/gasstocks
    rest/templates/blocks/curtail
    rest/templates/blocks/stocks
    rest/templates/html
    rest/templates/values

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

