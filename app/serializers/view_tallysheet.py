from marshmallow import fields, post_dump, pre_dump
from app import ma
from app.models.warehouse.ctms_cargo_job import CTMSCargoJob,CTMSBillDetails


class CTMSbillDetailsSchema(ma.SQLAlchemyAutoSchema):

    @post_dump()
    def get_data_from_context(self, data, **kwargs):
        if not data.get('cha_code'):
            data['cha_code'] = self.context.get('cha_code')
        data['truck_number'] = self.context.get('truck_number_'+str(data['ctms_cargo_job_id']))
        return data

    shipping_bill = fields.Method("get_shipping_bill")
    bill_of_entry = fields.Method("get_bill_of_entry")
    bill_of_lading = fields.Method("get_bill_of_lading")
    package_code = fields.Method("get_package_code")
    package_weight = fields.Float(data_key='packages_weight')
    area = fields.Number(data_key='area_of_cargo')
    cha_code = fields.Method("get_cha_code")
    commodity_code = fields.Method("get_commodity_code")
    commodity_description = fields.Method("get_commodity_description")
    no_of_packages_damaged = fields.Number(data_key='damaged_count')
    area_damaged = fields.Number(data_key='area_of_damaged_cargo')
    bill_date = fields.Method("get_bill_date")
    bol_date = fields.Method("get_bol_date")
    warehouse_id = fields.String(data_key='wh_id')

    def get_shipping_bill(self, obj):
        return obj.ccls_bill.shipping_bill_number
    
    def get_bill_of_entry(self, obj):
        return obj.ccls_bill.bill_of_entry
    
    def get_bill_of_lading(self, obj):
        return obj.ccls_bill.bill_of_lading
    
    def get_package_code(self, obj):
        return obj.ccls_bill.package_code
    
    def get_cha_code(self, obj):
        return obj.ccls_bill.cha_code
    
    def get_commodity_code(self, obj):
        return obj.ccls_bill.commodity.comm_cd if obj.ccls_bill.commodity else None
    
    def get_commodity_description(self, obj):
        return obj.ccls_bill.commodity.comm_desc if obj.ccls_bill.commodity else None
    
    def get_bill_date(self, obj):
        return obj.ccls_bill.bill_date
    
    def get_bol_date(self, obj):
        return obj.ccls_bill.bol_date


    class Meta:
        model = CTMSBillDetails
        fields = ("id",'ctms_cargo_job_id',"shipping_bill", "bill_of_entry","bill_of_lading","package_code","package_count","package_weight","damaged_packages_weight","area","area_damaged","grid_locations","truck_number","start_time","end_time","cha_code","commodity_code","commodity_description","no_of_packages_damaged","warehouse_name","stacking_type","bill_date","warehouse_id","ccls_grid_locations","gate_number","bol_date")


class ViewTallySheetOrderSchema(ma.SQLAlchemyAutoSchema):

    @pre_dump()
    def add_data_to_context(self, data, **kwargs):
        self.context['cha_code'] = data.ctms_job_order.carting_details.cha_code if data.ctms_job_order.carting_details else data.ctms_job_order.delivery_details.cha_code if data.ctms_job_order.delivery_details else None
        self.context['truck_number_'+str(data.id)] = data.truck_number
        return data
    
    cargo_carting_number = fields.Method("get_cargo_carting_number")
    crn_number = fields.Method("get_crn_number")
    gpm_number = fields.Method("get_gpm_number")
    gpm_date = fields.Method("get_gpm_date")
    job_type = fields.Method("get_job_type")
    container_flag = fields.Method("get_fcl_or_lcl")
    container_number = fields.Method("get_container_number")
    job_start_time = fields.Integer(data_key='start_time')
    job_end_time = fields.Integer(data_key='end_time')
    sline_code = fields.Method("get_shipping_liner_code")
    container_location_code = fields.Method("get_container_location_code")
    container_life = fields.Method("get_container_life")
    container_type = fields.Method("get_container_type")
    container_size =  fields.Method("get_container_size")
    container_iso_code = fields.Method("get_container_iso_code")
    private_or_concor_labour_flag = fields.Method("get_private_or_concor_labour_flag")
    icd_location_code = fields.Method("get_icd_location_code")
    handling_code = fields.Method("get_handling_code")
    cha_code = fields.Method("get_cha_code")
    gw_port_code = fields.Method("get_gw_port_code")
    reserved_flag = fields.Method("get_reserve_flag")
    contractor_job_order_no = fields.Method("get_contractor_job_order_no")
    contractor_job_order_date = fields.Method("get_contractor_job_order_date")
    cargo_details = fields.Nested(CTMSbillDetailsSchema, many=True)

    def get_cargo_carting_number(self, obj):
        return obj.ctms_job_order.carting_details.carting_order_number if obj.ctms_job_order.carting_details else None
    
    def get_crn_number(self, obj):
        return obj.ctms_job_order.carting_details.crn_number if obj.ctms_job_order.carting_details else obj.ctms_job_order.stuffing_details.crn_number if obj.ctms_job_order.stuffing_details else None
    
    def get_gpm_number(self, obj):
        return obj.ctms_job_order.delivery_details.gpm_number if obj.ctms_job_order.delivery_details else None
    
    def get_gpm_date(self, obj):
        return obj.ctms_job_order.delivery_details.gpm_created_date if obj.ctms_job_order.delivery_details else None
    
    def get_job_type(self, obj):
        return obj.ctms_job_order.job_type
    
    def get_fcl_or_lcl(self, obj):
        return obj.ctms_job_order.fcl_or_lcl
    
    def get_container_number(self,obj):
        return obj.ctms_job_order.container_info.container_number  if obj.ctms_job_order.container_info else None
    
    def get_shipping_liner_code(self,obj):
        return obj.ctms_job_order.shipping_liner_code
    
    def get_container_location_code(self,obj):
        return obj.ctms_job_order.container_info.container_location_code  if obj.ctms_job_order.container_info else None
    
    def get_container_life(self,obj):
        return obj.ctms_job_order.container_info.container_life  if obj.ctms_job_order.container_info else None
    
    def get_container_type(self,obj):
        # return obj.job_order.container_type if obj.container else None
        return obj.ctms_job_order.container_info.container_type  if obj.ctms_job_order.container_info else None
    
    def get_container_size(self,obj):
        return obj.ctms_job_order.container_info.container_size  if obj.ctms_job_order.container_info else None
    
    def get_container_iso_code(self,obj):
        # return obj.job_order.container_iso_code  if obj.container else None
        return obj.ctms_job_order.container_info.container_iso_code  if obj.ctms_job_order.container_info else None
    
    def get_private_or_concor_labour_flag(self,obj):
        return obj.ctms_job_order.private_or_concor_labour_flag
    
    def get_icd_location_code(self,obj):
        return obj.ctms_job_order.icd_location_code
    
    def get_handling_code(self,obj):
        return obj.ctms_job_order.destuffing_details.handling_code if obj.ctms_job_order.destuffing_details else None
    
    def get_cha_code(self,obj):
        self.context['cha_code'] = obj.ctms_job_order.carting_details.cha_code if obj.ctms_job_order.carting_details else obj.ctms_job_order.delivery_details.cha_code if obj.ctms_job_order.delivery_details else None

    def get_gw_port_code(self,obj):
        return obj.ctms_job_order.carting_details.gw_port_code if obj.ctms_job_order.carting_details else obj.ctms_job_order.stuffing_details.gw_port_code if obj.ctms_job_order.stuffing_details else None
    
    def get_reserve_flag(self,obj):
        return obj.ctms_job_order.carting_details.reserve_flag if obj.ctms_job_order.carting_details else None
    
    def get_contractor_job_order_no(self,obj):
        return obj.ctms_job_order.carting_details.contractor_job_order_no if obj.ctms_job_order.carting_details else None
    
    def get_contractor_job_order_date(self,obj):
        return obj.ctms_job_order.carting_details.contractor_job_order_date if obj.ctms_job_order.carting_details else None

    class Meta:
        model = CTMSCargoJob
        fields = ("id","cargo_carting_number","crn_number","gpm_number","gpm_date","total_package_count","job_type","container_flag","equipment_id","created_on_epoch",'container_number','job_start_time','job_end_time','sline_code','container_location_code','container_life','container_type','container_size','container_iso_code','private_or_concor_labour_flag','icd_location_code','handling_code','cargo_details',"gw_port_code","reserved_flag","contractor_job_order_no","contractor_job_order_date")
        include_relationships = True