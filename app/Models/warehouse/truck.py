from app import postgres_db as db
from app.Models.utils import IntegerDateTime
from datetime import datetime

class TruckDetails(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    truck_number = db.Column(db.String(10), nullable=False)
    truck_arrival_date = db.Column(db.BigInteger())
    job_order_id = db.Column(db.Integer, db.ForeignKey('ccls_job_details.id'))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    
    __tablename__ = 'truck_details'
