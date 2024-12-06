#!/bin/sh

set -xe

if [ ! -f cookie.txt ]; then
  echo "Please create a cookie.txt file with the Letterboxd cookie"
  exit 1
fi

COOKIE=$(cat cookie.txt)

DIR=data

rm -rf $DIR
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
