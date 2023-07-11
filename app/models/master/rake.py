from app import postgres_db as db
from sqlalchemy import JSON

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
    
    __tablename__ = 'tm_wgnmst'

class HldTrack(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    hld_track_no = db.Column(db.String(75))
    trns_dt_tm = db.Column(db.DateTime())
    user_id = db.Column(db.String(75))
    hld_track_desc = db.Column(db.String(75))
    
    __tablename__ = 'tm_chldtrack'

class TrackDetails(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    track_id = db.Column(db.BigInteger())
    track_no =  db.Column(db.String(75))
    track_cordinates = db.Column(JSON)

    __tablename__ = 'tm_track_details'