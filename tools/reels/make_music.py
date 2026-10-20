"""Generate short royalty-free background tracks (original synthesis) and mux them into reels."""
import numpy as np, subprocess, sys, wave, os

SR = 44100


def note(n):  # MIDI -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)


def env(n, a, r):
    e = np.ones(n)
    a, r = int(a * SR), int(r * SR)
    e[:a] = np.linspace(0, 1, a)
    e[-r:] *= np.linspace(1, 0, r)
    return e


def pad(freq, dur, bright=0.3):
    t = np.arange(int(dur * SR)) / SR
    s = np.zeros_like(t)
    for det in (-0.12, 0.0, 0.11):  # slightly detuned voices = warm chorus
        f = freq * 2 ** (det / 12)
        s += np.sin(2 * np.pi * f * t) + bright * np.sin(2 * np.pi * 2 * f * t) / 2 + bright * 0.5 * np.sin(2 * np.pi * 3 * f * t) / 3
    lfo = 0.85 + 0.15 * np.sin(2 * np.pi * 0.3 * t)
    return s * lfo * env(len(t), 0.6, 0.8) / 3


def pluck(freq, dur=1.2):
    t = np.arange(int(dur * SR)) / SR
    s = (np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * 2 * freq * t) + 0.12 * np.sin(2 * np.pi * 3 * freq * t))
    return s * np.exp(-t * 3.2) * env(len(t), 0.004, 0.05)


def soft_kick(dur=0.45):
    t = np.arange(int(dur * SR)) / SR
    f = 55 + 60 * np.exp(-t * 18)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)


def reverb(x, delays=(0.031, 0.047, 0.061, 0.083, 0.117), fb=0.45, mix=0.35):
    y = x.copy()
    for d in delays:
        n = int(d * SR); buf = np.zeros_like(x)
        for k in range(1, 6):
            if n * k < len(x):
                buf[n * k:] += x[:-n * k] * (fb ** k)
        y += buf * mix / len(delays)
    return y


MOODS = {
    # chords as MIDI lists, arpeggio pattern from chord tones
    "bright": dict(chords=[[57, 61, 64, 69], [54, 57, 61, 66], [50, 54, 57, 62], [52, 56, 59, 64]], bpm=100, kick=True, arp_oct=24),
    "cozy": dict(chords=[[48, 52, 55, 59], [45, 48, 52, 55], [41, 45, 48, 52], [43, 47, 50, 55]], bpm=84, kick=False, arp_oct=24),
    "spooky": dict(chords=[[45, 48, 52, 57], [41, 45, 48, 53], [44, 48, 51, 56], [40, 44, 47, 52]], bpm=90, kick=True, arp_oct=24),
}


def track(mood, dur):
    m = MOODS[mood]
    n = int(dur * SR) + SR
    out = np.zeros(n)
    seg = dur / len(m["chords"])
    beat = 60 / m["bpm"]
    for i, ch in enumerate(m["chords"]):
        st = int(i * seg * SR)
        for nn in ch:
            p = pad(note(nn), seg + 0.9, 0.25 if mood != "spooky" else 0.15) * 0.22
            out[st:st + len(p)] += p[:n - st]
    # arpeggio on 8th notes
    step = beat / 2
    k = 0; t = 0.15
    while t < dur - 0.3:
        ch = m["chords"][min(int(t / seg), len(m["chords"]) - 1)]
        nn = ch[[0, 2, 1, 3, 2, 1][k % 6]] + m["arp_oct"]
        p = pluck(note(nn)) * 0.16
        st = int(t * SR); out[st:st + len(p)] += p[:n - st]
        k += 1; t += step
    if m["kick"]:
        t = beat * 2
        while t < dur - 0.4:
            p = soft_kick() * 0.35; st = int(t * SR); out[st:st + len(p)] += p[:n - st]
            t += beat
    out = reverb(out)[:int(dur * SR)]
    out *= env(len(out), 0.35, 0.9)
    out /= np.max(np.abs(out)) + 1e-9
    out *= 0.6  # ~ -4.4 dBFS peak, gentle background level
    st = np.stack([out, np.roll(out, 300) * 0.96], axis=1)  # slight stereo width
    return (st * 32767).astype(np.int16)


def write_wav(path, data):
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())


if __name__ == "__main__":
    src, mood, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).decode())
    wav = dst + ".wav"
    write_wav(wav, track(mood, dur))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-i", wav, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", dst], check=True)
    os.remove(wav)
    print("ok", dst)
