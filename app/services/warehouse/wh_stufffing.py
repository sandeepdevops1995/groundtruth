from app.services.warehouse.soap_api_call import get_job_order_info
from app.logger import logger
import app.services.warehouse.constants as constants
from app.services.warehouse.data_formater import DataFormater
from app import postgres_db as db
from app.enums import JobOrderType,ContainerFlag
from app.serializers.ccls_cargo_serializer import CCLSCargoInsertSchema
from app.models.warehouse.ccls_cargo_details import MasterCargoDetails,StuffingCargoDetails
from app.user_defined_exception import DataNotFoundException

class WarehouseStuffing(object):

    def get_stuffing_details(self,container_number,job_type):
        cargo_details = get_job_order_info(container_number,"CWHStuffingRead","cwhstuffingreadbpel_client_ep","CWHStuffingReadBPEL_pt")
        if cargo_details:
            container_info, stuffing_details = map(lambda keys: {x: cargo_details[x] if x in cargo_details else None for x in keys}, [["container_number","container_type","container_size","container_iso_code","container_location_code","container_life"], ["container_number","stuffing_job_order","hsn_code","cargo_weight_in_crn"]])
            cargo_details['container_info'] = container_info
            container_info['container_life'] = int(float(container_info['container_life']))
            container_info['container_size'] = int(float(container_info['container_size']))
            cargo_details['stuffing_details'] = stuffing_details
            if job_type==JobOrderType.STUFFING_FCL.value:
                container_flag = ContainerFlag.FCL.value
            elif job_type==JobOrderType.STUFFING_LCL.value :
                container_flag = ContainerFlag.LCL.value
            else:
                container_flag = ContainerFlag.FCL.value
            cargo_details['job_type'] = job_type
            cargo_details['fcl_or_lcl'] = container_flag
            result = DataFormater().build_stuffing_response_obj(cargo_details)
            
            self.save_data_db(cargo_details)
            return result
        else:
            raise DataNotFoundException('GTService: job data not found in ccls system')
    
    def save_data_db(self,cargo_details):
        print("stuffing-----------------cargo_details",cargo_details)
        stuffing_cargo_query = db.session.query(StuffingCargoDetails).join(MasterCargoDetails).filter(StuffingCargoDetails.stuffing_job.property.mapper.class_.container_info.property.mapper.class_.container_life==cargo_details['container_info'].get('container_life'),StuffingCargoDetails.container_number==cargo_details['stuffing_details'].get('container_number')).first()
        if not stuffing_cargo_query:
            master_job_request = CCLSCargoInsertSchema().load(cargo_details, session=db.session)
            db.session.add(master_job_request)
            db.session.commit()