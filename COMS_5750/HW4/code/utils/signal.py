import math
import numpy as np

def detect_carrier(x_np, fs):
    mid = len(x_np) // 2
    segment = x_np[mid : mid + min(2048, len(x_np) - mid)]
    X_mag = np.abs(np.fft.rfft(segment))
    freqs = np.fft.rfftfreq(len(segment), 1.0 / fs)
    return float(freqs[np.argmax(X_mag)])

def extract_segments(x, fs, win_ms=5, threshold_ratio=0.2):
    win = max(1, int(fs * win_ms / 1000))
    energy = []
    for i in range(0, len(x) - win, win):
        chunk = x[i : i + win]
        rms = math.sqrt(sum(v**2 for v in chunk) / win)
        energy.append(rms)

    threshold = max(energy) * threshold_ratio
    segments = []
    in_burst = False
    seg_start = 0.0

    for j, e in enumerate(energy):
        t = j * win_ms / 1000.0
        if e > threshold and not in_burst:
            if j > 0:
                segments.append(('gap', t - seg_start))
            seg_start = t
            in_burst = True
        elif e <= threshold and in_burst:
            segments.append(('on', t - seg_start))
            seg_start = t
            in_burst = False

    if in_burst:
        segments.append(('on', len(energy) * win_ms / 1000.0 - seg_start))

    return segments


def classify_bursts(burst_durations, gap_durations):
    d_min = min(burst_durations)
    d_max = max(burst_durations)

    if d_max / d_min > 1.8:
        # Mixed: clear two clusters -- use midpoint threshold
        threshold = (d_min + d_max) / 2.0
        return ''.join('.' if d < threshold else '-' for d in burst_durations)
    else:
        # All same duration -- use burst-to-gap ratio to decide dot vs dash
        avg_burst = sum(burst_durations) / len(burst_durations)
        avg_gap   = sum(gap_durations) / len(gap_durations) if gap_durations else avg_burst
        ratio = avg_burst / avg_gap
        symbol = '.' if ratio < 2.0 else '-'
        return symbol * len(burst_durations)
