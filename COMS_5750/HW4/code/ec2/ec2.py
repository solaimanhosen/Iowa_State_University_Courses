import os
import sys
import wave
import struct

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT_DIR  = os.path.join(BASE_DIR, 'outputs', 'ec2')
os.makedirs(OUT_DIR, exist_ok=True)

sys.path.insert(0, os.path.join(BASE_DIR, 'code'))
from utils.audio import synthesize_sentence, FS

def overlay(samples_a, samples_b, gain=0.5):
    n = max(len(samples_a), len(samples_b))
    a = list(samples_a) + [0.0] * (n - len(samples_a))
    b = list(samples_b) + [0.0] * (n - len(samples_b))
    return [gain * a[i] + gain * b[i] for i in range(n)]

def write_wav(filepath, samples, fs=FS):
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        for s in samples:
            clamped = max(-1.0, min(1.0, s))
            wf.writeframes(struct.pack('<h', int(clamped * 32767)))

MESSAGES = [
    ('DO OR DO NOT THERE IS NO TRY', 550),
    ('A WAY THERE ALWAYS IS',        750),
]

if __name__ == '__main__':
    out_path = os.path.join(OUT_DIR, 'overlayed.wav')

    print('Synthesizing messages:')
    channels = []
    for text, freq in MESSAGES:
        samples = synthesize_sentence(text, freq)
        channels.append(samples)
        duration = len(samples) / FS
        print(f'  {freq} Hz  |  {duration:.2f}s  |  "{text}"')

    mixed = overlay(channels[0], channels[1], gain=0.5)
    duration_mixed = len(mixed) / FS

    write_wav(out_path, mixed)
    print(f'\nOverlayed audio saved to: {out_path}')
    print(f'Total duration: {duration_mixed:.2f}s')
