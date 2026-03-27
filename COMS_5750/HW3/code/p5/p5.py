import cv2
import numpy as np
import os

DIFF_THRESH    = 20       # absdiff pixel threshold to count as motion
MIN_AREA       = 200      # minimum contour area to consider as the object
TRAIL_COLOR    = (0, 255, 255)   # cyan trail
TRAIL_RADIUS   = 4               # dot radius at each trail point
TRAIL_THICK    = 2               # polyline thickness


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

    # morphological kernels
    kernel_open  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))

    trail = []   # list of (cx, cy) — never cleared

    ret, prev_frame = cap.read()
    if not ret:
        print(f'  Error: could not read first frame of {input_path}')
        cap.release()
        writer.release()
        return
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # write first frame as-is (no motion yet)
    writer.write(prev_frame)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --- motion mask from frame differencing ---
        diff = cv2.absdiff(curr_gray, prev_gray)
        _, mask = cv2.threshold(diff, DIFF_THRESH, 255, cv2.THRESH_BINARY)

        # remove noise, then merge leading/trailing edges into one blob
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel_open)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)

        # --- find largest contour → centroid ---
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest) >= MIN_AREA:
                M = cv2.moments(largest)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    trail.append((cx, cy))

        # --- draw persistent trail on original frame ---
        if len(trail) >= 2:
            pts = np.array(trail, dtype=np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], isClosed=False,
                          color=TRAIL_COLOR, thickness=TRAIL_THICK)
        for pt in trail:
            cv2.circle(frame, pt, TRAIL_RADIUS, TRAIL_COLOR, -1)

        writer.write(frame)
        prev_gray = curr_gray

    cap.release()
    writer.release()
    print(f'  Saved: {output_path}')


if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    for vid_num in [1, 2]:
        in_path  = os.path.join(script_dir, '..', '..', 'images', 'p5', 'in',  f'{vid_num}.mp4')
        out_path = os.path.join(script_dir, '..', '..', 'images', 'p5', 'out', f'{vid_num}.mp4')
        print(f'Processing video {vid_num}...')
        process_video(in_path, out_path)
    print('Done.')
