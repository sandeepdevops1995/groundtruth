import app.services.warehouse.constants as constants
from app.enums import JobOrderType
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

class WarehouseUploadTallySheetView(object):

   def upload_tallysheet(self,request_data):
        job_type = request_data.get('job_type')
        request_parameter = request_data.get('request_parameter')
        truck_number = request_data.get('truck_number')
        result = WarehouseTallySheetView().get_ctms_job_details(job_type,request_parameter,truck_number)
        result = self.process_data(result)
        user_id = request_data.get('user_id')
        trans_date_time = datetime.fromtimestamp(int(request_data.get('trans_date_time'))/1000, tz=pytz.utc)
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
