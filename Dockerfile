FROM python:2.7.18-slim-stretch
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# old stretch is old
RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list
RUN apt-get update && apt-get --no-install-recommends install -y \
    git \
    libpq-dev \
    build-essential \
    locales
RUN echo "it_IT.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=it_IT.UTF-8
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
ENV LANG=it_IT.UTF-8 \
    LANGUAGE=it_IT.UTF-8 \
    LC_ALL=it_IT.UTF-8
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements/ /app/requirements/
# The following two lines are needed to install the git src modules in /src instead of /app/src
WORKDIR /
RUN pip install --no-cache-dir -r /app/requirements/prod.txt
WORKDIR /app
CMD ["/bin/bash"]
