# Run a server.
from app import app
from app.controllers.urls import register_controllers
from app.services.ground_truth_service import start_rabbitMQ_service
import config

#from app.servicecs.gate_groundtruth_service

if __name__ == '__main__':
    #register all end points 
    register_controllers()
    # start_rabbitMQ_service()
    with app.app_context():
        from app import postgres_db
        from app.models import Permit
        postgres_db.create_all()
        print("db created")
    app.run(host=config.IP_ADDRESS,port=config.PORT, debug=config.DEBUG)
    # socketio.run(app, host=config.IP_ADDRESS,port=config.PORT, debug=config.DEBUG)

   
