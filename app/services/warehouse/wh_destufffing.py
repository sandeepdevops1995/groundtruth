
from app.services.warehouse.soap_api_call import call_api
from app.services.warehouse.database_service import WarehouseDB
from app.logger import logger
import app.services.warehouse.constants as constants
from app.services.warehouse.data_formater import DataFormater
from app.enums import ContainerFlag,JobOrderType
from app.Models.warehouse.job_order import CCLSJobOrder
from app import postgres_db as db

class WarehouseDeStuffing(object):
    def __init__(self) -> None:
        import os,json
        import config
        CCLS_SAMPLE_RESPONSE_FILE = os.path.join(config.BASE_DIR,'app/services/warehouse','ccls_sample_response.json')
        with open(CCLS_SAMPLE_RESPONSE_FILE, 'r') as f:
            self.warehouse_info = json.load(f)

    def get_destuffing_details(self,container_number,job_type):
        destuffing_details = call_api(container_number,"CWHDeStuffingRead","cwhdestuffingreadbpel_client_ep","CWHDeStuffingReadBPEL_pt")
        #destuffing_details = self.warehouse_info['destuffing_response']
        if job_type==JobOrderType.DE_STUFFING_FCL.value:
            container_flag = ContainerFlag.FCL.value
        else:
            container_flag = ContainerFlag.LCL.value
        destuffing_details['job_type'] = job_type
        destuffing_details['fcl_or_lcl'] = container_flag
        result = DataFormater().build_destuffing_response_obj(destuffing_details,container_flag)
        self.save_data_db(destuffing_details,container_number)
        return result

    def save_data_db(self,job_order_details,container_number):
        bill_details_list = job_order_details.pop('bill_details_list')
        # truck_details = job_order_details.pop('truck_details')
        if job_order_details['fcl_or_lcl']==ContainerFlag.FCL.value:
                filter_key = 'bill_of_entry'
        else:
                filter_key = 'bill_of_lading'
        query_object = db.session.query(CCLSJobOrder).filter(CCLSJobOrder.container_id==container_number)
        # query_object = db.session.query(CCLSJobOrder).join(Container).filter(Container.container_number==container_number,CCLSJobOrder.status==JobStatus.COMPLETED.value)
                                                                           
        container_id = WarehouseDB().save_container_details(job_order_details)
        job_order_id = WarehouseDB().save_ccls_job_order(job_order_details,container_id,query_object)
        WarehouseDB().save_ccls_cargo_details(bill_details_list,job_order_id,filter_key)
        # WarehouseDB().save_truck_details(truck_details,job_order_id)
