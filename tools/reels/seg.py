import sys,subprocess,numpy as np
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar","8000","-f","s16le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.int16).astype(float)/32768
for t in ["pop","phonk","lofi","halloween"]:
    x=load(f"tracks/{t}.wav"); sr=8000; L=len(x)/sr
    rms=[ (s, np.sqrt(np.mean(x[int(s*sr):int((s+6.1)*sr)]**2))) for s in np.arange(0, L-6.2, 0.5)]
    top=sorted(rms,key=lambda a:-a[1])[:6]
    print(t, round(L,1), [(round(s,1),round(r,3)) for s,r in top])
