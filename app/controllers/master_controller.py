from flask_restful import Resource, reqparse
import config
import app.constants as Constants
from app.enums import PendencyType
from flask import json, Response,request
from app.logger import logger
from app.services.rake.rake_db_service import RakeDbService as db_service
from app.services.decorator_service import custom_exceptions, api_auth_required
from app.serializers.master_data_serializers import *
from app.services.master_db_service import MasterData as master_db
from app.controllers.utils import View, soap_API_response

class ContainerStatDetails(View):
    @custom_exceptions
    # @api_auth_required
    def post(self):
        data = request.get_json()
        if data:
            if master_db.create_container_stat_details(data):
                return Response(json.dumps({"message":"success"}),status=200,mimetype='application/json')
        return Response(json.dumps({"message":"failed to save"}),status=400,mimetype='application/json')
    
    @custom_exceptions
    @api_auth_required
    def get(self):
        logger.info("GT,fetch gateway port master data")
        response = master_db.get_container_stat_details()
        response = CtrStatMasterSchema(many=True).dump(response)
        if response:
            return Response(json.dumps(response),status=200,mimetype='application/json')
        else:
            return Response(None,status=204,mimetype='application/json')
        
class StationDetails(View):
    @custom_exceptions
    # @api_auth_required
    def post(self):
        data = request.get_json()
        if data:
            if master_db.create_station_details(data):
                return Response(json.dumps({"message":"success"}),status=200,mimetype='application/json')
        return Response(json.dumps({"message":"failed to save"}),status=400,mimetype='application/json')
    
    @custom_exceptions
    @api_auth_required
    def get(self):
        logger.info("GT,fetch station code master data")
        response = master_db.get_station_details()
        response = StationMasterSchema(many=True).dump(response)
        if response:
            return Response(json.dumps(response),status=200,mimetype='application/json')
        else:
            return Response(None,status=204,mimetype='application/json')