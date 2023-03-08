import logging
import os

LOG_FORMAT ="%(asctime)s %(message)s"
DEFAULT_LEVEL =logging.DEBUG

class LogWrapper():
    #mode w means over write existing content. for appending use mode =a
    def __init__(self, name, mode="w"):
        self.create_directory()
        self.file_name = './logs/'+name+'.log'
        self.logger = logging.getLogger(name)
        self.logger.setLevel(DEFAULT_LEVEL)

        file_handler = logging.FileHandler(self.file_name, mode=mode)
        formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        #self.logger.debug('LogWrapper init ', self.file_name)

    def create_directory(self):
        log_path = "./logs"
        if not os.path.exists(log_path):
            os.makedirs(log_path)
    
if __name__ == "__main__":
    #name= str('test')
    log = LogWrapper(name="abc")
    log.logger.debug(" this is a test log")
