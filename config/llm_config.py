import os
from config.env_config import load_environment_variables

load_environment_variables()

class LLMConfig:
    @staticmethod
    def _parse_env(key, default, type_func):
        value = os.getenv(key, default)
        try:
            return type_func(value.split('#')[0].strip())
        except ValueError:
            print(f"警告: 无法解析环境变量{key},使用默认值: {default}")
            return type_func(default)
        
    MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'openai')
    # OpenAI 配置
    OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')  
    OPENAI_API_KEY =  os.getenv('OPENAI_API_KEY', "")
    # Claude 配置
    CLAUDE_BASE_URL = os.getenv('CLAUDE_BASE_URL', 'https://api.anthropic.com')
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', "")  
    MODEL = os.getenv('MODEL', 'gpt-4o-mini')
    LLM_MAX_TOKENS = os.getenv('LLM_MAX_TOKENS', 512)
    # Hugging Face 配置
    HuggingFACE_CACHE = os.getenv('HuggingFACE_CACHE', "./huggingface")
    HuggingFACE_TASK = os.getenv('HuggingFACE_TASK', "text-generation")
    IS_CUDA = _parse_env('IS_CUDA', "-1", int)
    # HuggingFace Endpoint 配置
    REPO_MODEL = os.getenv('REPO_MODEL', "mistralai/Mistral-7B-Instruct-v0.2")
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', "")
    # Ollama 配置
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://127.0.0.1:11434')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'phi3.5:3.8b')
    # vllm 配置
    VLLM_BASE_URL = os.getenv('VLLM_BASE_URL', "http://localhost:8000/v1")
    VLLM_API_KEY = os.getenv('VLLM_API_KEY', "")
    VLLM_MODEL = os.getenv('VLLM_MODEL', "mistralai/Mistral-7B-Instruct-v0.2")