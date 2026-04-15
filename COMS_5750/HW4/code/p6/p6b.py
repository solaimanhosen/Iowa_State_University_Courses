import os
import sys
import math
import soundfile as sf

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'code'))

from utils.signal import detect_carrier
from utils.plot import save_spectrogram_plot

MORSE_DASHES = {
    1: 'T',   # -
    2: 'M',   # --
    3: 'O',   # ---
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
    n_dashes = 0
    in_burst = False
    for e in energy:
        if e > threshold and not in_burst:
            n_dashes += 1
            in_burst = True
        elif e <= threshold:
            in_burst = False

    letter = MORSE_DASHES.get(n_dashes, '?')
    return letter, n_dashes, carrier, energy, win_ms, fs, x_np

if __name__ == '__main__':
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs', 'p6')
    OUT_IMAGE = os.path.join(BASE_DIR, 'images', 'p6', 'out', 'p6b_detection.png')

    files = ['letter5.wav', 'letter6.wav', 'letter7.wav']

    # print(f"{'File':<14} {'Dashes':>8} {'Carrier (Hz)':>14} {'Letter':>8}")
    # print('-' * 48)

    all_results = []
    for fname in files:
        fpath = os.path.join(INPUT_DIR, fname)
        letter, n_dashes, carrier, energy, win_ms, fs, x_np = decode_morse_file(fpath)
        # (fname, label, x_np, fs, carrier)
        all_results.append((fname, f'{letter} ({n_dashes} dash{"es" if n_dashes != 1 else ""})', x_np, fs, carrier))
        
        print(f"{'File':<14} {'Dashes':>8} {'Carrier (Hz)':>14} {'Letter':>8}")
        print('-' * 48)
        
        print(f"{fname:<14} {n_dashes:>8} {carrier:>14.1f} {letter:>8}\n\n")

    save_spectrogram_plot(all_results, OUT_IMAGE, title='Morse Code Dash Detection -- Spectrograms')
    print(f'\nSpectrogram plot saved to: {OUT_IMAGE}')
