from app import postgres_db as db
from datetime import datetime
import json


def db_format(data):
    for value in data:
        if isinstance(data[value],dict):
            data[value] = json.dumps(data[value])
        elif isinstance(data[value],list):
            data[value] = json.dumps(data[value])
    return data
            
class db_functions():
    def __init__(self,data):
        self.data = data
        if isinstance(data,list):
            self.many = True
        else:
            self.many = False
        
    def as_dict(self):
        def dict_data(table):
            return {c.name: getattr(table, c.name) for c in table.__table__.columns}
            
        if self.many:
            final_data = []
            for table in self.data:
                final_data.append(dict_data(table))
            return final_data
        else:
           return dict_data(self.data) 
    
    def as_json(self):
        def json_data(table):
            data = {}
            for c in table.__table__.columns:
                value = getattr(table, c.name)
                if isinstance(value, datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(value, str):
                    try:
                        value = json.loads(value)
                    except:
                        pass
                data[c.name] = value
            return data
    
        if self.many:
            
            final_data = []
            for table in self.data:
                final_data.append(json_data(table))
            return json.dumps(final_data)
        else:
            return json.dumps(json_data(self.data)) 
        
            
class Permit(db.Model):
    # currently using fields
    permit_no = db.Column(db.String(50),primary_key=True)
    permit_date = db.Column(db.DateTime())
    permit_expiry_date = db.Column(db.DateTime())
    container_no = db.Column(db.String(50))
    container_size = db.Column(db.String(50)) 
    container_type = db.Column(db.String(50))
    container_status = db.Column(db.String(50))         #permit_details
    container_life_no = db.Column(db.DateTime())        #permit details
    hazard_status = db.Column(db.Boolean())
    damage_status = db.Column(db.Boolean())
    sline_code = db.Column(db.String(50))               #permit_details
    sline_no = db.Column(db.String(50))
    crn_no = db.Column(db.String(50))
    seal_count = db.Column(db.Integer())
    seal_no = db.Column(db.String(50))
    seal_type = db.Column(db.String(50))
    vehicle_no =  db.Column(db.String(50))
    gate_in_time = db.Column(db.DateTime())
    gate_out_time = db.Column(db.DateTime())
    user_id = db.Column(db.String(50))
    gate_no = db.Column(db.String(3))
    stk_loc = db.Column(db.String(20))
    dmg_code = db.Column(db.String(20))
    dt_seal = db.Column(db.DateTime())
    
    #Fields may require in future
    permit_type = db.Column(db.String(50))
    container_type = db.Column(db.String(50))
    iso_code = db.Column(db.String(50))
    liner_seal = db.Column(db.String(50))
    custom_seal = db.Column(db.String(50), nullable=True)
    reefer = db.Column(db.String(50), nullable=True)
    is_empty_or_laden = db.Column(db.String(10))
    cargo_type = db.Column(db.String(50))
    POD = db.Column(db.String(50))
    permit_details = db.Column(db.Text)
    bill_info = db.Column(db.Text)
    truck = db.Column(db.Text)
    hazard = db.Column(db.Text)
    un_number = db.Column(db.Text)
    

class CCLSRake(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    rake_id = db.Column(db.BigInteger())
    train_number = db.Column(db.String(10))
    train_origin_station = db.Column(db.String(25))
    train_destination_station = db.Column(db.String(25))
    rake_type = db.Column(db.String(5))
    rake_number = db.Column(db.String(25))
    wagon_type =  db.Column(db.String(3))
    wagon_number = db.Column(db.BigInteger())
    wagon_sequence_number = db.Column(db.Integer())
    wagon_ldd_mt = db.Column(db.String(1), nullable=True)
    wagon_owner = db.Column(db.String(25))
    container_number = db.Column(db.String(11))
    container_life_number = db.Column(db.DateTime()) 
    container_size = db.Column(db.Integer())
    container_type = db.Column(db.String(2))
    container_status = db.Column(db.String(2))
    container_gross_weight = db.Column(db.Float())
    container_origin_station = db.Column(db.String(25))
    container_destination_station = db.Column(db.String(25))
    iso_code = db.Column(db.String(25))
    container_stg_flag = db.Column(db.String(1), nullable=True)
    container_iwb_flag = db.Column(db.String(1), nullable=True)
    cargo_type = db.Column(db.String(25))
    fcl_lcl_flg = db.Column(db.String(3), nullable=True)
    station_cd = db.Column(db.String(25))
    gw_port_cd = db.Column(db.String(25))
    error_flg = db.Column(db.String(1), nullable=True)
    remark = db.Column(db.String(100))
    cancel_flg = db.Column(db.String(1), nullable=True)
    trans_date = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    wagon_life_number = db.Column(db.DateTime())
    smtp_no = db.Column(db.String(25))
    smtp_date = db.Column(db.DateTime())
    port_name = db.Column(db.String(25))
    train_dept = db.Column(db.DateTime())
    seal_number = db.Column(db.String(10))
    hazardious_status = db.Column(db.String(2))
    sline_code = db.Column(db.String(6))
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
    date_actual_departure =  db.Column(db.DateTime())
    ldd_mt_flg = db.Column(db.String(2))
    imp_exp_flg = db.Column(db.String(1), nullable=True)
    adv_boe_flg = db.Column(db.String(2), nullable=True)
    error_msg = db.Column(db.String(100))
    status_flg = db.Column(db.String(1), nullable=True)
    track_number = db.Column(db.String(10), nullable=True)
    
    __tablename__ = 'xxccls_rake_trnsdtls_tbl'

    
    
class ISOcode(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    ctr_size = db.Column(db.Integer())
    ctr_type = db.Column(db.String(2))
    ctr_iso_cd = db.Column(db.String(4))
    
    __tablename__ = 'TM_CCTRISOCD'
    
    
class CtrSize(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    ctr_size = db.Column(db.Integer())
    ctr_tare_wt = db.Column(db.Float(precision=2))
    ldd_ctr_wt = db.Column(db.Float(precision=2))
    user_id = db.Column(db.String(100))
    teu = db.Column(db.Float(precision=1))
    
    __tablename__ = 'TM_CCTRSIZE'
    

class CtrType(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    ctr_type =  db.Column(db.String(2))
    ctr_type_desc = db.Column(db.String(25))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_CCTRTYPE'

class Ctry(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    ctry_cd = db.Column(db.String(5))
    ctry_nam = db.Column(db.String(30))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_CCTRY'
    
class CtryCustom(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    ctry_cd = db.Column(db.String(5))
    ctry_nam = db.Column(db.String(30))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_CCTRY_CUSTOM'
    
class ChaCustom(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    cha_cd = db.Column(db.String(10))
    cha_nam = db.Column(db.String(100))
    adr1 = db.Column(db.String(100))
    adr2 = db.Column(db.String(100))
    city = db.Column(db.String(25))
    
    __tablename__ = 'TM_CCHA_CUSTOM'
    
class Cha(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    cha_cd = db.Column(db.String(6))
    cha_nam = db.Column(db.String(100))
    adr1 = db.Column(db.String(100))
    adr2 = db.Column(db.String(35))
    city = db.Column(db.String(25))
    state = db.Column(db.String(25))
    pin = db.Column(db.String(6))
    cha_ph = db.Column(db.String(15))
    cha_fax = db.Column(db.String(15))
    cha_tlx = db.Column(db.String(15))
    chq_facility = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    tds_flg = db.Column(db.String(1))
    tan_no = db.Column(db.String(12))
    trns_dt_tm = db.Column(db.DateTime())
    pan_no = db.Column(db.String(10))
    email_id = db.Column(db.String(50))
    customer_id = db.Column(db.String(20))
    cha_license_no = db.Column(db.String(50))
    cha_license_vld_date = db.Column(db.DateTime())
    country = db.Column(db.String(50))
    gstin_no = db.Column(db.String(15))
    active_flag = db.Column(db.String(1))
    hold_rels_flag = db.Column(db.String(1))
    create_dt_tm = db.Column(db.DateTime())
    msme_flg = db.Column(db.String(1))
    oth1 = db.Column(db.String(50))
    oth2 = db.Column(db.String(50))
    oth3 = db.Column(db.String(50))
    prov_gstin_no = db.Column(db.String(15))
    cin_no = db.Column(db.String(50))
    
    __tablename__ = 'TM_CCHA'
    
class ChaDirectory(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    cha_cd = db.Column(db.String(15))
    cha_cd_regn = db.Column(db.String(6))
    cha_nam = db.Column(db.String(100))
    cha_regn = db.Column(db.DateTime())
    cha_expry = db.Column(db.DateTime())
    
    __tablename__ = 'TM_CCHA_DIRECTORY'
    
    
class ImprExprCustom(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    party_iec_cd = db.Column(db.String(12))
    party_nam = db.Column(db.String(100))
    party_adr = db.Column(db.String(40))
    
    __tablename__ = 'TM_CIMPREXPR_CUSTOM'
    
class PortCustom(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    port_cd = db.Column(db.String(6))
    port_nam = db.Column(db.String(50))
    ctry_cd = db.Column(db.String(5))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_CPORT_CUSTOM'
    
class CustEmail(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    sline_cd = db.Column(db.String(5))
    sline_nam = db.Column(db.String(100))
    email_id = db.Column(db.String(50))
    send_flg = db.Column(db.String(1))
    sent_flg = db.Column(db.String(1))
    sent_dt_tm = db.Column(db.DateTime())
    
    __tablename__ = 'TM_CUST_EMAIL'
    
class CustDtls(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    customer_id = db.Column(db.String(20))
    party_code = db.Column(db.String(20))
    party_type = db.Column(db.String(1))
    person_name = db.Column(db.String(50))
    mobile_no = db.Column(db.Integer())
    email_id = db.Column(db.String(50))
    phone_no = db.Column(db.String(20))
    department = db.Column(db.String(50))
    designation = db.Column(db.String(50))
    active_flag = db.Column(db.String(20))
    create_dt_tm = db.Column(db.DateTime())
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_CUSTOMER_DTLS'


class Acty(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    acty_cd = db.Column(db.String(3))
    acty_desc = db.Column(db.String(25))
    acty_type = db.Column(db.String(1))
    frm_loc = db.Column(db.String(3))
    to_loc = db.Column(db.String(3))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_CACTY'
    
class Agency(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    agency_cd = db.Column(db.String(5))
    agency_nam = db.Column(db.String(25))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_CAGENCY'
    
class BlWhrf(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    whrf_comm_cat = db.Column(db.Integer())
    crg_wt = db.Column(db.Float(precision=2))
    dt_wef = db.Column(db.DateTime())
    holi_flg = db.Column(db.String(5))
    day_frm = db.Column(db.Integer())
    day_to = db.Column(db.Integer())
    rate_pr_day = db.Column(db.Float(precision=2))
    imp_exp_flg = db.Column(db.String(5))
    fcl_lcl_flg = db.Column(db.String(5))
    crg_type = db.Column(db.String(5))
    wt_flg = db.Column(db.String(5))
    min_chrg = db.Column(db.Float(precision=2))
    cur_flg = db.Column(db.String(5))
    user_id = db.Column(db.String(5))
    max_chrg_20 = db.Column(db.Integer())
    max_chrg_40 = db.Column(db.Integer())
    
    __tablename__ = 'TM_CBLWHRF'
    
class Cfs(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    cfs_cd = db.Column(db.String(3))
    cfs_nam = db.Column(db.String(30))
    user_id = db.Column(db.String(100))
    trans_dt_tm = db.Column(db.DateTime())
    
    __tablename__ = 'TM_CCFS'
    
class CncrWgnDtls(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    wgn_no = db.Column(db.String(13))
    wgn_type = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_CCNCRWGNDTLS'
    
class Cnsldtor(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    cnsldtor_cd = db.Column(db.String(5))
    cnsldtor_nam = db.Column(db.String(35))
    cnsldtor_adr = db.Column(db.String(75))
    cnsldtor_ph = db.Column(db.String(15))
    cnsldtor_fax = db.Column(db.String(15))
    cnsldtor_tlx = db.Column(db.String(15))
    chq_facility = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    map_code = db.Column(db.String(10))
    trns_dt_tm = db.Column(db.DateTime())
    actv_flg = db.Column(db.String(1))
    
    __tablename__ = 'TM_CCNSLDTOR'
    
class Commodity(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    comm_cd = db.Column(db.Integer())
    comm_desc = db.Column(db.String(1))
    spl_flg = db.Column(db.String(1))
    comm_wt = db.Column(db.Float(precision=2))
    concor_haz_flg = db.Column(db.String(1))
    imp_concor_labour_flg = db.Column(db.String(1))
    exp_concor_labour_flg = db.Column(db.String(1))
    imp_hndg_comm_cat = db.Column(db.String(1))
    exp_hndg_comm_cat = db.Column(db.String(1))
    imp_whrf_comm_cat = db.Column(db.String(1))
    exp_whrf_comm_cat = db.Column(db.String(1))
    dt_wef = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    trns_dt_tm = db.Column(db.DateTime())
    srvc_exmp_cat_flg = db.Column(db.String(1))
    srvc_exmp_flg = db.Column(db.String(1))
    active_flg = db.Column(db.String(1))
    rail_gst_code = db.Column(db.String(10))
    rail_gst_applicable = db.Column(db.String(1))
    
    __tablename__ = 'TM_CCOMMODITY'
    
class CtrTarewt(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    ctr_size = db.Column(db.Integer())
    ctr_type = db.Column(db.String(2))
    ctr_tare_wt = db.Column(db.Float(precision=2))
    user_id = db.Column(db.String(100))
    trans_dt_tm = db.Column(db.DateTime())
    ldd_ctr_wt = db.Column(db.Float(precision=2))
    
    __tablename__ = 'TM_CCTR_TAREWT'
    
class CtrDtls(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    ctr_no = db.Column(db.String(12))
    ctr_life_no = db.Column(db.DateTime())
    ctr_iso_cd = db.Column(db.String(4))
    sline_cd = db.Column(db.String(5))
    ctr_size = db.Column(db.Integer())
    ctr_type = db.Column(db.String(2))
    ctr_stat = db.Column(db.String(2))
    hold_rels_flg = db.Column(db.String(1))
    ldd_mt_flg = db.Column(db.String(1))
    imp_exp_flg = db.Column(db.String(1))
    fcl_lcl_flg = db.Column(db.String(3))
    seal_stat = db.Column(db.String(1))
    seal_no = db.Column(db.String(1))
    dmg_flg = db.Column(db.String(1))
    ctr_stg_flg = db.Column(db.String(1))
    ctr_nom_flg = db.Column(db.String(1))
    ctr_loc_flg = db.Column(db.String(1))
    acty_cd = db.Column(db.String(3))
    dt_acty = db.Column(db.DateTime())
    icd_loc_cd = db.Column(db.String(3))
    stk_loc = db.Column(db.String(9))
    dt_arr = db.Column(db.DateTime())
    dt_dep = db.Column(db.DateTime())
    mode_arr = db.Column(db.String(1))
    mode_dep = db.Column(db.String(1))
    gw_port_cd = db.Column(db.String(4))
    dt_start = db.Column(db.DateTime())
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    ctr_ht = db.Column(db.String(2))
    ctr_ht_cat = db.Column(db.String(1))
    dmg_code = db.Column(db.String(5))
    frm_loc = db.Column(db.String(9))
    fac_dep_by_road = db.Column(db.String(1))
    
    __tablename__ = 'TM_CCTRDTLS'
    
class EqptDtls(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    eqpt_id = db.Column(db.String(4))
    eqpt_desc = db.Column(db.String(30))
    eqpt_type = db.Column(db.String(1))
    eqpt_stat = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    wh_flg = db.Column(db.String(1))
    
    __tablename__ = 'TM_CEQPTDTLS'
    
class EqptMst(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    eqpt_id = db.Column(db.String(10))
    acty_cd = db.Column(db.String(30))
    party_cd = db.Column(db.String(10))
    commisioned_on = db.Column(db.DateTime())
    active_flg = db.Column(db.String(1))
    deccommisioned_on = db.Column(db.DateTime())
    ins_dt = db.Column(db.DateTime())
    lst_upd_dt = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_CEQPTMST'

    
class ErrorMessages(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    error_code = db.Column(db.String(6))
    error_description = db.Column(db.String(150))
    
    __tablename__ = 'TM_CERRORMESSAGES'

class Gwport(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    gw_port_cd = db.Column(db.String(4))
    gw_port_nam = db.Column(db.String(30))
    pay_facility = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    port_type = db.Column(db.String(1))
    
    __tablename__ = 'TM_CGWPORT'
    
class GwportState(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    gw_port_cd = db.Column(db.String(4))
    gw_port_nam = db.Column(db.String(30))
    pay_facility = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    port_type = db.Column(db.String(100))
    stat_cd = db.Column(db.String(2))
    gstin_stat_cd = db.Column(db.String(2))
    sline_cd  = db.Column(db.String(5))
    
    __tablename__ = 'TM_CGWPORT_STATE'
    
class ChaEmail(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    cha_cd = db.Column(db.String(6))
    cha_nam = db.Column(db.String(100))
    email_id1 = db.Column(db.String(75))
    email_id2 = db.Column(db.String(75))
    user_id = db.Column(db.String(100))
    email_id5 = db.Column(db.String(75))
    
    __tablename__ = 'TM_CHAEMAIL'
    
class HldTrack(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    hld_track_no = db.Column(db.String(75))
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(75))
    hld_track_desc = db.Column(db.String(75))
    
    __tablename__ = 'TM_CHLDTRACK'
    

class Hndg(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    hndg_cd = db.Column(db.Integer())
    imp_exp_flg = db.Column(db.String(1))
    hndg_desc = db.Column(db.String(25))
    out_loc_cd = db.Column(db.String(3))
    user_id = db.Column(db.String(100))
    ldd_mt_flg = db.Column(db.String(1))
    
    __tablename__ = 'TM_CHNDG'
    
class HndgActy(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    hndg_cd = db.Column(db.Integer())
    prev_acty_cd = db.Column(db.String(3))
    curr_acty_cd = db.Column(db.String(3))
    prev_acty_comp_flg = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_CHNDGACTY'
    
class IcdLoc(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    icd_loc_cd = db.Column(db.String(3))
    icd_loc_desc = db.Column(db.String(25))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_CICDLOC'

class Pkg(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    pkg_cd = db.Column(db.String(3))
    pkg_desc = db.Column(db.String(25))
    imp_hndg_pkg_cat = db.Column(db.String(2))
    exp_hndg_pkg_cat = db.Column(db.String(2))
    dt_wef = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    trns_dt_tm = db.Column(db.DateTime())
    
    __tablename__ = 'TM_CPKG'
    

class UsrFiling(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    usr_id = db.Column(db.String(100))
    password = db.Column(db.String(40))
    usr_nm = db.Column(db.String(50))
    module_cd = db.Column(db.String(20))
    party_cd = db.Column(db.String(10))
    party_type = db.Column(db.String(1))
    file_name = db.Column(db.String(20))
    usr_id_etms = db.Column(db.String(100))
    trns_dt_tm = db.Column(db.DateTime())
    actve_dectve_flg = db.Column(db.String(1))
    admn_typ = db.Column(db.String(1))
    email_id = db.Column(db.String(75))
    mail_sent_flg = db.Column(db.String(1))
    last_trns_dt_tm = db.Column(db.DateTime())
    mobile_no = db.Column(db.String(15))
    dt_valid_from = db.Column(db.DateTime())
    dt_valid_upto = db.Column(db.DateTime())
    login_auth = db.Column(db.String(30))
    alloc_pass = db.Column(db.String(30))
    pki_serial = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_USRFILING'
    
class WgnMst(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    rake_no = db.Column(db.String(50))
    wgn_no = db.Column(db.String(50))
    wgn_typ = db.Column(db.String(5))
    commisioned_on = db.Column(db.DateTime())
    ccls_wgn = db.Column(db.String(25))
    usr_id = db.Column(db.String(100))
    ins_dt = db.Column(db.DateTime())
    lst_upd_dt = db.Column(db.DateTime())
    trns_trml_id = db.Column(db.String(5))
    active_flg = db.Column(db.String(1))
    old_wgn = db.Column(db.String(50))
    conv_dt = db.Column(db.DateTime())
    
    __tablename__ = 'TM_WGNMST'
    
class WgnMstEtms(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    rake_no = db.Column(db.String(50))
    wgn_no = db.Column(db.String(50))
    wgn_typ = db.Column(db.String(5))
    commisioned_on = db.Column(db.String(50))
    etms_wgn = db.Column(db.String(25))
    usr_id = db.Column(db.String(15))
    ins_dt = db.Column(db.DateTime())
    lst_upd_dt = db.Column(db.DateTime())
    trns_trml_id = db.Column(db.String(5))
    wgn_tare_wt = db.Column(db.Float(precision=2))
    wgn_capacity = db.Column(db.Float(precision=2))
    rmrks = db.Column(db.String(50))
    comm_dt = db.Column(db.DateTime())
    actve_inactve = db.Column(db.String(1))
    mapped_wgn = db.Column(db.String(15))
    dt_conversion = db.Column(db.DateTime())
    
    __tablename__ = 'TMC_WGNMST_ETMS'
        
class BlActy(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    acty_cd = db.Column(db.String(100))
    acty_desc = db.Column(db.String(100))
    dt_wef = db.Column(db.DateTime())
    day_frm = db.Column(db.Integer())
    day_to = db.Column(db.Integer())
    chrg = db.Column(db.Float(precision=2))
    chrg_type = db.Column(db.Integer())
    cur_flg = db.Column(db.String(100))
    acty_flg = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
    min_chrgs = db.Column(db.Float(precision=2))
    trns_dt_tm = db.Column(db.DateTime())
    
    __tablename__ = 'TH_TM_CBLACTY'
    
    
class WgnType(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    wgn_type = db.Column(db.String(1))
    wgn_desc = db.Column(db.String(10))
    cncl_flg = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_CWGNTYPE'
    

class SlineConv(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    sline_cus = db.Column(db.String(10))
    sline_cncr = db.Column(db.String(5))
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_FSLINECONV'
    
    
class PodConv(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    pod_cus = db.Column(db.String(6))
    pod_cncr = db.Column(db.String(3))
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_FPODCONV'
    
    
class Port(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    port_cd = db.Column(db.String(3))
    port_nam = db.Column(db.String(30))
    ctry_cd = db.Column(db.String(5))
    ctry_nam = db.Column(db.String(30))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_CPORT'

class PortConv(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    orgn_stn_cd = db.Column(db.String(4))
    orgn_stn_name = db.Column(db.String(4))
    dest_stn_cd = db.Column(db.String(4))
    dest_stn_name = db.Column(db.String(4))
    conv_dest_cd = db.Column(db.String(5))
    user_id = db.Column(db.String(100))
    trns_dt_tm = db.Column(db.DateTime())
    
    __tablename__ = 'TM_CPORTCONV'
    

class OutLoc(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    out_loc_cd = db.Column(db.String(3))
    out_loc_desc = db.Column(db.String(25))
    nom_flg = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_COUTLOC'
    
class OutPort(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    h_port = db.Column(db.String(4))
    c_port = db.Column(db.String(4))
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_COUTPORT'
    
class UserDtls(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    user_cd = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
    trns_dt_tm = db.Column(db.DateTime())
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    proj_code = db.Column(db.String(15))
    proj_join_dt = db.Column(db.DateTime())
    proj_end_dt = db.Column(db.DateTime())
    role = db.Column(db.String(50))
    designation = db.Column(db.String(50))
    
    __tablename__ = 'TM_USERDTLS'
    
class Station(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    station_cd = db.Column(db.String(5))
    station_name = db.Column(db.String(50))
    
    __tablename__ = 'TM_STATION'
    
    
class ModuleCd(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    module_cd = db.Column(db.String(5))
    module_desc = db.Column(db.String(50))
    user_id = db.Column(db.String(100))
    trns_dt_tm = db.Column(db.DateTime())
    proj_code = db.Column(db.String(15))
        
    __tablename__ = 'TM_MODULE_CD'
    

class GwPortConv(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    gw_port_cus = db.Column(db.String(10))
    gw_port_cncr = db.Column(db.String(4))
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_FGWPORTCONV'
    

class CfsConv(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    cfs_cur = db.Column(db.String(4))
    cfs_cncr = db.Column(db.String(4))
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'TM_FCFSCONV'
    

class Comm(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    comm_cd = db.Column(db.Integer())
    comm_desc = db.Column(db.String(4))
    spl_flg = db.Column(db.String(4))
    comm_wt = db.Column(db.Float(precision=2))
    concor_haz_flg = db.Column(db.String(4))
    imp_concor_labour_flg = db.Column(db.String(4))
    exp_concor_labour_flg = db.Column(db.String(4))
    imp_hndg_comm_cat = db.Column(db.String(4))
    exp_hndg_comm_cat = db.Column(db.String(4))
    imp_whrf_comm_cat = db.Column(db.Integer())
    exp_whrf_comm_cat = db.Column(db.Integer())
    dt_wef = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    trns_dt_tm = db.Column(db.DateTime())
    
    __tablename__ = 'TM_COMM'
    
class Track(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    track_no = db.Column(db.String(75), unique= True)
    train_no = db.Column(db.String(75), unique= True, nullable=True)
    trans_date = db.Column(db.DateTime())
    user_id = db.Column(db.String(75))
    created_at = db.Column(db.DateTime(), default = datetime.now)
    updated_at = db.Column(db.DateTime(), default = datetime.now, onupdate=datetime.now)
    
    __tablename__ = 'Track'
    
class KyclContainerLocation(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    container_no = db.Column(db.String(11))
    to_loc = db.Column(db.String(15))
    che_id = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(), default = datetime.now)
    
class Diagnostics(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    url = db.Column(db.String(200))
    request = db.Column(db.JSON)
    response =  db.Column(db.JSON)
    
    __tablename__ = 'Diagnostics'