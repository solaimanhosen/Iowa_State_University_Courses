import os
import sys
import soundfile as sf

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'code'))

from utils.morse import MORSE_TABLE, decode_segments
from utils.signal import detect_carrier, extract_segments
from utils.plot import save_spectrogram_plot

def make_threshold(durations):
    d_min, d_max = min(durations), max(durations)
    if d_max / d_min > 1.8:
        return (d_min + d_max) / 2.0
    # Single cluster: assume all are the same symbol type -- threshold
    # set above max so everything is classified as the shorter type.
    return d_max * 1.5

def decode_segments_two_level(segments):
    on_durs  = [d for typ, d in segments if typ == 'on']
    gap_durs = [d for typ, d in segments if typ == 'gap']

    on_thresh  = make_threshold(on_durs)
    gap_thresh = make_threshold(gap_durs) if gap_durs else float('inf')

    decoded = ''
    current_letter_symbols = ''

    for typ, dur in segments:
        if typ == 'on':
            current_letter_symbols += '.' if dur < on_thresh else '-'
        else:  # gap
            if dur >= gap_thresh:
                # Inter-letter boundary -- flush current letter
                decoded += MORSE_TABLE.get(current_letter_symbols, '?')
                current_letter_symbols = ''
            # Short gaps (intra-letter) are just ignored; symbols accumulate

    # Flush the last letter
    if current_letter_symbols:
        decoded += MORSE_TABLE.get(current_letter_symbols, '?')

    return decoded

def decode_word_file(filepath):
    x_raw, fs = sf.read(filepath)
    x_np = x_raw if x_raw.ndim == 1 else x_raw[:, 0]
    x = x_np.tolist()

    carrier = detect_carrier(x_np, fs)

    segments = extract_segments(x, fs)
    text = decode_segments_two_level(segments)

    return text, carrier, x_np, fs

if __name__ == '__main__':
    INPUT_DIR = os.path.join(BASE_DIR, 'inputs', 'p8')
    OUT_IMAGE = os.path.join(BASE_DIR, 'images', 'p8', 'out', 'p8a_detection.png')
    os.makedirs(os.path.dirname(OUT_IMAGE), exist_ok=True)

    files = [f'word{i}.wav' for i in range(1, 5)]

    all_results = []
    for fname in files:
        fpath = os.path.join(INPUT_DIR, fname)
        text, carrier, x_np, fs = decode_word_file(fpath)
        # (fname, label, x_np, fs, carrier)
        all_results.append((fname, text, x_np, fs, carrier))
        
        print(f"{'File':<12} {'Carrier (Hz)':>14}   {'Decoded Text'}")
        print('-' * 50)
        print(f"{fname:<12} {carrier:>14.1f}   {text}\n\n")

    save_spectrogram_plot(all_results, OUT_IMAGE, title='Morse Code Word Parsing -- Spectrograms')
    print(f'\nSpectrogram plot saved to: {OUT_IMAGE}\n\n')
