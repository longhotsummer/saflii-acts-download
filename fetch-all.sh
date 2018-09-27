#!/bin/bash

date

for REGION in ZA; do
  echo $REGION
  $HOME/saflii-legislation/fetch.py --target /data/home/saflii/raw/${REGION}-legislation/ --regions $REGION
done
