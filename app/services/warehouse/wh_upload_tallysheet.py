import app.services.warehouse.constants as constants
from app.enums import JobOrderType,JobStatus
from app import postgres_db as db
from app.logger import logger
from app.services.warehouse.ccls_post.carting import BuildCartingObject
from app.services.warehouse.ccls_post.stuffing import BuildStuffingObject
from app.services.warehouse.ccls_post.destuffing import BuildDeStuffingObject
from app.services.warehouse.ccls_post.delivery import BuildDeliveryObject
from app.services.warehouse.soap_api_call import upload_tallysheet_data
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
        crn_number = request_data.get('crn_number')
        bills = request_data.get('bills')
        date_key_name = WarehouseTallySheetView().get_date_key_name(job_type)
        filter_date = request_data.get(date_key_name)
        is_upload_tallysheet_for_all = request_data.get('is_upload_tallysheet_for_all')
        if is_upload_tallysheet_for_all:
            if job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value]:
               query_object = WarehouseTallySheetView().get_ctms_job_obj(job_type,crn_number,truck_number,None,bills,filter_date)
            else:
               query_object = WarehouseTallySheetView().get_ctms_job_obj(job_type,request_parameter,None,None,bills,filter_date)
        else:
            if job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value]:
               query_object = WarehouseTallySheetView().get_ctms_job_obj(job_type,crn_number,truck_number,request_parameter,bills,filter_date)
            else:
               query_object = WarehouseTallySheetView().get_ctms_job_obj(job_type,request_parameter,truck_number,None,bills,filter_date)
        status = self.is_tallysheet_already_uploaded(query_object)
        data = WarehouseDB().upload_tallysheet_details(query_object.all(),request_parameter,job_type)
        result,ctms_job_order_id_list,trucks = self.process_data(data,job_type)
        if status==403:
           return trucks,status
        user_id = request_data.get('user_id')
        trans_date_time = convert_timestamp_to_ccls_date(request_data.get('trans_date_time'))
        if job_type==JobOrderType.CARTING_FCL.value:
           self.send_carting_data_to_ccls(result,user_id,trans_date_time,request_parameter,job_type)
        elif job_type==JobOrderType.CARTING_LCL.value:
           self.send_carting_data_to_ccls(result,user_id,trans_date_time,request_parameter,job_type)
        elif job_type in  [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value]:
           self.send_stuffing_data_to_ccls(result,user_id,trans_date_time,request_parameter,job_type)
        elif job_type in  [JobOrderType.DE_STUFFING_FCL.value,JobOrderType.DE_STUFFING_LCL.value]:
           self.send_destuffing_data_to_ccls(result,user_id,trans_date_time,request_parameter,job_type)
        elif job_type in [JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
           self.send_delivery_data_to_ccls(result,user_id,trans_date_time,request_parameter,job_type)
        self.update_tallysheet_status(ctms_job_order_id_list,request_parameter,job_type,trans_date_time)
        return trucks,status

   def is_tallysheet_already_uploaded(self,query_object):
      if query_object.filter(CTMSCargoJob.status==JobStatus.TALLYSHEET_UPLOADED.value):
         return 403
      return 200

   def send_carting_data_to_ccls(self,result,user_id,trans_date_time,request_parameter,job_type):
      for each_job in result:
         job_details = BuildCartingObject(each_job,user_id,trans_date_time).__dict__
         logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_REQUEST_DATA_FOR_UPLOAD_TALLYSHEET,'JT_'+str(job_type),request_parameter,job_details))
         upload_tallysheet_data(job_details,"CWHExportCrgUNLDGTSWrite","cwhexportcrgunldgtsbpel_client_ep","CWHExportCrgUNLDGTSBPEL_pt",request_parameter)

   def send_stuffing_data_to_ccls(self,result,user_id,trans_date_time,request_parameter,job_type):
      for each_job in result:
         job_details = BuildStuffingObject(each_job,user_id,trans_date_time).__dict__
         logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_REQUEST_DATA_FOR_UPLOAD_TALLYSHEET,'JT_'+str(job_type),request_parameter,job_details))
         upload_tallysheet_data(job_details,"CWHExprtCrgDSTFWrite","cwhexprtcrgdstfwritebpel_client_ep","CWHExprtCrgDSTFWriteBPEL_pt",request_parameter)

   def send_destuffing_data_to_ccls(self,result,user_id,trans_date_time,request_parameter,job_type):
      for each_job in result:
         job_details = BuildDeStuffingObject(each_job,user_id,trans_date_time).__dict__
         logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_REQUEST_DATA_FOR_UPLOAD_TALLYSHEET,'JT_'+str(job_type),request_parameter,job_details))
         upload_tallysheet_data(job_details,"CWHImportCrgDSTFWrite","cwhimportcrgdstfwritebpel_client_ep","CWHImportCrgDSTFWriteBPEL_pt",request_parameter)

   def send_delivery_data_to_ccls(self,result,user_id,trans_date_time,request_parameter,job_type):
      for each_job in result:
         job_details = BuildDeliveryObject(each_job,user_id,trans_date_time).__dict__
         logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_REQUEST_DATA_FOR_UPLOAD_TALLYSHEET,'JT_'+str(job_type),request_parameter,job_details))
         upload_tallysheet_data(job_details,"CWHImportCrgLDGTS","cwhimportcrgldgts_client_ep","CWHImportCrgLDGTS_pt",request_parameter)


   def process_data(self,data,job_type):
      result = []
      ctms_job_order_id_list = []
      trucks = []
      for each_bill in data:
         ctms_job_order_id_list.append(each_bill.get('id'))
         cargo_details = each_bill.pop('cargo_details')
         for each_item in cargo_details:
            if job_type in [JobOrderType.CARTING_FCL.value,JobOrderType.CARTING_LCL.value,JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
               trucks.append(each_item.get('truck_number'))
            each_item.update(each_bill)
            result.append(each_item)
      return result,ctms_job_order_id_list,trucks
   
   def update_tallysheet_status(self,ctms_job_order_id_list,request_parameter,job_type,trans_date_time):
      db.session.query(CTMSCargoJob).filter(CTMSCargoJob.id.in_(ctms_job_order_id_list)).update({"status":JobStatus.TALLYSHEET_UPLOADED.value,"trans_date_time":trans_date_time})
      db_response = db.session.commit()
      logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_UPDATE_STATUS_AFTER_UPLOAD_TALLYSHEET,'JT_'+str(job_type),request_parameter,db_response))