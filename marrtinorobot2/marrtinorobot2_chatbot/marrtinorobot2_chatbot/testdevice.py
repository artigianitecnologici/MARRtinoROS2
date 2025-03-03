import sounddevice as sd

device_info = sd.query_devices()
for i, device in enumerate(device_info):
    print(f"ID: {i}, Nome: {device['name']}, Tipo: {'Input' if device['max_input_channels'] > 0 else 'Output'}")


