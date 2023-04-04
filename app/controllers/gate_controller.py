from flask_restful import Resource, reqparse
import app.constants as Constants
from flask import json, Response,request
from app.services.decorator_service import custom_exceptions, api_auth_required
from app.services.gate.database_service import GateDbService, Iso6346CodeService
from app.logger import logger
parser = reqparse.RequestParser()
ContainerId = None


class Model(Resource):

    def add_arguments_to_parser(self, args_list):
        for arg in args_list:
            parser.add_argument(arg)
        return parser.parse_args()

class ContainerData(Model):
    @custom_exceptions
    # @api_auth_required
    def post(self):
        container_details = request.json
        try:
            if "records_count" in container_details:
                GateDbService.save_ctr_permit_records(container_details["records_count"])
            else:
                GateDbService.save_containers_data(container_details)
            logger.debug('Added data to the database')
            return Response(None, status=200, mimetype='application/json')
        except Exception as e:
            print(e)
        return Response(None, status=406, mimetype='application/json')
    
    
    @custom_exceptions
    # @api_auth_required
    def get(self):
        permit_number = str(request.args.get(Constants.KEY_PERMIT_NUMBER))
        logger.info('GT,Get request from the GATE service : {}'.format(permit_number))
        result = GateDbService().get_details_permit_number(permit_number)
        logger.info('Conainer details response: {}'.format(result))
        if result:
            return Response(result, status=200, mimetype='application/json')
        else:
            return Response(json.dumps({"status": "not found"}), status=404, mimetype='application/json')


    


class CclsData(Model):
    @custom_exceptions
    # @api_auth_required
    def get(self):
        permit_number = request.args.get(Constants.KEY_PERMIT_NUMBER,None)
        container_number = request.args.get(Constants.KEY_CN_NUMBER,None)
        crn_number = request.args.get(Constants.KEY_CRN_NUMBER,None)
        if permit_number is not None:
            logger.info('GT,Get request from the GATE service : {}'.format(permit_number))
            result = GateDbService().get_details_permit_number(permit_number)
            logger.info('GT,Get request from the GATE service - permit number: {}'.format(permit_number))
        elif container_number is not None:
            logger.info('GT,Get request from the GATE service : {}'.format(container_number))
            result = GateDbService().get_details_by_container_number(container_number)
            logger.info('GT,Get request from the GATE service - container number: {}'.format(container_number))
        else:
            logger.info('GT,Get request from the GATE service : {}'.format(crn_number))
            result = GateDbService().get_details_by_crn_number(crn_number)
            logger.info('GT,Get request from the GATE service - crn number: {}'.format(crn_number))
        
        logger.info('Conainer details response: {}'.format(result))
        return Response(result, status=200, mimetype='application/json')

class GateInModel(Model):
    @custom_exceptions
    @api_auth_required
    def get(self):
        container_number = request.args.get(Constants.KEY_CN_NUMBER,None)
        logger.info('GT, Update GATE In service : {}'.format(container_number))
        result = GateDbService().update_gateIn_info(container_number)
        logger.info('GT, Update GATE In service - permit number: {}'.format(container_number))
        logger.info('Conainer details response: {}'.format(result))
        return Response(result, status=200, mimetype='application/json')

class GateOutModel(Model):
    @custom_exceptions
    @api_auth_required
    def get(self):
        container_number = request.args.get(Constants.KEY_CN_NUMBER,None)
        result = GateDbService().update_gateOut_info(container_number)
        logger.info('GT, Update GATE In service - container number: {}'.format(container_number))
        logger.info('Conainer details response: {}'.format(result))
        return Response(result, status=200, mimetype='application/json')

class UpdateContainerDetails(Model):
    @custom_exceptions
    # @api_auth_required
    def post(self):
        data = json.loads(request.data)
        # logger.info('ContainerInfo, Get Container details service : {}'.format(data['container_number']))
        result = GateDbService().update_container_info(data)
        if result:
            logger.info('Conainer details response: {}'.format(result))
            return Response(json.dumps({"message":"success"}), status=200, mimetype='application/json')
        else:
            return Response(json.dumps({"message":"No permit found"}), status=400, mimetype='application/json')

class UpdateCtrStackDetails(Model):
    @custom_exceptions
    # @api_auth_required
    def post(self):
        data = request.data
        logger.info('ContainerInfo, Get Container Stack Location details service : {}'.format(data['container_number']))
        result = GateDbService().update_ctr_stack_info(data)
        logger.info('Conainer Stack Location  details response: {}'.format(result))
        return Response(result, status=200, mimetype='application/json')

class ISO6346Data(Model):
    @custom_exceptions
    @api_auth_required
    def get(self):
        iso_code = request.args.get(Constants.KEY_ISO_CODE,None)
        if(iso_code):
            result = Iso6346CodeService().validate(iso_code.upper(),Constants.KEY_RETRY_COUNT)
            return Response(result, status=200, mimetype='application/json')
        return Response(json.dumps({"message":"please provide ISO Code"}), status=404, mimetype='application/json')
