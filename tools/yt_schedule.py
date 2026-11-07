import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from yt_upload import post,token,tg
done=json.load(open('data/yt_done.json'));plan=json.load(open('data/yt_schedule.json'));tk=token();out=[]
for k,when in plan.items():
    vid=done.get(k)
    if not vid:out.append('%s: non ancora caricato'%k);continue
    body=dict(id=vid,status=dict(privacyStatus='private',publishAt=when,selfDeclaredMadeForKids=False))
    s,h,b=post('https://www.googleapis.com/youtube/v3/videos?part=status',json.dumps(body).encode(),{'Authorization':'Bearer '+tk,'Content-Type':'application/json'},method='PUT')
    out.append('%s (%s): %s %s'%(k,vid,'programmato '+when if s==200 else 'ERRORE',b[:200] if s!=200 else ''))
print('\n'.join(out));tg('YouTube programmazione:\n'+'\n'.join(out))
