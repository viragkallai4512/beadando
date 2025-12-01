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

target_freq = TARGET_NOTES[note]
    clear_console()
    print(f"🎵 Hangolás: {note} ({target_freq} Hz)")
    print("Pengetsd meg a húrt...")

 last_freq = None
    pengetes_kiirva = True 
    
while True:
        freq = get_frequency()
        if freq is None:
            continue

if last_freq is None:
            last_freq = freq

  if abs(freq - last_freq) < FREQ_THRESHOLD:
            continue

   diff = freq - target_freq

   if abs(diff) <= TOLERANCE_OK:
            direction = "ok"
        elif abs(diff) <= TOLERANCE_NEAR:
            direction = "near"
        elif diff > 0:
            direction = "down"
        else:
            direction = "up"

   print("\r" + " " * 80, end="")
        print("\r", end="")
        print(f"{needle(diff)} ", end="")

   if direction == "ok":
            print("✅ Hangolt húr!", end="")
            print()
            action = input("Visszalépsz a húrválasztáshoz (V) vagy kilépsz a programból (K)? [V/K]: ").strip().upper()
            if action == "V":
                break
            elif action == "K":
                print("Kiléptél a programból.")
                exit()
        elif direction == "near":
            print("🔹 Közel jó, finomhangolj!", end="")
        elif direction == "down":
            print("⬇️ Engedni kell a húrt!", end="")
        else:
            print("⬆️ Húzni kell a húrt!", end="")

  last_freq = freq
        time.sleep(0.1)

ez pedig az ahol amivel a megfelelő mikrofont amit használ a program azzal kerestem meg (lehet mindenkinek más és azért raktam be); 

import sounddevice as sd
import numpy as np

DURATION = 0.3   # 300 ms felvétel

def list_devices():
    print("Elérhető eszközök:")
    print(sd.query_devices())

def test_mic(device_id=None):
    print("Mikrofon teszt indul...")

while True:
        audio = sd.rec(int(DURATION * 44100),
                       samplerate=44100,
                       channels=1,
                       device=device_id)
        sd.wait()

volume = np.sqrt(np.mean(audio**2))

 print(f"Hangerő: {volume}")

# --- FUTTATÁS ---
if __name__ == "__main__":
    print("Először listázzuk az eszközöket:")
    list_devices()

print("\nAdd meg a mikrofon device ID-ját (Enter = alapértelmezett):")
    inp = input("> ")

 if inp.strip() == "":
        test_mic(None)
    else:
        test_mic(int(inp))
