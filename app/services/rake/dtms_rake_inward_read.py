from app.services.decorator_service import query_debugger
from app.services.rake.rake_inward_read import RakeInwardReadService
from app.models import  WgnMst, MissedInwardContainers, DomesticContainers
from app import db
from app.constants import GroundTruthType
import app.constants as Constants
from app.services import soap_service
from app.logger import logger
from app.services.rake.gt_upload_service import commit
from sqlalchemy import cast, DATE, desc
from datetime import datetime,timedelta
import config
import json
import time


class DTMSRakeInwardReadService:

    @query_debugger()
    def get_train_details(query_values,rake_id=None,track_number=None,trans_delay=2,from_date=None,to_date=None,count=Constants.KEY_RETRY_COUNT,isRetry=Constants.KEY_RETRY_VALUE):
        try:
            if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
                pass
            elif config.GROUND_TRUTH == GroundTruthType.SOAP.value:
                result = {}
                if from_date and to_date:
                    result = soap_service.get_domestic_train_details(from_date=from_date,to_date=to_date)
                    if result:
                        data = DTMSRakeInwardReadService.save_in_db(result)
                        return DTMSRakeInwardReadService.format_rake_data(data)                        
                    return []
                # elif "train_number" in query_values["train_number"]:
                #     result = soap_service.get_exim_train_details(query_values["train_number"])
            if "trans_date" in query_values:
                trans_date = query_values.pop('trans_date')
                start_date = trans_date - timedelta(days = trans_delay)
                end_date =  trans_date + timedelta(days = trans_delay)
                rake_query = DomesticContainers.query.filter(cast(DomesticContainers.trans_date, DATE)>=start_date, cast(DomesticContainers.trans_date, DATE)<=end_date)
                rake_query = rake_query.filter_by(**query_values)
            else:
                rake_query = DomesticContainers.query.filter_by(**query_values)
            update_data = {}
            if track_number:
                update_data['track_number'] = track_number
            if rake_id :
                update_data['rake_id'] = rake_id
            if update_data:
                rake_query.update(dict(update_data))
            else:
                rake_query = rake_query.distinct(DomesticContainers.container_number).order_by('container_number')
            commit()
            data = rake_query.order_by(desc('trans_date')).all()
            missed_container_data = []
            if 'rake_id' in query_values:
                missed_containers = MissedInwardContainers.query.filter_by(rake_id=query_values['rake_id'],trans_type=Constants.DOMESTIC_RAKE).all()
                if missed_containers:
                    missed_container_data = json.loads(RakeInwardReadService.format_rake_data(missed_containers,category="Domestic"))
            # if not data and "train_number" in query_values:
            #    logger.info("fetch train details from soap service for train number "+query_values['train_number'])
            #    result = soap_service.get_domestic_train_details(train_number=query_values['train_number'])
            #    if result:
            #        logger.info("Data exists in Soap Servcie for given train number "+query_values['train_number'])
            #        data = DTMSRakeInwardReadService.save_in_db(result)
            domestic_containers = json.loads(DTMSRakeInwardReadService.format_rake_data(data))
            if missed_container_data:
                if domestic_containers:
                    domestic_containers[Constants.WAGON_LIST] += missed_container_data[Constants.WAGON_LIST]
                    domestic_containers[Constants.CONTAINER_LIST] += missed_container_data[Constants.CONTAINER_LIST]
                    return json.dumps(domestic_containers)
                else:
                    return json.dumps(missed_container_data)
            else:
                return json.dumps(domestic_containers)
            
        except Exception as e:
            logger.exception(str(e))
            if isRetry and count >= 0 :
                count=count-1 
                time.sleep(Constants.KEY_RETRY_TIMEDELAY) 
                DTMSRakeInwardReadService.get_train_details(query_values,rake_id,track_number,from_date,to_date,count,isRetry)

    def save_in_db(data_list):
        final_data = []
        for each in data_list:
            wagon = {}
            wagon["train_id"] =  each["DACTRANID"]
            wagon["train_number"] = each["DACTRANNUMB"]
            wagon["rake_number"] = each["DAVRAKEID"]
            wagon["station_from"] = each["DAVSTTNFROM"]
            wagon["station_to"] = each["DAVSTTNTO"]
            wagon["crntsttn"] = each["DAVCRNTSTTN"]
            wagon["rake_pcml_flag"] = each["DACRAKEPCMLFLAG"]
            wagon["withdrawl_time"] = each["DADWITHDRAWLTIME"]
            wagon["destination_plct_time"] = each["DADDSTNPLCTTIME"]
            wagon["line_number"] = each["DACLINENUMB"]
            wagon["rlsd_time"] = each["DADRLSDTIME"]
            wagon["wagon_number"] = each["DACWGONNUMB"].strip() if each["DACWGONNUMB"] else each["DACWGONNUMB"]
            wagon["wagon_type"] = each["DAVWGONTYPE"]
            wagon["sequence_number"] = each["DANSQNCNUMB"]
            wagon["wagon_ldd_mt"] = each["DACLEFLAG_WGON"]
            wagon["top_bottom_flag"] = each["DACTOPBTMFLAG"]
            wagon["man_wagon_cc"] = each["MANWGONCC"]
            wagon["container_id"] = each["DAVCNTRID"]
            wagon["container_number"] = each["DACCNTRNUMB"].strip() if each["DACCNTRNUMB"] else each["DACCNTRNUMB"]
            wagon["iso_code"] = each["DACCNTRTYPE"]
            wagon["container_size"] = each["DANCNTRSIZE"]
            wagon["container_type"] = each["DACCNTRTYPE"]
            wagon["container_from_station"] = each["DAVSTTNFROM_CNTR"]
            wagon["container_to_station"] = each["DAVSTTNTO_CNTR"]
            wagon["ldd_mt_flg"] = each["DACLEFLAG_CNTR"]
            wagon["commodity_code"] = each["DAVCMDTCODE"]
            wagon["seal_number"] = each["DAVSEALNUMB"]
            wagon["mac_hazard_flag"] = each["MACHZDSFLAG"]
            wagon["container_net_weight"] = each["DANNETWGHT"]
            wagon["container_gross_weight"] = each["DANGROSSWGHT"]
            wagon["trans_date"] = each["DADWITHDRAWLTIME"]
            wagon["wagon_ldd_mt"] = "L" if wagon["container_number"] else "E"
            query_fields = {"wagon_number" : wagon["wagon_number"],
             "container_number" : wagon["container_number"],
            "trans_date" : wagon["trans_date"],
            "train_number" : wagon["train_number"]}
            
            # save in CCLSRake
            wagon_model = DomesticContainers(**wagon)
            final_data.append(wagon_model)
            try:
                result = DomesticContainers.query.filter_by(**query_fields)
                if result.all():
                    result.update(dict(wagon))
                    # logger.info("Updated existing wagon")
                else:
                    db.session.add(wagon_model)
                commit()
            except Exception as e:
                logger.exception(str(e))
            
            # Save in Wagon Master
            wagon_data = {"wgn_no" : wagon["wagon_number"]}
            try:
                wagon = WgnMst.query.filter_by(**wagon_data).all()
                if not wagon:
                    wagon_data["wgn_typ"] = "BLCB"
                    wagon_data["commisioned_on"] = datetime.now()
                    wagon = WgnMst(**wagon_data)
                    db.session.add(wagon)
                    commit()
            except Exception as e:
                logger.exception(str(e))
        
        return final_data

    def format_rake_data(data):
        response = {}
        if len(data)>0:
            response[Constants.RAKE_ID] = data[0].rake_id
            response[Constants.TRACK_NUMBER] = data[0].track_number
            response[Constants.RAKE_NUMBER]  = data[0].rake_number
            response[Constants.TRAIN_NUMBER]  = data[0].train_number
            response[Constants.RAKE_TYPE] = data[0].rake_type
            response[Constants.WAGON_LIST] = []
            response[Constants.CONTAINER_LIST] = []
            for i in range(len(data)):
                wagon_record = {Constants.WAGON_NUMBER :{ Constants.NUMBER : str(data[i].wagon_number),Constants.KEY_ID:None,Constants.WAGON_LDD_MT:data[i].wagon_ldd_mt}}
                response[Constants.WAGON_LIST].append(wagon_record)
                container_record ={}
                container_record[Constants.CONTAINER_NUMBER] = {Constants.VALUE : data[i].container_number}
                container_record[Constants.COMMIDITY]= data[i].commodity_code
                container_record[Constants.LINER_SEAL] = {Constants.VALUE : None,Constants.SEAL_DATE: None}
                container_record[Constants.CUSTOM_SEAL] = {Constants.VALUE : data[i].seal_number,Constants.SEAL_DATE: None}
                container_record[Constants.POD] = data[i].container_to_station
                container_record[Constants.ISO_CODE] = {Constants.VALUE : data[i].iso_code if data[i].iso_code else str(int(data[i].container_size))+str(data[i].container_type) if data[i].container_size and data[i].container_type else None}
                container_record[Constants.LDD_MT_FLAG] = {Constants.VALUE : data[i].ldd_mt_flg} 
                container_record[Constants.KEY_SLINE_CODE] =  {Constants.VALUE : None}
                container_record[Constants.WAGON_NUMBER] = wagon_record[Constants.WAGON_NUMBER]
                # container_record[Constants.CONTAINER_STAT] = "E"
                container_record[Constants.CATEGORY] = "Domestic"
                container_record[Constants.CONTAINER_STAT] = data[i].container_stat
                container_record[Constants.KEY_CONTAINER_WEIGHT] = data[i].container_gross_weight
                container_record[Constants.KEY_CONTAINER_SIZE] = data[i].container_size
                container_record[Constants.KEY_CONTAINER_TYPE] = data[i].container_type
                
                response[Constants.CONTAINER_LIST].append(container_record)
                logger.info("fetched DTMS data %s",response)
        return json.dumps(response)
    
    def format_dtms_data(data):
        response = []
        for i in range(len(data)):
            container_record ={}
            container_record[Constants.RAKE_ID] = data[i].rake_id
            container_record[Constants.TRACK_NUMBER] = data[i].track_number
            container_record[Constants.RAKE_NUMBER]  = data[i].rake_number
            container_record[Constants.TRAIN_NUMBER]  = data[i].train_number
            container_record[Constants.RAKE_TYPE] = data[i].rake_type
            container_record[Constants.WAGON_LIST] = []
            wagon_record = {Constants.WAGON_NUMBER :{ Constants.NUMBER : str(data[i].wagon_number),Constants.KEY_ID:None}}
            container_record[Constants.WAGON_LIST].append(wagon_record)
            container_record[Constants.CONTAINER_NUMBER] = {Constants.VALUE : data[i].container_number}
            container_record[Constants.COMMIDITY]= data[i].commodity_code
            container_record[Constants.LINER_SEAL] = {Constants.VALUE : None}
            container_record[Constants.CUSTOM_SEAL] = {Constants.VALUE : data[i].seal_number}
            container_record[Constants.POD] = data[i].container_to_station
            container_record[Constants.ISO_CODE] = {Constants.VALUE : data[i].iso_code if data[i].iso_code else str(int(data[i].container_size))+str(data[i].container_type) if data[i].container_size and data[i].container_type else None}
            container_record[Constants.LDD_MT_FLAG] = {Constants.VALUE : data[i].ldd_mt_flg} 
            container_record[Constants.KEY_SLINE_CODE] =  {Constants.VALUE : None}
            container_record[Constants.WAGON_NUMBER] = { Constants.NUMBER : str(data[i].wagon_number),Constants.KEY_ID:None}
            container_record[Constants.CONTAINER_STAT] = "E"
            container_record[Constants.CATEGORY] = "Domestic"
            container_record[Constants.CONTAINER_STAT] = data[i].container_stat
            container_record[Constants.KEY_CONTAINER_WEIGHT] = data[i].container_gross_weight
            container_record[Constants.KEY_CONTAINER_SIZE] = data[i].container_size
            container_record[Constants.KEY_CONTAINER_TYPE] = data[i].container_type
            response.append(container_record)
        return json.dumps(response)

    # @query_debugger()
    # def get_dtms_details(start_date,end_date):
    #     rake_query = DomesticContainers.query.filter(cast(DomesticContainers.trans_date, DATE)>=start_date, cast(DomesticContainers.trans_date, DATE)<=end_date).all()
    #     if rake_query:
    #         return DTMSRakeInwardReadService.format_dtms_data(rake_query)
    #     return rake_query
    
    def get_train_number(container_list,wagon_list,trans_date,trans_delay):
        train_number = None
        start_date = trans_date - timedelta(days = trans_delay)
        end_date =  trans_date + timedelta(days = trans_delay)
        rake_query = DomesticContainers.query.filter(cast(DomesticContainers.trans_date, DATE)>=start_date, cast(DomesticContainers.trans_date, DATE)<=end_date)
        if container_list:
            data = rake_query.filter(DomesticContainers.container_number.in_(container_list)).order_by(DomesticContainers.trans_date.desc()).all()
            train_number = data[0].train_number if data else None
        if not train_number and wagon_list:
            data = rake_query.filter(DomesticContainers.wagon_number.in_(wagon_list)).order_by(DomesticContainers.trans_date.desc()).all()
            train_number = data[0].train_number if data else None
        logger.info("dom train number %s, given trans_date: %s, trans_delay %s, wagon_list: %s,container_list : %s",train_number,str(trans_date),str(trans_delay),str(wagon_list),str(container_list) )
        return train_number
    
    def update_rake_id_and_track_number(trans_date,trans_delay,train_number,rake_id,track_number):
        start_date = trans_date - timedelta(days = trans_delay)
        end_date =  trans_date + timedelta(days = trans_delay)
        rake_query = DomesticContainers.query.filter(cast(DomesticContainers.trans_date, DATE)>=start_date, cast(DomesticContainers.trans_date, DATE)<=end_date).filter_by(train_number=train_number)
        update_data = {}
        if track_number:
                update_data['track_number'] = track_number
        if rake_id :
            update_data['rake_id'] = rake_id
        if update_data:
            rake_query.update(dict(update_data))
            if commit():
                return True
        return False

    @query_debugger()
    def get_dtms_train_no_details(train_no):
        rake_query = DomesticContainers.query.filter_by(train_number=train_no).all()
        if rake_query:
            return DTMSRakeInwardReadService.format_dtms_data(rake_query)
        return rake_query
        
    @query_debugger()
    def dtms_details(start_date,end_date,train_no=None):
        if train_no:
            rake = DomesticContainers.query.filter(cast(DomesticContainers.trans_date, DATE)>=start_date, cast(DomesticContainers.trans_date, DATE)<=end_date)
            rake_query = rake.filter_by(train_number=train_no).all()
        else:
            rake_query = DomesticContainers.query.filter(cast(DomesticContainers.trans_date, DATE)>=start_date, cast(DomesticContainers.trans_date, DATE)<=end_date).all()
        if rake_query:
            return DTMSRakeInwardReadService.format_dtms_data(rake_query)
        return rake_query