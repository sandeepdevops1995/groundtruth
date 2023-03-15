from app import postgres_db as db
from datetime import datetime
from app.Models.utils import IntegerDateTime
from sqlalchemy import JSON

class CCLSCargoDetails(db.Model):
    def __init__(self, **kwargs):
        allowed_args = self.__mapper__.class_manager  # returns a dict
        kwargs = {k: v for k, v in kwargs.items() if k in allowed_args}
        super().__init__(**kwargs)
    id =  db.Column(db.BigInteger(), primary_key=True)
    commodity_id = db.Column(db.Integer, db.ForeignKey('wh_commodity.id'))
    commodity = db.relationship("WarehouseCommodity")
    shipping_bill = db.Column(db.Integer(), nullable=True)
    bill_of_entry = db.Column(db.Integer(), nullable=True)
    bill_of_lading = db.Column(db.Integer(), nullable=True)
    bill_date = db.Column(db.BigInteger(), nullable=True)
    importer_code = db.Column(db.String(30), nullable=True)
    importer_name = db.Column(db.String(100), nullable=True)
    package_code = db.Column(db.String(10), nullable=True)
    no_of_packages_declared = db.Column(db.String(11))
    package_weight = db.Column(db.Float(), nullable=True)
    cha_code = db.Column(db.String(10), nullable=True)
    job_order_id = db.Column(db.Integer, db.ForeignKey('ccls_job_details.id'))
    ctms_cargo_id = db.Column(db.Integer, db.ForeignKey('ctms_cargo_details.id'))
    ctms_cargo = db.relationship("CTMSCargoDetails")
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    
    __tablename__ = 'ccls_cargo_details'

class CTMSCargoDetails(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    # commodity_id = db.Column(db.Integer, db.ForeignKey('wh_commodity.id'))
    # shipping_bill = db.Column(db.Integer(), nullable=True)
    # bill_of_entry = db.Column(db.Integer(), nullable=True)
    # bill_of_lading = db.Column(db.Integer(), nullable=True)
    # bill_date = db.Column(db.BigInteger(), nullable=True)
    # importer_code = db.Column(db.String(10), nullable=True)
    # importer_name = db.Column(db.String(10), nullable=True)
    # package_code = db.Column(db.String(10), nullable=True)
    full_or_part_destuff = db.Column(db.String(10), nullable=True)
    package_count = db.Column(db.Integer(), nullable=True)
    no_of_packages_damaged = db.Column(db.Integer(), nullable=True)
    area = db.Column(db.Integer(), nullable=True)
    grid_number = db.Column(db.Integer(), nullable=True)
    area_damaged = db.Column(db.Integer(), nullable=True)
    grid_locations = db.Column(JSON,nullable=True)
    # cha_code = db.Column(db.String(10), nullable=True)
    package_weight = db.Column(db.Float(), nullable=True)
    damaged_packages_weight = db.Column(db.Float(), nullable=True)
    truck_number = db.Column(db.String(15), nullable=True)
    # container_number = db.Column(db.String(15), nullable=True)
    start_time = db.Column(db.BigInteger(), nullable=True)
    end_time = db.Column(db.BigInteger(), nullable=True)
    warehouse_name = db.Column(db.String(50), nullable=True)
    stacking_type = db.Column(db.Integer(), nullable=True)
    # ctms_job_order = db.relationship("FinalJobOrder", back_populates="bill_details")
    # job_order_id = db.Column(db.Integer, db.ForeignKey('final_job_order.id'))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    
    __tablename__ = 'ctms_cargo_details'