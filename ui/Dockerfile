FROM iojs:2.3

MAINTAINER Antonio Esposito "kobe@befair.it"

COPY . /code/ui
COPY ./bower.json /code/libs/bower.json

RUN npm install -g $(cat /code/ui/deps/npm)
RUN cd /code/libs && bower install --allow-root

WORKDIR /code/ui
EXPOSE 5000
CMD ["harp", "server", "-i", "0.0.0.0", "-p", "5000", "/code"]
