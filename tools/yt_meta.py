import json,os,sys,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from yt_upload import post,token,tg
done=json.load(open('data/yt_done.json'));tk=token();H={'Authorization':'Bearer '+tk,'Content-Type':'application/json'}
BASE=['i simpson','simpson','springfieldpedia']
SH=['shorts simpson','curiosità simpson','lo sapevi','i simpson curiosità']
T={'V1b':['homer simpson','classifica simpson','migliori scene simpson','follie di homer','top 10 simpson'],
'M1':['chi ha sparato al signor burns','who shot mr burns','simpson misteri','teorie simpson','simpson spiegazione','mr burns simpson'],
'F3':['i simpson prevedono il futuro','previsioni simpson avverate','simpson previsioni','simpson previsioni 2026','simpson previsioni 2027','simpson trump','simpson profezie'],
'F4':['moe szyslak','storia di moe','moe simpson','personaggi simpson','simpson curiosità personaggi'],
'R4':['simpson stagione 4','simpson stagione 4 episodi','migliori episodi dei simpson','retrospettiva simpson','classifica simpson'],
'V1':['springfieldpedia','simpson curiosità','simpson dietro le quinte','simpson episodi','nico springfieldpedia'],
'C1':['last exit to springfield','marge contro la monorotaia','marge vs the monorail','miglior episodio simpson','simpson stagione 4','scontro tra episodi']}
HT={'V1b':'#Classifica','M1':'#MisteriSimpson','F3':'#PrevisioniSimpson','F4':'#StoriaDiUnPersonaggio','R4':'#Stagione4','C1':'#ScontroTraEpisodi'}
LONG=['V1b','M1','F3','F4','R4','C1']
TIT={'V1b':'Le 10 follie di Homer','M1':'Chi ha sparato al signor Burns?','F3':'I Simpson hanno previsto il futuro?','F4':'La storia di Moe','R4':'I 10 migliori episodi della stagione 4','C1':'Last Exit to Springfield vs Marge contro la monorotaia'}
NEW='3 video a settimana e uno Short al giorno. Iscriviti e attiva la campanella!'
out=[]
for k,vid in done.items():
    if k.startswith('_') or not isinstance(vid,str):continue
    s,h,b=post('https://www.googleapis.com/youtube/v3/videos?part=snippet&id='+vid,None,H,'GET');j=json.loads(b)
    if not j.get('items'):out.append(k+': non trovato');continue
    sn=j['items'][0]['snippet'];d=sn.get('description','');tags=sn.get('tags',[])
    new=[]
    for t in BASE+(T.get(k) or SH)+tags:
        if t.lower() not in [x.lower() for x in new]:new.append(t)
    while sum(len(x)+1 for x in new)>450:new.pop()
    d=re.sub(r'Due video a settimana, martedì e venerdì alle 17:00, più Short ogni giorno\.?','3 video a settimana e uno Short al giorno.',d)
    d=re.sub(r'Nuovi video ogni martedì e venerdì alle 17:00\.?',NEW,d)
    d=re.sub(r'Su Springfieldpedia escono [^\n]*',NEW,d) if 'Guarda anche' not in d and k in LONG else d
    if k in LONG and 'Guarda anche' not in d:
        rel=[x for x in LONG if x!=k and x in done][:3]
        d=d.rstrip()+'\n\nGuarda anche:\n'+'\n'.join('%s https://youtu.be/%s'%(TIT[x],done[x]) for x in rel)
        if '#' not in d.split('Guarda anche')[0].split('\n')[-1]:d+='\n\n#ISimpson #Simpson #Springfieldpedia '+HT[k]
    if k not in LONG and '#ISimpson' not in d:d=d.rstrip()+' #ISimpson'
    if k in LONG and NEW not in d:d=d.replace('Guarda anche:',NEW+'\n\nGuarda anche:',1)
    sn['tags']=new;sn['description']=d[:4900]
    body=dict(id=vid,snippet=sn)
    s,h,b=post('https://www.googleapis.com/youtube/v3/videos?part=snippet',json.dumps(body).encode(),H,'PUT')
    out.append('%s: %s %s'%(k,'ok' if s==200 else 'ERRORE',b[:160] if s!=200 else ''))
print('\n'.join(out));tg('YouTube metadati:\n'+'\n'.join(out))
