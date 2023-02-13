from flask_restful import Resource, reqparse
from flask import json, Response,request
from app.services.decorator_service import custom_exceptions
from app.services.warehouse_db_service import WarehouseDbService as db_service
# from app.services.warehouse_db_service import Key_Mapping
from app.logger import logger
parser = reqparse.RequestParser()

class Model(Resource):

    def add_arguments_to_parser(self, args_list):
        for arg in args_list:
            parser.add_argument(arg)
        return parser.parse_args()

class WarehouseData(Model):
    @custom_exceptions
    def post(self):
        print("got warehouse post request===")
        file = request.files['file']
        warehouse_data = db_service().get_warehouse_file_data(file)
        db_service().get_warehouse_details(warehouse_data)
        return Response(None, status=200, mimetype='application/json')

    def get(self):
        print("request args ::", request.args, request.args.get('job_order') )
        job_order = request.args.get('job_order')
        logger.info('GT,Get request from the Warehouse service : {}'.format(job_order))
        result = db_service.get_warehouse_details(self, job_order)
        if result:
            logger.info('response: {}'.format(result))
            return Response(json.dumps(result), status=200, mimetype='application/json')
        else:
            return Response(None, status=404, mimetype='application/json')
