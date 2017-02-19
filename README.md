# Jetscraper

A python3 tool for getting Jetstar AU CC transactions for budgeting.

`jetscrape -u <username> -p <password> -d <days> -f <outfile> -v`

Where:
- `days` is the number of days to retrieve, defaults to 31
- `outfile` is where to place the resulting .csv, defaults to stdout
- `-v` spit out debug logging, optional
