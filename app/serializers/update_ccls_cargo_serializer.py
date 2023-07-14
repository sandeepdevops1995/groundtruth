from marshmallow import fields, EXCLUDE, pre_load
from app import ma
from app.models.warehouse.ccls_cargo_details import MasterCargoDetails,CartingCargoDetails,CCLSCargoBillDetails,StuffingCargoDetails,DeStuffingCargoDetails,DeliveryCargoDetails
from app import postgres_db as db
from app.serializers.container_serializer import ContainerUpdateSchema
from app.models.master.warehouse import Commodity as WarehouseCommodity
from app.serializers import Nested

class CartingJobUpdateSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = CartingCargoDetails
        fields = ("id","crn_number", "crn_date", "carting_order_number","con_date","is_cargo_card_generated","cha_code","gw_port_code","party_code","reserve_flag","max_date_unloading","contractor_job_order_no","contractor_job_order_date")
        include_relationships = True
        load_instance = True
 
class StuffingJobUpdateSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = StuffingCargoDetails
        fields = ("id","container_number", "stuffing_job_order", "crn_number", "cargo_weight_in_crn","hsn_code","gw_port_code")
        include_relationships = True
        load_instance = True

class DeStuffingJobUpdateSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = DeStuffingCargoDetails
        fields = ("id","container_number", "destuffing_job_order", "destuffing_plan_date","handling_code","hld_rls_flag")
        include_relationships = True
        load_instance = True
 
class DeliveryJobUpdateSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = DeliveryCargoDetails
        fields = ("id","gpm_number", "gpm_valid_date", "gp_stat","con_date","cha_code","gpm_created_date")
        include_relationships = True
        load_instance = True

class CCLSBillDetailsUpdateSchema(ma.SQLAlchemyAutoSchema):

    @pre_load()
    def change_data(self, data, **kwargs):
        data['bill_date'] = data.get('shipping_bill_date') if 'shipping_bill_date' in data else data.get('bill_date')
        # date_time_str = '2002-01-19 00:00:00.000+05:30'
        # data['bill_date'] = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f%z')
        # if data['bill_date'] and isinstance(data['bill_date'], datetime):
        #         data['bill_date']=convert_ccls_date_to_timestamp(data['bill_date'])
        query_object = db.session.query(WarehouseCommodity).filter(WarehouseCommodity.comm_cd==data.get('commodity_code')).first()
        if query_object:
            data['commodity_id'] = query_object.id
        return data

    boe_number = fields.String(attribute='bill_of_entry',allow_none=True)
    bol_number = fields.String(attribute='bill_of_lading',allow_none=True)

    class Meta:
        model = CCLSCargoBillDetails
        fields = ("id","shipping_bill_number", "boe_number","bol_number","bill_date","bol_date","importer_code","importer_name","package_code","no_of_packages_declared","package_weight","cha_code","cargo_type","commodity_id","job_order_id","exporter_name")
        # include_relationships = True
        load_instance = True
        unknown = EXCLUDE
       

class CCLSCargoUpdateSchema(ma.SQLAlchemyAutoSchema):

    @pre_load()
    def change_key_name(self, data, **kwargs):
        data['gross_weight'] = data.get('gross_weight') if 'gross_weight' in data else data.get('cargo_gross_weight') if 'cargo_gross_weight' in data else None
        data['shipping_liner_code'] = data.get('shipping_liner_code') if 'shipping_liner_code' in data else data.get('shipping_line_code') if 'shipping_line_code' in data else None
        return data
    
    class Meta:
        model = MasterCargoDetails
        fields = ("id","gross_weight", "private_or_concor_labour_flag", "shipping_liner_code","cncl_flag","icd_location_code","container_info","carting_details","job_type","fcl_or_lcl","stuffing_details","destuffing_details","delivery_details","cha_name")
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE

    container_info = Nested(ContainerUpdateSchema, allow_none=True)
    container_id = ma.auto_field("master_job_container")
    carting_details = Nested(CartingJobUpdateSchema, allow_none=True)
    carting_cargo_id = ma.auto_field("carting_job")
    stuffing_details = Nested(StuffingJobUpdateSchema, allow_none=True)
    stuffing_cargo_id = ma.auto_field("stuffing_job")
    destuffing_details = Nested(DeStuffingJobUpdateSchema, allow_none=True)
    destuffing_cargo_id = ma.auto_field("destuffing_job")
    delivery_details = Nested(DeliveryJobUpdateSchema, allow_none=True)
    delivery_cargo_id = ma.auto_field("delivery_job")


class CCLSBillDetailsGetSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = CCLSCargoBillDetails
        fields = ("id","shipping_bill_number", "bill_of_entry","bill_of_lading")