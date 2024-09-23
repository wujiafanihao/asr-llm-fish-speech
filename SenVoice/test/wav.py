import pyaudio
from wave import *

def record_audio(filename, duration=5):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    print("Recording...")
    frames = []
    for _ in range(0, int(16000 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    print("Recording finished.")

    # 关闭流
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 保存录音到文件
    wf = open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Audio saved to {filename}")

record_audio("wujiafa.wav")
