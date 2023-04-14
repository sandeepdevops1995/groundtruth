import app.services.warehouse.constants as constants
from app.enums import JobOrderType,JobStatus
from app.models.warehouse.job_order import CCLSJobOrder
from app import postgres_db as db
from app.logger import logger
from app.services.warehouse.database_service import WarehouseDB
from sqlalchemy.orm import contains_eager
from app.models.warehouse.bill_details import CCLSCargoDetails
from app.services.warehouse.ccls_post.carting import BuildCartingObject
from app.services.warehouse.ccls_post.stuffing import BuildStuffingObject
from app.services.warehouse.ccls_post.destuffing import BuildDeStuffingObject
from app.services.warehouse.ccls_post.delivery import BuildDeliveryObject
from app.services.warehouse.soap_api_call import post_job_info
from datetime import datetime
import pytz
class WarehouseUploadTallySheetView(object):

   def upload_tallysheet(self,request_data):
        job_type = request_data.get('job_type')
        request_parameter = request_data.get('request_parameter')
        user_id = request_data.get('user_id')
        trans_date_time = datetime.fromtimestamp(int(request_data.get('trans_date_time'))/1000, tz=pytz.utc)
        filter_data = {"job_type":job_type}
        if job_type==JobOrderType.CARTING_FCL.value:
           filter_data.update({"crn_number":request_parameter})
           self.send_carting_data_to_ccls(filter_data,user_id,trans_date_time)
        elif job_type==JobOrderType.CARTING_LCL.value:
           filter_data.update({"carting_order_number":request_parameter})
           self.send_carting_data_to_ccls(filter_data,user_id,trans_date_time)
        elif job_type in  [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value]:
           filter_data.update({"container_id":request_parameter})
           self.send_stuffing_data_to_ccls(filter_data,user_id,trans_date_time)
        elif job_type in  [JobOrderType.DE_STUFFING_FCL.value,JobOrderType.DE_STUFFING_LCL.value]:
           filter_data.update({"container_id":request_parameter})
           self.send_destuffing_data_to_ccls(filter_data,user_id,trans_date_time)
        elif job_type in [JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
           filter_data.update({"gpm_number":request_parameter})
           self.send_delivery_data_to_ccls(filter_data,user_id,trans_date_time)
        self.update_status_in_job(filter_data,JobStatus.COMPLETED.value)

   def get_data_from_db(self,filter_data):
      query_object = db.session.query(CCLSJobOrder).filter_by(**filter_data).join(CCLSJobOrder.cargo_details).options(contains_eager(CCLSJobOrder.cargo_details)).filter(CCLSCargoDetails.ctms_cargo_id!=None).all()
      result = WarehouseDB().get_final_job_details(query_object)
      result = self.process_data(result)
      print("result------------",result)
      return result

   def send_carting_data_to_ccls(self,filter_data,user_id,trans_date_time):
      result = self.get_data_from_db(filter_data)
      for each_job in result:
         job_details = BuildCartingObject(each_job,user_id,trans_date_time).__dict__
         print("job_details------------",job_details)
         post_job_info(job_details,"CWHImportUnLoading","unloadbpel_client_ep","UnLoadBpel_pt")

   def send_stuffing_data_to_ccls(self,filter_data,user_id,trans_date_time):
      result = self.get_data_from_db(filter_data)
      for each_job in result:
         job_details = BuildStuffingObject(each_job,user_id,trans_date_time).__dict__
         print("job_details------------",job_details)
         post_job_info(job_details,"CWHExportStuffing","cwhexportstuffbpel_client_ep","CWHExportStuffBpel_pt")

   def send_destuffing_data_to_ccls(self,filter_data,user_id,trans_date_time):
      result = self.get_data_from_db(filter_data)
      for each_job in result:
         job_details = BuildDeStuffingObject(each_job,user_id,trans_date_time).__dict__
         print("job_details------------",job_details)
         post_job_info(job_details,"CWHImportCargoDestuffing","cwhimptcrgdestuffingbpel_client_ep","CWHImptCrgDestuffingBPEL_pt")

   def send_delivery_data_to_ccls(self,filter_data,user_id,trans_date_time):
      result = self.get_data_from_db(filter_data)
      for each_job in result:
         job_details = BuildDeliveryObject(each_job,user_id,trans_date_time).__dict__
         print("job_details------------",job_details)
         # post_job_info(job_details,"CWHImportCargoDestuffing","cwhimptcrgdestuffingbpel_client_ep","CWHImptCrgDestuffingBPEL_pt")

   def update_status_in_job(self,filter_data,status):
      db.session.query(CCLSJobOrder).filter_by(**filter_data).update(dict({"status":JobStatus.COMPLETED.value}))
      db.session.commit()
      logger.info("update status %s in ccls job order",'completed')

   def process_data(self,data):
      result = []
      cargo_details = data.pop('cargo_details')
      for each_item in cargo_details:
         each_item.update(data)
         result.append(each_item)
      return result
