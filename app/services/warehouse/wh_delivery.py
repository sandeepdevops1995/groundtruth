
from app.services.warehouse.soap_api_call import call_api
from app.services.warehouse.database_service import WarehouseDB
from app.logger import logger
import app.services.warehouse.constants as constants
from app.services.warehouse.data_formater import DataFormater
from app.enums import JobStatus
from app.Models.warehouse.job_order import CCLSJobOrder
from app import postgres_db as db

class WarehouseDelivery(object):
    def __init__(self) -> None:
        import os,json
        import config
        CCLS_SAMPLE_RESPONSE_FILE = os.path.join(config.BASE_DIR,'app/services/warehouse','ccls_sample_response.json')
        with open(CCLS_SAMPLE_RESPONSE_FILE, 'r') as f:
            self.warehouse_info = json.load(f)

    def get_delivery_details(self,gpm_number,job_type,container_flag):
        delivery_details = call_api(gpm_number,"CWHDeliveryRead","cwhdeliveryreadbpel_client_ep","CWHDeliveryReadBPEL_pt")
        #delivery_details = self.warehouse_info['delivery_response']
        delivery_details['gpm_number'] = gpm_number
        delivery_details['job_type'] = job_type
        delivery_details['fcl_or_lcl'] = container_flag
        result = DataFormater().build_delivery_response_obj(delivery_details,container_flag)
        self.save_data_db(delivery_details)
        return result

    def save_data_db(self,job_order_details):
        print("job_order_details---------",job_order_details)
        filter_data = {"gpm_number":job_order_details['gpm_number'],"status":JobStatus.COMPLETED.value}
        bill_details_list = job_order_details.pop('bill_details_list')
        # truck_details = job_order_details.pop('truck_details')
        query_object = db.session.query(CCLSJobOrder).filter_by(**filter_data)
        container_id = WarehouseDB().save_container_details(job_order_details)
        job_order_id = WarehouseDB().save_ccls_job_order(job_order_details,container_id,query_object)
        WarehouseDB().save_ccls_cargo_details(bill_details_list,job_order_id,'bill_of_entry')
        # WarehouseDB().save_truck_details(truck_details,job_order_id)
