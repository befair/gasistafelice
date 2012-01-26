Doppia partita
==============

Il sistema economico del GAS.

|head2_descr|
-------------

La gestione della contabilità di un GAS (e dei relativi pagamenti) può coinvolgere, a seconda dell'organizzazione interna del GAS, più ruoli: Referente, Turnista, Contabile.  Ognuno di questi ruoli svolge compiti diversi in fasi diverse dei processi che avvengono nel GAS: anche per questo aspetto, i dettagli possono variare da GAS a GAS.

La gestione contabile di un GAS (come quella di ogni altra organizzazione) può essere modellizzata mediante un sistema di contabilità a partita doppia (*double-entry accounting*).  

Partita doppia
++++++++++++++


In sostanza, il sistema contabile da modellizzare (in questo caso, un GAS) viene descritto definendo un insieme di Conti (*Accounts*), ognuno dei quali rappresenta o uno stock (deposito) di denaro *nel* sistema - positivo o negativo (debiti) - oppure un punto di ingresso o di uscita di denaro *dal* sistema.  

Un flusso di denaro che interessa il sistema viene definito Transazione (*Transaction*), e può causare due effetti distinti:  il trasferimento di una somma di denaro da un stock all'altro del sistema oppure un flusso di denaro - in entrata o in un uscita - tra il sistema e l'esterno.  Nel primo caso il bilancio economico globale del sistema rimane invariato, nel secondo si verifica una variazione della quantità di denaro contenuta nel sistema.  Per definizione, una Transazione coinvolge *almeno* due Conti, *almeno* uno dei quali è interno al sistema in considerazione; sono possibili Transazioni che coinvolgono tre o più Conti (*split transactions*), ma si tratta di uno scenario più avanzato e che possiamo trascurare in prima battuta. 

Quindi, nella maggior parte dei casi, una Transazione rappresenta un flusso di denaro da un Conto (sorgente) ad un altro (Destinazione); di conseguenza, ad ogni Conto risulta automaticamente associato un insieme di Transazioni: quelle che hanno il Conto in questione come sorgente.  Inoltre, ad ogni Transazione dal Conto A al Conto B corrisponde una Transazione (uguale e opposta in segno) dal Conto B al Conto A: questa proprietà della contabilità a partita doppia fornisce un forte controllo di integrità e consistenza dei movimenti finanziari tracciati.

In generale, un Conto può avere uno o più sotto-Conti (*Sub-accounts*): questo consente di aggregare/scorporare le Transazioni in base alle specifiche necessità contabili: questo comporta che i Conti di un sistema hanno naturalmente una struttura gerarchica, ad albero, e sono contenuti in un conto "radice" (*root account*), che rappresenta il sistema nel suo complesso.  È possibile che un Conto serva solo ad aggreggare altri Conti - senza contenere direttamente alcuna Transazione al suo interno: questi sono Conti "segnaposto" ('placeholders').

transazione
+++++++++++


Un conto può essere di diversi tipi, a seconda della tipologia di Transazioni che contiene; i tipi di base sono i seguenti:

* Attività (*Assets*): rappresenta uno stock di denaro all'interno del sistema: liquidità, un conto corrente o altri beni di valore quantificabile, come titoli finanziari e cespiti vari;

* Passività (*Liabilities*): rappresenta uno stock di denaro *negativo* - a livello concettuale - come ad esempio una carta di credito o delle fatture non pagate;

* Entrate (*Income*): è un punto di entrata di denaro nel sistema, solitamente collegato ad una determinata attività (stipendio, pensione, interessi finanziari, ..)

* Uscite (*Expenses*): è un punto di uscita di denaro nel sistema, solitamente collegato ad una determinata attività.


Gestione economica del GAS
++++++++++++++++++++++++++

Come si applica questo modello concettuale ad un GAS ?  A grandi linee, in un GAS ci sono tre categorie primarie di Conti:

* conto del gasista: ogni gasista nel GAS ha un conto che rappresenta il credito/debito che ha maturato nei confronti del suo GAS;
* conto del GAS: è quella che viene spesso chiamata "cassa del GAS"; rappresenta la disponibilità finanziaria corrente del GAS (al netto dei Contigasista);
* Conto produttore: ogni Fornitore di un GAS ha un conto che rappresenta il credito/debito che ha maturato nei confronti del GAS che fornisce; generalmente, serve per tracciare le fatture emesse e quelle effettivamente pagate dal GAS.

In aggiunta a questi, un GAS necessità di altri Conti "secondari", ad esempio per registrare il pagamento delle quote associative, le spese per la gestione della sede, i pagamenti ai fornitori, ecc.


Struttura
---------

La gerarchia degli account relativi ad un GAS potrebbe essere di questo tipo:

.. note::

   GAS  +
        |----------- cash [A]
        +----------- members [P,A]+
        |                +--- <UID member #1>  [A]
        |                | ..
        |                +--- <UID member #n>  [A]
        +----------- expenses [P,E]+
        |                +--- TODO: OutOfNetwork
        |                +--- suppliers [P, E] +
        |                        +--- <UID supplier #1>  [E]
        |                        | ..
        |                        +--- <UID supplier #n>  [E]
        +----------- incomes [P,I]+
        |                +--- recharges [I] 
        |                +--- fees [I]
        |                +--- TODO: Other

 Member +
        **GAS-side**
        . ROOT (/)
        +----------- members [P,A]+
        |                +--- <UID member #1>  [A]
        |                | ..
        |                +--- <UID member #n>  [A]

        **Person-side**
        . ROOT (/)
        |--- wallet [A]
        +--- expenses [P,E]+
                +--- gas [P, E] +
                        +--- <UID gas #1>  [P, E]+
                        |            +--- recharges [E]
                        |            +--- fees [E]
                        | ..
                        +--- <UID gas #n>  [P, E]
                                    +--- recharges [E]
                                    +--- fees [E]

   PACT +
        **GAS-side**
        . ROOT (/)
        +----------- expenses [P,E]+
        |               +--- suppliers [P, E] +
        |                       +--- <UID supplier #1>  [E]
        |                       | ..
        |                       +--- <UID supplier #n>  [E]

        **SUPPLIER-side**
        . ROOT (/)
        +----------- incomes [P,I]+
                        +--- gas [P, I] +
                                +--- <UID gas #1>  [P, I]
                                | ..
                                +--- <UID gas #n>  [P, I]

   Prod +
        |----------- wallet [A]
        +----------- incomes [P,I]+
        |                +--- gas [P, I] +
        |                        +--- <UID gas #1>  [P, I]
        |                        | ..
        |                        +--- <UID gas #n>  [P, I]
        |                +--- TODO: Other (Bonus? Subvention? Investment?)
        +----------- expenses [P,E]+
                        +--- TODO: Other (Correction?, Donation?, )

Legenda
^^^^^^^

* A:= Assets
* L:= Liabilities
* I:= Income
* E:= Expenses
* P:= Placeholder


Transazioni comuni
------------------

Riportiamo di seguito le tipologie di Transazioni più comuni che avvengono tra i Conti di cui sopra, suddivise per causale:

Ricarica
++++++++

* *ricarica*: in un GAS in cui c'è una gestione economica "a prepagato" (ovvero i Gasisti anticipano al GAS degli importi di denaro per ridurre o eliminare lo scambio di contante) un gasista può "ricaricare" il suo conto del gasista (acquisendo un credito nei confronti del GAS da utilizzare per il pagamento dei suoi Ordinigasista, dei Prelievi, della quota associativa annuale, ecc.).  

Decurtazione
++++++++++++

* *pagamento acquisto*: un gasista effettua il pagamento di un acquisto (oppure il Contabile lo effettua in sua vece); l'importo dell'acquisto viene prelevato dal conto del gasista e depositato sul conto del GAS

Prelievo
++++++++

* *pagamento Prelievo*: un gasista effettua il pagamento di un Prelievo effettuato (oppure il Contabile lo effettua in sua vece); l'importo del Prelievo viene prelevato dal conto del gasista e depositato sul conto del GAS

Quota
+++++

* *pagamento quota associativa*: un gasista effettua il pagamento della quota associativa annuale (oppure il Contabile lo effettua automaticamente in sua vece, oppure il Sistema lo effettua automaticamente al momento del rinnovo, previa conferma da parte del gasista); l'importo del Prelievo viene prelevato dal conto del gasista e depositato sul conto del GAS (o su un Conto ad-hoc)

Pagamento produttore: Fattura
+++++++++++++++++++++++++++++

* *pagamento ordine*: il GAS effettua il pagamento di un ordine, in base alla relativa fattura; l'importo della fattura viene prelevato dal conto del GAS, addebitato sul Conto "pagamenti fornitori" e scalato dal Conto produttore
* *consegna ordine*: il Fornitore consegna un ordine (e, contestualmente, la relativa fattura); l'importo della fattura viene addebitato sul Conto produttore

Spese di utenza
+++++++++++++++

* *spese varie del GAS*: il GAS effettua il pagamento di una spesa di natura varia non riconducibile ad un ordine (canone di affitto, utenze, ecc.) L'importo viene prelevato dal conto del GAS e addebitato su un Conto specifico.    
