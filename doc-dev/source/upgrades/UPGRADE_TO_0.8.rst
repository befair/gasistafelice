
Aggiornare dalla 0.7 alla 0.8
=============================

Oltre a sincronizzare il proprio codice sorgente con 
https://github.com/feroda/gasistafelice

# git clone https://github.com/feroda/gasistafelice.git

nell'aggiornamento a questa versione è necessario:

1. Aggiornare il sottomodulo django-simple-accounting

Aggiornare il sottomodulo django-simple-accounting
--------------------------------------------------

# git submodule update --init
# cd submodules/django-simple-accounting

Verificare di essere nel branch *master*

# git branch
* master

Installare il sottomodulo

# python setup.py install

Verificare che sia installato il nuovo modulo
(metodo artigianale)

# python
>>> import simple_accounting
>>> simple_accounting.__file__
(posizione del file __init__.pyc)
>>> CTRL+D

# ls -l submodules/django-simple-accounting/simple_accounting/models.py (directory trovata prima)/models.py
e verificare che la dimensione sia la stessa

o meglio

# md5sum submodules/django-simple-accounting/simple_accounting/models.py (directory trovata prima)/models.py
e verificare che l'hash sia lo stesso

Se non sono gli stessi fare:

# rm -rf (directory trovata prima)/

e ripetere l'operazione lanciando la shell python (da "# python")

Buon divertimento!
Luca `fero` Ferroni
