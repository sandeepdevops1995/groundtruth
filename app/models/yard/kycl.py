from app import postgres_db as db
from datetime import datetime
import json


class KyclContainerLocation(db.Model):
    id =  db.Column(db.BigInteger(), primary_key=True)
    container_no = db.Column(db.String(11))
    to_loc = db.Column(db.String(15))
    che_id = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(), default = datetime.now)