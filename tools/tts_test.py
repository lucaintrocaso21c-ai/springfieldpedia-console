import os,sys,json,base64,wave,urllib.request,urllib.error
K=(os.environ.get('GEMINI_TTS_KEY') or os.environ.get('GEMINI_API_KEY') or '').strip()
if not K:print('NESSUN SECRET');sys.exit(1)
def call(url,body=None):
    r=urllib.request.Request(url,data=json.dumps(body).encode() if body else None,headers={'Content-Type':'application/json','x-goog-api-key':K})
    try:
        with urllib.request.urlopen(r,timeout=300) as x:return x.status,json.loads(x.read())
    except urllib.error.HTTPError as e:return e.code,e.read().decode()[:500]
s,m=call('https://generativelanguage.googleapis.com/v1beta/models?pageSize=200')
print('list',s)
tts=[x['name'] for x in m['models'] if 'tts' in x['name'].lower()] if s==200 else []
print(tts)
os.makedirs('out',exist_ok=True)
for model in tts:
  for vc in [{'prebuiltVoiceConfig':{'voiceName':'Nico SimpsonsPedia 1'}},{'prebuiltVoiceConfig':{'voiceName':'Charon'}}]:
    body={'contents':[{'parts':[{'text':'Ciao, io sono Nico, e oggi parliamo di Homer.'}]}],'generationConfig':{'responseModalities':['AUDIO'],'speechConfig':{'voiceConfig':vc}}}
    s,r=call('https://generativelanguage.googleapis.com/v1beta/%s:generateContent'%model,body)
    print(model,list(vc['prebuiltVoiceConfig'].values()),s,r if s!=200 else 'OK')
