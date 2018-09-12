#!/bin/bash

date

#for MUNI in \
 # CPT \
 # ETH \
 # JHB \
 # ; do
 # echo $MUNI
 # $HOME/openbylaws-saflii/fetch.py --target /data/home/saflii/raw/ZA${MUNI}ByLaws/ --regions za-$MUNI
#done

#for LEG in \
 # -LEGISLATION \
  #ETH \
  #JHB \
  #; do
  #echo $MUNI
  #/media/user/Data_1/saflii/home/alfred/legislation-import/openbylaws-saflii/fetch.py --target /media/user/Data_1/saflii/home/raw/ZA${LEG}/ 
#done


for REGION in ZA; do
  echo $REGION
  #$HOME/openbylaws-saflii/fetch.py --target /data/home/saflii/raw/${REGION}-acts/ --regions $REGION
  #/media/user/Data_1/saflii/home/alfred/legislation-saflii/fetch.py --target /media/user/Data_1/saflii/home/raw/${REGION}-legislation/ --regions $REGION/
 /home/gkempe/saflii-legislation/fetch.py --target /data/home/saflii/raw/${REGION}-legislation/ --regions $REGION/
  
done
