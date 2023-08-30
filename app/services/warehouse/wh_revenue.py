from app.services.warehouse.soap_api_call import get_revenue_details
from app.logger import logger
import app.services.warehouse.constants as constants
from app import postgres_db as db
from app.user_defined_exception import DataNotFoundException

class RevenueView(object):

    def get_revenue_details(self,from_date,to_date,type):
        if type=='export':
            revenue_details = get_revenue_details(from_date,to_date,constants.KEY_EXPORT_REVENUE_SERVICE_TYPE,constants.KEY_EXPORT_REVENUE_SERVICE_NAME,constants.KEY_EXPORT_REVENUE_PORT_NAME)
        else:
            revenue_details = get_revenue_details(from_date,to_date,constants.KEY_IMPORT_REVENUE_SERVICE_TYPE,constants.KEY_IMPORT_REVENUE_SERVICE_NAME,constants.KEY_IMPORT_REVENUE_PORT_NAME)
        if revenue_details:
            return revenue_details
        else:
            raise DataNotFoundException('GTService: job data not found in ccls system')    