import os
import sys
import math
import soundfile as sf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'code', 'p3'))
from p3a import fft

def next_pow2(n):
    p = 1
    while p < n:
        p <<= 1
    return p

def hamming(M):
    if M == 1:
        return [1.0]
    return [0.54 - 0.46 * math.cos(2 * math.pi * k / (M - 1)) for k in range(M)]

def custom_spectrogram(x, fs, win_len, noverlap, nfft):
    N = len(x)
    hop = win_len - noverlap
    win = hamming(win_len)
    num_freqs = nfft // 2 + 1
    num_frames = (N - noverlap) // hop

    S = []
    for i in range(num_frames):
        idx_start = i * hop

        # Extract frame; zero-pad at signal boundary
        frame = [0.0] * win_len
        for k in range(win_len):
            idx = idx_start + k
            if idx < N:
                frame[k] = float(x[idx])

        # Apply Hamming window
        frame = [frame[k] * win[k] for k in range(win_len)]

        # Zero-pad to nfft
        frame_padded = frame + [0.0] * (nfft - win_len)

        # FFT via Part 3a
        X = fft(frame_padded)

        # One-sided magnitude
        S.append([abs(X[k]) for k in range(num_freqs)])

    # Transpose to [num_freqs x num_frames]
    S_T = [[S[col][row] for col in range(num_frames)] for row in range(num_freqs)]

    f = [k * fs / nfft for k in range(num_freqs)]
    t = [(i * hop + win_len / 2) / fs for i in range(num_frames)]

    return S_T, f, t

if __name__ == '__main__':
    # Load audio
    # INPUT_FILE = os.path.join(BASE_DIR, 'inputs', 'p5', 'siren.wav')
    INPUT_FILE = os.path.join(BASE_DIR, 'inputs', 'p5', 'custom2.wav')
    x_raw, fs = sf.read(INPUT_FILE)
    x = x_raw.tolist() if x_raw.ndim == 1 else x_raw[:, 0].tolist()
    N = len(x)

    print('=== Audio File Info ===')
    print(f'  File:          {os.path.basename(INPUT_FILE)}')
    print(f'  Sampling rate: {fs} Hz')
    print(f'  Num samples:   {N}')
    print(f'  Duration:      {N/fs:.4f} s')

    # Compute parameters matching MATLAB defaults
    win_len  = max(1, N // 8)
    noverlap = win_len // 2
    hop      = win_len - noverlap
    nfft     = max(256, next_pow2(win_len))

    print('\n=== Spectrogram Parameters ===')
    print(f'  Window type:   Hamming')
    print(f'  Window length: {win_len} samples ({win_len/fs:.4f} s)')
    print(f'  Overlap:       {noverlap} samples (50%)')
    print(f'  Hop size:      {hop} samples')
    print(f'  NFFT:          {nfft}')

    # Compute spectrogram
    print('\nComputing spectrogram...')
    S, f, t = custom_spectrogram(x, fs, win_len, noverlap, nfft)

    # Convert to dB
    eps = 1e-10
    S_dB = [[10 * math.log10(S[r][c] ** 2 + eps)
             for c in range(len(t))]
            for r in range(len(f))]

    peak_dB = max(v for row in S_dB for v in row)
    vmin = peak_dB - 60
    vmax = peak_dB

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    img = ax.imshow(
        S_dB,
        aspect='auto',
        origin='lower',
        extent=[t[0], t[-1], f[0], f[-1]],
        vmin=vmin, vmax=vmax,
        cmap='inferno'
    )
    cbar = fig.colorbar(img, ax=ax)
    cbar.set_label('Power (dB)')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_title(
        f'Spectrogram of {os.path.basename(INPUT_FILE)}  |  fs={fs} Hz, '
        f'win={win_len}, overlap=50%, NFFT={nfft}'
    )

    OUT_FILE = os.path.join(BASE_DIR, 'images', 'p5', 'out', f'{os.path.splitext(os.path.basename(INPUT_FILE))[0]}_spectrogram.png')
    fig.tight_layout()
    fig.savefig(OUT_FILE, dpi=150)
    print(f'\nSpectrogram saved to: {OUT_FILE}')
