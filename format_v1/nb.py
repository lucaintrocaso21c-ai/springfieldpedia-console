import numpy as np,wave,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
S='/tmp/claude-0/-home-claude/87164e15-4779-5c7a-be25-1e13b780e99b/scratchpad/'
D='/mnt/user-data/uploads/Desktop/Springfieldpedia/08_Definitivo_v2/'
W,H,FPS=1920,1080,30
YEL=(255,217,15)
LIL=lambda s:ImageFont.truetype(S+'lilita-one-latin-400-normal.ttf',s)
yy,xx=np.mgrid[0:H,0:W];vig=(1-0.45*(((xx-W/2)/(W/2))**2*.8+((yy-H/2)/(H/2))**2*.9)).clip(.3,1)[...,None].astype(np.float32)
def ld(p):
    x=np.asarray(Image.open(D+p).convert('RGB').resize((W,H),Image.LANCZOS),dtype=np.float32)/255
    x=(x-.5)*1.1+.5;x[...,0]*=1.03;x[...,2]*=1.05;x*=vig
    return Image.fromarray((x.clip(0,1)*255).astype('uint8')).convert('RGBA')
NM={'c':'chiusa','e':'e_semi','a':'a_aperta','o':'o','i':'i_sorriso'}
PO=['saluta','spiega_mani_aperte','dito_alzato']
POSE={p:{k:ld('bocche/%s_%s.png'%(p,n)) for k,n in NM.items()} for p in PO}
def eo(t):t=min(max(t,0),1);return 1-(1-t)**3
def chip(base,t,cx,cy,size,col,al=1):
    L=Image.new('RGBA',(W,300),(0,0,0,0));d=ImageDraw.Draw(L);f=LIL(size);tw=d.textlength(t,font=f);h=size*1.6
    d.rounded_rectangle([W/2-tw/2-44,150-h/2,W/2+tw/2+44,150+h/2],radius=h/2,fill=col+(235,),outline=(255,255,255,255),width=5)
    d.text((W/2-tw/2,150-size*.64),t,font=f,fill=(255,255,255))
    if al<1:L.putalpha(L.getchannel('A').point(lambda v:int(v*max(al,0))))
    base.alpha_composite(L,(int(cx-W/2),int(cy-150)))
def big(base,t,cx,cy,size,fill,al=1):
    L=Image.new('RGBA',(W,400),(0,0,0,0));d=ImageDraw.Draw(L);f=LIL(size);tw=d.textlength(t,font=f)
    d.text((W/2-tw/2+5,200-size*.6+7),t,font=f,fill=(0,0,0,180));d.text((W/2-tw/2,200-size*.6),t,font=f,fill=fill,stroke_width=4,stroke_fill=(0,0,0))
    if al<1:L.putalpha(L.getchannel('A').point(lambda v:int(v*max(al,0))))
    base.alpha_composite(L,(int(cx-W/2),int(cy-200)))
def states(a,SR,T):
    nfr=int(T*FPS);hop=SR//FPS;env=np.zeros(nfr)
    for i in range(nfr):
        s=i*hop
        if s<len(a)-hop:env[i]=np.sqrt(np.mean(a[s:s+hop+hop//2]**2)+1e-9)
    env=np.convolve(env,np.ones(2)/2,'same');lv=env/np.percentile(env[env>0.01],90)
    st=[];cyc=0;prev='c';hold=0
    for v in lv:
        if v<0.12:s='c'
        elif v<0.45:s=('e','o','e','i')[cyc%4]
        else:s=('a','a','i','a','e')[cyc%5]
        if s!=prev:
            if hold<2 and prev!='c' and s!='c':s=prev
            else:cyc+=1;hold=0
        hold+=1;prev=s;st.append(s)
    return st
TIT={1:None,2:('10','S02E15 · Oh Brother, Where Art Thou?',(61,95,168)),3:('9','S04E03 · Homer the Heretic',(242,107,33)),4:('8','S02E11 · One Fish, Two Fish…',(40,140,90)),5:('7','S04E09 · Mr. Plow',(200,70,130)),6:('6','S07E07 · King-Size Homer',(61,95,168)),7:('5','S06E12 · Homer the Great',(242,107,33)),8:('4','S06E09 · Homer Badman',(40,140,90)),9:('3','S03E17 · Homer at the Bat',(200,70,130)),10:('2','S05E15 · Deep Space Homer',(61,95,168)),11:('1','S01E01 · Simpsons Roasting on an Open Fire',(242,107,33)),12:None}
def run(b):
    w=wave.open('vo%02d.wav'%b);SR=w.getframerate();a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    dur=len(a)/SR+0.5;nfr=int(dur*FPS);st=states(a,SR,dur)
    # pose schedule: switch ~every 6.5 s
    seg=6.5;order=[0,1,2,1] if b%2 else [1,2,0,2]
    if b==1:order=[0,1,2,1,0]
    out='nb%02d.mp4'%b
    pr=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','%dx%d'%(W,H),'-r',str(FPS),'-i','-','-i','vo%02d.wav'%b,'-af','apad=whole_dur=%.3f,aresample=48000'%dur,'-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t','%.3f'%dur,out],stdin=subprocess.PIPE)
    for i in range(nfr):
        t=i/FPS;p=PO[order[int(t//seg)%len(order)]]
        im=POSE[p][st[i]].copy()
        info=TIT[b]
        if info:
            n,tt,col=info
            big(im,'N°'+n,420,300,200,YEL,al=min(eo(t/.25),eo((dur-t)/.3)))
            if t>.5:chip(im,tt,960,1010,44,col,al=eo((t-.5)/.25))
        elif b==1:
            if t>1:chip(im,'LE 10 FOLLIE PIÙ GRANDI DI HOMER',960,1010,50,(61,95,168),al=min(eo((t-1)/.25),eo((7-t)/.25)))
        elif b==12 and t>dur-9:
            chip(im,'ISCRIVITI',420,300,84,(220,30,30),al=eo((t-(dur-9))/.2))
            chip(im,'MARTEDÌ + VENERDÌ · ORE 17:00',960,1010,46,(61,95,168),al=eo((t-(dur-8))/.2))
        pr.stdin.write(im.convert('RGB').tobytes())
    pr.stdin.close();pr.wait()
if __name__=='__main__':
    for b in map(int,sys.argv[1:]):run(b)
