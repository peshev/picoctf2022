#!/bin/bash

image=disk.flag.img
image_url=https://artifacts.picoctf.net/c/330/$image.gz
if ! ([ -f $image ] || [ -f $image.gz ]); then
  wget -N -c $image_url
fi
if [ -f $image.gz ]; then
  gunzip $image.gz
fi

offset="$(fdisk -l $image | grep ${image}3 | awk '{ print $2 }')"
flag_file="/$(fls -p -r -o "$offset" $image | grep flag | grep -v '*' | awk '{ print $NF }')"
fcat -o "$offset" "$flag_file" $image
