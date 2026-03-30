import cv2
import math
import os

# Mode flag
DRAW_PATHS = True

# Detection config
DIFF_THRESH  = 20
MIN_AREA     = 200

# Trail appearance config
MAX_LIFE     = 180
TRAIL_RADIUS = 4
PATH_THICK   = 2

MAX_DIST     = 40
MAX_MISS     = 10

KERNEL_OPEN  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
KERNEL_CLOSE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))

def detect_centroids(curr_gray, prev_gray):
    diff = cv2.absdiff(curr_gray, prev_gray)
    _, mask = cv2.threshold(diff, DIFF_THRESH, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  KERNEL_OPEN)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, KERNEL_CLOSE)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    centroids = []
    for contour in contours:
        if cv2.contourArea(contour) < MIN_AREA:
            continue
        M = cv2.moments(contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            centroids.append((cx, cy))
    return centroids

def draw_color(life):
    intensity = int(255 * life / MAX_LIFE)
    return (intensity, intensity, 0)

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

    ret, prev_frame = cap.read()
    if not ret:
        print(f'  Error: could not read first frame of {input_path}')
        cap.release()
        writer.release()
        return
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    writer.write(prev_frame)

    trail_points = []
    tracks = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        centroids = detect_centroids(curr_gray, prev_gray)

        if DRAW_PATHS:
            matched_tracks = set()
            matched_centroids = set()

            assignments = []
            for ci, (cx, cy) in enumerate(centroids):
                for ti, track in enumerate(tracks):
                    lx, ly, _ = track['points'][-1]
                    dist = math.hypot(cx - lx, cy - ly)
                    if dist <= MAX_DIST:
                        assignments.append((dist, ci, ti))

            assignments.sort()
            for dist, ci, ti in assignments:
                if ci in matched_centroids or ti in matched_tracks:
                    continue
                matched_centroids.add(ci)
                matched_tracks.add(ti)
                cx, cy = centroids[ci]
                tracks[ti]['points'].append([cx, cy, MAX_LIFE])
                tracks[ti]['missed'] = 0

            for ci, (cx, cy) in enumerate(centroids):
                if ci not in matched_centroids:
                    tracks.append({'points': [[cx, cy, MAX_LIFE]], 'missed': 0})

            for ti, track in enumerate(tracks):
                if ti not in matched_tracks:
                    track['missed'] += 1

            for track in tracks:
                for pt in track['points']:
                    pt[2] -= 1
                track['points'] = [p for p in track['points'] if p[2] > 0]

            tracks = [t for t in tracks
                      if t['missed'] <= MAX_MISS and len(t['points']) > 0]

            for track in tracks:
                pts = track['points']
                for i in range(len(pts) - 1):
                    x1, y1, life1 = pts[i]
                    x2, y2, life2 = pts[i + 1]
                    cv2.line(frame, (x1, y1), (x2, y2),
                             draw_color((life1 + life2) // 2), PATH_THICK)
                cx, cy, life = pts[-1]
                cv2.circle(frame, (cx, cy), TRAIL_RADIUS, draw_color(life), -1)

        else:
            for cx, cy in centroids:
                trail_points.append([cx, cy, MAX_LIFE])

            for pt in trail_points:
                cx, cy, life = pt
                cv2.circle(frame, (cx, cy), TRAIL_RADIUS, draw_color(life), -1)

            for pt in trail_points:
                pt[2] -= 1
            trail_points = [p for p in trail_points if p[2] > 0]

        writer.write(frame)
        prev_gray = curr_gray

    cap.release()
    writer.release()
    print(f'  Saved: {output_path}')

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    for vid_num in [1, 2]:
        in_path  = os.path.join(script_dir, '..', '..', 'images', 'ec1', 'in',  f'{vid_num}.mp4')
        out_path = os.path.join(script_dir, '..', '..', 'images', 'ec1', 'out', f'{vid_num}.mp4')
        print(f'Processing video {vid_num}...')
        process_video(in_path, out_path)

    print('\nVideo Processing Completed.')
