from app.services.warehouse.soap_api_call import get_revenue_details,get_revenue_amount
from app.logger import logger
import app.services.warehouse.constants as constants
from app import postgres_db as db
from app.user_defined_exception import DataNotFoundException
from app.enums import RevenueType

class RevenueView(object):

    def get_revenue_details(self,from_date,to_date,type):
        from_date = self.ccls_date_format(from_date)
        to_date = self.ccls_date_format(to_date)
        if type=='export':
            revenue_details = get_revenue_details(from_date,to_date,constants.KEY_EXPORT_REVENUE_SERVICE_TYPE,constants.KEY_EXPORT_REVENUE_SERVICE_NAME,constants.KEY_EXPORT_REVENUE_PORT_NAME)
        else:
            revenue_details = get_revenue_details(from_date,to_date,constants.KEY_IMPORT_REVENUE_SERVICE_TYPE,constants.KEY_IMPORT_REVENUE_SERVICE_NAME,constants.KEY_IMPORT_REVENUE_PORT_NAME)
        if revenue_details:
            return revenue_details
        else:
            raise DataNotFoundException('GTService: job data not found in ccls system')


    def get_revenue_amount(self,request):
        request_type = int(request.args.get('request_type'))
        to_date = request.args.get('to_date')
        to_date = self.convert_date_based_on_ccls_date_format(to_date)
        if request_type==RevenueType.EXPORT_FCL_REVENUE.value:
            request_data = {"LV_CTR_NO":request.args.get('container_number'),"P_DATE":to_date}
            revenue_details = get_revenue_amount(request_data,request_type,constants.KEY_EXPORT_FCL_ESTIMATED_REVENUE_SERVICE_TYPE,constants.KEY_EXPORT_FCL_ESTIMATED_REVENUE_SERVICE_NAME,constants.KEY_EXPORT_FCL_ESTIMATED_REVENUE_PORT_NAME)
            if revenue_details:
                amount = revenue_details[0]['CALC_WHF_EXP_FCL_CTMS']
                revenue_details={'amount':amount}
        elif request_type==RevenueType.EXPORT_LCL_REVENUE:
            to_date = request.args.get('to_date')
            to_date = self.convert_date_based_on_ccls_date_format(to_date)
            request_data = {"LV_SBILL_NO":request.args.get('shipping_bill'),"P_DATE":to_date,'LD_SBILL_DT':None}
            revenue_details = get_revenue_amount(request_data,request_type,constants.KEY_EXPORT_LCL_ESTIMATED_REVENUE_SERVICE_TYPE,constants.KEY_EXPORT_LCL_ESTIMATED_REVENUE_SERVICE_NAME,constants.KEY_EXPORT_LCL_ESTIMATED_REVENUE_PORT_NAME)
            if revenue_details:
                amount = revenue_details[0]['CALC_WHF_EXP_LCL_CTMS']
                revenue_details={'amount':amount}
        elif request_type==RevenueType.IMPORT_FCL_REVENUE:
            request_data = {"LV_CTR_NO":request.args.get('container_number'),"P_DATE":to_date}
            revenue_details = get_revenue_amount(request_data,request_type,constants.KEY_IMPORT_FCL_ESTIMATED_REVENUE_SERVICE_TYPE,constants.KEY_IMPORT_FCL_ESTIMATED_REVENUE_SERVICE_NAME,constants.KEY_IMPORT_FCL_ESTIMATED_REVENUE_PORT_NAME)
            if revenue_details:
                amount = revenue_details[0]['CALC_WHF_CTMS_DATE']
                revenue_details={'amount':amount}
        else:
            request_data = {"LV_CTR_NO":request.args.get('container_number'),"P_DATE":to_date,"P_BOE_NO":request.args.get('bill_number')}
            revenue_details = get_revenue_amount(request_data,request_type,constants.KEY_IMPORT_LCL_ESTIMATED_REVENUE_SERVICE_TYPE,constants.KEY_IMPORT_LCL_ESTIMATED_REVENUE_SERVICE_NAME,constants.KEY_IMPORT_LCL_ESTIMATED_REVENUE_PORT_NAME)
            if revenue_details:
                amount = revenue_details[0]['CALC_WHF_IMP_BLWISE_CTMS']
                revenue_details={'amount':amount}
        if revenue_details:
            return revenue_details
        else:
            raise DataNotFoundException('GTService: job data not found in ccls system')
        
    def convert_date_based_on_ccls_date_format(self,timestamp):
        from datetime import datetime
        if timestamp:
            datetime_format='%Y-%m-%dT%H:%M:%S'                
            ccls_date = datetime.fromtimestamp(int(timestamp)/1000).strftime(datetime_format)
            return ccls_date
        return None
    
    def ccls_date_format(self,date):
        from datetime import datetime
        if date:
            datetime_format='%Y-%m-%d %H:%M:%S'
            ccls_date = datetime.strptime(str(date), datetime_format)
            return ccls_date 
        return None