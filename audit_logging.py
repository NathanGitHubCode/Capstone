import logging
import datetime
from logging.handlers import TimedRotatingFileHandler
import os
import glob

now = datetime.datetime.now()
current_time = now.strftime("%Y-%m-%d_%H-%M-%S")

logger = logging.getLogger('audit')
logger.setLevel(logging.INFO)

def setup_logger():
    log_file = f"audit_log_{current_time}.log"
    file_handler = TimedRotatingFileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%m-%d-%Y %H:%M:%S')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

def log_info(action):
    message = f'{action}'
    logger.info(message)

def log_error(action):
    message = f'{action}'
    logger.error(message)
    
def delete_audit_logs():
    log_dir = '../Capstone/'
    file_pattern = log_dir + 'audit_*.log'
    files = glob.glob(file_pattern)
    if(len(files) == 1 or len(files) == 0):
        print("No audit log files to delete.")
    else: 
        print(f"Found {len(files) - 1} audit log(s):")
        for file in files[:files.__len__()-1]:
            print(f"\t- {file[12:]}")
        confirm = input("Are you sure you want to delete all audit logs? (y/n) ")
        if confirm.lower() == "y":
            for file in files[:files.__len__()-1]:
                log_info(f"log {file[12:]} deleted")
                print(f"Deleting {file[12:]}")
                os.remove(file)
        else:
            print("Cancelled.")