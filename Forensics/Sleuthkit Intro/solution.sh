#!/bin/bash

image=disk.img
image_url=https://artifacts.picoctf.net/c/114/$image.gz
if ! ([ -f $image ] || [ -f $image.gz ]); then
  wget -N -c $image_url
fi
if [ -f $image.gz ]; then
  gunzip $image.gz
fi

fdisk -l $image | grep ${image}1 | awk '{ print $5 }' | nc saturn.picoctf.net 52279 | grep pico
