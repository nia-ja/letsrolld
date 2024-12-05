#!/bin/sh

set -e

FROMADDR=ihar.hrachyshka@gmail.com
TOADDRS=$FROMADDR

tmpdir=$(mktemp -d)
reportfile=$tmpdir/movies.report
./scripts/gen_report.sh -s "$reportfile"

mailsend-go -from $FROMADDR -t $TOADDRS -sub "Movies for $(date '+%Y-%m-%d')" \
  -use gmail auth -user $FROMADDR -pass "$(pass priv/google.com-mutt)" \
  body -file "$reportfile"

rm -r "$tmpdir"
