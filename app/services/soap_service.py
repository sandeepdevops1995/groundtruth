
import zeep
import config
from datetime import datetime
from app import constants as Constants
from app.models import CCLSRake
from app import postgres_db as db
from app.logger import logger
from app.services.rake.gt_upload_service import commit,save_in_diagnostics
from app.models.utils import db_format
import json
from zeep.transports import Transport
import xmltodict

transport = Transport(timeout=10)


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
        print(result)
    except Exception as e:
        logger.exception('Get Permit, Exception ( EXIM ) : '+str(e))
        result = {}
    return result

def get_domestic_permit_details(permit_number):
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/DTMSGateAPIRead/dtmsgatereadbpel_client_ep?WSDL"
    try:
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="dtmsgatereadbpel_client_ep",
                        port_name="DTMSGateReadBPEL_pt")
        logger.debug('Get Permit, soap service request with permit_number ( DOM ) : '+permit_number)
        start_time = datetime.now()
        result = soap.service.process(permit_number)
        end_time = datetime.now()
        save_in_diagnostics(Constants.CCLS_DATA_ENDPOINT+ " (DOM) ",{"permit_number":permit_number},{"output":str(result)},start_time,end_time)
        logger.debug('Get Permit, soap service response ( DOM ) : '+str(result))
    except Exception as e:
        logger.exception('Get Permit, Exception ( DOM ) : '+str(e))
        result = {}
    return result

def update_container_details(update_data):
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/GateWriteOperation/gatewriteoperation_client_ep?WSDL"
    try:      
        logger.debug('Update Container Details, soap service request with data : '+ str(update_data))
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="gatewriteoperation_client_ep",
                        port_name="GateWriteOperation_pt")
        
        start_time = datetime.now()
        result = soap.service.process(**update_data)
        end_time = datetime.now()
        save_in_diagnostics(Constants.UPDATE_CONTAINER_DETAILS_ENDPOINT,{"data":str(update_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Update Container Details, soap service response : '+ str(result))
        
    except Exception as e:
        # logger.exception('Update Container Details, Exception : '+str(e))
        result = {}
    return result

def get_exim_train_details(train_number='',from_date='', to_date = ''):
    try:
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/RakeReadOperation/rakereadproocess_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="rakereadproocess_client_ep",
                        port_name="RakeReadProocess_pt")
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
        result = {}
        return result
    
def get_domestic_train_details(train_number='',from_date='', to_date = ''):
    try:
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/DTMSRakeInwardProcess/dtmsrakeinwardapi_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="dtmsrakeinwardapi_client_ep",
                        port_name="DTMSRakeInwardAPI_pt")
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
        result = {}
        return result
    

def update_inward_rake(rake_data,api_url="Inward Write"):
    try: 
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/RakeInwardWriteOperation/rakewriteinward_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="rakewriteinward_client_ep",
                        port_name="RakeWriteInward_pt")
        logger.debug('Update Inward Rake Details, soap service request with data : '+ str(rake_data))
        start_time = datetime.now()
        result = soap.service.process(**rake_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(rake_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Update Inward Rake Details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Update Inward Rake Details, Exception : '+str(e))
        result = {}
        return result
    
def get_pendancy_details(gateway_port_data,api_url="/pendency_containers"):
    try: 
        
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/CCLSRakePendencyList/cclsrakependencybpel_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url,
                        service_name="cclsrakependencybpel_client_ep",
                        port_name="CCLSRakePendencyBPEL_pt")
        start_time = datetime.now()
        result = soap.service.process(**gateway_port_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(gateway_port_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Get LOADED pendancy container details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Get LOADED pendancy container details, Exception : '+str(e))
        result = []
        return result

def get_empty_pendancy_details(gateway_port_data,api_url="/pendency_containers"):
    try: 
        result = []        
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/CCLSRakeEmptyPendency/cclsrakeemptypendencybpel_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, service_name="cclsrakeemptypendencybpel_client_ep", port_name="CCLSRakeEmptyPendencyBPEL_pt")
        start_time = datetime.now()
        result = soap.service.process(**gateway_port_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(gateway_port_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Get EMPTY pendancy container details, soap service response : '+ str(result))
        
        return result
    except Exception as e:
        logger.exception('Get EMPTY pendancy container details, Exception : '+str(e))
        result = []
        return result

def get_block_pendancy_details(gateway_port_data,api_url="/pendency_containers"):
    try: 
        result = []        
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/CCLSRakeBlockPendncy/cclsblockpendencybpel_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, service_name="cclsblockpendencybpel_client_ep", port_name="CCLSBlockpendencyBpel_pt")
        start_time = datetime.now()
        result = soap.service.process(**gateway_port_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(gateway_port_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Get BLOCK pendancy container details, soap service response : '+ str(result))
        
        return result
    except Exception as e:
        logger.exception('Get BLOCK pendancy container details, Exception : '+str(e))
        result = []
        return result

def get_express_pendancy_details(gateway_port_data,api_url="/pendency_containers"):
    try: 
        result = []        
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/CCLSRakeExpressPendency/expressbpel_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, service_name="expressbpel_client_ep", port_name="ExpressBpel_pt")
        start_time = datetime.now()
        result = soap.service.process(**gateway_port_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(gateway_port_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Get EXPRESS pendancy container details, soap service response : '+ str(result))
        
        return result
    except Exception as e:
        logger.exception('Get EXPRESS pendancy container details, Exception : '+str(e))
        result = []
        return result

# def get_lcl_pendancy_details(gateway_port_data,api_url="/pendency_containers"):
#     try: 
#         result = []        
#         wsdl_url = config.WSDL_URL+'/soa-infra/services/default/CCLSRakeEmptyPendency/cclsrakeemptypendencybpel_client_ep?WSDL'
#         soap = zeep.Client(wsdl=wsdl_url, service_name="cclsrakeemptypendencybpel_client_ep", port_name="CCLSRakeEmptyPendencyBPEL_pt")
#         start_time = datetime.now()
#         result = soap.service.process(**gateway_port_data)
#         end_time = datetime.now()
#         save_in_diagnostics(api_url,{"data":str(gateway_port_data)},{"output":str(result)},start_time,end_time)
#         logger.debug('Get ICD pendancy empty container details, soap service response : '+ str(result))
        
#         return result
#     except Exception as e:
#         logger.exception('Get ICD pendancy container details, Exception : '+str(e))
#         result = []
#         return result

def update_outward_rake(rake_data,api_url="Outward Write"):
    try: 
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/RakeOutwardWriteOperation/rakeoutwardwrite_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="rakeoutwardwrite_client_ep",
                        port_name="RakeOutwardWrite_pt")
        logger.debug('Update Outward Rake Details, soap service request with data : '+ str(rake_data))
        start_time = datetime.now()
        result = soap.service.process(**rake_data)
        end_time = datetime.now()
        save_in_diagnostics(api_url,{"data":str(rake_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Update Outward Rake Details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Update Outward Rake Details, Exception : '+str(e))
        result = {}
        return result
            

def update_container_stack_location(data):
    try:
        stack_data = {}
        stack_data["trnNo"] = "TGS601809"
        stack_data["dtSeal"] = str(datetime.now().isoformat())
        stack_data["createdDate"] = str(datetime.now().isoformat())                                                                                   
        stack_data["ctrNo"] = data["container_number"]
        stack_data["stkLoc"] = data["stack_location"]
        stack_data["attribute1"] = data["equipment_id"]
        stack_data["trlNo"] = data["trailer_number"]
        # RECHECK THIS LINE OF CODE
        #stack_data["tmOpn"] = str(datetime.strptime(data["operation_time"], '%Y-%m-%d %H:%M:%S').isoformat())
        stack_data["frmLoc"] = data["from_location"]
        stack_data["toLoc"] = data["to_location"]
        stack_data["updatedDate"] = str(datetime.now().isoformat())
        stack_data["updatedBy"] = "ctms_user"
        logger.debug('Update Container Stack Location, soap service request with data : '+ str(stack_data))
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/YardWriteOperation/yardwriteoperation_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="yardwriteoperation_client_ep",
                        port_name="YardWriteOperation_pt")
        start_time = datetime.now()
        result = soap.service.process(**stack_data)
        end_time = datetime.now()
        save_in_diagnostics(Constants.STACK_LOCATION_ENDPOINT,{"data":str(stack_data)},{"output":str(result)},start_time,end_time)
        logger.debug('Update Container Stack Location,soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Update Container Stack Location, Exception : '+str(e))
        result = {}
        return result 