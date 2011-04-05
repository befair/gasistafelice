
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
* Le variabili e gli attributi (non i :ref:`ManyToManyField`) che identificano più di un elemento sono pluralizzati 
* Per recuperare un valore:
 * in caso di computazione minima, usare una property
 * in caso di computazione più complessa, usare un metodo 

Django
------

Il file models.py
^^^^^^^^^^^^^^^^^

* Le classi del models.py vengono scritte nel modo più intuitivo possibile. Ad esempio: se la persona ha vari contatti, si scrive prima la classe Person e il riferimento alla classe Contact nel campo ManyToManyField dei contatti viene messa tra apici
* Cercare di massimizzare i campi ``blank=True``. Lo specifico perché è importante non ragionare su `cosa l'utente dovrebbe scrivere di un determinato oggetto, ma qual è il minimo sforzo con cui può farlo`. Ad esempio: ha senso inserire il nome della categoria di prodotto e non la descrizione? Secondo me sì. Per appuntare un "reminder" sulla nuova categoria ad esempio. Poi il software si occuperà di mostrare un messaggio "non hai inserito la descrizione della categoria del prodotto" all'utente amministratore del programma.

.. _ManyToManyField:

Nomi dei campi ManyToManyField
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

I campi ManyToManyField si comportano come manager. Di esse viene impostato automaticamente un `related_name` con il nome del modello seguito da _set.
Per uniformità di utilizzo si conviene che:

* i nomi dei campi ManyToManyField 
* i relativi related_name che devono essere ridefiniti a causa di conflitti nel naming automatico

finiscano con _set e per avere invece l'accesso diretto agli attributi si definiscano :func:`property` con i nomi plurali dei campi. 

Esempio:

.. sourcecode:: python

    related_name="solidal_pact_set"
    related_name="gas_members_set"
    related_name="gas_members_available_set"

    @property
    def solidal_pacts(self):
        return self.solidal_pact_set.all()

    @property
    def solidal_pact(self):
        return self.gas.solidal_pacts.get(supplier=self.supplier)

Struttura classi del modello
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Prima ci sono i campi
* Poi i manager
* Poi la classe Meta
* Poi le property
* Poi i metodi



