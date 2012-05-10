.. _role-gasmember:

Il gasista
==========

|head2_descr|
-------------

Il |res_gasmember| è una persona che appartiene ad un :ref:`GAS <resource-gas>`. 
Lo scopo del |res_gasmember| è ordinare prodotti, resi disponibili in un :ref:`ordine <resource-order>` aperto da un :ref:`referente fornitore <role-gasreferrersupplier>`. 
|project_short_name| consente ad una persona di appartenere a più |res_gas| contemporaneamente.

|head2_actions|
---------------

* Ordina 
* |sym_gas_conf| vede gli ordini per fornitore o per consegna
* |sym_gas_conf| riceve email di conferma
* Gestisce il paniere
* Visualizza la consegna
* Modifica la scheda gasista


|head2_terms|
-------------

Breve definizione dei termini:

* Ordine: l'ordine che il referente fornitore apre, chiude ed invia al Fornitore con i prodotti ordinati dai gasisti
* Consegna
* Paniere: l'insieme dei prodotti ordinati per gli ordini aperti
* Paniere da consegnare: l'insieme dei prodotti ordinati negli ordini attualmente chiusi e da consegnare
* Fornitore: soggetto che fornisce un GAS
* Prezzo ordinato: prezzo di un prodotto al momento dell'ordine
* Prezzo consegnato: prezzo di un prodotto al momento della consegna

|head2_start|
-------------

Il gasista non deve pensare a curare i seguenti aspetti che sono di competenza di altri ruoli:

* :ref:`GAS <resource-gas>` già inserito
* :ref:`Fornitori <resource-supplier>` già inseriti
* :ref:`Patto di solidarietà <resource-pact>` già costituito
* :ref:`Ordine <resource-order>` già aperto

