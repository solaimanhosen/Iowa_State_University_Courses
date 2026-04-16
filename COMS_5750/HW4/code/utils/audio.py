import math
import wave
import struct

FS            = 8000   # sampling rate (Hz)
DOT_MS        =   60   # 1 unit
DASH_MS       =  180   # 3 units
INTRA_GAP_MS  =   60   # 1 unit -- between elements of the same letter
LETTER_GAP_MS =  180   # 3 units -- between letters within a word
WORD_GAP_MS   =  420   # 7 units -- between words
FADE_MS       =    5   # cosine taper length (ms)
AMPLITUDE     =  0.8   # peak amplitude (0-1)

def ms_to_samples(ms):
    """Convert milliseconds to sample count at FS."""
    return int(FS * ms / 1000)

def sine_burst(freq, duration_ms):
    n_total = ms_to_samples(duration_ms)
    n_fade  = ms_to_samples(FADE_MS)
    samples = []
    for i in range(n_total):
        s = AMPLITUDE * math.sin(2 * math.pi * freq * i / FS)
        if i < n_fade:
            s *= 0.5 * (1 - math.cos(math.pi * i / n_fade))
        elif i >= n_total - n_fade:
            s *= 0.5 * (1 - math.cos(math.pi * (n_total - i) / n_fade))
        samples.append(s)
    return samples

def silence(duration_ms):
    return [0.0] * ms_to_samples(duration_ms)

def synthesize_sentence(text, freq):
    from utils.morse import MORSE_ENCODE

    words = text.upper().split()
    samples = []

    for w_idx, word in enumerate(words):
        if w_idx > 0:
            samples += silence(WORD_GAP_MS)

        for c_idx, char in enumerate(word):
            if c_idx > 0:
                samples += silence(LETTER_GAP_MS)

            code = MORSE_ENCODE.get(char, '')
            if not code:
                continue  # skip unknown characters

            for e_idx, symbol in enumerate(code):
                if e_idx > 0:
                    samples += silence(INTRA_GAP_MS)
                duration = DOT_MS if symbol == '.' else DASH_MS
                samples += sine_burst(freq, duration)

    return samples

def write_wav(filepath, samples, fs=FS):
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)       # 16-bit
        wf.setframerate(fs)
        for s in samples:
            clamped = max(-1.0, min(1.0, s))
            wf.writeframes(struct.pack('<h', int(clamped * 32767)))
