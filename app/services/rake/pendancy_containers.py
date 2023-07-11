from app.services.decorator_service import query_debugger
from app.models import PendancyContainer
from app import db
from app.constants import GroundTruthType
import app.constants as Constants
from app.services import soap_service
from app.logger import logger
from app.services.rake.gt_upload_service import commit
from sqlalchemy import cast, DATE
from datetime import datetime,timedelta
from app.models.utils import db_format,db_functions
import config
import json
import time


class PendancyService():

    def format_data_from_ccls(ccls_data,save_data=False):
        pendancy_list = []
        for each in ccls_data:
            data = {}
            data["container_number"] = each["ctrNo"]
            data["container_life_number"] = each["ctrLifeNo"]
            data["container_stat"] = each["ctrStat"]
            data["container_size"] = each["ctrSize"]
            data["container_type"] = each["ctrType"]
            data["container_weight"] = each["wt"]
            data["container_acty_code"] = each["ctrActyCd"]
            data["icd_loc_code"] = each["locCd"]
            data["stuffed_at"] = each["stfAt"]
            data["stack_loc"] = each["stkLoc"]
            data["sline_code"] = each["slineCd"]
            data["gateway_port_code"] = each["gwPortCd"]
            data["arrival_date"] = each["arrDate"]
            data["seal_number"] = each["sealNo"]
            data["seal_date"] = each["sealDate"]
            data["sbill_number"] = None
            data["sbill_date"] = None
            data["pid_number"] = None
            data["odc_flag"] = each["odcFlg"]
            data["hold_flg"] = None
            data["hold_rels_flg"] = each["holdRelsFlg"]
            data["hold_rels_flg_next"] = None
            data["q_no"] = None

            if save_data:
                PendancyService.save_in_db(data)
                
            if data["container_weight"]:
                data["container_weight"] = float(data["container_weight"])
            if data["seal_date"]:
                data["seal_date"] = data["seal_date"].strftime("%Y-%m-%dT%H:%M:%S")
            if data["arrival_date"]:
                data["arrival_date"] = data["arrival_date"].strftime("%Y-%m-%dT%H:%M:%S")
            if data["container_life_number"]:
                data["container_life_number"] = data["container_life_number"].strftime("%Y-%m-%dT%H:%M:%S")

            pendancy_list.append(data)
    
        return pendancy_list

    def save_in_db(data):
        try:
            container = PendancyContainer(**data)
            result = PendancyContainer.query.filter_by(container_number=data["container_number"])
            if result.all():
                result = result.filter_by(container_life_number=data["container_life_number"])
                if result.all():
                    result.update(dict(data))
                    logger.info("Updated existing container "+ data["container_number"])
                else:
                    db.session.add(container)
                    logger.info("container ( "+data["container_number"]+ ")  exists but container life number is different")
            else:
                logger.info("added new container "+data["container_number"])
                db.session.add(container)
            commit()
        except Exception as e:
            logger.exception(str(e))

    @query_debugger()
    def get_pendancy_list(gateway_ports,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                final_data = []
                for port in gateway_ports:
                    request_params = {'GW_PORT_CODE': port,
                                    # 'P_STUFF_AT': 'FAC',
                                    'P_CUTOFF_DATE': ''}
                    data = soap_service.get_pendancy_details(request_params)
                    if data:
                        final_data += data
                    # for ICD
                    # request_params = {'GW_PORT_CODE': port}
                    # data = soap_service.get_icd_pendancy_details(request_params)
                    # if data:
                    #     for obj in data:
                    #         obj['ctrType'] = 'N/A'
                    #         obj['ctrActyCd'] = 'N/A'
                    #         obj['stfAt'] = 'N/A'
                    #         obj['arrDate'] = None
                    #         obj['sealDate'] = None
                    #         obj['sealNo'] = 'N/A'
                    #         obj['odcFlg'] = 'N/A'
                    #         obj['wt'] = 0
                    #     final_data += data

                if final_data:
                    data = PendancyService.format_data_from_ccls(final_data,True)
                    logger.info("data fetched from CCLS service")
                    return json.dumps(data)
                
            data = PendancyContainer.query.filter(PendancyContainer.gateway_port_code.in_(gateway_ports)).order_by(PendancyContainer.gateway_port_code).all()
            logger.info("data fetched from local db")
            return db_functions(data).as_json()
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1
                time.sleep(Constants.KEY_RETRY_TIMEDELAY)
                PendancyService.get_pendancy_list(data,count=count,isRetry=Constants.KEY_RETRY_VALUE)
