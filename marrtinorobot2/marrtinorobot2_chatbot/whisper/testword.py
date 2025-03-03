import pvporcupine
import sounddevice as sd
import whisper
import numpy as np
import wavio

# Configura Porcupine con la parola chiave personalizzata
porcupine = pvporcupine.create(keywords=["hey google", "computer"])  # Puoi sostituire con altre parole chiave supportate

# Parametri di registrazione
samplerate = 16000
duration = 5  # Durata della registrazione (in secondi) dopo il trigger
audio_filename = "audio.wav"

# Modello Whisper
model = whisper.load_model("base")

def audio_callback(indata, frames, time, status):
    pcm = np.frombuffer(indata, dtype=np.int16)
    keyword_index = porcupine.process(pcm)
    if keyword_index >= 0:
        print("Parola chiave rilevata! Inizia la registrazione...")
        record_and_transcribe()

def record_and_transcribe():
    # Registra l'audio per la durata specificata
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    
    # Salva l'audio in un file WAV
    wavio.write(audio_filename, audio, samplerate, sampwidth=2)
    
    # Trascrivi l'audio con Whisper
    result = model.transcribe(audio_filename, language="it")
    print("Hai detto:", result["text"])

# Avvia lo streaming audio
with sd.InputStream(callback=audio_callback, channels=1, samplerate=samplerate, blocksize=porcupine.frame_length, dtype='int16'):
    print("In ascolto della parola chiave... (es. 'Ehi Marrtino')")
    while True:
        pass
