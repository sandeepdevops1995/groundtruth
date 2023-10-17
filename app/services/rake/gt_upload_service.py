from app.models import CCLSRake, Diagnostics, PendancyContainer, CtrStat
from app.logger import logger
from app import postgres_db as db
from sqlalchemy.exc import SQLAlchemyError
from flask import Response, abort
import json

def commit():
    try:
        db.session.commit()
        return True
    except SQLAlchemyError as e :
        logger.exception(str(e))
        db.session.rollback()
        db.session.remove()
        return False
        # raise abort(Response(json.dumps({"message":str(e.orig)}), status=400, mimetype='application/json')) 


def upload_ccls_rake_date(rake_data):
    for wagon in rake_data:
        record = CCLSRake(**wagon)
        db.session.add(record)
    commit()
    return True

def upload_pendancy_data(data):
    for container in data:
        if "ctrStat" in container and container["ctrStat"]:
            container_stat = CtrStat.query.filter_by(ctr_stat=container["ctrStat"]).all()
            container["ldd_mt_flg"] = container_stat[0].ldd_mt_flg if container_stat else None
        if not container["ldd_mt_flg"]:
            container["ldd_mt_flg"] = "L" if container["container_weight"] else "E"
        record = PendancyContainer(**container)
        db.session.add(record)
        commit()
    return True


def save_in_diagnostics(url,request,response,start_time,end_time,type=None):
    diag = Diagnostics(url=url,request=request,response=response,start_time=start_time,end_time=end_time,type=type)
    db.session.add(diag)
    commit()