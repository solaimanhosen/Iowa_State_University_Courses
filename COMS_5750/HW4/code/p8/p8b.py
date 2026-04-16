import os
import sys
import soundfile as sf

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'code'))

from utils.morse import decode_segments
from utils.signal import detect_carrier, extract_segments
from utils.plot import save_spectrogram_plot

def decode_sentence_file(filepath):
    x_raw, fs = sf.read(filepath)
    x_np = x_raw if x_raw.ndim == 1 else x_raw[:, 0]
    x = x_np.tolist()

    carrier = detect_carrier(x_np, fs)

    segments = extract_segments(x, fs)
    text = decode_segments(segments)

    return text, carrier, x_np, fs

if __name__ == '__main__':
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs', 'p8')
    OUT_IMAGE = os.path.join(BASE_DIR, 'images', 'p8', 'out', 'p8b_detection.png')
    os.makedirs(os.path.dirname(OUT_IMAGE), exist_ok=True)

    files = [f'sentence{i}.wav' for i in range(1, 5)]

    all_results = []
    for fname in files:
        fpath = os.path.join(INPUT_DIR, fname)
        text, carrier, x_np, fs = decode_sentence_file(fpath)
        # (fname, label, x_np, fs, carrier)
        all_results.append((fname, text, x_np, fs, carrier))

        print(f"{'File':<16} {'Carrier (Hz)':>14}   {'Decoded Text'}")
        print('-' * 70)
        print(f"{fname:<16} {carrier:>14.1f}   {text}\n\n")

    save_spectrogram_plot(all_results, OUT_IMAGE, title='Morse Code Sentence Parsing -- Spectrograms')
    print(f'\nSpectrogram plot saved to: {OUT_IMAGE}\n\n')
