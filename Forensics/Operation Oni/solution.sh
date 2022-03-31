#!/bin/bash

image=disk.img
image_url=https://artifacts.picoctf.net/c/373/$image.gz
if ! ([ -f $image ] || [ -f $image.gz ]); then
  wget -N -c $image_url
fi
if [ -f $image.gz ]; then
  gunzip $image.gz
fi

if [ -f $image.gz ]; then gunzip $image.gz; fi;
offset="$(fdisk -l $image | grep ${image}2 | awk '{ print $2 }')"
key_file="/$(fls -p -r -o $offset $image | grep .ssh/id_ | grep -v pub | awk '{ print $NF }')"
fcat -o $offset $key_file $image > key_file
chmod 600 key_file
ssh -i key_file -p 60643 ctf-player@saturn.picoctf.net cat flag.txt
echo
