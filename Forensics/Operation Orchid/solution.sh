#!/bin/bash

image=disk.flag.img
image_url=https://artifacts.picoctf.net/c/236/$image.gz
if ! ([ -f $image ] || [ -f $image.gz ]); then
  wget -N -c $image_url
fi
if [ -f $image.gz ]; then
  gunzip $image.gz
fi

offset="$(fdisk -l $image | grep ${image}3 | awk '{ print $2 }')"
history_file="/$(fls -p -r -o $offset $image | grep .ash_history | awk '{ print $NF }')"
key="$(fcat -o $offset $history_file $image | grep "openssl aes256" | grep -oE -- "-k [^ ]+" | cut -d\  -f2)"
flag_enc_file="/$(fls -p -r -o $offset $image | grep flag.txt.enc | awk '{ print $NF }')"
fcat -o $offset $flag_enc_file $image | openssl aes256 -d -k $key 2>/dev/null
echo
