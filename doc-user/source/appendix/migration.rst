
Migrazione dei GAS su Gasista Felice
====================================

In questo documento si definisce una procedura di migrazione dei GAS
alla piattaforma Gasista Felice. L'obiettivo è ovviamente quello di 
semplificare l'integrazione di ogni GAS e di poter effettuare i test 
di utilizzo nell'ambiente di produzione minimizzando gli sforzi di chi
effettua e di chi supervisiona il test.

La procedura proposta prevede l'interazione fra l'area comunicazione,
il gruppo di sviluppo, un tutor, il referente informatico del GAS, e tutti i gasisti.
Essa è composta dai seguenti passi:

1. Richiesta al referente informatico dei GAS i dati da importare
2. Importazione dei dati da parte del gruppo di sviluppo
3. Abilitazione del referente informatico del GAS
4. Il referente informatico del GAS abilita gli utenti:

 * aggiunge i gasisti
 * assegna gli altri ruoli (referente informatico, referente fornitore, fornitore)

La demo che viene fatta sul posto dovrebbe avvenire fra la fase 3 e la fase 4, o in ogni caso,
dopo che il gruppo sviluppo abbia creato l'utente ed assegnato il ruolo di *referente informatico del GAS*

Dati da importare
-----------------

.. note::
    L'importazione dei dati si spinge fin dove il referente informatico di ogni GAS intende portarla,
    sulla base delle proprie esigenze, disponibilità di tempo e dei dati del proprio GAS!
    I dati richiesti si dividono in obbligatori e opzionali. L'invito è di mettere TUTTI i dati a
    disposizione. Questo semplificherà l'interazione con il software ed eviterà integrazioni future.

I documenti da cui si importano i dati sono fogli di calcolo elaborati con il proprio programma
di foglio di calcolo preferito ed inviati via mail al team operativo del DES.
Si prega di creare file con un solo foglio. Il primo.

Il formato dei documenti di importazione deve essere uno a scelta fra:

1. ``ods`` 
2. ``xls`` 

.. note:
    TUTTE le colonne obbligatorie devono essere presenti nel file consegnato anche se vuote.

Vengono messi a disposizione dei file di esempio per facilitare la compilazione

.. note
    TODO Li sta preparando Peppe di Civitanova che ringraziamo


**Programmi per la realizzazione**

In un contesto di economia solidale si privilegiano i programmi liberi di cui citiamo i più diffusi:

* `LibreOffice <http://www.libreoffice.org>`__ (su tutti sistemi operativi)
* `GNUmeric <http://it.wikipedia.org/wiki/Gnumeric>`__ (per sistemi GNU/Linux)

Per ulteriori approfondimenti rimandiamo alla pagina di Wikipedia `Software di produttività personale <http://it.wikipedia.org/wiki/Software_di_produttivit%C3%A0_personale>`__

.. _import-GAS:

GAS
^^^

Le informazioni da comunicare relative al "soggetto" GAS sono poche e non è necessario comunicarle tramite un foglio di calcolo,
basta inserirle nella mail in cui si comunicano gli altri dati. Esse sono:

* nome del GAS
* città
* recapito email per comunicazioni del gestionale (v. sotto) del GAS
* recapito email informativo del GAS
* recapito telefonico informativo del GAS

e opzionalmente:

* logo (se ce lo avete. Come immagine allegata o come indirizzo http va bene uguale)
* i nomi delle persone cui si possono chiedere informazioni sul GAS
* quanto è la quota di iscrizione annuale
* entro quanto richiedete che la quota venga pagata: questo ci servirà per poter mandare un reminder a tutti i gasisti, ma non ci sarà nella prima implementazione

Il recapito email per comunicazioni del gestionale verso il GAS è importante 
per poter inviare alcune (le minime) comunicazioni del gestionale, che potete leggere al capitolo :ref:`notifications`




.. _import-gasmembers:

Gasisti
^^^^^^^

**Campi obbligatori**

1. Nome
2. Cognome
3. Indirizzo email
4. Città 

**Campi opzionali**

5. Nome del file con l'immagine che sarà inviata insieme al foglio di calcolo compilato
6. Indirizzo
7. Nome da visualizzare (a piacere)
8. Numero di telefono
9. Numero di tessera nel GAS

.. note::
    Il nome utente (username) verrà impostato al nome della persona, seguito da un numero progressivo per evitare duplicati.

.. _import-company:

Fornitori - il soggetto giuridico
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Campi obbligatori**

1. (IDFORNITORE) Identificativo univoco: è un valore a piacere che serve per identificare il fornitore in altri fogli di calcolo
2. Ragione sociale
3. Tipo: valori ammissibili sono azienda/cooperativa/professionista/
4. Città
5. Recapito telefonico
6. Recapito email: mettere nonholindirizzo chiocciola desmacerata.it nel caso il fornitore non abbia il recapito

**Campi opzionali**

7. Indirizzo civico
8. Certificazioni: elenco separato da ``,`` (virgola) dei valori elencati fra parentesi in :ref:`list-certifications`
9. Sito web
10. Codice IBAN
11. Numero di persone
12. Numero di partita IVA
13. Codice fiscale
14. Nome del file con l'immagine che sarà inviata insieme al foglio di calcolo compilato
15. Descrizione

Fornitori - le persone associate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:
    Per ogni fornitore è fondamentale associare una persona di tipo RAPPRESENTANTE

Esistono 3 tipi di soggetti che ruotano intorno al fornitore: 

* il rappresentante della piattaforma;
* la persona che funge da contatto informativo;
* chi opera nella piattaforma;

I campi obbligatori per l'importazione di questi tipi di soggetti sono:

1. IDFORNITORE: v. :ref:`import-company`. Ha il compito di legare questa riga al soggetto giuridico interessato
2. Tipo: a scelta fra:

 * ``RAPPRESENTANTE``: il rappresentante. È importante che ci sia uno e un solo rappresentante per ogni fornitore;
 * ``INFO``: una persona per il contatto;
 * ``OPERATORE``: un operatore nella piattaforma;
 * ``OP_INFO``: operatore e persona di contatto;
 * ``OP_RAPP``: operatore e rappresentante;

e a seguire gli altri campi previsti per i :ref:`import-gasmembers`

.. note::
    Le persone di tipo "RAPPRESENTANTE" e "INFO" non avranno un utente abilitato all'accesso al sistema

.. note::
    Si consiglia di mettere in questa scheda solamente le persone che non sono già gasisti.
    Il referente informatico potrà gestire al meglio l'associazione dei propri gasisti ai propri fornitori.

Prodotti
^^^^^^^^

Per ora parliamo solamente dei produttori, ossia chi vende prodotti realizzati in proprio.

I prodotti prevedono vari campi obbligatori:

1. IDFORNITORE: v. :ref:`import-company`. Ha il compito di legare questa riga al soggetto giuridico interessato
2. Nome
3. Prezzo ivato
4. IVA: aliquota espressa in intero senza simbolo % (21, 10 o 4 in sostanza)
5. Unità di prodotto: a scelta fra :ref:`list-product-units`

Campi opzionali:

6. Unità di misura: a scelta fra :ref:`list-measure-units`
7. Unità di misura per unità di prodotto
8. Categoria di prodotto: a scelta fra :ref:`list-product-categories`
9. Codice identificativo
10. Quantità minima ordinabile: espressa in termini di unità di prodotto
11. Quantità di unità di prodotto per cartone
12. Quantità minima del dettaglio
13. Quantità minima di avanzamento

**Esempi** 

Il caso più semplice è *1 KG di prosciutto crudo*:

* Nome = prosciutto crudo
* Unità di prodotto = KG

Un caso più interessante è *1 CF da 500 GR di pasta di semola di grano duro*:

* Nome = pasta di semola di grano duro
* Unità di prodotto = CF (Confezione)
* Unità di misura = GR
* Unità di misura per prodotto = 500

Infine poniamo il caso del prodotto *1 forma da 10 KG di formaggio pecorino tagliabile a fette di 20gr*. I campi assumono i valori:

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



