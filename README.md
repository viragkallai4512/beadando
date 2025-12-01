#ez a program mikrofont használ ami az elején be lett állitva nekem a 18-as ID-val létező mikrofon tömböt használja de lehet ez másnál más. 
Fő kód ami maga a a gitár hangoló:

import numpy as np

import sounddevice as sd

import os

import platform

import time

MIC_INDEX = 18
sd.default.device = (MIC_INDEX, None)

VOLUME_THRESHOLD = 0.00005

TARGET_NOTES = {
    "E2": 82.41,
    "A2": 110.00,
    "D3": 146.83,
    "G3": 196.00,
    "B3": 246.94,
    "E4": 329.63
}

SAMPLE_RATE = 44100
DURATION = 0.5
FREQ_THRESHOLD = 0.5  

TOLERANCE_OK = 1      
TOLERANCE_NEAR = 3    

def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def get_frequency():
    audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    samples = audio.flatten()
    volume = np.sqrt(np.mean(samples**2))
    if volume < VOLUME_THRESHOLD:
        return None
    fft = np.fft.fft(samples)
    freqs = np.fft.fftfreq(len(fft), 1/SAMPLE_RATE)
    idx = np.argmax(np.abs(fft[:len(fft)//2]))
    return abs(freqs[idx])

def needle(diff):
    scale = 20
    pos = int((diff/2 + 20) / 40 * scale)
    pos = max(0, min(scale, pos))
    line = ["-"] * (scale + 1)
    line[pos] = "|"
    return "".join(line)

def choose_string():
    while True:
        clear_console()
        print("🎸 Gitárhangoló")
        print("Válaszd ki a húrt (1-6) vagy Q a kilépéshez:")
        for i, note in enumerate(TARGET_NOTES.keys(), start=1):
            print(f"{i}. {note}")
        choice = input("> ").strip().upper()
        if choice == "Q":
            return None
        if choice in ["1","2","3","4","5","6"]:
            return list(TARGET_NOTES.keys())[int(choice)-1]
            
while True:
    note = choose_string()
    if note is None:
        print("Kiléptél a programból.")
        break




import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100
DURATION = 1  # másodperc

# Ha több mikrofon is van, ki lehet választani:
# print(sd.query_devices())
MIC_INDEX = 18  # itt állítsd be a megfelelő mikrofon ID-t
sd.default.device = (MIC_INDEX, None)

VOLUME_THRESHOLD = 0.00005

def get_frequency(audio):
    samples = audio.flatten()
    fft = np.fft.fft(samples)
    freqs = np.fft.fftfreq(len(fft), 1/SAMPLE_RATE)
    idx = np.argmax(np.abs(fft[:len(fft)//2]))
    return abs(freqs[idx])

print("🎤 Mikrofon teszt: beszélj vagy készíts hangot a mikrofonba...")

audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1)
sd.wait()

samples = audio.flatten()
volume = np.sqrt(np.mean(samples**2))
freq = get_frequency(audio)

print(f"Hangerő (RMS): {volume:.6f}")
if volume < VOLUME_THRESHOLD:
    print("❌ Nem érzékel hangot, ellenőrizd a mikrofont vagy a hangerőt.")
else:
    print("✅ Hang érzékelve!")
    print(f"Domináns frekvencia: {freq:.2f} Hz")
