import cv2
import numpy as np
import os

# Preview ROI (pixels in the top-right panel)
PREVIEW_Y1, PREVIEW_Y2 = 30, 82
PREVIEW_X1, PREVIEW_X2 = 255, 350

SAT_THRESH   = 80     # min HSV saturation to count as piece pixel
MIN_PIXELS   = 150    # min active pixels to consider a valid piece frame
DIFF_THRESH  = 0.10   # mean pixel diff below this → same shape (skip)
SAMPLE_EVERY = 3      # process every Nth frame for speed
TEMPLATE_SIZE = (PREVIEW_X2 - PREVIEW_X1, PREVIEW_Y2 - PREVIEW_Y1)  # (95, 52)

def get_binary_mask(roi):
    """Binary mask of piece pixels (high saturation) in the ROI."""
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    s = hsv[:, :, 1]
    _, mask = cv2.threshold(s, SAT_THRESH, 255, cv2.THRESH_BINARY)
    return mask


def tight_crop(mask, roi):
    """Crop mask and roi tightly to the bounding box of active pixels."""
    coords = cv2.findNonZero(mask)
    if coords is None:
        return mask, roi
    x, y, w, h = cv2.boundingRect(coords)
    return mask[y:y+h, x:x+w], roi[y:y+h, x:x+w]


def is_new_shape(mask, saved_templates):
    """True if mask differs enough from every saved template."""
    m = cv2.resize(mask, TEMPLATE_SIZE).astype(np.float32) / 255.0
    for t in saved_templates:
        diff = np.mean(np.abs(m - t))
        if diff < DIFF_THRESH:
            return False
    return True


def extract_templates(video_path, template_dir):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f'  Error: cannot open {video_path}')
        return

    os.makedirs(template_dir, exist_ok=True)

    saved = []      # normalized float32 arrays (for dedup comparison)
    existing = len([f for f in os.listdir(template_dir)
                    if f.startswith('template_') and '_ref' not in f])
    # load already-saved templates so cross-video dedup works
    for i in range(existing):
        path = os.path.join(template_dir, f'template_{i}.png')
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            saved.append(img.astype(np.float32) / 255.0)

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1
        if frame_idx % SAMPLE_EVERY != 0:
            continue

        roi  = frame[PREVIEW_Y1:PREVIEW_Y2, PREVIEW_X1:PREVIEW_X2]
        mask = get_binary_mask(roi)

        if np.sum(mask > 0) < MIN_PIXELS:
            continue   # empty or transitioning preview

        # crop tightly to just the piece shape
        mask_crop, roi_crop = tight_crop(mask, roi)

        if is_new_shape(mask_crop, saved):
            idx = len(saved)
            norm = cv2.resize(mask_crop, TEMPLATE_SIZE).astype(np.float32) / 255.0
            saved.append(norm)

            cv2.imwrite(os.path.join(template_dir, f'template_{idx}.png'),
                        cv2.resize(mask_crop, TEMPLATE_SIZE))
            cv2.imwrite(os.path.join(template_dir, f'template_{idx}_ref.png'),
                        cv2.resize(roi_crop, TEMPLATE_SIZE))
            print(f'  Saved template_{idx}')

    cap.release()


if __name__ == '__main__':
    script_dir   = os.path.dirname(__file__)
    template_dir = os.path.join(script_dir, '..', '..', 'images', 'p9', 'templates')

    for vid_num in [1, 2]:
        video_path = os.path.join(script_dir, '..', '..', 'images', 'p9', 'in', f'{vid_num}.mp4')
        print(f'Extracting from video {vid_num}...')
        extract_templates(video_path, template_dir)

    print(f'\nDone. Templates saved to: {template_dir}')
    print('Inspect the _ref.png files to identify each piece, then update PIECE_NAMES in p9.py.')
