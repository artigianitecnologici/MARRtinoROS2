import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import whisper
import wavio
import numpy as np
import time
import threading

# Percorso al modello Vosk in italiano
model_path = "../models/vosk-model-it-0.22"
model_vosk = Model(model_path)

# Carica il modello Whisper
model_whisper = whisper.load_model("base")

# Parametri di registrazione audio
samplerate = 16000
q = queue.Queue()

# Trova l'indice corretto per il dispositivo ReSpeaker 4-Mic Array (solo input)
device_info = sd.query_devices()
input_device_index = None
output_device_index = None

for i, device in enumerate(device_info):
    if "ReSpeaker" in device['name']:
        input_device_index = i
        print(f"Trovato ReSpeaker 4-Mic Array come input all'indice {input_device_index}")
    elif "Cuffie" in device['name'] or "Altoparlanti" in device['name']:
        output_device_index = i
        print(f"Trovato dispositivo di output all'indice {output_device_index}")

if input_device_index is None:
    raise ValueError("ReSpeaker 4-Mic Array non trovato. Controlla le connessioni del dispositivo.")

if output_device_index is None:
    raise ValueError("Nessun dispositivo di output audio trovato. Collega cuffie o altoparlanti.")

# Imposta il dispositivo di input su ReSpeaker e di output su cuffie/altoparlanti
sd.default.device = (input_device_index, output_device_index)
sd.default.samplerate = samplerate
sd.default.channels = 1

# Funzione di callback per aggiungere i dati audio alla coda
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# Funzione per riprodurre un suono beep in un thread separato
def play_beep(frequency=1000, duration=0.5, volume=0.5):
    t = np.linspace(0, duration, int(samplerate * duration), False)
    wave = (volume * np.sin(2 * np.pi * frequency * t)).astype(np.float32)
    
    try:
        with sd.OutputStream(samplerate=samplerate, channels=1, dtype='float32', device=output_device_index) as stream:
            stream.write(wave)
        print("Suono beep riprodotto.")
    except Exception as e:
        print(f"Errore durante la riproduzione del beep: {e}")

# Funzione per ascoltare la parola chiave
def listen_for_keyword():
    recognizer = KaldiRecognizer(model_vosk, samplerate)
    print("In ascolto della parola chiave... (e.g., 'Ciao')")
    try:
        with sd.RawInputStream(samplerate=samplerate, dtype='int16',
                               channels=1, callback=audio_callback, device=input_device_index,
                               blocksize=16000):
            while True:
                if not q.empty():
                    data = q.get()
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        detected_text = result.get('text', '').lower().strip()
                        if detected_text:
                            print("Rilevato:", detected_text)
                            if "ciao" in detected_text:
                                threading.Thread(target=play_beep).start()  # Avvia il beep in un thread separato
                                record_and_transcribe()
                else:
                    time.sleep(0.1)
    except Exception as e:
        print(f"Errore nell'apertura dello stream di input: {e}")

# Funzione per registrare e trascrivere audio
def record_and_transcribe(duration=5):
    print("Inizia a parlare...")
    try:
        sd.stop()  # Assicurati che lo stream precedente sia chiuso
        audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16', device=input_device_index)
        sd.wait()
        
        # Salva l'audio in un file WAV
        wavio.write("audio.wav", audio, samplerate, sampwidth=2)
        
        # Trascrivi l'audio con Whisper
        result = model_whisper.transcribe("audio.wav", language="it")
        print("Hai detto:", result["text"])
        print("Ritorno in ascolto della parola chiave... (e.g., 'Ciao')")
    except Exception as e:
        print(f"Errore durante la registrazione dell'audio: {e}")

# Avvia l'ascolto della parola chiave
listen_for_keyword()
