Il referente contabile del GAS
==============================

|head2_descr|
-------------

Il gestore della cassa. Tiene i conti. Sa in qualsiasi momento lo stato economico di un soggetto partecipante alla retina. L'economico deve poter curare la casa e i movimenti del suo GAS.

Il referente economico può essere più di una figura all'interno di un GAS. Ciascuno a suo turno.

L'economico deve essere in grado di dire in qualsiasi momento quale sono:
- lo stato economico di un gassista e correggere il suo conto
- lo stato economico di un produttore e avere in mano la gestione delle consegne effetuate  ma che risultano non pagate cioè insolute.
- conoscere il saldo della cassa del GAS
- differenziare nella cassa del GAS:
1 - la disponibilità effettiva del GAS: i soldi del GAS detto anche il borsellino 
2 - l'ammontare dei depositi gassisti
3 - il totale degli insoluti dovuti ai produttori

L'economico deve avere uno strumento che lui permette di ricostruire la cronologia dei flussi economici. E sempre disponibile un ordinamento temporale del succedersi delle transazione economiche.

Gestione d'ordine
++++++++++++
Nel gestionale un referente produttore ha la possibilità di gestire anche la decurtazione dei gasisti che hanno partecipato ad uno suo ordine. Varie operazione del cassiere possono essere affidate al respettivo responsabile di consegna di un ordine. 


.. warning::

   Regole: L'economico non deve sapere niente della consegna. Interessa solo il totale famiglia consegnato. Il sistema attuale non prevede che l'economico o il referente  scende alla gestione economica al livello del prodotto.


I soggetti che compongono il Distretto di Economia Solidale sono
Gasista
GAS
Produttore
anonimo: uscita(spese di utenza) o entrata(introiti, incassi) dalla rete 

Una transazione economica si verificarsi tra due soggetti  o solo uno.  

Si identifica il Distretto di Economia Solidale basandosi sulla movimentazione delle transazione tra soggetti.

Se un gassista ricarica il suo conto. Si verifica un spostamento di monete tra il gassista e la cassa. Il saldo della rete rimane invariata.
Se il GAS paga un produttore. La rete verifica una perdita.
I pagamento di una fattura o altre servizi esterni verificano un uscita. 

|head2_terms|
-------------

* Vari conti (gasista, fornitore, cassa gas, borsellino gas)
* Prezzo ordinato / prezzo consegnato
* Totale ordinato / Fattura emessa dal produttore / Totale famiglie decurtato
* Registra il pagamento di uno o più ordini (gestione degli insoluti)

.. warning::

   regola: un ordine per un produttore

Nella gestione ordinaria di un ordine, l'economico deve eseguire 3 operazioni:
1 la registrazione della fattura
2 la decurtazione del totale famiglia per produttore. 
L'operazione 2 viene eseguita n volte quante ci sono di famiglie avendo partecipato all'ordine
3 Il pagamento effettivo del produttore. Questa operazione è indipendente delle 2 prime e si può verificare dopo un tempo non prevedibile.

il verificarsi dei punti 1 e 2, qualsiasi l'ordine di apparenza, provoca il cambio di stato dell'ordine. L'ordine passa dallo stato CHIUSO à CONSEGNATO. Entra in una fase di gestione degli insoluti. 
il punto 3 è asincrono. Se fatto insieme al punto 1 e 2 provoca il cambio dello stato fino ad ARCHIVIATO. Se no questo ordine è un insoluto che viene trattatto dopo che, passato un certo tempo tra la consegna e l'effettivo pagamento del produttore, il referente economico lo archivia definitivamente. 


.. warning::

   Un ordine archiviato non può essere modificato. 
   Ogni modifica future deve essere fatte tramite correzione. 

Variante. Oltre all'economico di turno, il punto 1 e 2 possono essere effettuate dal referente produttore di quel ordine. 

Oltre alla gestione dell'ordine, il referente economico deve poter effettuare le seguente operazioni:

1 correzione sugli soggetti attivi: Gassista e produttori
2 entrata e uscita della propria cassa senza punto di ingresso o di arrivo.


|head2_start|
-------------

* Consegne effettuate
* Importi

|head2_homepage|
-----------------

|head2_actions|
---------------

Gestione di un ordine
+++++++++++++++++++++

* Registra la Fattura di un ordine
* Decurta il totale famiglia per ciascun famiglie di un ordine
* Aggiunge una famiglia, inizialmente assente, e decurta il totale famiglia

Verifica conti dei soggetti
++++++++++++++++++++++++++

* Verifica i conti produttori
* Verifica i conti gassisti
* Verifica la cassa del GAS
* Verifica il borsellino del GAS

Ricarica di un Gasista
++++++++++++++++++++++

La gestione delle ricariche segue il modello del prepagato. Un gasista consegna soldi al referente economico che lo registra nel gestionale. La ricarica accredita il conto gasista. 

La gestione delle ricariche è abilitata per i referenti economici
Un economico accede al riquadro delle ricariche my-GF-ECO-Ricarica_ andando su:
DES > pagina del GAS > tab Conto

La griglia delle ricariche presenta la lista dei gasisti del GAS. 
Per ciascuno è evidenziato l'ultima ricarica fatta con la relativa data. 
Cosi l'economico tiene sotto occhio le ricariche fatte.

[FAQ] Ricaricare un gasista
Un referente economico vede i pulsanti di gestione: **Visualizza** e **Modifica**
Cliccando su **Modifica** la griglia passa in modalità di editing.
Appare una colonna *Recharge* dove è possibile inserire di fronte al nome del gasista l'importo da accreditare.
In questa modalità di editing appare anche un pulsante **Prepagato: ricarica il conto gasista**
Il referente economico ripete l'operazione per tutti gasisti da ricaricare lasciando vuoto l'inserimento da quelli da lasciare invariato.
Una volta inserito tutti gasisti da ricaricare, il referente economico preme su **Prepagato: ricarica il conto gasista**
La pagina viene rinfrescata e le somme vengono accreditate ad ciascuno gasista. L'economico può controllare l'effettivo versamento scorrendo la colonna *Last recharge*. 

.. _my-GF-ECO-Ricarica:

.. figure:: GF-ECO-Ricarica.png
   :align:   center

   Griglia per la gestione delle ricariche

[FAQ] Ho sbagliato a ricaricare un gasista
L'economico non può ritornare su una transazione economica. In questo caso l'economico deve portare una correzione. 
* Se l'ammontare da accreditare e superiore a quanto ricaricato, l'economico può procedere ad una seconda ricarica con la differenza mancante. 

* Se l'ammontare accreditato sul conto è superiore a quanto sborsato realmente dal gassista allora rimane solo una correzione in negativo da portare sul conto gasista. cf. my-correct-gasmember_


Correggere una transazione
+++++++++++++++++++++++

.. _my-correct-gasmember:

TODO *non implementato ancora*

Genera un bilancio annuale? (in futuro)
+++++++++++++++++++++++++++++++++++++++

FUTURE *non previsto ancora*

