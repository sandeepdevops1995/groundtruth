from app.services.warehouse.soap_api_call import get_job_order_info
from app.logger import logger
import app.services.warehouse.constants as constants
from app.services.warehouse.data_formater import DataFormater
from app import postgres_db as db
from app.enums import JobOrderType,ContainerFlag
from app.serializers.ccls_cargo_serializer import CCLSCargoInsertSchema
from app.models.warehouse.ccls_cargo_details import MasterCargoDetails,StuffingCargoDetails,CCLSCargoBillDetails
from app.user_defined_exception import DataNotFoundException
import app.logging_message as LM
from app.serializers.update_ccls_cargo_serializer import CCLSBillDetailsGetSchema,CCLSBillDetailsUpdateSchema
from app.serializers.update_ccls_cargo_serializer import CCLSCargoUpdateSchema

class WarehouseStuffing(object):

    def get_stuffing_details(self,container_number,job_type,service_type,service_name,port_name):
        cargo_details = get_job_order_info(container_number,service_type,service_name,port_name)
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
        stuffing_cargo_query = db.session.query(StuffingCargoDetails).join(MasterCargoDetails).filter(StuffingCargoDetails.stuffing_job.property.mapper.class_.container_info.property.mapper.class_.container_life==cargo_details['container_info'].get('container_life'),StuffingCargoDetails.container_number==cargo_details['stuffing_details'].get('container_number')).first()
        if stuffing_cargo_query:
            job_order_id = stuffing_cargo_query.stuffing_job[0].id
            cargo_details['id'] = job_order_id
            cargo_details['stuffing_details']['id'] = stuffing_cargo_query.id
            logger.debug("{}, {}, {}, {}, {}, {}, {}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_ALREADY_EXISTS_CARGO_DETAILS_IN_DB,'JT_'+str(cargo_details.get('job_type')),cargo_details['stuffing_details'].get('container_number'),job_order_id))
            self.update_bill_details(cargo_details,job_order_id,cargo_details['stuffing_details'].get('container_number'))
            master_cargo_schema = CCLSCargoUpdateSchema().load(cargo_details, session=db.session)
        else:
            master_cargo_schema = CCLSCargoInsertSchema().load(cargo_details, session=db.session)            
        logger.debug("{}, {}, {}, {}, {}, {}, {}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_INSET_OR_UPDATE_STUFFING_DATA_INTO_DB,'JT_'+str(cargo_details.get('job_type')),cargo_details['stuffing_details'].get('container_number'),cargo_details))
        db.session.add(master_cargo_schema)
        db.session.commit()


    def update_bill_details(self,cargo_details,job_order_id,request_parameter):
        bill_query = db.session.query(CCLSCargoBillDetails).filter(CCLSCargoBillDetails.job_order_id==job_order_id).all()
        existed_bill_details = CCLSBillDetailsGetSchema().dump(bill_query,many=True)
        logger.debug("{}, {}, {}, {}, {}, {}, {}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_GET_BILL_DETAILS_FROM_DB,'JT_'+str(cargo_details.get('job_type')),request_parameter,existed_bill_details))
        latest_bill_details = cargo_details.pop('shipping_bill_details_list')
        for item in latest_bill_details:
            for each_bill in existed_bill_details:
                if int(item[constants.CCLS_SHIPPING_BILL_NUMBER]) == each_bill[constants.CCLS_SHIPPING_BILL_NUMBER]:
                    item['id'] = each_bill['id']
            item['job_order_id'] = job_order_id
        bill_schema = CCLSBillDetailsUpdateSchema().load(latest_bill_details, session=db.session, many=True)
        for each_bill_schema in bill_schema:
            db.session.add(each_bill_schema)