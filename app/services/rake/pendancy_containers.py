from app.services.decorator_service import query_debugger
from app.models import PendancyContainer, CtrStat
from app import db
from app.constants import GroundTruthType
from app.enums import PendencyType
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
                data["seal_date"] = each["dtSeal"]
            if data["seal_date"]:
                #data["seal_date"] = data["seal_date"].strftime("%Y-%m-%dT%H:%M:%S")
                #data['seal_date'] = datetime.strptime(data['seal_date'], '%Y-%m-%d %H:%M:%S').isoformat()
                data['seal_date'] = data['seal_date'].isoformat()
                logger.warn("seal_date type:"+str(type(data['seal_date'])))
            """
            if data["seal_datetime"]:
                #data["seal_datetime"] = data["seal_datetime"].strftime("%Y-%m-%dT%H:%M:%S")
                data['seal_datetime'] = datetime.strptime(data['seal_datetime'], '%Y-%m-%d %H:%M:%S').isoformat()
                logger.warn("seal_datetime type:"+str(type(data['seal_datetime'])))
            """
            if isinstance(data['arrival_date'], datetime) and data["arrival_date"]:
                data["arrival_date"] = data["arrival_date"].strftime("%Y-%m-%dT%H:%M:%S")
            else:
                logger.warn("arrival_date is not datetime format: "+str(data['arrival_date']))
                ##data['arrival_date'] = None
                data['arrival_date'] = datetime.now().replace(microsecond=0).isoformat()
                ##data['arrival_date'] = datetime.now()
                ##data['arrival_date'] = datetime.strptime(data['arrival_date'], '%Y-%m-%d %H:%M:%S').isoformat()
                #data['arrival_date'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                ###datetime.strptime(data["permit_date"], '%Y-%m-%d %H:%M:%S').isoformat() if data["permit_date"]
                #data['arrival_date'] = datetime.now()
                logger.warn("arrival_date type:"+str(type(data['arrival_date'])))
                ##logger.warn("arrival_date value: "+data['arrival_date'])
            if data["container_life_number"]:
                ##data["container_life_number"] = data["container_life_number"].strftime("%Y-%m-%dT%H:%M:%S")
                #data['container_life_number'] = datetime.strptime(data['container_life_number'], '%Y-%m-%d %H:%M:%S').isoformat()
                data['container_life_number'] = data['container_life_number'].isoformat()
                logger.warn("container_life_number data type:"+str(type(data['container_life_number'])))
            if data["hold_rels_flg"]:
                data['hold_rels_flg'] = data['hold_rels_flg'].isoformat()
                logger.warn("hold rels flag data type:"+str(type(data['hold_rels_flg'])))
                
            container_stat = CtrStat.query.filter_by(ctr_stat=each["ctrStat"]).all()
            data["imp_exp_flg"] = container_stat[0].imp_exp_flg if container_stat else None
            data["ldd_mt_flg"] = container_stat[0].ldd_mt_flg if container_stat else None
            data["gw_port_cd"] = container_stat[0].gw_port_cd if container_stat else None

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
    def get_pendancy_list(pendency_types,gateway_ports,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                final_data = []
                logger.info("pendency types = ",str(pendency_types), type(pendency_types))
                for pendency_type in pendency_types:
                    pendency_type = int(pendency_type)
                    if PendencyType.LOADED.value == pendency_type:
                        logger.info("fetching LOADED pendancy containers")
                        for port in gateway_ports:
                            request_params = {'GW_PORT_CODE': port,
                                            # 'P_STUFF_AT': 'FAC',
                                            'P_CUTOFF_DATE': ''}
                            data = soap_service.get_pendancy_details(request_params)
                            if data:
                                final_data += data
                    elif PendencyType.EMPTY.value == pendency_type:
                        logger.info("fetching EMPTY pendancy containers")
                        for port in gateway_ports:
                            request_params = {'GW_PORT_CODE': port}
                            data = soap_service.get_empty_pendancy_details(request_params)
                            if data:
                                for obj in data:
                                    obj['ctrType'] = 'N/A'
                                    obj['ctrActyCd'] = 'N/A'
                                    obj['stfAt'] = 'N/A'
                                    obj['arrDate'] = None
                                    obj['sealDate'] = None
                                    obj['sealNo'] = 'N/A'
                                    obj['odcFlg'] = 'N/A'
                                    obj['wt'] = 0
                                final_data += data

                    elif PendencyType.BLOCK.value == pendency_type:
                        logger.info("fetching BLOCK pendancy containers")
                        for port in gateway_ports:
                            request_params = {'GW_PORT_CODE': port}
                            data = soap_service.get_block_pendancy_details(request_params)
                            if data:
                                final_data += data

                    elif PendencyType.EXPRESS.value == pendency_type:
                        logger.info("fetching EXPRESS pendancy containers")
                        for port in gateway_ports:
                            request_params = {'GW_PORT_CODE': port}
                            data = soap_service.get_express_pendancy_details(request_params)
                            if data:
                                final_data += data

                    elif PendencyType.LCL.value == pendency_type:
                        logger.info("fetching LCL pendancy containers")
                        pass
                        # logger.info("fetching LCL peendancy containers")
                        # for port in gateway_ports:
                        #     request_params = {'GW_PORT_CODE': port}
                        #     data = soap_service.get_lcl_pendancy_details(request_params)
                        #     if data:
                        #         final_data += data

                if final_data:
                    data = PendancyService.format_data_from_ccls(final_data,True)
                    #logger.info("data fetched from CCLS service: "+str(data))
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
