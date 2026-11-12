import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from yt_upload import post,token,tg
done=json.load(open('data/yt_done.json'));tk=token();H={'Authorization':'Bearer '+tk,'Content-Type':'application/json'};out=[]
for k in (os.environ.get('PAUSE_KEYS') or 'S7,S8,F3,F4,R4,C1').split(','):
    vid=done[k]
    body=dict(id=vid,status=dict(privacyStatus='private',selfDeclaredMadeForKids=False))
    s,h,b=post('https://www.googleapis.com/youtube/v3/videos?part=status',json.dumps(body).encode(),H,'PUT')
    out.append('%s: %s %s'%(k,'in pausa (privato, senza data)' if s==200 else 'ERRORE',b[:150] if s!=200 else ''))
print('\n'.join(out));tg('YouTube pausa:\n'+'\n'.join(out))
