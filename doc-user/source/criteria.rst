Aspetti chiave
==============

TODO: rileggere e migliorare

Identità del GAS
----------------

Ogni GAS ha una marcata identità, e peculiarità che lo distinguono da ogni altro GAS: pertanto, non è possibile né opportuno tentare di omologarli rispetto alla gestione dei processi informativi interni, né tantomeno nella presentazione delle attività del GAS verso l'esterno.

Soluzione proposta
^^^^^^^^^^^^^^^^^^

* L'identità di un GAS si sviluppa principalmente attraverso la `Vetrina <Struttura#Vetrina>`_ e quindi:

 * Offrire ai GAS la possibilità di disporre di un sito-vetrina all'interno della piattaforma Gasista Felice, personalizzabile in toto a partire dall'aspetto grafico
 * Offrire ai GAS la possibilità di mantenere il proprio (eventuale) sito preesistente e di integrare le proprie news nel portale del DES esportandole in formato `RSS <http://it.wikipedia.org/wiki/RSS>`_. Anche il sito del GAS viene direttamente linkato dalla vetrina del DES; in questo modo i GAS vengono invitati a mostrare la loro appartenenza al DES. Le modalità specifiche con cui evidenziare l'identità di un GAS all'interno della piattaforma verranno discusse in una fase successiva (ad es. tramite un link, un logo, un tema?).

* Al livello del Gestionale questa problematica viene affrontata in questo modo:

 * Offrire ai GAS numerose opzioni di configurazione che consentano di adattare il comportamento del software alle dinamiche operative e gestionali che gli sono proprie 

Soggettività
------------

Uno dei principi ispiratori che guida lo sviluppo di questo software è quello della soggettività, ovvero: non deve essere l'utente ad adattarsi alle logiche di funzionamento della piattaforma, ma la piattaforma informatica a venire incontro alle esigenze e al modus operandi dei soggetti che la utilizzano.


Soluzione proposta
^^^^^^^^^^^^^^^^^^

Per abbracciare i molteplici casi d'uso del software, sono stati previsti vari ruoli, ognuno dei quali avrà accesso a funzionalità diverse in base alle specifiche esigenze.

I ruoli principali individuati sono:

* gasista
* referente informatico di un GAS
* contabile di un GAS
* referente fornitore (di un gas)
* fornitore/produttore
* referente fornitore

altri, non usati in tutti i GAS, ma comunque necessari per rispettare l'identità sono: 

* referente di consegna
* referente di ritiro
* referente di ordine

Infine

* CONFIG: Offrire al GAS la possibilità di configurare il proprio ambiente selezionando i ruoli effettivamente utilizzati e segnalando al sistema a quali ruoli associare gli eventuali ruoli non implementati


Vocabolario
-----------

Nell'affrontare il lavoro di analisi preliminare allo sviluppo della piattaforma web, come prima cosa abbiamo ritenuto opportuno e necessario definire una terminologia condivisa da tutto il gruppo di lavoro; in questo modo, avremmo avuto a disposizione un linguaggio comune e non ambiguo per discutere le problematiche relative al dominio applicativo del progetto.  Il frutto dei nostri sforzi in questo senso è quello che noi abbiamo chiamato un `Vocabolario <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario>`_, un documento "in progress" ma comunque utile come punto di riferimento.

Nel corso della stesura del Vocabolario, che è uno strumento ad esclusivo uso interno del gruppo di lavoro, sono sorti alcuni dubbi su quali fossero i termini più corretti da utilizzare invece nell'interfaccia utente: alcuni esempi:

* `produttore` vs `fornitore`: qual termine è più adeguato per definire chi fornisce i prodotti ad un GAS ? qual è il termine più usato e familiare nella prassi operativa dei GAS ? In effetti, non tutti i fornitori di un GAS producono tutti i prodotti che vendono, per cui tecnicamente in questi casi si avrebbero dei `distributori`; d'altra parte, uno dei principi costitutivi dei GAS è la ricerca della disintermediazione nei rapporti economici, per cui in molti casi i `fornitori` sono anche `produttori`.  

* nel corso dell'analisi, abbiamo convenuto sulla necessità di implementare un recipiente "virtuale" in cui i gasisti potessero accumulare i prodotti ordinati (quello che in un sito di e-commerce si chiama generalmente `carrello`). Abbiamo avviato una discussione in `questo ticket <http://www.jagom.org/trac/REESGas/ticket/22>`_, aprendo anche un `sondaggio <http://doodle.com/cnw93b3745u9g2bd>`_ sul tema.       


Soluzione proposta
^^^^^^^^^^^^^^^^^^

Visto che il termine `fornitore` ha un utilizzo valido in tutti i casi analizzati, ed essendo un'attività principale degli informatici evitare di dover declinare le cose, la proposta è di utilizzare `fornitore`. Ma lasciamo a voi la parola, chiedendovi anche: dovendo scegliere un termine unico, su quale ricadrebbe la scelta se un domani il GAS volesse acquistare servizi (ad es: viaggi, corsi di formazione, ..) ?

La domanda relativa al carrello non è prioritaria.


Costruzione del prezzo
-------------------------------------------------
Un fornitore potrebbe decidere di applicare prezzi diversi a GAS diversi in base, ad esempio, ad aspetti di carattere logistico come
ad esempio il costo di consegna: consegnare a GAS più lontani o più difficilmente raggiungibili comporta dei costi maggiori

Quindi: come gestire la variazione del prezzo di listino per ogni singolo GAS?

Riferimenti
^^^^^^^^^^^
* http://www.jagom.org/trac/REESGas/ticket/24

Soluzione proposta
^^^^^^^^^^^^^^^^^^

Dalla nostra analisi è emerso questo scenario:

* il fornitore mette un prodotto sul mercato con un determinato prezzo
* nel patto di solidarietà che stipula con un dato GAS tale prezzo POTREBBE subire una variazione in positivo o in negativo per accordi tra il fornitore e il GAS (ad, es. per i motivi elencati in precedenza)
* **DUBBIO AMLETICO ANCHE DI ORDINE LEGALE**: il GAS potrebbe decidere di applicare un ricarico sui prodotti che acquista per pagare le spese vive legate alle gestione del GAS (ad esempio la sede, le bollette, etc). La normativa attuale non consente ai GAS di retribuire le persone che svolgono attività al loro interno (e tantomeno ricaricare sui prodotti per coprire questi costi), ma devono comunque pagare le bollette. Possono farlo ricaricando sul prezzo dei prodotti con la logica: chi più usufruisce del GAS più contribuisce al suo mantenimento?
* CONFIG: Offrire al GAS la possibilità di configurare il proprio ambiente con una procedura di adattamento del prezzo (nel caso si decidesse di implementare questa funzionalità)

Inoltre, una questione ancora aperta nel gruppo di lavoro è se le modifiche debbano essere applicate ''a percentuale'' sull'intero importo dei prodotti, oppure le variazioni possano essere relative ad un prodotto specifico. La proposta che va per la maggiore è la variazione in percentuale per evitare discriminazioni tra fornitori e prodotti (quelli a cui venisse applicato un ricarico sarebbero ovviamente penalizzati rispetto agli altri).


Variazioni dei prezzi tra l'ordine e la consegna
-------------------------------------------------

Il prezzo effettivo di un prodotto alla consegna potrebbe subire variazioni rispetto al prezzo dello stesso al momento dell'invio dell'ordine dal GAS al fornitore (a causa di esigenze logistiche del fornitore, o per motivi di altro genere). Quindi: come gestire le eventuali variazioni del prezzo di listino che avvengano tra l'ordine e la consegna?

Soluzione proposta
^^^^^^^^^^^^^^^^^^

* consentire ai referenti dei fornitori all'interno di un GAS di applicare le eventuali variazioni che venissero comunicate dai fornitori prima della consegna
* verificare e rendicontare il prezzo effettivo al momento della consegna ("Fa fede la fattura")  


Flusso dell'ordine
------------------

L'ordine è il processo chiave di tutto il sistema (in effetti, sarebbe meglio parlare di "ordini": dai gasisti al GAS e dal GAS ai fornitori). Per implementare una gestione informatizzata del processo di ordine, prima di tutto è necessario catturare i casi d'uso che si riscontrano nell'attività dei GAS .  Un motto che riassume quanto la realtà sia articolata potrebbe essere: ''"Prima della consegna può succedere di tutto"''.

Ad esempio, in un sistema di e-commerce dopo la conferma è improbabile (spesso impossibile) che si verifichi una variazione del prezzo; invece la nostra piattaforma in Gasista Felice deve prevedere questa eventualità, perché può accadere nei GAS.

Esistono inoltre alcuni GAS che preferiscono che gli ordini vengano confermati dai gasisti, altri che invece registrano subito l'ordine come valido.

Riferimenti
^^^^^^^^^^^
* http://www.jagom.org/trac/REESGas/ticket/27

Soluzione proposta
^^^^^^^^^^^^^^^^^^

* Prevedere più tipi di flusso dell'ordine: uno semplice, uno più complicato, uno che richiede la conferma del gasista, l'altro no
* CONFIG: Offrire al GAS la possibilità di configurare il proprio ambiente con il flusso di ordine usato

Disponibilità dei prodotti
--------------------------

Gestire una disponibilità quantitativa dei prodotti dà modo di capire quanti ne sono rimasti, quanti sono ordinabili e quanti si possono redistribuire fra i GAS a cui mancano, in caso di surplus di offerta verso un GAS. Tuttavia una gestione di questo tipo comporta l'onere di inserimento delle quantità disponibili da parte del fornitore (o del gasista referente del fornitore).

Soluzione proposta
^^^^^^^^^^^^^^^^^^

* Implementare in prima battuta una gestione qualitativa della disponibilità (''c'è o non c'è'')
* In un secondo momento valutare l'interesse in una gestione quantitativa ed, eventualmente, implementarla 
* CONFIG: Offrire al GAS la possibilità di configurare il proprio ambiente con la gestione a qualità o a quantità (nel caso quest'ultima venga implementata)

Visualizzazione degli ordini aperti
-----------------------------------

Alcuni GAS preferiscono visualizzare i prodotti ordinabili raggruppati per fornitore, altri in base al momento in cui verranno consegnati: come conciliare queste due esigenze ?

Soluzione proposta
^^^^^^^^^^^^^^^^^^

* CONFIG: Offrire al GAS la possibilità di configurare il proprio ambiente con la visualizzazione degli ordini per produttore o per consegna



