#!/usr/bin/env python3
"""Burn a big TikTok-style hook (two pills) over the first seconds of a reel.
usage: hook.py in.mp4 out.mp4 "line1" "line2" [trim_start] [hook_end] [cy] [bright_until]
"""
import sys, subprocess, os, tempfile
from PIL import Image, ImageDraw, ImageFont

src, out, l1, l2 = sys.argv[1:5]
ts = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
he = float(sys.argv[6]) if len(sys.argv) > 6 else 3.2
cy = int(sys.argv[7]) if len(sys.argv) > 7 else 770
bu = float(sys.argv[8]) if len(sys.argv) > 8 else 0.0

W, H = 1080, 1920
F = ImageFont.truetype("/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf", 86)
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

def pill(text, y, fill, fg, boxw=None):
    tw = d.textlength(text, font=F)
    # shrink font if too wide
    f = F
    while tw > W - 140:
        f = ImageFont.truetype(F.path, f.size - 4); tw = d.textlength(text, font=f)
    padx, pady = 38, 20
    bw = max(boxw or 0, tw + 2 * padx)
    x0 = (W - bw) / 2
    bb = d.textbbox((0, 0), text, font=f)
    th = bb[3] - bb[1]
    d.rounded_rectangle([x0, y, x0 + bw, y + th + 2 * pady], radius=26, fill=fill)
    d.text(((W - tw) / 2, y + pady - bb[1]), text, font=f, fill=fg)
    return th + 2 * pady

# shadow-ish dim band behind both pills so the old small caption is hidden
h1 = 86 + 40
top = cy - h1 - 4
d.rectangle([0, top - 40, W, cy + h1 + 54], fill=(0, 0, 0, 200))
bw = min(W - 100, max(d.textlength(l1, font=F), d.textlength(l2, font=F)) + 76)
pill(l1, top, (255, 255, 255, 255), (17, 17, 17, 255), bw)
pill(l2, cy + 4, (255, 196, 0, 255), (17, 17, 17, 255), bw)

tmp = tempfile.mkdtemp()
png = os.path.join(tmp, "hook.png")
img.save(png)

d_in = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                             "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
dur = round(d_in - ts, 2)
fo = max(0, dur - 0.6)
vf = "[0:v]"
pre = f"eq=gamma=1.12:contrast=1.08:saturation=1.25:enable='lt(t,{bu})'," if bu > 0 else ""
fc = (f"[0:v]{pre}format=yuv420p[v0];"
      f"[v0][1:v]overlay=0:0:enable='lt(t,{he})',format=yuv420p[v]")
cmd = ["ffmpeg", "-y", "-v", "error", "-ss", str(ts), "-i", src, "-loop", "1", "-i", png,
       "-filter_complex", fc, "-map", "[v]", "-map", "0:a:0",
       "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-r", "30",
       "-af", f"afade=t=in:st=0:d=0.08,afade=t=out:st={fo}:d=0.6",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", str(dur),
       "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
print(out, dur)
