import cv2
import numpy as np
import os

# ── Region of interest for the score display (hardcoded) ──────────────────────
# The right panel shows "score  <value>" in a box at this location.
# Frame size: 360 × 416 (height × width)
SCORE_ROI = (130, 160, 310, 405)   # (y1, y2, x1, x2)

# Threshold to binarize the score region: digit pixels are dark (~0–70),
# background is light (~200+).  BINARY_INV makes digits white on black.
THRESH_VAL = 80

# Minimum blob dimensions to accept as a digit candidate
MIN_BLOB_W = 2
MIN_BLOB_H = 5

# Template directory (relative to this script's location)
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__),
                             '..', '..', 'images', 'p4', 'in', 'templates')
# Maps template filename suffix → canonical digit label.
# Multiple templates for the same digit handle sub-pixel antialiasing variants.
DIGIT_TEMPLATES = {
    '0':  '0',   # "0" hollow at cols 2-3 (position x=49 in ROI)
    '0b': '0',   # "0" hollow at cols 3-4 (position x=39 in ROI)
    '1':  '1',
    '2':  '2',
    '3':  '3',
    '4':  '4',
    '8':  '8',
}

# Where to draw the recognized score on the output frame
DISPLAY_POS  = (10, 45)              # (x, y) in pixels
DISPLAY_SCALE = 1.0
DISPLAY_COLOR = (30, 30, 30)         # near-black
DISPLAY_THICK = 2


# ── Template helpers ───────────────────────────────────────────────────────────

def load_templates(template_dir, digit_map):
    """Load binary digit templates from PNG files.

    digit_map: dict of {filename_suffix -> canonical_digit_label}
    Returns:   dict of {filename_suffix -> (canonical_label, binary_image)}
    """
    templates = {}
    for suffix, canonical in digit_map.items():
        path = os.path.join(template_dir, f'digit_{suffix}.png')
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f'Template not found: {path}')
        _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        templates[suffix] = (canonical, binary)
    return templates


def match_digit(crop, templates):
    """Return canonical digit label for the best-matching template."""
    best_label, best_conf = '?', -1.0
    for canonical, template in templates.values():
        # Resize template to the crop's size so matchTemplate returns a 1×1 result
        t = cv2.resize(template, (crop.shape[1], crop.shape[0]),
                       interpolation=cv2.INTER_NEAREST)
        result = cv2.matchTemplate(crop.astype(np.float32),
                                   t.astype(np.float32),
                                   cv2.TM_CCOEFF_NORMED)
        conf = float(result[0, 0])
        if conf > best_conf:
            best_conf = conf
            best_label = canonical
    return best_label, best_conf


# ── Per-frame score recognition ────────────────────────────────────────────────

def recognize_score(frame, templates):
    """
    Extract the score value from the frame.
    Returns the score as a string of digit characters (e.g. '1200').
    """
    y1, y2, x1, x2 = SCORE_ROI
    roi  = frame[y1:y2, x1:x2]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, THRESH_VAL, 255, cv2.THRESH_BINARY_INV)

    # Find connected-component blobs; commas are too sparse to cross the filter
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for c in contours:
        bx, by, bw, bh = cv2.boundingRect(c)
        if bw > MIN_BLOB_W and bh > MIN_BLOB_H:
            boxes.append((bx, by, bw, bh))
    boxes.sort(key=lambda b: b[0])   # left → right order

    if not boxes:
        return None

    digits = []
    for bx, by, bw, bh in boxes:
        crop  = thresh[by:by + bh, bx:bx + bw]
        label, _ = match_digit(crop, templates)
        digits.append(label)

    return ''.join(digits)


def format_score(score_str):
    """Add thousands comma, e.g. '1200' → '1,200'."""
    try:
        return f'{int(score_str):,}'
    except (ValueError, TypeError):
        return score_str or '0'


# ── Video processing ───────────────────────────────────────────────────────────

def process_video(input_path, output_path, templates):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f'  Error: cannot open {input_path}')
        return

    fps    = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    last_score = '0'   # carry the last known score across frames

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        raw = recognize_score(frame, templates)
        if raw is not None:
            last_score = raw

        label_text = f'Score: {format_score(last_score)}'

        # Draw a white background rectangle so text is readable over the board
        (tw, th), baseline = cv2.getTextSize(
            label_text, cv2.FONT_HERSHEY_SIMPLEX, DISPLAY_SCALE, DISPLAY_THICK)
        px, py = DISPLAY_POS
        cv2.rectangle(frame,
                      (px - 4, py - th - 4),
                      (px + tw + 4, py + baseline + 2),
                      (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, label_text,
                    (px, py),
                    cv2.FONT_HERSHEY_SIMPLEX, DISPLAY_SCALE,
                    DISPLAY_COLOR, DISPLAY_THICK, cv2.LINE_AA)

        writer.write(frame)

    cap.release()
    writer.release()
    print(f'  Saved: {output_path}')


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    templates = load_templates(TEMPLATE_DIR, DIGIT_TEMPLATES)
    print(f'Loaded templates: {list(templates.keys())}')

    script_dir = os.path.dirname(__file__)
    for vid_num in [1, 2]:
        in_path  = os.path.join(script_dir, '..', '..', 'images', 'p4', 'in',  f'{vid_num}.mp4')
        out_path = os.path.join(script_dir, '..', '..', 'images', 'p4', 'out', f'{vid_num}.mp4')
        print(f'Processing video {vid_num}...')
        process_video(in_path, out_path, templates)

    print('Done.')
