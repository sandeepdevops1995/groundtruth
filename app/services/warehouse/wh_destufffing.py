
from app.services.warehouse.soap_api_call import get_job_order_info
from app.logger import logger
import app.services.warehouse.constants as constants
from app.services.warehouse.data_formater import DataFormater
from app.enums import ContainerFlag,JobOrderType
from app import postgres_db as db
from app.serializers.ccls_cargo_serializer import CCLSCargoInsertSchema
from app.models.warehouse.ccls_cargo_details import MasterCargoDetails,DeStuffingCargoDetails
from app.user_defined_exception import DataNotFoundException

class WarehouseDeStuffing(object):

    def get_destuffing_details(self,container_number,job_type):
        cargo_details = get_job_order_info(container_number,"CWHDeStuffingRead","cwhdestuffingreadbpel_client_ep","CWHDeStuffingReadBPEL_pt")
        if cargo_details:
            container_info, destuffing_details = map(lambda keys: {x: cargo_details[x] if x in cargo_details else None for x in keys}, [["container_number","container_type","container_size","container_iso_code","container_location_code","container_life"], ["container_number","destuffing_job_order","destuffing_plan_date","handling_code","hld_rls_flag"]])
            cargo_details['container_info'] = container_info
            container_info['container_life'] = int(float(container_info['container_life']))
            container_info['container_size'] = int(float(container_info['container_size']))
            cargo_details['destuffing_details'] = destuffing_details
            if job_type==JobOrderType.DE_STUFFING_FCL.value:
                container_flag = ContainerFlag.FCL.value
            else:
                container_flag = ContainerFlag.LCL.value
            cargo_details['job_type'] = job_type
            cargo_details['fcl_or_lcl'] = container_flag
            result = DataFormater().build_destuffing_response_obj(cargo_details,container_flag)
            self.save_data_db(cargo_details)
            return result
        else:
            raise DataNotFoundException('GTService: job data not found in ccls system')

    def save_data_db(self,cargo_details):
        print("destuffing-----------------cargo_details",cargo_details)
        destuffing_cargo_query = db.session.query(DeStuffingCargoDetails).join(MasterCargoDetails).filter(DeStuffingCargoDetails.destuffing_job.property.mapper.class_.container_info.property.mapper.class_.container_life==cargo_details['container_info'].get('container_life'),DeStuffingCargoDetails.container_number==cargo_details['destuffing_details'].get('container_number')).first()
        if not destuffing_cargo_query:
            master_job_request = CCLSCargoInsertSchema().load(cargo_details, session=db.session)
            db.session.add(master_job_request)
            db.session.commit()
