import json,os,sys,urllib.request,urllib.parse,time,subprocess
def post(url,data=None,headers=None,method='POST'):
    r=urllib.request.Request(url,data=data,headers=headers or {},method=method)
    try:
        with urllib.request.urlopen(r,timeout=600) as x:return x.status,dict(x.headers),x.read()
    except urllib.error.HTTPError as e:return e.code,dict(e.headers),e.read()
def token():
    d=urllib.parse.urlencode(dict(client_id=os.environ['YT_CLIENT_ID'].strip(),client_secret=os.environ['YT_CLIENT_SECRET'].strip(),refresh_token=os.environ['YT_REFRESH_TOKEN'].strip(),grant_type='refresh_token')).encode()
    s,h,b=post('https://oauth2.googleapis.com/token',d,{'Content-Type':'application/x-www-form-urlencoded'});j=json.loads(b)
    if 'access_token' not in j:
        tg('YouTube: rinnovo token fallito: %s / %s'%(j.get('error'),j.get('error_description')));print(j.get('error'),j.get('error_description'));sys.exit(1)
    return j['access_token']
def tg(msg):
    try:
        d=urllib.parse.urlencode(dict(chat_id=os.environ['TELEGRAM_CHAT_ID'].strip(),text=msg,disable_web_page_preview='true')).encode()
        post('https://api.telegram.org/bot%s/sendMessage'%os.environ['TELEGRAM_BOT_TOKEN'].strip(),d)
    except Exception as e:print('tg err',e)
def upload(tk,it,path):
    body=dict(snippet=dict(title=it['title'][:100],description=it['description'],tags=it['tags'],categoryId='24',defaultLanguage='it',defaultAudioLanguage='it'),status=dict(privacyStatus='private',selfDeclaredMadeForKids=False,**({'publishAt':it['publishAt']} if it.get('publishAt') else {})))
    size=os.path.getsize(path)
    s,h,b=post('https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status',json.dumps(body).encode(),{'Authorization':'Bearer '+tk,'Content-Type':'application/json; charset=UTF-8','X-Upload-Content-Length':str(size),'X-Upload-Content-Type':'video/mp4'})
    if s!=200:return None,'init %s %s'%(s,b[:300])
    loc=h.get('Location') or h.get('location')
    with open(path,'rb') as f:data=f.read()
    s,h,b=post(loc,data,{'Content-Type':'video/mp4','Content-Length':str(size)},method='PUT')
    if s not in (200,201):return None,'put %s %s'%(s,b[:300])
    return json.loads(b)['id'],''
def main():
    man=json.load(open('data/yt_manifest.json'));done=json.load(open('data/yt_done.json')) if os.path.exists('data/yt_done.json') else {}
    limit=int(os.environ.get('MAX_UPLOADS','6'));tk=token();n=0;lines=[]
    for it in man:
        if it['id'] in done or it['id']=='_thumbed':continue
        if n>=limit:break
        p='dl/'+it['file']
        if not os.path.exists(p):lines.append('%s: file mancante'%it['id']);continue
        vid,err=upload(tk,it,p)
        if not vid:lines.append('ERRORE %s: %s'%(it['id'],err));
        else:
            n+=1;done[it['id']]=vid;lines.append('OK %s -> https://youtu.be/%s (programmato %s)'%(it['id'],vid,it.get('publishAt','NESSUNO: privato')))
            if it.get('thumb') and os.path.exists('dl/'+it['thumb']):
                d=open('dl/'+it['thumb'],'rb').read();s,h,b=post('https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId='+vid,d,{'Authorization':'Bearer '+tk,'Content-Type':'image/jpeg'})
                lines.append('  miniatura: %s'%('ok' if s==200 else 'non impostata (%s)'%s))
        json.dump(done,open('data/yt_done.json','w'),indent=1)
        if err and 'quota' in err.lower():break
    th=done.setdefault('_thumbed',[])
    for it in man:
        if it['id'] in done and it['id'] not in th and it.get('thumb') and os.path.exists('dl/'+it['thumb']):
            d=open('dl/'+it['thumb'],'rb').read();s,h,b=post('https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId='+done[it['id']],d,{'Authorization':'Bearer '+tk,'Content-Type':'image/jpeg'})
            lines.append('miniatura %s: %s'%(it['id'],'ok' if s==200 else 'non impostata (%s %s)'%(s,str(b)[:120])))
            if s==200:th.append(it['id'])
    json.dump(done,open('data/yt_done.json','w'),indent=1)
    rest=[i['id'] for i in man if i['id'] not in done]
    print('\n'.join(lines))
    tg('YouTube upload:\n'+'\n'.join(lines)+('\nDa caricare ancora: '+', '.join(rest) if rest else '\nTutto caricato.'))
main()
