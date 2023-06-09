
import zeep
import config
from app.logger import logger
import xmltodict
import json
import requests
import app.logging_message as LM
import os
from zeep.helpers import serialize_object
from app.enums import JobOrderType

def get_job_order_info(input_value,service_type,service_name,port_name,request_data,job_type=None):
    
    try:
            if config.IS_MOCK_ENABLED or (job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value] and config.IS_STUFFING_MOCK_ENABLED):
                wsdl_url = config.WSDL_URL+"/soa-infra/services/default/"+service_type+"/"+service_name+"?WSDL"
                logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_GET_REQUEST_TO_CCLS_TO_FETCH_JOB_ORDER_DATA,input_value,wsdl_url))
                soap = zeep.Client(wsdl=wsdl_url, service_name=service_name)
                with soap.settings(raw_response=False):
                    result = soap.service.process(input_value)
                    import xml.etree.ElementTree as ET
                    # data = xmltodict.parse(result)
                    data = xmltodict.parse(result,force_list={'truck_details': True, 'shipping_bill_details_list': True, 'bill_details_list': True})
                    # using json.dumps to convert dictionary to JSON
                    result = json.loads(json.dumps(data, indent = 3))
                    result = result['root']
            else:
                service_url = service_name.strip('_ep')
                wsdl_path = WSDL_FILE = os.path.join(config.BASE_DIR,"modified_soap_wsdls",service_url+"_1.wsdl")
                logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_GET_REQUEST_TO_CCLS_TO_FETCH_JOB_ORDER_DATA,input_value,wsdl_path))
                soap = zeep.Client(wsdl_path)
                with soap.settings(raw_response=False):
                    zeep_object = soap.service.process(**request_data)
                    result = serialize_object(zeep_object)
            logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_RESPONSE_FROM_CCLS_OF_JOB_ORDER_DATA,input_value,result))
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError('GTService: getting connection error while calling to ccls service').with_traceback(e.__traceback__)
    except Exception as e:
        logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_RESPONSE_FROM_CCLS_OF_JOB_ORDER_DATA,input_value,e))
        result={}
        #raise Exception('GTService: getting internal error while fetching job details from ccls service').with_traceback(e.__traceback__)
    return result

def upload_tallysheet_data(job_info,service_type,service_name,port_name,request_parameter):
    return "success"
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/"+service_type+"/"+service_name+"?WSDL"
    try:
        logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_GET_REQUEST_TO_CCLS_TO_UPLOAD_TALLYSHEET,request_parameter,wsdl_url,job_info))
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name=service_name,
                        port_name=port_name)
        if config.IS_MOCK_ENABLED:
            result = soap.service.process(str(job_info))
        else:
            result = soap.service.process(**job_info)
        logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_RESPONSE_FROM_CCLS_OF_UPLOAD_TALLYSHEET,request_parameter,result))
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError('GTService: getting connection error while posting job details to ccls service').with_traceback(e.__traceback__)
    except Exception as e:
        raise Exception('GTService: getting internal error while posting job details to ccls service').with_traceback(e.__traceback__)