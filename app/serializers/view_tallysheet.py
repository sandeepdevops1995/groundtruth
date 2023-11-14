from marshmallow import fields, post_dump, pre_dump
from app import ma
from app.models.warehouse.ctms_cargo_job import CTMSCargoJob,CTMSBillDetails
import config
from app.enums import JobOrderType, SerialNumberType
from app.models.warehouse.truck import TruckDetails
from app import postgres_db as db


class CTMSbillDetailsSchema(ma.SQLAlchemyAutoSchema):

    @post_dump()
    def get_data_from_context(self, data, **kwargs):
        if not data.get('cha_code'):
            data['cha_code'] = self.context.get('cha_code')
        if not data.get('cha_name'):
            data['cha_name'] = self.context.get('cha_name')
        data['truck_number'] = self.context.get('truck_number_'+str(data['ctms_cargo_job_id']))
        data['container_number'] = self.context.get('container_number_'+str(data['ctms_cargo_job_id']))
        truck_query = db.session.query(TruckDetails).filter(TruckDetails.truck_number==data['truck_number']).order_by(TruckDetails.created_at.desc()).first()
        if truck_query:
            data['truck_arrival_date'] = truck_query.truck_arrival_date
        else:
            data['truck_arrival_date'] = None
        if not data.get('exporter_name'):
            data['exporter_name'] = self.context.get('exporter_name')
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
    exporter_name = fields.Method("get_exporter_name")
    importer_name = fields.Method("get_importer_name")
    no_of_packages_declared = fields.Method("get_no_of_packages_declared")
    cha_name = fields.Method("get_cha_name")
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
    
    def get_cha_code(self, obj):
        return obj.ccls_bill.cha_code
    
    def get_commodity_code(self, obj):
        return obj.ccls_bill.commodity.comm_cd if obj.ccls_bill.commodity else None
    
    def get_commodity_description(self, obj):
        return obj.ccls_bill.commodity.comm_desc if obj.ccls_bill and obj.ccls_bill.commodity else None
    
    def get_bill_date(self, obj):
        return obj.ccls_bill.bill_date
    
    def get_bol_date(self, obj):
        return obj.ccls_bill.bol_date
    
    def get_exporter_name(self,obj):
        return obj.ccls_bill.exporter_name
    
    def get_importer_name(self,obj):
        return obj.ccls_bill.importer_name
    
    def get_no_of_packages_declared(self,obj):
        return obj.ccls_bill.no_of_packages_declared
    
    def get_cha_name(self, obj):
        return obj.ccls_bill.cha_name
    
    def get_hsn_code(self, obj):
        return obj.ccls_bill.hsn_code
    
    def get_ctms_start_time(self, obj):
        return obj.start_time
    
    def get_ctms_end_time(self, obj):
        return obj.end_time


    class Meta:
        model = CTMSBillDetails
        fields = ("id",'ctms_cargo_job_id',"shipping_bill", "bill_of_entry","bill_of_lading","package_code","package_count","package_weight","damaged_packages_weight","area","area_damaged","grid_locations","truck_number","ctms_start_time","ctms_end_time","cha_code","commodity_code","commodity_description","no_of_packages_damaged","warehouse_name","stacking_type","bill_date","warehouse_id","ccls_grid_locations","gate_number","bol_date","exporter_name","importer_name","no_of_packages_declared",'hsn_code')


class ViewTallySheetOrderSchema(ma.SQLAlchemyAutoSchema):

    @pre_dump()
    def add_data_to_context(self, data, **kwargs):
        self.context['cha_code'] = data.ctms_job_order.carting_details.cha_code if data.ctms_job_order.carting_details else data.ctms_job_order.delivery_details.cha_code if data.ctms_job_order.delivery_details else None
        self.context['exporter_name'] =  data.ctms_job_order.carting_details.exporter_name if data.ctms_job_order.carting_details else None
        self.context['truck_number_'+str(data.id)] = data.truck_number
        self.context['container_number_'+str(data.id)] = data.container_number
        return data
    
    @post_dump()
    def update_data(self, data, **kwargs):
        if data.get('job_type') in [JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value]:
            if not data.get('destuffing_date'):
                container_number = data.get('container_number')
                from app.services.warehouse.wh_tallysheet import WarehouseTallySheetView
                data['destuffing_date'] = WarehouseTallySheetView().get_destuffing_date_for_delivery(container_number)
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
    gross_weight = fields.Method("get_gross_weight")
    cha_name = fields.Method("get_cha_name")
    serial_number = fields.Method("get_serial_number")
    seal_number = fields.Method("get_seal_number")
    ccls_seal_number = fields.Method("get_ccls_seal_number")
    exporter_name = fields.Method("get_exporter_name")
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
    
    def get_gpm_date(self, obj):
        return obj.ctms_job_order.delivery_details.gpm_created_date if obj.ctms_job_order.delivery_details else None
    
    def get_job_type(self, obj):
        return obj.ctms_job_order.job_type
    
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
    
    def get_container_location_code(self,obj):
        return obj.ctms_job_order.container_info.container_location_code  if obj.ctms_job_order.container_info else None
    
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
    
    def get_gross_weight(self,obj):
        return obj.ctms_job_order.gross_weight
    
    def get_cha_name(self,obj):
        return obj.ctms_job_order.cha_name
    
    def get_serial_number(self,obj):
        if config.IS_PREFIX_REQUIRED:
            job_type=obj.ctms_job_order.job_type
            if job_type in [JobOrderType.CARTING_FCL.value,JobOrderType.CARTING_LCL.value]:
                serial_number_prefix=SerialNumberType.CARTING.value
            elif job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value]:
                serial_number_prefix=SerialNumberType.STUFFING.value
            elif job_type == JobOrderType.DIRECT_STUFFING.value:
                serial_number_prefix=SerialNumberType.DIRECT_STUFFING.value
            elif job_type in [JobOrderType.DE_STUFFING_FCL.value,JobOrderType.DE_STUFFING_LCL.value]:
                serial_number_prefix=SerialNumberType.DESTUFFING.value
            elif job_type in [JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value]:
                serial_number_prefix=SerialNumberType.DELIVERY.value
            elif job_type == JobOrderType.DIRECT_DELIVERY.value:
                serial_number_prefix=SerialNumberType.DIRECT_DELIVERY.value
            return serial_number_prefix+str(obj.serial_number)
        return obj.serial_number
    
    def get_seal_number(self,obj):
        return obj.seal_number
    
    def get_ccls_seal_number(self,obj):
        return obj.ctms_job_order.seal_number
    
    def get_exporter_name(self,obj):
        self.context['exporter_name'] =  obj.ctms_job_order.carting_details.exporter_name if obj.ctms_job_order.carting_details else None

    def get_destuffing_plan_date(self,obj):
        return obj.ctms_job_order.destuffing_details.destuffing_plan_date if obj.ctms_job_order.destuffing_details else None
    
    def get_cncl_flag(self,obj):
        return obj.ctms_job_order.cncl_flag
    
    def get_is_cargo_card_generated(self,obj):
        return obj.ctms_job_order.carting_details.is_cargo_card_generated if obj.ctms_job_order.carting_details else None

    class Meta:
        model = CTMSCargoJob
        fields = ("id","cargo_carting_number","crn_number","gpm_number","gpm_date","total_package_count","job_type","container_flag","equipment_id","created_on_epoch",'container_number','job_start_time','job_end_time','sline_code','container_location_code','container_life','container_type','container_size','container_iso_code','private_or_concor_labour_flag','icd_location_code','handling_code','cargo_details',"gw_port_code","reserved_flag","contractor_job_order_no","contractor_job_order_date","gross_weight","cha_name","serial_number","ccls_seal_number","destuffing_date","seal_number","created_at","updated_at","created_by","updated_by",'comments','destuffing_plan_date','cncl_flag','is_cargo_card_generated')
        include_relationships = True