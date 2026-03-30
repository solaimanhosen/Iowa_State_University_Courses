import cv2
import numpy as np
import os

# HSV ranges used only for initial color sampling
LOWER_ORANGE = np.array([5,  150, 150])
UPPER_ORANGE = np.array([20, 255, 255])

LOWER_GREEN  = np.array([40, 100, 100])
UPPER_GREEN  = np.array([80, 255, 255])

# How close a pixel must be to the sampled orange (per channel, in BGR)
TOLERANCE = 80

def sample_color(frame, lower_hsv, upper_hsv):
    """Return median BGR of pixels matching the given HSV range, or None."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    pixels = frame[mask > 0]
    if len(pixels) == 0:
        return None
    return np.median(pixels, axis=0).astype(np.uint8)


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

    # Sample orange and green BGR values from the first usable frame
    orange_bgr = None
    green_bgr  = None
    frames_buffer = []

    while (orange_bgr is None or green_bgr is None) and len(frames_buffer) < 30:
        ret, frame = cap.read()
        if not ret:
            break
        frames_buffer.append(frame)
        if orange_bgr is None:
            orange_bgr = sample_color(frame, LOWER_ORANGE, UPPER_ORANGE)
        if green_bgr is None:
            green_bgr = sample_color(frame, LOWER_GREEN, UPPER_GREEN)

    if orange_bgr is None or green_bgr is None:
        print(f'  Error: could not sample orange or green from {input_path}')
        cap.release()
        writer.release()
        return

    print(f'  Orange BGR: {orange_bgr}  →  Green BGR: {green_bgr}')

    def recolor_frame(frame):
        # Find pixels close to the sampled orange value
        diff = np.abs(frame.astype(np.int16) - orange_bgr.astype(np.int16))
        mask = np.all(diff <= TOLERANCE, axis=2)
        frame[mask] = green_bgr
        return frame

    for frame in frames_buffer:
        writer.write(recolor_frame(frame))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        writer.write(recolor_frame(frame))

    cap.release()
    writer.release()
    print(f'  Saved: {output_path}')


if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    for vid_num in [1, 2]:
        in_path  = os.path.join(script_dir, '..', '..', 'images', 'p6', 'in',  f'{vid_num}.mp4')
        out_path = os.path.join(script_dir, '..', '..', 'images', 'p6', 'out', f'{vid_num}_2.mp4')
        print(f'Processing video {vid_num}...')
        process_video(in_path, out_path)
    print('Done.')
