Overview
========

The DES accounting model adopted by GasistaFelice is a concrete implementation of the generic accounting model at the hearth of the django-simple-accounting_ app.

In fact, django-simple-accounting_ was designed and developed with a DES-like scenario in mind: i.e., multiple economic actors and complex money flows amongst them.

Economic subjects
=================

In a DES, there are three primary kinds of economic actors (o, as we like to say, **economic subjects**): People, GASs and Suppliers.  

Each economic subject can exchange money, goods and services with other economic subjects within the same (or another) DES;  money flows between economic subjects are called **transactions**. 

In order to record and manage transactions, we need the concept of **account**.  An account is just a way to group and label transactions between economic subjects: a transaction can be described as a money flow from a source account to one or more target accounts, potentially passing through intermediate accounts.  Each account belongs to one (and only one) economic subject, the account's owner; accounts belonging to a given subject are organized in tree-like structure (**account hierarchy**) and together made what we call the subject's **accounting system**.

Accounts  can be of one of two very different types:
* **stock-like** accounts represent amounts of money owned by the subject. By convention, if these amounts are positive they are called *assets* (e.g. cash in wallet), while if negative they are called **liabilities** (e.g. a debt);
* **flux-like** accounts are similar to counters recording money flows *between* different accounting systems

Generally, a transaction involves at least 2 accounts; more complex transaction can involve up to ``3n + 1`` accounts, where ``n`` is the number of splits constituting the transaction itself.

Every robust accounting solution should implement what is know as **double-entry** accounting: in a nutshell, double-entry accounting - in its simplest form --  requires that every transaction generates two accounting records: one for both the source and target accounts.  This way, integrity of accounting records is automatically enforced (i.e. no money amount can disappear or be created from the vacuum).  In more general setups - as the DES one - transactions may involve more than 2 accounts, so more than two accounting records may be created for the transaction (one for each of the involved accounts). Such accounting records are called **ledger entries**, since they can be thought of as entries in a ledger associated to the given account.


Account hierarchies
===================

Generalities
------------

As we said, every economic subject in a DES (people, GASs, suppliers) operates its own accounting system, made up of a hierarchy of accounts meant to record and organize transactions involving the subject itself.  Some general facts about account hierarchies (a.k.a. **account trees**):

- every account tree is rooted at a special account called `ROOT`;
- an account belonging in a given account tree can be referenced by a string (**account path**) describing the path to follow in the tree in order to reach the given account, starting from the root account; 
- account paths are constructed by joining account names with a delimiter, that we refer as the *account path separator*; hereafter, we assume that account names are separated by the `/` characters, but it can be easily configured [1]_;
- by convention, the root account of a tree has an empty path (i.e. `/`);
- each account (barring the root one) has one of four basic account types: **asset**, **liability**, **income**, **expense**, depending on its meaning within the accounting system it belongs to.  Remember that assets and liabilities are stock-like accounts (i.e., they represent amounts of money), while incomes and expenses are flux-like accounts (they act as counters for money flows between accounting systems);
- due to their own nature, stock-like accounts can contain only other stock-like accounts; the same is true for flux-like ones;
- an account is said to be a **placeholder account** if it can't (directly) contain transactions (strictly speaking, ledger entries), but it's only used as a way to group other accounts.

DES-specific account hierarchies
--------------------------------

Below, for every type of economic subject in a DES, we describe the corresponding hierarchy of accounts composing its accounting system. For the sake of clarity, we provide both a visual representation and some descriptive notes.

*Meaning of abbreviations*:

* A:= Asset
* L:= Liability
* I:= Income
* E:= Expense
* P:= Placeholder

People
------
From an accounting point of view, a person-like subject can be abstracted as:

* an asset-type account (*wallet*), (virtually) containing money the person is willing to inject in the DES's financial circuit (e.g. by making purchases as a GAS member)
* an expense-type hierarchy of accounts used to record money amounts flowing out his/her accounting system; in practice, payments (s)he makes to one of the GASs (s)he is member of (recall that a person can be member of multiple GASs); in turn, payments made to a GAS could represent:
 
  - recharges to the member own (virtual) pre-payed account in the GAS
  - payment of GAS's annual membership fees (if any)

::

      . ROOT (/)
      |----------- wallet [A]
      |
      +----------- expenses [P,E]+
				 |
      			         +--- gas [P, E] +
				      	      	 |
      				     	       	 +--- <UID gas #1>  [P, E]+
						 | 			  |
						 |  			  +--- recharges [E]
						 | ..			  |	 
						 | 			  +--- fees [E]
						 | 
						 | 
      		      				 +--- <UID gas #n>  [P, E]
						 			  |
						  			  +--- recharges [E]
						 			  |	 
						 			  +--- fees [E]
						 


GASs
----
A GAS's account hierarchy reflects the role played by the GAS itself in a DES: that of being an interface between people (purchasers) and suppliers (providers of goods and services). As every interface, a GAS is a "double-sided" entity: one side is person-facing, the other is supplier-facing.

The person-facing interface is based on the concept of *GAS membership*: a person can be member of more than one GAS, and this membership defines the details of the person <-> GAS relation.  From an accounting point of view, this relation is managed via three accounts:

- `/members/<member UID>` is a stock-like account representing the credit a person (as a GAS member) has against the GAS (s)he belongs to; this account may be thought as a pre-payed card from which the GAS draws when it need to pay suppliers (or other expenses related to GAS management)  
- `/incomes/recharges` is used to record recharges made by GAS members to their own "virtual pre-payed cards"
- `/incomes/fees` is used to record payment of annual membership fees by the GAS members (if required by the GAS)

The supplier-facing interface is made of two accounts:

- `/cash` is a stock-like account representing the actual money amount available to a GAS for its expenses (think it as a sort of "virtual wallet"); supplier payments draw from the GAS' cash
- `/expenses/suppliers/<supplier UID>` is used to record payments made from the GAS to a given supplier

::

      . ROOT (/)
      |----------- cash [A]
      |
      +----------- members [P,A]+
      |				|
      |				+--- <UID member #1>  [A]
      |		      		| ..
      |		      		+--- <UID member #n>  [A]
      |
      +----------- incomes [P,I]+
      |				|
      |			        +--- recharges [I] 
      |				|     
      |			        +--- fees [I]
      |
      |
      +----------- expenses [P,E]+
				 |
      			         +--- suppliers [P, E] +
				      		       |
      				     	       	       +--- <UID supplier #1>  [E]
						       | ..
      		      				       +--- <UID supplier #n>  [E]

    

Suppliers
---------
From an accounting point of view, a supplier-like subject can be abstracted as:

* an asset-type account (*wallet*), (virtually) containing supplier-owned money originating from the DES's financial circuit (currently, purchases made by GASs, but one may also envision supplier-to-supplier economic exchanges)
* an income-type hierarchy of accounts recording payments made by GASs having subscribed solidal pacts with the supplier itself

::

      . ROOT (/)
      |----------- wallet [A]
      |
      +----------- incomes [P,I]+
				 |
      			         +--- gas [P, I] +
				      	      	 |
      				     	       	 +--- <UID gas #1>  [P, I]
						 | 			  
						 |  			  
						 | ..			  
						 | 			  
						 | 
						 | 
      		      				 +--- <UID gas #n>  [P, I]
						 			  
						  			 


Common transactions
===================

In the following sections, we list the most common types of transactions happening between economic subjects in a DES.

For each kind of transaction, we give a general description plus technical details about how to use the accounting API provided by GasistaFelice to record a concrete transaction of the given type.

For convenience reasons, transaction types are grouped by the subject(s) they involve.

Person <--> GAS
---------------

Membership fees
~~~~~~~~~~~~~~~
*description*
  A GAS may requires its members to pay a membership fee (usually on a per-year basis).

*transaction scheme*

|  ``gas``:= GAS to which the fee is payed
|  ``person``:= person being member of GAS ``gas``

::
  person.accounting.system['/wallet'] -> person.accounting.system['/expenses/gas/<gas.uid>/fees'] -> 
  -> gas.accounting.system['/incomes/fees'] -> gas.accounting.system['/cash']

*usage*
  To record the payment of a membership fee by a GAS member, call ``person.subject.accounting.pay_membership_fee(gas, year)``

  *arguments*

	``gas``
	  the GAS to which this fee is being payed (as a ``GAS`` model instance)
	``year``
	  the year (as a string) to which this fee refers to  

  *return value*	
  	``None``

  *exceptions*
	 if  ``person`` is not a member of GAS ``gas``, a ``MalformedTransaction`` exception is raised

Recharges
~~~~~~~~~
*description*
  GAS members can (actually, should!) recharge their virtual pre-payed credit cards on a regular basis, in order to provide their GAS with financial coverage for orders they made;  we refer to these routine operations simply as *recharges*.

*transaction scheme*

|  ``gas``:=  GAS with respect to which the recharge is being done
|  ``person``:= person being member of GAS ``gas``

::

  person.accounting.system['/wallet'] -> person.accounting.system['/expenses/gas/<gas.uid>/recharges'] -> 
  -> gas.accounting.system['/incomes/recharges'] -> gas.accounting.system['/members/<member.uid>']

*usage*
  To record a recharge made by a person (as a GAS member), call ``person.accounting.do_recharge(gas, amount)``

  *arguments*

	``gas``
	  the GAS to which this recharge is being made (as a ``GAS`` model instance)
	``amount``
	  the recharge's amount

  *return value*	
  	``None``

  *exceptions*
	If ``person`` is not a member of GAS ``gas``, or if ``amount`` is a negative number, a ``MalformedTransaction`` exception is raised.

GAS <--> GAS
------------

Withdrawals from GAS members' accounts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*description*
  Withdraw a given amount of money from a GAS member's account and bestow it to the GAS's cash.  

*transaction scheme*

|  ``gas``:=  GAS making the withdrawal
|  ``member``:= GAS member whose account undergoes the withdrawal

::

  gas.accounting.system['/members/<member.uid>'] -> gas.accounting.system['/cash']

*usage*
  To record a withdrawal made by a GAS from a GAS member's account, call ``gas.accounting.withdraw_from_member_account(self, member, amount, refs=None)``

  *arguments*

	``member``
	   the GAS member whose account undergoes the withdrawal
	``amount``
	   amount of the withdrawal 
	``refs``
	   [optional] any references for this transaction (as an iterable of model instances);
           For example:  a list of GAS member orders this withdrawal is related to

  *return value*	
  	``None``

  *exceptions*
	 If ``member`` is not a member of ``gas``, a ``MalformedTransaction`` exception is raised.	


GAS <--> Supplier
-----------------
Supplier payments
~~~~~~~~~~~~~~~~~
*description*
  A payment made by a GAS to a supplier.  Note this kind of payment is generic, i.e. it may refer to one or more supplier orders, or even part thereof.

*transaction scheme*

| ``gas``:=  GAS making the payment
| ``supplier``:= supplier receiving the payment

::

  gas.accounting.system['/cash'] -> gas.accounting.system['/expenses/suppliers/<supplier.uid>'] -> 
  -> supplier.accounting.system['/incomes/gas/<gas.uid>'] -> supplier.accounting.system['/wallet']

*usage*
  To record a payment made by a GAS to a supplier, call ``gas.accounting.pay_supplier(self, pact, amount, refs=None)``

  *arguments*

	``pact``
	   the solidal pact w.r.t. which this payment is made (i.e. ``pact.gas == gas``, ``pact.supplier == supplier``)	
	``amount``
	   the (positive) payment amount 
	``refs``
	   [optional] any references for this transaction (as an iterable of model instances);
           For example:  a list of supplier orders this payment is related to

  *return value*	
  	``None``

  *exceptions*
	If ``amount`` is negative, a ``MalformedTransaction`` exception is raised (supplier-to-GAS money transfers should be treated as *refunds*).


Order payments
~~~~~~~~~~~~~~
*description*
  A payment made by a GAS to a supplier referring to a specific supplier order.
  Actually, such operation is a two-step process:

    1. First, the GAS withdraws from each member's account an amount of money corresponding
       to the total cost of products (s)he bought during the given order (price & quantity are as recorded by the invoice!)
    2. Then, the GAS collects this money amounts and transfers them to the supplier's account 

*transaction scheme*
  This transaction is just a combination of `Supplier payments`_ and `Withdrawals from GAS members' accounts`_ (see description above for details)

*usage*
  To record an order payment made by a GAS to a supplier, call ``gas.accounting.pay_supplier_order(self, order)``

  *arguments*

	``order``
	   the supplier order being payed (a ``GASSupplierOrder`` model instance)

  *return value*	
  	``None``

  *exceptions*
	If the given supplier order hasn't been fully withdrawn by GAS members yet, raise ``MalformedTransaction``

Refunds
~~~~~~~
*description*
  A refund made by a supplier to a GAS (think e.g. of discounts made by the supplier in case of damaged goods).  

*transaction scheme*

|  ``supplier``:= supplier making the payment
|  ``gas``:=  GAS receiving the payment

::

  supplier.accounting.system['/wallet']   -> supplier.accounting.system['/incomes/gas/<gas.uid>'] ->   
  -> gas.accounting.system['/expenses/suppliers/<supplier.uid>'] -> gas.accounting.system['/cash']

*usage*
  To record a refund made by a supplier to a GAS, call ``supplier.accounting.refund_gas(self, gas, amount, refs=None)``

  *arguments*

	``gas``
	   the GAS being refunded (as a ``GAS model instance``)
	``amount``
	   the (positive) amount of the refund
	``refs`` 
	   [optional] any references for this transaction (as an iterable of model instances);
           For example:  a list of supplier orders this refund is related to

  *return value*	
  	``None``

  *exceptions*
	If GAS ``gas`` doesn't have an active solidal pact with this supplier, or if ``amount`` is negative, raise a ``MalformedTransaction`` exception.

Utility functions
=================
confirm_invoice_payment
-----------------------
*description*
  A supplier should be able to confirm that an invoice issued by him/her has been actually payed.

*usage*
  To confirm the payment of an invoice issued by a supplier, call ``supplier.accounting.confirm_invoice_payment(self, invoice)``
	
  *arguments*

	``invoice``
	   the invoice to be confirmed (as an ``Invoice`` model instance)

  *return value*	
  	``None``

  *exceptions*
	If ``invoice`` isn't an ``Invoice`` model instance, or if it was issued by another subject, raise ``ValueError``.

        

accounted_amount_by_gas_member
------------------------------
*description*
  Given a supplier order ``order``, return an annotated set of GAS members  partecipating to that order.
        
  Each GAS member instance will have an ``.accounted_amount`` attribute, representing the total amount of money already accounted for with respect 
  to the entire set of orders placed by that GAS member within ``order``.
        
   A (member) order is considered to be "accounted" iff a transaction recording it
   exists within that GAS's accounting system.
        

*usage*
  If ``gas`` is the GAS who issued the supplier order, call ``gas.accounting.accounted_amount_by_gas_member(self, order)``

  *arguments*

	``order``
	    the order to be accounted for (as a ``GASSupplierOrder`` model instance)

  *return value*	
  	``None``

  *exceptions*
	If ``order`` has not been placed by the GAS owning this accounting system,  raise ``TypeError``.   



----

.. _django-simple-accounting: https://github.com/seldon/django-simple-accounting

.. [1] By setting the variable ``ACCOUNT_PATH_SEPARATOR`` in ``settings.py`` (default: `/`)
