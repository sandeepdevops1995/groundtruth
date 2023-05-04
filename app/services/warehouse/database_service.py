# from app.models.warehouse.bill_details import CCLSCargoDetails,CTMSCargoDetails
# from app.models.warehouse.job_order import CCLSJobOrder,CTMSJobOrder
from app.models.warehouse.truck import TruckDetails
from app.models.warehouse.container import Container
from app.logger import logger
from app import postgres_db as db
from app.services.warehouse.data_formater import DataFormater
from app.serializers.commodity_serializer import CCLSCommodityList
from app.enums import JobOrderType,JobStatus
from app.models.master.warehouse import Commodity as WarehouseCommodity
from app.serializers.view_tallysheet import ViewTallySheetOrderSchema

class WarehouseDB(object):

    def get_tallysheet_details(self,query_object,request_parameter):
        result = {}
        if query_object:
            result = ViewTallySheetOrderSchema().dump(query_object)
            # result = result[0] if result else {}
        logger.info("{},{},{}:{}".format("GTService: tallysheet details from database" ,result,"job_order",request_parameter))
        return result
    
    def get_commodities(self):
        result = {}
        query_object = db.session.query(WarehouseCommodity).all()
        if query_object:
            result = CCLSCommodityList().dump(query_object,many=True)
        logger.info("GTService: commodities from db------------")
        return result
    
    def save_commodities(self,commodity_data):
        for each_commodity in commodity_data:
            each_commodity = {k.lower(): v for k, v in each_commodity.items()}
            commodity_code = int(each_commodity['comm_cd'])
            logger.info("GTService: commodity_code--------%d",commodity_code)
            each_commodity['srvc_exmp_cat_flg'] = str(int(each_commodity['srvc_exmp_cat_flg'])) if 'srvc_exmp_cat_flg' in each_commodity and each_commodity['srvc_exmp_cat_flg']!=None else 0
            query_object = db.session.query(WarehouseCommodity).filter(WarehouseCommodity.comm_cd==commodity_code)
            if query_object.first():
                query_object.update(dict(each_commodity))
                logger.info("GTService: commodity details updated successfully")
            else:
                db_object = WarehouseCommodity(**each_commodity)
                db.session.add(db_object, _warn=False)
        db.session.commit()
        db.session.refresh(db_object)
        logger.info("GTService: commodity details created successfully")