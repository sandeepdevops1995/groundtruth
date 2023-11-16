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
from app.models.warehouse.ctms_cargo_job import CTMSCargoJob, CTMSBillDetails
import app.logging_message as LM
from app.controllers.utils import convert_timestamp_to_ccls_date
import time
from app.models.warehouse.ccls_cargo_details import MasterCargoDetails, CartingCargoDetails, CCLSCargoBillDetails, StuffingCargoDetails, DeStuffingCargoDetails, DeliveryCargoDetails

class WarehouseUploadTallySheetView(object):

   def upload_tallysheet_while_generation(self,ctms_job_id,request_parameter,job_type,user_id):
        query_object = db.session.query(CTMSCargoJob).filter(CTMSCargoJob.id==ctms_job_id).first()
        data = WarehouseDB().get_tallysheet_details_for_ccls(query_object,request_parameter,job_type)
        result = self.format_uploaded_data(data,job_type)
        trans_date_time = int(time.time())*1000
        trans_date_time = convert_timestamp_to_ccls_date(trans_date_time)
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
        self.update_tallysheet_status_after_upload(ctms_job_id,request_parameter,job_type,trans_date_time)

   def upload_tallysheet(self,request_data):
        job_type = request_data.get('job_type')
        request_parameter = request_data.get('request_parameter')
        truck_number = request_data.get('truck_number')
        crn_number = request_data.get('crn_number')
        bills = request_data.get('bills')
        date_key_name = WarehouseTallySheetView().get_date_key_name(job_type)
        filter_date = request_data.get(date_key_name)
        if job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value]:
            query_object = WarehouseTallySheetView().get_ctms_job_obj(job_type,crn_number,None,None,bills,filter_date)
        else:
            query_object = WarehouseTallySheetView().get_ctms_job_obj(job_type,request_parameter,None,None,bills,filter_date)
        if job_type in [JobOrderType.DE_STUFFING_FCL.value,JobOrderType.DE_STUFFING_LCL.value]:
           query_object = WarehouseTallySheetView().filter_with_bill_details(query_object,bills,job_type)
        data = WarehouseDB().upload_tallysheet_details(query_object.all(),request_parameter,job_type)
        trucks_or_containers = self.process_data(data,job_type)
        return trucks_or_containers

   def send_carting_data_to_ccls(self,result,user_id,trans_date_time,request_parameter,job_type):
      for each_job in result:
         job_details = BuildCartingObject(each_job,user_id,trans_date_time).__dict__
         logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_REQUEST_DATA_FOR_UPLOAD_TALLYSHEET,'JT_'+str(job_type),request_parameter,job_details))
         upload_tallysheet_data(job_details,"CWHExportCrgUNLDGTSWrite","cwhexportcrgunldgtsbpel_client_ep","CWHExportCrgUNLDGTSBPEL_pt",request_parameter,job_type)

   def send_stuffing_data_to_ccls(self,result,user_id,trans_date_time,request_parameter,job_type):
      for each_job in result:
         job_details = BuildStuffingObject(each_job,user_id,trans_date_time).__dict__
         logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_REQUEST_DATA_FOR_UPLOAD_TALLYSHEET,'JT_'+str(job_type),request_parameter,job_details))
         upload_tallysheet_data(job_details,"CWHExprtCrgDSTFWrite","cwhexprtcrgdstfwritebpel_client_ep","CWHExprtCrgDSTFWriteBPEL_pt",request_parameter,job_type)

   def send_destuffing_data_to_ccls(self,result,user_id,trans_date_time,request_parameter,job_type):
      for each_job in result:
         job_details = BuildDeStuffingObject(each_job,user_id,trans_date_time).__dict__
         logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_REQUEST_DATA_FOR_UPLOAD_TALLYSHEET,'JT_'+str(job_type),request_parameter,job_details))
         upload_tallysheet_data(job_details,"CWHImportCrgDSTFWrite","cwhimportcrgdstfwritebpel_client_ep","CWHImportCrgDSTFWriteBPEL_pt",request_parameter,job_type)

   def send_delivery_data_to_ccls(self,result,user_id,trans_date_time,request_parameter,job_type):
      for each_job in result:
         job_details = BuildDeliveryObject(each_job,user_id,trans_date_time).__dict__
         logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_REQUEST_DATA_FOR_UPLOAD_TALLYSHEET,'JT_'+str(job_type),request_parameter,job_details))
         upload_tallysheet_data(job_details,"CWHImportCrgLDGTS","cwhimportcrgldgts_client_ep","CWHImportCrgLDGTS_pt",request_parameter,job_type)


   def format_uploaded_data(self,data,job_type):
      total_package_count = data.get('total_package_count',0)
      result = []
      cargo_details = data.pop('cargo_details')
      no_of_bills=0
      for each_item in cargo_details:
         no_of_bills+=1
      for each_item in cargo_details:
         each_item['total_package_count_of_bill'] = self.get_total_package_count_of_bill(data,each_item,job_type)
         self.get_short_or_excess(total_package_count,each_item)
         each_item.update(data)
         each_item['no_of_bills'] = no_of_bills
         result.append(each_item)
      return result
   
   def get_total_package_count_of_bill(self,data,each_item,job_type):
      if job_type in [JobOrderType.CARTING_FCL.value,JobOrderType.CARTING_LCL.value,JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value]:
         shipping_bill = each_item['shipping_bill']
         bill_query = db.session.query(CTMSBillDetails).filter(CTMSBillDetails.ccls_bill.has(CCLSCargoBillDetails.shipping_bill_number==shipping_bill))
         if job_type==JobOrderType.CARTING_FCL.value:
            crn_number = data['crn_number']
            bill_query = bill_query.filter(CTMSBillDetails.ctms_job_order_bill_details.has(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.carting_details.has(CartingCargoDetails.crn_number==crn_number))))
         elif job_type==JobOrderType.CARTING_LCL.value:
            con_number = data['cargo_carting_number']
            bill_query = bill_query.filter(CTMSBillDetails.ctms_job_order_bill_details.has(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.carting_details.has(CartingCargoDetails.carting_order_number==con_number))))
         else:
            crn_number = data['crn_number']
            bill_query = bill_query.filter(CTMSBillDetails.ctms_job_order_bill_details.has(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.stuffing_details.has(StuffingCargoDetails.crn_number==crn_number))))
      elif job_type in [JobOrderType.DE_STUFFING_FCL.value,JobOrderType.DE_STUFFING_LCL.value]:
         container_number = data['container_number']
         bill_query = db.session.query(CTMSBillDetails).filter(CTMSBillDetails.ctms_job_order_bill_details.has(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.destuffing_details.has(DeStuffingCargoDetails.container_number==container_number))))
         if job_type==JobOrderType.DE_STUFFING_FCL.value:
            bill_of_entry = each_item['bill_of_entry']
            bill_query = bill_query.filter(CTMSBillDetails.ccls_bill.has(CCLSCargoBillDetails.bill_of_entry==bill_of_entry))
         else:
            bill_of_lading = each_item['bill_of_lading']
            bill_query = bill_query.filter(CTMSBillDetails.ccls_bill.has(CCLSCargoBillDetails.bill_of_lading==bill_of_lading))
      elif job_type in [JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
         gpm_number = data['gpm_number']
         bill_of_entry = each_item['bill_of_entry']
         bill_query = db.session.query(CTMSBillDetails).filter(CTMSBillDetails.ccls_bill.has(CCLSCargoBillDetails.bill_of_entry==bill_of_entry)).filter(CTMSBillDetails.ctms_job_order_bill_details.has(CTMSCargoJob.ctms_job_order.has(MasterCargoDetails.delivery_details.has(DeliveryCargoDetails.gpm_number==gpm_number))))
      bill_query = bill_query.with_entities(db.func.sum(CTMSBillDetails.package_count).label("total_package_count_of_bill")).first()
      if bill_query:
            total_package_count_of_bill = bill_query.total_package_count_of_bill
      return total_package_count_of_bill
         

   
   def get_short_or_excess(self,total_package_count,each_item):
      package_count = each_item.get('total_package_count_of_bill')
      if total_package_count>package_count:
         each_item['short'] = total_package_count-package_count
      elif package_count>total_package_count:
         each_item['excess'] = package_count-total_package_count
   
   def update_tallysheet_status_after_upload(self,ctms_job_order_id,request_parameter,job_type,trans_date_time):
      db.session.query(CTMSCargoJob).filter(CTMSCargoJob.id==ctms_job_order_id).update({"status":JobStatus.TALLYSHEET_UPLOADED.value,"trans_date_time":trans_date_time})
      db_response = db.session.commit()
      logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_UPDATE_STATUS_AFTER_UPLOAD_TALLYSHEET,'JT_'+str(job_type),request_parameter,db_response))

   def process_data(self,data,job_type):
      trucks_or_containers = []
      for each_bill in data:
         cargo_details = each_bill.pop('cargo_details')
         for each_item in cargo_details:
            if job_type in [JobOrderType.CARTING_FCL.value,JobOrderType.CARTING_LCL.value,JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
               trucks_or_containers.append(each_item.get('truck_number'))
            else:
               trucks_or_containers.append(each_item.get('container_number'))
            each_item.update(each_bill)
      return trucks_or_containers
   
   def update_tallysheet_status(self,ctms_job_order_id_list,request_parameter,job_type,trans_date_time):
      db.session.query(CTMSCargoJob).filter(CTMSCargoJob.id.in_(ctms_job_order_id_list)).update({"status":JobStatus.TALLYSHEET_UPLOADED.value,"trans_date_time":trans_date_time})
      db_response = db.session.commit()
      logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_UPDATE_STATUS_AFTER_UPLOAD_TALLYSHEET,'JT_'+str(job_type),request_parameter,db_response))