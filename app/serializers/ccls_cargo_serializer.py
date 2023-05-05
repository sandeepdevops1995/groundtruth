from marshmallow import fields, EXCLUDE, pre_load
from app import ma
from app.serializers.truck_serializer import TruckInsertSchema
from app.models.warehouse.ccls_cargo_details import MasterCargoDetails,CartingCargoDetails,CCLSCargoBillDetails,StuffingCargoDetails,DeStuffingCargoDetails,DeliveryCargoDetails
from app import postgres_db as db
from app.serializers.container_serializer import ContainerInsertSchema
from app.models.master.warehouse import Commodity as WarehouseCommodity
from datetime import datetime
from app.controllers.utils import convert_ccls_date_to_timestamp

class Nested(fields.Nested):
    """Nested field that inherits the session from its parent."""

    def _deserialize(self, *args, **kwargs):
        if hasattr(self.schema, "session"):
            self.schema.session = db.session  # overwrite session here
            self.schema.transient = self.root.transient
        return super()._deserialize(*args, **kwargs)

class CartingJobInsertSchema(ma.SQLAlchemyAutoSchema):

    @pre_load()
    def change_data(self, data, **kwargs):
        if data['con_date'] and isinstance(data['con_date'], datetime):
                data['con_date']=convert_ccls_date_to_timestamp(data['con_date'])
        if data['crn_date'] and isinstance(data['crn_date'], datetime):
                data['crn_date']=convert_ccls_date_to_timestamp(data['crn_date'])
        return data
    class Meta:
        model = CartingCargoDetails
        fields = ("crn_number", "crn_date", "carting_order_number","con_date","is_cargo_card_generated","cha_code","gw_port_code","party_code","reserve_flag")
        include_relationships = True
        load_instance = True
 
class StuffingJobInsertSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = StuffingCargoDetails
        fields = ("container_number", "stuffing_job_order", "cargo_weight_in_crn","hsn_code")
        include_relationships = True
        load_instance = True

class DeStuffingJobInsertSchema(ma.SQLAlchemyAutoSchema):

    @pre_load()
    def change_data(self, data, **kwargs):
        if data['destuffing_plan_date'] and isinstance(data['destuffing_plan_date'], datetime):
                data['destuffing_plan_date']=convert_ccls_date_to_timestamp(data['destuffing_plan_date'])
        return data
    
    class Meta:
        model = DeStuffingCargoDetails
        fields = ("container_number", "destuffing_job_order", "destuffing_plan_date","handling_code","hld_rls_flag")
        include_relationships = True
        load_instance = True
 
class DeliveryJobInsertSchema(ma.SQLAlchemyAutoSchema):

    @pre_load()
    def change_data(self, data, **kwargs):
        if data['gpm_valid_date'] and isinstance(data['gpm_valid_date'], datetime):
                data['gpm_valid_date']=convert_ccls_date_to_timestamp(data['gpm_valid_date'])
        return data

    class Meta:
        model = DeliveryCargoDetails
        fields = ("gpm_number", "gpm_valid_date", "gp_stat","con_date","cha_code")
        include_relationships = True
        load_instance = True

class CCLSBillDetailsInsertSchema(ma.SQLAlchemyAutoSchema):

    @pre_load()
    def change_data(self, data, **kwargs):
        print("CCLSBillDetailsInsertSchema---------",data)
        data['bill_date'] = data.get('shipping_bill_date') if 'shipping_bill_date' in data else data.get('bill_date')
        # date_time_str = '2002-01-19 00:00:00.000+05:30'
        # data['bill_date'] = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f%z')
        if data['bill_date'] and isinstance(data['bill_date'], datetime):
                data['bill_date']=convert_ccls_date_to_timestamp(data['bill_date'])
        # print("data['bill_date']-------",data['bill_date'])
        query_object = db.session.query(WarehouseCommodity).filter(WarehouseCommodity.comm_cd==data.get('commodity_code')).first()
        if query_object:
            data['commodity_id'] = query_object.id
        return data

    # shipping_bill_date = fields.Integer(attribute='bill_date')
    boe_number = fields.Integer(attribute='bill_of_entry')
    bol_number = fields.Integer(attribute='bill_of_lading')

    class Meta:
        model = CCLSCargoBillDetails
        fields = ("shipping_bill_number", "boe_number","bol_number","bill_date","importer_code","importer_name","package_code","no_of_packages_declared","package_weight","cha_code","cargo_type","commodity_id")
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        # exclude = ("master_job_order",)

    # job_order_id = ma.auto_field("master_job_order_truck")

class CCLSCargoInsertSchema(ma.SQLAlchemyAutoSchema):
    @pre_load()
    def change_key_name(self, data, **kwargs):
        data['bill_details'] = data.get('shipping_bill_details_list') if 'shipping_bill_details_list' in data else data.get('bill_details_list')
        return data

    class Meta:
        model = MasterCargoDetails
        fields = ("gross_weight", "private_or_concor_labour_flag", "shipping_liner_code","cncl_flag","icd_location_code","truck_details","container_info","bill_details","carting_details","job_type","fcl_or_lcl","stuffing_details","destuffing_details","delivery_details")
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        # exclude = ("stuffing_cargo_id","destuffing_cargo_id","delivery_cargo_id",)

    truck_details = Nested(TruckInsertSchema, many=True, allow_none=True)
    container_info = Nested(ContainerInsertSchema, allow_none=True)
    container_id = ma.auto_field("master_job_container")
    carting_details = Nested(CartingJobInsertSchema, allow_none=True)
    carting_cargo_id = ma.auto_field("carting_job")
    stuffing_details = Nested(StuffingJobInsertSchema, allow_none=True)
    stuffing_cargo_id = ma.auto_field("stuffing_job")
    destuffing_details = Nested(DeStuffingJobInsertSchema, allow_none=True)
    destuffing_cargo_id = ma.auto_field("destuffing_job")
    delivery_details = Nested(DeliveryJobInsertSchema, allow_none=True)
    delivery_cargo_id = ma.auto_field("delivery_job")
    bill_details = Nested(CCLSBillDetailsInsertSchema, many=True, allow_none=True)