import cv2
import numpy as np
import random
import os

random.seed(42)

# --- Hardcoded source hues for each Tetris piece color (OpenCV H: 0-180) ---
# Identified from inspecting the videos across all HW3 problems
SOURCE_HUES = [
    5,    # Red
    15,   # Orange
    30,   # Yellow
    60,   # Green
    90,   # Cyan
    120,  # Blue
    150,  # Magenta
]

SAT_THRESHOLD = 60    # min HSV saturation to treat a pixel as a piece (not background)
HUE_MATCH_TOL = 12    # pixels within this hue distance of a source get remapped


def hue_dist(a, b):
    """Circular hue distance (0-180 scale)."""
    d = abs(a - b)
    return min(d, 180 - d)


# --- Build random target hue mapping (computed once at startup) ---
# Each source hue gets a random target that is:
#   - far from all source hues
#   - far from all already-chosen target hues
#   - meaningfully different from its own source
MIN_DIST_FROM_SRC     = 30   # target must differ from its own source
MIN_DIST_FROM_TARGETS = 15   # target must differ from already-chosen targets

chosen_targets = []
TARGET_HUES = []

for src in SOURCE_HUES:
    for _ in range(100000):
        candidate = random.uniform(0, 180)
        far_from_src     = hue_dist(candidate, src) > MIN_DIST_FROM_SRC
        far_from_targets = all(hue_dist(candidate, t) > MIN_DIST_FROM_TARGETS
                               for t in chosen_targets)
        if far_from_src and far_from_targets:
            TARGET_HUES.append(candidate)
            chosen_targets.append(candidate)
            break

MAPPING = list(zip(SOURCE_HUES, TARGET_HUES))
print("Color mapping (source hue → target hue):")
for src, tgt in MAPPING:
    print(f"  {round(src):>3} → {round(tgt):>3}")


# --- Per-frame hue remapping ---
def remap_frame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

    saturated = s > SAT_THRESHOLD
    new_h = h.copy()

    for src_hue, tgt_hue in MAPPING:
        diff = np.abs(h - src_hue)
        dist = np.minimum(diff, 180 - diff)
        match = saturated & (dist < HUE_MATCH_TOL)
        new_h[match] = tgt_hue

    out_hsv = np.stack([new_h, s, v], axis=2).astype(np.uint8)
    return cv2.cvtColor(out_hsv, cv2.COLOR_HSV2BGR)


# --- Process videos ---
def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f'  Error: cannot open {input_path}')
        return

    fps    = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        writer.write(remap_frame(frame))

    cap.release()
    writer.release()
    print(f'  Saved: {output_path}')


if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    for vid_num in [1, 2]:
        in_path  = os.path.join(script_dir, '..', '..', 'images', 'p7', 'in',  f'{vid_num}.mp4')
        out_path = os.path.join(script_dir, '..', '..', 'images', 'p7', 'out', f'{vid_num}.mp4')
        print(f'\nProcessing video {vid_num}...')
        process_video(in_path, out_path)
    print('\nDone.')
