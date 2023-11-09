from app.services.decorator_service import query_debugger
from app import db
from app.services import soap_service
from app.models import PendancyContainer
from app.models.utils import db_format,db_functions
from app.logger import logger
from app.services.rake.gt_upload_service import commit
from sqlalchemy import cast, DATE, desc
from datetime import datetime,timedelta
import config
import json
import time


class DTMSRakeOutwardReadService:
    def format_data_from_ccls(ccls_data,pendency_type,save=False):
        pendency_containers = []
        for each in ccls_data:
            data = {}
            data["container_number"] = each["DACCNTRNUMB"]
            data["container_type"] = each["DACCNTRTYPE"]
            data["container_weight"] = float(each["D_DANWGHT"])
            data["stack_loc"] = each["DACSTCKLOCN"].strip() if each["DACSTCKLOCN"] else each["DACSTCKLOCN"]
            data["seal_number"] = each["DAVSEALNUMB"]
            data["seal_date"] = each["DADCNFRMSEALTIME"]
            data["station_from"] = each["DAVSTTNFROM"]
            data["station_to"] = each["DAVSTTNTO"]
            data["ldd_mt_flg"] = each["DACLEFLAG"]
            data["commodity_code"] = each["DAVCMDTCODE"]
            data["pendency_type"] = int(pendency_type)
            data["container_size"] = 20 if each["DACCNTRTYPE"] and each["DACCNTRTYPE"].startswith('2') else 40
            data["container_type"] = each["DACCNTRTYPE"]
            data["container_category"] = "Domestic"
            # data["container_tare_weight"] = float(each["MANTARE"])
            # data[""] = each["DACSRVCMODE"]
            # data[""] = each["DAVCNSRCODE"]
            # data[""] = each["DAVCNSECODE"]
            # data[""] = each["DACCRNTSTTS"]
            # data[""] = float(each["DANWGHT"])

            # may be required
            data["container_life_number"] = None
            data["container_stat"] = None
            data["container_acty_code"] = None
            data["icd_loc_code"] = None
            data["stuffed_at"] = None
            data["sline_code"] = None
            data["gateway_port_code"] = None
            data["arrival_date"] = None
            data["sbill_number"] =  None
            data["sbill_date"] = None
            data["cargo_flag"] =  None
            data["pid_number"] = None
            data["odc_flag"] = None
            data["hold_flg"] = None
            data["hold_rels_flg"] = None
            data["hold_rels_flg_next"] = None
            data["q_no"] = None
            if save:
                DTMSRakeOutwardReadService.save_in_db(data)
            if data["seal_date"]:
                data['seal_date'] = data['seal_date'].isoformat()
            pendency_containers.append(data)
        return pendency_containers
    
    def save_in_db(data):
        try:
            container = PendancyContainer(**data)
            result = PendancyContainer.query.filter_by(container_number=data["container_number"])
            if result.all():
                result.update(dict(data))
            else:
                logger.info("added new dom container "+data["container_number"])
                db.session.add(container)
            commit()
        except Exception as e:
            logger.exception(str(e))
    
    
    def get_outward_domestic_containers(dom_pendency_list):
        final_data = []
        for each in dom_pendency_list:
            for station in  each["station_code"]:
                data = {"Port" : station}
                ccls_data = soap_service.get_domestic_outward_train_details(data)
                final_data += DTMSRakeOutwardReadService.format_data_from_ccls(ccls_data,each['pendency_type'],True)
        if final_data:
            return final_data
        logger.info("domestic container data fetched from local db")
        data = []
        for each in dom_pendency_list:
            data += PendancyContainer.query.filter(PendancyContainer.station_to.in_(each['station_code']),PendancyContainer.pendency_type == int(each["pendency_type"])).all()
        data = db_functions(data).as_json()
        return json.loads(data)


