import json,os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from yt_upload import post,token,tg
done=json.load(open('data/yt_done.json'));tk=token();H={'Authorization':'Bearer '+tk,'Content-Type':'application/json'}
T={'L01':'Chi ha sparato a Burns? Tutti gli indizi','L02':'I Simpson avevano previsto Trump?','L03':'Che fine hanno fatto i personaggi dimenticati dei Simpson?','L04':'La storia completa di Telespalla Bob','L09':'Homer Simpson è cambiato davvero?','L10':'Il signor Burns: da magnate crudele a icona'}
MAP={'S01':'L03','S01b':'L03','S01c':'L03','S02':'L02','S02b':'L02','S02c':'L02','S04':'L01','S05':'L04','S06':'L09','L01':'L10','L10':'L01'}
out=[]
for k,t in MAP.items():
    vid=done.get(k);tv=done.get(t)
    if not vid or not tv:out.append(k+': id mancante');continue
    s,h,b=post('https://www.googleapis.com/youtube/v3/videos?part=snippet&id='+vid,None,H,'GET');j=json.loads(b)
    if not j.get('items'):out.append(k+': non trovato');continue
    sn=j['items'][0]['snippet'];d=sn.get('description','')
    if tv in d:out.append(k+': gia collegato');continue
    link='▶ '+('Guarda anche' if k.startswith('L') else 'Il video completo')+': '+T[t]+' https://youtu.be/'+tv
    sn['description']=(link+'\n\n'+d)[:4900]
    s,h,b=post('https://www.googleapis.com/youtube/v3/videos?part=snippet',json.dumps(dict(id=vid,snippet=sn)).encode(),H,'PUT')
    r='%s -> %s: %s'%(k,t,'ok' if s==200 else 'ERRORE %s %s'%(s,b[:150]))
    if s==200 and not k.startswith('L'):
        c=dict(snippet=dict(videoId=vid,topLevelComment=dict(snippet=dict(textOriginal='▶ Il video completo qui: https://youtu.be/%s\nIscriviti per non perdere i prossimi!'%tv))))
        s2,h2,b2=post('https://www.googleapis.com/youtube/v3/commentThreads?part=snippet',json.dumps(c).encode(),H,'POST')
        r+=' | commento: %s'%('ok' if s2==200 else 'ERRORE %s %s'%(s2,b2[:120]))
    out.append(r)
print('\n'.join(out));tg('YouTube link Short->video:\n'+'\n'.join(out))
