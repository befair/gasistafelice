FROM kobe25/uwsgi-python2:latest

MAINTAINER Antonio Esposito "kobe@befair.it"

ENV LC_ALL                  it_IT.UTF-8
ENV LANG                    it_IT.UTF-8
ENV LANGUAGE                it_IT.UTF-8

ENV PYTHONPATH              /code:/code/gasistafelice:/usr/local/lib/python2.7/site-packages
ENV UWSGI_CHDIR             /code/gasistafelice
ENV UWSGI_WSGI_FILE         /code/gasistafelice/gf/wsgi.py
ENV DJANGO_SETTINGS_MODULE  gf.settings
#ENV UWSGI_STATIC_MAP        /static/admin=/usr/local/lib/python2.7/site-packages/django/contrib/admin/static/admin
ENV UWSGI_STATIC_MAP        /static=/code/gasistafelice/static
ENV UWSGI_STATIC_SAFE       /usr/local/lib/python2.7/site-packages/django/contrib/admin/static/admin

COPY . /code/gasistafelice
COPY ./deps/locale.gen /etc/locale.gen

RUN apt update && \
    apt install -y $(cat /code/gasistafelice/deps/debian) && \
    rm -rf /var/lib/apt/lists/*
RUN locale-gen
RUN pip install -r /code/gasistafelice/deps/dev.txt

WORKDIR /code/gasistafelice
