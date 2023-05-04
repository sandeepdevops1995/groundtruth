from marshmallow import fields, EXCLUDE, post_load
from app import ma
from app.models.warehouse.ccls_cargo_details import CCLSCargoBillDetails
from app import postgres_db as db
from app.models.warehouse.ctms_cargo_job import CTMSCargoJob,CTMSBillDetails
from sqlalchemy import or_,and_


class Nested(fields.Nested):
    """Nested field that inherits the session from its parent."""

    def _deserialize(self, *args, **kwargs):
        if hasattr(self.schema, "session"):
            self.schema.session = db.session  # overwrite session here
            self.schema.transient = self.root.transient
        return super()._deserialize(*args, **kwargs)

class CTMSBillDetailsInsertSchema(ma.SQLAlchemyAutoSchema):

    @post_load(pass_original=True)
    def get_ccls_bill_id(self, data, original_data, **kwargs):
        query_object = db.session.query(CCLSCargoBillDetails).filter(CCLSCargoBillDetails.job_order_id==self.context.get('job_order_id')).filter(or_(and_(CCLSCargoBillDetails.shipping_bill_number==original_data.get('shipping_bill'),CCLSCargoBillDetails.shipping_bill_number!=None),and_(CCLSCargoBillDetails.bill_of_entry==original_data.get('bill_of_entry'),CCLSCargoBillDetails.bill_of_entry!=None),and_(CCLSCargoBillDetails.bill_of_lading==original_data.get('bill_of_lading'),CCLSCargoBillDetails.bill_of_lading!=None))).order_by(CCLSCargoBillDetails.created_at.desc()).first()
        if query_object:
            data['ccls_bill_id'] = query_object.id
        return data

    damaged_count = fields.Integer(attribute='no_of_packages_damaged')
    area_of_cargo = fields.Integer(attribute='area')
    area_of_damaged_cargo = fields.Integer(attribute='area_damaged')
    packages_weight = fields.Integer(attribute='package_weight')
    concor_warehouse_id = fields.String(attribute='warehouse_id')
    
    class Meta:
        model = CTMSBillDetails
        fields = ("full_or_part_destuff", "package_count","damaged_count","area_of_cargo","grid_number","grid_locations","ccls_grid_locations","packages_weight","damaged_packages_weight","start_time","end_time","warehouse_name","concor_warehouse_id","stacking_type","area_of_damaged_cargo")
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        # exclude = ("master_job_order",)

    ctms_cargo_job_id = ma.auto_field("ctms_job_order_bill_details")

class CTMSCargoJobInsertSchema(ma.SQLAlchemyAutoSchema):

    @post_load
    def get_job_id_from_context(self, data, **kwargs):
        data['job_order_id'] = self.context.get('job_order_id')
        return data

    start_time = fields.Integer(attribute='job_start_time')
    end_time = fields.Integer(attribute='job_end_time')
    class Meta:
        model = CTMSCargoJob
        fields = ("equipment_id", "ph_location", "start_time","end_time","total_package_count","total_no_of_packages_damaged","total_no_area","max_date_unloading","total_no_of_packages_excess","total_no_of_packages_short","gate_number","container_number","created_on_epoch","job_order_id","cargo_details","truck_number")
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        # exclude = ("stuffing_cargo_id","destuffing_cargo_id","delivery_cargo_id",)

    cargo_details = Nested(CTMSBillDetailsInsertSchema, many=True, allow_none=True)