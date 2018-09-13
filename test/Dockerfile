FROM debian:stretch

RUN apt-get update \
    && apt-get install -y wget gnupg2

RUN wget -O- http://pike.esi.uclm.es/arco/key.asc | apt-key add - \
    && echo "deb http://pike.esi.uclm.es/arco sid main" > /etc/apt/sources.list.d/pike.list \
    && apt-get update \
    && apt-get install -y make g++ libdb5.3-java \
    && apt-get install -y zeroc-ice36 python3-zeroc-ice python-prego
