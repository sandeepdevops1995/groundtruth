import app.services.warehouse.constants as constants
from app.enums import JobOrderType,JobStatus
from app.Models.warehouse.job_order import CCLSJobOrder
from app import postgres_db as db
from app.logger import logger

class WarehouseUploadTallySheetView(object):

    def upload_tallysheet(self,request_data):
        job_type = request_data.get('job_type')
        request_parameter = request_data.get('request_parameter')
        if job_type==JobOrderType.CARTING_FCL.value:
           query_object = db.session.query(CCLSJobOrder).filter(CCLSJobOrder.crn_number==request_parameter,CCLSJobOrder.job_type==job_type)
        elif job_type==JobOrderType.CARTING_LCL.value:
           query_object = db.session.query(CCLSJobOrder).filter(CCLSJobOrder.carting_order_number==request_parameter,CCLSJobOrder.job_type==job_type)
        elif job_type==JobOrderType.STUFFING_FCL.value or job_type==JobOrderType.STUFFING_LCL.value or job_type==JobOrderType.DIRECT_STUFFING.value:
           query_object = db.session.query(CCLSJobOrder).filter(CCLSJobOrder.container_id==request_parameter,CCLSJobOrder.job_type==job_type)
        elif job_type==JobOrderType.DE_STUFFING_FCL.value or job_type==JobOrderType.DE_STUFFING_LCL.value:
           query_object = db.session.query(CCLSJobOrder).filter(CCLSJobOrder.container_id==request_parameter,CCLSJobOrder.job_type==job_type)
        elif job_type==JobOrderType.DELIVERY_FCL.value or job_type==JobOrderType.DELIVERY_LCL.value or job_type==JobOrderType.DIRECT_DELIVERY.value:
           query_object = db.session.query(CCLSJobOrder).filter(CCLSJobOrder.gpm_number==request_parameter,CCLSJobOrder.job_type==job_type)
        if query_object.first():
           query_object.update(dict({"status":JobStatus.COMPLETED.value}))
           db.session.commit()
           logger.info("update status %s in ccls job order",'completed')
