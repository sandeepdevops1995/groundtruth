
import zeep
import config
from app.logger import logger
import xmltodict
import json
from app.enums import JobStatus,JobOrderType

def call_api(input_value,service_type,service_name,port_name,job_type):
    wsdl_url = config.WSDL_URL+"/soa-infra/services/default/"+service_type+"/"+service_name+"?WSDL"
    print("wsdl_url-----------",wsdl_url)
    try:
        logger.info('request to ccls with this input %s',input_value)
        soap = zeep.Client(wsdl=wsdl_url, service_name=service_name)
        with soap.settings(raw_response=False):
            result = soap.service.process(input_value)
            # result = soap.service.CWHCartingReadBPEL(input_value)
            # result = soap.service.CWHStuffingReadBPEL(input_value)
            # result = soap.service.CWHDeStuffingReadBPEL(input_value)
            # result = soap.service.CWHDeliveryReadBPEL(input_value)
            #print(result.content)
            # print(result)
            import xml.etree.ElementTree as ET
            # data = xmltodict.parse(result)
            if job_type in [JobOrderType.CARTING_FCL.value,JobOrderType.CARTING_LCL.value,JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING]:
                data = xmltodict.parse(result,force_list={'truck_details': True, 'shipping_bill_details_list': True})
            else:

                data = xmltodict.parse(result,force_list={'truck_details': True, 'bill_details_list': True})
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
        logger.error(e)
        result = {}
    return result