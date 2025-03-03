import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import whisper
import wavio
import numpy as np

# Path to the Vosk Italian model
model_path = "../models/vosk-model-it-0.22"
model_vosk = Model(model_path)

# Load the Whisper model
model_whisper = whisper.load_model("base")

# Audio recording parameters
samplerate = 16000
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

# Function to play a beep sound
def play_beep(frequency=1000, duration=0.5, volume=0.5):
    samplerate = 44100
    t = np.linspace(0, duration, int(samplerate * duration), False)
    wave = volume * np.sin(2 * np.pi * frequency * t)
    sd.play(wave, samplerate)
    sd.wait()

# Function to listen for the keyword
def listen_for_keyword():
    recognizer = KaldiRecognizer(model_vosk, samplerate)
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        print("Listening for the keyword... (e.g., 'Ciao')")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                detected_text = result.get('text', '').lower()
                if "ciao" in detected_text:
                    play_beep()  # Play beep sound instead of a text message
                    record_and_transcribe()

# Function to record and transcribe audio
def record_and_transcribe(duration=5):
    print("Start speaking...")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    
    # Save the audio to a WAV file
    wavio.write("audio.wav", audio, samplerate, sampwidth=2)
    
    # Transcribe the audio with Whisper
    result = model_whisper.transcribe("audio.wav", language="it")
    print("You said:", result["text"])

# Start listening for the keyword
listen_for_keyword()
