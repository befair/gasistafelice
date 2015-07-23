#! /bin/bash

#source /usr/local/bin/virtualenvwrapper.sh
#export WORKON_HOME=

#workon gasdev

if test -z "$DIR"
then
  DIR=/var/log
  if [ ! -d "$DIR" ]; then
     echo "ERROR: DIR is not set and $DIR does not exist. Exiting"
     exit 1
  fi
  echo "Warning: DIR is not set, assuming $DIR"
fi

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

PROF_LOG_DIR="$(settings_var 'PROFILE_LOG_BASE')"
if [ ! -d "$PROF_LOG_DIR" ]; then
  echo "ERROR: $PROF_LOG_DIR does not exist. Exiting"
  exit 1
fi

TAR_DIR=$DIR/profiles_gf

if ! [ -e "$TAR_DIR" ]; then
    mkdir $TAR_DIR
fi

DATE=`date +'%Y%m%d'`
TARGET_DIR=$TAR_DIR/$DATE

if ! [ -e "$TARGET_DIR" ]; then
    mkdir $TARGET_DIR
fi


for profile in $PROF_LOG_DIR/*
do
  if [[ $profile == *$DATE* ]] 
    then 
      mv $profile $TARGET_DIR;
  fi
done

#rotating tar files
#savelog $DIR/backup_gf.tar.gz

#tar file
tar cvzf $TAR_DIR/$DATE.tgz $TARGET_DIR 
