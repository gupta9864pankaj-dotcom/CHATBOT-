from PIL import Image
import imageio.v2 as imageio
import numpy as np

in_gif = "demo/demo-video.gif"
out_mp4 = "demo/demo-video.mp4"

im = Image.open(in_gif)
frames = []
durations = []

try:
    while True:
        frame = im.convert("RGB")
        frames.append(np.array(frame))
        durations.append(im.info.get("duration", 2200))
        im.seek(im.tell() + 1)
except EOFError:
    pass

if not frames:
    raise RuntimeError("No frames found in GIF")

# Convert varying GIF durations to repeated frames at 10 fps
fps = 10
out_frames = []
for frame, dur_ms in zip(frames, durations):
    repeat = max(1, round((dur_ms / 1000.0) * fps))
    out_frames.extend([frame] * repeat)

writer = imageio.get_writer(out_mp4, fps=fps, codec="libx264", quality=8, pixelformat="yuv420p")
for fr in out_frames:
    writer.append_data(fr)
writer.close()

print(f"Created {out_mp4}")
