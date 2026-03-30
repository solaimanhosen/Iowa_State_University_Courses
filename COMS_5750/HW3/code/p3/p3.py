import cv2
import numpy as np
import os

# Game board region (pixel coords)
BOARD_X1, BOARD_Y1 = 5,  20
# BOARD_X2, BOARD_Y2 = 195, 320
BOARD_X2, BOARD_Y2 = 180, 336
BOARD_ROWS = 18

# Detection thresholds
BRIGHTNESS_THRESH = 230
ROW_FLASH_RATIO   = 0.6

def process_video(input_path, output_path):
    vr     = cv2.VideoCapture(input_path)
    fps    = vr.get(cv2.CAP_PROP_FPS)
    width  = int(vr.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vr.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    vw     = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # board_w    = BOARD_X2 - BOARD_X1
    # board_h_px = BOARD_Y2 - BOARD_Y1
    # vw_board = cv2.VideoWriter(output_path.replace('.mp4', '_board.mp4'), fourcc, fps, (board_w, board_h_px), isColor=False)

    # show text for 3 seconds
    TEXT_DURATION = int(fps * 3)
    text_timer   = 0
    display_text = ""
    prev_lines   = 0

    while True:
        ret, frame = vr.read()
        if not ret:
            break

        # print(frame.shape)

        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        board = gray[BOARD_Y1:BOARD_Y2, BOARD_X1:BOARD_X2]

        # # Optional: Draw board region for debugging
        # cv2.rectangle(frame, (BOARD_X1, BOARD_Y1), (BOARD_X2, BOARD_Y2), (255, 0, 0), 2)

        board_h = board.shape[0]
        row_h   = board_h // BOARD_ROWS

        # cv2.line(frame, (BOARD_X1, BOARD_Y2), (BOARD_X2, BOARD_Y2), (255, 0, 0), 1)

        # # Optional: Draw horizontal lines to visualize row strips
        # for r in range(1, BOARD_ROWS):
        #     y = BOARD_Y2 - r * row_h
        #     cv2.line(frame, (BOARD_X1, y), (BOARD_X2, y), (255, 0, 0), 1)
        # # cv2.rectangle(frame, (BOARD_X1, BOARD_Y1), (BOARD_X2, BOARD_Y2), (255, 0, 0), 2)

        # max_pixel = max(max_pixel, np.max(board))
        # print(f"Max pixel in board: {max_pixel}")

        # Count flashing game rows
        lines_cleared = 0
        for r in range(4):  # check bottom 4 rows
            # print(f"Checking row {BOARD_ROWS - r} (pixels {BOARD_Y2 - r * row_h} to {BOARD_Y2 - (r + 1) * row_h})")
            # # row_strip    = board[BOARD_Y2 - r * row_h : BOARD_Y2 - (r + 1) * row_h, :]
            row_strip = board[board_h - (r+1)*row_h : board_h - r*row_h, :]

            # print(row_strip)
            bright_ratio = np.mean(row_strip > BRIGHTNESS_THRESH)
            # print(f"Row {BOARD_ROWS - r}: Bright Ratio = {bright_ratio:.2f}")
            if bright_ratio > ROW_FLASH_RATIO:
                lines_cleared += 1

        if lines_cleared > 0 and prev_lines == 0:
            label        = "Line" if lines_cleared == 1 else "Lines"
            display_text = f"{lines_cleared} {label} Cleared!"
            text_timer   = TEXT_DURATION

        prev_lines = lines_cleared

        # Draw overlay text
        if text_timer > 0:
            cv2.putText(frame, display_text,
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
            text_timer -= 1

        vw.write(frame)
        # vw_board.write(board)

    vr.release()
    vw.release()
    # vw_board.release()
    print(f'  Saved: {output_path}')

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    for vid_num in [1, 2]:
        in_path  = os.path.join(script_dir, '..', '..', 'images', 'p3', 'in',  f'{vid_num}.mp4')
        out_path = os.path.join(script_dir, '..', '..', 'images', 'p3', 'out', f'{vid_num}.mp4')
        print(f'Processing video {vid_num}...')
        process_video(in_path, out_path)

    print('\nVideo Processing Completed.')
