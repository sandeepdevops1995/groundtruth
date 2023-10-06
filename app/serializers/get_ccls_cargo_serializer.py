from app import ma
from marshmallow import fields, pre_dump, post_dump
from app.serializers.truck_serializer import GETTruckDetailsSchema
from app.models.warehouse.ccls_cargo_details import MasterCargoDetails, CCLSCargoBillDetails
from app.serializers import Nested


class CCLSCargoDetailsSchema(ma.SQLAlchemyAutoSchema):
    @post_dump()
    def get_data_from_context(self, data, **kwargs):
        if not data.get('cha_code'):
            data['cha_code'] = self.context.get('cha_code')
        if not data.get('exporter_name'):
            data['exporter_name'] = self.context.get('exporter_name')
        return data

    shipping_bill_number = fields.String(data_key='shipping_bill')
    bill_of_entry = fields.String()
    bill_of_lading = fields.String()
    commodity_details = fields.Method("get_commodity_details")

    def get_commodity_details(self, obj):
        commodity_details={}
        commodity_details['commodity_code'] = obj.commodity.comm_cd if obj.commodity else None
        commodity_details['commodity_description'] = obj.commodity.comm_desc if obj.commodity else None
        commodity_details['package_code'] = obj.package_code
        commodity_details['package_count'] = obj.no_of_packages_declared
        commodity_details['package_weight'] = obj.package_weight
        return [commodity_details]

    class Meta:
        model = CCLSCargoBillDetails
        fields = ("shipping_bill_number", "bill_of_entry","bill_of_lading","bill_date","bol_date","commodity_details","cha_code","exporter_name",'importer_name')



class GetCCLSJobSchema(ma.SQLAlchemyAutoSchema):

    @pre_dump()
    def add_data_to_context(self, data, **kwargs):
        self.context['cha_code'] = data.carting_details.cha_code if data.carting_details else data.delivery_details.cha_code if data.delivery_details else None
        self.context['exporter_name'] = data.carting_details.exporter_name if data.carting_details else None
        return data
    
    @post_dump()
    def sort_bill_details_by_date(self, data, **kwargs):
        data['bill_details'] = sorted(data['bill_details'], key=lambda d: d['bill_date'], reverse=True) 
        return data
    
    cargo_carting_number = fields.Method("get_con_number")
    crn_number = fields.Method("get_crn_number")
    gpm_number = fields.Method("get_gpm_number")
    gpm_created_date = fields.Method("get_gpm_created_date")
    fcl_or_lcl = fields.Integer(data_key='container_flag')
    container_number = fields.Method("get_container_number")
    container_size = fields.Method("get_container_size")
    is_cargo_card_generated = fields.Method("get_is_cargo_card_generated")
    stuffing_job_order = fields.Method("get_stuffing_job_order")
    destuffing_job_order = fields.Method("get_destuffing_job_order")
    sline_code = fields.Method("get_shipping_liner_code")
    crn_date = fields.Method("get_crn_date")
    con_date = fields.Method("get_con_date")
    gpm_valid_date = fields.Method("get_gpm_valid_date")
    truck_details = Nested(GETTruckDetailsSchema, many=True)
    bill_details = Nested(CCLSCargoDetailsSchema, many=True)

    def get_con_number(self,obj):
        return obj.carting_details.carting_order_number if obj.carting_details else None
    
    def get_container_number(self,obj):
        if obj.carting_details:
            container_number = []
            container_details = obj.carting_details.container_details
            if container_details:
                if isinstance(container_details,list):
                    for each_container in container_details:
                        container_number.append(each_container['container_number'])
                else:
                    container_number.append(container_details['container_number'])
            return container_number
        return obj.container_info.container_number  if obj.container_info else None
    
    def get_container_size(self,obj):
        return obj.container_info.container_size  if obj.container_info else None
    
    def get_crn_number(self, obj):
        return obj.carting_details.crn_number if obj.carting_details else obj.stuffing_details.crn_number if obj.stuffing_details else None
    
    def get_gpm_number(self, obj):
        return obj.delivery_details.gpm_number if obj.delivery_details else None
    
    def get_gpm_created_date(self, obj):
        return obj.delivery_details.gpm_created_date if obj.delivery_details else None
    
    def get_is_cargo_card_generated(self,obj):
        return obj.carting_details.is_cargo_card_generated if obj.carting_details else None
    
    def get_shipping_liner_code(self,obj):
        return obj.shipping_liner_code
    
    def get_stuffing_job_order(self,obj):
        return obj.stuffing_details.stuffing_job_order if obj.stuffing_details else None

    def get_destuffing_job_order(self,obj):
        return obj.destuffing_details.destuffing_job_order if obj.destuffing_details else None
    
    def get_crn_date(self,obj):
        return obj.carting_details.crn_date if obj.carting_details else obj.stuffing_details.crn_date if obj.stuffing_details else None
    
    def get_con_date(self,obj):
        return obj.carting_details.con_date if obj.carting_details else obj.stuffing_details.crn_date if obj.stuffing_details else None
    
    def get_gpm_valid_date(self,obj):
        return obj.delivery_details.gpm_valid_date if obj.delivery_details else None

    class Meta:
        model = MasterCargoDetails
        fields = ("cargo_carting_number", "container_flag", "container_number","container_size","crn_number","gpm_number","gpm_created_date","truck_details","bill_details","is_cargo_card_generated","sline_code","stuffing_job_order","destuffing_job_order","crn_date","con_date","gpm_valid_date","seal_number")
        include_relationships = True