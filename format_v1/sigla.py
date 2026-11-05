import numpy as np,subprocess,wave,math
from PIL import Image,ImageDraw,ImageFont
S='/tmp/claude-0/-home-claude/87164e15-4779-5c7a-be25-1e13b780e99b/scratchpad/'
K='/home/claude/springfieldpedia/out/'
W,H,FPS,T=1920,1080,30,5.5
LIL=lambda s:ImageFont.truetype(S+'lilita-one-latin-400-normal.ttf',s)
BAL=lambda s:ImageFont.truetype(S+'baloo-2-latin-800-normal.ttf',s)
lo=Image.open(K+'logo_orizzontale.png').convert('RGBA');lo=lo.crop(lo.getbbox())
em=Image.open(K+'logo_emblema.png').convert('RGBA');em=em.crop(em.getbbox())
yy,xx=np.mgrid[0:H,0:W]
def eo(t):t=min(max(t,0),1);return 1-(1-t)**3
def eb(t):
    t=min(max(t,0),1);c=1.70158;return 1+(c+1)*(t-1)**3+c*(t-1)**2
def frame(i):
    t=i/FPS
    g=np.exp(-(((xx-W/2)/800)**2+((yy-H/2)/450)**2))[...,None]*np.array([80,40,125],dtype=np.float32)
    # rays
    a=np.arctan2(yy-H/2,xx-W/2);r=np.exp(-(((xx-W/2)/900)**2+((yy-H/2)/900)**2))
    rays=(np.sin(a*14+t*1.5)>.6)*r*18*eo(t/.8)
    x=np.array([14,8,34],dtype=np.float32)+g+rays[...,None]*np.array([1,.8,.4])
    im=Image.fromarray(x.clip(0,255).astype('uint8')).convert('RGBA')
    sc=.3+.7*eb(t/.7)
    L=lo.resize((int(lo.width*520/lo.height*sc),int(520*sc)),Image.LANCZOS)
    L.putalpha(L.getchannel('A').point(lambda v:int(v*eo(t/.3))))
    im.alpha_composite(L,(int(W/2-L.width/2),int(470-L.height/2)))
    d=ImageDraw.Draw(im)
    if t>1.0:
        al=eo((t-1.0)/.5);tx='Tutto quello che non sapevi sui Simpson';f=BAL(64);tw=d.textlength(tx,font=f)
        T_=Image.new('RGBA',(W,200),(0,0,0,0));dd=ImageDraw.Draw(T_);dd.text((W/2-tw/2+4,100-40+5),tx,font=f,fill=(0,0,0,180));dd.text((W/2-tw/2,100-40),tx,font=f,fill=(255,255,255,255))
        T_.putalpha(T_.getchannel('A').point(lambda v:int(v*al)));im.alpha_composite(T_,(0,780-100))
    if t<.12:im=Image.blend(im,Image.new('RGBA',(W,H),(255,255,255,255)),1-t/.12)
    if t>T-.4:im=Image.blend(im,Image.new('RGBA',(W,H),(0,0,0,255)),(t-(T-.4))/.4)
    return im.convert('RGB')
MR=44100;n=int(T*MR);m=np.zeros(n)
mid=lambda p:440*2**((p-69)/12)
def tone(f,t0,d,amp,harm=(1,.5),atk=.01,rel=.5):
    i0=int(t0*MR);k=int(d*MR);i1=min(n,i0+k);x=np.arange(i1-i0)/MR;y=sum(h*np.sin(2*np.pi*f*(j+1)*x) for j,h in enumerate(harm))
    e=np.minimum(1,x/atk)*np.minimum(1,(d-x)/rel).clip(0,1);m[i0:i1]+=amp*y*e
rng=np.random.default_rng(3)
k=int(1.2*MR);x=np.arange(k)/MR;m[:k]+=.9*(np.sin(2*np.pi*(80-40*x/1.2)*x)*np.exp(-x*3)+.25*rng.normal(0,1,k)*np.exp(-x*12))
for j,p in enumerate([60,64,67,72,76,79,84]):tone(mid(p),.15+j*.11,1.2,.1,(1,.3),rel=.8)
for p in [60,64,67,72]:tone(mid(p),1.0,4.2,.08,(1,.5,.2),atk=.05,rel=1.5)
m/=np.abs(m).max();m*=.8;m[-int(.4*MR):]*=np.linspace(1,0,int(.4*MR))
with wave.open('sigla.wav','w') as o:o.setnchannels(1);o.setsampwidth(2);o.setframerate(MR);o.writeframes((m*32767).astype('<i2').tobytes())
pr=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-i','sigla.wav','-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest','sigla.mp4'],stdin=subprocess.PIPE)
for i in range(int(T*FPS)):pr.stdin.write(frame(i).tobytes())
pr.stdin.close();pr.wait()
frame(60).resize((640,360)).save('sigla_prev.jpg')
