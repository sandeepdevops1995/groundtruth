from marshmallow import fields
import json
from app.models.warehouse.job_order import CCLSJobOrder
from app.models.warehouse.bill_details import CCLSCargoDetails
from app import ma
from app.models.master.warehouse import Commodity as WarehouseCommodity


class CCLSCargoDetailsSchema(ma.SQLAlchemyAutoSchema):
    # area = fields.Number(data_key='area_of_cargo')
    # area_damaged = fields.Number(data_key='area_of_damaged_cargo')
    # package_weight = fields.Number(data_key='packages_weight')
    truck_number = fields.Method("get_truck_number")
    # container_number = fields.Method("get_container_number")
    package_count = fields.Method("get_package_count")
    package_weight = fields.Method("get_package_weight",data_key='packages_weight')
    no_of_packages_damaged = fields.Method("get_damaged_count",data_key='damaged_count')
    damaged_packages_weight = fields.Method("get_damaged_packages_weight")
    area = fields.Method("get_area",data_key='area_of_cargo')
    area_damaged = fields.Method("get_area_damaged",data_key='area_of_damaged_cargo')
    grid_number = fields.Method("get_grid_number")
    grid_locations = fields.Method("get_grid_locations")
    start_time = fields.Method("get_start_time")
    end_time = fields.Method("get_end_time")
    commodity_code = fields.Method("get_commodity_code")
    commodity_description = fields.Method("get_commodity_description")
    sline_code = fields.Method("get_sline_code")
    warehouse_name = fields.Method("get_warehouse_name")
    stacking_type = fields.Method("get_stacking_type")

    def get_truck_number(self, obj):
        return obj.ctms_cargo.truck_number
    
    # def get_container_number(self, obj):
    #     return obj.ctms_cargo.container_number

    def get_package_count(self, obj):
        return obj.ctms_cargo.package_count

    def get_package_weight(self, obj):
        return obj.ctms_cargo.package_weight
    
    def get_damaged_count(self, obj):
        return obj.ctms_cargo.no_of_packages_damaged

    def get_damaged_packages_weight(self, obj):
        return obj.ctms_cargo.damaged_packages_weight

    def get_area(self, obj):
        return obj.ctms_cargo.area

    def get_area_damaged(self, obj):
        return obj.ctms_cargo.area_damaged
    
    def get_grid_number(self, obj):
        return obj.ctms_cargo.grid_number
    
    def get_grid_locations(self, obj):
        return obj.ctms_cargo.grid_locations
    
    def get_start_time(self, obj):
        return obj.ctms_cargo.start_time
    
    def get_end_time(self, obj):
        return obj.ctms_cargo.end_time
    
    def get_commodity_code(self, obj):
        return obj.commodity.comm_cd
    
    def get_commodity_description(self, obj):
        return obj.commodity.comm_desc
    
    def get_sline_code(self, obj):
        return "AA1233"

    def get_warehouse_name(self,obj):
        return obj.ctms_cargo.warehouse_name
    
    def get_stacking_type(self,obj):
        return obj.ctms_cargo.stacking_type
    class Meta:
        model = CCLSCargoDetails
        fields = ("shipping_bill", "bill_of_entry","bill_of_lading","package_code","package_count","package_weight","damaged_packages_weight","area","area_damaged","grid_locations","truck_number","start_time","end_time","cha_code","commodity_code","commodity_description","no_of_packages_damaged","area_damaged","sline_code","warehouse_name","stacking_type","bill_date")


class CCLSJobOrderSchema(ma.SQLAlchemyAutoSchema):

    cargo_details = fields.Nested(CCLSCargoDetailsSchema, many=True)
    carting_order_number = fields.String(data_key='cargo_carting_number')
    total_package_count = fields.Method("get_total_package_count")
    
    gate_number = fields.Method("get_gate_number")
    container_id = fields.String(data_key='container_number')
    
    fcl_or_lcl = fields.Number(data_key='container_flag')
    block_locations = fields.Method("get_block_locations")
    rack_locations = fields.Method("get_rack_locations")
    equipment_id = fields.Method("get_equipment_id")
    created_on_epoch = fields.Method("get_created_on_epoch")
    start_time = fields.Method("get_job_start_time")
    end_time = fields.Method("get_job_end_time")
    shipping_liner_code  = fields.String(data_key='sline_code')
    container_type = fields.Method("get_container_type")
    container_size =  fields.Method("get_container_size")
    container_iso_code = fields.Method("get_container_iso_code")

    def get_total_package_count(self, obj):
        return obj.ctms_job.total_package_count
    
    def get_gate_number(self,obj):
        return obj.ctms_job.gate_number
    
    def get_equipment_id(self,obj):
        return obj.ctms_job.equipment_id
    
    def get_job_start_time(self,obj):
        return obj.ctms_job.job_start_time
    
    def get_job_end_time(self,obj):
        return obj.ctms_job.job_end_time
    
    def get_created_on_epoch(self,obj):
        return obj.ctms_job.created_on_epoch
    
    def get_container_type(self,obj):
        return obj.container.container_type if obj.container else None
    
    def get_container_size(self,obj):
        return obj.container.container_size  if obj.container else None
    
    def get_container_iso_code(self,obj):
        return obj.container.container_iso_code  if obj.container else None

    class Meta:
        model = CCLSJobOrder
        fields = ("carting_order_number","crn_number","gpm_number","total_package_count","job_type","fcl_or_lcl","gate_number","cargo_details","equipment_id","created_on_epoch",'container_id','start_time','end_time','shipping_liner_code','container_location_code','container_life','container_type','container_size','container_iso_code','private_or_concor_labour_flag','icd_location_code','handling_code')
        include_relationships = True
    
class CCLSCommodityList(ma.SQLAlchemyAutoSchema):
    comm_cd = fields.String(data_key='commodity_code')
    comm_desc = fields.String(data_key='commodity_description')
    class Meta:
        model = WarehouseCommodity
        fields = ("comm_cd",'comm_desc')     
        
class InsertCCLSJobOrderSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = CCLSJobOrder
        load_instance = True
        include_fk = True
        fields=("job_type","fcl_or_lcl","con_date","crn_date","shipping_liner_code","party_code","cha_code","gw_port_code","container_location_code","container_life","gross_weight","gpm_number","gpm_valid_date","carting_order_number","crn_number","cargo_weight_in_crn","weight_remaining","stuffing_job_order","destuffing_job_order","private_or_concor_labour_flag","handling_code","icd_location_code","is_cargo_card_generated","reserve_flag","cncl_flag","hsn_code","destuffing_plan_date","hld_rls_flag","gp_stat")