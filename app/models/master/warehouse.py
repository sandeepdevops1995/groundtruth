from app import postgres_db as db

class Commodity(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    comm_cd = db.Column(db.Integer())
    comm_desc = db.Column(db.String(100))
    spl_flg = db.Column(db.String(1), nullable=True)
    comm_wt = db.Column(db.Float(precision=2), nullable=True)
    concor_haz_flg = db.Column(db.String(1), nullable=True)
    imp_concor_labour_flg = db.Column(db.String(1), nullable=True)
    exp_concor_labour_flg = db.Column(db.String(1), nullable=True)
    imp_hndg_comm_cat = db.Column(db.String(1), nullable=True)
    exp_hndg_comm_cat = db.Column(db.String(1), nullable=True)
    imp_whrf_comm_cat = db.Column(db.String(1), nullable=True)
    exp_whrf_comm_cat = db.Column(db.String(1), nullable=True)
    dt_wef = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(db.String(100), nullable=True)
    trns_dt_tm = db.Column(db.DateTime(), nullable=True)
    srvc_exmp_cat_flg = db.Column(db.String(1), nullable=True)
    srvc_exmp_flg = db.Column(db.String(1), nullable=True)
    active_flg = db.Column(db.String(1), nullable=True)
    rail_gst_code = db.Column(db.String(10), nullable=True)
    rail_gst_applicable = db.Column(db.String(1), nullable=True)
    
    __tablename__ = 'tm_ccommodity'