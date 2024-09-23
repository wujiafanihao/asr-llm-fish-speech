from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from funasr import AutoModel
import soundfile as sf
from config.config import ASRConfig
import os

config = ASRConfig()

os.environ['MODELSCOPE_CACHE'] = config.MODELSCOPE_CACHE
os.environ['MODELSCOPE_MODULES_CACHE'] = config.MODELSCOPE_MODULES_CACHE

def init_asr_model():
    return pipeline(
        task=Tasks.auto_speech_recognition,
        model='iic/SenseVoiceSmall',
        model_revision="master",
        device="cuda:0",
    )

def init_vad_model():
    return AutoModel(
        model="fsmn-vad",
        model_revision="v2.0.4",
        disable_pbar=True,
        max_end_silence_time=200,
        speech_noise_thres=0.8,
        disable_update=True
    )

def init_tts_model():
    return pipeline(
        task=Tasks.text_to_speech,
        model='AI-ModelScope/fish-speech-1.4',
        model_revision="v1.4",
        device="cuda:0",
    )

def init_sv_model():

    sv_pipeline = pipeline(
        task='speaker-verification',
        model='iic/speech_campplus_sv_zh_en_16k-common_advanced',
        model_revision='v1.0.0',
        window_size=400  
    )

    reg_spks_files = [
        "./SenVoice/test/wujiafa.wav"
    ]

    def reg_spk_init(files):
        reg_spk = {}
        for f in files:
            data, sr = sf.read(f, dtype="float32")
            k, _ = os.path.splitext(os.path.basename(f))
            reg_spk[k] = {
                "data": data,
                "sr":   sr,
            }
        return reg_spk

    reg_spks = reg_spk_init(reg_spks_files)
    return sv_pipeline, reg_spks