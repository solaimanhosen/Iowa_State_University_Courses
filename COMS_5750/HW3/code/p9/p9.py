import cv2
import numpy as np
import os

# --- Preview ROI ---
PREVIEW_Y1, PREVIEW_Y2 = 30, 82
PREVIEW_X1, PREVIEW_X2 = 255, 350

# --- Template settings ---
TEMPLATE_SIZE = (PREVIEW_X2 - PREVIEW_X1, PREVIEW_Y2 - PREVIEW_Y1)  # (95, 52)
SAT_THRESH    = 80     # min HSV saturation to count as piece pixel
MIN_PIXELS    = 150    # min active pixels for a valid preview frame
MIN_MATCH     = 0.3    # min matchTemplate score to accept a result

# --- Piece name mapping: template index → name ---
# Inspect images/p9/templates/template_*_ref.png to verify
PIECE_NAMES = {
    0: 'Skew',
    1: 'T',
    2: 'Square',
    3: 'L',
    4: 'Straight',
    5: 'L',
    6: 'Skew',
}

# --- HSV hue → color name (OpenCV H: 0-180) ---
HUE_COLORS = [
    ((0,   10),  'Red'),
    ((10,  25),  'Orange'),
    ((25,  35),  'Yellow'),
    ((35,  85),  'Green'),
    ((85, 105),  'Cyan'),
    ((105,135),  'Blue'),
    ((135,165),  'Magenta'),
    ((165,180),  'Red'),
]

# --- Overlay style ---
FONT       = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.55
FONT_THICK = 2
TEXT_POS   = (10, 20)    # top-left of frame


def load_templates(template_dir):
    """Load binary templates as normalized float32 arrays."""
    templates = {}
    for idx in PIECE_NAMES:
        path = os.path.join(template_dir, f'template_{idx}.png')
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f'Template not found: {path}')
        templates[idx] = img.astype(np.float32) / 255.0
    return templates


def get_binary_mask(roi):
    """Binary mask of piece pixels (high saturation)."""
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    s = hsv[:, :, 1]
    _, mask = cv2.threshold(s, SAT_THRESH, 255, cv2.THRESH_BINARY)
    return mask


def tight_crop(mask):
    """Crop mask to the bounding box of active pixels."""
    coords = cv2.findNonZero(mask)
    if coords is None:
        return mask
    x, y, w, h = cv2.boundingRect(coords)
    return mask[y:y+h, x:x+w]


def identify_piece(mask, templates):
    """Return (piece_idx, score) of the best-matching template."""
    cropped = tight_crop(mask)
    m = cv2.resize(cropped, TEMPLATE_SIZE).astype(np.float32) / 255.0
    best_idx, best_score = -1, -1.0
    for idx, t in templates.items():
        result = cv2.matchTemplate(m, t, cv2.TM_CCOEFF_NORMED)
        score = float(result[0, 0])
        if score > best_score:
            best_score = score
            best_idx = idx
    return best_idx, best_score


def identify_color(roi, mask):
    """Return color name of the dominant hue among piece pixels."""
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    hue_vals = hsv[:, :, 0][mask > 0]
    if len(hue_vals) == 0:
        return 'Unknown'
    median_hue = int(np.median(hue_vals))
    for (lo, hi), name in HUE_COLORS:
        if lo <= median_hue < hi:
            return name
    return 'Unknown'


def color_bgr(color_name):
    """BGR value for each color name (for text rendering)."""
    mapping = {
        'Red':     (0,   0,   220),
        'Orange':  (0,   140, 255),
        'Yellow':  (0,   220, 220),
        'Green':   (0,   200,  50),
        'Cyan':    (220, 220,   0),
        'Blue':    (220,  50,   0),
        'Magenta': (220,   0, 220),
        'Unknown': (200, 200, 200),
    }
    return mapping.get(color_name, (200, 200, 200))


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

    last_name  = ''
    last_color = ''

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        roi  = frame[PREVIEW_Y1:PREVIEW_Y2, PREVIEW_X1:PREVIEW_X2]
        mask = get_binary_mask(roi)

        if np.sum(mask > 0) >= MIN_PIXELS:
            idx, score = identify_piece(mask, templates)
            if score >= MIN_MATCH:
                last_name  = PIECE_NAMES.get(idx, 'Unknown')
                last_color = identify_color(roi, mask)

        if last_name:
            text = f'Next: {last_name} ({last_color})'
            bgr  = color_bgr(last_color)

            # dark background for readability
            (tw, th), baseline = cv2.getTextSize(text, FONT, FONT_SCALE, FONT_THICK)
            px, py = TEXT_POS
            cv2.rectangle(frame,
                          (px - 3, py - th - 3),
                          (px + tw + 3, py + baseline + 2),
                          (30, 30, 30), cv2.FILLED)
            cv2.putText(frame, text, (px, py),
                        FONT, FONT_SCALE, bgr, FONT_THICK, cv2.LINE_AA)

        writer.write(frame)

    cap.release()
    writer.release()
    print(f'  Saved: {output_path}')


if __name__ == '__main__':
    script_dir   = os.path.dirname(__file__)
    template_dir = os.path.join(script_dir, '..', '..', 'images', 'p9', 'templates')

    templates = load_templates(template_dir)
    print(f'Loaded {len(templates)} templates.')

    for vid_num in [1, 2]:
        in_path  = os.path.join(script_dir, '..', '..', 'images', 'p9', 'in',  f'{vid_num}.mp4')
        out_path = os.path.join(script_dir, '..', '..', 'images', 'p9', 'out', f'{vid_num}.mp4')
        print(f'Processing video {vid_num}...')
        process_video(in_path, out_path, templates)

    print('Done.')
