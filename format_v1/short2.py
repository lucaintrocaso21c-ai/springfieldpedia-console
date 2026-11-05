import sys,json,subprocess,numpy as np
from PIL import Image,ImageDraw
import nb
from nb import POSE,LIL,states,eo,YEL
import wave
from broll import F
FD='/tmp/claude-0/-home-claude/87164e15-4779-5c7a-be25-1e13b780e99b/scratchpad'
FPS=30
EPN={1:('S02E15','Oh Brother, Where Art Thou?'),2:('S03E17','Homer at the Bat'),3:('S05E15','Deep Space Homer'),4:('S04E09','Mr. Plow'),5:('S06E12','Homer the Great'),6:('S07E07','King-Size Homer'),7:('S02E11','One Fish, Two Fish…'),8:('S04E03','Homer the Heretic')}
# scenes: (t, ep, src, dur); nico_end: seconds of Nico at the end
SC={1:[(0.9,'S02E15',660,4.8),(5.7,'S02E15',995,4.6),(10.3,'S02E15',1050,1.0),(11.3,'S02E15',1102,3.6),(14.9,'S02E15',1268,2.4)],
2:[(1.6,'S03E17',519,3.5),(5.1,'S03E17',737.9,5.4),(11.0,'S03E17',1067.4,2.3)],
3:[(0.7,'S05E15',405,5.8),(6.5,'S05E15',858,1.9),(8.4,'S05E15',949,2.6),(11.0,'S05E15',1134,2.8),(13.8,'S05E15',616,3.2)],
4:[(0.9,'S04E09',331.4,6.9),(7.8,'S04E09',337.9,4.4)],
5:[(1.0,'S06E12',226.2,4.2),(5.2,'S06E12',440.8,6.0),(11.2,'S06E12',450.5,3.1)],
6:[(0.7,'S07E07',188,4.6),(5.3,'S07E07',329.4,2.5),(7.8,'S07E07',1068.3,5.6)],
7:[(0.8,'S02E11',302,1.8),(2.6,'S02E11',436,5.8),(8.4,'S02E11',446.2,1.1),(9.5,'S02E11',806.7,2.8)],
8:[(0.8,'S04E03',569,3.4),(4.2,'S04E03',570.8,2.3),(6.5,'S04E03',574.3,3.4),(8.2,'S04E03',599,3.1),(11.3,'S04E03',1203,3.0)]}
W,H=1080,1920
CR={}
def crop(p,m):
    k=(p,m)
    if k not in CR:CR[k]=POSE[p][m].crop((696,0,1304,1080)).resize((W,H),Image.LANCZOS).convert('RGB')
    return CR[k]
def bgimg():
    yy,xx=np.mgrid[0:H,0:W];g=np.exp(-(((xx-W/2)/700)**2+((yy-H/2)/900)**2))[...,None]*np.array([60,30,100],dtype=np.float32)
    return Image.fromarray((np.array([12,8,30],dtype=np.float32)+g).clip(0,255).astype('uint8'))
def overlay_png(k):
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    def chip(t,cx,cy,size,col):
        f=LIL(size);tw=d.textlength(t,font=f);h=size*1.6
        d.rounded_rectangle([cx-tw/2-36,cy-h/2,cx+tw/2+36,cy+h/2],radius=h/2,fill=col+(240,),outline=(255,255,255,255),width=5);d.text((cx-tw/2,cy-size*.64),t,font=f,fill=(255,255,255))
    chip('LO SAPEVI?',W/2,150,78,(220,40,60))
    chip(EPN[k][0]+' · '+EPN[k][1],W/2,290,40,(61,95,168))
    f=LIL(46);t='Springfieldpedia';tw=d.textlength(t,font=f);d.text((W/2-tw/2+3,1800+4),t,font=f,fill=(0,0,0,200));d.text((W/2-tw/2,1800),t,font=f,fill=(255,217,15),stroke_width=3,stroke_fill=(0,0,0))
    im.save('s2/ov%d.png'%k)
def ts(x):
    h=int(x//3600);m=int(x%3600//60);s=x%60;return '%d:%02d:%05.2f'%(h,m,s)
def ass(k,sent):
    A='[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Italic,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV\nStyle: C,Lilita One,84,&H00FFFFFF,&H00000000,&H80000000,0,0,1,7,3,8,60,60,1240\n[Events]\nFormat: Layer,Start,End,Style,Text\n'
    for s in sent:
        ws=s['s'].replace('?','?').split();n=len(ws)
        wt=[len(w)+1 for w in ws];tot=sum(wt);span=max(s['t1']-s['t0']-.12,.3);t=s['t0']
        times=[]
        for w,x in zip(ws,wt):times.append((t,t+span*x/tot));t+=span*x/tot
        for i in range(n):
            g0=(i//3)*3;grp=list(range(g0,min(g0+3,n)))
            txt=' '.join(('{\\c&H0FD9FF&}%s{\\c&HFFFFFF&}'%ws[j].upper()) if j==i else ws[j].upper() for j in grp)
            end=times[i+1][0] if i+1<n else s['t1']
            A+='Dialogue: 0,%s,%s,C,%s\n'%(ts(times[i][0]),ts(end),txt)
    open('s2/c%d.ass'%k,'w').write(A)
def run(k):
    S=json.load(open('s2/sent.json'))[str(k)];D=S['dur']+.4
    w=wave.open('s2/sv%d.wav'%k);SR=w.getframerate();a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float32)/32768
    st=states(a,SR,D);nfr=int(D*FPS)
    sc=SC[k];covered=lambda t:any(x[0]<=t<x[0]+x[3] for x in sc)
    bg=bgimg();overlay_png(k);ass(k,S['sent'])
    pr=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','s2/base%d.mp4'%k],stdin=subprocess.PIPE)
    for i in range(nfr):
        t=i/FPS;p='saluta' if t<2 else 'dito_alzato'
        im=crop(p,st[i]) if True else bg
        pr.stdin.write(np.asarray(im).tobytes())
    pr.stdin.close();pr.wait()
    cmd=['ffmpeg','-v','error','-y','-i','s2/base%d.mp4'%k,'-i','s2/sv%d.wav'%k,'-stream_loop','-1','-i','music.wav','-i','s2/ov%d.png'%k]
    fc='';last='[0:v]'
    for i,(t,ep,ss,d) in enumerate(sc):
        cmd+=['-ss',str(ss),'-t',str(d),'-i',F(ep)];n=4+i
        fc+='[%d:v]fps=30,setpts=PTS-STARTPTS+%.2f/TB,split[x%d][y%d];'%(n,t,i,i)
        fc+='[x%d]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:6,eq=brightness=-0.3[b%d];'%(i,i)
        fc+='[y%d]scale=1056:594,pad=1080:618:12:12:white[f%d];'%(i,i)
        fc+='%s[b%d]overlay=0:0:enable=\'between(t,%.2f,%.2f)\':eof_action=pass[p%d];[p%d][f%d]overlay=0:520:enable=\'between(t,%.2f,%.2f)\':eof_action=pass[q%d];'%(last,i,t,t+d,i,i,i,t,t+d,i);last='[q%d]'%i
    fc+='%s[3:v]overlay=0:0[o1];[o1]ass=s2/c%d.ass:fontsdir=%s[v];[1:a]aresample=48000,aformat=channel_layouts=stereo[va];[2:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.10[ma];[va][ma]amix=inputs=2:normalize=0:duration=first[a]'%(last,k,FD)
    cmd+=['-filter_complex',fc,'-map','[v]','-map','[a]','-t','%.2f'%D,'-c:v','libx264','-crf','22','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart','s2/short2_%d.mp4'%k]
    r=subprocess.run(cmd,capture_output=True,text=True);print(k,r.returncode,r.stderr[-400:],flush=True)
if __name__=='__main__':
    for k in map(int,sys.argv[1:]):run(k)
