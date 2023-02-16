# Ground Truth Service


Ground truth service is a interface between the Django server and client server for fetching the ground truth details from client system / database. example container details with permit number, containers list by with train number etc.

### Client integration Types:

1. Through SOAP Service (Real time fetch)
2. Through Oracle Database
3. Through Our Postgres Database


### Configuration and execution:
config file path: **atco-groundtruth/config.py**


**Run Ground truth service:**
1. Go to "atco-groundtruth"  folder
2. Install python dependencies $ make install
3. Run server $ make run

