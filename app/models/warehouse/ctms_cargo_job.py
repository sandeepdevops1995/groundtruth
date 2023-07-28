from app import postgres_db as db
from datetime import datetime
from sqlalchemy import JSON
from app.enums import JobStatus




class CTMSCargoJob(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    serial_number = db.Column(db.String(20), nullable=True)
    equipment_id = db.Column(db.String(13), nullable=True)
    ph_location = db.Column(db.String(13), nullable=True)
    job_start_time = db.Column(db.BigInteger(), nullable=True)
    job_end_time = db.Column(db.BigInteger(), nullable=True)
    total_package_count = db.Column(db.Integer(), nullable=True)
    total_no_of_packages_damaged = db.Column(db.Integer(), nullable=True)
    total_no_area = db.Column(db.Integer(), nullable=True)
    max_date_unloading = db.Column(db.BigInteger(), nullable=True)
    total_no_of_packages_excess = db.Column(db.Integer(), nullable=True)
    total_no_of_packages_short = db.Column(db.Integer(), nullable=True)
    container_number = db.Column(db.String(15), nullable=True)
    truck_number = db.Column(db.String(15), nullable=True)
    created_on_epoch = db.Column(db.BigInteger(), nullable=True)
    destuffing_date = db.Column(db.BigInteger(), nullable=True)
    seal_number = db.Column(db.String(15), nullable=True)
    job_order_id = db.Column(db.BigInteger, db.ForeignKey('ccls_master_cargo_details.id'))
    ctms_job_order = db.relationship("MasterCargoDetails", back_populates='ccls_cargo_master', lazy='joined')
    cargo_details = db.relationship('CTMSBillDetails', back_populates='ctms_job_order_bill_details', lazy='joined')
    status = db.Column(db.Integer(), default=JobStatus.TALLYSHEET_GENERATED.value)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow())
    created_by = db.Column(db.String(100), nullable=True)
    updated_by = db.Column(db.String(100), nullable=True)

    __tablename__ = 'ctms_cargo_job'


class CTMSBillDetails(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    full_or_part_destuff = db.Column(db.String(10), nullable=True)
    package_count = db.Column(db.Integer(), nullable=True)
    no_of_packages_damaged = db.Column(db.Integer(), nullable=True)
    area = db.Column(db.Integer(), nullable=True)
    grid_number = db.Column(db.Integer(), nullable=True)
    area_damaged = db.Column(db.Integer(), nullable=True)
    grid_locations = db.Column(JSON,nullable=True)
    ccls_grid_locations = db.Column(JSON,nullable=True)
    package_weight = db.Column(db.Float(), nullable=True)
    damaged_packages_weight = db.Column(db.Float(), nullable=True)
    start_time = db.Column(db.BigInteger(), nullable=True)
    end_time = db.Column(db.BigInteger(), nullable=True)
    warehouse_name = db.Column(db.String(50), nullable=True)
    gate_number = db.Column(db.String(10), nullable=True)
    warehouse_id = db.Column(db.String(50), nullable=True)
    stacking_type = db.Column(db.Integer(), nullable=True)
    ctms_cargo_job_id = db.Column(db.Integer, db.ForeignKey('ctms_cargo_job.id'))
    ctms_job_order_bill_details = db.relationship("CTMSCargoJob", back_populates="cargo_details", lazy='joined')
    ccls_bill_id = db.Column(db.Integer, db.ForeignKey('ccls_cargo_bill_details.id'))
    ccls_bill = db.relationship('CCLSCargoBillDetails', back_populates='ctms_cargo_details', lazy='joined')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    
    __tablename__ = 'ctms_cargo_job_bill_details'