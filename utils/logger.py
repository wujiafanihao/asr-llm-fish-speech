import logging

def setup_logger(name):
    """
    设置一个DEBUG级别的日志记录器

    参数:
        name (str): 日志记录器的名称

    返回:
        logging.Logger: 配置好的日志记录器对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger

def setup_logger_info(name):
    """
    设置一个INFO级别的日志记录器

    参数:
        name (str): 日志记录器的名称

    返回:
        logging.Logger: 配置好的日志记录器对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

