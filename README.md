# Description
Python/Postgres Sample Project.
## Tested Environment:
- Python 3.8
- Postgres 12
- Ubuntu 20.04
- `plpython3u` Extension for Postgres
- `psycopg2`, `deep_translator` Python packages

## Assumptions:
- Dataset columns are fixed.
- Dataset file name is `dataset.csv`
- Postgres functions commited manually

## Install Dependencies:
### Install PL/Python package on Ubuntu:
```bash
	sudo apt-get install postgresql-plpython3-12
```
### Activate PL/Python extension for Target Database in Postgres:
```bash
	CREATE EXTENSION plpython3u
```
### Install Python dependencies:
```bash
	pip install psycopg2
	pip install deep_translator
```
## How to use:
### Configure Project:
1. Configure database config in `config,json`
2. Commit Postgres functions and trigger exists in `sql` directory
### Run Project:
```bash
	python3 ./main.py
```
### Debug Project at Runtime:
```bash
	tail -f ./debug.log
```
### Test Postgres Function:
for get number of people per sex of the given native country, execute this function with `native country` such as United-States:
```bash
	SELECT number_of_people( 'United-States' );
```
