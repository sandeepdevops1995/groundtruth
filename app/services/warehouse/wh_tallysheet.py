from app.services.warehouse.data_formater import DataFormater
from app.services.warehouse.database_service import WarehouseDB
import app.services.warehouse.constants as constants
from app.enums import JobOrderType
from app.models.warehouse.job_order import CCLSJobOrder,CTMSJobOrder
from app import postgres_db as db
from sqlalchemy.orm import contains_eager
from app.models.warehouse.bill_details import CCLSCargoDetails

class WarehouseTallySheetView(object):

    def get_tally_sheet_info(self,request):
        job_type = int(request.args.get('job_type',0))
        job_order = request.args.get('request_parameter')
        filter_data = {"job_type":job_type}
        if job_type==JobOrderType.CARTING_FCL.value:
            filter_data.update({"crn_number":job_order})
        elif job_type==JobOrderType.CARTING_LCL.value:
            filter_data.update({"carting_order_number":job_order})
        elif job_type==JobOrderType.STUFFING_FCL.value or job_type==JobOrderType.STUFFING_LCL.value or job_type==JobOrderType.DE_STUFFING_FCL.value or job_type==JobOrderType.DE_STUFFING_LCL.value or job_type==JobOrderType.DIRECT_STUFFING.value:
            filter_data.update({"container_id":job_order})
        elif job_type==JobOrderType.DELIVERY_FCL.value or job_type==JobOrderType.DELIVERY_LCL.value or job_type==JobOrderType.DIRECT_DELIVERY.value:
            filter_data.update({"gpm_number":job_order})
        query_object = db.session.query(CCLSJobOrder).filter_by(**filter_data).join(CCLSJobOrder.cargo_details).options(contains_eager(CCLSJobOrder.cargo_details)).filter(CCLSCargoDetails.ctms_cargo_id!=None).first()
        result = WarehouseDB().get_final_job_details(query_object)
        return result
    
    def process_tally_sheet_info(self,tally_sheet_data):
        job_type = tally_sheet_data['job_type']
        if job_type==JobOrderType.CARTING_FCL.value:
            crn_number = tally_sheet_data.get('crn_number')
            query_object = db.session.query(CTMSJobOrder).join(CCLSJobOrder).filter(CCLSJobOrder.crn_number==crn_number,CCLSJobOrder.job_type==job_type)
            filter_data = {"crn_number":crn_number}
            cargo_filter_key = 'shipping_bill'
        elif job_type==JobOrderType.CARTING_LCL.value:
            carting_order_number = tally_sheet_data.get('cargo_carting_number')
            query_object = db.session.query(CTMSJobOrder).join(CCLSJobOrder).filter(CCLSJobOrder.carting_order_number==carting_order_number,CCLSJobOrder.job_type==job_type)
            filter_data = {"carting_order_number":carting_order_number}
            cargo_filter_key = 'shipping_bill'
        elif job_type==JobOrderType.STUFFING_FCL.value or job_type==JobOrderType.STUFFING_LCL.value or job_type==JobOrderType.DIRECT_STUFFING.value:
            container_number = tally_sheet_data.get('container_number')
            query_object = db.session.query(CTMSJobOrder).join(CCLSJobOrder).filter(CCLSJobOrder.container_id==container_number,CCLSJobOrder.job_type==job_type)
            filter_data = {"container_id":container_number}
            cargo_filter_key = 'shipping_bill'
        elif job_type==JobOrderType.DE_STUFFING_FCL.value or job_type==JobOrderType.DE_STUFFING_LCL.value:
            container_number = tally_sheet_data.get('container_number')
            query_object = db.session.query(CTMSJobOrder).join(CCLSJobOrder).filter(CCLSJobOrder.container_id==container_number,CCLSJobOrder.job_type==job_type)
            filter_data = {"container_id":container_number}
            cargo_filter_key= "bill_of_entry" if job_type==JobOrderType.DE_STUFFING_FCL.value else "bill_of_lading"
        elif job_type==JobOrderType.DELIVERY_FCL.value or job_type==JobOrderType.DELIVERY_LCL.value or job_type==JobOrderType.DIRECT_DELIVERY.value:
            gpm_number = tally_sheet_data.get('gpm_number')
            query_object = db.session.query(CTMSJobOrder).join(CCLSJobOrder).filter(CCLSJobOrder.gpm_number==gpm_number,CCLSJobOrder.job_type==job_type)
            filter_data = {"gpm_number":gpm_number}
            cargo_filter_key= "bill_of_entry"
        filter_data.update({"job_type":job_type})
        bill_details = tally_sheet_data.pop('cargo_details')
        final_job_order_details = DataFormater().ctms_job_order_table_formater(tally_sheet_data)
        job_order_id = WarehouseDB().save_ctms_job_order(final_job_order_details,query_object,filter_data)
        WarehouseDB().save_ctms_bill_details(bill_details,job_order_id,cargo_filter_key,job_type)
