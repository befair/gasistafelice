#!/bin/bash

if test -z "$DIR"
then
  DIR=/var/backups
  if [ ! -d "$DIR" ]; then
     echo "ERROR: DIR is not set and $DIR does not exist. Exiting"
     exit 1
  fi
  echo "Warning: DIR is not set, assuming $DIR"
fi

TAR_DIR=$DIR/backup_gf
META=$TAR_DIR/META
HASH=`git log --format=format:"%H" | head -1`
DATE=`date +%Y-%m-%d`

if ! [ -e "$TAR_DIR" ]; then
    mkdir $TAR_DIR
fi

#producing the META file
echo "Hash: $HASH" > $META
echo "Data: $DATE" >> $META

#dumping database basing on settings.py information
if test -z "$GF_HOME"
then
  GF_HOME=/usr/local/gasistafelice
  if [ ! -d "$GF_HOME" ]; then
     echo "ERROR: GF_HOME is not set and $GF_HOME does not exist. Exiting"
     exit 1
  fi
  echo "Warning: GF_HOME is not set, assuming $GF_HOME"
fi

cd $GF_HOME

export GF_HOME
export PYTHONPATH=$GF_HOME:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=gf.maintenance_settings

function settings_var {
  export name=$1
  (cd $GF_HOME; (echo "from settings import *"; echo "print $name" ) |python )
}

db_name="$(settings_var 'DATABASES["default"]["NAME"]')"
db_user="$(settings_var 'DATABASES["default"]["USER"]')"

pg_dump -U $db_user $db_name  > $TAR_DIR/backup_gf.dump

#rotating tar files
savelog $DIR/backup_gf.tar.gz

#tar file
tar cvzf $DIR/backup_gf.tgz $TAR_DIR 
