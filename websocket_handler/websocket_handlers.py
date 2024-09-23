from fastapi import WebSocket, WebSocketDisconnect
from config.config import ASRConfig
from utils.model import init_asr_model, init_vad_model
from vad_handler.audio_processing import process_vad_audio
from utils.format import format_str_v3
import numpy as np
from llm.langchain_init import stream_predict
from websocket_handler.TranscriptionResponse import TranscriptionResponse
from urllib.parse import parse_qs
from TTS.tts_client import TTSClient 
import asyncio
from utils.conversation_logger import log_conversation
from utils.logger import setup_logger_info
import io

logger = setup_logger_info(__name__)

config = ASRConfig()
asr_model = init_asr_model()  # 初始化语音识别模型
vad_model = init_vad_model()  # 初始化语音活动检测模型

async def transcribe(websocket: WebSocket):
    """
    语音识别和语言模型处理的主要函数
    
    参数:
        websocket (WebSocket): WebSocket连接对象
    """
    await websocket.accept()
    tts_client = TTSClient()  # 创建语音合成客户端
    try:
        # 解析查询参数
        query_params = parse_qs(websocket.scope['query_string'].decode())
        sv = query_params.get('sv', ['false'])[0].lower() in ['true', '1', 't', 'y', 'yes']
        lang = query_params.get('lang', ['auto'])[0].lower()
        
        chunk_size = int(config.CHUNK_SIZE_MS * config.SAMPLE_RATE * config.CHANNELS * (config.BIT_DEPTH // 8) / 1000)
        
        audio_buffer = np.array([])  # 音频缓冲区
        audio_vad = np.array([])  # 语音活动检测的音频缓冲区
        cache = {}
        last_vad_beg = last_vad_end = -1
        offset = 0

        while True:
            data = await websocket.receive_bytes()  # 接收音频数据

            # 将接收到的音频数据添加到缓冲区
            audio_buffer = np.append(audio_buffer, np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0)
            """
            将音频数据分割成块,并进行语音活动检测
            # 将音频数据分割成块,并进行语音活动检测
            # Split the audio data into chunks and perform voice activity detection
            
            # audio_buffer: 音频缓冲区，存储接收到的音频数据
            # audio_buffer: Audio buffer, stores received audio data
            
            # chunk_size: 每个音频块的大小
            # chunk_size: Size of each audio chunk
            
            # chunk: 当前处理的音频块
            # chunk: Current audio chunk being processed
            
            # audio_vad: 用于语音活动检测的音频缓冲区
            # audio_vad: Audio buffer for voice activity detection
            
            # res: 语音活动检测的结果
            # res: Result of voice activity detection
            
            # vad_segments: 检测到的语音片段
            # vad_segments: Detected voice segments
            
            # segment: 单个语音片段的开始和结束时间
            # segment: Start and end time of a single voice segment
            
            # last_vad_beg: 最后一个语音片段的开始时间
            # last_vad_beg: Start time of the last voice segment
            
            # last_vad_end: 最后一个语音片段的结束时间
            # last_vad_end: End time of the last voice segment
            
            # offset: 用于调整语音片段的时间偏移
            # offset: Used to adjust the time offset of voice segments
            
            # beg: 语音片段的开始样本索引
            # beg: Start sample index of the voice segment
            
            # end: 语音片段的结束样本索引
            # end: End sample index of the voice segment
            
            # result: 语音处理的结果
            # result: Result of voice processing
            """
            while len(audio_buffer) >= chunk_size:
                chunk = audio_buffer[:chunk_size]
                audio_buffer = audio_buffer[chunk_size:]
                    
                audio_vad = np.append(audio_vad, chunk)
                res = vad_model.generate(input=chunk, cache=cache, is_final=False, chunk_size=config.CHUNK_SIZE_MS)
                if len(res[0]["value"]):
                    vad_segments = res[0]["value"]
                    for segment in vad_segments:
                        if segment[0] > -1: 
                            last_vad_beg = segment[0]
                        if segment[1] > -1: 
                            last_vad_end = segment[1]
                        if last_vad_beg > -1 and last_vad_end > -1:
                            last_vad_beg -= offset
                            last_vad_end -= offset
                            offset += last_vad_end
                            beg = int(last_vad_beg * config.SAMPLE_RATE / 1000)
                            end = int(last_vad_end * config.SAMPLE_RATE / 1000)
                            result = process_vad_audio(audio_vad[beg:end], sv=True, lang=lang)
                            audio_vad = audio_vad[end:]
                            last_vad_beg = last_vad_end = -1
                            
                            if  result is not None:
                                transcribed_text = format_str_v3(result[0]['text'])
                                print(f"语音识别结果: {transcribed_text}")
    
                                full_response = ""
                                async for chunk in stream_predict(transcribed_text):
                                    full_response += chunk
                                    response = TranscriptionResponse(
                                    code=0,
                                    msg="streaming",
                                    data=chunk
                                    )
                                    await websocket.send_json(response.model_dump())
                                    await asyncio.sleep(0)
                                
                                # 记录对话日志
                                await log_conversation(transcribed_text, full_response)

                                # 发送完成信号
                                final_response = TranscriptionResponse(
                                    code=0,
                                    msg="complete",
                                    data=full_response
                                )
                                
                                # 语音合成
                                audio = await asyncio.to_thread(tts_client.synthesize, final_response.data, play_audio=False)
                                audio_bytes = io.BytesIO()
                                audio.export(audio_bytes, format="wav")
                                
                                # 发送音频
                                await websocket.send_bytes(audio_bytes.getvalue())
                                
                                # 发送JSON响应
                                await websocket.send_json(final_response.model_dump())
    except WebSocketDisconnect:
        logger.info("WebSocket连接已断开")
    except Exception as e:
        logger.error(f"发生意外错误: {e}")
        await websocket.close()
    finally:
        audio_buffer = np.array([])
        audio_vad = np.array([])
        cache.clear()
        logger.info("WebSocket连接断开后清理了资源")
