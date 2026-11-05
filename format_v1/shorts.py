import subprocess,sys,concurrent.futures as cf
from PIL import Image,ImageDraw,ImageFont
from broll import F,BR
S='/tmp/claude-0/-home-claude/87164e15-4779-5c7a-be25-1e13b780e99b/scratchpad/'
LIL=lambda s:ImageFont.truetype(S+'lilita-one-latin-400-normal.ttf',s)
TT={2:('N°10','Oh Brother, Where Art Thou?'),3:('N°9','Homer the Heretic'),4:('N°8','One Fish, Two Fish, Blowfish, Blue Fish'),5:('N°7','Mr. Plow'),6:('N°6','King-Size Homer'),7:('N°5','Homer the Great'),8:('N°4','Homer Badman'),9:('N°3','Homer at the Bat'),10:('N°2','Deep Space Homer'),11:('N°1','Simpsons Roasting on an Open Fire')}
def title(b):
    n,e=TT[b];im=Image.new('RGBA',(1080,180),(0,0,0,0));d=ImageDraw.Draw(im)
    f=LIL(110);tw=d.textlength(n,font=f);d.text((540-tw/2+4,4+6),n,font=f,fill=(0,0,0,200));d.text((540-tw/2,4),n,font=f,fill=(255,217,15),stroke_width=5,stroke_fill=(0,0,0))
    f2=LIL(40);tw=d.textlength(e,font=f2);d.text((540-tw/2,132),e,font=f2,fill=(255,255,255),stroke_width=3,stroke_fill=(0,0,0))
    im.save('sh/t%d.png'%b)
def run(b):
    title(b);a,bb,c=[x[2] for x in BR[b]]
    ss=[(a,5.5),(bb,5.5),(c,5.5),(a+6,5.5),(bb+6,5.5),(c+6,5.5)];ep=BR[b][0][1]
    cmd=['ffmpeg','-v','error','-y','-i','nb%02d.mp4'%b]
    for s,d in ss:cmd+=['-ss',str(s),'-t',str(d),'-i',F(ep)]
    cmd+=['-i','sh/t%d.png'%b,'-i','clips/c%d.mp4'%(11-b+1) if False else 'clips/c%d.mp4'%(12-b)]
    k=len(ss)+1
    fc='[0:v]split[a][b];[a]crop=1080:960:640:0[n];[b]scale=-2:1920,crop=1080:1920,boxblur=30,eq=brightness=-0.3[bg];[bg][n]overlay=0:960[v0];[v0]drawbox=x=0:y=246:w=1080:h=616:color=white:t=fill[v1];'
    last='[v1]'
    for i,(s,d) in enumerate(ss):
        t=i*5.5
        fc+='[%d:v]scale=1080:608,setsar=1,fps=30,setpts=PTS-STARTPTS+%.2f/TB[w%d];%s[w%d]overlay=0:250:enable=\'between(t,%.2f,%.2f)\':eof_action=pass[o%d];'%(i+1,t,i,last,i,t,t+d,i);last='[o%d]'%i
    fc+='%s[%d:v]overlay=0:0[nv];'%(last,k)
    m=k+1
    fc+='[%d:v]fps=30,setsar=1,split[c1][c2];[c1]scale=-2:1920,crop=1080:1920,boxblur=30,eq=brightness=-0.3[cb];[c2]scale=1080:608[cf];[cb][cf]overlay=0:656[cv];'%m
    fc+='[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[%d:a]aresample=48000,aformat=channel_layouts=stereo[a1];[nv]fps=30,format=yuv420p[nv2];[cv]format=yuv420p[cv2];[nv2][a0][cv2][a1]concat=n=2:v=1:a=1[v][a]'%m
    cmd+=['-filter_complex',fc,'-map','[v]','-map','[a]','-c:v','libx264','-crf','23','-preset','veryfast','-c:a','aac','-b:a','160k','-movflags','+faststart','sh/short_N%s.mp4'%TT[b][0][2:]]
    r=subprocess.run(cmd,capture_output=True,text=True);print(b,r.returncode,r.stderr[-400:],flush=True)
if __name__=='__main__':
    with cf.ThreadPoolExecutor(2) as ex:list(ex.map(run,[int(x) for x in sys.argv[1:]]))
