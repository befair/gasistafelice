#!/bin/bash

# Questo script consente di caricare un virtualenv
# e posizionarsi nella cartella del progetto Gasista Felice

if [ -z "$2" ]; then
    echo "Usage $0 <project root> <virtualenv name>"
fi
PRJ_HOME=$1
VIRTUALENV=$2

# Check for WORKON_HOME envvar
if [ -z "$WORKON_HOME" ]; then
    WORKON_HOME=/var/lib/virtualenvs
    echo "Warning: WORKON_HOME environment variable is not set, assuming $WORKON_HOME"
fi

cd $WORKON_HOME
export WORKON_HOME

source /usr/bin/virtualenvwrapper.sh
workon $VIRTUALENV

