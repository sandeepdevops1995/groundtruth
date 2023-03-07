# Run a server.
from app import app,scheduler
from app.controllers.urls import register_controllers
from app.services.ground_truth_service import start_rabbitMQ_service
from app.services.rake_directory_watcher_service import RakeDataEvents
import config

#from app.servicecs.gate_groundtruth_service

@scheduler.task('cron', id='CCLS Rake Data', day='*', misfire_grace_time=900)
def scheduleTask():
    with scheduler.app.app_context():
        from app.services.rake_db_service import RakeDbService
        from datetime import datetime, timedelta
        from app.logger import logger
        from_date = (datetime.now()-timedelta(days = 1)).strftime("%Y-%m-%dT%H:%M:%S")
        to_date = (datetime.now()+timedelta(days = 2)).strftime("%Y-%m-%dT%H:%M:%S")
        result = RakeDbService.get_train_details({},from_date=from_date,to_date=to_date)
        logger.info("Task Scheduled from_date: "+from_date+" to_date: "+to_date)
    
if __name__ == '__main__':
    #register all end points 
    register_controllers()
    RakeDataEvents()
    # start_rabbitMQ_service()
    app.run(host=config.IP_ADDRESS,port=config.PORT, debug=config.DEBUG)
    # socketio.run(app, host=config.IP_ADDRESS,port=config.PORT, debug=config.DEBUG)

   
