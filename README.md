# Countries Population Service

A Docker-based service that:

- Downloads and parses population data for all countries

- Stores raw (non-aggregated) country-level data in PostgreSQL

- Prints aggregated statistics per region using a single SQL query

- Supports multiple data sources with a parser-factory architecture.

## Features

- Asynchronous Python implementation

- Two data sources supported:

- Wikipedia

- StatisticsTimes

- Parser switching via environment variable

- Data stored unaggregated

- Aggregated output generated with ONE SQL query

- Docker Compose orchestration

- PostgreSQL automatically started with health checks

- Clean repository & modular design (parsers, repositories, models)

### Environment Setup
Before running the service, create a ```.env ```file:
```
cp .env.example .env
```

### Running the Service

```git clone <your_repo>``` \
```cd countries-population-service```

### Download and store data

```docker-compose up get_data``` 

This will:

- Start PostgreSQL

- Wait until it's healthy

- Fetch the HTML (or reuse cached file)

- Parse it

- Insert countries into the database

### Print region summary

```docker-compose up print_data```

Output example:

```
Region: South America
Total population: 438105376
Largest country in the region (population): Brazil
Largest population in there: 212812405
Smallest country in the region (population): Falkland Islands (Malvinas)
Smallest population in there: 3469
```

### Switching Data Source

```
SOURCE_URL=https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_%28United_Nations%29&oldid=1215058959
```
or:
```
SOURCE_URL=https://statisticstimes.com/demographics/countries-by-population.php
```
The parser factory automatically picks the correct class.

