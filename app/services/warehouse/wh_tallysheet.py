from app.services.warehouse.data_formater import DataFormater
from app.services.warehouse.database_service import WarehouseDB
import app.services.warehouse.constants as constants
from app.enums import JobOrderType
from app.Models.warehouse.job_order import CCLSJobOrder,CTMSJobOrder
from app import postgres_db as db

class WarehouseTallySheetView(object):

    def get_tally_sheet_info(self,request):
        job_type = int(request.args.get('job_type',0))
        print("job_type----------",job_type)
        if job_type==JobOrderType.CARTING_FCL.value:
            job_order = request.args.get('crn_number',0)
            filter_data = {"crn_number":job_order}
        elif job_type==JobOrderType.CARTING_LCL.value:
            job_order = request.args.get('cargo_carting_number',0)
            filter_data = {"cargo_carting_number":job_order}
        elif job_type==JobOrderType.STUFFING_FCL.value or job_type==JobOrderType.STUFFING_LCL.value or job_type==JobOrderType.DE_STUFFING_FCL.value or job_type==JobOrderType.DE_STUFFING_FCL.value:
            job_order = request.args.get('container_number',0)
            filter_data = {"container_id":job_order}
        elif job_type==JobOrderType.DELIVERY_FCL.value or job_type==JobOrderType.DELIVERY_LCL.value:
            job_order = request.args.get('gpm_number',0)
            filter_data = {"gpm_number":job_order}
        result = WarehouseDB().get_final_job_details(filter_data)
        return result
    
    def process_tally_sheet_info(self,tally_sheet_data):
        print("tally_sheet_data--------",tally_sheet_data)
        job_type = tally_sheet_data['job_type']
        if job_type==JobOrderType.CARTING_FCL.value:
            crn_number = tally_sheet_data.get('crn_number')
            query_object = db.session.query(CTMSJobOrder).join(CCLSJobOrder).filter(CCLSJobOrder.crn_number==crn_number)
            filter_data = {"crn_number":crn_number}
            cargo_filter_key = 'shipping_bill'
        elif job_type==JobOrderType.CARTING_LCL.value:
            carting_order_number = tally_sheet_data.get('cargo_carting_number')
            query_object = db.session.query(CTMSJobOrder).join(CCLSJobOrder).filter(CCLSJobOrder.carting_order_number==carting_order_number)
            filter_data = {"carting_order_number":carting_order_number}
            cargo_filter_key = 'shipping_bill'
        elif job_type==JobOrderType.STUFFING_FCL.value or job_type==JobOrderType.STUFFING_LCL.value:
            container_number = tally_sheet_data['cargo_details'][0].get('container_number')
            query_object = db.session.query(CTMSJobOrder).join(CCLSJobOrder).filter(CCLSJobOrder.container_id==container_number)
            filter_data = {"container_id":container_number}
            cargo_filter_key = 'shipping_bill'
        elif job_type==JobOrderType.DE_STUFFING_FCL.value or job_type==JobOrderType.DE_STUFFING_LCL.value:
            container_number = tally_sheet_data['cargo_details'][0].get('container_number')
            query_object = db.session.query(CTMSJobOrder).join(CCLSJobOrder).filter(CCLSJobOrder.container_id==container_number)
            filter_data = {"container_id":container_number}
            cargo_filter_key= "bill_of_entry" if job_type==JobOrderType.DE_STUFFING_FCL.value else "bill_of_lading"
        elif job_type==JobOrderType.DELIVERY_FCL.value or job_type==JobOrderType.DELIVERY_LCL.value:
            gpm_number = tally_sheet_data.get('gpm_number')
            query_object = db.session.query(CTMSJobOrder).join(CCLSJobOrder).filter(CCLSJobOrder.gpm_number==gpm_number)
            filter_data = {"gpm_number":gpm_number}
            cargo_filter_key= "bill_of_entry"
        bill_details = tally_sheet_data.pop('cargo_details')
        final_job_order_details = DataFormater().ctms_job_order_table_formater(tally_sheet_data)
        job_order_id = WarehouseDB().save_ctms_job_order(final_job_order_details,query_object,filter_data)
        WarehouseDB().save_ctms_bill_details(bill_details,job_order_id,cargo_filter_key)
