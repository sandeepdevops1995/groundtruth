from app.services.warehouse.wh_revenue import RevenueView
from flask_restful import Resource, reqparse
from flask import json, Response,request
from app.logger import logger
from app.services.warehouse.wh_job_view import WarehouseJobView
from app.services.warehouse.wh_tallysheet import WarehouseTallySheetView
from app.services.warehouse.wh_commodity import WarehouseCommodityView
from app.services.warehouse.wh_upload_tallysheet import WarehouseUploadTallySheetView
import pandas as pd
import app.logging_message as LM
from app.services.warehouse.wh_exception_handler import custom_exceptions
from datetime import datetime

parser = reqparse.RequestParser()

class View(Resource):

    def add_arguments_to_parser(self, args_list):
        for arg in args_list:
            parser.add_argument(arg)
        return parser.parse_args()


class JobDetails(View):

    @custom_exceptions(LM.KEY_GET_JOB_ORDER_DATA)
    def get(self):
        job_order = request.args.get('request_parameter')
        job_type = int(request.args.get('res_job_type',0))
        container_flag = int(request.args.get('container_flag',0))
        logger.debug("{}, {}, {}, {}, {}, {}, {}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_GET_REQUEST_FROM_CTMS_FOR_FETCH_CARGO_DETAILS,'JT_'+str(job_type),job_order,request.args))
        result = WarehouseJobView().get_job_details(job_order,job_type,container_flag)
        logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GET_JOB_ORDER_DATA,LM.KEY_FETCH_JOB_ORDER_DATA_SUCCESS,'JT_'+str(job_type),job_order,result))
        return Response(json.dumps(result), status=200, mimetype='application/json')
    
    @custom_exceptions(LM.KEY_UPLOAD_TALLYSHEET)
    def post(self):
        request_data=request.json
        logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_GET_REQUEST_FROM_CTMS_FOR_UPLOAD_TALLYSHEET,'JT_'+str(request_data.get('job_type')),request_data.get('request_parameter')))
        uploaded_trucks,status = WarehouseUploadTallySheetView().upload_tallysheet(request_data)
        logger.info("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_TALLYSHEET,LM.KEY_TALLYSHEET_DATA_UPLOADED,'JT_'+str(request_data.get('job_type')),request_data.get('request_parameter'),uploaded_trucks))
        return Response(json.dumps({"message":"tallysheet uploaded successfully",'uploaded_trucks':uploaded_trucks}), status=status, mimetype='application/json')
        
        
class WarehouseTallySheet(View):

    @custom_exceptions(LM.KEY_VIEW_TALLYSHEET)
    def get(self):
        logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_VIEW_TALLYSHEET,LM.KEY_GET_REQUEST_FROM_CTMS_FOR_VIEW_TALLYSHEET,'JT_'+str(request.args.get('job_type')),request.args.get('request_parameter')))
        result = WarehouseTallySheetView().get_tally_sheet_info(request)
        if not result:
            logger.exception("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_VIEW_TALLYSHEET,LM.KEY_TALLYSHEET_DOES_NOT_EXISTS,'JT_'+str(request.args.get('job_type')),request.args.get('request_parameter')))
            return Response(None, status=204, mimetype='application/json')
        logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_VIEW_TALLYSHEET,LM.KEY_FETCH_TALLYSHEET_DATA,'JT_'+str(request.args.get('job_type')),request.args.get('request_parameter')))
        return Response(json.dumps(result), status=200, mimetype='application/json')
        
    @custom_exceptions(LM.KEY_GENERATE_TALLYSHEET)
    def post(self):
        tally_sheet_data=request.json
        request_parameter = tally_sheet_data.get('crn_number') if tally_sheet_data.get('crn_number') else tally_sheet_data.get('cargo_carting_number') if  tally_sheet_data.get('cargo_carting_number') else tally_sheet_data.get('container_number') if tally_sheet_data.get('container_number') else tally_sheet_data.get('gpm_number') if tally_sheet_data.get('gpm_number') else None
        logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GENERATE_TALLYSHEET,LM.KEY_GET_REQUEST_FROM_CTMS_FOR_GENERATE_TALLYSHEET,'JT_'+str(tally_sheet_data.get('job_type')),request_parameter,tally_sheet_data))
        WarehouseTallySheetView().generate_tally_sheet_info(tally_sheet_data)
        logger.info("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_GENERATE_TALLYSHEET,LM.KEY_TALLYSHEET_DATA_CREATED,'JT_'+str(tally_sheet_data.get('job_type')),request_parameter))
        return Response(json.dumps({"message":"GTService: tallysheet generated successfully"}), status=200, mimetype='application/json')
        
    @custom_exceptions(LM.KEY_UPDATE_TALLYSHEET)
    def put(self):
        tally_sheet_data=request.json
        request_parameter = tally_sheet_data.get('crn_number') if tally_sheet_data.get('crn_number') else tally_sheet_data.get('cargo_carting_number') if  tally_sheet_data.get('cargo_carting_number') else tally_sheet_data.get('container_number') if tally_sheet_data.get('container_number') else tally_sheet_data.get('gpm_number') if tally_sheet_data.get('gpm_number') else None
        logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPDATE_TALLYSHEET,LM.KEY_GET_REQUEST_FROM_CTMS_FOR_UPDATE_TALLYSHEET,'JT_'+str(tally_sheet_data.get('job_type')),request_parameter,tally_sheet_data))
        WarehouseTallySheetView().update_tally_sheet_info(tally_sheet_data)
        logger.info("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPDATE_TALLYSHEET,LM.KEY_TALLYSHEET_DATA_UPDATED,'JT_'+str(tally_sheet_data.get('job_type')),request_parameter,tally_sheet_data))
        return Response(json.dumps({"message":"GTService: tallysheet updated successfully"}), status=200, mimetype='application/json')
    
class WarehouseCommodities(View):

    @custom_exceptions(LM.KEY_FETCH_COMMODITIES)
    def get(self):
        logger.debug("{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_FETCH_COMMODITIES,LM.KEY_GET_REQUEST_FROM_CTMS_FOR_COMMODITIES))
        result=WarehouseCommodityView().get_commodity_details()
        if not result:
            logger.exception("{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_FETCH_COMMODITIES,LM.KEY_COMMODITIES_DOES_NOT_EXISTS))
            return Response(None, status=204, mimetype='application/json')
        logger.info("{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_FETCH_COMMODITIES,LM.KEY_GET_COMMODITIES_SUCCESS))
        return Response(json.dumps(result), status=200, mimetype='application/json')
    
    @custom_exceptions(LM.KEY_UPLOAD_COMMODITIES)
    def post(self):
        logger.debug("{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_COMMODITIES,LM.KEY_GET_REQUEST_FROM_CTMS_FOR_UPLOAD_COMMODITIES))
        file = request.files['file']
        if not file:
            return "No file"
        df = pd.read_csv(file, encoding='unicode_escape')
        commodity_data = json.loads(df.to_json(orient="records"))
        WarehouseCommodityView().process_commodity_details(commodity_data)
        logger.debug("{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_UPLOAD_COMMODITIES,LM.KEY_UPLOAD_COMMODITIES_SUCCESS))
        return Response(json.dumps({"message":"commodities uploaded successfully"}), status=200, mimetype='application/json')
        

class WarehousePrintTallySheet(View):

    @custom_exceptions(LM.KEY_PRINT_TALLYSHEET)
    def get(self):
        logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_PRINT_TALLYSHEET,LM.KEY_GET_REQUEST_FROM_CTMS_FOR_PRINT_TALLYSHEET,'JT_'+str(request.args.get('job_type')),request.args.get('request_parameter')))
        result = WarehouseTallySheetView().print_tally_sheet(request)
        if not result:
            logger.exception("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_PRINT_TALLYSHEET,LM.KEY_TALLYSHEET_DOES_NOT_EXISTS,'JT_'+str(request.args.get('job_type')),request.args.get('request_parameter')))
            return Response(None, status=204, mimetype='application/json')
        logger.debug("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_PRINT_TALLYSHEET,LM.KEY_FETCH_PRINT_TALLYSHEET_DATA,'JT_'+str(request.args.get('job_type')),request.args.get('request_parameter')))
        return Response(json.dumps(result), status=200, mimetype='application/json')
    

class WarehouseRevenue(View):

    @custom_exceptions(LM.KEY_WAREHOUSE_REVENUE)
    def get(self):
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        type = request.args.get('type')
        logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_WAREHOUSE_REVENUE,LM.KEY_GET_REQUEST_FROM_CTMS_FOR_WAREHOUSE_REVENUE,from_date,to_date,type))
        result = RevenueView().get_revenue_details(from_date,to_date,type)
        if not result:
            logger.exception("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_WAREHOUSE_REVENUE,LM.KEY_WAREHOUSE_REVENUE_DOES_NOT_EXISTS,from_date,to_date,type))
            return Response(None, status=204, mimetype='application/json')
        logger.debug("{},{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_WAREHOUSE_REVENUE,LM.KEY_FETCH_WAREHOUSE_REVENUE_DATA,from_date,to_date,type))
        return Response(json.dumps(result), status=200, mimetype='application/json')
    

class GetRevenueInfo(View):

    @custom_exceptions(LM.KEY_WAREHOUSE_REVENUE)
    def get(self):
        logger.debug("{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_WAREHOUSE_REVENUE,LM.KEY_GET_REQUEST_FROM_CTMS_FOR_WAREHOUSE_REVENUE,request))
        result = RevenueView().get_revenue_amount(request)
        if not result:
            logger.exception("{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_WAREHOUSE_REVENUE,LM.KEY_WAREHOUSE_REVENUE_DOES_NOT_EXISTS,request))
            return Response(None, status=204, mimetype='application/json')
        logger.debug("{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,LM.KEY_WAREHOUSE_REVENUE,LM.KEY_FETCH_WAREHOUSE_REVENUE_DATA,request))
        return Response(json.dumps(result), status=200, mimetype='application/json')



