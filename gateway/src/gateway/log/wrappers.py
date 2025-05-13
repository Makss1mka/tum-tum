import logging
import inspect

def log_entrance_debug(logger: logging.Logger):
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            logger.debug(f"Function {func.__name__} entrance | args {args} ; kwargs {kwargs}")
            result = await func(*args, **kwargs)
            logger.debug(f"Function {func.__name__} exit | Result {result}")
            return result
        
        def sync_wrapper(*args, **kwargs):
            logger.debug(f"Function {func.__name__} entrance | args {args} ; kwargs {kwargs}")
            result = func(*args, **kwargs)
            logger.debug(f"Function {func.__name__} exit | Result {result}")
            return result
        
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator

def log_entrance_info(logger: logging.Logger):
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            logger.info(f"Function {func.__name__} entrance | args {args} ; {kwargs}")
            result = await func(*args, **kwargs)
            logger.info(f"Function {func.__name__} exit | Result {result}")
            return result
        
        def sync_wrapper(*args, **kwargs):
            logger.info(f"Function {func.__name__} entrance | args {args} ; {kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"Function {func.__name__} exit | Result {result}")
            return result
        
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator

def log_entrance_error(logger: logging.Logger):
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            logger.error(f"Function {func.__name__} entrance | args {args} ; {kwargs}")
            result = await func(*args, **kwargs)
            logger.error(f"Function {func.__name__} exit | Result {result}")
            return result
        
        def sync_wrapper(*args, **kwargs):
            logger.error(f"Function {func.__name__} entrance | args {args} ; {kwargs}")
            result = func(*args, **kwargs)
            logger.error(f"Function {func.__name__} exit | Result {result}")
            return result
        
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator
