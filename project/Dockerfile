# pull official base image
FROM python:3.10

RUN apt-get update && \
    apt-get -qq -y install  libxpm4 libxrender1 libgtk2.0-0 libnss3\
       libgconf-2-4  libpango1.0-0 libxss1 libxtst6 fonts-liberation\
       libappindicator1 xdg-utils

RUN apt-get -y install \
               xvfb gtk2-engines-pixbuf \
              xfonts-100dpi xfonts-75dpi xfonts-base xfonts-scalable \
               imagemagick x11-apps zip


RUN apt-get update && apt-get install -y wget unzip gcc && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ../requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
