import logging

def log_entrance_debug(logger: logging.Logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.debug(f"Function {func.__name__} entrance | args {args} ; {kwargs}")
            result = func(*args, **kwargs)
            logger.debug(f"Function {func.__name__} exit | Result {result}")
            
            return result
        return wrapper
    return decorator

def log_entrance_info(logger: logging.Logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.info(f"Function {func.__name__} entrance | args {args} ; {kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"Function {func.__name__} exit | Result {result}")
            
            return result
        return wrapper
    return decorator

def log_entrance_error(logger: logging.Logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.error(f"Function {func.__name__} entrance | args {args} ; {kwargs}")
            result = func(*args, **kwargs)
            logger.error(f"Function {func.__name__} exit | Result {result}")
            
            return result
        return wrapper
    return decorator
