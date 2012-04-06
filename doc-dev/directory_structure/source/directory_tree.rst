.. Gasista Felice documentation master file, created by
   sphinx-quickstart on Thu Mar 29 07:53:14 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Gasista Felice's documentation!
==========================================

Contents:

.. toctree::
   :maxdepth: 2
   
   base
   gas
   supplier
   des
   des_notification
   rest


Overview
============

* **Base:**
  economic accounts management, logging management, constants and base classes to extend in the other applications 

* **Gas:**
  extends and implements the classes into the **Base** application

* **Supplier:**
  contains the implementation of the forms useful to manage the suppliers and some information about Products, Suppliers, Producers. It relies to the **Base** app.

* **Des:**
  API for DES management (create, edit, ...) and control of the relation between DES and other economical subjects. It also manages the authentication of the DES users.

* **Des_notification:**
  application used to trace changes into the DES as well as to notify them.

* **Rest:**
  application for the User Interface. The UI is composed of all the blocks of the program: a block collects fetures related with each other.


 Applications and modules::

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

