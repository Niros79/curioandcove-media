"""Build a 1080x1920 YouTube Short: real b-roll cuts, hook text from frame 0, Kokoro voiceover, synced captions, light music."""
import json, os, subprocess, sys, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
from kokoro_onnx import Kokoro

W, H, SR = 1080, 1920, 24000
BASE = os.path.dirname(os.path.abspath(__file__))
FOOT = os.path.join(BASE, "footage")
BOLD = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
BLACK = "/usr/share/fonts/truetype/google-fonts/Poppins-ExtraBold.ttf"
if not os.path.exists(BLACK):
    BLACK = BOLD
_k = None


def tts(text, voice, speed):
    global _k
    if _k is None:
        _k = Kokoro(os.path.join(BASE, "kokoro.onnx"), os.path.join(BASE, "voices.bin"))
    s, sr = _k.create(text, voice=voice, speed=speed, lang="en-us")
    assert sr == SR
    # trim leading/trailing silence
    idx = np.where(np.abs(s) > 0.01)[0]
    if len(idx):
        s = s[max(0, idx[0] - 600): idx[-1] + 1200]
    return s


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def text_png(path, text, size, y_center, fg, bg, highlight=None, pad=26, maxw=920, font=BLACK):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(font, size)
    lines = wrap(d, text, f, maxw)
    lh = int(size * 1.32)
    total = lh * len(lines)
    y = y_center - total // 2
    ys = [y + i * lh for i in range(len(lines))]
    if bg:
        for ln, yy in zip(lines, ys):
            tw = d.textlength(ln, font=f)
            x = (W - tw) / 2
            d.rounded_rectangle([x - pad, yy - pad * 0.35, x + tw + pad, yy + lh + pad * 0.35], radius=18, fill=bg)
    for ln, yy in zip(lines, ys):
        tw = d.textlength(ln, font=f)
        x = (W - tw) / 2
        col = fg
        if highlight and any(h.lower() in ln.lower() for h in highlight):
            col = (255, 214, 64, 255)
        d.text((x, yy), ln, font=f, fill=col, stroke_width=0 if bg else 6, stroke_fill=(0, 0, 0, 255))
    img.save(path)


def music(dur, root, out):
    t = np.arange(int(dur * 44100)) / 44100
    bpm = 112
    beat = 60 / bpm
    s = np.zeros_like(t)
    prog = [0, 5, 7, 3] if root % 2 else [0, 7, 9, 5]
    for i, c in enumerate(prog * 20):
        st = i * beat * 4
        if st > dur:
            break
        n = slice(int(st * 44100), int(min(dur, st + beat * 4) * 44100))
        tt = t[n] - st
        for iv in (0, 4 if root % 2 else 3, 7):
            f = 440 * 2 ** ((root + c + iv - 69) / 12)
            s[n] += 0.10 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 0.6)
    for k in np.arange(0, dur, beat):  # soft kick
        n = slice(int(k * 44100), int(min(dur, k + 0.25) * 44100))
        tt = t[n] - k
        s[n] += 0.35 * np.sin(2 * np.pi * (55 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14)
    for k in np.arange(beat / 2, dur, beat):  # hat
        n = slice(int(k * 44100), int(min(dur, k + 0.05) * 44100))
        s[n] += 0.04 * np.random.randn(n.stop - n.start) * np.exp(-np.arange(n.stop - n.start) / 400)
    fade = int(1.0 * 44100)
    s[-fade:] *= np.linspace(1, 0, fade)
    s = s / (np.abs(s).max() + 1e-9) * 0.9
    sf.write(out, s, 44100)


def build(spec):
    name = spec["name"]
    out = os.path.join(BASE, "out", name)
    os.makedirs(out, exist_ok=True)
    gap = int(0.12 * SR)
    # --- voice, chunk by chunk (gives exact caption timing)
    audio, cues, t = [], [], 0.25
    audio.append(np.zeros(int(0.25 * SR)))
    for ch in spec["chunks"]:
        s = tts(ch, spec.get("voice", "am_michael"), spec.get("speed", 1.12))
        d = len(s) / SR
        cues.append((t, t + d, ch))
        audio += [s, np.zeros(gap)]
        t += d + gap / SR
    endcard = 2.2
    total = t + endcard
    voice = np.concatenate(audio + [np.zeros(int(endcard * SR))])
    sf.write(f"{out}/voice.wav", voice, SR)
    music(total + 0.5, spec.get("root", 57), f"{out}/music.wav")
    # --- b-roll timeline
    segs, cur, i = [], 0.0, 0
    clips = spec["clips"]
    while cur < total - 0.01:
        c = clips[i % len(clips)]
        d = min(c.get("d", 2.6), total - cur)
        segs.append((c, d))
        cur += d
        i += 1
    parts = []
    for j, (c, d) in enumerate(segs):
        p = f"{out}/seg{j:02d}.mp4"
        z = 1.0 + 0.06 * (j % 2)
        vf = (f"scale={int(W*z)}:{int(H*z)}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H},setsar=1,fps=30,eq=contrast=1.06:saturation=1.12")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(c.get("ss", 0)), "-i", f"{FOOT}/{c['f']}.mp4",
                        "-t", f"{d:.3f}", "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", p], check=True)
        parts.append(p)
    with open(f"{out}/list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in parts)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt",
                    "-c", "copy", f"{out}/broll.mp4"], check=True)
    # --- overlays
    ov = []
    hook_end = spec.get("hook_end", min(3.0, cues[0][1] + 0.4))
    text_png(f"{out}/hook.png", spec["hook"], 104, 560, (255, 255, 255, 255), (0, 0, 0, 205),
             highlight=spec.get("hook_hl"), maxw=900)
    ov.append((f"{out}/hook.png", 0, hook_end))
    for k, (a, b, ch) in enumerate(cues):
        p = f"{out}/cap{k:02d}.png"
        text_png(p, ch, 84, 1360, (255, 255, 255, 255), (0, 0, 0, 150), highlight=spec.get("cap_hl"), maxw=880, font=BLACK, pad=22)
        ov.append((p, a, b + 0.08))
    text_png(f"{out}/end1.png", spec.get("end_top", "Full guide"), 80, 800, (255, 255, 255, 255), (0, 0, 0, 205))
    text_png(f"{out}/end2.png", "curioandcove.com", 92, 960, (20, 20, 20, 255), (255, 214, 64, 255))
    ov.append((f"{out}/end1.png", total - endcard, total))
    ov.append((f"{out}/end2.png", total - endcard, total))
    inputs = ["-i", f"{out}/broll.mp4", "-i", f"{out}/voice.wav", "-i", f"{out}/music.wav"]
    fc, last = [], "0:v"
    for n, (p, a, b) in enumerate(ov):
        inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", p]
        idx = n + 3
        fc.append(f"[{last}][{idx}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[v{n}]")
        last = f"v{n}"
    fc.append("[1:a]volume=1.6[va];[2:a]volume=0.13[ma];[va][ma]amix=inputs=2:duration=first:normalize=0,"
              "alimiter=limit=0.95[a]")
    final = os.path.join(BASE, "out", f"{name}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
                    "-map", f"[{last}]", "-map", "[a]", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", final],
                   check=True)
    print(name, round(total, 1), "s")


if __name__ == "__main__":
    for spec in json.load(open(sys.argv[1])):
        if len(sys.argv) < 3 or spec["name"] in sys.argv[2:]:
            build(spec)
