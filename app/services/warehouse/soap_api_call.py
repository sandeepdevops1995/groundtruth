
import zeep
import config
from app.logger import logger
import xmltodict
import json
import requests

def get_job_info(input_value,service_type,service_name,port_name):
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/"+service_type+"/"+service_name+"?WSDL"
    try:
        logger.info("{},{},{}:{}".format("GTService: request to ccls" ,wsdl_url,"job_order",input_value))
        soap = zeep.Client(wsdl=wsdl_url, service_name=service_name)
        with soap.settings(raw_response=False):
            result = soap.service.process(input_value)
            if config.IS_MOCK_ENABLED:
                import xml.etree.ElementTree as ET
                # data = xmltodict.parse(result)
                data = xmltodict.parse(result,force_list={'truck_details': True, 'shipping_bill_details_list': True, 'bill_details_list': True})
                # using json.dumps to convert dictionary to JSON
                result = json.loads(json.dumps(data, indent = 3))
                result = result['root']
        logger.info("{},{},{}:{}".format("GTService: response from ccls" ,result,"job_order",input_value))
    except requests.exceptions.ConnectionError as e:
        raise Exception('GTService: getting connection error while calling to ccls service').with_traceback(e.__traceback__)
    except Exception as e:
        raise Exception('GTService: getting internal error while fetching job details from ccls service').with_traceback(e.__traceback__)
    return result

def post_job_info(job_info,service_type,service_name,port_name,request_parameter):
    # return "success"
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/"+service_type+"/"+service_name+"?WSDL"
    try:
        logger.info("{},{},{}:{},{}:{}".format("GTService: request to ccls" ,wsdl_url,'request_body',job_info,"job_order",request_parameter))
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name=service_name,
                        port_name=port_name)
        if config.IS_MOCK_ENABLED:
            result = soap.service.process(str(job_info))
        else:
            result = soap.service.process(**job_info)
        logger.info("{},{},{}:{}".format("GTService: response from ccls" ,result,"job_order",request_parameter))
    except requests.exceptions.ConnectionError as e:
        raise Exception('GTService: getting connection error while posting job details to ccls service').with_traceback(e.__traceback__)
    except Exception as e:
        raise Exception('GTService: getting internal error while posting job details to ccls service').with_traceback(e.__traceback__)