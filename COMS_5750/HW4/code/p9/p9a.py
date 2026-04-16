import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT_DIR  = os.path.join(BASE_DIR, 'outputs', 'p9')
os.makedirs(OUT_DIR, exist_ok=True)

sys.path.insert(0, os.path.join(BASE_DIR, 'code'))

from utils.morse import MORSE_ENCODE as MORSE_TABLE
from utils.audio import (
    FS, DOT_MS, DASH_MS, INTRA_GAP_MS,
    sine_burst, silence, write_wav,
)

# Alias INTRA_GAP_MS as GAP_MS for clarity in this file
GAP_MS = INTRA_GAP_MS

def synthesize_char(char, freq):
    code = MORSE_TABLE.get(char.upper(), '')
    if not code:
        raise ValueError(f"Unknown character: {char!r}")

    samples = []
    for idx, symbol in enumerate(code):
        if idx > 0:
            samples += silence(GAP_MS)          # intra-element gap
        duration = DOT_MS if symbol == '.' else DASH_MS
        samples += sine_burst(freq, duration)

    return samples

INPUTS = [
    ('N', 800),
    ('O', 750),
    ('P', 600),
    ('3', 575),
]

if __name__ == '__main__':
    print(f"{'Output file':<16} {'Char':>6} {'Freq (Hz)':>10} {'Morse code':>12}")
    print('-' * 48)

    for idx, (char, freq) in enumerate(INPUTS, start=1):
        code    = MORSE_TABLE[char.upper()]
        samples = synthesize_char(char, freq)
        out_path = os.path.join(OUT_DIR, f'char{idx}.wav')
        write_wav(out_path, samples)
        print(f"char{idx}.wav          {char:>6} {freq:>10}   {code:>12}")

    print(f'\nAll files saved to: {OUT_DIR}')
