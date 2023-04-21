from flask_restful import Resource, reqparse
from flask import json, Response,request
from app.services.decorator_service import custom_exceptions
# from app.services.warehouse_db_service import WarehouseDbService as db_service
# from app.services.warehouse_db_service import Key_Mapping
from app.logger import logger
from app.services.warehouse.wh_job_view import WarehouseJobView
from app.services.warehouse.wh_tallysheet import WarehouseTallySheetView
from app.services.warehouse.wh_commodity import WarehouseCommodityView
from app.services.warehouse.wh_upload_tallysheet import WarehouseUploadTallySheetView
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

parser = reqparse.RequestParser()

class View(Resource):

    def add_arguments_to_parser(self, args_list):
        for arg in args_list:
            parser.add_argument(arg)
        return parser.parse_args()

class JobDetails(View):
    def get(self):
        try:
            job_order = request.args.get('request_parameter')
            job_type = int(request.args.get('res_job_type',0))
            container_flag = int(request.args.get('container_flag',0))
            logger.info("{},{}:{}".format("GTService: Get request from the ctms for getting cargo job data" ,"job_order",request.args.get('request_parameter')))
            result = WarehouseJobView().get_job_details(job_order,job_type,container_flag)#db_service.get_warehouse_details(self, job_order)
            return Response(json.dumps(result), status=200, mimetype='application/json')
        except SQLAlchemyError as e:
            logger.exception("{},{},{}:{}".format("GTService: getting error while perform operation on database", str(e),"job_order",request.args.get('request_parameter')))
            return Response(json.dumps({"message":"GTService: getting error while perform operation on database"}), status=500, mimetype='application/json')
        except Exception as e:
            logger.exception("{},{}:{}".format(str(e),"job_order",request.args.get('request_parameter')))
            return Response(json.dumps({"message":str(e)}), status=500, mimetype='application/json')
        
    def post(self):
        try:
            request_data=request.json
            logger.info("{},{}:{}".format("GTService: Get request from the ctms for upload tallysheet" ,"job_order",request_data.get('request_parameter')))
            WarehouseUploadTallySheetView().upload_tallysheet(request_data)
            logger.info("{},{}:{}".format("GTService: tallysheet uploaded successfully" ,"job_order",request_data.get('request_parameter')))
            return Response(json.dumps({"message":"tallysheet uploaded successfully"}), status=200, mimetype='application/json')
        except SQLAlchemyError as e:
            logger.exception("{},{},{}:{}".format("GTService: getting error while perform operation on database", str(e),"job_order",request_data.get('request_parameter')))
            return Response(json.dumps({"message":"GTService: getting error while perform operation on database"}), status=500, mimetype='application/json')
        except Exception as e:
            logger.exception("{},{}:{}".format(str(e),"job_order",request_data.get('request_parameter')))
            return Response(json.dumps({"message":str(e)}), status=500, mimetype='application/json')
        
        
class WarehouseTallySheet(View):
    def get(self):
        try:
            result = WarehouseTallySheetView().get_tally_sheet_info(request)
            logger.info("{},{}:{}".format("GTService: Get request from ctms to view tallysheet" ,"job_order",request.args.get('request_parameter')))
            if not result:
                logger.exception("{},{}:{}".format("GTService: tallysheet doesn't exists in groundtruth database" ,"job_order",request.args.get('request_parameter')))
                return Response(json.dumps({"message":"GTService: job data not found in ccls system"}), status=204, mimetype='application/json')
            logger.info("{},{},{}:{}".format("GTService: get tallysheet info successfully",result,"job_order",request.args.get('request_parameter')))
            return Response(json.dumps(result), status=200, mimetype='application/json')
        except SQLAlchemyError as e:
            logger.exception("{},{},{}:{}".format("GTService: getting error while perform operation on database", str(e),"job_order",request.args.get('request_parameter')))
            return Response(json.dumps({"message":"GTService: getting error while perform operation on database"}), status=500, mimetype='application/json')
        except Exception as e:
            logger.exception("{},{}:{}".format(str(e),"job_order",request.args.get('request_parameter')))
            return Response(json.dumps({"message":str(e)}), status=500, mimetype='application/json')

    def post(self):
        try:
            tally_sheet_data=request.json
            request_parameter = tally_sheet_data.get('crn_number') if tally_sheet_data.get('crn_number') else tally_sheet_data.get('cargo_carting_number') if  tally_sheet_data.get('cargo_carting_number') else tally_sheet_data.get('container_number') if tally_sheet_data.get('container_number') else tally_sheet_data.get('gpm_number') if tally_sheet_data.get('gpm_number') else None
            logger.info("{},{}:{}".format("GTService:  Get request from ctms to generate tallysheet with this data" ,"job_order",request_parameter))
            WarehouseTallySheetView().process_tally_sheet_info(tally_sheet_data)
            logger.info("{},{}:{}".format("GTService:  tallysheet generated successfully" ,"job_order",request_parameter))
            return Response(json.dumps({"message":"GTService: tallysheet generated successfully"}), status=200, mimetype='application/json')
        except SQLAlchemyError as e:
            logger.exception("{},{},{}:{}".format("GTService: getting error while perform operation on database", str(e),"job_order",request_parameter))
            return Response(json.dumps({"message":"GTService: getting error while perform operation on database"}), status=500, mimetype='application/json')
        except Exception as e:
            logger.exception("{},{}:{}".format(str(e),"job_order",request_parameter))
            return Response(json.dumps({"message":str(e)}), status=500, mimetype='application/json')

    def put(self):
        try:
            tally_sheet_data=request.json
            request_parameter = tally_sheet_data.get('crn_number') if tally_sheet_data.get('crn_number') else tally_sheet_data.get('cargo_carting_number') if  tally_sheet_data.get('cargo_carting_number') else tally_sheet_data.get('container_number') if tally_sheet_data.get('container_number') else tally_sheet_data.get('gpm_number') if tally_sheet_data.get('gpm_number') else None
            logger.info("{},{}:{}".format("GTService:  Get request from ctms to update tallysheet with this data" ,"job_order",request_parameter))
            WarehouseTallySheetView().process_tally_sheet_info(tally_sheet_data)
            logger.info("{},{}:{}".format("GTService:  tallysheet updated successfully" ,"job_order",request_parameter))
            return Response(json.dumps({"message":"GTService: tallysheet updated successfully"}), status=200, mimetype='application/json')
        except SQLAlchemyError as e:
            logger.exception("{},{},{}:{}".format("GTService: getting error while perform operation on database", str(e),"job_order",request_parameter))
            return Response(json.dumps({"message":"GTService: getting error while perform operation on database"}), status=500, mimetype='application/json')
        except Exception as e:
            logger.exception("{},{}:{}".format(str(e),"job_order",request_parameter))
            return Response(json.dumps({"message":str(e)}), status=500, mimetype='application/json')
    
class WarehouseCommodities(View):
    def get(self):
        try:
            logger.info('GT,Get request from the ctms service to fetch commodities')
            result=WarehouseCommodityView().get_commodity_details()
            if not result:
                logger.exception("GTService: commodities doesn't exists in db")
                return Response(json.dumps({"message":"GTService: commodities doesn't exists in db"}), status=204, mimetype='application/json')
            logger.info('response: {}'.format(result))
            return Response(json.dumps(result), status=200, mimetype='application/json')
        except SQLAlchemyError as e:
            logger.exception('GTService: getting error while perform operation on database %s',e)
            return Response(json.dumps({"message":"GTService: getting error while perform operation on database"}), status=500, mimetype='application/json')
        except Exception as e:
            logger.exception('%s',e)
            return Response(json.dumps({"message":str(e)}), status=500, mimetype='application/json')

    def post(self):
        try:
            logger.info('GT,Get request from  to upload commodities')
            file = request.files['file']
            if not file:
                return "No file"
            df = pd.read_csv(file, encoding='unicode_escape')
            commodity_data = json.loads(df.to_json(orient="records"))
            WarehouseCommodityView().process_commodity_details(commodity_data)
            return Response(json.dumps({"message":"commodities uploaded successfully"}), status=200, mimetype='application/json')
        except SQLAlchemyError as e:
            logger.exception('GTService: getting error while perform operation on database %s',e)
            return Response(json.dumps({"message":"GTService: getting error while perform operation on database"}), status=500, mimetype='application/json')
        except Exception as e:
            logger.exception('%s',e)
            return Response(json.dumps({"message":str(e)}), status=500, mimetype='application/json')


