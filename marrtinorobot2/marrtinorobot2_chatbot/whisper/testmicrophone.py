import whisper
import sounddevice as sd
import numpy as np
import wavio

# Parametri di registrazione
duration = 5  # Durata della registrazione in secondi
samplerate = 16000  # Frequenza di campionamento

print("Inizia a parlare...")

# Registra l'audio
audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
sd.wait()

# Salva l'audio in un file WAV temporaneo
wavio.write("audio.wav", audio, samplerate, sampwidth=2)

# Carica il modello Whisper
model = whisper.load_model("base")

# Trascrivi l'audio registrato
result = model.transcribe("audio.wav", language="it")
print("Hai detto:", result["text"])
