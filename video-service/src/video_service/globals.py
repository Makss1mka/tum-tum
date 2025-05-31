from dotenv import load_dotenv
import logging
import os

load_dotenv()

#
# SERVER VARS
#
PORT = 8085
HOST = "localhost"


#
# LOGGING VARS
#
LOGS_LEVEL = logging.DEBUG
LOGS_FILENAME = "logs/{date}.log" 
LOGS_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


#
# DB
#
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_URL = os.environ.get("DB_URL")


#
# REDIS
#
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = int(os.environ.get("REDIS_PORT"))


#
# OTHER
# 
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

