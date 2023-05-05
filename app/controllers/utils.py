from flask_restful import Resource, reqparse
from flask import json, Response,request
parser = reqparse.RequestParser()
from datetime import datetime


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


class View(Resource):

    def add_arguments_to_parser(self, args_list):
        for arg in args_list:
            parser.add_argument(arg)
        return parser.parse_args()
    

def convert_ccls_date_to_timestamp(ccls_date):
    ccls_date = int(round(ccls_date.timestamp()*1000))
    return ccls_date