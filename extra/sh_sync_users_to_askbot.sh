#!/bin/bash

# Put users from Gasista Felice and Askbot application

if [ -z "$GF_HOME" ]; then
    GF_HOME=/usr/local/gasistafelice
fi

if [ -z "$GF_VENV" ]; then
    GF_VENV=desmacerata
fi

ASKBOT_HOME=$GF_HOME/../extra/forum/
DUMPFILE=`mktemp`.json

for d in $GF_HOME $ASKBOT_HOME; do

    if [ ! -d "$d" ]; then
        echo "Directory $d does not exist! Aborting.";
        exit 100;
    fi

done

./sh_start_venv.sh $GF_HOME $GF_VENV

/usr/bin/env python $GF_HOME/manage.py dumpdata auth.User > $DUMPFILE
/bin/sed -i 's@"groups": \[4], "user_permissions": \[], @@g' $DUMPFILE

/usr/bin/env python $ASKBOT_HOME/manage.py loaddata $DUMPFILE

