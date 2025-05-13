from dotenv import load_dotenv
import logging
import os

load_dotenv()


#
# SERVER VARS
#
PORT = 8081
HOST = "auth-service"


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
# TOKENS
# 
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ACCESS_EXPIRATION_TIME_MINUTES = int(os.environ.get("JWT_ACCESS_EXPIRATION_TIME_MINUTES"))
JWT_REFRESH_EXPIRATION_TIME_MINUTES = int(os.environ.get("JWT_REFRESH_EXPIRATION_TIME_DAYS")) * 24 * 60
SESSION_EXPIRATION_TIME = int(os.environ.get("SESSION_EXPIRATION_TIME"))

