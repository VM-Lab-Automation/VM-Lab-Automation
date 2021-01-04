FROM debian:buster

#Install
RUN apt-get update &&\
 apt-get install -y gnupg wget

RUN wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | apt-key add - && \
 wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | apt-key add -

RUN wget https://releases.hashicorp.com/vagrant/2.2.7/vagrant_2.2.7_x86_64.deb && \
 dpkg -i vagrant_2.2.7_x86_64.deb

RUN echo "deb [arch=amd64] https://download.virtualbox.org/virtualbox/debian buster contrib" >> /etc/apt/sources.list && \
 apt-get update && \
 apt-get install -y virtualbox-6.1

RUN apt-get update && apt-get install apt-transport-https && apt-get install -y \
    procps \
    python3 \
    python3-pip \
    ca-certificates \
    curl \
    lxc \
    iptables \
    supervisor \
    git

RUN curl -sSL https://get.docker.com/ | sh

ADD image-files/wrapdocker /usr/local/bin/wrapdocker
ADD image-files/etc /etc
RUN chmod +x /usr/local/bin/wrapdocker

# Worker
COPY image-files/build-images.sh /usr/local/bin/build-images.sh
RUN chmod +x /usr/local/bin/build-images.sh
WORKDIR /app
COPY . .
RUN git clone https://github.com/narogm/LabTemplates.git vm
RUN mkdir labs
RUN python3 setup.py install
ENV FLASK_APP="worker.app"
ENV FLASK_ENV="development"
ENTRYPOINT supervisord && /usr/local/bin/build-images.sh && flask run --host=0.0.0.0 --port=8080 --no-reload

