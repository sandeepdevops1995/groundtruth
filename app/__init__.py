
# Import flask 
from flask import Flask,render_template
from flask_restful import Api
from flask_cors import CORS
from sqlalchemy import create_engine
import config
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa

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
    database=config.PSQL_DATABASE,
)

# Define the application object
app = Flask(__name__)
engine = create_engine(oracle_url,echo=config.SQl_ECHO)
app.config["SQLALCHEMY_DATABASE_URI"] = postgres_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
postgres_db = SQLAlchemy(app)

@app.route("/")
def index():
  return render_template("index.html")

# this is used to call any get API to retrive master data from CCLS
@app.route("/master_data/<name>")
def get(name):
    from app.controllers.yard_controller import get_master_data_common
    return get_master_data_common(name)

#To support cross origin request
CORS(app)
api = Api(app)

 

 

