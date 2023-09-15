from app.services.warehouse.database_service import WarehouseDB
from app.enums import JobOrderType
from app import postgres_db as db
from app.models.warehouse.ctms_cargo_job import CTMSCargoJob
from app.models.warehouse.ccls_cargo_details import MasterCargoDetails, CartingCargoDetails, StuffingCargoDetails, DeStuffingCargoDetails, DeliveryCargoDetails
from app.serializers.generate_tallysheet import CTMSCargoJobInsertSchema
from app.serializers.update_tallysheet import CTMSCargoJobUpdateSchema
from app.user_defined_exception import DataNotFoundException
from datetime import datetime
from app.logger import logger
import app.logging_message as LM

class WarehouseTallySheetView(object):

    def get_tally_sheet_info(self,request):
        job_type = int(request.args.get('job_type',0))
        job_order = request.args.get('request_parameter')
        truck_number = request.args.get('truck_number')
        crn_number = request.args.get('crn_number')
        if job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value]:
            query_object = self.get_ctms_job_obj(job_type,crn_number,truck_number,job_order)
        else:
            query_object = self.get_ctms_job_obj(job_type,job_order,truck_number,None)
        result = WarehouseDB().get_tallysheet_details(query_object.first(),job_order,job_type)
        return result
    
    def get_ctms_job_obj(self,job_type,job_order,truck_number,container_number):
        query_object = db.session.query(CTMSCargoJob).filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.job_type==job_type))
        if job_type==JobOrderType.CARTING_FCL.value:
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.carting_details.has(CartingCargoDetails.crn_number==job_order)))
            if truck_number:
                query_object = query_object.filter(CTMSCargoJob.truck_number==truck_number)
        elif job_type==JobOrderType.CARTING_LCL.value:
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.carting_details.has(CartingCargoDetails.carting_order_number==job_order)))
            if truck_number:
                query_object = query_object.filter(CTMSCargoJob.truck_number==truck_number)
        elif job_type==JobOrderType.STUFFING_FCL.value or job_type==JobOrderType.STUFFING_LCL.value or job_type==JobOrderType.DIRECT_STUFFING.value:
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.stuffing_details.has(StuffingCargoDetails.crn_number==job_order)))
            if container_number:
                query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.stuffing_details.has(StuffingCargoDetails.container_number==container_number)))
        elif job_type==JobOrderType.DE_STUFFING_FCL.value or job_type==JobOrderType.DE_STUFFING_LCL.value:
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.destuffing_details.has(DeStuffingCargoDetails.container_number==job_order)))
        elif job_type==JobOrderType.DELIVERY_FCL.value or job_type==JobOrderType.DELIVERY_LCL.value or job_type==JobOrderType.DIRECT_DELIVERY.value:
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.delivery_details.has(DeliveryCargoDetails.gpm_number==job_order)))
            if truck_number:
                query_object = query_object.filter(CTMSCargoJob.truck_number==truck_number)
        query_object = query_object.order_by(CTMSCargoJob.updated_at.desc())
        return query_object
    
    def generate_tally_sheet_info(self,tally_sheet_data):
        job_type = tally_sheet_data['job_type']
        
        query_object = db.session.query(MasterCargoDetails).filter(MasterCargoDetails.job_type==job_type)
        if job_type==JobOrderType.CARTING_FCL.value:
            query_object = query_object.filter(MasterCargoDetails.carting_details.has(CartingCargoDetails.crn_number==tally_sheet_data.get('crn_number')))
        elif job_type==JobOrderType.CARTING_LCL.value:
            query_object = query_object.filter(MasterCargoDetails.carting_details.has(CartingCargoDetails.carting_order_number==tally_sheet_data.get('cargo_carting_number')))
        elif job_type==JobOrderType.STUFFING_FCL.value or job_type==JobOrderType.STUFFING_LCL.value or job_type==JobOrderType.DIRECT_STUFFING.value:
            query_object = query_object.filter(MasterCargoDetails.stuffing_details.has(StuffingCargoDetails.container_number==tally_sheet_data.get('container_number')))
        elif job_type==JobOrderType.DE_STUFFING_FCL.value or job_type==JobOrderType.DE_STUFFING_LCL.value:
            query_object = query_object.filter(MasterCargoDetails.destuffing_details.has(DeStuffingCargoDetails.container_number==tally_sheet_data.get('container_number')))
        elif job_type==JobOrderType.DELIVERY_FCL.value or job_type==JobOrderType.DELIVERY_LCL.value or job_type==JobOrderType.DIRECT_DELIVERY.value:
            query_object = query_object.filter(MasterCargoDetails.delivery_details.has(DeliveryCargoDetails.gpm_number==tally_sheet_data.get('gpm_number')))
            tally_sheet_data['destuffing_date'] = self.get_destuffing_date_for_delivery(tally_sheet_data.get('container_number'))
        query_object = query_object.order_by(MasterCargoDetails.updated_at.desc()).first()
        if query_object:
            job_order_id = query_object.id
            is_exists = self.check_tallysheet_exist_or_not(tally_sheet_data,job_order_id,job_type)
            if not is_exists:
                master_job_request = CTMSCargoJobInsertSchema(context={'job_order_id': job_order_id,"job_type":job_type}).load(tally_sheet_data, session=db.session)
                db.session.add(master_job_request)
                db.session.commit()
                logger.debug("{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GENERATE_TALLYSHEET,LM.KEY_GENERATE_TALLYSHEET_DATA_CREATED_SUCCESSFULLY,tally_sheet_data))
            else:
                logger.debug("{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GENERATE_TALLYSHEET,LM.KEY_GENERATE_TALLYSHEET_DATA_ALREADY_EXISTS,tally_sheet_data))
        else:
            raise DataNotFoundException("GTService: ccls data doesn't exists in database")
        
    def check_tallysheet_exist_or_not(self,tally_sheet_data,job_order_id,job_type):
        qs = db.session.query(CTMSCargoJob).filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.id==job_order_id))
        if job_type in [JobOrderType.CARTING_FCL.value,JobOrderType.CARTING_LCL.value,JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
            query_object = qs.filter(CTMSCargoJob.truck_number==tally_sheet_data.get('truck_number'))
        elif job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value,JobOrderType.DE_STUFFING_FCL.value,JobOrderType.DE_STUFFING_LCL.value]:
            query_object = qs.filter(CTMSCargoJob.container_number==tally_sheet_data.get('container_number'))
        if query_object.first():
            return True
        return False
        
        
    def get_destuffing_date_for_delivery(self,container_number):
        start_time=None
        query_object = db.session.query(CTMSCargoJob).filter(CTMSCargoJob.container_number==container_number).filter((CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.job_type==JobOrderType.DE_STUFFING_FCL.value)) | (CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.job_type==JobOrderType.DE_STUFFING_LCL.value)))
        query_object = query_object.order_by(CTMSCargoJob.created_at.desc()).first()
        if query_object:
            start_time = query_object.job_start_time
        return start_time

    def update_tally_sheet_info(self,tally_sheet_data):
        query_object = db.session.query(CTMSCargoJob).filter(CTMSCargoJob.id==tally_sheet_data.get('id')).first()
        if query_object:
            tally_sheet_data['updated_at'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
            master_job_request = CTMSCargoJobUpdateSchema().load(tally_sheet_data, instance=query_object, session=db.session)
            db.session.add(master_job_request)
            db.session.commit()
        else:
            raise DataNotFoundException("GTService: ccls data doesn't exists in database")
        
    def print_tally_sheet(self,request):
        job_type = int(request.args.get('job_type',0))
        job_order = request.args.get('request_parameter')
        truck_number = request.args.get('truck_number')
        crn_number = request.args.get('crn_number')
        if job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value]:
            query_object = self.get_ctms_job_obj(job_type,crn_number,None,None)
        else:
            query_object = self.get_ctms_job_obj(job_type,job_order,None,None)
        result = WarehouseDB().print_tallysheet_details(query_object.all(),job_order,job_type)
        tallysheet_data = {}
        cargo_details = []
        for each_item in result:
            if job_type in [JobOrderType.CARTING_FCL.value,JobOrderType.CARTING_LCL.value,JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL,JobOrderType.DIRECT_DELIVERY.value]:
                if each_item['cargo_details'][0]['truck_number'] == truck_number:
                    tallysheet_data = each_item
            elif job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value]:
                if each_item['crn_number'] == crn_number:
                    tallysheet_data = each_item
            else:
                tallysheet_data = each_item
            cargo_details+=each_item.pop('cargo_details')
        tallysheet_data['cargo_details'] = cargo_details
        self.update_start_and_end_time(tallysheet_data)
        return tallysheet_data
    
    def update_start_and_end_time(self,tallysheet_data):
        min_start_time = min(tallysheet_data['cargo_details'], key=lambda x:x['start_time'])['start_time'] if tallysheet_data['cargo_details'] else None
        max_end_time = max(tallysheet_data['cargo_details'], key=lambda x:x['end_time'])['end_time'] if tallysheet_data['cargo_details'] else None
        tallysheet_data['start_time'] = min_start_time
        tallysheet_data['end_time'] = max_end_time
