"""Viral-style Short (v2): short spoken hook, word-by-word karaoke captions (ASS), fast cuts with punch-in,
whoosh on cuts, no end card (loops back into the hook), comment question at the end.
usage: python3 make_viral.py spec.json [name ...]
"""
import json, os, subprocess, sys, numpy as np, soundfile as sf
from make_short import tts, SR, BASE, FOOT

W, H = 1080, 1920


def word_times(text, start, dur):
    words = text.split()
    wts = [len(w.strip(".,!?:;")) + 2 for w in words]
    tot, t, out = sum(wts), start, []
    for w, k in zip(words, wts):
        d = dur * k / tot
        out.append((t, t + d, w))
        t += d
    return out


def ass_time(t):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def esc(s):
    return s.replace("{", "(").replace("}", ")")


def build_ass(words, hook, hook_end, total, path, cap_y, group=3, hl=()):
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins,132,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,11,4,5,50,50,0,1
Style: Hook,Poppins,128,&H00FFFFFF,&H00FFFFFF,&H00000000,&HC8000000,-1,0,0,0,100,100,0,0,3,22,0,5,70,70,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    # hook box at top, first seconds
    ev.append(f"Dialogue: 1,{ass_time(0)},{ass_time(hook_end)},Hook,,0,0,0,,{{\\pos({W//2},430)\\fad(0,150)}}{esc(hook)}")
    # word groups
    groups = []
    for li in sorted(set(x[3] for x in words)):
        lw = [x[:3] for x in words if x[3] == li]
        groups += [lw[i:i + group] for i in range(0, len(lw), group)]
    for g in groups:
        for j, (a, b, w) in enumerate(g):
            end = g[j + 1][0] if j + 1 < len(g) else b
            parts = []
            for k, (_, _, ww) in enumerate(g):
                key = ww.strip(".,!?:;").lower()
                if k == j:
                    parts.append("{\\c&H00D6FF&\\fscx112\\fscy112}" + esc(ww) + "{\\c&HFFFFFF&\\fscx100\\fscy100}")
                elif any(h.lower() == key for h in hl):
                    parts.append("{\\c&H40D6FF&}" + esc(ww) + "{\\c&HFFFFFF&}")
                else:
                    parts.append(esc(ww))
            ev.append(f"Dialogue: 0,{ass_time(a)},{ass_time(end)},Cap,,0,0,0,,{{\\pos({W//2},{cap_y})}}" + " ".join(parts))
    open(path, "w").write(hdr + "\n".join(ev) + "\n")


def whoosh(n_samples, R=44100, seed=0):
    rng = np.random.default_rng(seed)
    d = int(0.28 * R)
    t = np.arange(d) / R
    noise = rng.standard_normal(d)
    # crude band sweep: moving average with shrinking window
    out = np.zeros(d)
    for i in range(d):
        w = int(40 - 34 * (i / d)) or 1
        out[i] = noise[max(0, i - w):i + 1].mean()
    env = np.sin(np.pi * t / t[-1]) ** 2
    return out * env * 3.0


def build(spec):
    name = spec["name"]
    out = os.path.join(BASE, "out", name)
    os.makedirs(out, exist_ok=True)
    voice_id, speed = spec.get("voice", "am_michael"), spec.get("speed", 1.12)
    lines = [spec["hook_spoken"]] + spec["chunks"] + [spec["question"]]
    audio, words, t = [np.zeros(int(0.08 * SR))], [], 0.08
    gap = int(0.06 * SR)
    hook_end = None
    for i, ln in enumerate(lines):
        s = tts(ln, voice_id, speed)
        d = len(s) / SR
        words += [w + (i,) for w in word_times(ln, t, d)]
        audio += [s, np.zeros(gap)]
        t += d + gap / SR
        if i == 0:
            hook_end = t + 0.3
    total = t + 0.15
    sf.write(f"{out}/voice.wav", np.concatenate(audio), SR)
    # music
    mdur = total
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(spec.get("music_start", 0)), "-t", f"{mdur:.3f}",
                    "-i", os.path.join(BASE, spec["music_file"]), "-af",
                    "afade=t=in:st=0:d=0.05,loudnorm=I=-20:TP=-2:LRA=7", "-ar", "44100", "-ac", "2",
                    f"{out}/music.wav"], check=True)
    # cuts
    cut = spec.get("cut", 1.6)
    clips, segs, cur, i = spec["clips"], [], 0.0, 0
    while cur < total - 0.01:
        c = clips[i % len(clips)]
        d = min(c.get("d", cut), total - cur)
        segs.append((c, d, cur))
        cur += d
        i += 1
    parts = []
    for j, (c, d, _) in enumerate(segs):
        p = f"{out}/seg{j:02d}.mp4"
        z = 1.0 if j % 2 == 0 else 1.10
        # slow push inside each segment + punch-in on alternate cuts
        vf = (f"scale={int(W*z*1.06)}:{int(H*z*1.06)}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H}:'(iw-{W})/2':'(ih-{H})/2+({H}*0.03)*(1-t/{max(d,0.1):.2f})',"
              f"setsar=1,fps=30,eq=contrast=1.08:saturation=1.18")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(c.get("ss", 0)), "-i", f"{FOOT}/{c['f']}.mp4",
                        "-t", f"{d:.3f}", "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", p],
                       check=True)
        parts.append(p)
    with open(f"{out}/list.txt", "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in parts)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt",
                    "-c", "copy", f"{out}/broll.mp4"], check=True)
    # whoosh track at cuts
    R = 44100
    sfx = np.zeros(int((total + 0.5) * R))
    wh = whoosh(0)
    for _, _, st in segs[1:]:
        a = max(0, int((st - 0.14) * R))
        n = min(len(wh), len(sfx) - a)
        sfx[a:a + n] += wh[:n] * 0.18
    sf.write(f"{out}/sfx.wav", np.stack([sfx, sfx], 1), R)
    # captions
    build_ass(words, spec["hook_text"], hook_end, total, f"{out}/caps.ass", spec.get("cap_y", 1250),
              spec.get("group", 3), spec.get("cap_hl", []))
    final = os.path.join(BASE, "out", f"{name}.mp4")
    fontsdir = "/usr/share/fonts/truetype/google-fonts"
    fc = (f"[0:v]ass={out}/caps.ass:fontsdir={fontsdir}[v];"
          "[1:a]aresample=44100,volume=1.7,asplit=2[va][vk];[2:a]volume=0.45[mraw];"
          "[mraw][vk]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=300[ma];"
          "[va][ma][3:a]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.2:LRA=9[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{out}/broll.mp4", "-i", f"{out}/voice.wav",
                    "-i", f"{out}/music.wav", "-i", f"{out}/sfx.wav", "-filter_complex", fc,
                    "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
                    final], check=True)
    print(name, round(total, 1), "s")


if __name__ == "__main__":
    for spec in json.load(open(sys.argv[1])):
        if len(sys.argv) < 3 or spec["name"] in sys.argv[2:]:
            build(spec)
