from dotenv import load_dotenv
import logging
import os

load_dotenv()

#
# SERVER VARS
#
PORT = 8083
HOST = "gateway"


#
# LOGGING VARS
#
LOGS_LEVEL = logging.DEBUG
LOGS_FILENAME = "logs/{date}.log" 
LOGS_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


#
# REDIS
#
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = int(os.environ.get("REDIS_PORT"))


#
# OTHER
# 
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
SERVICE_NOT_RESPONDING_TIMEOUT = 10

