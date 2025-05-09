import logging

#
# SERVER VARS
#
PORT = 8082
HOST = "localhost"


#
# LOGGING VARS
#
LOGS_LEVEL = logging.DEBUG
LOGS_FILENAME = "logs/{date}.log" 
LOGS_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
