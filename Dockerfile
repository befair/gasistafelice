FROM python:2.7.18-slim-stretch
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# old stretch is old
RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list
ENV LANG=it_IT.UTF-8
ENV LANGUAGE=it_IT.UTF-8
ENV LC_ALL=it_IT.UTF-8
RUN apt-get update && apt-get --no-install-recommends install -y \
    git \
    libpq-dev \
    build-essential \
    locales \
    && rm -rf /var/lib/apt/lists/*
RUN locale-gen
RUN dpkg-reconfigure locales
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir -r requirements/prod.txt
COPY . /app/
WORKDIR /app/
CMD ["/bin/bash"]
