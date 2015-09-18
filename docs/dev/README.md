# Gasista Felice development docs

## Overview

* **Base:** É l'app che contiene tutte le funzionalità di base estese da tutte le altre applicazioni. Organizza il sistema di gestione degli account.
* **Gas:** L'applicazione principale di Gasista Felice, qui vengono gestite principalmente le informazioni dei Gasisti (account, conti ecc.) e gli ordini ai fornitori. Core del progetto.
* **Supplier:** Contiene gli elementi per la gestione dei fornitori oltre ad informazioni su prodotti, fornitori e produttori.  Sistema di gestione dei fornitori del gas.
* **Des:** API per la gestione del DES e delle relazioni tra questo e altri soggetti economici. Controlla anche l'autenticazione degli utenti del DES.  Gestione dei rapporti tra i GAS nel DES.
* **Des_notification:** Tiene traccia ed informa sulle modifiche all'interno del DES.  Notifica cambiamenti nel DES.
* **Rest:** Interfaccia Utente. É composta da diversi blocchi, dove ogni blocco raggruppa funzionalità analoghe.
