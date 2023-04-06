from flask_restful import Resource, reqparse
import config
import app.constants as Constants
from flask import json, Response,request
from app.logger import logger
from app.services.rake.rake_db_service import RakeDbService as db_service
from app.services.decorator_service import custom_exceptions, api_auth_required
from app.constants import GroundTruthType
from app.serializers.master_data_serializers import *
from app.services.rake.rake_inward_write import RakeInwardWriteService
from app.services.rake.rake_outward_write import RakeOutwardWriteService
from app.services.rake.rake_inward_read import RakeInwardReadService
from app.services.rake.rake_outward_plan import RakeOutwardPlanService
from datetime import date, datetime
from app.controllers.utils import View, soap_API_response


class TrainDetails(View):   
    @custom_exceptions
    # @api_auth_required
    def get(self):
        train_number = request.args.get(Constants.TRAIN_NUMBER,None)
        track_number = request.args.get(Constants.TRACK_NUMBER,None)
        rake_id = request.args.get(Constants.RAKE_ID,None)
        rake_type = request.args.get(Constants.RAKE_TYPE,"AR")
        wagon_number = request.args.get(Constants.WAGON_NUMBER,None)
        container_number = request.args.get(Constants.KEY_CN_NUMBER,None)
        container_life_number = request.args.get(Constants.KEY_CN_LIFE_NUMBER,None)
        trans_date = request.args.get(Constants.KEY_TRANS_DATE,None)
        from_date = request.args.get(Constants.KEY_FROM_DATE,None)
        to_date = request.args.get(Constants.KEY_TO_DATE,None)
        data = {}
        if train_number:
            data["train_number"]=train_number
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
        logger.info('GT,Get request from the Rake service : {}'.format(train_number))
        result = {}
        if rake_type == "AR":
            result = RakeInwardReadService.get_train_details(data,rake_id,track_number,from_date=from_date,to_date=to_date)
        elif rake_type == "DE":
            result = RakeOutwardPlanService.get_rake_plan(rake_id,train_number,track_number)
        else:
            return Response({"mesaage":"unknown rake type"}, status=400, mimetype='application/json')
        logger.info('Conainer details response')
        return Response(result, status=200, mimetype='application/json')


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
        result = RakeInwardReadService.get_train_details(data)
        logger.info('Conainer details response')
        return Response(result, status=200, mimetype='application/json')

class PendancyList(View):
    @custom_exceptions
    # @api_auth_required
    def get(self):
        gateway_port = request.args.get(Constants.KEY_GATEWAY_PORT,None)
        if gateway_port:
            gateway_ports= gateway_port.split(",")
            logger.info("GT, pendacy list for port"+str(gateway_ports))
            response = db_service.get_pendancy_list(gateway_ports)
            # response = self.format_data(response,gateway_ports)
            return Response(response, status=200, mimetype='application/json')
        else:
            return Response(json.dumps({"message":"please provide gateway_port"}), status=400, mimetype='application/json')
    
    
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
        logger.info("GT,fetch wagon master data",wagon_number)
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
    @custom_exceptions
    @api_auth_required
    def post(self):
        data = request.get_json()
        if set(Constants.rake_write_required_fields).issubset(set(data.keys())):
            result = {}
            result =  RakeOutwardWriteService.update_outward_train_summary(data)
            return soap_API_response(result)
        else:
            return Response(json.dumps({"message":"please provide all required fields", "required fields" :Constants.rake_write_required_fields}), status=400, mimetype='application/json')
    
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
        if train_number and trans_date:
            response =  db_service.get_ground_truth_details(train_number,trans_date)
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
        response = {}
        response =  db_service.get_container_data(container_no)
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
