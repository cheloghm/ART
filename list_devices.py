import sounddevice as sd

devices = sd.query_devices()

for idx, device in enumerate(devices):
    if device['max_input_channels'] > 0:
        print(f"Device index: {idx}, Device name: {device['name']}")
