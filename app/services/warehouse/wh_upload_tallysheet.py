import app.services.warehouse.constants as constants
from app.enums import JobOrderType,JobStatus
from app import postgres_db as db
from app.logger import logger
from app.services.warehouse.ccls_post.carting import BuildCartingObject
from app.services.warehouse.ccls_post.stuffing import BuildStuffingObject
from app.services.warehouse.ccls_post.destuffing import BuildDeStuffingObject
from app.services.warehouse.ccls_post.delivery import BuildDeliveryObject
from app.services.warehouse.soap_api_call import upload_tallysheet_data
from datetime import datetime
import pytz
from app.services.warehouse.wh_tallysheet import WarehouseTallySheetView
from app.services.warehouse.database_service import WarehouseDB
from app.models.warehouse.ctms_cargo_job import CTMSCargoJob
import app.logging_message as LM
from app.controllers.utils import convert_timestamp_to_ccls_date

class WarehouseUploadTallySheetView(object):

   def upload_tallysheet(self,request_data):
        job_type = request_data.get('job_type')
        request_parameter = request_data.get('request_parameter')
        truck_number = request_data.get('truck_number')
        query_object = WarehouseTallySheetView().get_ctms_job_obj(job_type,request_parameter,truck_number)
        data = WarehouseDB().get_tallysheet_details(query_object.first(),request_parameter,job_type)
        result = self.process_data(data)
        user_id = request_data.get('user_id')
        trans_date_time = convert_timestamp_to_ccls_date(request_data.get('trans_date_time'))
        if job_type==JobOrderType.CARTING_FCL.value:
           self.send_carting_data_to_ccls(result,user_id,trans_date_time,request_parameter)
        elif job_type==JobOrderType.CARTING_LCL.value:
           self.send_carting_data_to_ccls(result,user_id,trans_date_time,request_parameter)
        elif job_type in  [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value]:
           self.send_stuffing_data_to_ccls(result,user_id,trans_date_time,request_parameter)
        elif job_type in  [JobOrderType.DE_STUFFING_FCL.value,JobOrderType.DE_STUFFING_LCL.value]:
           self.send_destuffing_data_to_ccls(result,user_id,trans_date_time,request_parameter)
        elif job_type in [JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
           self.send_delivery_data_to_ccls(result,user_id,trans_date_time,request_parameter)
        self.update_tallysheet_status(data.get('id'),request_parameter,job_type)

   def send_carting_data_to_ccls(self,result,user_id,trans_date_time,request_parameter):
      for each_job in result:
         job_details = BuildCartingObject(each_job,user_id,trans_date_time).__dict__
         upload_tallysheet_data(job_details,"CWHImportUnLoading","unloadbpel_client_ep","UnLoadBpel_pt",request_parameter)

   def send_stuffing_data_to_ccls(self,result,user_id,trans_date_time,request_parameter):
      for each_job in result:
         job_details = BuildStuffingObject(each_job,user_id,trans_date_time).__dict__
         upload_tallysheet_data(job_details,"CWHExportStuffing","cwhexportstuffbpel_client_ep","CWHExportStuffBpel_pt",request_parameter)

   def send_destuffing_data_to_ccls(self,result,user_id,trans_date_time,request_parameter):
      for each_job in result:
         job_details = BuildDeStuffingObject(each_job,user_id,trans_date_time).__dict__
         upload_tallysheet_data(job_details,"CWHImportCargoDestuffing","cwhimptcrgdestuffingbpel_client_ep","CWHImptCrgDestuffingBPEL_pt",request_parameter)

   def send_delivery_data_to_ccls(self,result,user_id,trans_date_time,request_parameter):
      for each_job in result:
         job_details = BuildDeliveryObject(each_job,user_id,trans_date_time).__dict__
         # upload_tallysheet_data(job_details,"CWHImportCargoDestuffing","cwhimptcrgdestuffingbpel_client_ep","CWHImptCrgDestuffingBPEL_pt",request_parameter)


   def process_data(self,data):
      result = []
      cargo_details = data.pop('cargo_details')
      for each_item in cargo_details:
         each_item.update(data)
         result.append(each_item)
      return result
   
   def update_tallysheet_status(self,ctms_job_order_id,request_parameter,job_type):
      db.session.query(CTMSCargoJob).filter(CTMSCargoJob.id==ctms_job_order_id).update({"status":JobStatus.TALLYSHEET_UPLOADED.value})
      db_response = db.session.commit()
      logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_UPDATE_STATUS_AFTER_UPLOAD_TALLYSHEET,'JT_'+str(job_type),request_parameter,db_response))