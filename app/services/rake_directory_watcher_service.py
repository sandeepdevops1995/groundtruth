from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import config
from app.logger import logger
from app.services.rake_db_service import RakeDbService as db_service

record ={}
temp = {}
class RakeDataEvents:

    def __init__(self):
        if not os.path.isdir(config.RAKE_DATA_DIRECTORY):
            print("rake data dir not exists")
        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, path=config.RAKE_DATA_DIRECTORY, recursive=False)
        observer.daemon=True
        observer.start()
        print("started directory watcher service For Rake Model")


class MyHandler(FileSystemEventHandler):
    def process(self, filepath):
        from app import app
        with app.app_context():
            rake_data =  db_service().get_rake_file_data(filepath)
            db_service().save_rake_details(rake_data)
            logger.info('Captured the Rake data and Saved In Data base : {}'.format(filepath))

    def on_created(self, event):
        fileName = os.path.basename(event.src_path)
        logger.info('On File Created : {}'.format(fileName))

        if "Temp" in fileName or ".tmp" in fileName or ".~lock." in fileName:
            return
        self.process(event.src_path)

    def on_moved(self, event):
        fileName = os.path.basename(event.dest_path)
        logger.info('On File Moved : {}'.format(fileName))
        if "Temp" in fileName:
            return
        self.process(event.dest_path)