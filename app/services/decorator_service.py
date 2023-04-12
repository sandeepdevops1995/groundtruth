from flask import json,Response
from app.logger import logger
from app.services import statuscodes as status
from flask import request
import requests
import config
import time
import json


def get_decorator():
    def decorator(func):
        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(repr(e), exc_info=True)
                result = json.dumps({"message":"unexpected error","error":str(e)})
                return Response(result,status=status.VALD_FAIL, mimetype='application/json')
        return new_func
    return decorator
custom_exceptions = get_decorator()

def is_valid_api_key(headers):
    url = config.IAM_SERVICE_URL +config.VALIDATE_AUTH_END_POINT
    is_authorised = False
    try:
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
            is_authorised = True
    except Exception as e:
        logger.info("Exception is may occured due to unavailability of iam service ")
        logger.exception(e)
        return is_authorised
    return is_authorised

def validate_auth():
    def decorator(func):
        def new_func(*args, **kwargs):
            if is_valid_api_key(request.headers):
                return func(*args, **kwargs)
            else:
                logger.info("Unauthorized to access this api...")
            return Response(json.dumps({ 'status': 'authentication failed (API token maybe missing)'}), 401, mimetype='application/json')
        return new_func
    return decorator
api_auth_required = validate_auth()

def query_debugger():
    def decorator(func):
        def new_func(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            logger.debug(f"{func.__qualname__} Query Execution Finished in : {(end - start):.2f}s")
            return result
        return new_func
    return decorator
