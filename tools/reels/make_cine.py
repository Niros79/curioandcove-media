import subprocess, os
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920
B="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"; M="/usr/share/fonts/truetype/google-fonts/Poppins-SemiBold.ttf"
if not os.path.exists(M): M="/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
OV="/home/claude/reels3/ov"; OUT="/home/claude/reels3/out"; SRC="/home/claude/reels3/src"; T="/home/claude/music/tracks/"
def wrap(d,t,f,mw):
    out=[];cur=""
    for w in t.split():
        x=(cur+" "+w).strip()
        if d.textlength(x,font=f)<=mw: cur=x
        else: out.append(cur);cur=w
    out.append(cur);return out
def hook_png(path,text,acc):
    im=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(im);f=ImageFont.truetype(B,92)
    lines=wrap(d,text,f,W-170);lh=118;y=560-len(lines)*lh//2
    for i,l in enumerate(lines):
        tw=d.textlength(l,font=f);bg=acc if i==len(lines)-1 else (255,255,255)
        d.rounded_rectangle([(W-tw)/2-34,y-10,(W+tw)/2+34,y+lh-8],radius=24,fill=bg+(255,))
        d.text(((W-tw)/2,y),l,font=f,fill=(17,17,17));y+=lh+6
    im.save(path)
def step_png(path,n,title,sub,acc):
    im=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(im);ft=ImageFont.truetype(B,70);fs=ImageFont.truetype(M,46)
    tl=wrap(d,title,ft,W-260);sl=wrap(d,sub,fs,W-200)
    h=len(tl)*84+len(sl)*58+90;y0=H-560-h
    d.rounded_rectangle([60,y0,W-60,y0+h+40],radius=36,fill=(10,14,20,190))
    d.ellipse([100,y0+34,180,y0+114],fill=acc+(255,));fn=ImageFont.truetype(B,52);t=str(n)
    d.text((140-d.textlength(t,font=fn)/2,y0+40),t,font=fn,fill=(17,17,17))
    y=y0+34
    for l in tl: d.text((210,y),l,font=ft,fill=(255,255,255));y+=84
    y+=10
    for l in sl: d.text((100,y),l,font=fs,fill=(235,235,235));y+=58
    im.save(path)
def cta_png(path,title,sub,site,acc):
    im=Image.new("RGBA",(W,H),(0,0,0,150));d=ImageDraw.Draw(im);ft=ImageFont.truetype(B,84);fs=ImageFont.truetype(M,54);fb=ImageFont.truetype(B,58)
    y=700
    for l in wrap(d,title,ft,W-160): d.text(((W-d.textlength(l,font=ft))/2,y),l,font=ft,fill=(255,255,255));y+=104
    y+=30
    for l in wrap(d,sub,fs,W-160): d.text(((W-d.textlength(l,font=fs))/2,y),l,font=fs,fill=(240,240,240));y+=70
    y+=60;tw=d.textlength(site,font=fb)
    d.rounded_rectangle([(W-tw)/2-50,y,(W+tw)/2+50,y+110],radius=55,fill=acc+(255,))
    d.text(((W-tw)/2,y+18),site,font=fb,fill=(17,17,17))
    im.save(path)
def site_tag(path,site):
    im=Image.new("RGBA",(W,H),(0,0,0,0));d=ImageDraw.Draw(im);f=ImageFont.truetype(B,40);tw=d.textlength(site,font=f)
    d.rounded_rectangle([(W-tw)/2-30,150,(W+tw)/2+30,220],radius=35,fill=(0,0,0,120));d.text(((W-tw)/2,160),site,font=f,fill=(255,255,255))
    im.save(path)
def reel(name,src,ss,hook,steps,cta,site,acc,music,mfilt="anull",grade="eq=contrast=1.06:saturation=1.15:brightness=0.01"):
    hp=f"{OV}/{name}_h.png";hook_png(hp,hook,acc)
    sp=[]
    for i,(t,s) in enumerate(steps,1): p=f"{OV}/{name}_s{i}.png";step_png(p,i,t,s,acc);sp.append(p)
    cp=f"{OV}/{name}_c.png";cta_png(cp,cta[0],cta[1],site,acc);tp=f"{OV}/{name}_t.png";site_tag(tp,site)
    D=13.0;hs,he=0,3.0;st=[(3.0,6.0),(6.0,8.6),(8.6,10.8)];cs=10.8
    ins=["-ss",str(ss),"-stream_loop","-1","-i",src,"-i",hp]+sum([["-i",p] for p in sp],[])+["-i",cp,"-i",tp,"-i",music]
    fc=(f"[0:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{grade},"
        f"zoompan=z='min(zoom+0.0006,1.08)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,trim=0:{D},setpts=PTS-STARTPTS[bg];"
        f"[bg][1:v]overlay=0:0:enable='between(t,{hs},{he})'[a0];")
    last="a0"
    for i,(a,b) in enumerate(st):
        fc+=f"[{last}][{2+i}:v]overlay=0:0:enable='between(t,{a},{b})'[a{i+1}];";last=f"a{i+1}"
    n=2+len(st)
    fc+=f"[{last}][{n}:v]overlay=0:0:enable='gte(t,{cs})'[b1];[b1][{n+1}:v]overlay=0:0:enable='lt(t,{cs})',format=yuv420p[v];"
    fc+=f"[{n+2}:a]{mfilt},atrim=0:{D},afade=t=in:d=0.3,afade=t=out:st={D-0.9}:d=0.9,volume=0.9[a]"
    subprocess.run(["ffmpeg","-y","-loglevel","error"]+ins+["-filter_complex",fc,"-map","[v]","-map","[a]","-t",str(D),"-c:v","libx264","-preset","medium","-crf","20","-c:a","aac","-b:a","160k","-movflags","+faststart",f"{OUT}/{name}.mp4"],check=True)
    return f"{OUT}/{name}.mp4"
CUR=(224,168,60); TRV=(242,140,40)
R=[
("c1-basil",f"{SRC}/c1.mp4",0,"Why your basil dies every winter",[("Too little light","Give it your sunniest window, or a small grow light."),("Too much water","Let the top of the soil dry before watering again."),("Cold glass at night","Keep leaves away from a frosty window.")],("8 easy herbs that grow all winter","Full guide: link in bio"),"curioandcove.com",CUR,T+"lofi.wav"),
("t1-weekend",f"{SRC}/t1.mp4",1,"Weekend la munte sau la mare? Zbor + cazare în 3 minute",[("Alegi datele","Vineri–duminică sau un weekend prelungit."),("Compari zborurile","Sute de companii aeriene, într-o singură căutare."),("Alegi cazarea","Hoteluri și apartamente pentru orice buget.")],("Zbor și cazare, într-un singur loc","Link în bio"),"4travel.pro",TRV,T+"pop.wav"),
("c2-halloween",f"{SRC}/c2.mp4",2,"No costume? 3 family looks from your closet",[("A family of cats","Black clothes, paper ears, a drawn-on nose."),("Cozy ghosts","An old white sheet with a cut-out face."),("Lumberjack crew","Plaid shirts and drawn-on beards.")],("15 easy group costume ideas","Full guide: link in bio"),"curioandcove.com",CUR,T+"halloween.wav"),
("t2-iarna",f"{SRC}/t2.mp4",1,"Când rezervi biletul pentru vacanța de iarnă?",[("Date de vârf","Crăciun și Revelion: ideal cu 5–7 luni înainte."),("N-ai rezervat încă?","Setează azi o alertă de preț pe ruta ta."),("Fii flexibil","O zi mai devreme sau mai târziu poate costa mai puțin.")],("Compară zborurile acum","Link în bio"),"4travel.pro",TRV,T+"phonk.wav"),
("c3-email",f"{SRC}/c3.mp4",0,"The awkward email you keep avoiding, written in 10 seconds",[("Tell a free AI 3 things","Who it's for, what you need, and the tone."),("Try this prompt","\"Politely ask my landlord to fix the heating.\""),("Edit one line","So it sounds like you, then send.")],("12 everyday tasks for a free AI","Full guide: link in bio"),"curioandcove.com",CUR,T+"lofi.wav","asetrate=44100*1.12,aresample=44100,atempo=1.0"),
("t3-combinat",f"{SRC}/t3.mp4",0,"Bilet mai ieftin cu două companii diferite? Se poate",[("Rute combinate","Unele căutări combină zboruri de la companii diferite."),("Poate ieși mai ieftin","Decât un singur bilet de la o companie."),("Verifică escala","Timpul dintre zboruri și regulile de bagaj.")],("Caută rute combinate","Link în bio"),"4travel.pro",TRV,T+"pop.wav","asetrate=44100*0.89,aresample=44100,atempo=1.08"),
]
for r in R: print(reel(*r))
