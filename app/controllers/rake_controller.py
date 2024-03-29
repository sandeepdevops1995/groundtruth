from flask_restful import Resource, reqparse
from app.services.soap_service import get_exim_train_details,get_domestic_train_details
import config
import app.constants as Constants
from flask import json, Response,request
from app.logger import logger
from app.services.rake.rake_db_service import RakeDbService as db_service
from app.services.decorator_service import custom_exceptions, api_auth_required
from app.constants import GroundTruthType
from app.serializers.master_data_serializers import *
from app.services.master_db_service import MasterData as master_db
from app.services.rake.rake_inward_write import RakeInwardWriteService,WriteInContainer
from app.services.rake.rake_outward_write import RakeOutwardWriteService
from app.services.rake.rake_inward_read import RakeInwardReadService
from app.services.rake.dtms_rake_inward_read import DTMSRakeInwardReadService
from app.services.rake.dtms_rake_inward_write import DTMSRakeInwardWriteService
from app.services.rake.dtms_rake_outward_write import DTMSRakeOutwardWriteService
from app.services.rake.rake_outward_plan import RakeOutwardPlanService
from app.services.rake.pendancy_containers import  PendancyService
from app.services.rake.dtms_rake_outward_read import DTMSRakeOutwardReadService
from datetime import date, datetime, timedelta
from app.controllers.utils import View, soap_API_response
import json


class TrainDetails(View):   
    @custom_exceptions
    # @api_auth_required
    def get(self):
        exim_train_number = request.args.get(Constants.EXIM_TRAIN_NUMBER,None)
        dom_train_number = request.args.get(Constants.DOM_TRAIN_NUMBER,None)
        track_number = request.args.get(Constants.TRACK_NUMBER,None)
        rake_id = request.args.get(Constants.RAKE_ID,None)
        rake_type = request.args.get(Constants.RAKE_TYPE,"AR")
        rake_tx_type = request.args.get(Constants.RAKE_TX_TYPE,Constants.EXIM_RAKE)
        wagon_number = request.args.get(Constants.WAGON_NUMBER,None)
        container_number = request.args.get(Constants.KEY_CN_NUMBER,None)
        container_life_number = request.args.get(Constants.KEY_CN_LIFE_NUMBER,None)
        trans_date = request.args.get(Constants.KEY_TRANS_DATE,None)
        trans_delay = int(request.args.get(Constants.KEY_TRANS_DELAY,2))
        from_date = request.args.get(Constants.KEY_FROM_DATE,None)
        to_date = request.args.get(Constants.KEY_TO_DATE,None)
        data = {}
        if wagon_number:
            data["wagon_number"]=wagon_number
        if container_number:
            data["container_number"] = container_number
        if container_life_number:
            data["container_life_number"] = container_life_number
        if trans_date:
            data["trans_date"] = datetime.strptime(trans_date, '%Y-%m-%d %H:%M:%S').date()
        
        if((not data)  and (not(from_date and to_date))):
            message = "please provide query parameters"
            return Response(json.dumps({"message":message}), status=400,mimetype='application/json')
        logger.info('GT,Get request from the Rake service : {},{}'.format(exim_train_number,dom_train_number))
        result = {}
        if rake_type == "AR":
            if from_date and to_date:
                self.request_soap_api(trans_delay,rake_tx_type,from_date,to_date)
                return Response({"message":"requested soap API"}, status=200, mimetype='application/json')
            result = self.get_inward_summary_containers(data,exim_train_number,dom_train_number,rake_id,rake_tx_type,track_number,trans_delay,from_date,to_date)
        elif rake_type == "DE":
            result = RakeOutwardPlanService.get_rake_plan(rake_id,exim_train_number,track_number)
        else:
            return Response({"mesaage":"unknown rake type"}, status=400, mimetype='application/json')
        logger.info('Conainer details response')
        return Response(result, status=200, mimetype='application/json')
    

    def get_inward_summary_containers(self,data,exim_train_number,dom_train_number,rake_id,rake_tx_type,track_number,trans_delay,from_date,to_date):
        result = {}
        if rake_tx_type in [Constants.EXIM_RAKE, Constants.HYBRID_RAKE] and exim_train_number :
            data['train_number'] = exim_train_number
            exim_containers = RakeInwardReadService.get_train_details(data,rake_id,track_number,trans_delay,from_date=from_date,to_date=to_date)
            result = json.loads(exim_containers) if exim_containers else {}
        if rake_tx_type in [Constants.DOMESTIC_RAKE, Constants.HYBRID_RAKE] and dom_train_number :
            data['train_number'] = dom_train_number
            dom_containers = DTMSRakeInwardReadService.get_train_details(data,rake_id,track_number,trans_delay,from_date=from_date,to_date=to_date)
            if dom_containers:
                dom_containers = json.loads(dom_containers) if dom_containers else {}
            if result and dom_containers:
                if Constants.WAGON_LIST in dom_containers:
                    if Constants.WAGON_LIST in result:
                        result[Constants.WAGON_LIST] += dom_containers[Constants.WAGON_LIST]
                    else:
                        result[Constants.WAGON_LIST] = dom_containers[Constants.WAGON_LIST]
                if Constants.CONTAINER_LIST in dom_containers:
                    if Constants.CONTAINER_LIST in result:
                        result[Constants.CONTAINER_LIST] += dom_containers[Constants.CONTAINER_LIST]
                    else:
                        result[Constants.CONTAINER_LIST] = dom_containers[Constants.CONTAINER_LIST]
            elif dom_containers:
                result = dom_containers
        return json.dumps(result)

    def request_soap_api(self,trans_delay,rake_tx_type,from_date=None,to_date=None):
        if not from_date:
            from_date = (datetime.now()-timedelta(days = trans_delay)).strftime("%Y-%m-%dT%H:%M:%S")
        if not to_date:
            to_date = (datetime.now()+timedelta(days = trans_delay)).strftime("%Y-%m-%dT%H:%M:%S")
        if rake_tx_type in [Constants.EXIM_RAKE, Constants.HYBRID_RAKE] :
            RakeInwardReadService.get_train_details({},from_date=from_date,to_date=to_date)
        if rake_tx_type in [Constants.DOMESTIC_RAKE, Constants.HYBRID_RAKE]:
            DTMSRakeInwardReadService.get_train_details({},from_date=from_date,to_date=to_date)


class TrainNumberDetails(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        rake_type = request.args.get(Constants.RAKE_TYPE,"AR")
        rake_tx_type = request.args.get(Constants.RAKE_TX_TYPE,Constants.EXIM_RAKE)
        wagon_list = request.args.get(Constants.WAGON_LIST,None)
        container_list = request.args.get(Constants.CONTAINER_LIST,None)
        trans_date = request.args.get(Constants.KEY_TRANS_DATE,None)
        trans_delay = int(request.args.get(Constants.KEY_TRANS_DELAY,2))
        if wagon_list:
            wagon_list = json.loads(wagon_list)
        if container_list:
            container_list = json.loads(container_list)
        if trans_date:
            trans_date = datetime.strptime(trans_date, '%Y-%m-%d %H:%M:%S').date()
        exim_train_number = dom_train_number = None 
        if rake_tx_type in [Constants.EXIM_RAKE,Constants.HYBRID_RAKE]:
            exim_train_number = RakeInwardReadService.get_train_number(container_list,wagon_list,trans_date,trans_delay)
            if not exim_train_number:
                TrainDetails().request_soap_api(trans_delay,Constants.EXIM_RAKE)
                exim_train_number = RakeInwardReadService.get_train_number(container_list,wagon_list,trans_date,trans_delay)

        if rake_tx_type in [Constants.DOMESTIC_RAKE,Constants.HYBRID_RAKE]:
            dom_train_number = DTMSRakeInwardReadService.get_train_number(container_list,wagon_list,trans_date,trans_delay)
            if not dom_train_number:
                TrainDetails().request_soap_api(trans_delay,Constants.DOMESTIC_RAKE)
                dom_train_number = DTMSRakeInwardReadService.get_train_number(container_list,wagon_list,trans_date,trans_delay)

        return Response(json.dumps({"exim_train_number":exim_train_number,"dom_train_number":dom_train_number}),status=200, mimetype='application/json')

class UpdateRakeDetails(View):
    @custom_exceptions
    @api_auth_required
    def put(self):
        data = request.get_json()
        rake_type = data.pop(Constants.RAKE_TYPE,"AR")
        rake_tx_type = data.pop(Constants.RAKE_TX_TYPE,Constants.EXIM_RAKE)
        rake_id = data.pop(Constants.RAKE_ID,None)
        track_number = data.pop(Constants.TRACK_NUMBER,None)
        exim_train_number = data.pop(Constants.EXIM_TRAIN_NUMBER,None)
        dom_train_number =   data.pop(Constants.DOM_TRAIN_NUMBER,None)
        trans_date = data.pop(Constants.KEY_TRANS_DATE,None)
        trans_delay = int(data.pop(Constants.KEY_TRANS_DELAY,2))
        if trans_date:
            trans_date = datetime.strptime(trans_date, '%Y-%m-%d %H:%M:%S').date()
        sucess =  None
        if rake_tx_type in [Constants.EXIM_RAKE,Constants.HYBRID_RAKE]:
            sucess = RakeInwardReadService.update_rake_id_and_track_number(trans_date,trans_delay,exim_train_number,rake_id,track_number)
        if rake_tx_type in [Constants.DOMESTIC_RAKE,Constants.HYBRID_RAKE]:
            sucess = DTMSRakeInwardReadService.update_rake_id_and_track_number(trans_date,trans_delay,dom_train_number,rake_id,track_number)
        if sucess:
            return Response(json.dumps({"message":"rake_id and track_number updated"}),status=200, mimetype='application/json')
        return Response(json.dumps({"message":"failed to update rake_id and track_number "}),status=400, mimetype='application/json')


class RakeData(View):
    @custom_exceptions
    # @api_auth_required
    def post(self):
        print("got rake post request===")
        if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
            db_service.push_test_data_arrival()
            db_service.push_test_data_departure()
        file = request.files['file']   
        rake_data = db_service().get_rake_file_data(file)
        response = db_service().save_rake_details(rake_data) 
        return Response(None, status=200, mimetype='application/json')


    @custom_exceptions
    # @api_auth_required
    def get(self):
        rake_number = request.args.get(Constants.RAKE_NUMBER,None)
        rake_id = request.args.get(Constants.RAKE_ID,None)
        track_number = request.args.get(Constants.TRACK_NUMBER,None)
        rake_type = request.args.get(Constants.RAKE_TYPE,"AR")
        trans_type = request.args.get(Constants.RAKE_TX_TYPE,"HYBRID")
        data = {}        
        if rake_id:
            data["rake_id"]=rake_id
        if track_number:
            data["track_number"]=track_number
        if rake_number:
            data["rake_number"] = rake_number
            
        if not rake_number and not track_number and not rake_id:
            message = "please provide query parameters"
            return Response(json.dumps({"message":message}), status=204,mimetype='application/json')
        logger.info('GT,Get request from the Rake service : {} {} {}'.format(rake_id,rake_number,track_number))
        result = {}
        if trans_type in [Constants.EXIM_RAKE, Constants.HYBRID_RAKE]:
            exim_containers = RakeInwardReadService.get_train_details(data)
            result = json.loads(exim_containers) if exim_containers else {}
        if trans_type in [Constants.DOMESTIC_RAKE, Constants.HYBRID_RAKE] :
            dom_containers = DTMSRakeInwardReadService.get_train_details(data)
            if dom_containers:
                dom_containers = json.loads(dom_containers) if dom_containers else {}
            if result and dom_containers:
                if Constants.WAGON_LIST in dom_containers:
                    if Constants.WAGON_LIST in result:
                        result[Constants.WAGON_LIST] += dom_containers[Constants.WAGON_LIST]
                    else:
                        result[Constants.WAGON_LIST] = dom_containers[Constants.WAGON_LIST]
                if Constants.CONTAINER_LIST in dom_containers:
                    if Constants.CONTAINER_LIST in result:
                        result[Constants.CONTAINER_LIST] += dom_containers[Constants.CONTAINER_LIST]
                    else:
                        result[Constants.CONTAINER_LIST] = dom_containers[Constants.CONTAINER_LIST]
            elif dom_containers:
                result = dom_containers
        return Response(json.dumps(result), status=200, mimetype='application/json')

class PendancyList(View):
    @custom_exceptions
    # @api_auth_required
    def get(self):
        pendency_types = request.args.get(Constants.KEY_PENDENCY_TYPE,None)
        if pendency_types:
            logger.info("GT, pendacy list for pendency types: "+pendency_types)
            pendency_types = json.loads(pendency_types)
            exim_pendency_list = []
            dom_pendency_list = []
            exim_response = dom_response = {}
            for each in pendency_types:
                if "station_code" in each:
                    dom_pendency_list.append(each)
                else:
                    exim_pendency_list.append(each)
            if exim_pendency_list:
                exim_response = PendancyService.get_pendancy_list(exim_pendency_list)
            if dom_pendency_list:
                dom_response = DTMSRakeOutwardReadService.get_outward_domestic_containers(dom_pendency_list)
            response = []
            if exim_response:
                response += exim_response
            if dom_response:
                response += dom_response
            return Response(json.dumps(response), status=200, mimetype='application/json')
        else:
            return Response(json.dumps({"message":"please provide pendancy types"}), status=400, mimetype='application/json')
    
    
    def format_data(self,response,gateway_ports):
        output = {}
        for port in gateway_ports:
            output[port] = []
        for each in json.loads(response):
            output[each["gateway_port_code"]].append(each)
        final_output =[]
        for port in gateway_ports:
            port_data ={}
            port_data["gateway_port"] = port
            port_data["containers"] = output[port]
            final_output.append(port_data)
        return json.dumps(final_output)
            

class DomesticPendancyList(View):
    @custom_exceptions
    # @api_auth_required
    def get(self):
        # process = request.args.get("process",None)
        data = {"Process" : None}
        logger.info("GT, Domestic pendacy list for pendency types: ")
        response = DTMSRakeOutwardReadService.get_outward_domestic_containers(data)
        return Response(response, status=200, mimetype='application/json')
        
class RakeInContainer(View):
    @custom_exceptions
    @api_auth_required
    def post(self):
        data = request.get_json()
        if data:
            if WriteInContainer.update_missed_container_details(data):
                return Response(json.dumps({"message":"success"}),status=200,mimetype='application/json')
        return Response(json.dumps({"message":"failed to save"}),status=400,mimetype='application/json')

class RakePlanDetails(View):
    @custom_exceptions
    # @api_auth_required
    def post(self):
        data = request.get_json()
        if data:
            if RakeOutwardPlanService.add_rake_plan(data):
                return Response(json.dumps({"message":"success"}),status=200,mimetype='application/json')
    
    @custom_exceptions
    # @api_auth_required
    def get(self):
        rake_id = request.args.get(Constants.KEY_RAKE_ID)
        if rake_id:
            logger.info("GT,fetch Rake plan details"+rake_id)
            response =  RakeOutwardPlanService.get_rake_plan(rake_id)
            return Response(response,status=200,mimetype='application/json')
        
class UpdateRakeContainerDetails(View):
    @custom_exceptions
    @api_auth_required
    def post(self):
        data = request.get_json()
        if data:
            tx_type = data.pop('tx_type')
            if tx_type == "INWARD":
                response = RakeInwardWriteService.update_container(data)
            elif tx_type == "OUTWARD":
                response = RakeOutwardWriteService.update_container(data)
            else:
                logger.info("rake_type is an unexpected format - "+tx_type)
                response = {}
            return soap_API_response(response)
        return Response(json.dumps({"message":"please provide valid data"}),status=400,mimetype='application/json')
        
class UpdateCGISurvey(View):
    @custom_exceptions
    @api_auth_required
    def post(self):
        data = request.get_json()
        if data:
            response = RakeInwardWriteService.update_CGI_survey(data)
            return soap_API_response(response)
        return Response(json.dumps({"message":"please provide valid data"}),status=400,mimetype='application/json')
   
class UpdateCGOSurvey(View):
    @custom_exceptions
    @api_auth_required
    def post(self):
        data = request.get_json()
        if data:
            response = RakeOutwardWriteService.update_CGO_survey(data)
            return soap_API_response(response)
        return Response(json.dumps({"message":"please provide valid data"}),status=400,mimetype='application/json')
   
class UpdateVGISurvey(View):
    @custom_exceptions
    @api_auth_required
    def post(self):
        data = request.get_json()
        if data:
            response = DTMSRakeInwardWriteService.update_VGI_survey(data)
            return soap_API_response(response)
        return Response(json.dumps({"message":"please provide valid data"}),status=400,mimetype='application/json')

class UpdateVGOSurvey(View):
    @custom_exceptions
    @api_auth_required
    def post(self):
        data = request.get_json()
        if data:
            response = DTMSRakeOutwardWriteService.update_VGO_survey(data)
            return soap_API_response(response)
        return Response(json.dumps({"message":"please provide valid data"}),status=400,mimetype='application/json')


class WagonMaster(View):
    @custom_exceptions
    # @api_auth_required
    def post(self):
        data = request.get_json()
        if data:
            if db_service.add_wagon_to_master_data(data):
                return Response(json.dumps({"message":"success"}),status=200,mimetype='application/json')
        return Response(json.dumps({"message":"failed to save"}),status=400,mimetype='application/json')
    
    @custom_exceptions
    # @api_auth_required
    def get(self):
        wagon_number = request.args.get(Constants.KEY_NUMBER,None)
        logger.info("GT,fetch wagon master data for wagon {}".format(wagon_number))
        response =  db_service.get_wagon_master_data(wagon_number)
        response = WagonMasterSchema(many=True).dump(response)
        if response:
            return Response(json.dumps(response),status=200,mimetype='application/json')
        else:
            return Response(None,status=204,mimetype='application/json')
class GatewayPortsMaster(View):
    @custom_exceptions
    # @api_auth_required
    def post(self):
        data = request.get_json()
        if data:
            if db_service.add_gateway_port_to_master_data(data):
                return Response(json.dumps({"message":"success"}),status=200,mimetype='application/json')
        return Response(json.dumps({"message":"failed to save"}),status=400,mimetype='application/json')
    
    @custom_exceptions
    @api_auth_required
    def get(self):
        logger.info("GT,fetch gateway port master data")
        response = db_service.get_gateway_port_master_data()
        response = GateWayPortMasterSchema(many=True).dump(response)
        if response:
            return Response(json.dumps(response),status=200,mimetype='application/json')
        else:
            return Response(None,status=204,mimetype='application/json')
    
            
class ValidateWagon(View):
    @api_auth_required
    def get(self):
        wagon_number = request.args.get(Constants.KEY_WAGON_NUMBER,None)
        logger.info("GT,validate wagon details"+wagon_number)
        if wagon_number:
            response =  db_service.validate_wagon_number(wagon_number)
            if response:
                return Response(json.dumps(response),status=200,mimetype='application/json')
            return Response(status=204,mimetype='application/json')
        return Response({"message" : "please provide with wagons_list"},status=400,mimetype='application/json')

class UpdateInwardRakeDetails(View):
    @custom_exceptions
    @api_auth_required
    def post(self):
        data = request.get_json()
        if set(Constants.rake_write_required_fields).issubset(set(data.keys())):
            result = {}
            result =  RakeInwardWriteService.update_inward_train_summary(data)
            return soap_API_response(result)
        else:
            return Response(json.dumps({"message":"please provide all required fields", "required fields" :Constants.rake_write_required_fields}), status=400, mimetype='application/json')


class UpdateOutwardRakeDetails(View):
    # @custom_exceptions
    @api_auth_required
    def post(self):
        data = request.get_json()
        if set(Constants.rake_write_required_fields).issubset(set(data.keys())):
            result = RakeOutwardWriteService.update_outward_train_summary(data)
            if not result: 
                error_message = {"message": "Cannot post CXNU type of container."}
                return Response(json.dumps(error_message), status=400, mimetype='application/json')
            return soap_API_response(result)
        else:
            error_message = {"message": "please provide all required fields", "required fields": Constants.rake_write_required_fields}
            return Response(json.dumps(error_message), status=400, mimetype='application/json')
    
class GroundTruthData(View):
    @custom_exceptions
    # @api_auth_required
    def post(self):
        data = request.get_json()
        success,message = db_service.post_ground_truth_details(data)
        if success:
            return Response(json.dumps({"message":"Saved successfully"}), status=201, mimetype='application/json')
        else:
            return Response(json.dumps({"message":message}),status=400,mimetype='application/json')
    
    @custom_exceptions
    # @api_auth_required
    def get(self):
        train_number = request.args.get(Constants.TRAIN_NUMBER,None)
        trans_date = request.args.get(Constants.KEY_TRANS_DATE,None)
        trans_type = request.args.get(Constants.RAKE_TX_TYPE,"EXIM")
        if train_number and trans_date:
            response =  db_service.get_ground_truth_details(train_number,trans_date,trans_type)
            if response:
                # logger.info('Ground truth found for given train_number ',train_number, 'for trans_date ',trans_date)
                return Response(response, status=200, mimetype='application/json')
            else:
                # logger.info('Ground truth does not exist for given train_number ',train_number, 'for trans_date ',trans_date)
                return Response(json.dumps({"message":"No transaction found with given train_number and trans_date"}), status=204, mimetype='application/json')
        return Response(json.dumps({"message":"please provide train_number and trans_date to fetch details"}),status=400, mimetype='application/json')
    
    
    
class RakeContainer(View):
    @custom_exceptions
    # @api_auth_required
    def get(self):
        container_no = request.args.get(Constants.KEY_CN_NUMBER)
        rake_id = request.args.get(Constants.KEY_RAKE_ID,None)
        response = {}
        response =  db_service.get_container_data(rake_id,container_no)
        # print("response for the container_no",container_no,response)
        return Response(response, status=200, mimetype='application/json')

class RakeWagon(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        wagon_number = request.args.get(Constants.WAGON_NUMBER,None)
        rake_type = request.args.get(Constants.RAKE_TYPE,"AR")
        if(not wagon_number):
            message = "please provide query parameters"
            return Response(json.dumps({"message":message}), status=204,mimetype='application/json')
        if(rake_type not in ["AR","DE"]):
            message = "please provide proper Rake Type"
            return Response(json.dumps({"message":message}), status=204,mimetype='application/json')
        response = {}
        response =  db_service.get_wagon_data(wagon_number=wagon_number,rake_type=rake_type)
        # print("response for the container_no",wagon_number,response)
        return Response(response, status=200, mimetype='application/json')

class UpdateWTR(View):
    @custom_exceptions
    @api_auth_required
    def post(self):
        data = request.get_json()
        rake_type =  data.get(Constants.RAKE_TYPE,"DE")
        if(rake_type not in ["AR","DE"]):
            message = "please provide proper Rake Type"
            return Response(json.dumps({"message":message}), status=204,mimetype='application/json')
        if rake_type == "AR":
            db_service.update_inward_wtr_train_summ(data)
        else:
            db_service.update_outward_wtr_train_summ(data)
        return Response(json.dumps({"message":"Posted Successfully"}), status=200, mimetype='application/json')

class  WagonTypes(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        try:
            response =  db_service.get_wagon_types()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')


class  SlineCodes(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        try:
            response =  db_service.get_sline_codes()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  IcdLocations(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        try:
            response =  db_service.get_icd_locations()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  PodCodes(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        try:
            response =  db_service.get_pod_codes()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')
class  ContainerTypes(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        try:
            response =  db_service.get_container_types()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  CommodityCodes(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        try:
            response =  db_service.get_commodity_codes()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  CommodityTypes(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        try:
            response =  db_service.get_commodity_types()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  ActivityTypes(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        try:
            response =  db_service.get_activity_types()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')
class  PortCodes(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        try:
            response =  db_service.get_port_codes()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  OutLocation(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        try:
            response =  db_service.get_out_location_codes()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')
class  OutPortCodes(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        try:
            response =  db_service.get_out_port_codes()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  CargoTypes(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        try:
            response =  db_service.get_cargo_types()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  UserList(View):
    @custom_exceptions
    @api_auth_required
    def get(self):
        try:
            response =  db_service.get_user_list()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class TrackMasterDetails(View):
    @custom_exceptions
    @api_auth_required
    def post(self):
        data = request.get_json()
        if data:
            if master_db.create_track_master_details(data):
                return Response(json.dumps({"message":"success"}),status=200,mimetype='application/json')
        return Response(json.dumps({"message":"failed to save"}),status=400,mimetype='application/json')
    
    @custom_exceptions
    @api_auth_required
    def get(self):
        logger.info("GT, fetching   TrackMasterDetails")
        track_no = request.args.get(Constants.KEY_TRACK_NO,None)
        track_id = request.args.get(Constants.KEY_TRACK_ID,None)
        update_data ={}
        if track_no:
            update_data["track_no"] = track_no
        if track_id:
            update_data["track_id"] = track_id
        response = master_db.get_track_master_details(update_data)
        response = TrackMasterSchema(many=True).dump(response)
        if response:
            return Response(json.dumps(response),status=200,mimetype='application/json')
        else:   
            return Response(None,status=204,mimetype='application/json')
        
class CclsResponseData(View):
    @custom_exceptions
    # @api_auth_required
    def get(self):
        trans_type = request.args.get('trans_type',None)
        train_no = request.args.get('train_no',None)
        start_date_request = request.args.get('start_date',None)
        end_date_request = request.args.get('end_date',None)
        process_type = request.args.get('process_type','GT')

        if not (start_date_request and end_date_request) and train_no:
            if str(trans_type).upper() == 'EXIM':
                data = RakeInwardReadService.get_ctms_train_no_details(train_no=train_no)
            elif str(trans_type).upper() == 'DOM':
                data = DTMSRakeInwardReadService.get_dtms_train_no_details(train_no=train_no)
            else:
                return Response(json.dumps({'message':"trans_type not given or invalid"}),status=400,mimetype='application/json')
            if data:
                return Response(data,status=200,mimetype='application/json')
            return Response(status=204,mimetype='application/json')
        try:
            start_data = date.strftime(datetime.strptime(start_date_request, "%Y-%m-%d"), "%Y-%m-%d")
            end_data = date.strftime(datetime.strptime(end_date_request, "%Y-%m-%d"), "%Y-%m-%d")
        except:
            return Response(json.dumps({'message':"start time or end time format is invalid"}),status=400,mimetype='application/json')
        
        if not str(process_type).upper() in ['GT','CONCOR']:
            return Response(json.dumps({'message':"process_type invalid"}),status=400,mimetype='application/json')
            
        if str(process_type).upper() == 'GT':
            if str(trans_type).upper() == 'EXIM':
                data = RakeInwardReadService.ctms_details(start_date=start_data,end_date=end_data,train_no=train_no)
            elif str(trans_type).upper() == 'DOM':
                data = DTMSRakeInwardReadService.dtms_details(start_date=start_data,end_date=end_data,train_no=train_no)
            else:
                return Response(json.dumps({'message':"trans_type not given or invalid"}),status=400,mimetype='application/json')
        else:
            if str(trans_type).upper() == 'EXIM':
                soap_data = get_exim_train_details(train_number=train_no,from_date=start_data,to_date=end_data)
                soap_data = soap_data if soap_data else []
                data = RakeInwardReadService.save_in_db(soap_data)
                data =  RakeInwardReadService.format_cmts_data(data)
            elif str(trans_type).upper() == 'DOM':
                soap_data = get_domestic_train_details(train_number=train_no,from_date=start_data,to_date=end_data)
                soap_data = soap_data if soap_data else []
                data = DTMSRakeInwardReadService.save_in_db(soap_data)
                data = DTMSRakeInwardReadService.format_dtms_data(data)
            else:
                return Response(json.dumps({'message':"trans_type not given or invalid"}),status=400,mimetype='application/json')
        if data:
            return Response(data,status=200,mimetype='application/json')
        return Response(status=204,mimetype='application/json')

# class GtRangeData(View):
#     @custom_exceptions
#     # @api_auth_required
#     def get(self):
#         trans_type = request.args.get('trans_type',None)
#         start_date_request = request.args.get('start_date',None)
#         end_date_request = request.args.get('end_date',None)
#         try:
#             start_date_format = datetime.strptime(start_date_request, "%Y-%m-%d")
#             start_data = date.strftime(start_date_format, "%Y-%m-%d")
#             end_date_format = datetime.strptime(end_date_request, "%Y-%m-%d")
#             end_data = date.strftime(end_date_format, "%Y-%m-%d")
#         except:
#             return Response(json.dumps({'message':"start time or end time format is invalid"}),status=400)
#         if str(trans_type).upper() == 'EXIM':
#             data = RakeInwardReadService.get_ctms_details(start_date=start_data,end_date=end_data)
#         elif str(trans_type).upper() == 'DOM':
#             data = DTMSRakeInwardReadService.get_dtms_details(start_date=start_data,end_date=end_data)
#         else:
#             return Response(json.dumps({'message':"trans_type not given or invalid"}),status=400)
#         if data:
#             return Response(data,status=200)
#         return Response(status=204)
    

# class GtTrainData(View):
#     @custom_exceptions
#     # @api_auth_required
#     def get(self):
#         trans_type = request.args.get('trans_type',None)
#         train_no = request.args.get('train_no',None)
#         if train_no:
#             if str(trans_type).upper() == 'EXIM':
#                 data = RakeInwardReadService.get_ctms_train_no_details(train_no)
#             elif str(trans_type).upper() == 'DOM':
#                 data = DTMSRakeInwardReadService.get_dtms_train_no_details(train_no)
#             else:
#                 return Response(json.dumps({'message':"trans_type not given or invalid"}),status=400)
#             if data:
#                 return Response(data,status=200)
#         else:
#             return Response(json.dumps({'message':"train_no not given"}),status=400)
#         return Response(status=204)
