from pydantic import BaseModel

class TranscriptionResponse(BaseModel):
    """
    语音识别响应模型
    
    属性:
        code (int): 响应状态码,0表示成功
        msg (str): 响应消息,如"streaming"表示正在流式传输,"complete"表示传输完成
        data (str): 响应数据,包含语音识别的文本结果或语言模型生成的文本
    """
    code: int
    msg: str
    data: str

    class Config:
        json_encoders = {
            str: lambda v: v.encode('utf-8').decode('utf-8')
        }