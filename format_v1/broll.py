import subprocess,glob,sys,concurrent.futures as cf
R='/mnt/user-data/uploads/Simpson/'
def F(ep):return glob.glob(R+'*/Season */*%s - *.mkv'%ep)[0]
# block -> list of (t_in_block, episode, source_start, dur)
HOOK=[(3.8,'S04E03',569,1.5),(5.4,'S02E15',1235,1.4),(6.8,'S02E11',302,1.5),(8.2,'S05E15',1134,1.3),(9.7,'S07E07',165,2.4),(12.4,'S04E09',543,0.9),(13.4,'S06E12',477,0.9),(14.4,'S03E17',745,0.9),(15.4,'S01E01',1171,0.9)]
BR={1:HOOK,
2:[(2.1,'S02E15',313,4.5),(6.9,'S02E15',880,5.0),(12.5,'S02E15',1050,3.5),(16.5,'S02E15',1123,3.5),(20.2,'S02E15',1235,3.0)],
3:[(2.4,'S04E03',105,5.0),(7.9,'S04E03',151.5,3.9),(14.6,'S04E03',603,4.0),(22.7,'S04E03',473.4,4.0)],
4:[(1.4,'S02E11',171.5,5.0),(7.3,'S02E11',306.5,4.5),(12.0,'S02E11',430.7,3.1),(15.8,'S02E11',1018,3.0),(19.1,'S02E11',806.7,5.0),(25.3,'S02E11',823,3.0)],
5:[(2.5,'S04E09',157,3.5),(6.0,'S04E09',355,3.0),(13.8,'S04E09',618.2,4.0),(20.6,'S04E09',780,4.0),(25.0,'S04E09',1125,4.0)],
6:[(9.2,'S07E07',329.4,3.5),(23.5,'S07E07',379,4.5),(28.4,'S07E07',1063.6,4.5),(31.5,'S07E07',1078.3,3.4)],
7:[(2.3,'S06E12',278,5.0),(10.3,'S06E12',427,3.0),(13.5,'S06E12',486.8,4.0),(17.5,'S06E12',892,2.2),(19.5,'S06E12',954,4.0),(23.9,'S06E12',971,3.5)],
8:[(3.3,'S06E09',120,4.0),(7.7,'S06E09',578.7,4.5),(12.5,'S06E09',631,3.0),(19.4,'S06E09',597.6,3.5)],
9:[(2.8,'S03E17',715,4.0),(8.7,'S03E17',487,5.5),(15.2,'S03E17',1051,4.5),(19.8,'S03E17',1067.4,3.0),(22.2,'S03E17',1098.2,3.5)],
10:[(2.7,'S05E15',255.6,5.5),(9.4,'S05E15',318.3,2.4),(11.9,'S05E15',858.1,3.5),(15.8,'S05E15',949,3.5),(19.5,'S05E15',1134,2.4)],
11:[(3.3,'S01E01',464,4.0),(6.6,'S01E01',675,3.4),(10.2,'S01E01',962,3.3),(13.6,'S01E01',1097,2.1),(15.8,'S01E01',1171,1.0),(16.9,'S01E01',1239.8,4.2),(24.0,'S01E01',1282,4.5)]}
SPLIT={2:12.35,3:11.8,4:15.2,5:13.64,6:9.1,7:9.2,8:15.7,9:7.3,10:8.3,11:21.1}
def run(b):
    L=BR[b];base='nb%02d.mp4'%b;out='nbx%02d.mp4'%b
    cmd=['ffmpeg','-v','error','-y','-i',base];fc='';last='[0:v]'
    for k,(t,ep,ss,d) in enumerate(L):
        cmd+=['-ss',str(ss),'-t',str(d),'-i',F(ep)]
        fc+='[%d:v]scale=1920:1080,setsar=1,fps=30,setpts=PTS-STARTPTS+%.2f/TB[b%d];'%(k+1,t,k)
        fc+='%s[b%d]overlay=enable=\'between(t,%.2f,%.2f)\':eof_action=pass[o%d];'%(last,k,t,t+d,k);last='[o%d]'%k
    cmd+=['-filter_complex',fc.rstrip(';'),'-map',last,'-map','0:a','-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p','-c:a','copy',out]
    r=subprocess.run(cmd,capture_output=True,text=True);print(b,r.returncode,r.stderr[:300],flush=True)
def split(b):
    import subprocess as sp
    t=SPLIT[b]
    for nm,a,d in (('a',0,t),('b',t,None)):
        cmd=['ffmpeg','-v','error','-y','-i','nbx%02d.mp4'%b]+(['-ss','%.3f'%a])+([] if d is None else ['-t','%.3f'%(d-a)])
        cmd=['ffmpeg','-v','error','-y','-ss','%.3f'%a,'-i','nbx%02d.mp4'%b]+([] if d is None else ['-t','%.3f'%(d-a)])+['-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','nbx%02d%s.mp4'%(b,nm)]
        sp.run(cmd,capture_output=True)
if __name__=='__main__':
    bs=[int(x) for x in sys.argv[1:]]
    with cf.ThreadPoolExecutor(2) as ex:list(ex.map(run,bs))
