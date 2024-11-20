#!/bin/sh

set -e

# Accept a parameter --start-server to start the server before sending the email.
if [ "$1" = "--start-server" ]; then
  flox activate -- make webapp &
  sleep 10 # Wait for the server to start.
fi

FROMADDR=ihar.hrachyshka@gmail.com
TOADDRS=$FROMADDR

tmpdir=$(mktemp -d)
reportfile=$tmpdir/movies.report

flox activate -- lcli report render --name default > "$reportfile"
mailsend-go -from $FROMADDR -t $TOADDRS -sub "Movies for $(date '+%Y-%m-%d')" \
  -use gmail auth -user $FROMADDR -pass "$(pass priv/google.com-mutt)" \
  body -file "$reportfile"

rm -r "$tmpdir"

kill %1
exit
