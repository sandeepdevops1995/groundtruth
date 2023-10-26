from marshmallow import fields, EXCLUDE
from app import ma
from app import postgres_db as db
from app.models.warehouse.ctms_cargo_job import CTMSCargoJob,CTMSBillDetails
from sqlalchemy import or_
from app.serializers import Nested


class CTMSBillDetailsUpdateSchema(ma.SQLAlchemyAutoSchema):

    damaged_count = fields.Integer(attribute='no_of_packages_damaged')
    area_of_cargo = fields.Integer(attribute='area')
    area_of_damaged_cargo = fields.Integer(attribute='area_damaged')
    packages_weight = fields.Float(attribute='package_weight')
    
    class Meta:
        model = CTMSBillDetails
        fields = ("id","full_or_part_destuff", "package_count","damaged_count","area_of_cargo","grid_number","grid_locations","ccls_grid_locations","packages_weight","damaged_packages_weight","area_of_damaged_cargo","full_or_part_flag")
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        # exclude = ("master_job_order",)

    ctms_cargo_job_id = ma.auto_field("ctms_job_order_bill_details")

class CTMSCargoJobUpdateSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = CTMSCargoJob
        fields = ("total_package_count","total_no_of_packages_damaged","total_no_area","max_date_unloading","total_no_of_packages_excess","total_no_of_packages_short","cargo_details",'updated_at','truck_number','comments')
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        # exclude = ("stuffing_cargo_id","destuffing_cargo_id","delivery_cargo_id",)

    cargo_details = Nested(CTMSBillDetailsUpdateSchema, many=True, allow_none=True)