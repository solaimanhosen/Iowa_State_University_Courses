import os
import sys
import math
import soundfile as sf

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'code'))

from utils.signal import detect_carrier
from utils.plot import save_spectrogram_plot

MORSE_DOTS = {
    1: 'E',   # .
    2: 'I',   # ..
    3: 'S',   # ...
    4: 'H',   # ....
}

def rms_envelope(x, win_samples):
    energy = []
    for i in range(0, len(x) - win_samples, win_samples):
        chunk = x[i : i + win_samples]
        rms = math.sqrt(sum(v**2 for v in chunk) / win_samples)
        energy.append(rms)
    return energy

def decode_morse_file(filepath, win_ms=10, threshold_ratio=0.2):
    x_raw, fs = sf.read(filepath)
    x_np = x_raw if x_raw.ndim == 1 else x_raw[:, 0]
    x = x_np.tolist()

    carrier = detect_carrier(x_np, fs)

    # Energy envelope
    win_samples = max(1, int(fs * win_ms / 1000))
    energy = rms_envelope(x, win_samples)

    peak_energy = max(energy)
    threshold   = peak_energy * threshold_ratio

    # Count distinct bursts (on -> off transitions)
    n_dots = 0
    in_burst = False
    for e in energy:
        if e > threshold and not in_burst:
            n_dots += 1
            in_burst = True
        elif e <= threshold:
            in_burst = False

    letter = MORSE_DOTS.get(n_dots, '?')
    return letter, n_dots, carrier, energy, win_ms, fs, x_np

if __name__ == '__main__':
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs', 'p6')
    OUT_IMAGE = os.path.join(BASE_DIR, 'images', 'p6', 'out', 'p6a_detection.png')

    files = ['letter1.wav', 'letter2.wav', 'letter3.wav', 'letter4.wav']

    # print(f"{'File':<14} {'Dots':>6} {'Carrier (Hz)':>14} {'Letter':>8}")
    # print('-' * 46)

    all_results = []
    for fname in files:
        fpath = os.path.join(INPUT_DIR, fname)
        letter, n_dots, carrier, energy, win_ms, fs, x_np = decode_morse_file(fpath)
        # (fname, label, x_np, fs, carrier)
        all_results.append((fname, f'{letter} ({n_dots} dot{"s" if n_dots != 1 else ""})', x_np, fs, carrier))
        print(f"{'File':<14} {'Dots':>6} {'Carrier (Hz)':>14} {'Letter':>8}")
        print('-' * 46)
        print(f"{fname:<14} {n_dots:>6} {carrier:>14.1f} {letter:>8}\n\n")

    save_spectrogram_plot(all_results, OUT_IMAGE, title='Morse Code Dot Detection -- Spectrograms')
    print(f'\nSpectrogram plot saved to: {OUT_IMAGE}')
