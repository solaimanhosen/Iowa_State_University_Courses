import cv2
import numpy as np
import os

def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fps    = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    vw = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=False)

    mhist = np.zeros((height, width), dtype=np.uint8)

    ret, pFrame = cap.read()
    pFrameGray = cv2.cvtColor(pFrame, cv2.COLOR_BGR2GRAY)

    while True:
        ret, cFrame = cap.read()
        if not ret:
            break

        cFrameGray = cv2.cvtColor(cFrame, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(cFrameGray, pFrameGray)
        mhist[diff > 20] = 255
        vw.write(mhist)

        mhist = np.clip(mhist.astype(np.int16) - 10, 0, 255).astype(np.uint8)

        pFrameGray = cFrameGray

    cap.release()
    vw.release()
    print(f'  Saved: {output_path}')

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    for vid_num in [1, 2]:
        in_path  = os.path.join(script_dir, '..', '..', 'images', 'p1', 'in',  f'{vid_num}.mp4')
        out_path = os.path.join(script_dir, '..', '..', 'images', 'p1', 'out', f'{vid_num}b.mp4')
        print(f'Processing video {vid_num}...')
        process_video(in_path, out_path)

    print('\nVideo Processing Completed.')
