from app.services.warehouse.soap_api_call import get_job_info
from app.services.warehouse.database_service import WarehouseDB
from app.logger import logger
import app.services.warehouse.constants as constants
from app.services.warehouse.data_formater import DataFormater
from app.models.warehouse.job_order import CCLSJobOrder
from app import postgres_db as db
from app.enums import JobOrderType,ContainerFlag

class WarehouseStuffing(object):
    def __init__(self) -> None:
        import os,json
        import config
        CCLS_SAMPLE_RESPONSE_FILE = os.path.join(config.BASE_DIR,'app/services/warehouse','ccls_sample_response.json')
        with open(CCLS_SAMPLE_RESPONSE_FILE, 'r') as f:
            self.warehouse_info = json.load(f)

    def get_stuffing_details(self,container_number,job_type):
        stuffing_details = get_job_info(container_number,"CWHStuffingRead","cwhstuffingreadbpel_client_ep","CWHStuffingReadBPEL_pt")
        #stuffing_details = self.warehouse_info['stuffing_response']
        
        if job_type==JobOrderType.STUFFING_FCL.value:
            container_flag = ContainerFlag.FCL.value
        elif job_type==JobOrderType.STUFFING_LCL.value :
            container_flag = ContainerFlag.LCL.value
        else:
            container_flag = ContainerFlag.FCL.value
        stuffing_details['job_type'] = job_type
        stuffing_details['fcl_or_lcl'] = container_flag
        result = DataFormater().build_stuffing_response_obj(stuffing_details)
        
        self.save_data_db(stuffing_details,container_number)
        return result
    
    def save_data_db(self,job_order_details,container_number):
        bill_details_list = job_order_details.pop('shipping_bill_details_list')
        # truck_details = job_order_details.pop('truck_details')
        container_id = WarehouseDB().save_container_details(job_order_details)
        # query_object = db.session.query(CCLSJobOrder).join(Container).filter(Container.container_number==container_number,CCLSJobOrder.status==JobStatus.COMPLETED.value)
        query_object = db.session.query(CCLSJobOrder).filter(CCLSJobOrder.container_id==container_number)
        job_order_id = WarehouseDB().save_ccls_job_order(job_order_details,container_id,query_object)
        WarehouseDB().save_ccls_cargo_details(bill_details_list,job_order_id,'shipping_bill')
        # WarehouseDB().save_truck_details(truck_details,job_order_id)