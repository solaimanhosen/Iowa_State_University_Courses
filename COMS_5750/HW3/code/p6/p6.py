import cv2
import numpy as np
import os

# HSV ranges
LOWER_ORANGE = np.array([5,  150, 150])
UPPER_ORANGE = np.array([20, 255, 255])

LOWER_GREEN  = np.array([40, 100, 100])
UPPER_GREEN  = np.array([80, 255, 255])

# Slight dilation to cover anti-aliased block edges
DILATE_KERNEL = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

def sample_green(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)
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

    green_bgr = None
    frames_buffer = []
    while green_bgr is None and len(frames_buffer) < 30:
        ret, frame = cap.read()
        if not ret:
            break
        frames_buffer.append(frame)
        green_bgr = sample_green(frame)

    if green_bgr is None:
        print(f'  Warning: no green pixels found in {input_path}, using default green')
        green_bgr = np.array([34, 139, 34], dtype=np.uint8)  # fallback forest green

    print(f'  Green reference BGR: {green_bgr}')

    def recolor_frame(frame, green_bgr):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        orange_mask = cv2.inRange(hsv, LOWER_ORANGE, UPPER_ORANGE)
        frame[orange_mask > 0] = green_bgr
        return frame

    for frame in frames_buffer:
        writer.write(recolor_frame(frame, green_bgr))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        sampled = sample_green(frame)
        if sampled is not None:
            green_bgr = sampled

        writer.write(recolor_frame(frame, green_bgr))

    cap.release()
    writer.release()
    print(f'  Saved: {output_path}')

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    for vid_num in [1, 2]:
        in_path  = os.path.join(script_dir, '..', '..', 'images', 'p6', 'in',  f'{vid_num}.mp4')
        out_path = os.path.join(script_dir, '..', '..', 'images', 'p6', 'out', f'{vid_num}.mp4')
        print(f'Processing video {vid_num}...')
        process_video(in_path, out_path)
    print('Video Processing Completed.')
