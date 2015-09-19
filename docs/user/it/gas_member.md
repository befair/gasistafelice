# Il gasista

## Descrizione

Il gasista è una persona che appartiene ad un [GAS](resource_gas.md).
Lo scopo del gasista è ordinare prodotti, resi disponibili in un [ordine](resource_order.md) aperto da un [referente fornitore](gas_referrer_supplier.md).

Le tipiche attività del gasista comprendono:

* ordinare i prodotti;
* visualizzare il paniere contenente i prodotti ordinati;
* confermare i prodotti, se previsto nel modo di operare del GAS.

> *Gasista Felice* consente ad una persona di appartenere a più GAS contemporaneamente.

## Azioni

### Entra con nome utente e password

Nella pagina iniziale del sito, un utente inserisce il nome utente e la password. In questo modo il sistema può identificare l'utente, consentirgli di ordinare e di fare tutte le azioni corrispondenti ai ruoli che riveste.

È solo dopo aver messo nome utente e password che il sistema sa se l'utente è un "semplice" gasista, un referente fornitore, un fornitore, un referente economico o un referente informatico del GAS.

![Schermata di autenticazione](_static/gas_member_auth.png)

> Pagina iniziale: l'utente inserisce nome utente e password.

### Ordina

Il gasista accede direttamente alla pagina con il listino dei prodotti ordinabili. La lista dei prodotti che si trova davanti è quella degli ordini aperti per il suo GAS (se solo un ordine o se listino misto di più ordini, questo è deciso dal referente informatico).

Dei prodotti che si trova davanti, il gasista dovrà impostare la quantità richiesta e eventualmente inserire delle note (ad esempio: "tagliato fino", "se possibile già pulito")

Premendo il bottone "Metti nel paniere" i prodotti selezionati andranno nel paniere.

![Schermata di gestione del paniere](_static/order.png)

> Gestione del paniere: permette l'inserimento dei prodotti che si vuole ordinare

### Gestisce il proprio paniere

Una volta ordinati i prodotti è possibile visualizzarli nella scheda paniere --> blocco paniere.

![Schermata di gestione del paniere](_static/basket.png)

> Paniere dei prodotti ordinati: permette la modifica/eliminazione/conferma dei prodotti ordinati

Se il gas lo richiede è necessario confermare i prodotti ordinati.

Una volta che l'ordine è chiuso, i prodotti passano dal "paniere" al "paniere da consegnare". A questo punto non resta che attendere la consegna dei prodotti! Quantità e note non sono più modificabili.

![Schermata del paniere dei prodotti in consegna](_static/basket_to_deliver.png)

> Paniere dei prodotti in consegna: visualizza i prodotti da ricevere. Non modificabili

### Modifica la propria scheda gasista

Il gasista può modificare le informazioni relative al proprio profilo utente: nome, cognome, indirizzo, recapiti.

Nella scheda del gasista troviamo due riquadri (blocchi): scheda del gasista e scheda della persona. Il primo contiene informazioni relative all'appartenenza della persona in un GAS, l'altro le informazioni relative alla persona nel suo complesso.

In questo secondo blocco è possibile anche cambiare la propria password

![Scheda del gasista](_static/gas_member_info.png)

> Visualizzazione e gestione informazioni del profilo utente

## Terminologia

Breve definizione dei termini:

* Ordine: l'ordine che il referente fornitore apre, chiude ed invia al fornitore con i prodotti ordinati dai gasisti
* Consegna: processo in cui un fornitore consegna fisicamente ad un GAS la merce relativa ad un ordine
* Paniere: l'insieme dei prodotti ordinati per gli ordini aperti
* Paniere da consegnare: l'insieme dei prodotti ordinati negli ordini attualmente chiusi e da consegnare
* fornitore: soggetto che fornisce un GAS
* Prezzo ordinato: prezzo di un prodotto al momento dell'ordine
* Prezzo consegnato: prezzo di un prodotto al momento della consegna

## Da cosa parte

Il gasista non deve pensare a curare i seguenti aspetti che sono di competenza di altri ruoli:

* [GAS](resource_gas.md) già inserito
* [Fornitori](resource_supplier.md) già inseriti
* [Patto di solidarietà](resource_pact.md) già costituito
* [Ordine](resource_order.md) già aperto
