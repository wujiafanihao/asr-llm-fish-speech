import asyncio
from utils.logger import setup_logger_info

logger = setup_logger_info(__name__)

async def log_conversation(user_input, assistant_response):
    """
    记录对话日志
    
    参数:
        user_input (str): 用户输入
        assistant_response (str): 助手回复
    """
    logger.info(f"用户: {user_input}")
    logger.info(f"助手: {assistant_response}")
    
    # 模拟异步I/O操作,例如写入数据库或文件
    await asyncio.sleep(0)
