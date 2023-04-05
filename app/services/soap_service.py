
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
transport = Transport(timeout=10)


def get_permit_details(permit_number):
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/EmpltyTrailer/emptytrailerbpel_client_ep?WSDL"
    
    try:
        # soap = zeep.Client(wsdl=wsdl_url, 
        #                 service_name="emptytrailerbpel_client_ep",
        #                 port_name="EmptyTrailerBPEL_pt")
        soap = zeep.Client(config.WSDL_FILE,transport=transport)
        logger.debug('Get Permit, soap service request with permit_number : '+permit_number)
        result = soap.service.process(permit_number)
        save_in_diagnostics(Constants.CCLS_DATA_ENDPOINT,{"permit_number":permit_number},{"output":str(result)})
        logger.debug('Get Permit, soap service response : '+str(result))
    except Exception as e:
        logger.exception('Get Permit, Exception : '+str(e))
        result = {}
    return result

def update_container_details(update_data):
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/GateWriteOperation/gatewriteoperation_client_ep?WSDL"
    try:      
        logger.debug('Update Container Details, soap service request with data : '+ str(update_data))
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="gatewriteoperation_client_ep",
                        port_name="GateWriteOperation_pt")
        
        
        result = soap.service.process(**update_data)
        save_in_diagnostics(Constants.UPDATE_CONTAINER_DETAILS_ENDPOINT,{"data":str(update_data)},{"output":str(result)})
        logger.debug('Update Container Details, soap service response : '+ str(result))
        
    except Exception as e:
        logger.exception('Update Container Details, Exception : '+str(e))
        result = {}
    return result

def get_train_data(train_number='',from_date='', to_date = ''):
    try:
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/RakeReadOperation/rakereadproocess_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="rakereadproocess_client_ep",
                        port_name="RakeReadProocess_pt")
        rake_data = {'TrainNumber': train_number, 'From': from_date,'To':to_date }
        logger.debug('Get Train Details, soap service request with data : '+ str(rake_data))
        result = soap.service.process(**rake_data)
        save_in_diagnostics(Constants.TRAIN_DETAILS_ENDPOINT,{"data":str(rake_data)},{"output":str(result)})
        logger.debug('Get Train Details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Get Train Details, Exception : '+str(e))
        result = {}
        return result
    

def update_inward_rake(rake_data,api_url="Inward Write"):
    try: 
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/RakeInwardWriteOperation/rakewriteinward_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="rakewriteinward_client_ep",
                        port_name="RakeWriteInward_pt")
        logger.debug('Update Inward Rake Details, soap service request with data : '+ str(rake_data))
        result = soap.service.process(**rake_data)
        save_in_diagnostics(api_url,{"data":str(rake_data)},{"output":str(result)})
        logger.debug('Update Inward Rake Details, soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Update Inward Rake Details, Exception : '+str(e))
        result = {}
        return result
    
def update_outward_rake(rake_data,api_url="Outward Write"):
    try: 
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/RakeOutwardWriteOperation/rakeoutwardwrite_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="rakeoutwardwrite_client_ep",
                        port_name="RakeOutwardWrite_pt")
        logger.debug('Update Outward Rake Details, soap service request with data : '+ str(rake_data))
        result = soap.service.process(**rake_data)
        save_in_diagnostics(api_url,{"data":str(rake_data)},{"output":str(result)})
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
        stack_data["updatedDate"] = str(datetime.strptime(data["updated_at"], '%Y-%m-%d %H:%M:%S').isoformat())
        stack_data["updatedBy"] = "ctms_user"
        logger.debug('Update Container Stack Location, soap service request with data : '+ str(stack_data))
        wsdl_url = config.WSDL_URL+'/soa-infra/services/default/YardWriteOperation/yardwriteoperation_client_ep?WSDL'
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name="yardwriteoperation_client_ep",
                        port_name="YardWriteOperation_pt")
        result = soap.service.process(**stack_data)
        save_in_diagnostics(Constants.STACK_LOCATION_ENDPOINT,{"data":str(stack_data)},{"output":str(result)})
        logger.debug('Update Container Stack Location,soap service response : '+ str(result))
        return result
    except Exception as e:
        logger.exception('Update Container Stack Location, Exception : '+str(e))
        result = {}
        return result 