
from app.services.warehouse.soap_api_call import get_job_order_info
from app.logger import logger
import app.services.warehouse.constants as constants
from app.services.warehouse.data_formater import DataFormater
from app.enums import ContainerFlag
from app import postgres_db as db
from app.enums import JobOrderType
from app.serializers.ccls_cargo_serializer import CCLSCargoInsertSchema
from app.models.warehouse.ccls_cargo_details import CartingCargoDetails
from app.user_defined_exception import DataNotFoundException

class WarehouseCarting(object):

    def get_carting_details(self,crn_number,job_type):
        cargo_details = get_job_order_info(crn_number,"CWHCartingRead","cwhcartingreadbpel_client_ep","CWHCartingReadBPEL_pt")
        if cargo_details:
            container_info, carting_details = map(lambda keys: {x: cargo_details[x] if x in cargo_details else None for x in keys}, [["container_number","container_type","container_size","container_iso_code","container_location_code","container_life"], ["crn_number","crn_date","carting_order_number","con_date","is_cargo_card_generated","cha_code","gw_port_code","party_code","reserve_flag"]])
            cargo_details['container_info'] = container_info
            container_info['container_life'] = int(float(container_info['container_life']))
            container_info['container_size'] = int(float(container_info['container_size']))
            cargo_details['carting_details'] = carting_details
            if job_type==JobOrderType.CARTING_FCL.value:
                container_flag=ContainerFlag.FCL.value
                carting_cargo_query = db.session.query(CartingCargoDetails).filter(CartingCargoDetails.crn_number==cargo_details['carting_details'].get('crn_number'),CartingCargoDetails.crn_date==cargo_details['carting_details'].get('crn_date')).first()
            else:
                container_flag=ContainerFlag.LCL.value
                carting_cargo_query = db.session.query(CartingCargoDetails).filter(CartingCargoDetails.carting_order_number==cargo_details['carting_details'].get('carting_order_number'),CartingCargoDetails.con_date==cargo_details['carting_details'].get('con_date')).first()
            cargo_details['job_type'] = job_type
            cargo_details['fcl_or_lcl'] = container_flag
            result = DataFormater().build_carting_response_obj(cargo_details,container_flag)
            self.save_data_db(cargo_details,carting_cargo_query)
            return result
        else:
            raise DataNotFoundException('GTService: job data not found in ccls system')


    def save_data_db(self,cargo_details,carting_cargo_query):
        if not carting_cargo_query:
            master_job_request = CCLSCargoInsertSchema().load(cargo_details, session=db.session)
            db_object = db.session.add(master_job_request)
            db.session.commit()