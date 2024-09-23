import os
from dotenv import load_dotenv

def load_environment_variables():
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取项目根目录（假设 config 文件夹在项目根目录下）
    root_dir = os.path.dirname(current_dir)
    # 构造 .env 文件的路径
    dotenv_path = os.path.join(root_dir, '.env')

    # 加载 .env 文件，并打印结果
    load_result = load_dotenv(dotenv_path, override=True)
    return load_result