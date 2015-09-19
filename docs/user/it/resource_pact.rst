.. _resource-pact:

Il patto di solidarietà
=======================

Descrizione
-------------

Il Patto di Solidarietà è l'insieme delle condizioni di fornitura, economiche e non, condivise e sottoscritte da un :ref:`GAS <resource-gas>` e un :ref:`fornitore <role-supplier>`. È composto da diversi punti, di cui i principali sono :

* il catalogo del fornitore per il GAS, cioè i prodotti che il GAS sceglie di includere nei suoi :ref:`ordini <resource-order>` verso il fornitore, scelti tra quelli resi disponibili dal fornitore stesso; 
* i gasisti che fungono da :ref:`referenti fornitore <role-gasreferrersupplier>` per il fornitore;
* quanti giorni prima della consegna è necessario chiudere l'ordine;
* le spese di consegna per ogni ordine.

per una descrizione dettagliata di come è possibile configurare il patto di solidarietà, andare alla sezione di :ref:`modifica del patto <pact-options>`.

Il patto di solidarietà è una risorsa fondamentale nel DES, poichè è il tramite attraverso il quale i gasisti sono in grado di ordinare prodotti. Infatti, benchè sia un fornitore a consegnarli fisicamente, in realtà è il patto di solidarietà stesso a fungere da contesto per l'ordine tra il GAS e un particolare fornitore tra quelli attivi nel DES.

Nella pratica, il percorso intrapreso dal prodotto comprende tre passi:

* il fornitore si affaccia sul DES: in questo momento non viene ancora considerato attivo, poichè non è associato a nessun patto di solidarietà;
* il fornitore viene associato as un patto di solidarietà con un GAS, e da questo momento in poi viene considerato attivo nel DES (può comunque essere collegato a piu di un patto di solidarietà, ognuno con un GAS diverso);
* il GAS apre un ordine sul patto di solidarietà scegliendo tra i prodotti disponibili nel listino del fornitore quelli ordinabili dai gasisti.

Nella figura sottostante, per chiarezza, mostriamo il percorso intrapreso dal prodotto nel DES, dal fornitore al GAS:



.. figure:: _static/des_pact.png
    :alt: I tre livelli del percorso del prodotto nel DES 
    :align: center
    
    Percorso del prodotto dal fornitore al gasista



Terminologia
-------------

* Listino fornitore
* Listino fornitore per il GAS
* Ordine

.. _pact-options:

Opzioni di configurazione
---------------

Il software offre l'opportunità di configurare ogni aspetto del patto di solidarietà, in particolare:

* la data dell'accordo, ovvero anno, mese e giorno in cui il patto di solidarietà è stato stipulato;
* un copia elettronica del Documento, un patto bilaterale firmato dal GAS e dal fornitore interessato che contiene gli accordi solidali che entrambe le parti si impegnano di rispettare, ad esempio la trasparenza sui processi produttivi del fornitore e l'adempimento degli impegni economici, da parte dei gasisti, in seguito alla fornitura.
* le spese di consegna che è necessario affrontare alla consegna di un ordine del fornitore;
* il tempo da attendere prima della consegna,ovvero l'itervallo minimo che intercorre tra la chiusura dell'ordine da parte del GAS e l'effettiva consegna dei prodotti da parte del fornitore;
* una lista dei membri del GAS a cui il fornitore è collegato attraverso il patto di solidarietà, tra cui è possibile scegliere uno o più referenti fornitori per il patto stesso.
* l'eventuale importo minimo al di sotto del quale le parti concordano che non è possibile far partire un ordine.


.. figure:: _static/pact_config.png
    :alt: Configurazione del patto di solidarietà
    :align: center
    
    Schermata per la configurazione del patto di solidarietà



Relazioni con le altre risorse del DES
-----------------

* :ref:`GAS <resource-gas>` 
* :ref:`Fornitore <role-supplier>`
* :ref:`Ordine <resource-order>` 
* :ref:`Gasista <role-gasmember>`
* :ref:`Referente fornitore <role-gasreferrersupplier>` 
