FROM python:3.6.8
ENV PYTHONUNBUFFERED 1

RUN apt-get update --fix-missing
RUN apt-get install -y \
    python-pip \
    python-dev \
    libpq-dev \
    gettext \
    libreadline-dev \
    libssl-dev \
    libjpeg-dev \
    libfreetype6-dev \
    binutils \
    libproj-dev \
    gdal-bin \
    postgis

RUN mkdir /code
COPY . /code/
VOLUME /code

WORKDIR /code/

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements/docker.pip

RUN mkdir logs
CMD ["python3.6"]