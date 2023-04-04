import getpass
import os
from app.constants import GroundTruthType

BASE_DIR = os.path.dirname(__file__)
SQL_DIR =(os.path.join(BASE_DIR,'app','sql'))
WSDL_FILE = os.path.join(BASE_DIR,'GateWithEmptyTrailer.wsdl')

# Server config
IP_ADDRESS = '172.16.30.12'
PORT = '5000'
DEBUG = True
LOG_DIRECTORY_PATH = 'app/logs/'

#ORACLE DATABASE
SQL_DRIVER = "oracle"
SQL_USERNAME = "ccls_dev"
SQL_PASSOWRD = "Welcome123"
SQL_IP="10.60.62.140"
SQL_PORT = "1521"
SQL_DATABASE = "xe"
SQl_ECHO = False # Set false for production configuration

#POSTGRES_DATABASE
PSQL_DRIVER = "postgresql"
PSQL_USERNAME = "postgres"
PSQL_PASSOWRD = "Welcome123"
PSQL_IP="localhost"
PSQL_PORT = "5432"
PSQL_DATABASE = "ground_truth"
PSQl_ECHO = False # Set false for production configuration


#Ground truth config
IS_EVENT_BASED = True # set it is False for the real time fetch
CCLS_GROUND_TRUTH = True #set it true to get data from test oracle db
CONTAINERS_DATA_DIRECTORY = "containers_data" #folder  to listen for the new files
RAKE_DATA_DIRECTORY = 'rake_data'
GROUND_TRUTH = GroundTruthType.SOAP.value
WSDL_URL = "http://10.1.100.101:8001"

#logstash config
LOGSTASH_IP = '10.60.62.55'
LOGSTASH_PORT = 5044


#CCLS / other config details:
CLIENT_GROUND_TRUTH_END_POINT       = "http://127.0.0.1:5005/container_data"
CLIENT_RAKE_GROUND_TRUTH_END_POINT  = "http://127.0.0.1:5005/rake_data"
CLIENT_WAREHOUSE_GROUND_TRUTH_END_POINT = "http://127.0.0.1:5005/warehouse_data"

#gate ground truth keys
PERMIT_NUMBER       = "permit_no"
PERMIT_TYPE         = "permit_type"
CONTAINER_NUMBER   = "container_no"
TRUCK_NUMBER        = "truck_no"
GT_TRUCK_NUMBER     = "gt_truck_no"
ISO_CODE            = "iso_code"
LINER_SEAL          = "liner_seal"
REFEER_TEMPERATURE  = "reefer"
IS_EMPTY            = 'is_empty'
CUSTOM_SEAL         = "custom_seal"
CARGO_TYPE          = "cargo_type"
POD                 = "POD"
PERMIT_DATE         = "permit_date"
PERMIT_EXPIRY_DATE  = "permit_expiry_date"
BILL_NUMBER         = "bill_no"
BILL_TYPE           = "bill_type"
BILL_DATE           = "bill_date"
BILL_INFO           = "bill_info"
PERMIT_DETAILS      = "permit_details"
DRIVER_NAME         = "driver_name"
DRIVER_LICENSE      = "driver_license"
DRIVER_NUMBER       = "driver_number"
IS_ONE_DOOR_OPEN    = "is_one_door_open"
IS_RFID_SEAL        = "is_rfid_seal"

#rake ground truth keys
CONTAINER_NUM       = "CTR_NO"
CONTAINER_SIZE      = "CTR_SIZE"
CONTAINER_TYPE      = "CTR_TYPE"
CONTAINER_STATUS    = "CTR_STAT"
SEAL_NUMBER         = "SEAL_NO"
COMMIDITY           = "COMM_DESC"
DESTINATION_STATION = "DEST_STN"
RAKE_NUMBER         = "TRN_NO"
RAKE_TYPE           = "TRN_TYP"
WAGON_NUMBER        = "WGN_NO"
DATE_OF_DEPART      = "DT_DEP"
TRACK_NUMBER        = "TRK_NO"
LDD_MT_FLAG         = "LDD_MT_FLG"
R_LINER_SEAL        = "LINER_SEAL"
R_CUSTOM_SEAL       = "CUST_SEAL"
UN_NUMBER           = "UN_NUMBER"
HAZARD              = "HAZARD"


#IAM service
IAM_SERVICE_URL="http://10.60.62.137:8030"
VALIDATE_AUTH_END_POINT='/apiKey'
