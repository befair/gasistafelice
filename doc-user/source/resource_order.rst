.. _resource-order:

L'ordine
========

|head2_descr|
-------------

Un ordine che il:ref:`|res_gas| <resource-gas>`  invia ad un :ref:`fornitore <role-supplier>`: è formato dall'insieme dei prodotti ordinati dai singoli gasisti che hanno preso parte all'ordine, scegliendo tra i prodotti disponibili nel listino del |res_supplier| per quel particolare ordine.
Un ordine è inoltre caratterizzato da:

* il fornitore;
* la data di apertura e quella di chiusura;
* un appuntamento di consegna, cioè le modalità con cui il fornitore consegna al |res_gas| la merce ordinata;
* un appuntamento di ritiro, cioè le modalità di distribuzione della merce ordinata ai Gasisti;
* un eventuale importo minimo, sotto il quale il |res_supplier| non accetta l'ordine. 


|head2_terms|
-------------

* Report gasista
* Report dell'ordine
* Ritiro
* Consegna

|head2_options|
---------------

|TODO| elencare le opzioni di configurazione del |res_gas| che influiscono sull'ordine

Il software offre un'elevata possibilità di configurazione del |res_gas|; molte delle opzioni che possono essere configurate, inoltre, vanno ad influire sull'ordine che il |res_gas| esegue sul |res_pds|.
Di seguito sono elencate le opzioni riguardanti l'ordine che possono essere configurate nel |res_gas|:

* visualizzazine solo della prossima consegna: rende possibile il filtraggio degli ordini in modo che i gasisti visualizzino solo quelli che condividono il prossimo appuntamento di ritiro;
* selezione di un ordine alla volta: limita la selezione a un solo un ordine aperto alla volta;
* conferma automatica degli ordini dei gasisti: se selezionato, gli ordini dei gasisti vengono automaticamente confermati, altrimenti ogni gasista deve confermare manualmente i propri ordini;
* giorno, ora e minuto predefinito di chiusura degli ordini;
* giorno, ora e minuto predefinito della settimana di consegna degli ordini;
* possibilità di cambiare il luogo di consegna ad ogni ordine: se selezionata, rende possibile specificare il luogo della consegna ad ogni ordine. Se non selezioanta, il |res_gas| usa solo il luogo predefinito di consegna nel caso questo sia definito, altrimenti la sede del GAS.
* luogo di consegna predefinito: va specificato se diverso dal luogo di ritiro;
* possibilità di cambiare il luogo di ritiro ad ogni ordine:  se selezionata, è possibile specificare il luogo di ritiro ad ogni ordine. Se non selezionata, il |res_gas| usa solo il luogo predefinito di ritiro nel caso questo sia deinito, altrimenti la sede del GAS.
* luogo di ritiro predefinito: va specificato se è diverso dalla sede;
* giorni di preavviso prima della chiusura dell'ordine: quanti giorni prima si vuole ricevere un promemoria degli ordini di chiusura del |res_gas|.

Nell'immagine seguente è possibile ossrvare come tutte le opzioni sopra elencate siano effettivamente configurabili:


.. figure:: _static/.png
    :alt: Schermata di configurazione del GAS
    :align: center

    La: l'utente inserisce nome utente e password.


|head2_relations|
-----------------

|TODO| Relazioni con gli altri soggetti del sistema

* Patto
* Ordini dei gasisti
* Referenti


