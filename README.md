# Ground Truth Service


Ground truth service is a interface between the Django server and client server for fetching the ground truth details from client system / database. example container details with permit number, containers list by with train number etc.

### Client integration Types:

1. Through SOAP Service (Real time fetch)
2. Through Oracle Database
3. Through Our Postgres Database


### Configuration and execution:
config file path: **atco-groundtruth/config.py**

## configuration:
In config.py edit the following properties:

```

# Server config
IP_ADDRESS = 'SYSTEM IP'
PORT = 'SYSTEM PORT'   # on which port you want to run

#POSTGRES_DATABASE
PSQL_DRIVER = "postgresql"
PSQL_USERNAME = "DB USERNAME"
PSQL_PASSOWRD = "DB PASSWORD"
PSQL_IP="DB IP"
PSQL_PORT = "5432"
PSQL_DATABASE = "DB NAME"

#IAM service
IAM_SERVICE_URL="http://127.0.0.1:8030"

```
# create database in postgres

```

make reinstate-db

```

## setup:

```
make install
make run

```


**Run Ground truth service:**
1. Go to "atco-groundtruth"  folder
2. Install python dependencies $ make install
3. Run server $ make run

