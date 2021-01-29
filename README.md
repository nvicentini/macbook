# Landlord [WIP]

## the project.

It's a simple ETL.

## what it does.

- Extracts -> unconstructed land information published in MercadoLibre, available trough their API.
- Transforms -> saves specific information from Jsonline files into CSV files.
- Loads -> it populates a Postgres database for further analysis (coming soon).

## how to use it.
- sudo snap install docker
- clone this repositorie
- $ sudo docker-compose up
