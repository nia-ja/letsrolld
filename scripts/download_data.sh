#!/bin/sh

set -e
set -x

COOKIE=$(cat cookie.txt)

DIR=data
mkdir -p $DIR

curl 'https://letterboxd.com/data/export/' \
  -H 'authority: letterboxd.com' \
  -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H "cookie: ${COOKIE}" \
  -H 'referer: https://letterboxd.com/settings/data/' \
  -H 'x-requested-with: XMLHttpRequest' \
  --compressed > $DIR/letterboxd-export.zip

unzip -o $DIR/letterboxd-export.zip -d $DIR
rm $DIR/letterboxd-export.zip
