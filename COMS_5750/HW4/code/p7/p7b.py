import os
import sys
import soundfile as sf

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'code'))

from utils.morse import MORSE_ALPHA
from utils.signal import detect_carrier, extract_segments, classify_bursts
from utils.plot import save_spectrogram_plot

def detect_bursts(x, fs, win_ms=5, threshold_ratio=0.2):
    """Return burst durations and inter-burst gap durations (in seconds)."""
    segs = extract_segments(x, fs, win_ms=win_ms, threshold_ratio=threshold_ratio)
    bursts = [d for typ, d in segs if typ == 'on']
    gaps   = [d for typ, d in segs if typ == 'gap']
    return bursts, gaps

def decode_letter_file(filepath):
    x_raw, fs = sf.read(filepath)
    x_np = x_raw if x_raw.ndim == 1 else x_raw[:, 0]
    x = x_np.tolist()

    carrier = detect_carrier(x_np, fs)

    bursts, gaps = detect_bursts(x, fs)
    sequence = classify_bursts(bursts, gaps)
    letter = MORSE_ALPHA.get(sequence, '?')

    return letter, sequence, carrier, x_np, fs

if __name__ == '__main__':
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs', 'p7')
    OUT_IMAGE = os.path.join(BASE_DIR, 'images', 'p7', 'out', 'p7b_detection.png')
    os.makedirs(os.path.dirname(OUT_IMAGE), exist_ok=True)

    files = [f'letter{i}.wav' for i in range(1, 6)]


    all_results = []
    for fname in files:
        fpath = os.path.join(INPUT_DIR, fname)
        letter, seq, carrier, x_np, fs = decode_letter_file(fpath)
        # (fname, label, x_np, fs, carrier)
        all_results.append((fname, f'{letter} ({seq})', x_np, fs, carrier))

        print(f"{'File':<14} {'Sequence':<8} {'Carrier (Hz)':>14} {'Letter':>8}")
        print('-' * 48)
        print(f"{fname:<14} {seq:<8} {carrier:>14.1f} {letter:>8}\n\n")

    save_spectrogram_plot(all_results, OUT_IMAGE, title='Morse Code Letter Recognition -- Spectrograms')
    print(f'\nSpectrogram plot saved to: {OUT_IMAGE}')
