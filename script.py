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
        #time.sleep(1)

        file_path = event.src_path
        
        if not os.path.exists(file_path):
            return 
        
        if file_path.endswith(".crdownload"): #if theres a .crdownload file it means the download hasn't finished and chrome is still sending data to the file
            while os.path.exists(file_path):
                print(f"FILE PENDING: {file_path}\n")
                time.sleep(1)
            return None
        
        value = self.error_handling(file_path)
        if value:
            result = link_returner(file_path, value)
            dest = self.config["DIRECTORIES"]["Destination"]
            if result is not None:
                move_files(dest, [result], self.config, logger)
            
    
    def error_handling(self, file_path):
        try:
            attr = xattr.getxattr(file_path, 'com.apple.metadata:kMDItemWhereFroms')
            value = plistlib.loads(attr)
            return value
        except plistlib.InvalidFileException as e:
            logger.error(f"Plist data invalid, error: '{e}'")
            return None
        except UnicodeDecodeError as e: 
            logger.error(f"Unicode decoding error occured '{e}'")
            return None
        except OSError as e:
            if e.errno == 93:
                logger.info(f"Skipped hidden file: '{file_path}'") #Most likely a hidden file, but not sure yet
            else:
                logger.error(f"OS error occured '{e}'")
            return None
        except Exception as e:
            logger.error(f"Error not accounted for yet (please report this error!): '{e}'")
            return None
        

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
    config.read("config.ini")
    logging.basicConfig(filename='script.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.getLogger('watchdog').setLevel(logging.WARNING)
    logger = logging.getLogger('script.log')

    create_folder(config["DIRECTORIES"]["Destination"], config["LINKS"], logger)
    start_watchdog(config)

