from app.logger import logger
from app import postgres_db as db
from app.serializers.commodity_serializer import CCLSCommodityList
from app.models.master.warehouse import Commodity as WarehouseCommodity
from app.serializers.view_tallysheet import ViewTallySheetOrderSchema
import app.logging_message as LM
from app.models.warehouse.ccls_cargo_details import MasterCargoDetails, CartingCargoDetails, StuffingCargoDetails, DeStuffingCargoDetails, DeliveryCargoDetails
from app.serializers.get_ccls_cargo_serializer import GetCCLSJobSchema
from app.enums import JobOrderType
from app.user_defined_exception import DataNotFoundException

class WarehouseDB(object):

    def get_tallysheet_details(self,query_object,request_parameter,job_type):
        result = {}
        if query_object:
            result = ViewTallySheetOrderSchema().dump(query_object)
        logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_VIEW_TALLYSHEET,LM.KEY_FETCH_TALLYSHEET_DATA_FROM_DATABASE,'JT_'+str(job_type),request_parameter,result))
        return result
    
    def upload_tallysheet_details(self,query_object,request_parameter,job_type):
        result = {}
        if query_object:
            result = ViewTallySheetOrderSchema().dump(query_object,many=True)
        logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_VIEW_TALLYSHEET,LM.KEY_FETCH_TALLYSHEET_DATA_FROM_DATABASE,'JT_'+str(job_type),request_parameter,result))
        return result
    
    def print_tallysheet_details(self,query_object,request_parameter,job_type):
        result = []
        if query_object:
            if job_type in [JobOrderType.DE_STUFFING_FCL.value,JobOrderType.DE_STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value]:
                result = ViewTallySheetOrderSchema().dump(query_object)
            else:
                result = ViewTallySheetOrderSchema().dump(query_object,many=True)
        logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_PRINT_TALLYSHEET,LM.KEY_FETCH_TALLYSHEET_DATA_FROM_DATABASE,'JT_'+str(job_type),request_parameter))
        return result
    
    def get_commodities(self):
        result = {}
        query_object = db.session.query(WarehouseCommodity).all()
        if query_object:
            result = CCLSCommodityList().dump(query_object,many=True)
        logger.info("GTService: commodities result lenght %s",len(result))
        return result
    
    def save_commodities(self,commodity_data):
        for each_commodity in commodity_data:
            each_commodity = {k.lower(): v for k, v in each_commodity.items()}
            commodity_code = int(each_commodity['comm_cd'])
            logger.info("GTService: commodity_code--------%d",commodity_code)
            each_commodity['srvc_exmp_cat_flg'] = str(int(each_commodity['srvc_exmp_cat_flg'])) if 'srvc_exmp_cat_flg' in each_commodity and each_commodity['srvc_exmp_cat_flg']!=None else 0
            db_object = db.session.query(WarehouseCommodity).filter(WarehouseCommodity.comm_cd==commodity_code)
            if db_object.first():
                db_object.update(dict(each_commodity))
                logger.info("GTService: commodity details updated successfully")
            else:
                db_object = WarehouseCommodity(**each_commodity)
                db.session.add(db_object, _warn=False)
        db.session.commit()
        logger.info("GTService: commodity details created successfully")

    def get_cargo_details_from_db(self,request_parameter,job_type):
        if job_type==JobOrderType.CARTING_FCL.value:
            query_object = db.session.query(MasterCargoDetails).filter(MasterCargoDetails.carting_details.has(CartingCargoDetails.crn_number==request_parameter)).order_by(MasterCargoDetails.created_at.desc()).first()
        elif job_type==JobOrderType.CARTING_LCL.value:
            query_object = db.session.query(MasterCargoDetails).filter(MasterCargoDetails.carting_details.has(CartingCargoDetails.carting_order_number==request_parameter)).order_by(MasterCargoDetails.created_at.desc()).first()
        elif job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value]:
            query_object = db.session.query(MasterCargoDetails).filter(MasterCargoDetails.stuffing_details.has(StuffingCargoDetails.container_number==request_parameter)).order_by(MasterCargoDetails.created_at.desc()).first()
        elif job_type in [JobOrderType.DE_STUFFING_FCL.value,JobOrderType.DE_STUFFING_LCL.value]:
            query_object = db.session.query(MasterCargoDetails).filter(MasterCargoDetails.destuffing_details.has(DeStuffingCargoDetails.container_number==request_parameter)).order_by(MasterCargoDetails.created_at.desc()).first()
        elif job_type in [JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
            query_object = db.session.query(MasterCargoDetails).filter(MasterCargoDetails.delivery_details.has(DeliveryCargoDetails.gpm_number==request_parameter)).order_by(MasterCargoDetails.created_at.desc()).first()
        else:
            query_object = None
        if query_object:
            result = GetCCLSJobSchema().dump(query_object)
            total_package_count = 0
            result['cargo_details'] = result.pop('bill_details')
            for each_cargo in result['cargo_details']:
                for each_commodity in each_cargo['commodity_details']:
                    total_package_count+=each_commodity['package_count']
            result['total_package_count'] = total_package_count
            logger.debug("{}, {}, {}, {}, {}, {}, {}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_GET_CARGO_DETAILS_FROM_DB,'JT_'+str(job_type),request_parameter,result))
            return result
        else:
            raise DataNotFoundException('GTService: job data not found in ccls system')