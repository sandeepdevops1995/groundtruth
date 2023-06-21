from app import postgres_db as db
from datetime import datetime

class Container(db.Model):
    id = db.Column(db.String(11), primary_key=True)
    container_number = db.Column(db.String(11), nullable=True)
    container_type = db.Column(db.String(20), nullable=True)
    container_size =  db.Column(db.Integer(), nullable=True)
    container_iso_code = db.Column(db.String(4), nullable=True)
    container_location_code = db.Column(db.String(20), nullable=True)
    container_life = db.Column(db.BigInteger(), nullable=True)
    master_job_container = db.relationship("MasterCargoDetails", back_populates="container_info", lazy='joined')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    
    __tablename__ = 'container'
