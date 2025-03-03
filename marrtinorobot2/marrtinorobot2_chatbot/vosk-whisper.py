import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import whisper
import wavio

# Percorso al modello Vosk in italiano
model_path = "./model/vosk-model-it-0.22"
model_vosk = Model(model_path)

# Carica il modello Whisper
model_whisper = whisper.load_model("base")

# Parametri di registrazione audio
samplerate = 16000
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

# Funzione per ascoltare la parola chiave
def ascolta_parola_chiave():
    recognizer = KaldiRecognizer(model_vosk, samplerate)
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        print("In ascolto della parola chiave... (es. 'Ehi Marrtino')")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                testo_rilevato = result.get('text', '').lower()
                if "ciao" in testo_rilevato:
                    print("Parola chiave rilevata! Inizia la registrazione...")
                    registra_e_trascrivi()

# Funzione per registrare e trascrivere l'audio
def registra_e_trascrivi(durata=5):
    print("Parla ora...")
    audio = sd.rec(int(samplerate * durata), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    
    # Salva l'audio in un file WAV
    wavio.write("audio.wav", audio, samplerate, sampwidth=2)
    
    # Trascrivi l'audio con Whisper
    risultato = model_whisper.transcribe("audio.wav", language="it")
    print("Hai detto:", risultato["text"])

# Avvia l'ascolto della parola chiave
ascolta_parola_chiave()
