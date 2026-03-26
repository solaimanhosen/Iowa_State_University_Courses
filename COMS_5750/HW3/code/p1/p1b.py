import cv2
import numpy as np

#open input video
cap = cv2.VideoCapture('./../../images/p1/in/1.mp4')
# cap = cv2.VideoCapture('./../../images/p1/in/2.mp4')

fps = cap.get(cv2.CAP_PROP_FPS)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

# Setup video writer
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fourcc = cv2.VideoWriter_fourcc(*'avc1')

vw = cv2.VideoWriter('./../../images/p1/out/1b.mp4', fourcc, fps, (int(width), int(height)), isColor=False)
# vw = cv2.VideoWriter('./../../images/p1/out/2b.mp4', fourcc, fps, (int(width), int(height)), isColor=False)

mhist = np.zeros((int(height), int(width)), dtype=np.uint8)

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

print('Motion history video saved.')
