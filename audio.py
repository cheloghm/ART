import sounddevice as sd
import numpy as np

audio_level = 0

def audio_callback(indata, frames, time, status):
    global audio_level
    audio_level = np.linalg.norm(indata) * 10

def get_audio_level():
    global audio_level
    with sd.InputStream(callback=audio_callback):
        sd.sleep(1000)
    return audio_level
