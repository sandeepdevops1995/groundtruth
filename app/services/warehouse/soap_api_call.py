
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
from app.services.rake.gt_upload_service import save_in_diagnostics
from datetime import datetime
import app.services.warehouse.constants as constants

def trim_grid_no(job_info):
    grid_no = job_info['gridNo']
    if grid_no:
        if len(grid_no)>3:
            job_info['gridNo'] = grid_no[-3:]
    return job_info


def get_revenue_details(from_date,to_date,service_type,service_name,port_name):
    try:
        wsdl_url = config.REVENUE_WSDL_URL+"/soa-infra/services/default/"+service_type+"/"+service_name+"?WSDL"
        logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_GET_REQUEST_TO_CCLS_TO_FETCH_JOB_ORDER_DATA,from_date,to_date,wsdl_url))
        soap = zeep.Client(wsdl=wsdl_url, service_name=service_name)
        with soap.settings(strict=False, raw_response=False, xsd_ignore_sequence_order=True):
            zeep_object = soap.service.process(from_date,to_date)
            if config.IS_MOCK_ENABLED:
                import xml.etree.ElementTree as ET
                data = xmltodict.parse(zeep_object)
                # data = xmltodict.parse(result,force_list={'truck_details': True, 'shipping_bill_details_list': True, 'bill_details_list': True})
                # using json.dumps to convert dictionary to JSON
                result = json.loads(json.dumps(data, indent = 3))
                result = result['root']['result_json_list']
                
            else:
                result = serialize_object(zeep_object)
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError('GTService: getting connection error while calling to ccls service').with_traceback(e.__traceback__)
    except Exception as e:
        logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_RESPONSE_FROM_CCLS_OF_JOB_ORDER_DATA,from_date,to_date,e))
        result={}
        #raise Exception('GTService: getting internal error while fetching job details from ccls service').with_traceback(e.__traceback__)
    return result

def get_job_order_info(input_value,service_type,service_name,port_name,request_data,job_type,strict=True):
    
    try:
            if config.IS_MOCK_ENABLED or (job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value] and config.IS_STUFFING_MOCK_ENABLED):
                wsdl_url = config.WSDL_URL+"/soa-infra/services/default/"+service_type+"/"+service_name+"?WSDL"
                logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_GET_REQUEST_TO_CCLS_TO_FETCH_JOB_ORDER_DATA,input_value,wsdl_url))
                soap = zeep.Client(wsdl=wsdl_url, service_name=service_name)
                with soap.settings(strict=strict, raw_response=False, xsd_ignore_sequence_order=True):
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
                start_time = datetime.now()
                soap = zeep.Client(wsdl_path)
                with soap.settings(strict=strict, raw_response=False, xsd_ignore_sequence_order=True):
                    zeep_object = soap.service.process(**request_data)
                    result = serialize_object(zeep_object)
                end_time = datetime.now()
                save_in_diagnostics(JobOrderType(job_type).name+":"+wsdl_path,request_data,{"output":str(zeep_object)},start_time,end_time,type=constants.KEY_CCLS_RESPONSE_TYPE)
            logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_RESPONSE_FROM_CCLS_OF_JOB_ORDER_DATA,input_value,result))
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError('GTService: getting connection error while calling to ccls service').with_traceback(e.__traceback__)
    except Exception as e:
        logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_RESPONSE_FROM_CCLS_OF_JOB_ORDER_DATA,input_value,e))
        result={}
        #raise Exception('GTService: getting internal error while fetching job details from ccls service').with_traceback(e.__traceback__)
    return result

def upload_tallysheet_data(job_info,service_type,service_name,port_name,request_parameter):
    try:
        if config.IS_MOCK_ENABLED:
            return "success"
            wsdl_url = config.WSDL_URL+"/soa-infra/services/default/"+service_type+"/"+service_name+"?WSDL"
            logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_GET_REQUEST_TO_CCLS_TO_UPLOAD_TALLYSHEET,request_parameter,wsdl_url,job_info))
            soap = zeep.Client(wsdl=wsdl_url, 
                        service_name=service_name,
                        port_name=port_name)
            result = soap.service.process(str(job_info))
        else:
            service_url = service_name.strip('_ep')
            wsdl_path = os.path.join(config.BASE_DIR,"modified_soap_wsdls_post",service_url+"_1.wsdl")
            logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_GET_REQUEST_TO_CCLS_TO_UPLOAD_TALLYSHEET,request_parameter,wsdl_path,job_info))
            if config.IS_TRIM_GRID_NO_REQUIRED:
                job_info = trim_grid_no(job_info)
                logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_UPLOAD_TALLYSHEET_TRIM_GRID_NO,request_parameter,wsdl_path,job_info['gridNo']))
            soap = zeep.Client(wsdl_path)
            with soap.settings(raw_response=False):
                result = soap.service.process(**job_info)
        logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_RESPONSE_FROM_CCLS_OF_UPLOAD_TALLYSHEET,request_parameter,result))
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError('GTService: getting connection error while posting job details to ccls service').with_traceback(e.__traceback__)
    except Exception as e:
        raise Exception('GTService: getting internal error while posting job details to ccls service').with_traceback(e.__traceback__)