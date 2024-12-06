#!/bin/sh

set -e

start_server=0
while getopts 's' OPTION; do
  case "$OPTION" in
    s)
      start_server=1
      ;;
    *)
      echo "Usage: $0 [-s] <outfile>"
      exit 1
      ;;
  esac
done
shift $(( OPTIND - 1 ))

outfile=$1

# Make sure the latest code is installed in python env.
flox activate -- make install

# Accept a parameter --start-server to start the server before sending the email.
if [ $start_server -eq 1 ]; then
  flox activate -- make webapp &
  trap 'kill %1' EXIT
  sleep 10 # Wait for the server to start.
fi

flox activate -- lcli report render --name default > "$outfile"
