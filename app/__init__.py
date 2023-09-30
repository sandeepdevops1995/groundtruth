
# Import flask 
from flask import Flask,render_template
from flask_restful import Api
from flask_cors import CORS
from sqlalchemy import create_engine
import config
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from flask_apscheduler import APScheduler
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

oracle_url = sa.engine.URL.create(
    drivername=config.SQL_DRIVER,
    username=config.SQL_USERNAME,
    password=config.SQL_PASSOWRD,
    host=config.SQL_IP,
    database=config.SQL_DATABASE,
)

postgres_url = sa.engine.URL.create(
    drivername=config.PSQL_DRIVER,
    username=config.PSQL_USERNAME,
    password=config.PSQL_PASSOWRD,
    host=config.PSQL_IP,
    port=config.PSQL_PORT,
    database=config.PSQL_DATABASE,
)

# Define the application object
app = Flask(__name__)
engine = create_engine(oracle_url,echo=config.SQl_ECHO)
# "connect_args":{
#     "keepalives": 50,
#     "keepalives_idle": 30,
#     "keepalives_interval": 10,
#     "keepalives_count": 5
# }
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": config.PSQl_CONNECTION_POOL_PING
}
app.config["SQLALCHEMY_DATABASE_URI"] = postgres_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['SQLALCHEMY_POOL_SIZE'] = 10
# app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800

postgres_db = SQLAlchemy(app)
migrate = Migrate(app, postgres_db)
ma = Marshmallow(app)


scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

@app.route("/")
def index():
  return "HELLO WORLD!"

# this is used to call any get API to retrive master data from CCLS
@app.route("/master_data/<name>")
def get(name):
    from app.controllers.yard_controller import get_master_data_common
    return get_master_data_common(name)

#To support cross origin request
CORS(app)
api = Api(app)

from app.models import *
 
from app.urls import register_controllers
from app.services.rake.directory_watcher_service import RakeDataEvents

@scheduler.task('cron', id='CCLS Rake Data', hour='*', misfire_grace_time=900)
def scheduleTask():
    with scheduler.app.app_context():
        from app.services.rake.rake_inward_read import RakeInwardReadService
        from datetime import datetime, timedelta
        from app.logger import logger
        from_date = (datetime.now()-timedelta(days = 1)).strftime("%Y-%m-%dT%H:%M:%S")
        to_date = (datetime.now()+timedelta(days = 2)).strftime("%Y-%m-%dT%H:%M:%S")
        
        #Exim train details
        result = RakeInwardReadService.get_train_details({},from_date=from_date,to_date=to_date)
        
        #Domestic train details
        from app.services.rake.dtms_rake_inward_read import DTMSRakeInwardReadService
        result = DTMSRakeInwardReadService.get_train_details({},from_date=from_date,to_date=to_date)
        logger.info("Task Scheduled from_date: "+from_date+" to_date: "+to_date)
 
register_controllers()
RakeDataEvents()

@scheduler.task('interval',id="redis_scheduled_task",minutes=config.REDIS_SCHEDULE_TASK_TIME,misfire_grace_time=900)
def redis_scheduleTask():
    from app.services.soap_service import get_pendancy_details,get_domestic_permit_details,update_exim_container_details,update_domestic_container_details,get_exim_train_details,get_domestic_train_details,update_inward_rake,get_pendancy_details,get_empty_pendancy_details,get_block_pendancy_details,get_express_pendancy_details,update_outward_rake,update_container_stack_location,get_domestic_outward_train_details,update_domestic_inward_rake,update_domestic_container_stack_location
    from app.logger import logger
    with scheduler.app.app_context():
        from app.redis_config import cache
        import json
        import time
        failed_data_list = cache.lrange("ground_truth_queue",0,-1)
        if failed_data_list:
            # cache.ltrim("ground_truth_queue", -1, 0)
            failed_data_list.reverse()
            for failed_data in failed_data_list:
                failed_data = json.loads(failed_data)
                method = eval(failed_data['method_name'])
                request_data = failed_data['request_data']
                # logger.debug("Removed from cache retry mechanism, details:  " +str(failed_data))
                # method(**request_data)
                # time.sleep(config.REDIS_TASK_SLEEP_TIME)