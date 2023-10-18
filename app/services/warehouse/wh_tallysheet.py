from app.services.warehouse.database_service import WarehouseDB
from app.enums import JobOrderType, JobStatus
from app import postgres_db as db
from app.models.warehouse.ctms_cargo_job import CTMSCargoJob
from app.models.warehouse.ccls_cargo_details import MasterCargoDetails, CartingCargoDetails, StuffingCargoDetails, DeStuffingCargoDetails, DeliveryCargoDetails, CCLSCargoBillDetails
from app.serializers.generate_tallysheet import CTMSCargoJobInsertSchema
from app.serializers.update_tallysheet import CTMSCargoJobUpdateSchema
from app.user_defined_exception import DataNotFoundException
from datetime import datetime
from app.logger import logger
import app.logging_message as LM
import json
import pandas as pd
from app.serializers.get_ccls_cargo_serializer import CCLSCargoDetailsSchema

class WarehouseTallySheetView(object):

    def get_tally_sheet_info(self,request):
        job_type = int(request.args.get('job_type',0))
        job_order = request.args.get('request_parameter')
        truck_number = request.args.get('truck_number')
        crn_number = request.args.get('crn_number')
        date_key_name = self.get_date_key_name(job_type)
        filter_date = request.args.get(date_key_name)
        bills = json.loads(request.args.get('bills'))
        if job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value]:
            query_object = self.get_ctms_job_obj(job_type,crn_number,truck_number,job_order,bills,filter_date)
        else:
            query_object = self.get_ctms_job_obj(job_type,job_order,truck_number,None,bills,filter_date)
        query_object = self.filter_with_bill_details(query_object,bills,job_type)
        result = WarehouseDB().get_tallysheet_details(query_object.first(),job_order,job_type)
        return result
    
    def get_date_key_name(self,job_type):
        if job_type in [JobOrderType.CARTING_FCL.value,JobOrderType.STUFFING_FCL.value,JobOrderType.DIRECT_STUFFING.value]:
            date_key_name = 'crn_date'
        elif job_type in [JobOrderType.CARTING_LCL.value,JobOrderType.STUFFING_LCL.value]:
            date_key_name = 'con_date'
        elif job_type in [JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
            date_key_name = 'gpm_created_date'
        else:
            date_key_name = 'None'
        return date_key_name
    
    def get_ctms_job_obj(self,job_type,job_order,truck_number,container_number,bills,filter_date):
        query_object = db.session.query(CTMSCargoJob).filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.job_type==job_type))
        if job_type==JobOrderType.CARTING_FCL.value:
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.carting_details.has(CartingCargoDetails.crn_number==job_order)))
            if filter_date:
                query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.carting_details.has(CartingCargoDetails.crn_date==filter_date)))
            if truck_number:
                query_object = query_object.filter(CTMSCargoJob.truck_number==truck_number)
        elif job_type==JobOrderType.CARTING_LCL.value:
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.carting_details.has(CartingCargoDetails.carting_order_number==job_order)))
            if filter_date:
                query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.carting_details.has(CartingCargoDetails.con_date==filter_date)))
            if truck_number:
                query_object = query_object.filter(CTMSCargoJob.truck_number==truck_number)
        elif job_type==JobOrderType.STUFFING_FCL.value or job_type==JobOrderType.STUFFING_LCL.value or job_type==JobOrderType.DIRECT_STUFFING.value:
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.stuffing_details.has(StuffingCargoDetails.crn_number==job_order)))
            if filter_date:
                query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.stuffing_details.has(StuffingCargoDetails.crn_date==filter_date)))
            if container_number:
                query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.stuffing_details.has(StuffingCargoDetails.container_number==container_number)))
        elif job_type==JobOrderType.DE_STUFFING_FCL.value or job_type==JobOrderType.DE_STUFFING_LCL.value:
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.destuffing_details.has(DeStuffingCargoDetails.container_number==job_order)))
        elif job_type==JobOrderType.DELIVERY_FCL.value or job_type==JobOrderType.DELIVERY_LCL.value or job_type==JobOrderType.DIRECT_DELIVERY.value:
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.delivery_details.has(DeliveryCargoDetails.gpm_number==job_order)))
            if filter_date:
                query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.delivery_details.has(DeliveryCargoDetails.gpm_created_date==filter_date)))
            if truck_number:
                query_object = query_object.filter(CTMSCargoJob.truck_number==truck_number)
        query_object = query_object.order_by(CTMSCargoJob.updated_at.desc())
        return query_object
    
    def filter_with_bill_details(self,query_object,bills,job_type):
        for each_bill in bills:
            if job_type in [JobOrderType.CARTING_FCL.value, JobOrderType.CARTING_LCL.value, JobOrderType.STUFFING_FCL.value, JobOrderType.STUFFING_LCL.value, JobOrderType.DIRECT_STUFFING.value]:
                query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.bill_details.any(CCLSCargoBillDetails.shipping_bill_number==each_bill['bill_number'])))
                # .filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.bill_details.any(CCLSCargoBillDetails.bill_date==each_bill['bill_date'])))
            elif job_type in [JobOrderType.DE_STUFFING_FCL.value, JobOrderType.DELIVERY_FCL.value, JobOrderType.DELIVERY_LCL.value, JobOrderType.DIRECT_DELIVERY.value]:
                query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.bill_details.any(CCLSCargoBillDetails.bill_of_entry==each_bill['bill_number'])))
                # .filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.bill_details.any(CCLSCargoBillDetails.bill_date==each_bill['bill_date'])))
            else:
                query_object = query_object.filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.bill_details.any(CCLSCargoBillDetails.bill_of_lading==each_bill['bill_number'])))
                # .filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.bill_details.any(CCLSCargoBillDetails.bol_date==each_bill['bill_date'])))
        return query_object
    
    def generate_tally_sheet_info(self,tally_sheet_data):
        job_type = tally_sheet_data['job_type']
        
        query_object = db.session.query(MasterCargoDetails).filter(MasterCargoDetails.job_type==job_type)
        if job_type==JobOrderType.CARTING_FCL.value:
            request_parameter = tally_sheet_data.get('crn_number')
            query_object = query_object.filter(MasterCargoDetails.carting_details.has(CartingCargoDetails.crn_number==tally_sheet_data.get('crn_number')))
        elif job_type==JobOrderType.CARTING_LCL.value:
            request_parameter = tally_sheet_data.get('cargo_carting_number')
            query_object = query_object.filter(MasterCargoDetails.carting_details.has(CartingCargoDetails.carting_order_number==tally_sheet_data.get('cargo_carting_number')))
        elif job_type==JobOrderType.STUFFING_FCL.value or job_type==JobOrderType.STUFFING_LCL.value or job_type==JobOrderType.DIRECT_STUFFING.value:
            request_parameter = tally_sheet_data.get('container_number')
            query_object = query_object.filter(MasterCargoDetails.stuffing_details.has(StuffingCargoDetails.container_number==tally_sheet_data.get('container_number')))
        elif job_type==JobOrderType.DE_STUFFING_FCL.value or job_type==JobOrderType.DE_STUFFING_LCL.value:
            request_parameter = tally_sheet_data.get('container_number')
            query_object = query_object.filter(MasterCargoDetails.destuffing_details.has(DeStuffingCargoDetails.container_number==tally_sheet_data.get('container_number')))
        elif job_type==JobOrderType.DELIVERY_FCL.value or job_type==JobOrderType.DELIVERY_LCL.value or job_type==JobOrderType.DIRECT_DELIVERY.value:
            request_parameter = tally_sheet_data.get('gpm_number')
            query_object = query_object.filter(MasterCargoDetails.delivery_details.has(DeliveryCargoDetails.gpm_number==tally_sheet_data.get('gpm_number')))
            tally_sheet_data['destuffing_date'] = self.get_destuffing_date_for_delivery(tally_sheet_data.get('container_number'))
        query_object = query_object.order_by(MasterCargoDetails.updated_at.desc()).first()
        if query_object:
            job_order_id = query_object.id
            is_exists,ctms_query_object = self.check_tallysheet_exist_or_not(tally_sheet_data,job_order_id,job_type)
            if not is_exists:
                master_job_request = CTMSCargoJobInsertSchema(context={'job_order_id': job_order_id,"job_type":job_type}).load(tally_sheet_data, session=db.session)
                db.session.add(master_job_request)
                db.session.commit()
                ctms_job_id   = master_job_request.id
                is_required_to_send_data_to_ccls = True
                logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GENERATE_TALLYSHEET,LM.KEY_GENERATE_TALLYSHEET_DATA_CREATED_SUCCESSFULLY,tally_sheet_data,ctms_job_id,is_required_to_send_data_to_ccls))
                
            else:
                is_required_to_send_data_to_ccls = False
                if ctms_query_object.filter(CTMSCargoJob.status==JobStatus.TALLYSHEET_GENERATED.value).first():
                    is_required_to_send_data_to_ccls = True
                ctms_job_id   = ctms_query_object.first().id
                #tally_sheet_data['id'] = ctms_query_object.id
                # master_job_request = CTMSCargoJobUpdateSchema().load(tally_sheet_data, instance=ctms_query_object, session=db.session)
                logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GENERATE_TALLYSHEET,LM.KEY_GENERATE_TALLYSHEET_DATA_ALREADY_EXISTS,tally_sheet_data,ctms_job_id,is_required_to_send_data_to_ccls))
            if is_required_to_send_data_to_ccls:
                user_id = tally_sheet_data.get('user_id')
                from app.services.warehouse.wh_upload_tallysheet import WarehouseUploadTallySheetView
                WarehouseUploadTallySheetView().upload_tallysheet_while_generation(ctms_job_id,request_parameter,job_type,user_id)
            
        else:
            raise DataNotFoundException("GTService: ccls data doesn't exists in database")
        
    def check_tallysheet_exist_or_not(self,tally_sheet_data,job_order_id,job_type):
        qs = db.session.query(CTMSCargoJob).filter(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.id==job_order_id))
        if job_type in [JobOrderType.CARTING_FCL.value,JobOrderType.CARTING_LCL.value,JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
            query_object = qs.filter(CTMSCargoJob.truck_number==tally_sheet_data.get('truck_number'))
        elif job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value,JobOrderType.DE_STUFFING_FCL.value,JobOrderType.DE_STUFFING_LCL.value]:
            query_object = qs.filter(CTMSCargoJob.container_number==tally_sheet_data.get('container_number'))
        query_object = query_object.order_by(CTMSCargoJob.updated_at.desc())
        if query_object.first():
            return True,query_object
        return False,None
        
        
    def get_destuffing_date_for_delivery(self,container_number):
        start_time=None
        query_object = db.session.query(CTMSCargoJob).filter(CTMSCargoJob.container_number==container_number).filter((CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.job_type==JobOrderType.DE_STUFFING_FCL.value)) | (CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.job_type==JobOrderType.DE_STUFFING_LCL.value)))
        query_object = query_object.order_by(CTMSCargoJob.created_at.desc()).first()
        if query_object:
            start_time = query_object.job_start_time
        return start_time

    def update_tally_sheet_info(self,tally_sheet_data):
        job_type = tally_sheet_data['job_type']
        if job_type in [JobOrderType.CARTING_FCL.value,JobOrderType.CARTING_LCL.value,JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
            tally_sheet_data['truck_number'] = tally_sheet_data['cargo_details'][0]['truck_number'] if tally_sheet_data['cargo_details'] else None
        query_object = db.session.query(CTMSCargoJob).filter(CTMSCargoJob.id==tally_sheet_data.get('id')).first()
        if query_object:
            tally_sheet_data['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
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
        bills = json.loads(request.args.get('bills'))
        date_key_name = self.get_date_key_name(job_type)
        filter_date = request.args.get(date_key_name)
        if job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value]:
            query_object = self.get_ctms_job_obj(job_type,crn_number,None,None,bills,filter_date)
        else:
            query_object = self.get_ctms_job_obj(job_type,job_order,None,None,bills,filter_date)
        tallysheet_data = {}
        cargo_details = []
        if job_type in [JobOrderType.CARTING_FCL.value,JobOrderType.CARTING_LCL.value,JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value,JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value]:
            result = WarehouseDB().print_tallysheet_details(query_object.all(),job_order,job_type)
            for each_item in result:
                if job_type in [JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
                    if each_item['gpm_number'] == job_order:
                        tallysheet_data = each_item
                        cargo_details+=each_item.pop('cargo_details')
                elif job_type in [JobOrderType.CARTING_FCL.value]:
                    if each_item['crn_number'] == job_order:
                        tallysheet_data = each_item
                        cargo_details+=each_item.pop('cargo_details')
                elif job_type in [JobOrderType.CARTING_LCL.value]:
                    if each_item['cargo_carting_number'] == job_order:
                        tallysheet_data = each_item
                        cargo_details+=each_item.pop('cargo_details')
                else:
                    if each_item['crn_number'] == crn_number:
                        tallysheet_data = each_item
                        cargo_details+=each_item.pop('cargo_details')
            tallysheet_data['cargo_details'] = cargo_details
            self.merge_bills_data(tallysheet_data,job_type)
        else:
            query_object = self.filter_with_bill_details(query_object,bills,job_type)
            result = WarehouseDB().print_tallysheet_details(query_object.first(),job_order,job_type)
            tallysheet_data = result
            cargo_details=result.pop('cargo_details')
            tallysheet_data['cargo_details'] = cargo_details
        self.update_start_and_end_time(tallysheet_data)
        
        return tallysheet_data
    
    def update_start_and_end_time(self,tallysheet_data):
        min_start_time = min(tallysheet_data['cargo_details'], key=lambda x:x['start_time'])['start_time'] if tallysheet_data['cargo_details'] else None
        max_end_time = max(tallysheet_data['cargo_details'], key=lambda x:x['end_time'])['end_time'] if tallysheet_data['cargo_details'] else None
        tallysheet_data['start_time'] = min_start_time
        tallysheet_data['end_time'] = max_end_time

    def merge_bills_data(self,tallysheet_data,job_type):
        self.get_bills_and_total_declared_count(tallysheet_data,job_type)
        cargo_details = tallysheet_data['cargo_details']
        df = pd.DataFrame(cargo_details)
        aggregation_functions = self.build_aggregate_function(cargo_details)
        group_by_key = 'truck_number'
        if job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value]:
            group_by_key = 'container_number'
        df = df.groupby(df[group_by_key]).aggregate(aggregation_functions)
        result = json.loads(df.to_json(orient="records"))
        tallysheet_data['cargo_details'] = result

    def get_bills_and_total_declared_count(self,tallysheet_data,job_type):
        bills = []
        if job_type in [JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
            cargo_details = tallysheet_data['cargo_details']
            for each_cargo in cargo_details:
                bill_no = each_cargo['bill_of_entry']
                bills.append(bill_no)
        else:
            if job_type == JobOrderType.CARTING_FCL.value:
                crn_number = tallysheet_data['crn_number']
                query_object = db.session.query(CCLSCargoBillDetails).filter(CCLSCargoBillDetails.master_job_order_bill_details.has(MasterCargoDetails.carting_details.has(CartingCargoDetails.crn_number==crn_number))).all()
            elif job_type == JobOrderType.CARTING_LCL.value:
                con_number = tallysheet_data['cargo_carting_number']
                query_object = db.session.query(CCLSCargoBillDetails).filter(CCLSCargoBillDetails.master_job_order_bill_details.has(MasterCargoDetails.carting_details.has(CartingCargoDetails.carting_order_number==con_number))).all()
            else:
                crn_number = tallysheet_data['crn_number']
                query_object = db.session.query(CCLSCargoBillDetails).filter(CCLSCargoBillDetails.master_job_order_bill_details.has(MasterCargoDetails.stuffing_details.has(StuffingCargoDetails.crn_number==crn_number))).all()
            result = CCLSCargoDetailsSchema().dump(query_object,many=True)
            total_package_count = 0
            for each_bill in result:
                package_count = each_bill['commodity_details'][0]['package_count'] if each_bill['commodity_details'] else 0
                total_package_count+=package_count
                shipping_bill = each_bill['shipping_bill']
                bills.append(shipping_bill)
            tallysheet_data['total_package_count'] = total_package_count
        bills = list(set(bills)) 
        tallysheet_data['bills'] = bills
        
    def build_aggregate_function(self,cargo_details):
        cargo_details = cargo_details[0]
        agg_func = {}
        for key in cargo_details.keys():
            if key == 'package_count':
                agg_func.update({key:'sum'})
            elif key == 'packages_weight':
                agg_func.update({key:'sum'})
            elif key == 'area_of_cargo':
                agg_func.update({key:'sum'})
            elif key == 'grid_locations':
                agg_func.update({key:lambda x: [e for l in x for e in l]})
            else:
                agg_func.update({key:'first'})
        return agg_func