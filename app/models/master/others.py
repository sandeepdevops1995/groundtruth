from app import postgres_db as db

class Ctry(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    ctry_cd = db.Column(db.String(5))
    ctry_nam = db.Column(db.String(30))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_cctry'
    
class CtryCustom(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    ctry_cd = db.Column(db.String(5))
    ctry_nam = db.Column(db.String(30))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_cctry_custom'
    
class ChaCustom(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    cha_cd = db.Column(db.String(10))
    cha_nam = db.Column(db.String(100))
    adr1 = db.Column(db.String(100))
    adr2 = db.Column(db.String(100))
    city = db.Column(db.String(25))
    
    __tablename__ = 'tm_ccha_custom'
    
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
    
    __tablename__ = 'tm_ccha'
    
class ChaDirectory(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    cha_cd = db.Column(db.String(15))
    cha_cd_regn = db.Column(db.String(6))
    cha_nam = db.Column(db.String(100))
    cha_regn = db.Column(db.DateTime())
    cha_expry = db.Column(db.DateTime())
    
    __tablename__ = 'tm_ccha_directory'
    
    
class ImprExprCustom(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    party_iec_cd = db.Column(db.String(12))
    party_nam = db.Column(db.String(100))
    party_adr = db.Column(db.String(40))
    
    __tablename__ = 'tm_cimprexpr_custom'
    
class PortCustom(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    port_cd = db.Column(db.String(6))
    port_nam = db.Column(db.String(50))
    ctry_cd = db.Column(db.String(5))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_cport_custom'
    
class CustEmail(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    sline_cd = db.Column(db.String(5))
    sline_nam = db.Column(db.String(100))
    email_id = db.Column(db.String(50))
    send_flg = db.Column(db.String(1))
    sent_flg = db.Column(db.String(1))
    sent_dt_tm = db.Column(db.DateTime())
    
    __tablename__ = 'tm_cust_email'
    
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
    
    __tablename__ = 'tm_customer_dtls'


class Acty(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    acty_cd = db.Column(db.String(3))
    acty_desc = db.Column(db.String(25))
    acty_type = db.Column(db.String(1))
    frm_loc = db.Column(db.String(3))
    to_loc = db.Column(db.String(3))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_cacty'
    
class Agency(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    agency_cd = db.Column(db.String(5))
    agency_nam = db.Column(db.String(25))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_cagency'
    
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
    
    __tablename__ = 'tm_cblwhrf'
    
class Cfs(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    cfs_cd = db.Column(db.String(3))
    cfs_nam = db.Column(db.String(30))
    user_id = db.Column(db.String(100))
    trans_dt_tm = db.Column(db.DateTime())
    
    __tablename__ = 'tm_ccfs'
    
class CncrWgnDtls(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    wgn_no = db.Column(db.String(13))
    wgn_type = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_ccnrwgndtls'
    
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
    
    __tablename__ = 'tm_ccnsldtor'
    
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
    
    __tablename__ = 'tm_ccommodity'
    

    

    


    
class ErrorMessages(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    error_code = db.Column(db.String(6))
    error_description = db.Column(db.String(150))
    
    __tablename__ = 'tm_cerrormessages'


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
    
    __tablename__ = 'tm_cgwport_state'
    
class ChaEmail(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    cha_cd = db.Column(db.String(6))
    cha_nam = db.Column(db.String(100))
    email_id1 = db.Column(db.String(75))
    email_id2 = db.Column(db.String(75))
    user_id = db.Column(db.String(100))
    email_id5 = db.Column(db.String(75))
    
    __tablename__ = 'tm_chaemail'
    

    

class Hndg(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    hndg_cd = db.Column(db.Integer())
    imp_exp_flg = db.Column(db.String(1))
    hndg_desc = db.Column(db.String(25))
    out_loc_cd = db.Column(db.String(3))
    user_id = db.Column(db.String(100))
    ldd_mt_flg = db.Column(db.String(1))
    
    __tablename__ = 'tm_chndg'
    
class HndgActy(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    hndg_cd = db.Column(db.Integer())
    prev_acty_cd = db.Column(db.String(3))
    curr_acty_cd = db.Column(db.String(3))
    prev_acty_comp_flg = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_chndgacty'
    
class IcdLoc(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    icd_loc_cd = db.Column(db.String(3))
    icd_loc_desc = db.Column(db.String(25))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_cicdloc'

class Pkg(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    pkg_cd = db.Column(db.String(3))
    pkg_desc = db.Column(db.String(25))
    imp_hndg_pkg_cat = db.Column(db.String(2))
    exp_hndg_pkg_cat = db.Column(db.String(2))
    dt_wef = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    trns_dt_tm = db.Column(db.DateTime())
    
    __tablename__ = 'tm_cpkg'
    

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
    
    __tablename__ = 'tm_usrfiling'
    

    
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
    
    __tablename__ = 'tmc_wgnmst_etms'
        
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
    
    __tablename__ = 'th_tm_cblacty'
    
    
class WgnType(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    wgn_type = db.Column(db.String(1))
    wgn_desc = db.Column(db.String(10))
    cncl_flg = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_cwgntype'
    

class SlineConv(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    sline_cus = db.Column(db.String(10))
    sline_cncr = db.Column(db.String(5))
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_fslineconv'
    
    
class PodConv(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    pod_cus = db.Column(db.String(6))
    pod_cncr = db.Column(db.String(3))
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_fpodconv'
    
    
class Port(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    port_cd = db.Column(db.String(3))
    port_nam = db.Column(db.String(30))
    ctry_cd = db.Column(db.String(5))
    ctry_nam = db.Column(db.String(30))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_cport'

class PortConv(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    orgn_stn_cd = db.Column(db.String(4))
    orgn_stn_name = db.Column(db.String(4))
    dest_stn_cd = db.Column(db.String(4))
    dest_stn_name = db.Column(db.String(4))
    conv_dest_cd = db.Column(db.String(5))
    user_id = db.Column(db.String(100))
    trns_dt_tm = db.Column(db.DateTime())
    
    __tablename__ = 'tm_cportconv'
    

class OutLoc(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    out_loc_cd = db.Column(db.String(3))
    out_loc_desc = db.Column(db.String(25))
    nom_flg = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_coutloc'
    
class OutPort(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    h_port = db.Column(db.String(4))
    c_port = db.Column(db.String(4))
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_coutport'
    
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
    
    __tablename__ = 'tm_userdtls'
    
class Station(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    station_cd = db.Column(db.String(5))
    station_name = db.Column(db.String(50))
    
    __tablename__ = 'tm_station'
    
    
class ModuleCd(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    module_cd = db.Column(db.String(5))
    module_desc = db.Column(db.String(50))
    user_id = db.Column(db.String(100))
    trns_dt_tm = db.Column(db.DateTime())
    proj_code = db.Column(db.String(15))
        
    __tablename__ = 'tm_module_cd'
    

class GwPortConv(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    gw_port_cus = db.Column(db.String(10))
    gw_port_cncr = db.Column(db.String(4))
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_fgwportconv'
    

class CfsConv(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    cfs_cur = db.Column(db.String(4))
    cfs_cncr = db.Column(db.String(4))
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_fcfsconv'
    

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
    
    __tablename__ = 'tm_comm'