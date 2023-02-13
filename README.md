# Ground Truth Service


Ground truth service is a interface between the Django server and client server for fetching the ground truth details from client system / database. example container details with permit number, containers list by with rake id etc.

It provides the synchronous and async communication to Django server for the ground truth details, for asynchronous communication used RabbitMQ broker.

### Client integration Types:

1. Event based : watching for the file(xlsx) in the specified directory. 
2. Real time fetch: Client API integration (Refer mock client server for more details)

**Client Gate Mock Application:**
Assuming client has their own database(xl file), and provided a API to get container details with Permit number, accordingly developed an mock client application.

### Configuration and execution:
config file path: **atco-back-end/micro_services/ground_truth/config.py**

Update server config (IP and Port)

**Gate:**

- Update config parameter  IS_EVENT_BASED to True and update CONTAINERS_DATA_DIRECTORY if client provided data in the file
- Update config parameter  IS_EVENT_BASED to False and update CLIENT_GROUND_TRUTH_END_POINT if Client given an API for container details
- Update client data filed names (provided xl file or client API )  in the "gate ground truth keys" section(eg CONTAINER_NUMBER="container_no")


**Rake:**

- Update config parameter  IS_EVENT_BASED to True and update CONTAINERS_DATA_DIRECTORY.  for listeing rake data events(xl files)
- Update client data filed names (provided xl file or client API )  in the "rake ground truth keys" section(Eg CONTAINER_NUMBER="container_no")

**Note**    If you want add data in the ground truth, provide data as xl sheet and palce the file in  CONTAINERS_DATA_DIRECTORY  path. (refer xl template in atco-back-end/micro_services/ground_truth/rake_data/ARRIVAL_RAKE_60_CN.xlsx)


**Run Ground truth service:**
1. Go to "atco-back-end/micro_services/ground_truth"  folder
2. Install python dependencies $ python3 -m pipenv install or $  python3 -m pipenv update
3. Activate virutal env  $ python3 -m pipenv shell
4. Run server $ python3 ground_truth.py

**Run Gate Client Mock Application:**
Go to "atco-back-end/micro_services/mock_services" and execute ccls_mock.py file