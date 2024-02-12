import os
import time
import configparser
import plistlib
import xattr
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from organizer import append_list, create_folder, move_files, link_checker, link_returner


class DownloadHandler(FileSystemEventHandler):
    def __init__(self, dir_path, config):
        super().__init__()
        self.dir_path = dir_path
        self.config = config

    def on_created(self, event):
        if event.is_directory:
            return

        #print(f"script {name}")
        time.sleep(1)

        file_path = event.src_path
        if os.path.exists(file_path):
            try:
                value = plistlib.loads(xattr.getxattr(file_path, 'com.apple.metadata:kMDItemWhereFroms'))
            except (IndexError, plistlib.InvalidFileException, UnicodeDecodeError):
                return 

            result = link_returner(file_path, value)
            dest = self.config["DIRECTORIES"]["Destination"]
            if result is not None:
                move_files(dest, [result], self.config, logger)

def start_watchdog(config):
    dir_path = config["DIRECTORIES"]["Downloads"]
    event_handler = DownloadHandler(dir_path, config)
    observer = Observer()
    observer.schedule(event_handler, path=dir_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":    
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform = lambda option: option
    #
    config.read("current_config.ini")
    logging.basicConfig(filename='script.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.getLogger('watchdog').setLevel(logging.WARNING)
    logger = logging.getLogger('script.log')

    create_folder(config["DIRECTORIES"]["Destination"], config["LINKS"], logger)
    start_watchdog(config)

