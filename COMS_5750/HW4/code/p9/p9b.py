import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT_DIR  = os.path.join(BASE_DIR, 'outputs', 'p9')
os.makedirs(OUT_DIR, exist_ok=True)

sys.path.insert(0, os.path.join(BASE_DIR, 'code'))

from utils.audio import FS, synthesize_sentence, write_wav

INPUTS = [
    ('HOMEWORK FOUR 5750', 625),
    ('WORKING WITH AUDIO IS FUN', 775),
]

if __name__ == '__main__':
    print(f"{'Output file':<16} {'Freq (Hz)':>10}   {'Text'}")
    print('-' * 65)

    for idx, (text, freq) in enumerate(INPUTS, start=1):
        samples  = synthesize_sentence(text, freq)
        out_path = os.path.join(OUT_DIR, f'sentence{idx}.wav')
        write_wav(out_path, samples)
        duration = len(samples) / FS
        print(f"sentence{idx}.wav      {freq:>10}   {text}  ({duration:.2f}s)")

    print(f'\nAll files saved to: {OUT_DIR}')
