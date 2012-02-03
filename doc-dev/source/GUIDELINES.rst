
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
* I ticket sono in italiano, le risposte date tramite i commit in inglese. Opzionalmente si può aggiungere di seguito alla versione inglese anche quella in italiano

Import
------

* Prima si importano i moduli inclusi nella distribuzione ufficiale di Django
* Poi i moduli di applicazioni Django non incluse nel progetto
* Infine i moduli delle applicazioni incluse nel progetto
* Poi le librerie di sistema
* Settings. Non usare 'import settings' ma 'from django.conf import settings'. Cosi l'importazione non adviene dal file ma da un oggetto lazy che puo essere cambiato a runtime.

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
* i nomi campi BooleanField o NullBooleanField devo iniziare con un verbo. Ad esempio: "is_active", "use_scheduler", "can_change_price", ...
* i nomi campi prediposti per memorizzare valori di default da usare in altri contesti, devono iniziare con "default_"
* usare funzione save() per codice che non rappresenta un estensione al modello. Usare signal (handler) per codice che rappresenta un estensione.


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

    related_name="pact_set"
    related_name="gasmember_set"
    related_name="gasmember_available_set"

    @property
    def pacts(self):
        return self.pact_set.all()

    @property
    def pact(self):
        return self.gas.pacts.get(supplier=self.supplier)

Struttura classi del modello
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In linea generale:

* Prima ci sono i campi
* Poi i manager
* Poi la classe Meta
* Poi le property
* Poi i metodi

Metodi clean, save, setup_data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nella `clean` ci vanno tutte le operazioni di validazione e sanitizzazione. La clean viene chiamata prima del salvataggio del modello (segnale `pre_save`)

Nella `save` ci vanno tutte le altre operazioni di gestione che non vanno nella `clean`

La `setup_data` è da considerarsi un "palliativo" per l'import delle fixture. Per ora duplichiamo il codice della `save` se necessario. C'è da dire che questo metodo viene chiamato dopo il salvataggio (segnale `post_save`), potremmo usarlo in modo ufficiale posto che ne cambiamo il nome perché il rischio di usare estensivamente i segnali è quello di "perdersi". Se lo chiamassimo `post_save` potremmo in pratica eliminare la `save`.


Convenzioni
^^^^^^^^^^^

* Le cose da fare sono marcate come `TODO`
* I commenti "che si vogliono indirizzare agli altri sviluppatori" iniziano con `#COMMENT <nick>`
* Le parti di codice pushate ma che hanno bisogno di revisione includono la stringa `TODO: NEEDS REVIEW`
* Il codice segue le linee guida del PEP-08
* L'indentazione delle righe spezzate è sempre di 4 spazi
* Le parti di codice che si commentano e si vogliono lasciare come promemoria si commentano con `#WAS`, se è una prova che non era andata a buon fine mettere `KO:`

ATTENZIONE A
-------------

1. **(NON) utilizzo della funzione `print`**
    * Non usare la funzione `print` senza le parentesi
    * Non usare la funzione `print` se non a scopo temporaneo di debug
    * Se si intende pushare codice con `print`, sostituirlo con `log.debug`

2. **Stringhe e internazionalizzazione (i18n)**
    * TUTTE le stringhe devono essere **UNICODE**. Il che vuol dire che qualunque
      stringa scriviamo deve essere preceduta da una **`u`** (ad es: `u"ciao mamma"`) 
    * Usare `ugettext` quando il valore della stringa viene recuperato a runtime,
      usare `ugettext_lazy` quando il valore della stringa viene recuperato ad import time
    * NON È POSSIBILE LOCALIZZARE STRINGHE CHE HANNO PIù DI UN %s al loro interno:
      usare sostituzione delle variabili per nome nei template (ad es: `_("ciao %(name)s")` )
3. **Impostazioni del proprio ambiente in settings.py**
    * Tutte le impostazioni relative alla propria installazione vanno in settings.py
      Ad esempio se non si ha un server email per le notifiche impostare `NOTIFICATION_BACKENDS = ()`




