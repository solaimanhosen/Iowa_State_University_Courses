import subprocess
import os

def process_video(input_path, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    command = [
        'ffmpeg', '-y',
        '-framerate', '30',
        '-i', input_path,
        '-vf', 'select=not(mod(n\\,5)),setpts=5*N/FRAME_RATE/TB',
        '-fps_mode', 'vfr',
        output_path
    ]
    subprocess.run(command, check=True)
    print(f'  Saved: {output_path}')

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    for vid_num in [1, 2]:
        in_path  = os.path.join(script_dir, '..', '..', 'images', 'p2', 'in',
                                str(vid_num), 'frame%d.jpg')
        out_path = os.path.join(script_dir, '..', '..', 'images', 'p2', 'out',
                                f'{vid_num}.mp4')
        print(f'Processing video {vid_num}...')
        process_video(in_path, out_path)

    print('\nVideo Processing Completed.')
