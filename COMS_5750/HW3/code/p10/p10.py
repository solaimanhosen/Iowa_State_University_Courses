import cv2
import numpy as np
import os

# Game board region
BOARD_X1, BOARD_Y1 = 48,  20
BOARD_X2, BOARD_Y2 = 225, 336
BOARD_ROWS = 18
BOARD_COLS = 10

# Green HSV range
LOWER_GREEN = np.array([40, 100, 100])
UPPER_GREEN = np.array([80, 255, 255])

# green block Threshold
CELL_THRESH = 0.4

# Text Config
FONT       = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.35
FONT_THICK = 1
FONT_COLOR = (0, 0, 0)

def count_green_blocks_per_row(green_mask, board_x1, board_y1,
                                board_x2, board_y2, n_rows, n_cols):
    board_h = board_y2 - board_y1
    board_w = board_x2 - board_x1
    row_h   = board_h / n_rows
    col_w   = board_w / n_cols

    counts = []
    for r in range(n_rows):
        ry1 = int(board_y1 + r * row_h)
        ry2 = int(board_y1 + (r + 1) * row_h)
        green_count = 0
        for c in range(n_cols):
            cx1 = int(board_x1 + c * col_w)
            cx2 = int(board_x1 + (c + 1) * col_w)
            cell = green_mask[ry1:ry2, cx1:cx2]
            if cell.size > 0 and np.mean(cell > 0) >= CELL_THRESH:
                green_count += 1
        counts.append(green_count)
    return counts

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

    board_h = BOARD_Y2 - BOARD_Y1
    row_h   = board_h / BOARD_ROWS

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv        = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        green_mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)

        counts = count_green_blocks_per_row(
            green_mask,
            BOARD_X1, BOARD_Y1, BOARD_X2, BOARD_Y2,
            BOARD_ROWS, BOARD_COLS
        )

        # DEBUG: draw grid lines
        # board_w = BOARD_X2 - BOARD_X1
        # col_w   = board_w / BOARD_COLS
        # # board outline
        # cv2.rectangle(frame, (BOARD_X1, BOARD_Y1), (BOARD_X2, BOARD_Y2), (0, 255, 0), 1)
        # # horizontal row lines
        # for r in range(1, BOARD_ROWS):
        #     y = int(BOARD_Y1 + r * row_h)
        #     cv2.line(frame, (BOARD_X1, y), (BOARD_X2, y), (0, 200, 0), 1)
        # # vertical column lines
        # for c in range(1, BOARD_COLS):
        #     x = int(BOARD_X1 + c * col_w)
        #     cv2.line(frame, (x, BOARD_Y1), (x, BOARD_Y2), (0, 200, 0), 1)

        for r, count in enumerate(counts):
            row_cy = int(BOARD_Y1 + (r + 0.5) * row_h)
            text = str(count)
            (tw, th), _ = cv2.getTextSize(text, FONT, FONT_SCALE, FONT_THICK)

            tx = BOARD_X1 - tw - 3
            ty = row_cy + th // 2

            cv2.putText(frame, text, (tx, ty),
                        FONT, FONT_SCALE, FONT_COLOR, FONT_THICK, cv2.LINE_AA)

        writer.write(frame)

    cap.release()
    writer.release()
    print(f'  Saved: {output_path}')

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    for vid_num in [1, 2]:
        in_path  = os.path.join(script_dir, '..', '..', 'images', 'p10', 'in',  f'{vid_num}.mp4')
        out_path = os.path.join(script_dir, '..', '..', 'images', 'p10', 'out', f'{vid_num}.mp4')
        print(f'Processing video {vid_num}...')
        process_video(in_path, out_path)

    print('\nVideo Processing Completed.')
