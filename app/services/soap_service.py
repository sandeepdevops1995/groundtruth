import os
import zeep
import config
from datetime import datetime
from app import constants as Constants
from app.models import CCLSRake
from app import postgres_db as db
from app.logger import logger
from app.services.rake.gt_upload_service import commit,save_in_diagnostics
from app.models.utils import db_format
from app.enums import EquipmentNames
import json
from zeep.transports import Transport
import xmltodict
import redis
from app.redis_config import cache
transport = Transport(timeout=10)
pendancy_transport = Transport(timeout=20)

def get_zeep_wsdl_client(file_name):
    wsdl_file = os.path.join(config.WSDL_DIR,file_name)
    return zeep.Client(wsdl_file)

def get_permit_details(permit_number):
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/EmpltyTrailer/emptytrailerbpel_client_ep?WSDL"
    
    try:
        # soap = zeep.Client(wsdl=wsdl_url, 
        #                 service_name="emptytrailerbpel_client_ep",
        #                 port_name="EmptyTrailerBPEL_pt")
        # soap = zeep.Client(config.WSDL_FILE,transport=transport)
        # logger.debug('Get Permit, soap service request with permit_number ( EXIM ) : '+permit_number)
        # start_time = datetime.now()
        # result = soap.service.process(permit_number)
        # end_time = datetime.now()
        # save_in_diagnostics(Constants.CCLS_DATA_ENDPOINT+ " (EXIM) ",{"permit_number":permit_number},{"output":str(result)},start_time,end_time)
        # logger.debug('Get Permit, soap service response ( EXIM ) : '+str(result))
        
        soap = zeep.Client(config.WSDL_FILE,transport=transport)
        logger.debug('Get Permit, soap service request with permit_number ( EXIM ) : '+permit_number)
        result = {}
        with soap.settings(raw_response=True):
            start_time = datetime.now()
            soap_res = soap.service.process(permit_number)
            end_time = datetime.now()
            data = xmltodict.parse(soap_res.text)
            result = json.loads(json.dumps(data, indent=3))
        if result and 'env:Envelope' in result and 'env:Body' in result['env:Envelope'] and 'EmptyTrailerOutput' in result['env:Envelope']['env:Body']:
            result = result['env:Envelope']['env:Body']['EmptyTrailerOutput']
            result.pop('@xmlns')
            result['DamageStatus'] = None
            result['VehicleGateInDateTime'] = None
            for a in result:
                if isinstance(result[a],dict):
                    result[a] = None
            # save in diagnostice
            save_in_diagnostics(Constants.CCLS_DATA_ENDPOINT+ " (EXIM) ",{"permit_number":permit_number},{"output":str(result)},start_time,end_time)
        logger.debug('Get Permit, soap service response ( EXIM ) : '+str(result))
    except Exception as e:
        logger.exception('Get Permit, Exception ( EXIM ) : '+str(e))
        # failed_data = {
        #     "method_name":"get_permit_details",
        #     "request_data":{
        #         "permit_number":permit_number
        #     }
        # }
        # failed_data=json.dumps(failed_data, default=str)
        # cache.rpush("ground_truth_queue",failed_data)
        # logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = {}
    return result

def get_domestic_permit_details(permit_number):
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/DTMSGateAPIRead/dtmsgatereadbpel_client_ep?WSDL"
    try:
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="dtmsgatereadbpel_client_ep",
                        port_name="DTMSGateReadBPEL_pt",transport=transport)
        logger.debug('Get Permit, soap service request with permit_number ( DOM ) : '+permit_number)
        start_time = datetime.now()
        result = soap.service.process(permit_number)
        end_time = datetime.now()
        save_in_diagnostics(Constants.CCLS_DATA_ENDPOINT+ " (DOM) ",{"permit_number":permit_number},{"output":str(result)},start_time,end_time)
        logger.debug('Get Permit, soap service response ( DOM ) : '+str(result))
    except Exception as e:
        logger.exception('Get Permit, Exception ( DOM ) : '+str(e))
        # failed_data = {
        #     "method_name":"get_domestic_permit_details",
        #     "request_data":{
        #         "permit_number":permit_number
        #     }
        # }
        # failed_data=json.dumps(failed_data, default=str)
        # cache.rpush("ground_truth_queue",failed_data)
        # logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = {}
    return result

def update_exim_container_details(update_data):
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/GateWriteOperation/gatewriteoperation_client_ep?WSDL"
    try:      
        logger.debug('Update EXIM Container Details, soap service request with data : '+ str(update_data))
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="gatewriteoperation_client_ep",
                        port_name="GateWriteOperation_pt",transport=transport)
        
        start_time = datetime.now()
        result = soap.service.process(**update_data)
        end_time = datetime.now()
        save_in_diagnostics(Constants.UPDATE_CONTAINER_DETAILS_ENDPOINT,{"data":str(update_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Update EXIM Container Details, soap service response : '+ str(result))
        
    except Exception as e:
        logger.exception('Update EXIM Container Details, Exception : '+str(e))
        failed_data = {
            "method_name":"update_exim_container_details",
            "request_data":{
                "update_data":update_data
            }
        }
        failed_data=json.dumps(failed_data, default=str)
        cache.rpush("ground_truth_queue",failed_data)
        logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = {}
    return result

def update_domestic_container_details(update_data):
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/DTMSGateWriteProcess/dtmswritebpel_client_ep?WSDL"
    try:      
        logger.debug('Update Domestic Container Details, soap service request with data : '+ str(update_data))
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="dtmswritebpel_client_ep",
                        port_name="DTMSWriteBPEL_pt",transport=transport)
        
        start_time = datetime.now()
        result = soap.service.process(**update_data)
        end_time = datetime.now()
        save_in_diagnostics(Constants.UPDATE_CONTAINER_DETAILS_ENDPOINT,{"data":str(update_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Update Domestic Container Details, soap service response : '+ str(result))
        
    except Exception as e:
        logger.exception('Update Domestic Container Details, Exception : '+str(e))
        failed_data = {
            "method_name":"update_domestic_container_details",
            "request_data":{
                "update_data":update_data
            }
        }
        failed_data=json.dumps(failed_data, default=str)
        cache.rpush("ground_truth_queue",failed_data)
        logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = {}
    return result

def get_exim_train_details(train_number='',from_date='', to_date = ''):
    try:
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/RakeReadOperation/rakereadproocess_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="rakereadproocess_client_ep",
                        port_name="RakeReadProocess_pt",transport=transport)
        rake_data = {'TrainNumber': train_number, 'From': from_date,'To':to_date }
        logger.debug('Get EXIM Train Details, soap service request with data : '+ str(rake_data))
        start_time = datetime.now()
        result = soap.service.process(**rake_data)
        end_time = datetime.now()
        save_in_diagnostics(Constants.TRAIN_DETAILS_ENDPOINT,{"data":str(rake_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Get EXIM Train Details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Get EXIM Train Details, Exception : '+str(e))
        # failed_data = {
        #     "method_name":"get_exim_train_details",
        #     "request_data":{
        #         "train_number":train_number,
        #         "from_date":from_date,
        #         "to_date":to_date
        #     }
        # }
        # failed_data=json.dumps(failed_data, default=str)
        # cache.rpush("ground_truth_queue",failed_data)
        # logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = []
        return result
    
def get_domestic_train_details(train_number='',from_date='', to_date = ''):
    try:
        #wsdl_url = config.WSDL_URL+'/soa-infra/services/default/DTMSRakeInwardProcess/dtmsrakeinwardapi_client_ep?WSDL'
        wsdl_url = "http://10.1.100.102:8001/soa-infra/services/default/DTMSRakeInwardProcess/dtmsrakeinwardapi_client_ep?WSDL"
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="dtmsrakeinwardapi_client_ep",
                        port_name="DTMSRakeInwardAPI_pt",transport=transport)
        rake_data = {'TrainNumber': train_number, 'From': from_date,'To':to_date }
        logger.debug('Get Domestic Train Details, soap service request with data : '+ str(rake_data))
        start_time = datetime.now()
        result = soap.service.process(**rake_data)
        end_time = datetime.now()
        save_in_diagnostics(Constants.TRAIN_DETAILS_ENDPOINT,{"data":str(rake_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Get Domestic Train Details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Get Domestic Train Details, Exception : '+str(e))
        # failed_data = {
        #     "method_name":"get_domestic_train_details",
        #     "request_data":{
        #         "train_number":train_number,
        #         "from_date":from_date,
        #         "to_date":to_date
        #     }
        # }
        # failed_data=json.dumps(failed_data, default=str)
        # cache.rpush("ground_truth_queue",failed_data)
        # logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = []
        return result
    

def update_inward_rake(rake_data,api_url="Inward Write"):
    try: 
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/RakeInwardWriteOperation/rakewriteinward_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="rakewriteinward_client_ep",
                        port_name="RakeWriteInward_pt",transport=transport)
        logger.debug('Update Inward Rake Details, soap service request with data : '+ str(rake_data))
        start_time = datetime.now()
        result = soap.service.process(**rake_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(rake_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Update Inward Rake Details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Update Inward Rake Details, Exception : '+str(e))
        failed_data = {
            "method_name":"update_inward_rake",
            "request_data":{
                "rake_data":rake_data
            }
        }
        failed_data=json.dumps(failed_data, default=str)
        cache.rpush("ground_truth_queue",failed_data)
        logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = {}
        return result

def update_domestic_inward_rake(rake_data,api_url="DOM Yard INWARD Write"):
    result = []
    try:
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/DTMSRakeWrite/dtmsrakewrite_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="dtmsrakewrite_client_ep",
                        port_name="DTMSRakeWrite_pt")
        logger.debug('Update DOM Inward Rake Details, soap service request with data : '+ str(rake_data))
        start_time = datetime.now()
        result = soap.service.process(**rake_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(rake_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Update DOM Inward Rake Details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Update DOM Inward rake details, Exception : '+str(e))
        failed_data = {
            "method_name":"update_domestic_inward_rake",
            "request_data":{
                "rake_data":rake_data
            }
        }
        failed_data=json.dumps(failed_data, default=str)
        cache.rpush("ground_truth_queue",failed_data)
        logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        return result
    
def get_pendancy_details(gateway_port_data,api_url="/pendency_containers"):
    try: 
        
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/CCLSRakePendencyList/cclsrakependencybpel_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url,
                        service_name="cclsrakependencybpel_client_ep",
                        port_name="CCLSRakePendencyBPEL_pt",transport=pendancy_transport)
        start_time = datetime.now()
        result = soap.service.process(**gateway_port_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(gateway_port_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Get LOADED pendancy container details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Get LOADED pendancy container details, Exception : '+str(e))
        # failed_data = {
        #     "method_name":"get_pendancy_details",
        #     "request_data":{
        #         "gateway_port_data":gateway_port_data
        #     }
        # }
        # failed_data=json.dumps(failed_data, default=str)
        # cache.rpush("ground_truth_queue",failed_data)
        # logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = []
        return result

def get_empty_pendancy_details(gateway_port_data,api_url="/pendency_containers"):
    try: 
        result = []        
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/CCLSRakeEmptyPendency/cclsrakeemptypendencybpel_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, service_name="cclsrakeemptypendencybpel_client_ep", port_name="CCLSRakeEmptyPendencyBPEL_pt",transport=pendancy_transport)
        start_time = datetime.now()
        result = soap.service.process(**gateway_port_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(gateway_port_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Get EMPTY pendancy container details, soap service response : '+ str(result))
        
        return result
    except Exception as e:
        logger.exception('Get EMPTY pendancy container details, Exception : '+str(e))
        # failed_data = {
        #     "method_name":"get_empty_pendancy_details",
        #     "request_data":{
        #         "gateway_port_data":gateway_port_data
        #     }
        # }
        # failed_data=json.dumps(failed_data, default=str)
        # cache.rpush("ground_truth_queue",failed_data)
        # logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = []
        return result

def get_block_pendancy_details(gateway_port_data,api_url="/pendency_containers"):
    try: 
        result = []        
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/CCLSRakeBlockPendncy/cclsblockpendencybpel_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, service_name="cclsblockpendencybpel_client_ep", port_name="CCLSBlockpendencyBpel_pt",transport=pendancy_transport)
        start_time = datetime.now()
        result = soap.service.process(**gateway_port_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(gateway_port_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Get BLOCK pendancy container details, soap service response : '+ str(result))
        
        return result
    except Exception as e:
        logger.exception('Get BLOCK pendancy container details, Exception : '+str(e))
        # failed_data = {
        #     "method_name":"get_block_pendancy_details",
        #     "request_data":{
        #         "gateway_port_data":gateway_port_data
        #     }
        # }
        # failed_data=json.dumps(failed_data, default=str)
        # cache.rpush("ground_truth_queue",failed_data)
        # logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = []
        return result

def get_express_pendancy_details(gateway_port_data,api_url="/pendency_containers"):
    try: 
        result = []        
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/CCLSRakeExpressPendency/expressbpel_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, service_name="expressbpel_client_ep", port_name="ExpressBpel_pt",transport=pendancy_transport)
        start_time = datetime.now()
        result = soap.service.process(**gateway_port_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(gateway_port_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Get EXPRESS pendancy container details, soap service response : '+ str(result))
        
        return result
    except Exception as e:
        logger.exception('Get EXPRESS pendancy container details, Exception : '+str(e))
        # failed_data = {
        #     "method_name":"get_express_pendancy_details",
        #     "request_data":{
        #         "gateway_port_data":gateway_port_data
        #     }
        # }
        # failed_data=json.dumps(failed_data, default=str)
        # cache.rpush("ground_truth_queue",failed_data)
        # logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = []
        return result
 
def get_domestic_outward_train_details(rake_data,api_url="/pendency_containers(DOM)"):
    result = []
    try:
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/DTMSRakeOutwardProcess/dtmsrakeoutwardprocess_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="dtmsrakeoutwardprocess_client_ep",
                        port_name="DTMSRakeOutwardProcess_pt")
        logger.debug('Get DOM Outward Rake details, soap service request with data : '+ str(rake_data))
        start_time = datetime.now()
        result = soap.service.process(**rake_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(rake_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Get DOM Outward Rake details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Get DOM Outward Rake  train details, Exception : '+str(e))
        # failed_data = {
        #     "method_name":"get_domestic_outward_train_details",
        #     "request_data":{
        #         "rake_data":rake_data
        #     }
        # }
        # failed_data=json.dumps(failed_data, default=str)
        # cache.rpush("ground_truth_queue",failed_data)
        # logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        return result


def update_outward_rake(rake_data,api_url="EXIM Yard Outward Write"):
    try: 
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/RakeOutwardWriteOperation/rakeoutwardwrite_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="rakeoutwardwrite_client_ep",
                        port_name="RakeOutwardWrite_pt",transport=transport)
        logger.debug('Update EXIM Outward Rake Details, soap service request with data : '+ str(rake_data))
        start_time = datetime.now()
        result = soap.service.process(**rake_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(rake_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Update EXIM Outward Rake Details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Update EXIM Outward Rake Details, Exception : '+str(e))
        failed_data = {
            "method_name":"update_outward_rake",
            "request_data":{
                "rake_data":rake_data
            }
        }
        failed_data=json.dumps(failed_data, default=str)
        cache.rpush("ground_truth_queue",failed_data)
        logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = {}
        return result          

def update_domestic_outward_rake(rake_data,api_url="DOM Yard Outward Write"):
    try:
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/DTMSRakeWrite/dtmsrakewrite_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="dtmsrakewrite_client_ep",
                        port_name="DTMSRakeWrite_pt")
        logger.debug('Update DOM Outward Rake Details, soap service request with data : '+ str(rake_data))
        start_time = datetime.now()
        result = soap.service.process(**rake_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(rake_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Update DOM Outward Rake Details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Update DOM Domestic outward rake details, Exception : '+str(e))
        failed_data = {
            "method_name":"update_domestic_outward_rake",
            "request_data":{
                "rake_data":rake_data
            }
        }
        failed_data=json.dumps(failed_data, default=str)
        cache.rpush("ground_truth_queue",failed_data)
        logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        return result

def update_container_stack_location(stack_data):
    try:
        logger.debug('Update Container Stack Location, soap service request with data : '+ str(stack_data))
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/YardWriteOperation/yardwriteoperation_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="yardwriteoperation_client_ep",
                        port_name="YardWriteOperation_pt",transport=transport)
        start_time = datetime.now()
        result = soap.service.process(**stack_data)
        end_time = datetime.now()
        save_in_diagnostics(Constants.STACK_LOCATION_ENDPOINT+("EXIM"),{"data":str(stack_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Update EXIM Container Stack Location,soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Update EXIM Container Stack Location, Exception : '+str(e))
        failed_data = {
            "method_name":"update_container_stack_location",
            "request_data":{
                "stack_data":stack_data
            }
        }
        failed_data=json.dumps(failed_data, default=str)
        cache.rpush("ground_truth_queue",failed_data)
        logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = {}
        return result 

def update_domestic_container_stack_location(stack_data):
    result = []
    try:
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/DTMSYardWrite/dtmsyardwritebpel_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="dtmsyardwritebpel_client_ep",
                        port_name="DTMSYardWriteBPEL_pt")
        logger.debug('Update Domestic Container Stack Location, soap service request with data : '+ str(stack_data))
        start_time = datetime.now()
        result = soap.service.process(**stack_data)
        end_time = datetime.now()
        save_in_diagnostics(Constants.STACK_LOCATION_ENDPOINT+("Domestic"),{"data":str(stack_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Update Domestic Container Stack Location,soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Update Domestic Container details in yard, Exception : '+str(e))
        failed_data = {
            "method_name":"update_domestic_container_stack_location",
            "request_data":{
                "stack_data":stack_data
            }
        }
        failed_data=json.dumps(failed_data, default=str)
        cache.rpush("ground_truth_queue",failed_data)
        logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        return result
        
def get_domestic_yard_container_details(data):
    try:
        logger.debug('Get Domestic Yard Container Details, soap service request with data : '+ str(data))
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/DTMSYard/dtmsyardinvbpel_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="dtmsyardinvbpel_client_ep",
                        port_name="DTMSYardInvBPEL_pt",transport=transport)
        start_time = datetime.now()
        result = soap.service.process(**data)
        end_time = datetime.now()
        save_in_diagnostics(Constants.DTMS_CONTAINER_DETAILS,{"data":str(data)},{"output":str(result)},start_time,end_time)
        logger.debug('Get Domestic Yard Container Details,soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Get Domestic Yard Container Details, Exception : '+str(e))
        # failed_data = {
        #     "method_name":"get_domestic_yard_container_details",
        #     "request_data":{
        #         "data":data
        #     }
        # }
        # failed_data=json.dumps(failed_data, default=str)
        # cache.rpush("ground_truth_queue",failed_data)
        # logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        result = {}
        return result 


def get_wagon_details(wagon_number):
    result = []
    try:
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/WagonMaster/wagonmasterbpel_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="wagonmasterbpel_client_ep",
                        port_name="WagonMasterBPEL_pt")
        logger.debug('Get wagon details, soap service request with data wagon_number: '+ str(wagon_number))
        start_time = datetime.now()
        data =  {'WagonNumber': wagon_number}
        result = soap.service.process(**data)
        end_time = datetime.now()
        save_in_diagnostics(Constants.WAGON_VALIDATION_ENDPOINT,{"data":str(data)},{"output":str(result)},start_time,end_time)
        logger.debug('Get wagon details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Get wagon details, , Exception : '+str(e))
        failed_data = {
            "method_name":"get_wagon_details",
            "request_data":{
                "wagon_number":wagon_number
            }
        }
        failed_data=json.dumps(failed_data, default=str)
        cache.rpush("ground_truth_queue",failed_data)
        logger.debug("Added to cache retry mechanism, details:  " +failed_data)
        return result
