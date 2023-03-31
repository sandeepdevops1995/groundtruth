
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
app.config["SQLALCHEMY_DATABASE_URI"] = postgres_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
 
from app.controllers.urls import register_controllers
from app.services.rake_directory_watcher_service import RakeDataEvents

@scheduler.task('cron', id='CCLS Rake Data', day='*/3', misfire_grace_time=900)
def scheduleTask():
    with scheduler.app.app_context():
        from app.services.rake_db_service import RakeDbService
        from datetime import datetime, timedelta
        from app.logger import logger
        from_date = (datetime.now()-timedelta(days = 1)).strftime("%Y-%m-%dT%H:%M:%S")
        to_date = (datetime.now()+timedelta(days = 2)).strftime("%Y-%m-%dT%H:%M:%S")
        result = RakeDbService.get_train_details({},from_date=from_date,to_date=to_date)
        logger.info("Task Scheduled from_date: "+from_date+" to_date: "+to_date)
 
register_controllers()
RakeDataEvents()