# Gasista Felice development docs

Before contributing, see [beFair coding styleguide](http://docs.befair.it/doku.php?id=dev:coding-styleguide).

## Overview

* **Base:** É l'app che contiene tutte le funzionalità di base estese da tutte le altre applicazioni. Organizza il sistema di gestione degli account.
* **Gas:** L'applicazione principale di Gasista Felice, qui vengono gestite principalmente le informazioni dei Gasisti (account, conti ecc.) e gli ordini ai fornitori. Core del progetto.
* **Supplier:** Contiene gli elementi per la gestione dei fornitori oltre ad informazioni su prodotti, fornitori e produttori.  Sistema di gestione dei fornitori del gas.
* **Des:** API per la gestione del DES e delle relazioni tra questo e altri soggetti economici. Controlla anche l'autenticazione degli utenti del DES.  Gestione dei rapporti tra i GAS nel DES.
* **Des_notification:** Tiene traccia ed informa sulle modifiche all'interno del DES.  Notifica cambiamenti nel DES.
* **Rest:** Interfaccia Utente. É composta da diversi blocchi, dove ogni blocco raggruppa funzionalità analoghe.

## Routing

New:

    / -> /ui/index.html
    /ui       UI
    /api/v1   API

Old:

    /static
    /gasistafelice        UI
    /gasistafelice/rest   API
    /gasistafelice/admin  Django Admin

## Frontend dependencies

Frontend dependencies are defined in `ui/deps/bower.json`, and installed during
the build of the frontend image. Additional dependencies have to be added in
`ui/deps/bower.json`.

To locally install the new dependencies, the frontend image has to be rebuilt:

    $ make rebuild-front

This will delete test containers (they will be recreated the next time `make
test` is used), rebuild the frontend image with the new dependencies installed,
and finally recreate the `front` and `proxy` containers. After that the
application should be updated and available for use.

Once the changes to `ui/deps/bower.json` are merged in the upstream, a hook for
rebuilding the image will be triggered on the registry, and the developers will
be able to update their development images with:

    $ docker-compose pull

### Troubleshooting

If `npm` reports connection issues, restart the Docker daemon and repeat
the build. Additional informations can be found
[here](https://stackoverflow.com/questions/27992146/cant-install-npm-in-the-docker-container).

If the application doesn't work after the rebuild, remove and recreate all the
containers:

    $ make rm             # remove containers
    $ make up             # recreate the containers
    $ make dbtest         # reload the db
