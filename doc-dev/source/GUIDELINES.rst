
Qualche linea guida sulla scrittura del codice
==============================================

Il codice viene indentato con 4 spazi. In `vim` impostare le opzioni

.. sourcecode:: vim

    set expandtab
    set tabstop=4
    set shiftwidth=4

* Il codice è in inglese
* I commenti possono essere in italiano
* La documentazione utente è in italiano

Naming
------

* I nomi delle classi sono CamelCase
* Le sigle sono tutte maiuscole e rimangono in italiano (GAS, DES)
* I nomi composti che non sono classi sono separati da "_"
* Le variabili che fanno riferimento a liste di oggetti sono singolari e finiscono per "_list" (...o "_set"?)
* Usare una property quando si effettua una computazione minima per recuperare un valore, usare un metodo anche se si tratta di un semplice getter quando invece è più complessa.
