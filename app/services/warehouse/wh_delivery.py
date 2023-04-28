
from app.services.warehouse.soap_api_call import get_job_order_info
from app.logger import logger
import app.services.warehouse.constants as constants
from app.services.warehouse.data_formater import DataFormater
from app.enums import JobOrderType,ContainerFlag
from app import postgres_db as db
from app.serializers.ccls_cargo_serializer import CCLSCargoInsertSchema
from app.models.warehouse.ccls_cargo_details import DeliveryCargoDetails
from app.user_defined_exception import DataNotFoundException

class WarehouseDelivery(object):

    def get_delivery_details(self,gpm_number,job_type):
        cargo_details = get_job_order_info(gpm_number,"CWHDeliveryRead","cwhdeliveryreadbpel_client_ep","CWHDeliveryReadBPEL_pt")
        if cargo_details:
            container_info, delivery_details = map(lambda keys: {x: cargo_details[x] if x in cargo_details else None for x in keys}, [["container_number","container_type","container_size","container_iso_code","container_location_code","container_life"], ["gpm_number","gpm_valid_date","gp_stat","cha_code"]])
            cargo_details['container_info'] = container_info
            container_info['container_life'] = int(float(container_info['container_life'])) if container_info['container_life']!=None else container_info['container_life']
            container_info['container_size'] = int(float(container_info['container_size'])) if container_info['container_size']!=None else container_info['container_size']
            cargo_details['delivery_details'] = delivery_details
            if job_type==JobOrderType.DELIVERY_FCL.value:
                container_flag = ContainerFlag.FCL.value
            elif job_type==JobOrderType.DELIVERY_LCL.value:
                container_flag = ContainerFlag.LCL.value
            else:
                container_flag = ContainerFlag.FCL.value
            cargo_details['job_type'] = job_type
            cargo_details['fcl_or_lcl'] = container_flag
            result = DataFormater().build_delivery_response_obj(cargo_details,container_flag)
            self.save_data_db(cargo_details)
            return result
        else:
            raise DataNotFoundException('GTService: job data not found in ccls system')

    def save_data_db(self,cargo_details):
        print("delivery-----------------cargo_details",cargo_details)
        delivery_cargo_query = db.session.query(DeliveryCargoDetails).filter(DeliveryCargoDetails.gpm_number==cargo_details['delivery_details'].get('gpm_number'),DeliveryCargoDetails.gpm_valid_date==cargo_details['delivery_details'].get('gpm_valid_date')).first()
        if not delivery_cargo_query:
            master_job_request = CCLSCargoInsertSchema().load(cargo_details, session=db.session)
            db.session.add(master_job_request)
            db.session.commit()
