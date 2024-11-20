#!/bin/sh

FROMADDR=ihar.hrachyshka@gmail.com
TOADDRS=$FROMADDR

REPORTFILE=movies.report

tmpdir=$(mktemp -d)
reportfile=$tmpdir/movies.report

lcli report render --name default > $reportfile
mailsend-go -from $FROMADDR -t $TOADDRS -sub "Movies for $(date '+%Y-%m-%d')" \
  -use gmail auth -user $FROMADDR -pass $(pass priv/google.com-mutt) \
  body -file $reportfile

rm -r $tmpdir
