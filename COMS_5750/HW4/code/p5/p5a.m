%% Load audio file
% [x, fs] = audioread('../../inputs/p5/ramp.wav');
[x, fs] = audioread('../../inputs/p5/custom1.wav');
x = x(:, 1);           % use first channel if stereo
N = length(x);
duration = N / fs;

fprintf('=== Audio File Info ===\n');
fprintf('  File:           ramp.wav\n');
fprintf('  Sampling rate:  %d Hz\n', fs);
fprintf('  Num samples:    %d\n', N);
fprintf('  Duration:       %.4f seconds\n\n', duration);

%% Spectrogram parameters
win_len  = max(1, floor(N / 8));
noverlap = floor(win_len / 2);
hop      = win_len - noverlap;
nfft     = max(256, 2^nextpow2(win_len));
num_freqs = floor(nfft / 2) + 1;
num_frames = floor((N - noverlap) / hop);

% Hamming window: w(n) = 0.54 - 0.46*cos(2*pi*n / (M-1)), n = 0..M-1
n_vec = (0 : win_len - 1)';
hamming_win = 0.54 - 0.46 * cos(2 * pi * n_vec / (win_len - 1));

fprintf('=== Spectrogram Parameters ===\n');
fprintf('  Window type:    Hamming\n');
fprintf('  Window length:  %d samples (%.4f s)\n', win_len, win_len/fs);
fprintf('  Overlap:        %d samples (%d%%)\n', noverlap, round(100*noverlap/win_len));
fprintf('  Hop size:       %d samples\n', hop);
fprintf('  NFFT:           %d\n', nfft);
fprintf('  Frequency bins: %d\n', num_freqs);
fprintf('  Time frames:    %d\n\n', num_frames);

%% Compute custom spectrogram
S = zeros(num_freqs, num_frames);

for i = 1:num_frames
    idx_start = (i - 1) * hop + 1;
    idx_end   = idx_start + win_len - 1;

    % Extract frame, zero-pad if it extends past the signal end
    frame = zeros(win_len, 1);
    valid = min(idx_end, N) - idx_start + 1;
    frame(1:valid) = x(idx_start : idx_start + valid - 1);

    % Apply Hamming window
    frame = frame .* hamming_win;

    % Zero-pad to NFFT and compute FFT
    frame_padded = [frame; zeros(nfft - win_len, 1)];
    X_frame = fft(frame_padded);

    % One-sided magnitude spectrum
    S(:, i) = abs(X_frame(1 : num_freqs));
end

%% Time and frequency axes
t = ((0 : num_frames - 1) * hop + win_len / 2) / fs;   % frame center times (s)
f = (0 : num_freqs - 1) * (fs / nfft);                  % frequency axis (Hz)

%% Plot
S_dB = 10 * log10(S .^ 2 + eps);   % power in dB
peak_dB = max(S_dB(:));

figure('Name', 'Custom Spectrogram — ramp.wav', 'NumberTitle', 'off');
imagesc(t, f, S_dB);
axis xy;                            % low frequencies at bottom
colormap(parula);
cb = colorbar;
ylabel(cb, 'Power (dB)');
clim([peak_dB - 60, peak_dB]);     % 60 dB dynamic range
xlabel('Time (s)');
ylabel('Frequency (Hz)');
title(sprintf('Spectrogram of ramp.wav  |  fs=%d Hz, win=%d, overlap=50%%, NFFT=%d', ...
    fs, win_len, nfft));

%% Save figure
% out_path = '../../images/p5/out/ramp_spectrogram.png';
out_path = '../../images/p5/out/custom1_spectrogram.png';
exportgraphics(gcf, out_path, 'Resolution', 150);
fprintf('Spectrogram saved to: %s\n', out_path);
