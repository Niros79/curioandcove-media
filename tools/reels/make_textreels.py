import subprocess, os, textwrap
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920
B="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"; M="/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf"
OUT="/home/claude/reels2/out"; os.makedirs(OUT,exist_ok=True)
PAL={"curio":dict(bg=(246,241,231),ink=(31,78,74),acc=(200,100,59),hl=(224,168,60),foot="curioandcove.com"),
     "travel":dict(bg=(15,35,64),ink=(255,255,255),acc=(242,140,40),hl=(141,200,232),foot="4travel.pro")}
def wrap(d,t,f,maxw):
    words=t.split(); lines=[]; cur=""
    for w in words:
        test=(cur+" "+w).strip()
        if d.textlength(test,font=f)<=maxw: cur=test
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def card(p,kind,text,sub=None,idx=None,path=None):
    im=Image.new("RGB",(W,H),p["bg"]); d=ImageDraw.Draw(im)
    size=104 if kind=="hook" else 84
    f=ImageFont.truetype(B,size); fs=ImageFont.truetype(M,52)
    lines=wrap(d,text,f,W-160); lh=int(size*1.18)
    blockh=len(lines)*lh+(90 if sub else 0)+(150 if idx else 0)
    y=(H-blockh)//2-60
    if idx:
        r=62; cx=W//2; d.ellipse([cx-r,y,cx+r,y+2*r],fill=p["acc"]); t=str(idx); fb=ImageFont.truetype(B,72)
        d.text((cx-d.textlength(t,font=fb)/2,y+18),t,font=fb,fill=(255,255,255)); y+=150
    for i,l in enumerate(lines):
        col=p["acc"] if (kind=="hook" and i==len(lines)-1) else p["ink"]
        d.text(((W-d.textlength(l,font=f))/2,y),l,font=f,fill=col); y+=lh
    if sub:
        y+=30
        for l in wrap(d,sub,fs,W-200):
            d.text(((W-d.textlength(l,font=fs))/2,y),l,font=fs,fill=p["ink"]); y+=66
    ff=ImageFont.truetype(B,46); ft=p["foot"]
    d.rounded_rectangle([W/2-260,H-260,W/2+260,H-170],radius=45,fill=p["hl"])
    d.text(((W-d.textlength(ft,font=ff))/2,H-248),ft,font=ff,fill=(17,17,17))
    im.save(path)
def reel(name,site,hook,points,cta,music):
    p=PAL[site]; imgs=[]
    card(p,"hook",hook,path=f"{OUT}/{name}_0.png"); imgs.append(f"{OUT}/{name}_0.png")
    for i,(t,s) in enumerate(points,1):
        fp=f"{OUT}/{name}_{i}.png"; card(p,"pt",t,s,i,fp); imgs.append(fp)
    fp=f"{OUT}/{name}_c.png"; card(p,"pt",cta[0],cta[1],None,fp); imgs.append(fp)
    durs=[2.6]+[2.6]*len(points)+[2.6]; xf=0.35
    inputs=[]; 
    for im,dd in zip(imgs,durs): inputs+=["-loop","1","-t",str(dd+xf),"-i",im]
    fc=""; 
    for i in range(len(imgs)):
        fc+=f"[{i}:v]scale=1188:2112,zoompan=z='min(zoom+0.0009,1.06)':d={int((durs[i]+xf)*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,setsar=1,format=yuv420p[v{i}];"
    last="v0"; off=0
    for i in range(1,len(imgs)):
        off+=durs[i-1]; fc+=f"[{last}][v{i}]xfade=transition=slideleft:duration={xf}:offset={off:.2f}[x{i}];"; last=f"x{i}"
    total=sum(durs)+xf
    fc+=f"[{len(imgs)}:a]afade=t=in:d=0.4,afade=t=out:st={total-0.8:.2f}:d=0.8,volume=0.8[a]"
    cmd=["ffmpeg","-y","-loglevel","error"]+inputs+["-i",music,"-filter_complex",fc,"-map",f"[{last}]","-map","[a]","-t",f"{total:.2f}","-c:v","libx264","-preset","medium","-crf","20","-c:a","aac","-b:a","160k","-movflags","+faststart",f"{OUT}/{name}.mp4"]
    subprocess.run(cmd,check=True); return f"{OUT}/{name}.mp4"
T="/home/claude/music/tracks/"
R=[
("c1-basil","curio","Why your basil dies every winter",[("Too little light","Give it your sunniest window, or a small grow light."),("Too much water","Let the top of the soil dry before you water again."),("Cold glass at night","Keep leaves from touching a frosty window.")],("8 easy herbs that grow all winter","Full guide: link in bio"),T+"lofi.wav"),
("t1-weekend","travel","Weekend la munte sau la mare? Zbor + cazare în 3 minute",[("Alegi datele","Vineri–duminică sau un weekend prelungit."),("Compari zborurile","Sute de companii aeriene, într-o singură căutare."),("Alegi cazarea","Hoteluri și apartamente pentru orice buget.")],("Totul într-un singur loc","4travel.pro · link în bio"),T+"pop.wav"),
("c2-halloween","curio","No costume? 3 family looks from your closet",[("A family of cats","Black clothes, paper ears and a drawn-on nose."),("Cozy ghosts","An old white sheet with a cut-out face."),("Lumberjack crew","Plaid shirts and drawn-on beards.")],("15 easy group costume ideas","Full guide: link in bio"),T+"halloween.wav"),
("t2-iarna","travel","Când rezervi biletul pentru vacanța de iarnă?",[("Date de vârf","Crăciun și Revelion: ideal cu 5–7 luni înainte."),("N-ai rezervat încă?","Setează azi o alertă de preț pe ruta ta."),("Fii flexibil","O zi mai devreme sau mai târziu poate costa mult mai puțin.")],("Compară zborurile acum","4travel.pro · link în bio"),T+"phonk.wav"),
("c3-email","curio","The awkward email you keep avoiding, written in 10 seconds",[("Tell a free AI 3 things","Who it's for, what you need, and the tone."),("Try this","\"Politely ask my landlord to fix the heating. Friendly but firm.\""),("Edit one line","So it sounds like you, then send.")],("12 everyday tasks for a free AI","Full guide: link in bio"),T+"lofi.wav"),
("t3-combinat","travel","Bilet mai ieftin cu două companii diferite? Se poate",[("Rute combinate","Unele căutări combină zboruri de la companii diferite."),("Poate ieși mai ieftin","Decât un singur bilet de la o companie."),("Verifică escala","Timpul dintre zboruri și regulile de bagaj.")],("Caută rute combinate","4travel.pro · link în bio"),T+"pop.wav"),
]
for r in R: print(reel(*r))
