import getpass
import os
from app.constants import GroundTruthType
from environs import Env

env = Env()
env.read_env()

BASE_DIR = os.path.dirname(__file__)
SQL_DIR =(os.path.join(BASE_DIR,'app','sql'))
WSDL_FILE = os.path.join(BASE_DIR,'GateWithEmptyTrailer.wsdl')

# Server config
IP_ADDRESS = env('IP_ADDRESS')
PORT = env('PORT')
DEBUG = env.bool('DEBUG')
LOG_DIRECTORY_PATH = 'app/logs/'

#ORACLE DATABASE
SQL_DRIVER = "oracle"
SQL_USERNAME = env('SQL_USERNAME')
SQL_PASSOWRD = env('SQL_PASSOWRD')
SQL_IP=env('SQL_IP')
SQL_PORT =env('SQL_PORT')
SQL_DATABASE =env('SQL_DATABASE')
SQl_ECHO = env.bool('SQl_ECHO') # Set false for production configuration

#POSTGRES_DATABASE
PSQL_DRIVER = "postgresql"
PSQL_USERNAME = env('PSQL_USERNAME')
PSQL_PASSOWRD = env('PSQL_PASSOWRD')
PSQL_IP=env('PSQL_IP')
PSQL_PORT = env('PSQL_PORT')
PSQL_DATABASE = env('PSQL_DATABASE')
PSQl_ECHO = env.bool('PSQl_ECHO') # Set false for production configuration


#Ground truth config
IS_EVENT_BASED = True # set it is False for the real time fetch
CCLS_GROUND_TRUTH = True #set it true to get data from test oracle db
CONTAINERS_DATA_DIRECTORY = "containers_data" #folder  to listen for the new files
RAKE_DATA_DIRECTORY = 'rake_data'
GROUND_TRUTH = GroundTruthType.SOAP.value
# WSDL_URL = "http://172.16.30.114:8007"
WSDL_URL = env('WSDL_URL')

#mock service
IS_MOCK_ENABLED=env.bool('IS_MOCK_ENABLED')

#logstash config
LOGSTASH_IP = env('LOGSTASH_IP')
LOGSTASH_PORT = env('LOGSTASH_PORT')


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
IAM_SERVICE_URL=env('IAM_SERVICE_URL')
VALIDATE_AUTH_END_POINT='/apiKey'
