from app import postgres_db as db
from datetime import datetime

class MasterCargoDetails(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    job_type = db.Column(db.Integer())
    fcl_or_lcl = db.Column(db.Integer())
    container_id = db.Column(db.String(11), db.ForeignKey('container.id'))
    container_info = db.relationship("Container", back_populates="master_job_container", lazy='joined')
    truck_details = db.relationship('TruckDetails', back_populates='master_job_order_truck')
    gross_weight = db.Column(db.Float(), nullable=True)
    private_or_concor_labour_flag = db.Column('private_or_concor_flag',db.String(1), nullable=True)
    shipping_liner_code = db.Column(db.String(20), nullable=True)
    cncl_flag = db.Column(db.String(1), nullable=True)
    icd_location_code = db.Column(db.String(20), nullable=True)
    cha_name = db.Column(db.String(100), nullable=True)
    seal_number = db.Column(db.String(20), nullable=True)
    carting_cargo_id = db.Column(db.BigInteger(), db.ForeignKey('ccls_carting_cargo_details.id'))
    carting_details = db.relationship("CartingCargoDetails", back_populates="carting_job", lazy='joined')
    stuffing_cargo_id = db.Column(db.BigInteger(), db.ForeignKey('ccls_stuffing_cargo_details.id'))
    stuffing_details = db.relationship("StuffingCargoDetails", back_populates="stuffing_job", lazy='joined')
    destuffing_cargo_id = db.Column(db.BigInteger(), db.ForeignKey('ccls_destuffing_cargo_details.id'))
    destuffing_details = db.relationship("DeStuffingCargoDetails", back_populates="destuffing_job", lazy='joined')
    delivery_cargo_id = db.Column(db.BigInteger(), db.ForeignKey('ccls_delivery_cargo_details.id'))
    delivery_details = db.relationship("DeliveryCargoDetails", back_populates="delivery_job", lazy='joined')
    bill_details = db.relationship('CCLSCargoBillDetails', back_populates='master_job_order_bill_details', lazy='joined')
    ccls_cargo_master = db.relationship("CTMSCargoJob", back_populates='ctms_job_order', lazy='joined')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow())
    created_by = db.Column(db.String(100), nullable=True)
    updated_by = db.Column(db.String(100), nullable=True)

    __tablename__ = 'ccls_master_cargo_details'




class CartingCargoDetails(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    crn_number = db.Column(db.String(20), nullable=True)
    crn_date = db.Column(db.BigInteger(), nullable=True)
    carting_order_number = db.Column(db.String(20), nullable=True)
    con_date = db.Column(db.BigInteger(), nullable=True)
    is_cargo_card_generated = db.Column(db.String(1), nullable=True)
    cha_code = db.Column(db.String(20), nullable=True)
    gw_port_code = db.Column(db.String(20), nullable=True)
    party_code = db.Column(db.String(20), nullable=True)
    reserve_flag = db.Column(db.String(1), nullable=True)
    max_date_unloading = db.Column(db.BigInteger(), nullable=True)
    contractor_job_order_no = db.Column(db.String(20), nullable=True)
    contractor_job_order_date = db.Column(db.BigInteger(), nullable=True)
    exporter_name = db.Column(db.String(100), nullable=True)
    carting_job = db.relationship("MasterCargoDetails", back_populates="carting_details", lazy='joined')

    __tablename__ = 'ccls_carting_cargo_details'

class StuffingCargoDetails(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    container_number = db.Column(db.String(20))
    crn_number = db.Column(db.String(20), nullable=True)
    stuffing_job_order = db.Column(db.String(20), nullable=True)
    cargo_weight_in_crn = db.Column(db.Float(), nullable=True)
    # hsn_code = db.Column(db.String(20), nullable=True)
    gw_port_code = db.Column(db.String(20), nullable=True)
    stuffing_job = db.relationship("MasterCargoDetails", back_populates="stuffing_details", lazy='joined')

    __tablename__ = 'ccls_stuffing_cargo_details'


class DeStuffingCargoDetails(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    container_number = db.Column(db.String(11))
    destuffing_job_order = db.Column(db.String(20), nullable=True)
    destuffing_plan_date = db.Column(db.BigInteger(), nullable=True)
    handling_code = db.Column(db.String(20), nullable=True)
    hld_rls_flag = db.Column(db.String(1), nullable=True)
    forwarder = db.Column(db.String(100), nullable=True)
    destuffing_job = db.relationship("MasterCargoDetails", back_populates="destuffing_details", lazy='joined')

    __tablename__ = 'ccls_destuffing_cargo_details'

class DeliveryCargoDetails(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    gpm_number = db.Column(db.String(20), nullable=True)
    gpm_valid_date = db.Column(db.BigInteger(), nullable=True)
    gpm_created_date = db.Column(db.BigInteger(), nullable=True)
    gp_stat = db.Column(db.String(1), nullable=True)
    cha_code = db.Column(db.String(20), nullable=True)
    delivery_job = db.relationship("MasterCargoDetails", back_populates="delivery_details", lazy='joined')

    __tablename__ = 'ccls_delivery_cargo_details'


class CCLSCargoBillDetails(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    commodity_id = db.Column(db.Integer, db.ForeignKey('tm_ccommodity.id'))
    commodity = db.relationship("Commodity")
    shipping_bill_number = db.Column(db.String(20), nullable=True)
    bill_of_entry = db.Column(db.String(20), nullable=True)
    bill_of_lading = db.Column(db.String(20), nullable=True)
    bill_date = db.Column(db.BigInteger(), nullable=True)
    bol_date = db.Column(db.BigInteger(), nullable=True)
    importer_code = db.Column(db.String(30), nullable=True)
    importer_name = db.Column(db.String(100), nullable=True)
    exporter_name = db.Column(db.String(100), nullable=True)
    package_code = db.Column(db.String(20), nullable=True)
    no_of_packages_declared = db.Column(db.Integer(),default=0)
    package_weight = db.Column(db.Float(), nullable=True)
    cha_code = db.Column(db.String(20), nullable=True)
    cha_name = db.Column(db.String(100), nullable=True)
    hsn_code = db.Column(db.String(20), nullable=True)
    cargo_type = db.Column(db.String(20), nullable=True)
    job_order_id = db.Column(db.BigInteger, db.ForeignKey('ccls_master_cargo_details.id'))
    master_job_order_bill_details = db.relationship("MasterCargoDetails", back_populates="bill_details", lazy='joined')
    ctms_cargo_details = db.relationship("CTMSBillDetails", back_populates="ccls_bill", lazy='joined')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    
    __tablename__ = 'ccls_cargo_bill_details'