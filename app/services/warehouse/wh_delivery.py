
from app.services.warehouse.soap_api_call import get_job_info
from app.services.warehouse.database_service import WarehouseDB
from app.logger import logger
import app.services.warehouse.constants as constants
from app.services.warehouse.data_formater import DataFormater
from app.enums import JobOrderType,ContainerFlag, JobStatus
from app.models.warehouse.job_order import CCLSJobOrder
from app import postgres_db as db

class WarehouseDelivery(object):
    def __init__(self) -> None:
        import os,json
        import config
        CCLS_SAMPLE_RESPONSE_FILE = os.path.join(config.BASE_DIR,'app/services/warehouse','ccls_sample_response.json')
        with open(CCLS_SAMPLE_RESPONSE_FILE, 'r') as f:
            self.warehouse_info = json.load(f)

    def get_delivery_details(self,gpm_number,job_type):
        delivery_details = get_job_info(gpm_number,"CWHDeliveryRead","cwhdeliveryreadbpel_client_ep","CWHDeliveryReadBPEL_pt")
        #delivery_details = self.warehouse_info['delivery_response']
        if delivery_details:
            if job_type==JobOrderType.DELIVERY_FCL.value:
                container_flag = ContainerFlag.FCL.value
            elif job_type==JobOrderType.DELIVERY_LCL.value:
                container_flag = ContainerFlag.LCL.value
            else:
                container_flag = ContainerFlag.FCL.value
            delivery_details['job_type'] = job_type
            delivery_details['fcl_or_lcl'] = container_flag
            filter_data = {'job_type':job_type,"status":JobStatus.INPROGRESS.value,"gpm_number":gpm_number}
            result = DataFormater().build_delivery_response_obj(delivery_details,container_flag)
            self.save_data_db(delivery_details,filter_data)
            return result
        else:
            raise Exception('GTService: job data not found in ccls system')

    def save_data_db(self,job_order_details,filter_data):
        # ,"status":JobStatus.COMPLETED.value
        bill_details_list = job_order_details.pop('bill_details_list')
        # truck_details = job_order_details.pop('truck_details')
        query_object = db.session.query(CCLSJobOrder).filter_by(**filter_data)
        container_id = WarehouseDB().save_container_details(job_order_details)
        job_order_id = WarehouseDB().save_ccls_job_order(job_order_details,container_id,query_object)
        WarehouseDB().save_ccls_cargo_details(bill_details_list,job_order_id,'bill_of_entry')
        # WarehouseDB().save_truck_details(truck_details,job_order_id)
