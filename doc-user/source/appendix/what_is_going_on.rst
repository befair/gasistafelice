
Stato dei lavori e segnalazione dei problemi
============================================

Questa pagina è mantenuta aggiornata per illustrare, alla versione attuale (**NOTA: da pubblicare lunedì 28/11/2011**), 
cosa funziona nel software, e cosa non funziona nella piattaforma *Gasista Felice* disponibile su http://ordini.desmacerata.it

Nella pagina si specificano anche **quali problemi segnalare**.

.. _what_works_now:

Cosa funziona
-------------

**Per i referenti fornitori e i fornitori**:

1. Modificare disponibilità e prezzo nel *listino fornitore* associato al fornitore.
2. Modifica prodotto

*NOTA: una modifica in questo punto del software comporterà il cambiamento per tutto il DES.
Per modificare la presenza di un prodotto nel listino del proprio GAS, agire nel "listino fornitore per il GAS" presente nella scheda "Prodotti" della pagina relativa a* :ref:`resource_pact`.

**Per i referenti fornitori**:

1. Apertura nuovo ordine e sua gestione (avanzamento --> chiusura)
2. Definire il listino dei prodotti di quel produttore per un GAS (nel patto)
3. Aggiustare il listino prezzo del fornitore a livello DES e a Livello GAS (CASCADING)
3. Aggiustare la disponibilità del listino del fornitore a livello DES e a Livello GAS (CASCADING)
3. Aggiustare l'ordine fatto prima di inviarlo al fornitore?
4. Generazione del documento PDF per l'ordine. Sia in stato aperto che chiuso: (Ridurre solo allo stato chiuso?1)

**Per tutti**:

5. Notifiche via mail settimanali ed eventuali giornaliere (v. :ref:`notifications`)
6. Ordinare
7. Produzione del documento PDF per il paniere del gasista
8. Possibilità di aggiungere note su tutte le risorse del sistema (persone, fornitori, patti, ordini, ...). Le note aggiunte agli ordini verranno inserite nel documento PDF dell'ordine

**Per i referenti informatici dei GAS**:

8. Configurazione del GAS. **È la prima cosa che i referenti informatici devono fare**
9. Assegnazione dei ruoli *referente informatico*, *referente economico*, *referente fornitore* e *fornitore*

.. _what_is_in_testing:

Cosa è in fase di test
----------------------

1. Aggiungi prodotto
2. Aggiungi/Modifica fornitore
3. Aggiungi/Modifica categoria
4. Aggiungi/Modifica GAS
5. Gestione economica: nel software sono presenti alcune griglie per la gestione economica, danno un'idea di come saranno gestiti i conti nel GAS, ma non funzionano ora
6. Apertura in automatico degli ordini
7. Avvanzamento in automatico dei stati degli ordini con chiusura e invio PDF
8. Gestione delle email per le notifiche
9. Trattamento economico 2/3 decurtare le singole famiglie per un dato ordine
10. Gestione ruoli della scheda del fornitore rest/supplier/id/
11. Rimuovere i ruoli riguardante il fornitore della lista della gestione ruoli della scheda del GAS rest/gas/id/

.. _what_does_not_work:

Cosa non funziona / non c'è
----------------------------

Le cose non citate qui sopra sono da considerarsi non funzionanti o non realizzate oggi. Ne citiamo alcune:

1. Registrazione nuova persona
2. Cambio password
3. Alcuni link per semplificare la navigazione
4. Visualizzazione ad immagini di prodotti e categorie
5. Filtro dei prodotti
6. Filtro dei produttori
7. Disaccopiare il CASCADING abilitazione prodotto dalla gestione "non c'è" (eliminare ordini gasisti)
8. Insoluti. Lista degli ordini chiusi ed consegnati ma non pagatti: gestione insoluti
9. Archivio. Lista degli ordini archiviati
10. Trattamento economico 1/3 registrare la fattura emmessa dal produttore per un dato ordine
11. Trattamento economico 3/3 a) pagamento di un produttore per un dato ordine
12. Trattamento economico 3/3 b) pagamento di un produttore per più ordini cumulati = gestione insoluti
13. Trattamento economico Anagrafiche - Lista flussi economici per i gasisti
14. Trattamento economico Anagrafiche - Lista flussi economici per i supplier
15. Trattamento economico Anagrafiche - Lista flussi economici per i gas (Borsellino + Deposito)
16. Trattamento economico Conti - Saldo gassista. Calcolo e Vissualizzazione grafica
17. Trattamento economico Conti - Saldo supplier. Livello GAS. Calcolo e Vissualizzazione grafica
18. Trattamento economico Conti - Saldo supplier. Livello DES. Multi Calcolo e Multi Vissualizzazione grafica
19. Trattamento economico Conti - Saldo GAS. Calcolo e Vissualizzazione grafica per Borsellino e Deposito
20. Trattamento economico manipulazione - modifica di un flusso economico esistente (tra 2 soggetti)


.. _which_problems:

Quali problemi segnalare
------------------------

In questa fase di primo utilizzo del software, vi chiediamo il piacere di segnalare esclusivamente problemi relativi alle parti:

* che sono ritenute funzionanti :ref:`what_works_now` e/o 
* ad altre parti che sono **bloccanti** per portare avanti la vostra attività di routine

Grazie

.. _how_to_tell_us_a_problem:

Come segnalare i problemi
-------------------------

Vi chiediamo di segnalare i problemi specificati al punto :ref:`which_problems` su http://dialogo.desmacerata.it dove potete accedere con lo stesso utente con cui accedete al gestionale.

Nel segnalare un problema vi chiediamo di:

1. **descrivere in modo sintetico il problema che riscontrate**
2. **indicare sempre l'indirizzo a cui si verifica**. Lo trovate in alto nella *barra degli indirizzir* ed è nella forma http://ordini.desmacerata.it/gasistafelice/... . Copiatelo e incollatelo così come lo vedete nel forum;
3. **indicare i passi necessari per riprodurre il problema**
4. **aggiungere i tag (etichette) 'informatica' e 'gestionale' e 'problema' nello spazio apposito** (senza virgolette). 

Questa modalità di lavoro:
* faciliterà il gruppo di sviluppo nella risoluzione
* faciliterà tutti nel suggerire il modo in cui aggirare il problema
* aiuterà a vedere solamente le domande relative al programma (in particolare se il punto 4. è fatto bene)

Prima di segnalare un problema avere l'accortezza di **vedere se è già stato segnalato** e in tal caso aggiungere un commento alla segnalazione precedente.

Se si intende fare una domanda relativa all'applicazione, usare solamente i tag 'informatica' e 'gestionale'.

Se si intende fare una domanda relativa agli aspetti informatici del DES diversi dal gestionale usare solo 'informatica'.
