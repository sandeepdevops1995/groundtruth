import app.services.warehouse.constants as constants
from app.enums import JobOrderType,JobStatus,CargoStatus
from app.models.warehouse.job_order import CCLSJobOrder
from app import postgres_db as db
from app.logger import logger
from app.services.warehouse.database_service import WarehouseDB
from sqlalchemy.orm import contains_eager
from app.services.warehouse.ccls_post.carting import BuildCartingObject
from app.services.warehouse.ccls_post.stuffing import BuildStuffingObject
from app.services.warehouse.ccls_post.destuffing import BuildDeStuffingObject
from app.services.warehouse.ccls_post.delivery import BuildDeliveryObject
from app.services.warehouse.soap_api_call import upload_tallysheet_data
from datetime import datetime
import pytz
from sqlalchemy import update

class WarehouseUploadTallySheetView(object):

   def upload_tallysheet(self,request_data):
        job_type = request_data.get('job_type')
        request_parameter = request_data.get('request_parameter')
        user_id = request_data.get('user_id')
        bills = request_data.get('bills')
        print("bills-------------------",bills)
        trans_date_time = datetime.fromtimestamp(int(request_data.get('trans_date_time'))/1000, tz=pytz.utc)
        filter_data = {"job_type":job_type}
        if job_type==JobOrderType.CARTING_FCL.value:
           filter_data.update({"crn_number":request_parameter})
           bill_number_key = "shipping_bill"
           self.send_carting_data_to_ccls(filter_data,user_id,trans_date_time)
        elif job_type==JobOrderType.CARTING_LCL.value:
           filter_data.update({"carting_order_number":request_parameter})
           bill_number_key = "shipping_bill"
           self.send_carting_data_to_ccls(filter_data,user_id,trans_date_time)
        elif job_type in  [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value]:
           filter_data.update({"container_id":request_parameter})
           bill_number_key = "shipping_bill"
           self.send_stuffing_data_to_ccls(filter_data,user_id,trans_date_time)
        elif job_type in  [JobOrderType.DE_STUFFING_FCL.value]:
           filter_data.update({"container_id":request_parameter})
           bill_number_key = "bill_of_entry"
           self.send_destuffing_data_to_ccls(filter_data,user_id,trans_date_time)
        elif job_type in  [JobOrderType.DE_STUFFING_LCL.value]:
           filter_data.update({"container_id":request_parameter})
           bill_number_key = "bill_of_lading"
           self.send_destuffing_data_to_ccls(filter_data,user_id,trans_date_time)
        elif job_type in [JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
           filter_data.update({"gpm_number":request_parameter})
           bill_number_key = "bill_of_entry"
           self.send_delivery_data_to_ccls(filter_data,user_id,trans_date_time)
        self.update_status_in_job(filter_data,JobStatus.COMPLETED.value,bill_number_key,bills)

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
         upload_tallysheet_data(job_details,"CWHImportUnLoading","unloadbpel_client_ep","UnLoadBpel_pt")

   def send_stuffing_data_to_ccls(self,filter_data,user_id,trans_date_time):
      result = self.get_data_from_db(filter_data)
      for each_job in result:
         job_details = BuildStuffingObject(each_job,user_id,trans_date_time).__dict__
         print("job_details------------",job_details)
         upload_tallysheet_data(job_details,"CWHExportStuffing","cwhexportstuffbpel_client_ep","CWHExportStuffBpel_pt")

   def send_destuffing_data_to_ccls(self,filter_data,user_id,trans_date_time):
      result = self.get_data_from_db(filter_data)
      for each_job in result:
         job_details = BuildDeStuffingObject(each_job,user_id,trans_date_time).__dict__
         print("job_details------------",job_details)
         upload_tallysheet_data(job_details,"CWHImportCargoDestuffing","cwhimptcrgdestuffingbpel_client_ep","CWHImptCrgDestuffingBPEL_pt")

   def send_delivery_data_to_ccls(self,filter_data,user_id,trans_date_time):
      result = self.get_data_from_db(filter_data)
      for each_job in result:
         job_details = BuildDeliveryObject(each_job,user_id,trans_date_time).__dict__
         print("job_details------------",job_details)
         # upload_tallysheet_data(job_details,"CWHImportCargoDestuffing","cwhimptcrgdestuffingbpel_client_ep","CWHImptCrgDestuffingBPEL_pt")

   def update_status_in_job(self,filter_data,status,bill_number_key,bills):
      # db_obj = db.session.query(CCLSJobOrder).filter_by(**filter_data).first()
      # if db_obj:
      #    job_order_id = db_obj.id
      # cargo_filter_data.update({"job_order_id":job_order_id})
      # db.session.query(CCLSCargoDetails,CCLSJobOrder).filter(CCLSCargoDetails.job_order_id==job_order_id).filter( getattr(CCLSCargoDetails,bill_number_key).in_(bills) ).filter_by().update(dict({"status":CargoStatus.TALLYSHEET_UPLOADED.value}))
      # db.session.commit()
      # query_object = db.session.query(CCLSJobOrder,CCLSCargoDetails).filter_by(**filter_data).filter(CCLSJobOrder.id==CCLSCargoDetails.job_order_id,CCLSCargoDetails.status==CargoStatus.TALLYSHEET_UPLOADED.value).update(**{"status":status})
      query = update(CCLSJobOrder).values(status=status).filter_by(**filter_data).filter(CCLSJobOrder.id==CCLSCargoDetails.job_order_id,CCLSCargoDetails.status==CargoStatus.TALLYSHEET_UPLOADED.value)
      for each_bill in bills:
         print("each_bill----------",each_bill)
         query = query.filter( CCLSCargoDetails.shipping_bill==int(each_bill))
      print("query-------------------",query)
      db.session.execute(query)
      db.session.commit()
      # if query_object:
      #    db.session.query(CCLSJobOrder).filter_by(**{"id":job_order_id}).update(dict({"status":status}))
      #    db.session.commit()
      logger.info("update status %s in ccls job order",'completed')

   def process_data(self,data):
      result = []
      cargo_details = data.pop('cargo_details')
      for each_item in cargo_details:
         each_item.update(data)
         result.append(each_item)
      return result
