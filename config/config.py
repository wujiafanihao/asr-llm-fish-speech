import os
from config.env_config import load_environment_variables

load_environment_variables()

class ASRConfig:
    """
    配置类,用于管理各种配置参数
    """
    @staticmethod
    def _parse_env(key, default, type_func):
        """
        解析环境变量的值,如果环境变量不存在或解析失败,则使用默认值
        
        参数:
            key (str): 环境变量名
            default (any): 默认值
            type_func (function): 类型转换函数,如int,float等
        
        返回:
            any: 解析后的环境变量值或默认值
        """
        value = os.getenv(key, default)
        try:
            # 移除可能的注释并转换类型
            return type_func(value.split('#')[0].strip())
        except ValueError:
            print(f"警告: 无法解析环境变量{key},使用默认值: {default}")
            return type_func(default)
        
    MODELSCOPE_CACHE = os.getenv('MODELSCOPE_CACHE', 'SenVoice\model')
    MODELSCOPE_MODULES_CACHE = os.getenv('MODELSCOPE_MODULES_CACHE', 'SenVoice\model')  
    SV_THR = _parse_env('SV_THR', "0.5", float)  # 说话人验证阈值
    CHUNK_SIZE_MS = _parse_env('CHUNK_SIZE_MS', '100', int)  # 音频块大小(毫秒)
    SAMPLE_RATE = _parse_env('SAMPLE_RATE', '16000', int)  # 采样率
    BIT_DEPTH = _parse_env('BIT_DEPTH', '16', int)  # 位深度
    CHANNELS = _parse_env('CHANNELS', '1', int)  # 音频通道数

    # @staticmethod
    # def print_env_vars():
    #     print("Environment variables:")
    #     print(f"SV_THR: {os.getenv('SV_THR')}")
    #     print(f"CHUNK_SIZE_MS: {os.getenv('CHUNK_SIZE_MS')}")
    #     print(f"SAMPLE_RATE: {os.getenv('SAMPLE_RATE')}")
    #     print(f"BIT_DEPTH: {os.getenv('BIT_DEPTH')}")
    #     print(f"CHANNELS: {os.getenv('CHANNELS')}")

class TTSConfig:
    @staticmethod
    def _parse_env(key, default, type_func):
        """
        解析环境变量的值,如果环境变量不存在或解析失败,则使用默认值
        
        参数:
            key (str): 环境变量名
            default (any): 默认值
            type_func (function): 类型转换函数,如int,float等
        
        返回:
            any: 解析后的环境变量值或默认值
        """
        value = os.getenv(key, default)
        try:
            return type_func(value)
        except (ValueError, TypeError):
            print(f"警告: 无法解析环境变量 {key},使用默认值: {default}")
            return type_func(default)

    URL = os.getenv('TTS_URL', 'http://127.0.0.1:8055/v1/tts')
    TTS_API_KEY = os.getenv('TTS_API_KEY', '')
    CACHE_DIR = os.getenv('CACHE_DIR', './cache')
    OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'wav')
    CHANNELS = _parse_env('CHANNELS', 1, int)
    SAMPLE_RATE = _parse_env('TTS_RATE', 44100, int)
    BIT_DEPTH = _parse_env('BIT_DEPTH', 16, int)
    CHUNK_SIZE = _parse_env('TTS_CHUNK_SIZE', 256, int)
    MP3_BITRATE = _parse_env('TTS_MP3_BITRATE', 128, int)
    OPUS_BITRATE = _parse_env('TTS_OPUS_BITRATE', 24000, int)
    TEMPERATURE = _parse_env('TTS_TEMPERATURE', 0.8, float)
    TOP_P = _parse_env('TTS_TOP_P', 0.8, float)
    TOP_K = _parse_env('TTS_TOP_K', 50, int)
    REPETITION_PENALTY = _parse_env('TTS_REPETITION_PENALTY', 1.2, float)
    MAX_NEW_TOKENS = _parse_env('TTS_MAX_NEW_TOKENS', 1024, int)
    LENGTH_PENALTY = _parse_env('TTS_LENGTH_PENALTY', 1.0, float)
    NO_REPEAT_NGRAM_SIZE = _parse_env('TTS_NO_REPEAT_NGRAM_SIZE', 3, int)
    STREAMING_BUFFER_SIZE = _parse_env('TTS_STREAMING_BUFFER_SIZE', 4096, int)
    STREAMING_LATENCY = _parse_env('TTS_STREAMING_LATENCY', 100, int)
    USE_CACHE = _parse_env('TTS_USE_CACHE', True, bool)
    NORMALIZE_AUDIO = _parse_env('TTS_NORMALIZE_AUDIO', True, bool)
    TRIM_SILENCE = _parse_env('TTS_TRIM_SILENCE', True, bool)

    # @staticmethod
    # def print_env_vars():
    #     print("Environment variables:")
    #     print(f"URL: {os.getenv('TTS_URL')}")
    #     print(f"CACHE_DIR: {os.getenv('CACHE_DIR')}")
    #     print(f"OUTPUT_FORMAT: {os.getenv('OUTPUT_FORMAT')}")
    #     print(f"CHANNELS: {os.getenv('CHANNELS')}")
    #     print(f"SAMPLE_RATE: {os.getenv('SAMPLE_RATE')}")
    #     print(f"BIT_DEPTH: {os.getenv('BIT_DEPTH')}")
    #     print(f"CHUNK_SIZE: {os.getenv('TTS_CHUNK_SIZE')}")
    #     print(f"MP3_BITRATE: {os.getenv('TTS_MP3_BITRATE')}")
    #     print(f"OPUS_BITRATE: {os.getenv('TTS_OPUS_BITRATE')}")
    #     print(f"TEMPERATURE: {os.getenv('TTS_TEMPERATURE')}")
    #     print(f"TOP_P: {os.getenv('TTS_TOP_P')}")
    #     print(f"TOP_K: {os.getenv('TTS_TOP_K')}")
    #     print(f"REPETITION_PENALTY: {os.getenv('TTS_REPETITION_PENALTY')}")
    #     print(f"MAX_NEW_TOKENS: {os.getenv('TTS_MAX_NEW_TOKENS')}")

# if __name__ == "__main__":
#     ASRConfig.print_env_vars()
#     TTSConfig.print_env_vars()
