import numpy as np
import sounddevice as sd

# Gitár húrok (EADGBE) referenciafrekvenciái
TARGET_NOTES = {
    "E2": 82.41,
    "A2": 110.00,
    "D3": 146.83,
    "G3": 196.00,
    "B3": 246.94,
    "E4": 329.63
}

SAMPLE_RATE = 44100
DURATION = 0.5  # másodperc – ennyi hangmintát elemezünk

def get_frequency():
    """Felvesz fél másodperc mikrofonhangot, és meghatározza a legerősebb frekvenciát."""
    print("🎤 Hallgatom a hangot... (pengetsd meg a húrt)")
    audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()

    # Átalakítás és FFT
    samples = audio.flatten()
    fft = np.fft.fft(samples)
    freqs = np.fft.fftfreq(len(fft), 1/SAMPLE_RATE)

    # Csak pozitív frekvenciák
    idx = np.argmax(np.abs(fft[:len(fft)//2]))
    dominant_freq = abs(freqs[idx])
    return dominant_freq

def needle(diff):
    """Egyszerű ASCII tű, bal = engedni, jobb = húzni."""
    scale = 20  # ennyi karakter széles a skála
    pos = int((diff + 20) / 40 * scale)  # diff -20Hz és +20Hz között várható
    pos = max(0, min(scale, pos))

    line = ["-"] * (scale + 1)
    if 0 <= pos <= scale:
        line[pos] = "|"

    return "".join(line)

print("🎸 Gitárhangoló indítva!")
print("Válaszd ki, melyik húrt hangolod:")

for i, note in enumerate(TARGET_NOTES.keys(), start=1):
    print(f"{i}. {note}")

choice = int(input("Húrszám (1-6): "))
note = list(TARGET_NOTES.keys())[choice - 1]
target_freq = TARGET_NOTES[note]

print(f"\nA(z) {note} húr referenciafrekvenciája: {target_freq} Hz")
print("Pengetsd meg a húrt...")

while True:
    freq = get_frequency()
    diff = freq - target_freq

    print(f"\n🎵 Mért frekvencia: {freq:.2f} Hz")
    print(needle(diff))

    if abs(diff) < 1:
        print("✅ Jó hangolás!")
    elif diff > 0:
        print("⬇️ Engedni kell a húrt!")
    else:
        print("⬆️ Húzni kell a húrt!")

    print("\n(CTRL+C a kilépéshez)\n")
