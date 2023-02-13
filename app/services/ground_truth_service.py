import pika, sys, os, time
from threading import Thread
import app.constants as Constants
import config
from app.logger import logger
from app.services.database_service import GateDbService as db_service
from app.services.decorator_service import is_valid_api_key

def start_rabbitMQ_service():
	thread = Thread(target=gate_ground_truth_service)
	thread.start()

	

def gate_ground_truth_service():
	credentials = pika.PlainCredentials(Constants.BROKER_USERNAME, Constants.BROKER_PASSWORD)
	parameters = pika.ConnectionParameters(Constants.BROKER_IP, Constants.BROKER_PORT, '/', credentials)
	connection = pika.BlockingConnection(parameters)
	channel=connection.channel()

	def callback(ch, method, prop, body):
		try:
			if is_valid_api_key(prop.headers["Authorization"]):
				permit_number = body.decode()
				print("received ground truth request",permit_number,prop, body,prop.headers)
				post_ground_truth_data(prop.headers,permit_number)
			else:
				print("Unauthorized to access")
			
		except Exception as e:
			print("error while posting data to gate main service",e)
	
	channel.exchange_declare(exchange=Constants.BROKER_CONSUME_EXCHANGE, exchange_type=Constants.BROKER_EXCHANGE_TYPE, durable=True)
	result = channel.queue_declare(queue='', exclusive=True)
	queue_name = result.method.queue
	channel.queue_bind(exchange=Constants.BROKER_CONSUME_EXCHANGE, queue=queue_name)
	channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
	print('Micro GT service started..')
	channel.start_consuming()

def post_ground_truth_data(headers, permit_number):
	response = "true"
	permit_number = permit_number
	container_data = db_service.get_details_permit_number(permit_number)
	logger.debug('Sent Container details through Rabbit MQ Service: {}'.format(container_data))
	properties = pika.BasicProperties(headers=headers, content_type='application/json',expiration='5000')
	credentials = pika.PlainCredentials(Constants.BROKER_USERNAME, Constants.BROKER_PASSWORD)
	parameters = pika.ConnectionParameters(Constants.BROKER_IP, Constants.BROKER_PORT, '/', credentials)
	connection = pika.BlockingConnection(parameters)
	channel=connection.channel()
	channel.exchange_declare(exchange=Constants.BROKER_PUBLISH_EXCHANGE, exchange_type=Constants.BROKER_EXCHANGE_TYPE, durable=True)
	channel.basic_publish(exchange=Constants.BROKER_PUBLISH_EXCHANGE, routing_key='', properties = properties, body=container_data)
	connection.close()

if __name__ == '__main__':
    try:
        get_ground_truth_data()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
