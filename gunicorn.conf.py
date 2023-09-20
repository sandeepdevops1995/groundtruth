import multiprocessing

bind = "0.0.0.0:8040"
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 8 
#worker_class = "eventlet"
worker_connections = 1000
wsgi_app = "ground_truth:app"
#print_config = True
timeout=360
