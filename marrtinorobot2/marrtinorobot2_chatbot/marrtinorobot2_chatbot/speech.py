import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import numpy as np
import time
import threading
from gtts import gTTS
import io
import soundfile as sf

# Percorso al modello Vosk in italiano
model_path = "../models/vosk-model-it-0.22"
model_vosk = Model(model_path)

# Frequenze di campionamento
input_samplerate = 16000  # Frequenza supportata dal ReSpeaker
output_samplerate = 44100  # Frequenza supportata dall'HDMI
q = queue.Queue()

# Indici dei dispositivi audio
input_device_index = 5  # ReSpeaker 4-Mic Array come input
output_device_index = 6  # Dispositivo HDMI come output

# Imposta il dispositivo di input su ReSpeaker e di output su HDMI
sd.default.device = (input_device_index, output_device_index)

# Variabile globale per interrompere il flusso audio
stop_listening = False
listening_active = True  # Controlla se il microfono è attivo

# Funzione di callback per aggiungere i dati audio alla coda
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    if listening_active:
        q.put(bytes(indata))

# Funzione per riprodurre un suono beep
def play_beep(frequency=1000, duration=0.5, volume=0.5):
    t = np.linspace(0, duration, int(output_samplerate * duration), False)
    wave = (volume * np.sin(2 * np.pi * frequency * t)).astype(np.float32)
    
    try:
        with sd.OutputStream(samplerate=output_samplerate, channels=1, dtype='float32', device=output_device_index) as stream:
            stream.write(wave)
        print("Suono beep riprodotto.")
    except Exception as e:
        print(f"Errore durante la riproduzione del beep: {e}")

# Funzione per riprodurre l'audio TTS con gTTS
def play_tts(text, lang="it"):
    global listening_active
    try:
        # Disabilita temporaneamente il microfono
        listening_active = False
        
        tts = gTTS(text=text, lang=lang)
        audio_data = io.BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)

        # Leggi i dati audio dalla memoria e forza la frequenza di campionamento a 44100 Hz
        data, samplerate = sf.read(audio_data, dtype='float32')
        if samplerate != output_samplerate:
            print(f"Frequenza di campionamento TTS non corretta ({samplerate} Hz), adattamento a {output_samplerate} Hz.")
            # Interpolazione e conversione a float32
            data = np.interp(
                np.linspace(0, len(data), int(len(data) * output_samplerate / samplerate)),
                np.arange(len(data)),
                data
            ).astype(np.float32)

        # Riproduci l'audio con sounddevice
        with sd.OutputStream(samplerate=output_samplerate, channels=1, dtype='float32', device=output_device_index) as stream:
            stream.write(data)
        
        print(f"Riproduzione TTS: {text}")
    except Exception as e:
        print(f"Errore durante la riproduzione TTS: {e}")
    finally:
        # Riattiva il microfono
        listening_active = True

# Funzione per ascoltare la parola chiave
def listen_for_keyword():
    global stop_listening
    recognizer = KaldiRecognizer(model_vosk, input_samplerate)
    print("In ascolto della parola chiave... (e.g., 'Ciao')")
    try:
        with sd.RawInputStream(samplerate=input_samplerate, dtype='int16',
                               channels=1, callback=audio_callback, device=input_device_index,
                               blocksize=16000):
            while not stop_listening:
                if not q.empty():
                    data = q.get()
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        deteccdted_text = result.get('text', '').lower().strip()
                        if detected_text:
                            print("Rilevato:", detected_text)
                            if "ciao" in detected_text:
                                threading.Thread(target=play_beep).start()
                                play_tts("Come posso aiutarti?")
                            if "gpt" in detected_text:
                                play_tts("tutti parlano di intelligenza artificiale ma riusciamo a fare la domanda giusta senza chiederlo a chatgpt")
                            if "cosa sai fare" in detected_text:
                                play_tts("vallo a chiedere a tua sorella")
                            if "cosa sei" in detected_text:
                                play_tts("il primo robot con deficenza artificiale")
                            elif "stop" in detected_text:
                                play_tts("Dispositivo in arresto. Arrivederci!")
                                stop_listening = True
                                break
                else:
                    time.sleep(0.1)
    except Exception as e:
        print(f"Errore nell'apertura dello stream di input: {e}")

# Avvia l'ascolto della parola chiave
play_beep(700, 0.3, 0.3)
listen_for_keyword()
