
#Endpoints constants
UPLOAD_DATA_ENDPOINT ="/container_data"
CCLS_DATA_ENDPOINT ="/ccls_data"
UPDATE_CONTAINER_DETAILS_ENDPOINT = "/updateContainerInfo"
TRAIN_DETAILS_ENDPOINT = "/train_details"
PENDANCY_CONTAINERS_ENDPOINT = "/pendency_containers"
RAKE_PLAN_ENDPOINT = "/rake_plan"
RAKE_UPLOAD_DATA_ENDPOINT = "/rake_data"
CONTAINER_DETAILS_ENDPOINT = "/container_details"
WAGON_DETAILS_ENDPOINT = "/wagon_details"
UPDATE_INWARD_WTR_ENDPOINT = "/update_inward_rake"
UPDATE_OUTWARD_WTR_ENDPOINT = "/update_outward_rake"
UPDATE_WTR_ENDPOINT = "/update_wtr"
WAREHOUSE_DATA_ENDPOINT = "/warehouse_details"
STACK_LOCATION_ENDPOINT = "/stack_location"
GROUND_TRUTH_TABLE_NAME = "Ground_truth"
ISO_6346_CODE_ENDPOINT = "/map_ccls_iso_code"
TRACK_DETAILS = '/track_details'
CGI_SURVEY_ENDPOINT = '/cgi_survey'
CGO_SURVEY_ENDPOINT = '/cgo_survey'
VGI_SURVEY_ENDPOINT = '/vgi_survey'
RAKE_INWARD_CONTAINER_ENDPOINT = "/rake_inward_container"
WAGON_ENDPOINT = '/wagon'
GATEWAY_PORT_ENDPOINT = '/gateway_port'
UPDATE_RAKE_CONTAINER_ENDPOINT = '/update_rake_container'
CONTAINER_STAT_ENDPOINT = "/container_stat"
TRACK_MASTER_DATA_ENDPOINT = '/track_mstr_data'

#WSDL files
#GATE

EXIM_GATE_READ_WSDL =  "GateWithEmptyTrailer.wsdl"
EXIM_GATE_WRITE_WSDL = "EXIMGateWrite_02092023.wsdl"
# EXIM_GATE_READ_WSDL = "EXIMGateRead_01092023.wsdl"
# EXIM_GATE_READ_WSDL ="EXIMGateRead_02092023.wsdl"
DOM_GATE_READ_WSDL = "DOMGateRead_02092023.wsdl"
DOM_GATE_WRITE_WSDL = "DOMGateWrite_02092023.wsdl"


#RAKE
EXIM_RAKE_INWARD_READ_WSDL = "EXIMRakeInwardRead_02092023.wsdl"
EXIM_RAKE_INWARD_WRITE_WSDL = "EXIMRakeInwardWrite_02092023.wsdl"
EXIM_RAKE_OUTARD_WRITE_WSDL = "EXIMRakeOutwardWrite_02092023.wsdl"

#YARD
EXIM_YARD_WRITE_WSDL = "EXIMYardWrite_02092023.wsdl"
EXIM_LOADED_PENDANCY_WSDL = "EXIMRakeOutwardReadLoaded_02092023.wsdl"
EXIM_BLOCK_PENDANCY_WSDL = "EXIMRakeOutwardReadBlock_02092023.wsdl"
EXIM_EMPTY_PENDANCY_WSDL = "EXIMRakeOutwardReadEmpty_02092023.wsdl"
EXIM_EXPRESS_PENDANCY_WSDL = "EXIMRakeOutwardReadExpress_02092023.wsdl"


#time format in db:
TIME_FORMAT ="%Y-%m-%d %H:%M:%S"
#Keys
KEY_NUMBER = "number"
KEY_CN_NUMBER= "container_number"
KEY_CN_LIFE_NUMBER = "container_life_number"
KEY_TRANS_DATE = "trans_date"
KEY_TRANS_DELAY = "trans_delay"
KEY_PERMIT_NUMBER ="permit_number"
KEY_LANE_TYPE = "lane_type"
KEY_CRN_NUMBER= "crn_number"
KEY_RETRY="isRetry"
KEY_RETRY_VALUE = False
KEY_RETRY_COUNT=3
KEY_RETRY_TIMEDELAY=2
KEY_TIME = "TIME"
KEY_ID = "id"
KEY_FROM_DATE = "from_date"
KEY_TO_DATE = "to_date"
KEY_GATEWAY_PORT = "gateway_port"
KEY_PENDENCY_TYPE = "pendency_type"


# RAKE 
KEY_RAKE_ID = "rake_id"
RAKE_TX_TYPE = "trans_type" # EXIM/DOM
EXIM_RAKE    = "EXIM"
DOMESTIC_RAKE  = "DOM"
HYBRID_RAKE = "HYBRID"
KEY_TRAIN_NUMBER = 'train_number'
KEY_TRACK_NUMBER = "track_number"
KEY_RAKE_NUMBER = "rake_number"
KEY_IMP_EXP_FLG = 'imp_exp_flg'
KEY_FROM_LOC = 'from_loc'
KEY_TO_LOC = 'to_loc'
KEY_DT_ACTUAL_DEPART = "dt_actual_depart"
KEY_TOTAL_WAGON_CONT = 'total_wagon_count'
KEY_CURRENT_WAGON_COUNT = 'current_wagon_count'
KEY_NO_LOADED_TEU_DEPART = "no_loaded_teu_depart"
KEY_NO_EMPTY_TEU_DEPART = "no_empty_teu_depart"
KEY_NO_LOADED_TEU_ARRIVAL = "no_loaded_teu_arrival"
KEY_NO_EMPTY_TEU_ARRIVAL = "no_empty_teu_arrival"
KEY_CONTAINER_NUMBER = "container_number"
KEY_CONTAINER_LIFE_NUMBER = "container_life_number"
KEY_SLINE_CODE = "sline_code"
KEY_ISO_CODE = "iso_code"
KEY_CONTAINER_TYPE = "container_type"
KEY_CONTAINER_SIZE = "container_size"
KEY_CONTAINER_WEIGHT = "container_weight"
KEY_CONTAINER_STAT = "container_stat"
KEY_CARGO_TYPE = "cargo_type"
KEY_LDD_MT_FLG = "ldd_mt_flg"
KEY_FCL_LCL_FLG = "fcl_lcl_flg"
KEY_WAGON_NUMBER = "wagon_number"
KEY_WAGON_LIFE_NUMBER = "wagon_life_number"
KEY_WAGON_TYPE = "wagon_type"
KEY_DAMAGE_FLAG = "damage_flg"
KEY_PLACEMENT_REMARK = "placement_remark"
KEY_HLD_TRACK_NUMBER = "hld_track_number"
KEY_GATEWAY_PORT_CD =  "gateway_port_cd"
KEY_SEAL_NUMBER = "seal_number"
KEY_SEAL_STATUS = "seal_status"
KEY_DAMAGE_CODE = "damage_code"
KEY_HAZARD_STATUS = "hazard_status"
KEY_WAGON_DEST = "wagon_destination"
KEY_DT_PLACEMENT = "dt_placement"
KEY_EQUIPMENT_ID = "equipment_id"
KEY_EQUIPMENT_NAME = "equipment_name"
KEY_ATTRIBUTE1 = "attribute1"
KEY_ATTRIBUTE2 = "attribute2"
KEY_ATTRIBUTE3 = "attribute3"
KEY_ATTRIBUTE4 = "attribute4"
KEY_ATTRIBUTE5 = "attribute5"
KEY_ATTRIBUTE6 = "attribute6"
KEY_ATTRIBUTE7 = "attribute7"
KEY_CREATED_AT = "created_at"
KEY_CREATED_BY = "created_by"
KEY_UPDATED_AT = "updated_at"
KEY_UPDATED_BY = "updated_by"
KEY_ERROR_MSG = "error_msg"
KEY_STATUS_FLG = "status_flg"
KEY_READ_FLG = "read_flg"
KEY_DT_DESP = "dt_desp"
KEY_DT_WTR = "dt_wtr"
KEY_FIRST_POD = "first_pod"
KEY_ORIGIN_STATION = "origin_station"
KEY_DEST_STATION = "dest_station"
KEY_TRACK_ID = "track_id"
KEY_TRACK_NO = "track_no"

# RAKE SOAP KEYS
KEY_SOAP_TRAIN_NUMBER = 'trnNo'
KEY_SOAP_RAKE_NUMBER = "rakeNo"
KEY_SOAP_IMP_EXP_FLG = 'impExpFlg'
KEY_SOAP_FROM_LOC = 'frmLoc'
KEY_SOAP_TO_LOC = 'toLoc'
KEY_SOAP_DT_ACTUAL_DEPART = "dtActDep"
KEY_SOAP_TOTAL_WAGON_CONT = 'totWgnCnt'
KEY_SOAP_CURRENT_WAGON_COUNT = 'wgnCntCurr'
KEY_SOAP_NO_LOADED_TEU_DEPART = "noLddTeuDep"
KEY_SOAP_NO_EMPTY_TEU_DEPART = "noMtTeuDep"
KEY_SOAP_NO_LOADED_TEU_ARRIVAL = "noLddTeuArr"
KEY_SOAP_NO_EMPTY_TEU_ARRIVAL = "noMtTeuArr"
KEY_SOAP_CONTAINER_NUMBER = "ctrNo"
KEY_SOAP_CONTAINER_LIFE_NUMBER = "ctrLifeNo"
KEY_SOAP_SLINE_CODE = "slineCd"
KEY_SOAP_ISO_CODE = "ctrIsoCd"
KEY_SOAP_CONTAINER_TYPE = "ctrType"
KEY_SOAP_CONTAINER_SIZE = "ctrSize"
KEY_SOAP_CONTAINER_STAT = "ctrStat"
KEY_SOAP_CONTAINER_WEIGHT = "ctrWt"
KEY_SOAP_CARGO_TYPE = "crgType"
KEY_SOAP_LDD_MT_FLG = "lddMtFlg"
KEY_SOAP_FCL_LCL_FLG = "fclLclFlg"
KEY_SOAP_WAGON_NUMBER = "wgnNo"
KEY_SOAP_WAGON_LIFE_NUMBER = "wgnLifeNo"
KEY_SOAP_WAGON_TYPE = "wgnType"
KEY_SOAP_DAMAGE_FLAG = "dmgFlg"
KEY_SOAP_PLACEMENT_REMARK = "plcmtRmk"
KEY_SOAP_HLD_TRACK_NUMBER = "hldTrackNo"
KEY_SOAP_GATEWAY_PORT_CD =  "gwPortCd"
KEY_SOAP_SEAL_NUMBER = "sealNo"
KEY_SOAP_SEAL_STATUS = "sealStat"
KEY_SOAP_DAMAGE_CODE = "dmgCode"
KEY_SOAP_HAZARD_STATUS = "hazardiousStatus"
KEY_SOAP_WAGON_DEST = "wgnDestn"
KEY_SOAP_DT_PLACEMENT = "dtPlcmt"
KEY_SOAP_EQUIPMENT_ID = "eqptId"
KEY_SOAP_ATTRIBUTE1 = "attribute1"
KEY_SOAP_ATTRIBUTE2 = "attribute2"
KEY_SOAP_ATTRIBUTE3 = "attribute3"
KEY_SOAP_ATTRIBUTE4 = "attribute4"
KEY_SOAP_ATTRIBUTE5 = "attribute5"
KEY_SOAP_ATTRIBUTE6 = "attribute6"
KEY_SOAP_ATTRIBUTE7 = "attribute7"
KEY_SOAP_CREATED_AT = "createdDate"
KEY_SOAP_CREATED_BY = "createdBy"
KEY_SOAP_UPDATED_AT = "updatedDate"
KEY_SOAP_UPDATED_BY = "updatedBy"
KEY_SOAP_ERROR_MSG = "errorMsg"
KEY_SOAP_STATUS_FLG = "statusFlag"
KEY_SOAP_READ_FLG = "readFlag"
KEY_SOAP_DT_DESP = "dtDesp"
KEY_SOAP_DT_WTR = "dtWtr"
KEY_SOAP_FIRST_POD = "firPod"
KEY_SOAP_ORIGIN_STATION = "orgStn"
KEY_SOAP_DEST_STATION = "destStn"


#GATE SOAP KEYS:
KEY_SOAP_G_VEH_NO = "VEH_NO"
KEY_SOAP_G_DT_VEH_ARR = "DT_VEH_ARR"
KEY_SOAP_G_VEH_TYPE = "VEH_TYPE"
KEY_SOAP_G_DT_VEH_DEP = "DT_VEH_DEP"
KEY_SOAP_G_GT_DOC_NO = "GT_DOC_NO"
KEY_SOAP_G_DT_GT_DOC = "DT_GT_DOC"
KEY_SOAP_G_DT_GT_DOC_VLD = "DT_GT_DOC_VLD"
KEY_SOAP_G_TO_LOC = "TO_LOC"
KEY_SOAP_G_SEAL_STAT = "SEAL_STAT"
KEY_SOAP_G_SEAL_NO = "SEAL_NO"
KEY_SOAP_G_FAC_IN_TM = "FAC_IN_TM"
KEY_SOAP_G_FAC_OUT_TM = "FAC_OUT_TM"
KEY_SOAP_G_DMG_FLG = "DMG_FLG"
KEY_SOAP_G_DMG_CODE = "DMG_CODE"
KEY_SOAP_G_CTR_NO = "CTR_NO"
KEY_SOAP_G_CTR_SIZE = "CTR_SIZE"
KEY_SOAP_G_CTR_TYPE = "CTR_TYPE"
KEY_SOAP_G_CTR_STAT = "CTR_STAT"
KEY_SOAP_G_USER_ID = "USER_ID"
KEY_SOAP_G_SLINE_CD = "SLINE_CD"
KEY_SOAP_G_ARR_PMT_NO = "ARR_PMT_NO"
KEY_SOAP_G_DEP_PMT_NO = "DEP_PMT_NO"
KEY_SOAP_G_DOC_NO = "DOC_NO"
KEY_SOAP_G_XPMT_NO = "XPMT_NO"
KEY_SOAP_G_DT_XPMT_NO = "DT_XPMT_NO"
KEY_SOAP_G_GATE_NO = "GATE_NO"
KEY_SOAP_G_CTR_LIFE_NO = "CTR_LIFE_NO"
KEY_SOAP_G_DT_SEAL = "DT_SEAL"
KEY_SOAP_G_DT_ACTY = "DT_ACTY"
KEY_SOAP_G_ACTY_CD = "ACTY_CD"
KEY_SOAP_G_HAZ_FLG = "HAZ_FLG"
KEY_SOAP_G_STK_LOC = "STK_LOC"
KEY_SOAP_G_DT_ARR = "DT_ARR"
KEY_SOAP_G_DT_DEP = "DT_DEP"
KEY_SOAP_G_MODE_DEP = "MODE_DEP"
KEY_SOAP_G_MODE_ARR = "MODE_ARR"
KEY_SOAP_G_CREATED_DATE = "createdDate"
KEY_SOAP_G_CREATED_BY = "createdBy"
KEY_SOAP_G_UPDATED_DATE = "UPDATED_DATE"
KEY_SOAP_G_UPDATED_BY = "UPDATED_BY"
KEY_SOAP_G_ERROR_MSG = "ERROR_MSG"
KEY_SOAP_G_STATUS_FLAG = "STATUS_FLAG"
KEY_SOAP_G_IN_OUT_FLAG = "IN_OUT_FLAG"
KEY_SOAP_G_EXCEPTION_FLAG = "EXCEPTION_FLAG"
KEY_SOAP_G_EXCEPTION_ERROR = "EXCEPTION_ERROR"
KEY_SOAP_G_ATTRIBUTE1 = "attribute1"
KEY_SOAP_G_ATTRIBUTE2 = "attribute2"
KEY_SOAP_G_ATTRIBUTE3 = "attribute3"
KEY_SOAP_G_ATTRIBUTE4 = "attribute4"
KEY_SOAP_G_ATTRIBUTE5 = "attribute5"
KEY_SOAP_G_ATTRIBUTE6 = "attribute6"
KEY_SOAP_G_ATTRIBUTE7 = "attribute7"
KEY_SOAP_G_ATTRIBUTE8 = "attribute8"
KEY_SOAP_G_ATTRIBUTE9 = "attribute9"
KEY_SOAP_G_ATTRIBUTE10 = "attribute10"
# Domestic Gate
KEY_SOAP_G_DTMS_GATEPASS_NUMER = 'davgpnumb'
KEY_SOAP_G_DTMS_VEH_NUMBER = 'davvhclnumb'
KEY_SOAP_G_DTMS_CTR_IN_OUT_FLAG = 'dacinoutfalg'
KEY_SOAP_G_DTMS_IN_OUT_TIMEIN = 'dadinouttimeIn'
KEY_SOAP_G_DTMS_IN_OUT_TIMEOUT = 'dadinouttimeOut'
KEY_SOAP_G_DTMS_CARGO_CONTAINER_FLAG = 'daccrgocntrflag'
KEY_SOAP_G_DTMS_CTR_NUMBER = 'daccntrnumb'
KEY_SOAP_G_DTMS_CTR_SIZE = 'dancntrsize'
KEY_SOAP_G_DTMS_HAZARD_STATUS = 'hazardiousStatus'
KEY_SOAP_G_DTMS_CTR_TYPE = 'daccntrtype'
KEY_SOAP_G_DTMS_DAMAGE_STATUS = 'damageStatus'
KEY_SOAP_G_DTMS_CTR_LDD_EMPTY_FLAG = 'dacleflag'
KEY_SOAP_G_DTMS_CARGO_LDD_EMPTY_FLAG_VEH = 'dacleflagVhcl'
KEY_SOAP_G_DTMS_FACTORY_IN_TIME = 'dadfactintime'
KEY_SOAP_G_DTMS_FACTORY_OUT_TIME = 'dadfactouttime'
KEY_SOAP_G_DTMS_FACTORY_REACH_TIME = 'dadfactreachtime'
KEY_SOAP_G_DTMS_USER_ID = 'davuserid'
KEY_SOAP_G_DTMS_REASON_CODE = 'dacresncode'




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
RAKE_ID             = "rake_id"
CONTAINER_SIZE      = "container_size"
CONTAINER_TYPE      = "container_type"
CONTAINER_HEIGHT    = "container_height"
CONTAINER_STAT      = "container_stat"
CONTAINER_LIFE_NO   = "container_life_no"
CATEGORY            = "category"
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

rake_write_required_fields = [KEY_TRAIN_NUMBER,KEY_CONTAINER_NUMBER,KEY_CONTAINER_LIFE_NUMBER,KEY_SLINE_CODE,
                            KEY_CONTAINER_SIZE,KEY_CONTAINER_TYPE,KEY_FCL_LCL_FLG,KEY_WAGON_NUMBER,
                            KEY_WAGON_LIFE_NUMBER,KEY_DAMAGE_FLAG,SEAL_NUMBER,HAZARD_STATUS]  
    
