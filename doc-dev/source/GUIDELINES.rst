
Qualche linea guida sulla scrittura del codice
==============================================

* Il codice viene indentato con 4 spazi. In `vim` impostare le opzioni

.. sourcecode:: vim

    set expandtab
    set tabstop=4
    set shiftwidth=4

* Il codice è in inglese
* I commenti possono essere in italiano
* La documentazione utente è in italiano
* La documentazione tecnica è in inglese (notare come queste linee guida non la rispettino. Adeguarle pls :))
* Stile `duck typing <http://en.wikipedia.org/wiki/Duck_typing>`__ riassunto da `Alex Martelli <http://en.wikipedia.org/wiki/Alex_Martelli>`__: `In other words, don't check whether it IS-a duck: check whether it QUACKS-like-a duck, WALKS-like-a duck, etc, etc, depending on exactly what subset of duck-like behaviour you need to play your language-games with.`

Naming
------

* I nomi delle classi sono CamelCase
* Le sigle sono tutte maiuscole e rimangono in italiano (GAS, DES)
* I nomi composti che non sono classi sono separati da "_"
* Le variabili che fanno riferimento a liste di oggetti sono singolari e finiscono per "_list" 
* Per recuperare un valore:
 * in caso di computazione minima, usare una property
 * in caso di computazione più complessa, usare un metodo 

Struttura classi del modello
----------------------------

* Prima ci sono i campi
* Poi i manager
* Poi la classe Meta
* Poi le property
* Poi i metodi



