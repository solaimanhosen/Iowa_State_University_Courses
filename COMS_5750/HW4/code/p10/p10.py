import os
import sys
import random

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT_DIR  = os.path.join(BASE_DIR, 'outputs', 'p10')
os.makedirs(OUT_DIR, exist_ok=True)

sys.path.insert(0, os.path.join(BASE_DIR, 'code'))

from utils.morse import ALPHABET
from utils.audio import synthesize_sentence, write_wav

# Reuse decoder from p8b
sys.path.insert(0, os.path.join(BASE_DIR, 'code', 'p8'))
from p8b import decode_sentence_file

def caesar_encrypt(text, shift=3):
    result = []
    for ch in text.upper():
        if ch in ALPHABET:
            result.append(ALPHABET[(ALPHABET.index(ch) + shift) % 26])
        else:
            result.append(ch)
    return ''.join(result)

if __name__ == '__main__':
    random.seed(42)

    INPUT_DIR = os.path.join(BASE_DIR, 'inputs', 'p10')

    print(f"{'File':<14} {'Orig freq':>10} {'New freq':>10}   {'Original text'}")
    print(f"{'':14} {'':10} {'':10}   {'Ciphered text'}")
    print('-' * 75)

    for idx in range(1, 3):
        in_path  = os.path.join(INPUT_DIR, f'message{idx}.wav')
        out_path = os.path.join(OUT_DIR,   f'message{idx}.wav')

        original_text, orig_freq, _, _ = decode_sentence_file(in_path)
        ciphered_text = caesar_encrypt(original_text, shift=3)
        new_freq = random.randint(500, 800)
        samples = synthesize_sentence(ciphered_text, new_freq)
        write_wav(out_path, samples)

        print(f"message{idx}.wav  {orig_freq:>10.1f} {new_freq:>10}   \"{original_text}\"")
        print(f"{'':14} {'':10} {'':10}   \"{ciphered_text}\"")
        print()

    print(f"Encrypted audio saved to: {OUT_DIR}")
