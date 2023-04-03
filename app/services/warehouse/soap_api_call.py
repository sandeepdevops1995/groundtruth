
import zeep
import config
from app.logger import logger
import xmltodict
import json

def get_job_info(input_value,service_type,service_name,port_name):
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/"+service_type+"/"+service_name+"?WSDL"
    logger.info("wsdl_url-----------%s",wsdl_url)
    try:
        logger.info('request to ccls with this input %s',input_value)
        soap = zeep.Client(wsdl=wsdl_url, service_name=service_name)
        with soap.settings(raw_response=False):
            result = soap.service.process(input_value)
            if config.IS_MOCK_ENABLED:
                import xml.etree.ElementTree as ET
                # data = xmltodict.parse(result)
                data = xmltodict.parse(result,force_list={'truck_details': True, 'shipping_bill_details_list': True, 'bill_details_list': True})
                # using json.dumps to convert dictionary to JSON
                print("type of response",type(data))
                result = json.loads(json.dumps(data, indent = 3))
                result = result['root']
            print('response from ccls---------',result)
        # soap = zeep.Client(wsdl=wsdl_url, 
        #                 service_name=service_name,
        #                 port_name=port_name)
        # result = soap.service.CWHCartingReadBPEL(input_value,1)
        logger.info('response from soap api of %s is %s',service_name,result)
    except Exception as e:
        # logger.error(e)
        logger.exception('Get job data, Exception : '+str(e))
        result = {}
    return result

def post_job_info(job_info,service_type,service_name,port_name):
    return "success"
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/"+service_type+"/"+service_name+"?WSDL"
    logger.info("wsdl_url-----------%s",wsdl_url)
    try:
        soap = zeep.Client(wsdl=wsdl_url, 
                        service_name=service_name,
                        port_name=port_name)
        logger.debug('post job data to ccls, soap service request with data : '+ str(job_info))
        result = soap.service.process(**job_info)
        logger.info('response from soap api of %s is %s',service_name,result)
    except Exception as e:
        # logger.error(e)
        logger.exception('post job data, Exception : '+str(e))
        result = {}
    return result