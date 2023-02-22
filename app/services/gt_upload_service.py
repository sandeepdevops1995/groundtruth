from app.models import CCLSRake, Diagnostics
from app import postgres_db as db
from sqlalchemy.exc import SQLAlchemyError
from flask import Response, abort
import json

def commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e :
        print(str(e))
        db.session.rollback()
        db.session.remove()
        raise abort(Response(json.dumps({"message":str(e.orig)}), status=400, mimetype='application/json')) 


def upload_ccls_rake_date(rake_data):
    for wagon in rake_data:
        record = CCLSRake(**wagon)
        db.session.add(record)
    commit()
    return True


def save_in_diagnostics(url,request,response):
    diag = Diagnostics(url=url,request=request,response=response)
    db.session.add(diag)
    commit()