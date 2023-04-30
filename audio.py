import sounddevice as sd
import numpy as np
import pyaudio
import struct
from scipy.signal import butter, filtfilt

audio_level = 0

def audio_callback(indata, frames, time, status):
    global audio_level
    audio_level = np.linalg.norm(indata) * 10

def get_audio_level():
    # Set up PyAudio
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    # Record audio
    data = stream.read(chunk)
    audio_data = struct.unpack(str(2 * chunk) + 'B', data)
    audio_np_array = np.array(audio_data, dtype='b')[::2] + 128

    # Calculate audio level and scale it from 0 to 100
    audio_level = np.mean(np.abs(audio_np_array - 128))
    audio_level = (audio_level / 128) * 100  # scale it to 0 - 100

    # Round audio level to nearest whole number
    audio_level = round(audio_level)

    # Clean up
    stream.stop_stream()
    stream.close()
    p.terminate()

    return audio_level

def audio_level_to_update_interval(audio_level, min_interval=0.05, max_interval=1.0, threshold=10):
    if audio_level < threshold:
        return None

    normalized_level = min(1.0, max(0.0, (audio_level - threshold) / (100 - threshold)))
    update_interval = max_interval - (max_interval - min_interval) * normalized_level

    return update_interval
