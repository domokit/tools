FROM ubuntu:14.04

MAINTAINER jamesr

RUN apt-get update && apt-get install -y \
	apache2 \
	bison \
	git \
	gperf \
	libapache2-mod-php5 \
	libcairo2-dev \
	libdbus-1-dev \
	libgconf2-dev \
	libgnome-keyring-dev \
	libgtk2.0-dev \
	libkrb5-dev \
	libnss3-dev \
	libpango1.0-0 \
	libpci-dev \
	libudev-dev \
	libxss-dev \
	libxtst-dev \
	openbox \
	python-dev \
	realpath \
	xvfb \
  && rm -rf /var/lib/apt/lists/*

RUN apt-get clean

RUN git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git

ENV PATH /depot_tools:$PATH

RUN mkdir /mojo

COPY .gclient /mojo/.gclient
COPY build.py /mojo/build.py
