# Appendice A: Terminologia

## A chi è rivolto questo documento

  * A chi vuole comprendere la terminologia del software e degli sviluppatori di Gasista Felice;
  * A chi vuole relazionarsi efficacemente con gli sviluppatori del software;
  * A chi è interessato a capire come il mondo dei GAS è stato strutturato dagli sviluppatori di Gasista Felice;

## Premessa

La documentazione per gli sviluppatori è scritta interamente in inglese.
Questo è un documento che funge da ponte verso lo sviluppo e include
i corrispettivi nomi inglesi e collegamenti ai modelli (software) che realizzano quanto descritto.

## Un obiettivo: terminologia condivisa per macro-aree

Nella descrizione dei processi relativi alla gestione operativa di un GAS entrano in gioco diverse entità e concetti: per consentire una descrizione efficace, sintetica e non ambigua di tali processi, è necessario definire una terminologia condivisa e utilizzarla sistematicamente, sia nei documenti tecnici che nel corso delle discussioni sul contenuto di tali documenti.  Per organizzare meglio il vocabolario, si sono suddivisi i termini in macro-aree, anche se in alcuni casi un termine potrebbe appartenere a più macro-aree.

## Area generale

### Sistema

È Gasista Felice, per gli amici GF ;)

### Installazione

È una installazione di GF, possiamo dire che è un indirizzo web (url) dove si può trovare installato ed usare GF.

### Utente

Indica un'utenza del [Installazione](#installazione).

Ad essa vengono assegnati i [Ruoli](#ruoli) e conseguentemente i [Permessi](#permessi).

### Risorsa

Ref: [Resource](https://github.com/befair/gasistafelice/blob/master-dj17/gasistafelice/gf/base/models.py#L41 "Il modello Resource")

È una astrazione che indica un modello base fondamentale per il sistema.

Una risorsa è **una qualunque entità del sistema che risponde alle seguenti caratteristiche**:

* implementa la [Resource API](#TODO-TODOC):
  * è identificata univocamente con un "urn" (uniform resource name) e un url;
  * da essa si recuperano le altre risorse del sistema;
* implementa la [Permission API](#TODO-TODOC):
  * vi si possono verificare (direttamente o indirettamente) i permessi;
* implementa la [Referrers API](#TODO-TODOC):
  * vi si possono recuperare (direttamente o indirettamente) i referenti;
* implementa la [Contact API](#TODO-TODOC):
  * vi si possono recuperare (direttamente o indirettamente) i contatti associati;
* implementa la [History API](#TODO-TODOC):
  * registra le sue modifiche nel tempo (versionamento);
  * può essere recuperata quindi ad un determinato istante temporale;
* implementa la [Icon API](#TODO-TODOC):
  * ha associata un'icona / un'immagine di default per il tipo e opzionalmente specializzata per l'oggetto specifico;
* può implementare la [Accounting API](#TODO-TODOC):
  * se è un [Soggetto economico](#soggetto-economico)
* può implementare la [Cache API](#TODO-TODOC):
  * può essere messa in memoria temporanea per aumentare le performance;
  * può essere invalidata la copia in cache;

### DES

Ref: [DES](https://github.com/befair/gasistafelice/blob/master-dj17/gasistafelice/des/models.py#L35 "Il modello DES")

Un DES è un [Distretto di Economia Solidale](http://web.resmarche.it/resmarche/articles/art_1978.html), ossia un territorio dove si pratica l'economia solidale e si esprimono relazioni solidali in tutti gli ambiti della vita quotidiana, o meglio ... in tutti gli ambiti in cui si riesce ;)

La caratteristica del DES è di essere strettamente legato al TERRITORIO che per ragioni culturali o geografiche
facilita l'incontro e lo scambio di beni o servizi tra gli attori presenti.

Ogni installazione di Gasista Felice può servire un solo DES.
Altrimenti detto, tutte le entità contenute in una installazione di Gasista Felice sono incluse in uno ed un solo DES.

Gasista Felice aiuta la realizzazione degli scambi economici in un DES e il monitoraggio del flusso economico solidale da essi prodotto.

### Persona

Ref: [Person](https://github.com/befair/gasistafelice/blob/master-dj17/gasistafelice/gf/base/models.py#L550 "Il modello Person")

Persona fisica. Da considerare come l'anagrafica di qualunque persona che si voglia registrare come contatto in Gasista Felice

### Soggetto

È un [utente](#utente) o una persona giuridica

### Soggetto economico

Ref: è indicato dal decoratore ```@economic_subject``` è qualunque risorsa che abbia un [Conto](#conto) nel sistema.

I soggetti economici in GF sono:

* Persona
* GAS
* Fornitore
* DES

### Luogo

Ref: [Place](https://github.com/befair/gasistafelice/blob/master-dj17/gasistafelice/gf/base/models.py#L929 "Il modello Place")

Un luogo, definito da un indirizzo e da coordinate GPS opzionali.

### Contatto

Ref: [Contact](https://github.com/befair/gasistafelice/blob/master-dj17/gasistafelice/gf/base/models.py#L903 "Il modello Contact")

Un contatto generico per una [risorsa](#risorsa). È composto da un tipo e un valore.
Attualmente i tipi disponibili sono:

* Telefono
* Fax
* E-mail

## Area fornitori

### Fornitore

Ref: [Supplier](https://github.com/befair/gasistafelice/blob/master-dj17/gasistafelice/gf/supplier/models.py#L47 "Il modello Supplier")

Soggetto che espone prodotti al [DES](#des).
Può entrare in relazione con uno o più [GAS](#gas) tramite un [Patto di solidarietà](#patto-di-solidarietà) (per ogni GAS).
Se un Fornitore ha un Patto di solidarietà con un GAS si dice che "il fornitore serve il GAS".

È caratterizzato da:

* una scheda aziendale che contiene le informazioni anagrafiche:
  * Nome e cognome
  * Sede -> [Luogo](#luogo)
  * Codice fiscale o Partita IVA
  * Contatti aziendali
  * Frontman -> [Persona](#persona) "simbolo" del fornitore
  * Lista di rappresentanti -> [Persone](#persona) di riferimento del fornitore
* le [Persone](#persona) con agganciate un [Utente](#utente) e [Ruolo Fornitore](#ruolo-fornitore);
* un [Listino produttore](#listino-produttore) con i prodotti offerti al [DES](#des)

### Prodotto

Ref: [Product](https://github.com/befair/gasistafelice/blob/master-dj17/gasistafelice/gf/supplier/models.py#L791 "Il modello Product")

Bene o servizio che un [Fornitore](#fornitore) espone al [DES](#des).
Riguarda l'essenza del bene, e non le sue modalità di vendita o distribuzione (perché esse possono essere multiple)
che invece sono nello [Stock](#stock).

È caratterizzato da:

* Nome e descrizione;
* Codice univoco per produttore;
* Produttore -> [Fornitore](#fornitore). Risponde alla domanda "chi ha prodotto il bene o il servizio?";
* Categoria -> una delle categorie classificate del DES;
* Unità di misura (UM) -> standard mondialmente riconosciuto (gr,lt,..). V. [unità di misura del DES](./list.md);
* Unità di prodotto (PU) -> confezione, pacco, dama, bottiglia, pezzo. V.  [unità di prodotto del DES](./list.md);
* Unità di misura per unità di prodotto (MUPPU) -> quantità di UM in un PU. Ad es: 1 pacco da 500gr di pasta;

### Catalogo fornitore

Ref: NON ha un modello corrispondente nel sistema, è solo un modo di identificare tutti i [Prodotti](#prodotto) associati ad un [Produttore](#fornitore).

### Stock

Ref: [SupplierStock](https://github.com/befair/gasistafelice/blob/master-dj17/gasistafelice/gf/supplier/models.py#L974 "Il modello SupplierStock")

Descrive le specifiche modalità di fornitura di un [Prodotto](#prodotto) da parte di un [Fornitore](#fornitore); è un'entità che estende il prodotto con informazioni non intrinseche ad esso (ad esempio legate a fattori contingenti come disponibilità o andamento del prezzo).

È caratterizzato dai seguenti attributi:

* [Fornitore](#fornitore): risponde alla domanda "chi fornisce il bene?";
* [Prodotto](#prodotto): rif. al modello che contiene le informazioni essenziali del prodotto;
* Categorizzazione interna del fornitore: categoria specifica utile solo al fornitore (per l'ordine);
* Codice del prodotto per il fornitore;
* Prezzo;
* Disponibilità (SI/NO);
* [opzionale] quantità disponibile;
* [opzionale] quantità minima ordinabile da un GAS espressa in PU (```units_minimum_amount```);
* [opzionale] step di incremento ordinabile da un GAS espresso in PU - cartoni (```units_per_box```);
* [opzionale] quantità minima ordinabile da un gasista espressa in PU (```detail_minimum_amount```);
* [opzionale] step di incremento ordinabile da un gasista espresso in PU (```detail_step```);
* note sulla consegna (ad es: uno scatolone rosso con 10 pacchi di pasta)

### Listino fornitore

Ref: NON ha un modello corrispondente nel sistema, è solo un modo di identificare tutti gli [Stock](#stock) associati ad un [Fornitore](#fornitore). E che sono quindi da esso esposti al [DES](#des).

Definisce l'offerta economica base che un Fornitore, in un dato istante, espone al DES; è una lista di [Stock](#stock).

Operazioni di modifica sul Listino fornitore, si ripercuotono a cascata sul [Listino del patto](#listino del patto) e [Listino degli ordini](#listino-di-ordine);

## Area GAS

### GAS

Ref: [GAS](https://github.com/befair/gasistafelice/blob/master-dj17/gasistafelice/gf/gas/models/base.py#L64 "Il modello GAS")

È la [Risorsa](#risorsa) di GF che rappresenta un [Gruppo di Acquisto Solidale](http://retegas.org/upload/dl/doc/GASDocumentoBase.PDF "La carta nazionale dei GAS").

È caratterizzato dai seguenti attributi

* Informazioni anagrafiche:
  * Nome;
  * Codice di 3 lettere identificativo nel [DES](#des);
  * Sede -> [Luogo](#luogo)
  * Descrizione;
  * Quota associativa;
  * Data di fondazione;
  * Codice fiscale o partita IVA se presenti;
  * Sito web;
* Elenco dei [Patti di solidarietà](#patto-di-solidarietà);
* Elenco dei [Referenti informatici](#TODO-TODOC);
* Elenco dei [Referenti fornitore](#TODO-TODOC);
* Elenco dei [Referenti economici](#TODO-TODOC);
* Elenco dei [Gasisti](#gasista);
* Elenco degli attivisti: le [Persone](#persona) che partecipano (non hanno un ruolo particolare in GF);

Esso è anche un [soggetto economico](#soggetto-economico), quindi ha una serie di conti associati:

* uno generale;
* uno per ogni gasista;
* uno per ogni patto di solidarietà;

### Retina

Ref: non è un modello nel software, è identificato nella configurazione di un GAS, dai GAS che possono ordinare con il GAS che si sta configurando.

Aggregato di GAS operanti in un territorio limitrofo, che per comodità possono avviare ordini InterGAS.

### Gasista

Ref: [GASMember](https://github.com/befair/gasistafelice/blob/master-dj17/gasistafelice/gf/gas/models/base.py#L839 "Il modello GASMember")

Il gasista è una risorsa del sistema.
Esso è l'associazione di una [Persona](#persona) ad un [GAS](#gas). Le persone che possono essere associate ai GAS sono solo le persone che a loro volta hanno associate un [Utente](#utente).

Oltre agli attributi "persona" e "gas" integra:

* Gli attributi necessari per la sospensione definitiva (cancellazione) o temporanea (ad es: vacanze);
* L'indicazione di quando è stata pagata la quota associativa;
* L'identificativo nel GAS, ossia il numero della tessera nel GAS se esiste;
* lista dei Ruoli (incarichi) che ha dato disponibilità a ricoprire (attualmente non utilizzato, non utile);

### Patto di solidarietà

Ref: [GASSupplierSolidalPact](https://github.com/befair/gasistafelice/blob/master-dj17/gasistafelice/gf/gas/models/base.py#L1697 "Il modello GASSupplierSolidalPact")

**TODO: REFACTORING in Pact**

È il rapporto reciproco tra un [GAS](#gas) e un [Fornitore](#fornitore), e una [risorsa](#risorsa) fondamentale del sistema, infatti ogni ordine è aperto relativamente ad un Patto di solidarietà.

Il suo compito base è di mettere in relazione le risorse GAS e Fornitore, ma è progettato anche per
contenere l'insieme delle condizioni di fornitura, economiche e non, condivise e sottoscritte.
In questo modo funge da configuratore delle impostazioni di default per gli ordini tra quel GAS e quel Fornitore).

Comprende/è collegato a:

* il [Listino del patto](#listino-del-patto) che include la scelta del GAS di specifici prodotti;
* Giorno, ora e luogo predefiniti per la consegna;
* La possibilità di inviare una mail alla chiusura;
* Gli attributi necessari per la sospensione definitiva (cancellazione) o temporanea (ad es: vacanze);
* il Documento;
* l'importo minimo di un [Ordine](#ordine);
* una modifica %, in positivo o negativo, sul prezzo base di ogni Prodotto in base agli accordi presi (che tenga conto, ad es., di fattori logistici e/o del volume di consumi del GAS);
* quanti giorni prima della [Consegna](#consegna) bisogna chiudere l'[Ordine](#ordine);
* vi sono associati i [referenti di patto](#il-ruolo-di-referente-del-patto);

### Stock del patto

Ref: [GASSupplierStock](https://github.com/befair/gasistafelice/blob/master-dj17/gasistafelice/gf/gas/models/base.py#L1446 "Il modello GASSupplierStock")

**TODO: REFACTORING in PactStock**

Descrive le specifiche modalità di fornitura di uno [Stock](#stock) di un determinato [Patto di solidarietà](#patto-di-solidarietà).

Esso è sostanzialmente uno [Stock](#stock) modificato in base al Patto di solidarietà tra il GAS e il Fornitore.

È caratterizzato dai seguenti attributi:

* [Stock](#stock): chiaramente lo stock a cui si riferisce;
* prezzo: praticato dal Fornitore al GAS. Esso comprende le eventuali modifiche apportate al prezzo base dal Patto di solidarietà;
* stato di abilitazione: abilitato o no;
* [opzionale] quantità minima ordinabile dal gasista: può essere impostata dal [referente del patto](il-ruolo-di-referente-del-patto) ad un sottomultiplo di quella stabilita dal Fornitore, per venire incontro alle esigenze dei Gasisti;
* [opzionale] step di incremento ordinabile dal Gasista: può essere impostato dal [referente del patto](il-ruolo-di-referente-del-patto) ad un sottomultiplo di quello stabilito dal Fornitore, per venire incontro alle esigenze dei Gasisti)

### Listino del patto

Ref: non è un modello nel Sistema, ma un aggregato di [Stock del patto](#stock-del-patto);

L'insieme degli Stock che un GAS è interessato ad acquistare da un determinato Fornitore; è, per definizione, un sottoinsieme del [Listino fornitore](#listino-fornitore) del Fornitore corrispondente.

Riceve le modifiche a cascata dal Listino fornitore.
Le modifiche fatte su di esso (disponibilità dei prodotti) si ripercuotono sul [Listino degli ordini](#listino-di-ordine).

## Area ordini TODO TODOC

### !OrdineFornitore ###
Un ordine che il GAS invia ad un Fornitore; è caratterizzato da:
* [[#Fornitore|Fornitore]]
* data di apertura
* data di chiusura
* [[#AppuntamentoDiConsegna|AppuntamentoDiConsegna]] (le modalità con cui il Fornitore consegna al GAS la merce ordinata )
* [[#AppuntamentoDiRitiro|AppuntamentoDiRitiro]] (le modalità di distribuzione della merce ordinata ai Gasisti)
* stato
* `APERTO` (i Gasisti possono contribuire all'!OrdineFornitore)
* `CHIUSO` (i Gasisti non possono più contribuire all'!OrdineFornitore)
* `IN_COMPLETAMENTO` (il ReferenteFornitoreGAS  ha attivato la [[procedura di completamento]] dell'!OrdineFornitore)
* `FINALIZZATO` (l'!OrdineFornitore è completo e non è più modificabile, in alcun modo, dai Gasisti)
* `INVIATO` (il ReferenteFornitoreGAS ha inviato l'!OrdineFornitore al Fornitore )
* `CONSEGNATO` (il Fornitore ha consegnato l'!OrdineFornitore nel [[#PuntoDiConsegna|PuntoDiConsegna]] previsto)
* `ECCEZIONE` (comprende gli stati di errore, da definire in seguito, es.: annullato, parzialmente consegnato dal Fornitore, presenza di merce difforme,..)
* il [[#ListinoFornitoreGasista|ListinoFornitoreGasista]] ad esso associato
* l'insieme degli [[#OrdiniGasista|OrdiniGasista]] ad esso associati
* [opzionale] importo minimo (sotto il quale l'!OrdineFornitore non viene accettato dal Fornitore)
### !ListinoFornitoreGasista ###
Descrive la selezione di Prodotti effettivamente ordinabili dai Gasisti nel contesto di un dato [[#OrdineFornitore|OrdineFornitore]], e include le informazioni necessarie a tracciare la [[#Consegna|Consegna]] dell'!OrdineFornitore in questione a livello di singolo Prodotto.  È una lista di elementi che potremmo chiamare ''!VoceDiOrdineFornitore'', caratterizzati dai seguenti attributi:
* [[#OrdineFornitore|OrdineFornitore]]
* [[#StockFornitoreGAS|StockFornitoreGAS]]
* [opzionale] quantità massima ordinabile (impostata dal [[#ReferenteFornitoreGAS|ReferenteFornitoreGAS]]; può servire per una distribuzione equa tra i Gasisti in caso di scarsità dell'offerta)
* prezzo di ordine (prezzo a cui è stato eseguito l'ordine di un'unità di Prodotto da parte del GAS al Fornitore)
* prezzo di consegna (prezzo unitario effettivamente applicato dal Fornitore al GAS al momento della [[#Consegna|Consegna]], come risultante da fattura)
* quantità ordinata (n. di unità di Prodotto complessivamente ordinate dal GAS nell'ambito dell' [[#OrdineFornitore|OrdineFornitore]])
* quantità consegnata (n. di unità di Prodotto effettivamente consegnate dal Fornitore al GAS nell'ambito dell' [[#OrdineFornitore|OrdineFornitore]])
### !ListinoGasista ###
È l'aggregato di tutti gli attuali [[#ListiniFornitoreGasista|ListiniFornitoreGasista]] su tutti gli [[#OrdineFornitore|OrdineFornitore]] attualmente aperti.
### Carrello ###
Un recipiente virtuale, specifico per ogni Gasista, che in ogni istante contiene l'insieme dei Prodotti selezionati dal Gasista nel corso delle sessioni  di uso del [[#Sistema|Sistema]] (sia quella attuale che quelle precedenti) e non ancora confermati (ovvero non convertiti in un [[#OrdineGasista|OrdineGasista]]); è una lista di !VociDiCarrello (in generale appartenenti a [[#OrdineFornitore|OrdiniFornitore]] diversi). In pratica, una !VoceDiCarrello è un !OrdineGasista nello stato NON_CONFERMATO.

>> ''Nota: il termine "Carrello" non è appropriato, essendo troppo legato all'ambiente  della GDO; meglio un termine come "Cesto", "Cestino", "Paniere", "Sporta",..; da scegliere ! (aprire un sondaggio tra i Gasisti ?)''''

> Se non si trova una condivisione potremo mettere il termine configurabile nell'interfaccia grafica.

### !OrdineGasista ###
Disposizione di acquisto "atomica" (mono-prodotto) da parte del Gasista verso il GAS; viene generato, automaticamente o dietro conferma dell'utente, in base al contenuto del Carrello; è caratterizzato da:
* Gasista (colui che effettua l'ordine)
* [[#OrdineFornitore|OrdineFornitore]]^[[#1|a]]
* Prodotto ordinato
* n. di unità di Prodotto ordinato
* prezzo (unitario) a cui stato eseguito l'!OrdineGasista
* n. di unità di Prodotto ritirate dal Gasista
* stato: può assumere i valori:
* NON_CONFERMATO: l'!OrdineGasista è solamente una [[#Carrello|VoceDiCarrello]]
* CONFERMATO: l'!OrdineGasista è stato confermato dal Gasista^[[#2|b]]
* FINALIZZATO: l'!OrdineFornitore associato all'!OrdineGasista è stato chiuso, per cui l'!OrdineGasista non è più modificabile dal Gasista
* INVIATO: l'!OrdineGasista è stato inviato al Fornitore
* RITIRABILE: l'!OrdineGasista è disponibile per il ritiro da parte del Gasista
* RITIRATO: l'!OrdineGasista è stato ritirato dal Gasista
* ANNULLATO: l'!OrdineGasista è stato annullato dal Fornitore

### !OrdineFornitorePeriodico ###
Un !OrdineFornitorePeriodico è un meccanismo utilizzabile da un [[#ReferenteFornitoreGAS|ReferenteFornitoreGAS]] per aprire (e chiudere) automaticamente un [[#OrdineFornitore|OrdineFornitore]], a cadenza fissata, secondo un determinato template specificato al momento della creazione dell'!OrdineFornitorePeriodico.  Ovviamente, solo alcuni !OrdiniFornitore si prestano ad essere generati tramite un !OrdineFornitorePeriodico: quelli che si ripropongono identici ad intervalli di tempo regolari.

Un !OrdineFornitorePeriodico è caratterizzato dai seguenti attributi:
* Fornitore
* [[BozzaAnalisiFunzionale/Gestione_degli_ordini/OrdiniPeriodici#Descrizionedellaproblematica|schema di ricorrenza]]
* [[BozzaAnalisiFunzionale/Gestione_degli_ordini/OrdiniPeriodici#Descrizionedellaproblematica|periodo di validità]]
* durata (n. di giorni in cui l'!OrdineFornitore generato rimane aperto)
* ora di apertura
* ora di chiusura
* numero di giorni trascorsi dall'ultima occorrenza generata
* [[BozzaVocabolario#AppuntamentoDiConsegna|AppuntamentoDiConsegna]]
* [[BozzaVocabolario#AppuntamentoDiRitiro|AppuntamentoDiRitiro]]
* [opzionale] importo minimo (sotto il quale l'[[BozzaVocabolario#OrdineFornitore|OrdineFornitore]] non viene accettato dal Fornitore)
* stato
* `ATTIVO`
* `DISATTIVO`
### !OrdineGasistaPeriodico ###
Un !OrdineGasistaPeriodico è un meccanismo utilizzabile da un Gasista per generare automaticamente un [[#OrdineGasista|OrdineGasista]], a cadenza fissata, secondo un determinato template specificato al momento della creazione dell'!OrdineGasistaPeriodico.  Ovviamente, solo alcuni !OrdiniGasista si prestano ad essere generati tramite un !OrdineGasistaPeriodico: quelli che si ripropongono identici ad intervalli di tempo regolari.

Un !OrdineGasistaPeriodico è caratterizzato dai seguenti attributi:
* Gasista
* [[BozzaAnalisiFunzionale/Gestione_degli_ordini/OrdiniPeriodici#Descrizionedellaproblematica|schema di ricorrenza]]
* [[BozzaAnalisiFunzionale/Gestione_degli_ordini/OrdiniPeriodici#Descrizionedellaproblematica|periodo di validità]]
* [[#Prodotto|Prodotto]] da ordinare
* n. di unità di Prodotto da ordinare
* numero di giorni trascorsi dall'ultima occorrenza generata
* stato
* `ATTIVO`
* `DISATTIVO`


[#1 a] Un !OrdineGasista ha senso solo nel contesto di un !OrdineFornitore [[BR]]
[#2 b] A seconda del GAS, la transizione !OrdineGasista NON_CONFERMATO -> CONFERMATO può avvenire automaticamente e in modo trasparente all'utente.[[BR]]
----

## Area logistica TODO TODOC

### Consegna
Indica il processo in cui un Fornitore consegna ad un GAS la merce relativa ad un [[#OrdineFornitore|OrdineFornitore]].
### !PuntoDiConsegna
È il luogo dove avviene una [[#Consegna|Consegna]].
### !AppuntamentoDiConsegna
Indica le modalità con cui avviene materialmente una [[#Consegna|Consegna]].  Uno stesso !AppuntamentoDiConsegna può essere relativo a più di un !OrdineFornitore (e spesso lo è).
È caratterizzato da:
* [[#PuntoDiConsegna|PuntoDiConsegna]]
* data
* ora
* [[#ReferenteConsegna|ReferenteConsegna]]
### Ritiro
Indica il processo in cui i Gasisti ritirano i Prodotti consegnati dai Fornitori, assistiti dal [[#Turnista|Turnista]].
### !PuntoDiRitiro
È il luogo dove avviene un [[#Ritiro|Ritiro]]; non coincide necessariamente con il !PuntoDiConsegna relativo allo stesso !OrdineFornitore.
### !AppuntamentoDiRitiro
Indica le modalità con cui avviene materialmente un [[#Ritiro|Ritiro]]. In generale, uno stesso !AppuntamentoDiRitiro è relativo a più di un !OrdineFornitore.
È caratterizzato da:
* [[#PuntoDiRitiro|PuntoDiRitiro]]
* data
* ora inizio
* ora fine
* [[#Turnista|Turnista]]/i
### Partita
La merce ritirabile dai Gasisti in occasione di un !AppuntamentoDiRitiro.
### Sede
Luogo in cui è ubicata la sede del GAS.
### Magazzino
Insieme dei Prodotti ordinati da un GAS per i quali non è pianificato il ritiro da parte di un Gasista specifico; è una lista di Giacenze.  Il Magazzino è il risultato di eventi del tipo:
* nell'ambito di un'!OrdineFornitore, il GAS ordina più Prodotti di quelli effettivamente richiesti dai Gasisti allo scopo di creare delle scorte
* nel corso di un appuntamento di Ritiro, un Gasista non preleva alcuni degli !OrdiniGasista che aveva effettuato
### Giacenza
Uno stock di Prodotti omogenenei, nella tipologia e nel prezzo, conservati nel Magazzino di un GAS. È caratterizzato dai seguenti attributi:
* Prodotto
* unità di Prodotto in giacenza
* prezzo (quello che il GAS ha effettivamente pagato al Fornitore per procurarsi i Prodotti presenti nella Giacenza)
### Prelievo
È l'atto con cui un Gasista preleva (una parte di) una Giacenza di Magazzino. È caratterizzato dai seguenti attributi:
* Gasista che effettua il prelievo
* data/ora del prelievo
* Giacenza da cui il Prelievo attinge
* unità di Prodotto prelevate
Un Prelievo può essere eseguito durante un normale Ritiro (ad es., se un Gasista ritira più di quello che ha ordinato) oppure in un altro momento (ad es. durante la riunione di un GAS).

## Area conti TODO TODOC

### Cassa

Conto fisico del GAS.

### Ricarica

Il Gasista da soldi al GAS per alimentare il !ContoGasista.

### Movimento totale del Sistema

Visualizza il totale delle transazioni economiche mensili ed annuali di un DES eventualmente diviso per categoria merceologica --> Statistiche
> Non mi sembra un concetto da introdurre a livello di Vocabolario, in quanto descrive un processo che andrebbe inserito nella opportuna pagina di Analisi

### Conto

Rappresenta la disponibilità economica (positiva o negativa) di uno dei Soggetti coinvolti nella gestione contabile di un GAS (nel linguaggio della contabilità a partita doppia, è un "account" o centro di costo/ricavo). È caratterizzato dai seguenti attributi:
* Soggetto titolare
* lista delle Transazioni associate
* saldo (disponibilità economica corrente)
All'interno di un GAS, i Conti che entrano in gioco sono di 3 tipi:
* [[#ContoGasista|ContoGasista]]
* [[#ContoGAS|ContoGAS]]
* [[#ContoFornitore|ContoFornitore]]

### !ContoGasista

Ogni Gasista ha il proprio; descrive il bilancio economico del Gasista nei confronti del GAS.
Gestione di cassa al livello di GAS. La cassa paga i Fornitore e altre spese. I gasisti ricaricano il loro Conto Gasista che finisce in Cassa.

### ContoGAS

È unico per ogni GAS; in sostanza, rappresenta la Cassa del GAS. Il saldo del Conto GAS è l'attuale disponibilità di cassa per il GAS.

### ContoFornitore

Ogni Fornitore che fornisce un GAS ha il proprio; descrive il bilancio economico del GAS nei confronti del Fornitore.

### Transazione

Movimento economico (flusso) tra due Conti. dei quali almeno uno gestito dal GAS. È caratterizzato dai seguenti attributi:
* Conto di partenza (se applicabile)
* Conto di arrivo (se applicabile)
* data/ora in cui la Transazione è stata eseguita
* causale (perché la Transazione è stata eseguita)
* importo economico (con segno) della Transazione

### Conto Totale Gas ###
Ad uso del  Contabile.

----

## Area ruoli

A livello implementativo e concettuale, la differenza tra Ruolo ed Entità è la seguente:

* un Entità è un'unità informativa all'interno del programma; può essere implementata come una classe, un oggetto, una tabella/record in un database,..
* un Ruolo è semplicemente un insieme di permessi operativi (i quali definiscono le azioni che un soggetto dotato di quel ruolo può eseguire all'interno del Sistema)

Di seguito sono descritti i ruoli previsti nel sistema:

### Il ruolo di Fornitore

**SUPPLIER**

È l'utente che gestisce la risorsa [Fornitore](#fornitore) in tutti i suoi aspetti dalla scheda anagrafica, al [Listino fornitore](#listino-fornitore), ad alcune opzioni di configurazione del Fornitore.

### Il ruolo di Referente informatico

**REFERRER_TECH**

È il Gasista che si occupa dell'amministrazione informatica dell'[Installazione](#installazione), limitatamente agli aspetti relativi al GAS di appartenenza.

### Il ruolo di Referente del patto

**REFERRER_SUPPLIER**

Funge da interfaccia tra un GAS e uno specifico Fornitore ed è responsabile del relativo !PattoDiSolidarietà

### Il ruolo di Referente dell'ordine

Gestisce un Ordine a livello di GAS
È scelto all'apertura di ogni ordine e modificabile fino alla chiusura tra i REFERRER_SUPPLIER e REFERRER_TECH

### Il ruolo di Referente dell'ordine di retina

Funge da interfaccia per un dato ordine tra una Retina di GAS ed un Fornitore in comune a tutti i GAS membri della Retina.
In Gasista Felice è il referente dell'ordine del GAS che ha aperto l'ordine di Retina.

### Il ruolo di Referente contabile

**REFERRER_CASH**

Gestisce i conti dei gasisti, dei GAS, e dei patti. Effettua le ricariche degli utenti nel GAS, il pagamento delle quote associative, il pagamento ai fornitori, redige il bilancio del GAS di fine anno.

### Referente di consegna

(NON USATO DAI GAS PER ORA, PARZ. IMPLEMENTATO, non rivista documentazione)

Un Gasista che si prende in carico gli aspetti logistici relativi ad un dato [[#AppuntamentoDiConsegna|AppuntamentoDiConsegna]], che possono comprendere:
* verifica della merce effettivamente consegnata dal/i Fornitore/i
* archiviazione dei DDT
* pagamento delle fatture
* trasporto della merce al [[#PuntoDiRitiro|PuntoDiRitiro]] (se diverso dal [[#PuntoDiConsegna|PuntoDiConsegna]])
* ..


### Turnista

(NON USATO DAI GAS PER ORA, PARZ. IMPLEMENTATO, non rivista documentazione)

Un Gasista che si prende in carico gli aspetti logistici relativi ad un dato [[#AppuntamentoDiRitiro|AppuntamentoDiRitiro]], che possono comprendere:
* gestione della corretta distribuzione della merce nel [[#PuntoDiRitiro|PuntoDiRitiro]]
* riscossione dei pagamenti da parte dei Gasisti
* rendicontazione dei Prodotti ritirati e di quelli non ritirati
* aggiornamento del [[#Magazzino|Magazzino]]
* ..

