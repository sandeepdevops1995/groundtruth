from app.models.warehouse.bill_details import CCLSCargoDetails,CTMSCargoDetails
from app.models.warehouse.job_order import CCLSJobOrder,CTMSJobOrder
from app.models.warehouse.truck import TruckDetails
from app.models.warehouse.container import Container
from app.logger import logger
from app import postgres_db as db
from app.services.warehouse.data_formater import DataFormater
from app.serializers.job_order import CCLSJobOrderSchema,CCLSCommodityList
from app.enums import JobOrderType,JobStatus
from app.models.master.warehouse import Commodity as WarehouseCommodity

class WarehouseDB(object):

    def save_container_details(self,job_order_details):
        container_details = DataFormater().container_table_formater(job_order_details)
        container_number = container_details.get('container_number',None)
        if container_number:
            db_object = db.session.query(Container).filter(Container.container_number == container_details.get('container_number',None)).first()
            if db_object:
                logger.info("GTService: container already exists in db")
                return db_object.container_number
            try:
                db_object = Container(**container_details)
                db.session.add(db_object)
                db.session.commit()
                db.session.refresh(db_object)
                logger.info("GTService: container created successfully")
                return db_object.container_number
            except Exception as e:
                logger.exception(e)
                db.session.rollback()
                raise

    
    def save_ccls_job_order(self,job_order_details,container_id,query_object):
        job_order_details = DataFormater().ccls_job_order_table_formater(job_order_details)
        print("job_order_details-----",job_order_details)
        job_order_details['container_id'] = container_id
        db_object = query_object.first()
        if db_object:
            query_object.update(dict(job_order_details))
            # db.session.add(db_object)
            db.session.commit()
            # db.session.refresh(db_object)
            logger.info("GTService: delivery job orders updated successfully")
        else:
            db_object = CCLSJobOrder(**job_order_details)
            db.session.add(db_object)
            db.session.commit()
            db.session.refresh(db_object)
            logger.info("GTService: delivery job orders created successfully")
        return db_object.id
            

    def save_ccls_cargo_details(self,bill_details,job_order_id,filter_key):
        for each_bill_info in bill_details:
            commodity_code = each_bill_info.pop('commodity_code')
            commodity_description = each_bill_info.pop('commodity_description')
            each_bill_info = DataFormater().ccls_cargo_details_table_formater(each_bill_info)
            commodity_id = self.get_commodity_instance(commodity_code,commodity_description)
            each_bill_info.update({"job_order_id":job_order_id,"commodity_id":commodity_id})
            filter_data = {filter_key:each_bill_info[filter_key],"job_order_id":job_order_id}
            query_object = db.session.query(CCLSCargoDetails).filter_by(**filter_data)
            # db_object = query_object.first()
            if query_object.first():
                query_object.update(dict(each_bill_info))
                db.session.commit()
                logger.info("GTService: cargo details updated successfully")
            else:
                db_object = CCLSCargoDetails(**each_bill_info)
                db.session.add(db_object, _warn=False)
                db.session.commit()
                db.session.refresh(db_object)
                logger.info("GTService: cargo details created successfully")

    def save_ctms_job_order(self,job_order_details,query_object,ccls_query_object):
        # job_order_details = DataFormater().ccls_job_order_table_formater(job_order_details)
        #print("job_order_details-----",job_order_details)
        #query_object = db.session.query(CTMSJobOrder).join(CCLSJobOrder).filter(CCLSJobOrder.crn_number==filter_data['crn_number'])
        # .filter_by(**filter_data)
        db_object = query_object.first()
        if db_object:
            db.session.query(CTMSJobOrder).filter(CTMSJobOrder.id==db_object.id).update(dict(job_order_details))
            # db.session.add(db_object)
            db.session.commit()
            # db.session.refresh(db_object)
            logger.info("GTService: job orders updated successfully")
        else:
            db_object = CTMSJobOrder(**job_order_details)
            db.session.add(db_object)
            db.session.commit()
            db.session.refresh(db_object)
            logger.info("GTService: job orders created successfully")
            self.update_ctms_job_order_in_ccls_job_order(db_object.id,ccls_query_object)
        return db_object.id
    
    def update_ctms_job_order_in_ccls_job_order(self,ctms_job_order_id,ccls_query_object):
        # filter_data = {}
        # print("ctms_job_order_id---------",ctms_job_order_id,filter_data)
        # query_object = db.session.query(CCLSJobOrder).filter_by(**filter_data)
        # if query_object:
        ccls_query_object.update(dict({'ctms_job_order_id':ctms_job_order_id}))#,"status":JobStatus.TALLYSHEET_GENERATED.value}))
        db.session.commit()
        logger.info("GTService: update ctms job order object in ccls job order table")
    
    def save_ctms_bill_details(self,bill_details,job_order_id,filter_key,job_type):
        for each_bill_info in bill_details:
            # commodity_code = each_bill_info.pop('commodity_code')
            # commodity_description = each_bill_info.pop('commodity_description')
            # commodity_id = self.get_commodity_instance(commodity_code,commodity_description)
            # each_bill_info.update({"job_order_id":job_order_id,"commodity_id":commodity_id})
            # filter_data = {filter_key:each_bill_info['shipping_bill']}
            # filter_data = {'CCLSCargoDetails.shipping_bill':each_bill_info['shipping_bill']}
            query_obj  = db.session.query(CCLSJobOrder).filter(CCLSJobOrder.ctms_job_order_id==job_order_id).first()
            if  query_obj:
                job_order_id = query_obj.id
                print("job_order_id--------",job_order_id)
            bill_number=each_bill_info[filter_key]
            each_bill_info = DataFormater().ctms_cargo_details_table_formater(each_bill_info)
            print("each_bill_info-----------save_ctms_bill_details",each_bill_info)
            if job_type in [JobOrderType.CARTING_FCL.value,JobOrderType.CARTING_LCL.value,JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value]:
                query_object = db.session.query(CTMSCargoDetails).join(CCLSCargoDetails).filter(CCLSCargoDetails.shipping_bill==bill_number,CCLSCargoDetails.job_order_id==job_order_id)
            elif job_type==JobOrderType.DE_STUFFING_FCL.value:
                query_object = db.session.query(CTMSCargoDetails).join(CCLSCargoDetails).filter(CCLSCargoDetails.bill_of_entry==bill_number,CCLSCargoDetails.job_order_id==job_order_id)
            elif job_type==JobOrderType.DE_STUFFING_LCL.value:
                query_object = db.session.query(CTMSCargoDetails).join(CCLSCargoDetails).filter(CCLSCargoDetails.bill_of_lading==bill_number,CCLSCargoDetails.job_order_id==job_order_id)
            elif job_type==JobOrderType.DELIVERY_FCL.value or job_type==JobOrderType.DELIVERY_LCL.value or job_type==JobOrderType.DIRECT_DELIVERY.value:
                query_object = db.session.query(CTMSCargoDetails).join(CCLSCargoDetails).filter(CCLSCargoDetails.bill_of_entry==bill_number,CCLSCargoDetails.job_order_id==job_order_id)
            # .filter_by(**filter_data)
            db_object = query_object.first()
            if db_object:
                update_obj = db.session.query(CTMSCargoDetails).filter(CTMSCargoDetails.id == db_object.id).update(dict(each_bill_info))
                db.session.commit()
                logger.info("GTService: CTMS cargo details updated successfully %s",update_obj)
            else:
                db_object = CTMSCargoDetails(**each_bill_info)
                db.session.add(db_object, _warn=False)
                db.session.commit()
                db.session.refresh(db_object)
                
                logger.info("GTService: CTMS cargo details created successfully")
                self.update_ctms_cargo_details_in_ccls_cargo_details(db_object.id,bill_number,job_order_id,filter_key)

    def update_ctms_cargo_details_in_ccls_cargo_details(self,cargo_id,bill_number,job_order_id,filter_key):
        # filter_data = {}
        
        query_object = db.session.query(CCLSCargoDetails).filter_by(**{filter_key:bill_number,"job_order_id":job_order_id})
        if query_object:
            query_object.update(dict({'ctms_cargo_id':cargo_id}))
            db.session.commit()
            logger.info("GTService: update ctms cargo details object in ccls cargo details table")

    def get_commodity_instance(self,commodity_code,commodity_description):
        db_object = db.session.query(WarehouseCommodity).filter(WarehouseCommodity.comm_cd == commodity_code).first()
        if db_object:
            logger.info("GTService: commodity already exists in db")
            return db_object.id
        db_object = WarehouseCommodity(comm_cd=commodity_code,comm_desc=commodity_description)
        db.session.add(db_object)
        db.session.commit()
        db.session.refresh(db_object)
        logger.info("GTService: commodity created successfully")
        return db_object.id
    
    def save_truck_details(self,truck_details,job_order_id):
        from datetime import datetime
        for each_truck in truck_details:
            each_truck['job_order_id'] = job_order_id
            each_truck['truck_arrival_date'] = each_truck['truck_arrival_date']
            truck_number = each_truck.get('truck_number',None)
            db_object = db.session.query(TruckDetails).filter(TruckDetails.truck_number == truck_number,TruckDetails.job_order_id == job_order_id).first()
            if not db_object:
                db_object = TruckDetails(**each_truck)
                db.session.add(db_object)
                db.session.commit()
                db.session.refresh(db_object)
                logger.info("GTService: truck created successfully")

    def get_final_job_details(self,query_object,request_parameter):
        result = {}
        if query_object:
            result = CCLSJobOrderSchema().dump(query_object,many=True)
            result = result[0] if result else {}
        logger.info("{},{},{}:{}".format("GTService: tallysheet details from database" ,result,"job_order",request_parameter))
        return result
    
    def get_commodities(self):
        result = {}
        query_object = db.session.query(WarehouseCommodity).all()
        if query_object:
            result = CCLSCommodityList().dump(query_object,many=True)
        logger.info("GTService: commodities from db------------",result)
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