import app.constants as Constants
from app.services.database_service import YardDbService
from flask import json, Response,request
from app.logger import logger

# this is a common function to retrieve master data from CCLS tables
def get_master_data_common(name):
    sql_filename = None
    if name == 'container_size':
        sql_filename = "get_ctr_size.sql"
    elif name == 'sline_codes':
        sql_filename = "get_sline_codes.sql"
    elif name == 'container_types':
        sql_filename = "get_ctr_types.sql"
    elif name == 'pods':
        sql_filename = "get_pods.sql"
    elif name == 'icd_names':
        sql_filename = "get_icd_names.sql"
    elif name == 'stack_layout':
        sql_filename = "get_stack_layout.sql"
    elif name == 'container_details':
        sql_filename = "get_ctr_details.sql"
    elif name == 'activity_codes':
        sql_filename = "get_activity_codes.sql"
    elif name == 'equipments':
        sql_filename = "get_equipments.sql"
    if not sql_filename:
        logger.debug('There is no such table exists')
        return Response(status=409)
    result = YardDbService().get_master_data(sql_filename)
    return Response(result, status=200, mimetype='application/json')