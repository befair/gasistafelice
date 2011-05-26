#!/bin/bash

GF_HOME=~/src/gasistafelice/gasistafelice
DJANGO_HOME=/usr/lib/pymodules/python2.6/django
TEMPLATE_NAMES=$(rgrep "admin/base_site.html" $DJANGO_HOME/contrib/admin/templates/admin/ | cut -f1 -d':')

for t in $TEMPLATE_NAMES; do
   sed s@admin/base_site.html@gas_admin/base_site.html@g $t > $GF_HOME/gas_admin/templates/admin/$(basename $t)
done
