import cv2
import os

PREVIEW_Y1, PREVIEW_Y2 = 30, 82
PREVIEW_X1, PREVIEW_X2 = 255, 350

BOX_COLOR = (0, 0, 255)   # red
BOX_THICK = 2


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

        cv2.rectangle(frame,
                      (PREVIEW_X1, PREVIEW_Y1),
                      (PREVIEW_X2, PREVIEW_Y2),
                      BOX_COLOR, BOX_THICK)

        writer.write(frame)

    cap.release()
    writer.release()
    print(f'  Saved: {output_path}')


if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    for vid_num in [1, 2]:
        in_path  = os.path.join(script_dir, '..', '..', 'images', 'p9', 'in',  f'{vid_num}.mp4')
        out_path = os.path.join(script_dir, '..', '..', 'images', 'p9', 'out', f'{vid_num}_debug_roi.mp4')
        print(f'Processing video {vid_num}...')
        process_video(in_path, out_path)
    print('Done.')
