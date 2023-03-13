from flask_restful import Resource, reqparse
from flask import json, Response,request
from app.services.decorator_service import custom_exceptions
# from app.services.warehouse_db_service import WarehouseDbService as db_service
# from app.services.warehouse_db_service import Key_Mapping
from app.logger import logger
from app.services.warehouse.wh_job_view import WarehouseJobView
from app.services.warehouse.wh_tallysheet import WarehouseTallySheetView


parser = reqparse.RequestParser()

class View(Resource):

    def add_arguments_to_parser(self, args_list):
        for arg in args_list:
            parser.add_argument(arg)
        return parser.parse_args()

class JobDetails(View):
    def get(self):
        print("request args ::", request.args, request.args.get('job_order') )
        job_order = request.args.get('request_parameter')
        job_type = int(request.args.get('res_job_type',0))
        container_flag = int(request.args.get('container_flag',0))
        logger.info('GT,Get request from the Warehouse service : {}'.format(job_order,job_type,container_flag))
        result = WarehouseJobView().get_job_details(job_order,job_type,container_flag)#db_service.get_warehouse_details(self, job_order)
        if result:
            logger.info('response: {}'.format(result))
            return Response(json.dumps(result), status=200, mimetype='application/json')
        else:
            return Response(None, status=404, mimetype='application/json')
        
    def post(self):
        tally_sheet_data=request.json
        return Response(json.dumps({"message":"tallysheet uploaded successfully"}), status=200, mimetype='application/json')

class WarehouseTallySheet(View):
    def get(self):
        result = WarehouseTallySheetView().get_tally_sheet_info(request)
        return Response(json.dumps(result), status=200, mimetype='application/json')

    def post(self):
        # try:
        tally_sheet_data=request.json
        WarehouseTallySheetView().process_tally_sheet_info(tally_sheet_data)
        return Response(json.dumps({"message":"tallysheet created successfully"}), status=200, mimetype='application/json')
        # except Exception as e:
        #     logger.error(e)
        #     return Response({}, status=400, mimetype='application/json')

    def put(self):
        tally_sheet_data=request.json
        WarehouseTallySheetView().process_tally_sheet_info(tally_sheet_data)
        return Response(json.dumps({"message":"tallysheet updated successfully"}), status=200, mimetype='application/json')
