import numpy as np
from scipy.signal import spectrogram as scipy_spectrogram
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def save_spectrogram_plot(all_results, out_path, title='Morse Code -- Spectrograms'):
    n = len(all_results)
    fig, axes = plt.subplots(n, 1, figsize=(12, 3 * n))
    if n == 1:
        axes = [axes]

    for ax, (fname, label, x_np, fs, carrier) in zip(axes, all_results):
        f, t, Sxx = scipy_spectrogram(x_np, fs=fs, nperseg=256, noverlap=192, nfft=512)
        Sxx_dB = 10 * np.log10(Sxx + 1e-10)
        peak = Sxx_dB.max()

        ax.pcolormesh(t, f, Sxx_dB, shading='gouraud',
                      vmin=peak - 60, vmax=peak, cmap='inferno')
        ax.axhline(carrier, color='cyan', linestyle='--', linewidth=0.8,
                   label=f'carrier {carrier:.0f} Hz')
        ax.set_ylim(0, fs / 2)
        ax.set_ylabel('Freq (Hz)')
        ax.legend(loc='upper right', fontsize=7)
        ax.set_title(f'{fname}  ->  "{label}"  | carrier {carrier:.0f} Hz', fontsize=9)

    axes[-1].set_xlabel('Time (s)')
    fig.suptitle(title, fontsize=11)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
