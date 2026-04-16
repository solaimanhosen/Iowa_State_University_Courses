MORSE_ALPHA = {
    '.-':   'A', '-...': 'B', '-.-.': 'C', '-..':  'D', '.':    'E',
    '..-.': 'F', '--.':  'G', '....': 'H', '..':   'I', '.---': 'J',
    '-.-':  'K', '.-..': 'L', '--':   'M', '-.':   'N', '---':  'O',
    '.--.': 'P', '--.-': 'Q', '.-.':  'R', '...':  'S', '-':    'T',
    '..-':  'U', '...-': 'V', '.--':  'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z',
}

MORSE_DIGITS = {
    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
    '.....': '5', '-....': '6', '--...': '7', '---..' : '8', '----.': '9',
}

MORSE_TABLE = {**MORSE_ALPHA, **MORSE_DIGITS}

# Reverse tables: character -> Morse code string (for synthesis/encoding)
MORSE_ENCODE_ALPHA = {v: k for k, v in MORSE_ALPHA.items()}
MORSE_ENCODE_DIGITS = {v: k for k, v in MORSE_DIGITS.items()}
MORSE_ENCODE = {**MORSE_ENCODE_ALPHA, **MORSE_ENCODE_DIGITS}

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def find_two_thresholds(durations):
    d_min, d_max = min(durations), max(durations)
    if d_max / d_min <= 1.8:
        # Single cluster
        return d_max * 1.5, float('inf')

    sorted_d = sorted(set(round(d, 3) for d in durations))
    # Consecutive jumps: (gap_size, lower_value, upper_value)
    jumps = sorted(
        [(sorted_d[i+1] - sorted_d[i], sorted_d[i], sorted_d[i+1])
         for i in range(len(sorted_d) - 1)],
        reverse=True
    )

    # Midpoint of the largest jump -> low threshold
    low_thresh = (jumps[0][1] + jumps[0][2]) / 2.0

    # Midpoint of the second-largest jump -> high threshold (if clearly distinct)
    if len(jumps) >= 2:
        high_thresh = (jumps[1][1] + jumps[1][2]) / 2.0
        # Ensure low < high
        if high_thresh < low_thresh:
            low_thresh, high_thresh = high_thresh, low_thresh
    else:
        high_thresh = float('inf')

    return low_thresh, high_thresh


def decode_segments(segments):
    on_durs  = [d for typ, d in segments if typ == 'on']
    gap_durs = [d for typ, d in segments if typ == 'gap']

    # On-burst threshold: dot vs dash
    on_min, on_max = min(on_durs), max(on_durs)
    on_thresh = (on_min + on_max) / 2.0 if on_max / on_min > 1.8 else on_max * 1.5

    # Gap thresholds: intra-letter | inter-letter | inter-word
    letter_thresh, word_thresh = find_two_thresholds(gap_durs)

    decoded = ''
    current_symbols = ''

    def flush_letter():
        nonlocal decoded, current_symbols
        if current_symbols:
            decoded += MORSE_TABLE.get(current_symbols, '?')
            current_symbols = ''

    for typ, dur in segments:
        if typ == 'on':
            current_symbols += '.' if dur < on_thresh else '-'
        else:  # gap
            if dur >= word_thresh:
                flush_letter()
                decoded += ' '
            elif dur >= letter_thresh:
                flush_letter()
            # intra-letter gaps: do nothing

    flush_letter()
    return decoded.strip()
