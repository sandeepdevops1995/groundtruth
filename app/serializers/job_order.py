from marshmallow import fields
import json
from app.Models.warehouse.job_order import CCLSJobOrder
from app.Models.warehouse.bill_details import CCLSCargoDetails
from app import ma
from app.Models.warehouse.commodity import WarehouseCommodity

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
        return obj.commodity.COMM_CD
    
    def get_commodity_description(self, obj):
        return obj.commodity.COMM_DESC
    
    def get_sline_code(self, obj):
        return "AD427"

    class Meta:
        model = CCLSCargoDetails
        fields = ("shipping_bill", "bill_of_entry","bill_of_lading","bill_date","importer_code","importer_name","package_code","package_count","package_weight","damaged_packages_weight","area","area_damaged","grid_locations","truck_number","start_time","end_time","sline_code","cha_code","commodity_code","commodity_description","no_of_packages_damaged","area_damaged")


class CCLSJobOrderSchema(ma.SQLAlchemyAutoSchema):

    cargo_details = fields.Nested(CCLSCargoDetailsSchema, many=True)
    carting_order_number = fields.String(data_key='cargo_carting_number')
    total_package_count = fields.Method("get_total_package_count")
    warehouse_name = fields.Method("get_warehouse_name")
    gate_number = fields.Method("get_gate_number")
    stacking_type = fields.Method("get_stacking_type")
    fcl_or_lcl = fields.Number(data_key='container_flag')
    block_locations = fields.Method("get_block_locations")
    rack_locations = fields.Method("get_rack_locations")
    equipment_id = fields.Method("get_equipment_id")
    created_on_epoch = fields.Method("get_created_on_epoch")

    def get_total_package_count(self, obj):
        return obj.ctms_job.total_package_count
    
    def get_warehouse_name(self,obj):
        return obj.ctms_job.warehouse_name
    
    def get_gate_number(self,obj):
        return obj.ctms_job.gate_number
    
    def get_stacking_type(self,obj):
        return 1
        return obj.ctms_job.stacking_type
    
    def get_block_locations(self,obj):
        return []
    
    def get_rack_locations(self,obj):
        return []
    
    def get_equipment_id(self,obj):
        return 1
    
    def get_created_on_epoch(self,obj):
        return 1678351776

    class Meta:
        model = CCLSJobOrder
        fields = ("carting_order_number","crn_number","gpm_number","total_package_count","job_type","fcl_or_lcl","warehouse_name","gate_number","stacking_type","cargo_details","block_locations","rack_locations","equipment_id","created_on_epoch")
        include_relationships = True

    
class CCLSCommodityList(ma.SQLAlchemyAutoSchema):
    COMM_CD = fields.String(data_key='commodity_code')
    COMM_DESC = fields.String(data_key='commodity_description')
    class Meta:
        model = WarehouseCommodity
        fields = ("COMM_CD",'COMM_DESC')