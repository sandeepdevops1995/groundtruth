from app.services.warehouse.database_service import WarehouseDB
import app.services.warehouse.constants as constants
from app.enums import JobOrderType
from app import postgres_db as db
from app.models.warehouse.ctms_cargo_job import CTMSCargoJob,CTMSBillDetails
from app.models.warehouse.ccls_cargo_details import MasterCargoDetails
from app.serializers.generate_tallysheet import CTMSCargoJobInsertSchema
from app.serializers.update_tallysheet import CTMSCargoJobUpdateSchema
from app.user_defined_exception import DataNotFoundException

class WarehouseTallySheetView(object):

    def get_tally_sheet_info(self,request):
        job_type = int(request.args.get('job_type',0))
        job_order = request.args.get('request_parameter')
        truck_number = request.args.get('truck_number')
        result = self.get_ctms_job_details(job_type,job_order,truck_number)
        return result
    
    def get_ctms_job_details(self,job_type,job_order,truck_number):
        query_object = db.session.query(CTMSCargoJob).join(CTMSBillDetails).join(MasterCargoDetails)
        if job_type==JobOrderType.CARTING_FCL.value:
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.property.mapper.class_.carting_details.property.mapper.class_.crn_number==job_order,CTMSCargoJob.ctms_job_order.property.mapper.class_.job_type==job_type,CTMSCargoJob.truck_number==truck_number)
        elif job_type==JobOrderType.CARTING_LCL.value:
            print("carting lcl------------")
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.property.mapper.class_.carting_details.property.mapper.class_.carting_order_number==job_order,CTMSCargoJob.ctms_job_order.property.mapper.class_.job_type==job_type,CTMSCargoJob.truck_number==truck_number)
        elif job_type==JobOrderType.STUFFING_FCL.value or job_type==JobOrderType.STUFFING_LCL.value or job_type==JobOrderType.DIRECT_STUFFING.value:
            print("stuffing------------")
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.property.mapper.class_.stuffing_details.property.mapper.class_.container_number==job_order,CTMSCargoJob.ctms_job_order.property.mapper.class_.job_type==job_type)
        elif job_type==JobOrderType.DE_STUFFING_FCL.value or job_type==JobOrderType.DE_STUFFING_LCL.value:
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.property.mapper.class_.destuffing_details.property.mapper.class_.container_number==job_order,CTMSCargoJob.ctms_job_order.property.mapper.class_.job_type==job_type)
        elif job_type==JobOrderType.DELIVERY_FCL.value or job_type==JobOrderType.DELIVERY_LCL.value or job_type==JobOrderType.DIRECT_DELIVERY.value:
            query_object = query_object.filter(CTMSCargoJob.ctms_job_order.property.mapper.class_.delivery_details.property.mapper.class_.gpm_number==job_order,CTMSCargoJob.ctms_job_order.property.mapper.class_.job_type==job_type,CTMSCargoJob.truck_number==truck_number)
        query_object = query_object.order_by(CTMSCargoJob.updated_at.desc()).first()
        result = WarehouseDB().get_tallysheet_details(query_object,job_order)
        return result
    
    def generate_tally_sheet_info(self,tally_sheet_data):
        job_type = tally_sheet_data['job_type']
        
        query_object = db.session.query(MasterCargoDetails).filter(MasterCargoDetails.job_type==job_type)
        if job_type==JobOrderType.CARTING_FCL.value:
            query_object = query_object.filter(MasterCargoDetails.carting_details.property.mapper.class_.crn_number==tally_sheet_data.get('crn_number'))
        elif job_type==JobOrderType.CARTING_LCL.value:
            query_object = query_object.filter(MasterCargoDetails.carting_details.property.mapper.class_.carting_order_number==tally_sheet_data.get('cargo_carting_number'))
        elif job_type==JobOrderType.STUFFING_FCL.value or job_type==JobOrderType.STUFFING_LCL.value or job_type==JobOrderType.DIRECT_STUFFING.value:
            query_object= query_object.filter(MasterCargoDetails.stuffing_details.property.mapper.class_.container_number==tally_sheet_data.get('container_number'))
        elif job_type==JobOrderType.DE_STUFFING_FCL.value or job_type==JobOrderType.DE_STUFFING_LCL.value:
            query_object = query_object.filter(MasterCargoDetails.destuffing_details.property.mapper.class_.container_number==tally_sheet_data.get('container_number'))
        elif job_type==JobOrderType.DELIVERY_FCL.value or job_type==JobOrderType.DELIVERY_LCL.value or job_type==JobOrderType.DIRECT_DELIVERY.value:
            query_object = query_object.filter(MasterCargoDetails.delivery_details.property.mapper.class_.gpm_number==tally_sheet_data.get('gpm_number'))
        query_object = query_object.order_by(MasterCargoDetails.updated_at.desc()).first()
        if query_object:
            job_order_id = query_object.id
            tally_sheet_data['truck_number'] = tally_sheet_data['cargo_details'][0].pop('truck_number')
            master_job_request = CTMSCargoJobInsertSchema(context={'job_order_id': job_order_id}).load(tally_sheet_data, session=db.session)
            db.session.add(master_job_request)
            db.session.commit()
        else:
            raise DataNotFoundException("GTService: ccls data doesn't exists in database")

    def update_tally_sheet_info(self,tally_sheet_data):
        query_object = db.session.query(CTMSCargoJob).filter(CTMSCargoJob.id==tally_sheet_data.get('id')).first()
        if query_object:
            master_job_request = CTMSCargoJobUpdateSchema().load(tally_sheet_data, instance=query_object, session=db.session)
            db.session.add(master_job_request)
            db.session.commit()
        else:
            raise DataNotFoundException("GTService: ccls data doesn't exists in database")
