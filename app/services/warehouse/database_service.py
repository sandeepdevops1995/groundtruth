from app.Models.warehouse.bill_details import CCLSCargoDetails,CTMSCargoDetails
from app.Models.warehouse.job_order import CCLSJobOrder,CTMSJobOrder
from app.Models.warehouse.commodity import WarehouseCommodity
from app.Models.warehouse.truck import TruckDetails
from app.Models.warehouse.container import Container
from app.logger import logger
from app import postgres_db as db
from app.services.warehouse.data_formater import DataFormater
from app.serializers.job_order import CCLSJobOrderSchema,CCLSCommodityList
from app.enums import JobOrderType
from app.Models.warehouse.commodity import WarehouseCommodity

class WarehouseDB(object):

    def save_container_details(self,job_order_details):
        container_details = DataFormater().container_table_formater(job_order_details)
        container_number = container_details.get('container_number',None)
        if container_number:
            db_object = db.session.query(Container).filter(Container.container_number == container_details.get('container_number',None)).first()
            if db_object:
                logger.info("container already exists in db")
                return db_object.container_number
            try:
                db_object = Container(**container_details)
                db.session.add(db_object)
                db.session.commit()
                db.session.refresh(db_object)
                logger.info("container created successfully")
                return db_object.container_number
            except Exception as e:
                logger.error(e)
                db.session.rollback()



    # def save_carting_job_order(self,job_order_details,container_id,filter_data):
    #     job_order_details = DataFormater().ccls_job_order_table_formater(job_order_details)
    #     print("job_order_details-----",job_order_details)
    #     job_order_details['container_id'] = container_id
    #     query_object = db.session.query(CCLSJobOrder).filter_by(**filter_data)
    #     db_object = query_object.first()
    #     if db_object:
    #         query_object.update(dict(job_order_details))
    #         # db.session.add(db_object)
    #         db.session.commit()
    #         # db.session.refresh(db_object)
    #         logger.info("carting job orders updated successfully")
    #     else:
    #         db_object = CCLSJobOrder(**job_order_details)
    #         db.session.add(db_object)
    #         db.session.commit()
    #         db.session.refresh(db_object)
    #         logger.info("cartingjob orders created successfully")
    #     return db_object.id
    
    # def save_stuffing_job_order(self,job_order_details,container_id,container_number):
    #     job_order_details = DataFormater().ccls_job_order_table_formater(job_order_details)
    #     print("job_order_details-----",job_order_details)
    #     job_order_details['container_id'] = container_id
    #     query_object = db.session.query(CCLSJobOrder).join(Container).filter(Container.container_number==container_number,CCLSJobOrder.status==JobStatus.COMPLETED.value)
    #     db_object = query_object.first()
    #     if db_object:
    #         db.session.query(CCLSJobOrder).filter(id==db_object.id).update(dict(job_order_details))
    #         # db.session.add(db_object)
    #         db.session.commit()
    #         # db.session.refresh(db_object)
    #         logger.info("stuffing job orders updated successfully")
    #     else:
    #         db_object = CCLSJobOrder(**job_order_details)
    #         db.session.add(db_object)
    #         db.session.commit()
    #         db.session.refresh(db_object)
    #         logger.info("stuffing job orders created successfully")
    #     return db_object.id
    
    # def save_destuffing_job_order(self,job_order_details,container_id,container_number):
    #     job_order_details = DataFormater().ccls_job_order_table_formater(job_order_details)
    #     print("job_order_details-----",job_order_details)
    #     job_order_details['container_id'] = container_id
    #     query_object = db.session.query(CCLSJobOrder).join(Container).filter(Container.container_number==container_number,CCLSJobOrder.status==JobStatus.COMPLETED.value)
    #     db_object = query_object.first()
    #     if db_object:
    #         db.session.query(CCLSJobOrder).filter(id==db_object.id).update(dict(job_order_details))
    #         # db.session.add(db_object)
    #         db.session.commit()
    #         # db.session.refresh(db_object)
    #         logger.info("destuffing job orders updated successfully")
    #     else:
    #         db_object = CCLSJobOrder(**job_order_details)
    #         db.session.add(db_object)
    #         db.session.commit()
    #         db.session.refresh(db_object)
    #         logger.info("destuffing job orders created successfully")
    #     return db_object.id
    
    # def save_delivery_job_order(self,job_order_details,container_id,filter_data):
    #     job_order_details = DataFormater().ccls_job_order_table_formater(job_order_details)
    #     print("job_order_details-----",job_order_details)
    #     job_order_details['container_id'] = container_id
    #     query_object = db.session.query(CCLSJobOrder).filter_by(**filter_data)
    #     db_object = query_object.first()
    #     if db_object:
    #         query_object.update(dict(job_order_details))
    #         # db.session.add(db_object)
    #         db.session.commit()
    #         # db.session.refresh(db_object)
    #         logger.info("delivery job orders updated successfully")
    #     else:
    #         db_object = CCLSJobOrder(**job_order_details)
    #         db.session.add(db_object)
    #         db.session.commit()
    #         db.session.refresh(db_object)
    #         logger.info("delivery job orders created successfully")
    #     return db_object.id
    
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
            logger.info("delivery job orders updated successfully")
        else:
            db_object = CCLSJobOrder(**job_order_details)
            db.session.add(db_object)
            db.session.commit()
            db.session.refresh(db_object)
            logger.info("delivery job orders created successfully")
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
                logger.info("cargo details updated successfully")
            else:
                db_object = CCLSCargoDetails(**each_bill_info)
                db.session.add(db_object, _warn=False)
                db.session.commit()
                db.session.refresh(db_object)
                logger.info("cargo details created successfully")

    def save_ctms_job_order(self,job_order_details,query_object,filter_data):
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
            logger.info("job orders updated successfully")
        else:
            db_object = CTMSJobOrder(**job_order_details)
            db.session.add(db_object)
            db.session.commit()
            db.session.refresh(db_object)
            logger.info("job orders created successfully")
            self.update_ctms_job_order_in_ccls_job_order(db_object.id,filter_data)
        return db_object.id
    
    def update_ctms_job_order_in_ccls_job_order(self,ctms_job_order_id,filter_data):
        # filter_data = {}
        print("ctms_job_order_id---------",ctms_job_order_id,filter_data)
        query_object = db.session.query(CCLSJobOrder).filter_by(**filter_data)
        if query_object:
            query_object.update(dict({'ctms_job_order_id':ctms_job_order_id}))
            db.session.commit()
            logger.info("update ctms job order object in ccls job order table")
    
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
                logger.info("CTMS cargo details updated successfully %s",update_obj)
            else:
                db_object = CTMSCargoDetails(**each_bill_info)
                db.session.add(db_object, _warn=False)
                db.session.commit()
                db.session.refresh(db_object)
                
                logger.info("CTMS cargo details created successfully")
                self.update_ctms_cargo_details_in_ccls_cargo_details(db_object.id,bill_number,job_order_id,filter_key)

    def update_ctms_cargo_details_in_ccls_cargo_details(self,cargo_id,bill_number,job_order_id,filter_key):
        # filter_data = {}
        
        query_object = db.session.query(CCLSCargoDetails).filter_by(**{filter_key:bill_number,"job_order_id":job_order_id})
        if query_object:
            query_object.update(dict({'ctms_cargo_id':cargo_id}))
            db.session.commit()
            logger.info("update ctms cargo details object in ccls cargo details table")

    def get_commodity_instance(self,commodity_code,commodity_description):
        db_object = db.session.query(WarehouseCommodity).filter(WarehouseCommodity.COMM_CD == commodity_code).first()
        if db_object:
            logger.info("commodity already exists in db")
            return db_object.id
        db_object = WarehouseCommodity(COMM_CD=commodity_code,COMM_DESC=commodity_description)
        db.session.add(db_object)
        db.session.commit()
        db.session.refresh(db_object)
        logger.info("commodity created successfully")
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
                logger.info("truck created successfully")

    def get_final_job_details(self,query_object):
        result = {}
        if query_object:
            result = CCLSJobOrderSchema().dump(query_object)
        logger.info("job details from database------------%s",result)
        return result
    
    def get_commodities(self):
        result = {}
        query_object = db.session.query(WarehouseCommodity).all()
        if query_object:
            result = CCLSCommodityList().dump(query_object,many=True)
        logger.info("commodities from db------------",result)
        return result
    
    def save_commodities(self,commodity_data):
        for each_commodity in commodity_data:
            try:
                commodity_code = int(each_commodity['COMM_CD'])
                logger.info("commodity_code--------%d",commodity_code)
                each_commodity['SRVC_EXMP_CAT_FLG'] = str(int(each_commodity['SRVC_EXMP_CAT_FLG'])) if 'SRVC_EXMP_CAT_FLG' in each_commodity and each_commodity['SRVC_EXMP_CAT_FLG']!=None else None
                query_object = db.session.query(WarehouseCommodity).filter(WarehouseCommodity.COMM_CD==commodity_code)
                if query_object.first():
                    query_object.update(dict(each_commodity))
                    logger.info("commodity details updated successfully")
                else:
                    db_object = WarehouseCommodity(**each_commodity)
                    db.session.add(db_object, _warn=False)
                    db.session.commit()
                    db.session.refresh(db_object)
                    logger.info("commodity details created successfully")
            except Exception as e:
                logger.error("getting error while saving commodities %s",e)