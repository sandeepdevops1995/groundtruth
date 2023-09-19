from app.services.decorator_service import query_debugger
from app import db
from app.services import soap_service
from app.logger import logger
from app.services.rake.gt_upload_service import commit
from sqlalchemy import cast, DATE, desc
from datetime import datetime,timedelta
import config
import json
import time


class DTMSRakeOutwardReadService:
    def format_data_from_ccls(ccls_data,save=False):
        pendency_containers = []
        for each in ccls_data:
            data = {}
            data["container_number"] = each["DACCNTRNUMB"]
            data["container_type"] = each["DACCNTRTYPE"]
            data["container_weight"] = each["D_DANWGHT"]
            data["stack_loc"] = each["DACSTCKLOCN"]
            data["seal_number"] = each["DAVSEALNUMB"]
            data["seal_date"] = each["DADCNFRMSEALTIME"]
            data["station_from"] = each["DAVSTTNFROM"]
            data["station_to"] = each["DAVSTTNTO"]
            data["ldd_mt_flg"] = each["DACLEFLAG"]
            data["commodity_code"] = each["DAVCMDTCODE"]
            data["container_tare_weight"] = each["MANTARE"]
            # data[""] = each["DACSRVCMODE"]
            # data[""] = each["DAVCNSRCODE"]
            # data[""] = each["DAVCNSECODE"]
            # data[""] = each["DACCRNTSTTS"]
            # data[""] = each["DANWGHT"]
            pendency_containers.append(data)
        return json.dumps(pendency_containers)
    
    def get_outward_domestic_containers(data):
        return soap_service.get_domestic_outward_train_details(data)



