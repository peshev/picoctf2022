#!/bin/bash

if ! sha256sum -c SHA256SUMS >/dev/null 2>/dev/null; then
  cat FILES | while read url; do
    curl -sO $url
  done
fi
if ! [ -f SHA256SUMS ]; then
  sha256sum $(cat FILES | while read url; do basename $url; done) >SHA256SUMS
else
  sha256sum -c SHA256SUMS >/dev/null || exit 1
fi
