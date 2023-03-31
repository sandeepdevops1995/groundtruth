from app import postgres_db as db

class Gwport(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    gw_port_cd = db.Column(db.String(4))
    gw_port_nam = db.Column(db.String(30))
    pay_facility = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    port_type = db.Column(db.String(1))
    
    __tablename__ = 'tm_cgwport'
        
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
    
    __tablename__ = 'tm_ceqptmst'
    
class EqptDtls(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    eqpt_id = db.Column(db.String(4))
    eqpt_desc = db.Column(db.String(30))
    eqpt_type = db.Column(db.String(1))
    eqpt_stat = db.Column(db.String(1))
    user_id = db.Column(db.String(100))
    wh_flg = db.Column(db.String(1))
    
    __tablename__ = 'tm_ceqptdtls'