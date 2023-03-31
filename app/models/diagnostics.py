from app import postgres_db as db
from datetime import datetime

class Diagnostics(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    url = db.Column(db.String(200))
    request = db.Column(db.JSON)
    response =  db.Column(db.JSON)
    created_at = db.Column(db.DateTime(), default = datetime.now)
    
    __tablename__ = 'Diagnostics'