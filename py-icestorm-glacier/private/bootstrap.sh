#!/bin/bash

wget -O- http://pike.esi.uclm.es/arco/key.asc | apt-key add -
echo "deb http://pike.esi.uclm.es/arco sid main" > /etc/apt/sources.list.d/pike.list
apt-get update
apt-get install -y zeroc-ice36-essential zeroc-ice36-services
