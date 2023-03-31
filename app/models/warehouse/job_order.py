from app import postgres_db as db
from app.enums import JobStatus
from datetime import datetime

class CCLSJobOrder(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    job_type = db.Column(db.Integer())
    fcl_or_lcl = db.Column(db.Integer())
    con_date = db.Column(db.BigInteger(), nullable=True)
    crn_date = db.Column(db.BigInteger(), nullable=True)
    shipping_liner_code = db.Column(db.String(10), nullable=True)
    party_code = db.Column(db.String(10), nullable=True)
    cha_code = db.Column(db.String(10), nullable=True)
    gw_port_code = db.Column(db.String(10), nullable=True)
    container_location_code = db.Column(db.String(10), nullable=True)
    container_life = db.Column(db.BigInteger(), nullable=True)
    gross_weight = db.Column(db.Float(), nullable=True)
    gpm_number = db.Column(db.String(10), nullable=True)
    gpm_created_date = db.Column(db.BigInteger(), nullable=True)
    carting_order_number = db.Column(db.String(13), nullable=True)
    crn_number = db.Column(db.String(13), nullable=True)
    cargo_weight_in_crn = db.Column(db.Float(), nullable=True)
    weight_remaining = db.Column(db.Float(), nullable=True)
    stuffing_job_order = db.Column(db.String(10), nullable=True)
    destuffing_job_order = db.Column(db.String(10), nullable=True)
    private_or_concor_labour_flag = db.Column(db.String(20), nullable=True)
    handling_code = db.Column(db.String(10), nullable=True)
    icd_location_code = db.Column(db.String(10), nullable=True)
    is_cargo_card_generated = db.Column(db.Boolean(),nullable=True)
    reserve_flag = db.Column(db.Boolean(),nullable=True)
    cargo_details = db.relationship('CCLSCargoDetails', backref='job_details')
    truck_details = db.relationship('TruckDetails', backref='job_order_truck')
    container_id = db.Column(db.String(11), db.ForeignKey('container.container_number'))
    container = db.relationship("Container")
    ctms_job_order_id = db.Column(db.Integer, db.ForeignKey('ctms_job_details.id'))
    ctms_job = db.relationship("CTMSJobOrder")
    status = db.Column(db.Integer(),default=JobStatus.INPROGRESS.value)
    
    # vehicle_nos
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    
    __tablename__ = 'ccls_job_details'

class CTMSJobOrder(db.Model):
    
    id =  db.Column(db.BigInteger(), primary_key=True)
    equipment_id = db.Column(db.String(13), nullable=True)
    ph_location = db.Column(db.String(13), nullable=True)
    # reserve_flag = db.Column(db.Boolean(),nullable=True)
    # shipping_liner_code = db.Column(db.String(10), nullable=True)
    # cha_code = db.Column(db.String(10), nullable=True)
    # gw_port_code = db.Column(db.String(10), nullable=True)
    job_start_time = db.Column(db.BigInteger(), nullable=True)
    job_end_time = db.Column(db.BigInteger(), nullable=True)
    total_package_count = db.Column(db.Integer(), nullable=True)
    # total_no_of_packages_stuffing = db.Column(db.Integer(), nullable=True)
    # total_no_of_packages_destuffing = db.Column(db.Integer(), nullable=True)
    # total_no_of_packages_delivered = db.Column(db.Integer(), nullable=True)
    total_no_of_packages_damaged = db.Column(db.Integer(), nullable=True)
    total_no_area = db.Column(db.Integer(), nullable=True)
    max_date_unloading = db.Column(db.BigInteger(), nullable=True)
    total_no_of_packages_excess = db.Column(db.Integer(), nullable=True)
    total_no_of_packages_short = db.Column(db.Integer(), nullable=True)
    gate_number = db.Column(db.String(10), nullable=True)
    container_number = db.Column(db.String(15), nullable=True)
    # cargo_weight_in_crn = db.Column(db.Float(), nullable=True)
    # weight_remaining = db.Column(db.Float(), nullable=True)
    # private_or_concor_labour_flag = db.Column(db.Boolean(),nullable=True)
    # handling_code = db.Column(db.String(10), nullable=True)
    warehouse_name = db.Column(db.String(50), nullable=True)
    # bill_details = db.relationship('FinalBillDetails', back_populates='ctms_job_order')
    # truck_id = db.Column(db.Integer, db.ForeignKey('truck_details.id'))
    # container_id = db.Column(db.Integer, db.ForeignKey('container.id'))
    # vehicle_nos
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    created_on_epoch = db.Column(db.BigInteger(), nullable=True)
    
    __tablename__ = 'ctms_job_details'