import logging

APP_LOGGER: logging.Logger = logging.getLogger("APP")
EXCEPTION_HANDLER_LOGGER: logging.Logger = logging.getLogger("EXCEPTION HANDLER")
TEST_LOGGER: logging.Logger = logging.getLogger("TEST")

SESSION_SERVICE_LOGGER: logging.Logger = logging.getLogger("SESSION SERVICE")
USER_CREDS_SERVICE_LOGGER: logging.Logger = logging.getLogger("USER CREDS SERVICE")
JWT_SERVICE_LOGGER: logging.Logger = logging.getLogger("JWT SERVICE")

USER_CREDS_SERVICE_ROUTER_LOGGER: logging.Logger = logging.getLogger("USER CREDS ROUTER")
KAFKA_SERVICE_LOGGER: logging.Logger = logging.getLogger("KAFKA SERVICE")
