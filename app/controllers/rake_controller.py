from flask_restful import Resource, reqparse
import config
import app.constants as Constants
from flask import json, Response,request
from app.services.decorator_service import custom_exceptions
from app.services.database_service import GateDbService as db_service
from app.logger import logger
from app.services.rake_db_service import RakeDbService as db_service
from app.services.decorator_service import custom_exceptions, jwt_auth_required
from app.constants import GroundTruthType
from datetime import date, datetime
parser = reqparse.RequestParser()


def soap_API_response(result):
    if result:
        if 'Error' in result:
            if result['Error']:
                return Response(json.dumps({"message":"Failed to save record","error":str(result["Error"]),"error_message":str(result['ErrorMessage'])}), status=400, mimetype='application/json')
            else:        
                return Response(json.dumps({"message":str(result["Result"])}), status=200, mimetype='application/json')                                
        else:
            return Response(json.dumps(result), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({"message":"Unable to save transaction"}), status=400, mimetype='application/json')

class Model(Resource):

    def add_arguments_to_parser(self, args_list):
        for arg in args_list:
            parser.add_argument(arg)
        return parser.parse_args()

class TrainDetails(Model):
    @custom_exceptions
    def get(self):
        train_number = request.args.get(Constants.TRAIN_NUMBER,None)
        track_number = request.args.get(Constants.TRACK_NUMBER,None)
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
        result = db_service.get_train_details(data,track_number,from_date=from_date,to_date=to_date)
        logger.info('Conainer details response')
        return Response(result, status=200, mimetype='application/json')

class TrackDetails(Model):
    @custom_exceptions
    def get(self):
        train_number = request.args.get(Constants.TRAIN_NUMBER,None)
        track_number = request.args.get(Constants.TRACK_NUMBER,None)
        trans_date = request.args.get(Constants.KEY_TRANS_DATE,None)
        data = {}
        if train_number:
            data["train_no"]=train_number
        if track_number:
            data["track_no"]=track_number
        if trans_date:
            data["trans_date"] = datetime.strptime(trans_date, '%Y-%m-%d %H:%M:%S').date()
            
        logger.info('GT,Get request from the Rake service')
        result = db_service.get_track_details(data)
        logger.info('Track details response')
        return Response(result, status=200, mimetype='application/json')
    
    def post(self):
        data = request.get_json()
        success,message = db_service.post_track_details(data)
        if success:
            return Response(json.dumps({"message":"Saved successfully"}), status=201, mimetype='application/json')
        else:
            return Response(json.dumps({"message":message}),status=400,mimetype='application/json')

class RakeData(Model):
    @custom_exceptions
    # @jwt_auth_required
    def post(self):
        if config.GROUND_TRUTH == GroundTruthType.ORACLE.value:
            db_service.push_test_data_arrival()
            db_service.push_test_data_departure() 
        return Response(None, status=200, mimetype='application/json')


    @custom_exceptions
    # @jwt_auth_required 
    def get(self):
        rake_number = request.args.get(Constants.RAKE_NUMBER,None)
        track_number = request.args.get(Constants.TRACK_NUMBER,None)
        rake_type = request.args.get(Constants.RAKE_TYPE,"AR")
        if not rake_number and not track_number:
            message = "please provide query parameters"
            return Response(json.dumps({"message":message}), status=204,mimetype='application/json')
        logger.info('GT,Get request from the Rake service : {} {}'.format(rake_number,track_number))
        success,result = db_service.get_rake_details(rake_number=rake_number,track_number=track_number,rake_type=rake_type)
        if success:
            logger.info('Conainer details response')
            print(result)
            return Response(result, status=200, mimetype='application/json')
        else:
            return Response(json.dumps({"message":result}), status=400, mimetype='application/json')

class UpdateInwardRakeDetails(Model):
    @custom_exceptions
    def post(self):
        data = request.get_json()
        result = {}
        result =  db_service.update_inward_rake_details(data)
        return soap_API_response(result)


class UpdateOutwardRakeDetails(Model):
    @custom_exceptions
    def post(self):
        data = request.get_json()
        result = {}
        result =  db_service.update_inward_rake_details(data)
        return soap_API_response(result)
    
class GroundTruthData(Model):
    @custom_exceptions
    def post(self):
        data = request.get_json()
        success,message = db_service.post_ground_truth_details(data)
        if success:
            return Response(json.dumps({"message":"Saved successfully"}), status=201, mimetype='application/json')
        else:
            return Response(json.dumps({"message":message}),status=400,mimetype='application/json')
    
    @custom_exceptions
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
    
    
    
class RakeContainer(Model):
    @custom_exceptions
    # @jwt_auth_required 
    def get(self):
        container_no = request.args.get(Constants.KEY_CN_NUMBER)
        response = {}
        response =  db_service.get_container_data(container_no)
        # print("response for the container_no",container_no,response)
        return Response(response, status=200, mimetype='application/json')

class RakeWagon(Model):
    @custom_exceptions
    # @jwt_auth_required
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

class UpdateWTR(Model):
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

class  WagonTypes(Model):
    def get(self):
        try:
            response =  db_service.get_wagon_types()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')


class  SlineCodes(Model):
    def get(self):
        try:
            response =  db_service.get_sline_codes()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  IcdLocations(Model):
    def get(self):
        try:
            response =  db_service.get_icd_locations()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  PodCodes(Model):
    def get(self):
        try:
            response =  db_service.get_pod_codes()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')
class  ContainerTypes(Model):
    def get(self):
        try:
            response =  db_service.get_container_types()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  CommodityCodes(Model):
    def get(self):
        try:
            response =  db_service.get_commodity_codes()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  CommodityTypes(Model):
    def get(self):
        try:
            response =  db_service.get_commodity_types()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  ActivityTypes(Model):
    def get(self):
        try:
            response =  db_service.get_activity_types()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')
class  PortCodes(Model):
    def get(self):
        try:
            response =  db_service.get_port_codes()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  OutLocation(Model):
    def get(self):
        try:
            response =  db_service.get_out_location_codes()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')
class  OutPortCodes(Model):
    def get(self):
        try:
            response =  db_service.get_out_port_codes()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  CargoTypes(Model):
    def get(self):
        try:
            response =  db_service.get_cargo_types()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')

class  UserList(Model):
    def get(self):
        try:
            response =  db_service.get_user_list()
            return Response(response, status=200, mimetype='application/json')
        except:
            return Response("No Data Found", status=400, mimetype='application/json')
