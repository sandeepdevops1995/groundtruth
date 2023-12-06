from app import postgres_db as db
from datetime import datetime


class DTMSContainerLocation(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    terminal_code = db.Column(db.String(25), nullable=True)
    container_number = db.Column(db.String(25), nullable=True)
    container_size = db.Column(db.Integer())
    container_type = db.Column(db.String(25), nullable=True)
    loaded_empty_flag = db.Column(db.String(25), nullable=True)
    container_special_flag = db.Column(db.String(25), nullable=True)
    stack_location = db.Column(db.String(25), nullable=True)
    prev_stack_location = db.Column(db.String(25), nullable=True)
    ISO_DSO_flag = db.Column(db.String(25), nullable=True)
    crntstts = db.Column(db.String(25), nullable=True)
    crntstts_time = db.Column(db.DateTime())
    prvsstts = db.Column(db.String(25), nullable=True)
    csf_code = db.Column(db.String(25), nullable=True)
    cbtgstrg_flag = db.Column(db.String(25), nullable=True)
    container_weight = db.Column(db.Float())
    container_tare_weight = db.Column(db.Float())
    seal_number = db.Column(db.String(25), nullable=True)
    handling_over_date = db.Column(db.DateTime())
    sline_code = db.Column(db.String(25), nullable=True)
    vldt_flag = db.Column(db.String(25), nullable=True)
    container_owner_flag = db.Column(db.String(25), nullable=True)