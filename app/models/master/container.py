from app import postgres_db as db

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
    
    __tablename__ = 'tm_cctrdtls'


class CtrSize(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    ctr_size = db.Column(db.Integer())
    ctr_tare_wt = db.Column(db.Float(precision=2))
    ldd_ctr_wt = db.Column(db.Float(precision=2))
    user_id = db.Column(db.String(100))
    teu = db.Column(db.Float(precision=1))
    
    __tablename__ = 'tm_cctrsize'
    

class CtrType(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    ctr_type =  db.Column(db.String(2))
    ctr_type_desc = db.Column(db.String(25))
    user_id = db.Column(db.String(100))
    
    __tablename__ = 'tm_cctrtype'
    
class CtrTarewt(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    ctr_size = db.Column(db.Integer())
    ctr_type = db.Column(db.String(2))
    ctr_tare_wt = db.Column(db.Float(precision=2))
    user_id = db.Column(db.String(100))
    trans_dt_tm = db.Column(db.DateTime())
    ldd_ctr_wt = db.Column(db.Float(precision=2))
    
    __tablename__ = 'tm_cctr_tarewt'
    
class ISOcode(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    ctr_size = db.Column(db.Integer())
    ctr_type = db.Column(db.String(2))
    ctr_iso_cd = db.Column(db.String(4))
    
    __tablename__ = 'tm_cctrisocd'