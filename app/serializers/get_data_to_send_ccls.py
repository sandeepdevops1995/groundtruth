from marshmallow import fields, post_dump, pre_dump
from app import ma
from app.models.warehouse.ctms_cargo_job import CTMSCargoJob,CTMSBillDetails
import config
from app.enums import JobOrderType, SerialNumberType
from app.models.warehouse.truck import TruckDetails
from app import postgres_db as db


class CTMSbillDetailsSchema(ma.SQLAlchemyAutoSchema):

    shipping_bill = fields.Method("get_shipping_bill")
    bill_of_entry = fields.Method("get_bill_of_entry")
    bill_of_lading = fields.Method("get_bill_of_lading")
    package_code = fields.Method("get_package_code")
    package_weight = fields.Float(data_key='packages_weight')
    area = fields.Number(data_key='area_of_cargo')
    commodity_code = fields.Method("get_commodity_code")
    commodity_description = fields.Method("get_commodity_description")
    no_of_packages_damaged = fields.Number(data_key='damaged_count')
    area_damaged = fields.Number(data_key='area_of_damaged_cargo')
    bill_date = fields.Method("get_bill_date")
    bol_date = fields.Method("get_bol_date")
    warehouse_id = fields.String(data_key='wh_id')
    no_of_packages_declared = fields.Method("get_no_of_packages_declared")
    hsn_code = fields.Method("get_hsn_code")
    ctms_start_time = fields.Method("get_ctms_start_time")
    ctms_end_time = fields.Method("get_ctms_end_time")

    def get_shipping_bill(self, obj):
        return obj.ccls_bill.shipping_bill_number
    
    def get_bill_of_entry(self, obj):
        return obj.ccls_bill.bill_of_entry
    
    def get_bill_of_lading(self, obj):
        return obj.ccls_bill.bill_of_lading
    
    def get_package_code(self, obj):
        return obj.ccls_bill.package_code
    
    def get_commodity_code(self, obj):
        return obj.ccls_bill.commodity.comm_cd if obj.ccls_bill.commodity else None
    
    def get_commodity_description(self, obj):
        return obj.ccls_bill.commodity.comm_desc if obj.ccls_bill and obj.ccls_bill.commodity else None
    
    def get_bill_date(self, obj):
        return obj.ccls_bill.bill_date
    
    def get_bol_date(self, obj):
        return obj.ccls_bill.bol_date
    
    def get_no_of_packages_declared(self,obj):
        return obj.ccls_bill.no_of_packages_declared
    
    def get_hsn_code(self, obj):
        return obj.ccls_bill.hsn_code
    
    def get_ctms_start_time(self, obj):
        return obj.start_time
    
    def get_ctms_end_time(self, obj):
        return obj.end_time


    class Meta:
        model = CTMSBillDetails
        fields = ("id",'ctms_cargo_job_id',"shipping_bill", "bill_of_entry","bill_of_lading","package_code","package_count","package_weight","damaged_packages_weight","area","area_damaged","truck_number","ctms_start_time","ctms_end_time","commodity_code","commodity_description","no_of_packages_damaged","bill_date","warehouse_id","ccls_grid_locations","bol_date","no_of_packages_declared","full_or_part_flag",'hsn_code','from_packet','to_packet')


class GetTallySheetOrderSchema(ma.SQLAlchemyAutoSchema):
    
    cargo_carting_number = fields.Method("get_cargo_carting_number")
    crn_number = fields.Method("get_crn_number")
    gpm_number = fields.Method("get_gpm_number")
    container_flag = fields.Method("get_fcl_or_lcl")
    container_number = fields.Method("get_container_number")
    sline_code = fields.Method("get_shipping_liner_code")
    container_life = fields.Method("get_container_life")
    container_type = fields.Method("get_container_type")
    container_size =  fields.Method("get_container_size")
    container_iso_code = fields.Method("get_container_iso_code")
    private_or_concor_labour_flag = fields.Method("get_private_or_concor_labour_flag")
    icd_location_code = fields.Method("get_icd_location_code")
    handling_code = fields.Method("get_handling_code")
    destuffing_plan_date = fields.Method("get_destuffing_plan_date")
    cncl_flag = fields.Method("get_cncl_flag")
    is_cargo_card_generated = fields.Method("get_is_cargo_card_generated")
    cargo_details = fields.Nested(CTMSbillDetailsSchema, many=True)

    def get_cargo_carting_number(self, obj):
        return obj.ctms_job_order.carting_details.carting_order_number if obj.ctms_job_order.carting_details else None
    
    def get_crn_number(self, obj):
        return obj.ctms_job_order.carting_details.crn_number if obj.ctms_job_order.carting_details else obj.ctms_job_order.stuffing_details.crn_number if obj.ctms_job_order.stuffing_details else None
    
    def get_gpm_number(self, obj):
        return obj.ctms_job_order.delivery_details.gpm_number if obj.ctms_job_order.delivery_details else None
    
    def get_fcl_or_lcl(self, obj):
        return obj.ctms_job_order.fcl_or_lcl
    
    def get_container_number(self,obj):
        if obj.ctms_job_order.carting_details:
            container_number = []
            container_details = obj.ctms_job_order.carting_details.container_details
            if container_details:
                if isinstance(container_details,list):
                    for each_container in container_details:
                        container_number.append(each_container['container_number'])
                else:
                    container_number.append(container_details['container_number'])
            return container_number
        return obj.ctms_job_order.container_info.container_number  if obj.ctms_job_order.container_info else None
    
    def get_shipping_liner_code(self,obj):
        return obj.ctms_job_order.shipping_liner_code
    
    def get_container_life(self,obj):
        if obj.ctms_job_order.carting_details:
            container_life = []
            container_details = obj.ctms_job_order.carting_details.container_details
            if container_details:
                if isinstance(container_details,list):
                    for each_container in container_details:
                        container_life.append(each_container['container_life'])
                else:
                    container_life.append(container_details['container_life'])
            container_life = container_life[0] if container_life else None
            return container_life
        return obj.ctms_job_order.container_info.container_life  if obj.ctms_job_order.container_info else None
    
    def get_container_type(self,obj):
        # return obj.job_order.container_type if obj.container else None
        if obj.ctms_job_order.carting_details:
            container_type = []
            container_details = obj.ctms_job_order.carting_details.container_details
            if container_details:
                if isinstance(container_details,list):
                    for each_container in container_details:
                        container_type.append(each_container['container_type'])
                else:
                    container_type.append(container_details['container_type'])
            container_type = container_type[0] if container_type else None
            return container_type
        return obj.ctms_job_order.container_info.container_type  if obj.ctms_job_order.container_info else None
    
    def get_container_size(self,obj):
        if obj.ctms_job_order.carting_details:
            container_size = []
            container_details = obj.ctms_job_order.carting_details.container_details
            if container_details:
                if isinstance(container_details,list):
                    for each_container in container_details:
                        container_size.append(each_container['container_size'])
                else:
                    container_size.append(container_details['container_size'])
            return container_size
        return obj.ctms_job_order.container_info.container_size  if obj.ctms_job_order.container_info else None
    
    def get_container_iso_code(self,obj):
        return obj.ctms_job_order.container_info.container_iso_code  if obj.ctms_job_order.container_info else None
    
    def get_private_or_concor_labour_flag(self,obj):
        return obj.ctms_job_order.private_or_concor_labour_flag
    
    def get_icd_location_code(self,obj):
        return obj.ctms_job_order.icd_location_code
    
    def get_handling_code(self,obj):
        return obj.ctms_job_order.destuffing_details.handling_code if obj.ctms_job_order.destuffing_details else None

    def get_destuffing_plan_date(self,obj):
        return obj.ctms_job_order.destuffing_details.destuffing_plan_date if obj.ctms_job_order.destuffing_details else None
    
    def get_cncl_flag(self,obj):
        return obj.ctms_job_order.cncl_flag
    
    def get_is_cargo_card_generated(self,obj):
        return obj.ctms_job_order.carting_details.is_cargo_card_generated if obj.ctms_job_order.carting_details else None

    class Meta:
        model = CTMSCargoJob
        fields = ("id","cargo_carting_number","crn_number","gpm_number","total_package_count","container_flag","equipment_id",'container_number','sline_code','container_life','container_type','container_size','private_or_concor_labour_flag','icd_location_code','handling_code','cargo_details',"created_at","updated_at","created_by","updated_by",'destuffing_plan_date','cncl_flag','is_cargo_card_generated')
        include_relationships = True