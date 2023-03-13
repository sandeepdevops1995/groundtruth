from app import postgres_db as db
from datetime import datetime

class WarehouseCommodity(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    COMM_CD = db.Column(db.Integer(), nullable=False)
    COMM_DESC = db.Column(db.String(30), nullable=True)
    SPL_FLG = db.Column(db.String(1), nullable=True)
    COMM_WT = db.Column(db.Integer(), nullable=True)
    #db.Column(db.Integer(10,2), nullable=True)
    CONCOR_HAZ_FLG = db.Column(db.String(1), nullable=True)
    IMP_CONCOR_LABOUR_FLG = db.Column(db.String(1), nullable=True)
    EXP_CONCOR_LABOUR_FLG = db.Column(db.String(1), nullable=True)
    IMP_HNDG_COMM_CAT = db.Column(db.String(2), nullable=True)
    EXP_HNDG_COMM_CAT = db.Column(db.String(2), nullable=True)
    IMP_WHRF_COMM_CAT = db.Column(db.Integer(), nullable=True)
    EXP_WHRF_COMM_CAT = db.Column(db.Integer(), nullable=True)
    DT_WEF = db.Column(db.DateTime())
    USER_ID = db.Column(db.String(100), nullable=True)
    TRNS_DT_TM = db.Column(db.DateTime())
    SRVC_EXMP_CAT_FLG = db.Column(db.String(1), nullable=True)
    SRVC_EXMP_FLG = db.Column(db.String(1), nullable=True)
    ACTIVE_FLG = db.Column(db.String(1), nullable=True)
    RAIL_GST_CODE = db.Column(db.String(10), nullable=True)
    RAIL_GST_APPLICABLE = db.Column(db.String(1), nullable=True)
    # commodity_code = db.Column(db.Integer())
    # commodity_description = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    
    __tablename__ = 'wh_commodity'
