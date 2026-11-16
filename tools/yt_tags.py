import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from yt_upload import post,token
MODE=os.environ.get('MODE','list')
done=json.load(open('data/yt_done.json'));tk=token();H={'Authorization':'Bearer '+tk,'Content-Type':'application/json'}
def get(u):
    s,h,b=post(u,None,H,'GET');return s,json.loads(b)
if MODE=='list':
    s,j=get('https://www.googleapis.com/youtube/v3/channels?part=brandingSettings,snippet,statistics&mine=true')
    print('CHANNEL',s,json.dumps(j.get('items',[{}])[0].get('brandingSettings',{}),ensure_ascii=False))
    for k,v in done.items():
        if k.startswith('_') or not isinstance(v,str):continue
        s,j=get('https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails&id='+v)
        if not j.get('items'):print(k,v,'non trovato');continue
        it=j['items'][0];sn=it['snippet']
        print('VID',k,v,it['contentDetails']['duration'],it['status']['privacyStatus'],'|',sn['title'],'|',json.dumps(sn.get('tags',[]),ensure_ascii=False))
else:
    T=json.load(open('data/yt_tags.json'))
    out=[]
    for k,tags in T['videos'].items():
        v=done.get(k)
        if not v:out.append(k+': non caricato');continue
        s,j=get('https://www.googleapis.com/youtube/v3/videos?part=snippet&id='+v)
        sn=j['items'][0]['snippet'];sn['tags']=tags
        s,h,b=post('https://www.googleapis.com/youtube/v3/videos?part=snippet',json.dumps(dict(id=v,snippet=sn)).encode(),H,'PUT')
        out.append('%s: %s %s'%(k,'ok' if s==200 else 'ERRORE',b[:200] if s!=200 else ''))
    s,j=get('https://www.googleapis.com/youtube/v3/channels?part=brandingSettings&mine=true')
    c=j['items'][0];c['brandingSettings']['channel']['keywords']=T['channel']
    s,h,b=post('https://www.googleapis.com/youtube/v3/channels?part=brandingSettings',json.dumps(dict(id=c['id'],brandingSettings=c['brandingSettings'])).encode(),H,'PUT')
    out.append('canale: %s %s'%('ok' if s==200 else 'ERRORE',b[:300] if s!=200 else ''))
    print('\n'.join(out))
