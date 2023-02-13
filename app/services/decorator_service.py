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
                result = json.dumps({"message":"unexpected error"})
                return Response(result,status=status.VALD_FAIL, mimetype='application/json')
        return new_func
    return decorator
custom_exceptions = get_decorator()

def is_valid_api_key(headers):
    url = config.IAM_SERVICE_URL +config.VALIDATE_AUTH_END_POINT
    status = False
    try:
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
            status = True
    except Exception as e:
        print("Iam service not available")
    return status

def validate_auth():
    def decorator(func):
        def new_func(*args, **kwargs):
            if is_valid_api_key(request.headers):
                return func(*args, **kwargs)
            else:
                print("Unauthorized to access this api...")
            return Response({ 'status': 'authentication failed (JWT token maybe missing/invalid/expired.)'}, 401)
        return new_func
    return decorator
jwt_auth_required = validate_auth()

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
