from app import postgres_db as db
from datetime import datetime

class PendancyContainer(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    pendency_type = db.Column(db.Integer())
    container_number = db.Column(db.String(11))
    container_life_number = db.Column(db.DateTime())
    container_stat = db.Column(db.String(2))
    container_size = db.Column(db.Integer())
    container_type = db.Column(db.String(5))
    container_weight = db.Column(db.Float())
    container_acty_code = db.Column(db.String(10))
    cargo_flag = db.Column(db.String(10))
    icd_loc_code = db.Column(db.String(10))
    stuffed_at = db.Column(db.String(10))
    stack_loc = db.Column(db.String(20))
    sline_code = db.Column(db.String(10))
    gateway_port_code = db.Column(db.String(10))
    arrival_date = db.Column(db.DateTime())
    seal_number = db.Column(db.String(20))
    seal_date = db.Column(db.DateTime())
    sbill_number = db.Column(db.String(10))
    sbill_date = db.Column(db.DateTime())
    pid_number = db.Column(db.String(10))
    odc_flag = db.Column(db.String(10))
    hold_flg = db.Column(db.String(10))
    hold_rels_flg = db.Column(db.String(30))
    hold_rels_flg_next = db.Column(db.String(10))
    q_no = db.Column(db.String(10))
    container_category = db.Column(db.String(20))

    # for Domestic containers
    station_from = db.Column(db.String(10))
    station_to  = db.Column(db.String(10))
    ldd_mt_flg = db.Column(db.String(10))
    commodity_code = db.Column(db.String(20))
    
class RakePlan(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    rake_id = db.Column(db.BigInteger())
    train_number = db.Column(db.String(10))
    dt_desp = db.Column(db.DateTime())
    rake_number = db.Column(db.String(25))
    hld_track_number = db.Column(db.String(10))
    dt_wtr = db.Column(db.DateTime())
    equipment_id = db.Column(db.String(25))
    gateway_port_cd= db.Column(db.String(25))
    container_number = db.Column(db.String(11))
    container_life_number = db.Column(db.DateTime())
    wagon_number = db.Column(db.String(25))
    wagon_life_number = db.Column(db.DateTime())
    damage_flg =  db.Column(db.String(1))
    sline_code = db.Column(db.String(6))
    container_size = db.Column(db.Integer())
    container_type = db.Column(db.String(2))
    container_status = db.Column(db.String(2))
    iso_code = db.Column(db.String(25))
    seal_number = db.Column(db.String(20))
    ldd_mt_flg = db.Column(db.String(2))
    damage_code = db.Column(db.String(25))
    container_weight = db.Column(db.Float())
    first_pod = db.Column(db.String(25))
    origin_station = db.Column(db.String(25))
    dest_station = db.Column(db.String(25))
    attribute_1 = db.Column(db.String(25))
    attribute_2 = db.Column(db.String(25))
    attribute_3 = db.Column(db.String(25))
    attribute_4 = db.Column(db.String(25))
    attribute_5 = db.Column(db.String(25))
    attribute_6 = db.Column(db.DateTime())
    attribute_7 = db.Column(db.DateTime())
    created_date = db.Column(db.DateTime(), default = datetime.now)
    created_by = db.Column(db.String(25))
    updated_date = db.Column(db.DateTime(), default = datetime.now, onupdate=datetime.now)
    updated_by = db.Column(db.String(25))
    error_msg = db.Column(db.String(100))
    status_flg = db.Column(db.String(1), nullable=True)
    read_flg  = db.Column(db.String(1), nullable=True)