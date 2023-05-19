
from app.services.warehouse.soap_api_call import get_job_order_info
from app.logger import logger
import app.services.warehouse.constants as constants
from app.services.warehouse.data_formater import DataFormater
from app.enums import JobOrderType,ContainerFlag
from app import postgres_db as db
from app.serializers.ccls_cargo_serializer import CCLSCargoInsertSchema
from app.models.warehouse.ccls_cargo_details import DeliveryCargoDetails,CCLSCargoBillDetails
from app.user_defined_exception import DataNotFoundException
import app.logging_message as LM
from app.serializers.update_ccls_cargo_serializer import CCLSBillDetailsGetSchema, CCLSBillDetailsUpdateSchema
from app.serializers.update_ccls_cargo_serializer import CCLSCargoUpdateSchema
from app.serializers.truck_serializer import TruckUpdateSchema
from app.models.warehouse.truck import TruckDetails

class WarehouseDelivery(object):

    def get_delivery_details(self,gpm_number,job_type,service_type,service_name,port_name):
        cargo_details = get_job_order_info(gpm_number,service_type,service_name,port_name)
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
        delivery_cargo_query = db.session.query(DeliveryCargoDetails).filter(DeliveryCargoDetails.gpm_number==cargo_details['delivery_details'].get('gpm_number'),DeliveryCargoDetails.gpm_valid_date==cargo_details['delivery_details'].get('gpm_valid_date')).first()
        if delivery_cargo_query:
            job_order_id = delivery_cargo_query.delivery_job[0].id
            cargo_details['id'] = job_order_id
            cargo_details['delivery_details']['id'] = delivery_cargo_query.id
            logger.debug("{}, {}, {}, {}, {}, {}, {}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_ALREADY_EXISTS_CARGO_DETAILS_IN_DB,'JT_'+str(cargo_details.get('job_type')),cargo_details['delivery_details'].get('gpm_number'),job_order_id))
            self.update_bill_details(cargo_details,job_order_id,cargo_details['delivery_details'].get('gpm_number'))
            self.update_truck_details(cargo_details,job_order_id,cargo_details['delivery_details'].get('gpm_number'))
            master_cargo_schema = CCLSCargoUpdateSchema().load(cargo_details, session=db.session)
        else:
            master_cargo_schema = CCLSCargoInsertSchema().load(cargo_details, session=db.session)
        logger.debug("{}, {}, {}, {}, {}, {}, {}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_INSET_OR_UPDATE_DELIVERY_DATA_INTO_DB,'JT_'+str(cargo_details.get('job_type')),cargo_details['delivery_details'].get('gpm_number'),cargo_details))
        db.session.add(master_cargo_schema)
        db.session.commit()

    def update_bill_details(self,cargo_details,job_order_id,request_parameter):
        bill_query = db.session.query(CCLSCargoBillDetails).filter(CCLSCargoBillDetails.job_order_id==job_order_id).all()
        existed_bill_details = CCLSBillDetailsGetSchema().dump(bill_query,many=True)
        logger.debug("{}, {}, {}, {}, {}, {}, {}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_GET_BILL_DETAILS_FROM_DB,'JT_'+str(cargo_details.get('job_type')),request_parameter,existed_bill_details))
        latest_bill_details = cargo_details.pop('bill_details_list')
        for item in latest_bill_details:
            for each_bill in existed_bill_details:
                existed_bill_number = each_bill[constants.BACKEND_BILL_OF_ENTRY_NUMBER] if constants.BACKEND_BILL_OF_ENTRY_NUMBER in each_bill else each_bill[constants.BACKEND_BILL_OF_LADEN_NUMBER]
                latest_bill_number = int(item[constants.CCLS_BILL_OF_ENTRY_NUMBER]) if constants.CCLS_BILL_OF_ENTRY_NUMBER in item else int(item[constants.CCLS_BILL_OF_LADEN_NUMBER])
                if existed_bill_number==latest_bill_number:
                    item['id'] = each_bill['id']
            item['job_order_id'] = job_order_id
        bill_schema = CCLSBillDetailsUpdateSchema().load(latest_bill_details, session=db.session, many=True)
        for each_bill_schema in bill_schema:
            db.session.add(each_bill_schema)


    def update_truck_details(self,cargo_details,job_order_id,request_parameter):
        truck_query = db.session.query(TruckDetails).filter(TruckDetails.job_order_id==job_order_id).all()
        existed_truck_details = TruckUpdateSchema().dump(truck_query,many=True)
        logger.debug("{}, {}, {}, {}, {}, {}, {}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_GET_BILL_DETAILS_FROM_DB,'JT_'+str(cargo_details.get('job_type')),request_parameter,existed_truck_details))
        latest_truck_details = cargo_details.pop('truck_details')
        for item in latest_truck_details:
            for each_truck in existed_truck_details:
                if item[constants.BACKEND_TRUCK_NUMBER] == each_truck[constants.BACKEND_TRUCK_NUMBER]:
                    item['id'] = each_truck['id']
            item['job_order_id'] = job_order_id
        truck_schema = TruckUpdateSchema().load(latest_truck_details, session=db.session, many=True)
        for each_truck_schema in truck_schema:
            db.session.add(each_truck_schema)
