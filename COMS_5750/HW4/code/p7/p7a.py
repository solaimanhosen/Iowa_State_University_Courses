import os
import sys
import math
import soundfile as sf

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'code'))

from utils.signal import detect_carrier, extract_segments, classify_bursts
from utils.plot import save_spectrogram_plot

MORSE_DIGITS = {
    '-----': 0,
    '.----': 1,
    '..---': 2,
    '...--': 3,
    '....-': 4,
    '.....': 5,
    '-....': 6,
    '--...': 7,
    '---..' : 8,
    '----.': 9,
}

def detect_bursts(x, fs, win_ms=5, threshold_ratio=0.2):
    segs = extract_segments(x, fs, win_ms=win_ms, threshold_ratio=threshold_ratio)
    bursts = [d for typ, d in segs if typ == 'on']
    gaps   = [d for typ, d in segs if typ == 'gap']
    return bursts, gaps

def decode_number_file(filepath):
    x_raw, fs = sf.read(filepath)
    x_np = x_raw if x_raw.ndim == 1 else x_raw[:, 0]
    x = x_np.tolist()

    carrier = detect_carrier(x_np, fs)

    bursts, gaps = detect_bursts(x, fs)
    sequence = classify_bursts(bursts, gaps)
    digit = MORSE_DIGITS.get(sequence, None)

    return digit, sequence, carrier, x_np, fs

if __name__ == '__main__':
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs', 'p7')
    OUT_IMAGE = os.path.join(BASE_DIR, 'images', 'p7', 'out', 'p7a_detection.png')
    os.makedirs(os.path.dirname(OUT_IMAGE), exist_ok=True)

    files = [f'number{i}.wav' for i in range(1, 6)]

    # print(f"{'File':<14} {'Sequence':<10} {'Carrier (Hz)':>14} {'Digit':>7}")
    # print('-' * 49)

    all_results = []
    for fname in files:
        fpath = os.path.join(INPUT_DIR, fname)
        digit, seq, carrier, x_np, fs = decode_number_file(fpath)
        label = str(digit) if digit is not None else '?'
        # (fname, label, x_np, fs, carrier)
        all_results.append((fname, f'{label} ({seq})', x_np, fs, carrier))

        print(f"{'File':<14} {'Sequence':<10} {'Carrier (Hz)':>14} {'Digit':>7}")
        print('-' * 49)
        print(f"{fname:<14} {seq:<10} {carrier:>14.1f} {label:>7}\n\n")

    save_spectrogram_plot(all_results, OUT_IMAGE, title='Morse Code Number Recognition -- Spectrograms')
    print(f'\nSpectrogram plot saved to: {OUT_IMAGE}')
