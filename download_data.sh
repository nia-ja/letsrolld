#!/bin/sh

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

unzip $DIR/letterboxd-export.zip -d $DIR/letterboxd-export
cp $DIR/letterboxd-export/watched.csv .
