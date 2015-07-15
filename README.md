# Gasista Felice

## Quickstart

    $ git clone https://github.com/kobe25/gasistafelice && cd gasistafelice
    $ make up

Then you could use the test database:

    $ make dbtest

Or you could initialize an empty database:

    $ make dbinit

Now go on:

* [`localhost:8080/`](http://localhost:8080/) for UI
* [`localhost:8080/gasistafelice/`](http://localhost:8080/gasistafelice/) for old UI
* [`localhost:8080/gasistafelice/admin/`](http://localhost:8080/gasistafelice/admin/) for Django Admin UI

and login with `admin`/`admin`.

If you want to change any (default) configuration, please edit the `settings.env` file.

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

## Development

### Test

To launch all the tests:

    $ make test

Additionally, you can visualize the end-to-end tests running in the browsers via a VNC client:

- `localhost:5900` for Firefox
- `localhost:5901` for Chrome
