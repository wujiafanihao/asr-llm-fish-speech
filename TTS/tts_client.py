import wave
import os
import uuid
from config.config import TTSConfig
import ormsgpack
import requests
import pyaudio
from pydub import AudioSegment
from config.config import TTSConfig
from dotenv import load_dotenv

from TTS.tools.commons import ServeReferenceAudio, ServeTTSRequest
from TTS.tools.file import audio_to_bytes, read_ref_text

# 重新加载 .env 文件
load_dotenv(override=True)

class TTSClient:
    def __init__(self):
        # 初始化TTS客户端，设置各种参数
        self.url = TTSConfig.URL
        self.cache_dir = TTSConfig.CACHE_DIR
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 设置音频相关参数
        self.bit_depth = TTSConfig.BIT_DEPTH
        self.mp3_bitrate = TTSConfig.MP3_BITRATE
        self.opus_bitrate = TTSConfig.OPUS_BITRATE
        
        # 设置生成参数
        self.temperature = TTSConfig.TEMPERATURE
        self.top_p = TTSConfig.TOP_P
        self.top_k = TTSConfig.TOP_K
        self.repetition_penalty = TTSConfig.REPETITION_PENALTY
        self.max_new_tokens = TTSConfig.MAX_NEW_TOKENS
        self.length_penalty = TTSConfig.LENGTH_PENALTY
        self.no_repeat_ngram_size = TTSConfig.NO_REPEAT_NGRAM_SIZE
        
        # 设置流式传输参数
        self.streaming_buffer_size = TTSConfig.STREAMING_BUFFER_SIZE
        self.streaming_latency = TTSConfig.STREAMING_LATENCY
        
        # 设置其他选项
        self.use_cache = TTSConfig.USE_CACHE
        self.normalize_audio = TTSConfig.NORMALIZE_AUDIO
        self.trim_silence = TTSConfig.TRIM_SILENCE

    def synthesize(self, text, reference_audio="openai.mp3", reference_text=None, reference_id=None, 
                   speaker="speaker_1", emotion="happy", play_audio=True, **kwargs):
        # 设置输出格式和音频参数
        output_format = TTSConfig.OUTPUT_FORMAT
        channels = TTSConfig.CHANNELS
        rate = TTSConfig.SAMPLE_RATE
        chunk_size = TTSConfig.CHUNK_SIZE

        # 准备参考音频和文本
        if reference_audio:
            byte_audio = audio_to_bytes(reference_audio)
            ref_text = read_ref_text(reference_text) if reference_text else ""
            references = [ServeReferenceAudio(audio=byte_audio, text=ref_text)]
        else:
            references = []

        # 准备请求数据
        data = {
            "text": text,
            "references": references,
            "reference_id": reference_id,
            "speaker": speaker,
            "emotion": emotion,
            "format": output_format,
            "streaming": True,
        }

        # 只添加非默认值的参数
        for key, value in kwargs.items():
            if value is not None:
                data[key] = value

        pydantic_data = ServeTTSRequest(**data)

        # 发送请求
        response = requests.post(
            self.url,
            data=ormsgpack.packb(pydantic_data, option=ormsgpack.OPT_SERIALIZE_PYDANTIC),
            stream=True,
            headers={
                "authorization": TTSConfig.TTS_API_KEY,
                "content-type": "application/msgpack",
            },
        )

        if response.status_code == 200:
            return self._handle_streaming(response, output_format, channels, rate, play_audio, chunk_size)
        else:
            print(f"请求失败,状态码为 {response.status_code}")
            print(response.json())
            return None

    def _handle_streaming(self, response, output_format, channels, rate, play_audio, chunk_size):
        # 初始化PyAudio
        p = pyaudio.PyAudio()
        audio_format = pyaudio.paInt16
        stream = p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)

        # 准备保存音频文件
        file_name = f"generated_audio_{uuid.uuid4().hex[:8]}.{output_format}"
        file_path = os.path.join(self.cache_dir, file_name)

        # 打开wave文件准备写入
        wf = wave.open(file_path, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(audio_format))
        wf.setframerate(rate)

        try:
            # 处理流式响应
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    if play_audio:
                        stream.write(chunk)
                    wf.writeframesraw(chunk)
                    
                    # 将音频片段yield出去
                    # yield chunk
                else:
                    break
        finally:
            # 关闭所有资源
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf.close()

        print(f"音频已保存至 '{file_path}'.")
        return AudioSegment.from_wav(file_path)

# 示例用法
if __name__ == "__main__":
    client = TTSClient()
    
    text = """
        额夜的坏处主要包括以下几点：

        1. **影响健康**：长期熬夜会导致生物钟紊乱，影响睡眠质量，从而引发疲劳、注意力不集中、记忆力下降等问题。

        2. **心理问题**：熬夜可能导致焦虑、抑郁等心理健康问题，情绪波动也会加剧。

        3. **免疫力下降**：缺乏足够的睡眠会削弱免疫系统，使身体更容易感染疾病。

        4. **皮肤问题**：熬夜会导致皮肤暗沉、出现黑眼圈和皱纹，影响外貌。

        5. **生活质量下降**：长期熬夜可能影响工作和学习效率，导致生活质量下降。
"""
    
    # 流式合成
    streaming_audio = client.synthesize(text)