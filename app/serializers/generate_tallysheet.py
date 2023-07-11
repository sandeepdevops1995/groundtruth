from marshmallow import fields, EXCLUDE, post_load, pre_load
from app import ma
from app.models.warehouse.ccls_cargo_details import CCLSCargoBillDetails
from app import postgres_db as db
from app.models.warehouse.ctms_cargo_job import CTMSCargoJob,CTMSBillDetails
from sqlalchemy import or_,and_
from app.serializers import Nested
from app.logger import logger
import app.logging_message as LM
import config
from app.models.warehouse.ccls_cargo_details import MasterCargoDetails

class CTMSBillDetailsInsertSchema(ma.SQLAlchemyAutoSchema):

    @post_load(pass_original=True)
    def get_ccls_bill_id(self, data, original_data, **kwargs):
        query_object = db.session.query(CCLSCargoBillDetails).filter(CCLSCargoBillDetails.job_order_id==self.context.get('job_order_id')).filter(or_(and_(CCLSCargoBillDetails.shipping_bill_number==original_data.get('shipping_bill'),CCLSCargoBillDetails.shipping_bill_number!=None),and_(CCLSCargoBillDetails.bill_of_entry==original_data.get('bill_of_entry'),CCLSCargoBillDetails.bill_of_entry!=None),and_(CCLSCargoBillDetails.bill_of_lading==original_data.get('bill_of_lading'),CCLSCargoBillDetails.bill_of_lading!=None))).order_by(CCLSCargoBillDetails.created_at.desc()).first()
        if query_object:
            data['ccls_bill_id'] = query_object.id
        logger.debug("{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GENERATE_TALLYSHEET,LM.KEY_GET_REQUEST_FROM_CTMS_FOR_GENERATE_TALLYSHEET,data))
        return data

    damaged_count = fields.Integer(attribute='no_of_packages_damaged')
    area_of_cargo = fields.Integer(attribute='area')
    area_of_damaged_cargo = fields.Integer(attribute='area_damaged')
    packages_weight = fields.Float(attribute='package_weight')
    concor_warehouse_id = fields.String(attribute='warehouse_id')
    
    class Meta:
        model = CTMSBillDetails
        fields = ("full_or_part_destuff", "package_count","damaged_count","area_of_cargo","grid_number","grid_locations","ccls_grid_locations","packages_weight","damaged_packages_weight","start_time","end_time","warehouse_name","concor_warehouse_id","stacking_type","area_of_damaged_cargo","gate_number")
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        # exclude = ("master_job_order",)

    ctms_cargo_job_id = ma.auto_field("ctms_job_order_bill_details")

class CTMSCargoJobInsertSchema(ma.SQLAlchemyAutoSchema):

    @pre_load()
    def change_data(self, data, **kwargs):
        job_type = self.context.get('job_type')
        db_obj = db.session.query(CTMSCargoJob).join(MasterCargoDetails).filter(MasterCargoDetails.job_type==job_type).order_by(CTMSCargoJob.id.desc()).first()
        if db_obj:
                serial_number = int(db_obj.serial_number)
                if config.IS_PREFIX_REQUIRED:
                    serial_number = str(serial_number+1)
                else:
                    serial_number = str(serial_number+1)
        else:
            serial_number = str(config.TS_SERIAL_NUMBER)
        data['serial_number'] = serial_number
        return data

    @post_load
    def get_job_id_from_context(self, data, **kwargs):
        data['job_order_id'] = self.context.get('job_order_id')
        return data

    start_time = fields.Integer(attribute='job_start_time')
    end_time = fields.Integer(attribute='job_end_time')
    class Meta:
        model = CTMSCargoJob
        fields = ("equipment_id", "ph_location", "start_time","end_time","total_package_count","total_no_of_packages_damaged","total_no_area","max_date_unloading","total_no_of_packages_excess","total_no_of_packages_short","gate_number","container_number","created_on_epoch","job_order_id","cargo_details","truck_number","serial_number")
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        # exclude = ("stuffing_cargo_id","destuffing_cargo_id","delivery_cargo_id",)

    cargo_details = Nested(CTMSBillDetailsInsertSchema, many=True, allow_none=True)