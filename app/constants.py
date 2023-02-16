
#Endpoints constants
UPLOAD_DATA_ENDPOINT ="/container_data"
CCLS_DATA_ENDPOINT ="/ccls_data"
TRAIN_DETAILS_ENDPOINT = "/train_details"
RAKE_UPLOAD_DATA_ENDPOINT = "/rake_data"
CONTAINER_DETAILS_ENDPOINT = "/container_details"
WAGON_DETAILS_ENDPOINT = "/wagon_details"
UPDATE_WTR_ENDPOINT = "/update_wtr"
WAREHOUSE_DATA_ENDPOINT = "/warehouse_details"
GROUND_TRUTH_TABLE_NAME = "Ground_truth"
ISO_6346_CODE_ENDPOINT = "/map_ccls_iso_code"

#time format in db:
TIME_FORMAT ="%Y-%m-%d %H:%M:%S"
#Keys
KEY_CN_NUMBER= "container_number"
KEY_PERMIT_NUMBER ="permit_number"
KEY_CRN_NUMBER= "crn_number"
KEY_RETRY="isRetry"
KEY_RETRY_VALUE = False
KEY_RETRY_COUNT=3
KEY_RETRY_TIMEDELAY=2
KEY_TIME = "TIME"
KEY_ID = "id"
KEY_ISO_CODE = "iso_code"
KEY_SLINE_CODE      = "sline_code" 
KEY_FROM_DATE = "from_date"
KEY_TO_DATE = "to_date"


#RABBIT_MQ QUEUES
BROKER_EXCHANGE='warehouse'
GATE_GT_REQUEST="GATE_GT_REQUEST"
GATE_GT_RESPONSE="GATE_GT_RESPONSE"
GATE_TRANSACTION="GATE_TRANSACTION"
BROKER_CONSUME_EXCHANGE='ground.truth.request'
BROKER_PUBLISH_EXCHANGE='ground.truth.response'
BROKER_EXCHANGE_TYPE='fanout'
BROKER_IP='10.60.62.42'
BROKER_PORT=5672
BROKER_USERNAME='whouse'
BROKER_PASSWORD='whouse'


#table keys
PERMIT_NUMBER       = "permit_no"
PERMIT_TYPE         = "permit_type"
CONTAINER_NUMBER    = "container_no"
VEHICLE_NUMBER      = "vehicle_no"
CTR_NO              = "ctr_no"
TRUCK_NUMBER        = "truck_no"
GT_TRUCK_NUMBER     = "gt_truck_no"
ISO_CODE            = "iso_code"
LINER_SEAL          = "liner_seal"
CUSTOM_SEAL         = "custom_seal"
REFEER_TEMPERATURE  = "reefer"
IS_EMPTY            = 'is_empty'
IS_EMPTY_OR_LADEN   = "is_empty_or_laden"
CARGO_TYPE          = "cargo_type"
POD                 = "POD"
PERMIT_DATE         = "permit_date"
PERMIT_EXPIRY_DATE  = "permit_expiry_date"
BILL_DETAILS        = "bill_details"
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
TRUCK_DETAILS       = "truck"
UN_NUMBER           = "un_number"
HAZARD              = "hazard"
SEALS               = "seals"
IS_DELETED          = "is_deleted"
TRUCK               = "truck"

#Rake table details
#CONTAINER_NUMBER    = "container_no"
CONTAINER_SIZE      = "container_size"
CONTAINER_TYPE      = "container_type"
CONTAINER_HEIGHT    = "container_height"
CONTAINER_STATUS    = "container_status"
CONTAINER_LIFE_NO   = "container_life_no"
HAZARD_STATUS       = "hazard_status"
DAMAGE_STATUS       = "damage_status"
HEALTH              = "health"
GATE_IN_TIME        = "gate_in_time"
SEAL_NUMBER         = "seal_no"
COMMIDITY           = "cargo_type"
DESTINATION_STATION = "destination_station"
TRAIN_NUMBER        = "train_number"
RAKE_NUMBER         = "rake_number"
WAGON_NUMBER        = "wagon_number"
WAGON_TYPE          = "wagon_types"
RAKE_TYPE           = "rake_type" #AR /DE
DATE_OF_DEPART      = "departure_date"
TRACK_NUMBER        = "track_number"
LDD_MT_FLAG         = "ldd_mt_flag"
WAGON_LIST          = "wagons_list"
CONTAINER_LIST      = "container_list"
RAKE_DETAILS        = "rake_details"
ARRIVAL             = "AR"
DEPARTURE           = "DE"
NUMBER              = "number"
VALUE               = "value"
UN_NUMBER           = "un_number"
HAZARD              = "hazard"
POD_CODE            = "pod_codes"
SLINE_CODE          = "sline_codes"
COMMIDITY_CODE      = "commodity_code"
COMMIDITY_TYPE      = "comm"
ACTY_TYPE           = "acty_type"
PORT_CODE           = "port_codes"
OUT_LOCATION        = "out_location"
OUT_PORT_LOCATION   = "out_port_location"
ICD_LOCATIONS       = "icd_loc"
USERS               = "users"
#container type mapping:

CONTAINER_LENGTH_ISO_MAPPING ={
    "20":"2",
    "40":"4"
}

CONTAINER_TYPE_ISO_MAPPING ={
    "GL":"2G1",
    "HQ":"5G1"
}

# As per BIC Standard https://www.bic-code.org/size-and-type-code/
ISO_CCLS_TYPE_MAPPING = {
    "G1":"GL",
    "P1":"PF",
    "T1":"TC",
    "U1":"OT",
    "R1":"RF"
}

ISO_CCLS_SIZE_MAPPING = {
    "2":"20",
    "4":"40",
    "L":"45",
    "M":"48"
}

# As per CCLS Format >=8.5 is N and <8.5 is H
ISO_CCLS_HEIGHT_MAPPING = {
    "2":"N",
    "5":"H"
}


# YARD master tables
CONTAINER_SIZE_TABLE = 'TM_CCTRSIZE'
SLINE_CODES = 'TM_CSLINE'
CONTAINER_TYPES = 'TM_CCTRTYPE'
PODS = 'TM_FPODCONV'
ICD_NAMES = 'TM_CRSTK'
STACK_LAYOUT = 'TM_CSTKLAYOUT'
CONTAINER_DETAILS = 'TM_CPHYCTRDTLS'
ACTIVITY_CODES = 'TM_CACTY'
EQUIPMENT_DETAILS = 'TM_CEQPTDTLS_NEW'

import enum
class GroundTruthType(enum.Enum):
    ORACLE = 0
    SOAP = 1
    POSTGRES = 2
    
