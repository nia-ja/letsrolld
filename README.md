Letsrolld, movie recommendation engine

Parses letterboxd html and uses undocumented GraphQL API for quickwatch. Use at
your peril.

## Usage

#. Add cookie.txt with Letterboxd authorized cookie.
#. Download data with `./scripts/download_data.sh`.
#. `pdm run recommend --config configs/default.json -d directors.csv`
