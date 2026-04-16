import os
import sys
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, spectrogram as scipy_spectrogram
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'code'))
sys.path.insert(0, os.path.join(BASE_DIR, 'code', 'p8'))

from p8b import decode_sentence_file as _decode_sf
from utils.signal import extract_segments
from utils.morse import decode_segments

def find_carriers(x_np, fs, n_carriers=2, min_separation_hz=100):
    X_mag = np.abs(np.fft.rfft(x_np))
    freqs = np.fft.rfftfreq(len(x_np), 1.0 / fs)

    carriers = []
    X_search = X_mag.copy()

    while len(carriers) < n_carriers:
        peak_idx = np.argmax(X_search)
        peak_freq = freqs[peak_idx]
        carriers.append(float(peak_freq))

        # Suppress the region around this peak so next search finds the other one
        suppress = np.abs(freqs - peak_freq) < min_separation_hz
        X_search[suppress] = 0.0

    return sorted(carriers)

def bandpass_filter(x_np, fs, center_hz, bandwidth_hz=100, order=5):
    nyq = fs / 2.0
    low  = max(1e-4, (center_hz - bandwidth_hz / 2) / nyq)
    high = min(0.999, (center_hz + bandwidth_hz / 2) / nyq)
    sos = butter(order, [low, high], btype='band', output='sos')
    return sosfilt(sos, x_np)

def decode_array(x_np, fs):
    segments = extract_segments(x_np.tolist(), fs)
    return decode_segments(segments)

def save_plot(x_np, filtered_signals, carriers, texts, fs, out_path):
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))

    def plot_spec(ax, sig, title):
        f, t, Sxx = scipy_spectrogram(sig, fs=fs, nperseg=256, noverlap=192, nfft=512)
        Sxx_dB = 10 * np.log10(Sxx + 1e-10)
        peak = Sxx_dB.max()
        ax.pcolormesh(t, f, Sxx_dB, shading='gouraud',
                      vmin=peak - 60, vmax=peak, cmap='inferno')
        ax.set_ylim(0, fs / 2)
        ax.set_ylabel('Freq (Hz)')
        ax.set_title(title, fontsize=9)

    plot_spec(axes[0], x_np, 'Overlapped signal (both messages)')
    for ax, sig, c, txt in zip(axes[1:], filtered_signals, carriers, texts):
        ax.axhline(c, color='cyan', linestyle='--', linewidth=0.8)
        plot_spec(ax, sig, f'Carrier ≈ {c:.0f} Hz  →  "{txt}"')
        ax.axhline(c, color='cyan', linestyle='--', linewidth=0.8,
                   label=f'{c:.0f} Hz')
        ax.legend(loc='upper right', fontsize=7)

    axes[-1].set_xlabel('Time (s)')
    fig.suptitle('EC1: Overlapped Morse Code — Split and Decoded', fontsize=11)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    print(f'Spectrogram saved to: {out_path}')

if __name__ == '__main__':
    INPUT_FILE = os.path.join(BASE_DIR, 'inputs', 'ec1', 'overlayed.wav')
    OUT_DIR    = os.path.join(BASE_DIR, 'images', 'ec1', 'out')
    os.makedirs(OUT_DIR, exist_ok=True)
    OUT_IMAGE  = os.path.join(OUT_DIR, 'ec1_detection.png')

    # Load
    x_raw, fs = sf.read(INPUT_FILE)
    x_np = x_raw if x_raw.ndim == 1 else x_raw[:, 0]
    print(f'Loaded: {INPUT_FILE}')
    print(f'  fs={fs} Hz, duration={len(x_np)/fs:.2f}s\n')

    # Find carriers
    carriers = find_carriers(x_np, fs, n_carriers=2)
    print(f'Detected carrier frequencies: {[f"{c:.1f} Hz" for c in carriers]}\n')

    # Bandpass + decode each channel
    filtered_signals = []
    decoded_texts    = []

    print(f"{'Carrier (Hz)':>14}   {'Decoded Message'}")
    print('-' * 70)

    for c in carriers:
        filtered = bandpass_filter(x_np, fs, center_hz=c, bandwidth_hz=120)
        filtered_signals.append(filtered)
        text = decode_array(filtered, fs)
        decoded_texts.append(text)
        print(f'{c:>14.1f}   "{text}"\n')

    # Save spectrogram
    save_plot(x_np, filtered_signals, carriers, decoded_texts, fs, OUT_IMAGE)
