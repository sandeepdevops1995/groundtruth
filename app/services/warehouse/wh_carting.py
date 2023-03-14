
from app.services.warehouse.soap_api_call import call_api
from app.services.warehouse.database_service import WarehouseDB
from app.logger import logger
import app.services.warehouse.constants as constants
from app.services.warehouse.data_formater import DataFormater
from app.enums import ContainerFlag
from app.Models.warehouse.job_order import CCLSJobOrder
from app import postgres_db as db
from app.enums import JobStatus,JobOrderType

class WarehouseCarting(object):
    def __init__(self) -> None:
        import os,json
        import config
        CCLS_SAMPLE_RESPONSE_FILE = os.path.join(config.BASE_DIR,'app/services/warehouse','ccls_sample_response.json')
        with open(CCLS_SAMPLE_RESPONSE_FILE, 'r') as f:
            self.warehouse_info = json.load(f)

    def get_carting_details(self,crn_number,job_type):
        carting_details = call_api(crn_number,"CWHCartingRead","cwhcartingreadbpel_client_ep","CWHCartingReadBPEL_pt")
        #carting_details = self.warehouse_info['carting_response']
        if job_type==JobOrderType.CARTING_FCL.value:
            filter_data = {"crn_number":crn_number}
            container_flag=ContainerFlag.FCL.value
        else:
            filter_data = {"carting_order_number":crn_number}
            container_flag=ContainerFlag.LCL.value
        # carting_details['crn_number'] = crn_number
        carting_details['job_type'] = job_type
        carting_details['fcl_or_lcl'] = container_flag
        result = DataFormater().build_carting_response_obj(carting_details,container_flag)
        self.save_data_db(carting_details,filter_data)
        return result


    def save_data_db(self,job_order_details,filter_data):
        bill_details_list = job_order_details.pop('shipping_bill_details_list')
        truck_details = job_order_details.pop('truck_details')
        container_id = WarehouseDB().save_container_details(job_order_details)
        query_object = db.session.query(CCLSJobOrder).filter_by(**filter_data)
        job_order_id = WarehouseDB().save_ccls_job_order(job_order_details,container_id,query_object)
        WarehouseDB().save_ccls_cargo_details(bill_details_list,job_order_id,'shipping_bill')
        WarehouseDB().save_truck_details(truck_details,job_order_id)