FROM n42org/tox
MAINTAINER Matías Aguirre <matiasaguirre@gmail.com>
RUN apt-get update
RUN apt-get install -y make libssl-dev libxml2-dev libxmlsec1-dev mongodb-server mongodb-dev swig openssl
RUN ln -s /usr/include/x86_64-linux-gnu/openssl/opensslconf.h /usr/include/openssl/opensslconf.h
