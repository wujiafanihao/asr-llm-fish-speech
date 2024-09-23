from config.config import ASRConfig
from utils.model import init_asr_model,init_sv_model
from utils.logger import setup_logger

logger = setup_logger(__name__)

config = ASRConfig()

asr_pipeline = init_asr_model()

sv_pipeline, reg_spks = init_sv_model()

# config.SV_THR = 0.29
logger.debug(f"Current SV_THR: {config.SV_THR}")

def process_vad_audio(audio, sv=True, lang="auto"):
    # 如果启用了说话人验证
    if sv:
        hit = False
        # 遍历所有注册的说话人
        for k, v in reg_spks.items():
            # 对当前音频和注册说话人的音频进行相似度比较
            res_sv = sv_pipeline([audio, v["data"]], thr=config.SV_THR)
            # 记录日志，显示每个说话人的验证结果
            logger.debug(f"[speaker check] {k}: {res_sv}")
            # 如果相似度得分高于阈值，标记为匹配成功
            if res_sv["score"] >= config.SV_THR:
                hit = True
                break  # 找到匹配的说话人后立即退出循环
        
        # 只有在匹配成功时才进行语音识别
        if hit:
            return asr_pipeline(audio, language=lang.strip())
        else:
            return None  # 如果没有匹配到说话人，返回 None
    
    # 如果没有启用说话人验证，直接进行语音识别
    return asr_pipeline(audio, language=lang.strip())