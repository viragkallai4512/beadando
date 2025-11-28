#ez a program mikrofont használ ami az elején be lett állitva nekem a 18-as ID-val létező mikrofon tömböt használja de lehet ez másnál más. Ezzel a kis #egyszerű kóddal ellenörizheti melyikkel müködik a a hangoló: 


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
