
Migrazione dei GAS su Gasista Felice
====================================

È opportuno condividere una procedura condivisa di migrazione dei GAS
alla piattaforma Gasista Felice. L'obiettivo è ovviamente quello di 
semplificare la migrazione di ogni GAS e di poter effettuare i test 
di utilizzo nell'ambiente di produzione minimizzando gli sforzi di chi
testa e di chi supervisiona il test.

La procedura proposta prevede l'interazione fra l'area comunicazione,
il gruppo di sviluppo, un formatore, il referente informatico del GAS, e tutti i gasisti.
Essa è composta dai seguenti passi:

1. Richiesta al referente informatico dei GAS dei dati da importare
2. Importazione dei dati da parte del gruppo di sviluppo
3. Abilitazione del referente informatico del GAS
4. Il referente informatico del GAS abilita gli utenti:
 * aggiunge i gasisti
 * assegna gli altri ruoli (referente informatico, referente fornitore, fornitore)

La demo che viene fatta sul posto dovrebbe avvenire fra la fase 3 e la fase 4, o in ogni caso,
dopo che il gruppo sviluppo abbia creato l'utente ed assegnato il ruolo di *referente informatico del GAS*

Dati da importare
-----------------

L'importazione dei dati si spinge fin dove il referente informatico di ogni GAS intende portarla,
sulla base delle proprie esigenze, disponibilità di tempo e dei dati del proprio GAS!
I dati possono essere importati anche in fasi separate.

I documenti da cui si importano i dati sono fogli di calcolo elaborati con il proprio programma
di foglio di calcolo preferito ed inviati via mail al team operativo del DES.

Il formato dei documenti di importazione deve essere uno a scelta fra:

1. ``ods`` 
2. ``xls`` 

.. note:
    TUTTE le colonne obbligatorie devono essere presenti nel file consegnato anche se vuote.

**Programmi per la realizzazione**

In un contesto di economia solidale si privilegiano i programmi liberi di cui citiamo i più diffusi:

* `LibreOffice <http://www.libreoffice.org>`__ (su tutti sistemi operativi)
* `GNUmeric <http://it.wikipedia.org/wiki/Gnumeric>`__ (per sistemi GNU/Linux)

Per ulteriori approfondimenti rimandiamo alla pagina http://it.wikipedia.org/wiki/Software_di_produttivit%C3%A0_personale

.. _gasmembers:

Gasisti
^^^^^^^

Campi obbligatori:

1. Nome
2. Cognome
3. Indirizzo email
4. Città 

Ulteriori campi opzionali:

5. Indirizzo
6. Nome da visualizzare (a piacere)
7. Numero di telefono

.. note::
    Il nome utente verrà impostato al nome della persona, seguito da un numero progressivo per evitare duplicati.

Fornitori
^^^^^^^^^

Soggetto giuridico
&&&&&&&&&&&&&&&&&&

Campi obbligatori:

1. Nome
2. Numero di partita IVA
3. Tipo: valori ammissibili sono azienda/cooperativa
4. Numero di persone
5. Indirizzo
6. Città
7. Recapito telefonico

Campo opzionale:

8. Recapito email
9. Certificazioni: elenco separato da ``,`` (virgola) dei valori elencati fra parentesi in :ref:`list-certifications`

Soggetto 
&&&&&&&&

Esistono 2 tipi di soggetti che ruotano intorno al fornitore: chi opera nella piattaforma,
e la persona che funge da contatto informativo.

I campi obbligatori per l'importazione di questi tipi di soggetti sono:

1. Tipo: a scelta fra ``OPERATORE`` (operatore), ``INFO`` (persona per il contatto), ``OP_INFO`` (entrambi)

e a seguire gli altri campi previsti per i :ref:`gasmembers`

Prodotti
^^^^^^^^

Per ora parliamo solamente dei produttori, ossia chi vende prodotti realizzati in proprio.

I prodotti prevedono vari campi obbligatori:

1. Nome
2. Prezzo ivato
3. IVA
4. Unità di prodotto: a scelta fra :ref:`list-product-units`

Campi opzionali:

5. Unità di misura: a scelta fra :ref:`list-measure-units`
6. Unità di misura per unità di prodotto
7. Categoria di prodotto: a scelta fra :ref:`list-product-categories`
8. Codice identificativo
9. Quantità minima ordinabile: espressa in termini di unità di prodotto
10. Quantità di unità di prodotto per cartone
11. Quantità minima del dettaglio
12. Quantità minima di avanzamento

**Esempio** 

Poniamo il caso del prodotto *1 forma da 10 KG di formaggio pecorino tagliabile a fette di 20gr*. I campi assumono i valori:

* Nome = formaggio pecorino
* Unità di prodotto = forma
* Unità di misura = KG
* Unità di misura per prodotto = 10
* Quantità minima del dettaglio = 20gr/10KG = 20/10000 = 0,002
* Quantità minima di avanzamento = 20gr/10KG = 20/10000 = 0,002

La quantità minima ordinabile entra in gioco se nel caso sia necessario ordinare almeno 2 forme di formaggio. 

In questo caso:

* Quantità minima ordinabile = 2


Importazione (per tecnici)
--------------------------

Aprire il file ed esportarlo in formato ``csv`` in cui i valori dei campi sono delimitati da ``"`` (doppio apice) e i campi sono separati da ``;`` (punto e virgola).

Eseguire il comando ``python manage.py import`` come l'opzione ``--subject=`` a scelta tra "person", "supplier", "person_supplier", "product".



