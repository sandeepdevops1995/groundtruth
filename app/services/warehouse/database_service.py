from app.logger import logger
from app import postgres_db as db
from app.serializers.commodity_serializer import CCLSCommodityList
from app.models.master.warehouse import Commodity as WarehouseCommodity
from app.serializers.view_tallysheet import ViewTallySheetOrderSchema
import app.logging_message as LM

class WarehouseDB(object):

    def get_tallysheet_details(self,query_object,request_parameter,job_type):
        result = {}
        if query_object:
            result = ViewTallySheetOrderSchema().dump(query_object)
        logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_VIEW_TALLYSHEET,LM.KEY_FETCH_TALLYSHEET_DATA_FROM_DATABASE,'JT_'+str(job_type),request_parameter,result))
        return result
    
    def print_tallysheet_details(self,query_object,request_parameter,job_type):
        result = []
        if query_object:
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