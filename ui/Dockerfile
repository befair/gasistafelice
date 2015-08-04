FROM iojs:2.4

MAINTAINER Antonio Esposito "kobe@befair.it"

RUN npm config set registry http://registry.npmjs.org/

COPY deps/npm /code/ui/deps/npm
RUN npm install -g $(cat /code/ui/deps/npm)

COPY ./bower.json /code/libs/bower.json
RUN cd /code/libs/ && bower install --allow-root

EXPOSE 5000

COPY ./ /code/ui/
WORKDIR /code/ui/

CMD ["harp", "server", "-i", "0.0.0.0", "-p", "5000", "/code"]
