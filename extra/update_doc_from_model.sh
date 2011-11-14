#!/bin/bash

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
export DJANGO_SETTINGS_MODULE=settings


for model in supplier.ProductPU supplier.ProductMU supplier.ProductCategory supplier.Certification; do

    case $model in
        'supplier.ProductPU')
            tmpl="* \(%(symbol)s) %(name)s";
            docfile="../doc-user/source/autogen/list-product-units.txt"
            ;;
        'supplier.ProductMU')
            tmpl="* \(%(symbol)s) %(name)s";
            docfile="../doc-user/source/autogen/list-measure-units.txt"
            ;;
        'supplier.Certification')
            tmpl="* \(%(symbol)s) %(name)s";
            docfile="../doc-user/source/autogen/list-certifications.txt"
            ;;
        'supplier.ProductCategory')
            tmpl="* \(%(id)s) %(name)s";
            docfile="../doc-user/source/autogen/list-product-categories.txt"
            ;;
        *)
            tmpl="* \(%(pk)s) %(name)s";
            docfile="/tmp/t"
            echo "No output file provided for this model appending to $docfile"
            ;;
    esac

    /usr/bin/env python manage.py print_qs $model "$tmpl" | tee $docfile
    echo "UPDATEDOC for model $model in file $docfile DONE"
done


