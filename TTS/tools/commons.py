from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field, conint


class ServeReferenceAudio(BaseModel):
    audio: bytes  # 音频数据
    text: str  # 音频对应的文本


class ServeTTSRequest(BaseModel):
    text: str  # 需要合成的文本
    chunk_length: Annotated[int, conint(ge=100, le=300, strict=True)] = 200  # 音频分块长度，范围100-300毫秒
    # 音频格式
    format: Literal["wav", "pcm", "mp3"] = "wav"  # 输出音频格式，支持wav、pcm和mp3
    mp3_bitrate: Literal[64, 128, 192] = 128  # MP3比特率，可选64、128或192 kbps
    # 用于上下文学习的参考音频
    references: list[ServeReferenceAudio] = []  # 参考音频列表，用于模型学习说话风格
    # 参考ID
    # 例如，如果你想使用 https://fish.audio/m/7f92f8afb8ec43bf81429cc1c9199cb1/
    # 只需传入 7f92f8afb8ec43bf81429cc1c9199cb1
    reference_id: str | None = None  # 参考音频的ID，用于指定特定的参考音频
    # 对英文和中文文本进行标准化处理，提高数字等内容的稳定性
    normalize: bool = True  # 是否对文本进行标准化处理
    mp3_bitrate: Optional[int] = 64  # MP3比特率，可选值
    opus_bitrate: Optional[int] = -1000  # Opus编码比特率，负值表示使用默认设置
    # 平衡模式将延迟降低到300毫秒，但可能降低稳定性
    latency: Literal["normal", "balanced"] = "normal"  # 延迟模式，normal为正常，balanced为平衡模式
    # 以下参数通常不使用
    streaming: bool = False  # 是否使用流式传输
    emotion: Optional[str] = None  # 情感参数，用于控制语音情感
    max_new_tokens: int = 1024  # 最大生成标记数
    top_p: Annotated[float, Field(ge=0.1, le=1.0, strict=True)] = 0.7  # 用于控制采样的概率阈值
    repetition_penalty: Annotated[float, Field(ge=0.9, le=2.0, strict=True)] = 1.2  # 重复惩罚系数
    temperature: Annotated[float, Field(ge=0.1, le=1.0, strict=True)] = 0.7  # 温度参数，控制生成的随机性
