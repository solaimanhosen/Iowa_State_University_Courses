import cv2
import numpy as np

# -------------------- Read input --------------------
a = cv2.imread("./../../images/p1/in/1.jpg")
# a = cv2.imread("./../../images/p1/in/2.jpg")
if a is None:
    raise FileNotFoundError("Input image not found")

# -------------------- im2bw(a, 0.9) --------------------
# MATLAB im2bw uses grayscale internally; threshold is in [0,1]
gray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
th_a = int(round(0.9 * 255))
_, b = cv2.threshold(gray, th_a, 255, cv2.THRESH_BINARY)

# bi = ~b  (invert)
bi = cv2.bitwise_not(b)

# -------------------- Load dot2.jpg -> se --------------------
s = cv2.imread("dot2.jpg", cv2.IMREAD_GRAYSCALE)
if s is None:
    raise FileNotFoundError("dot2.jpg not found")

th_s = int(round(0.5 * 255))
_, s1 = cv2.threshold(s, th_s, 255, cv2.THRESH_BINARY)

# se = ~s1  (dot becomes 255, background 0)
se = cv2.bitwise_not(s1)

# -------------------- Apos = imerode(bi, se) --------------------
Apos = cv2.erode(bi, se, iterations=1)

# -------------------- plus mask (kernel) --------------------
plus = np.array([
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
], dtype=np.uint8)

# onlyPlus = imdilate(Apos, plus)
onlyPlus = cv2.dilate(Apos, plus, iterations=1)

# -------------------- Color detected pixels RED on original --------------------
color_img = a.copy()

# mask where onlyPlus == 1 in MATLAB; here it's 255/nonzero
mask = (onlyPlus > 0)

# MATLAB sets R=255,G=0,B=0. OpenCV is BGR => (0,0,255)
color_img[mask] = (0, 0, 255)

# -------------------- Save result --------------------
cv2.imwrite("./../../images/p1/out/2a.jpg", color_img)
# cv2.imwrite("./../../images/p1/out/2b.jpg", color_img)

# Optional quick debug display (press any key to close)
# cv2.imshow("original", a)
# cv2.imshow("binary b", b)
# cv2.imshow("inverted bi", bi)
# cv2.imshow("Apos", Apos)
# cv2.imshow("onlyPlus", onlyPlus)
# cv2.imshow("result", color_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()