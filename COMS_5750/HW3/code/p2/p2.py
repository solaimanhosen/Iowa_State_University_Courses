import subprocess
import os

# input_path  = './../../images/p2/in/1/frame%d.jpg'
# output_path = './../../images/p2/out/1.mp4'

input_path  = './../../images/p2/in/2/frame%d.jpg'
output_path = './../../images/p2/out/2.mp4'

os.makedirs(os.path.dirname(output_path), exist_ok=True)

command = [
    'ffmpeg',
    '-framerate', '30',
    '-i', input_path,
    '-vf', 'select=not(mod(n\\,5)),setpts=5*N/FRAME_RATE/TB',
    '-fps_mode', 'vfr',       # replaces deprecated -vsync vfr
    output_path
]

subprocess.run(command, check=True)
print("Video saved to:", output_path)
