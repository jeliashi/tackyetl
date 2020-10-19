# Description

Simple ETL for scraping weather data from openweatherportal

# Installation

```
make install
```

# Testing

```
make test
```

# Usage

For downloading data:

```
tacky_get <LOCATION_ID> [--to_stdout] [--to_file <FILENAME>]
```
`LOCATION_ID` is the id for grabbing data
`--to_stdout` optional flag will pipe postproced data to stdout
`--to_file` optional flag with pipe postproced data to file `FILENAME`

For listing all meta data of scraped data

```
tacky_meta
```

For querying data

```
tacky_read <ID>
```
`ID` is the id to list the data. IDs can be viewed from `tacky_meta`
```
