import cv2
import numpy as np
import os

# HSV ranges for red (wraps around hue=0)
LOWER_RED1 = np.array([0,   150, 150])
UPPER_RED1 = np.array([10,  255, 255])
LOWER_RED2 = np.array([170, 150, 150])
UPPER_RED2 = np.array([180, 255, 255])

# O-piece validation thresholds
MIN_AREA        = 300    # minimum contour area (filters noise)
MIN_FILL_RATIO  = 0.85   # contour area / bounding rect area (rejects partial pieces)
MAX_ASPECT_DEV  = 0.25   # max deviation from aspect ratio 1.0 (|w/h - 1| <= this)

PURPLE = (128, 0, 128)
BOX_THICK = 2

KERNEL_OPEN  = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
KERNEL_CLOSE = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))


def get_red_mask(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
    mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
    mask  = cv2.bitwise_or(mask1, mask2)
    mask  = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  KERNEL_OPEN)
    mask  = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL_CLOSE)
    return mask


def is_valid_o_piece(contour):
    area = cv2.contourArea(contour)
    if area < MIN_AREA:
        return False, None

    x, y, w, h = cv2.boundingRect(contour)
    rect_area = w * h
    fill_ratio = area / rect_area
    if fill_ratio < MIN_FILL_RATIO:
        return False, None

    aspect_ratio = w / h
    if abs(aspect_ratio - 1.0) > MAX_ASPECT_DEV:
        return False, None

    return True, (x, y, w, h)


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

        red_mask = get_red_mask(frame)

        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            valid, bbox = is_valid_o_piece(contour)
            if valid:
                x, y, w, h = bbox
                cv2.rectangle(frame, (x, y), (x + w, y + h), PURPLE, BOX_THICK)

        writer.write(frame)

    cap.release()
    writer.release()
    print(f'  Saved: {output_path}')


if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    for vid_num in [1, 2]:
        in_path  = os.path.join(script_dir, '..', '..', 'images', 'p8', 'in',  f'{vid_num}.mp4')
        out_path = os.path.join(script_dir, '..', '..', 'images', 'p8', 'out', f'{vid_num}.mp4')
        print(f'Processing video {vid_num}...')
        process_video(in_path, out_path)
    print('Done.')
