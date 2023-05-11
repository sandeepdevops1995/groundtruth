from sqlalchemy.exc import SQLAlchemyError
from app.user_defined_exception import DataNotFoundException
import app.logging_message as LM
from app.logger import logger
from flask import json, Response,request
import app.services.warehouse.constants as Constants

def get_job_order_and_job_type(request):
    if request.method=='GET':
        job_order = request.args.get('request_parameter')
        job_type = request.args.get('res_job_type') if 'res_job_type' in request.args else request.args.get('job_type') if 'job_type' in request.args else None
    else:
        request_data=request.json
        job_order = request_data.get('request_parameter') if 'request_parameter' in request_data else request_data.get('crn_number') if request_data.get('crn_number') else request_data.get('cargo_carting_number') if  request_data.get('cargo_carting_number') else request_data.get('container_number') if request_data.get('container_number') else request_data.get('gpm_number') if request_data.get('gpm_number') else None
        job_type = request_data.get('job_type')
    job_type = 'JT_'+str(job_type) if job_type else None
    return job_order,job_type


#Error handling decorator
def custom_exceptions(event):
    def decorator(func):
        def new_func(*args, **kwargs):
            job_order,job_type = get_job_order_and_job_type(request)
            try:
                return func(*args, **kwargs)
            except ConnectionError as e:
                logger.exception("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,event,str(e),job_type,job_order))
                return Response(json.dumps({"message":Constants.WH_COMMON_EXCEPTION_MESSAGE}), status=500, mimetype='application/json')
            except SQLAlchemyError as e:
                logger.exception("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,event,str(e),job_type,job_order))
                return Response(json.dumps({"message":Constants.WH_COMMON_EXCEPTION_MESSAGE}), status=500, mimetype='application/json')
            except DataNotFoundException as e:
                logger.exception("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,event,str(e),job_type,job_order))
                return Response(json.dumps({"message":Constants.WH_CCLS_JOB_ORDER_NOT_FOUND}), status=404, mimetype='application/json')
            except Exception as e:
                logger.exception("{},{},{},{},{},{}".format(LM.KEY_CCLS_SERVICE,LM.KEY_CCLS_WAREHOUSE,event,str(e),job_type,job_order))
                return Response(json.dumps({"message":Constants.WH_COMMON_EXCEPTION_MESSAGE}), status=500, mimetype='application/json')
        return new_func
    return decorator