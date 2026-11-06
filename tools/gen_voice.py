import os,sys,json,re,base64,wave,urllib.request,urllib.error
K=os.environ['GEMINI_API_KEY'].strip()
STYLE=open('data/f3/prompt_voce_nico.txt').read().split('\n')[1]
def call(url,body=None):
    r=urllib.request.Request(url,data=json.dumps(body).encode() if body else None,headers={'Content-Type':'application/json','x-goog-api-key':K})
    try:
        with urllib.request.urlopen(r,timeout=300) as x:return x.status,json.loads(x.read())
    except urllib.error.HTTPError as e:return e.code,e.read().decode()[:600]
s,m=call('https://generativelanguage.googleapis.com/v1beta/models?pageSize=200')
if s!=200:print('LIST ERR',s,m);sys.exit(1)
tts=[x['name'] for x in m['models'] if 'tts' in x['name'].lower()]
print('TTS models:',tts)
model=os.environ.get('TTS_MODEL') or (tts[0] if tts else None)
voice=os.environ.get('VOICE','Charon')
txt=open('data/f3/copione.txt').read()
os.makedirs('out',exist_ok=True)
for mm in re.finditer(r'### B(\d+) [^\n]*\n(.*?)(?=\n###|\Z)',txt,re.S):
    b=int(mm.group(1));t=mm.group(2).strip()
    body={'contents':[{'parts':[{'text':STYLE+'\n\nLeggi questo testo con questa voce:\n'+t}]}],'generationConfig':{'responseModalities':['AUDIO'],'speechConfig':{'voiceConfig':{'prebuiltVoiceConfig':{'voiceName':voice}}}}}
    s,r=call('https://generativelanguage.googleapis.com/v1beta/%s:generateContent'%model,body)
    if s!=200:print('ERR',b,s,r);continue
    d=r['candidates'][0]['content']['parts'][0]['inlineData']['data'];pcm=base64.b64decode(d)
    w=wave.open('out/Previsioni_blocco%02d.wav'%b,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(pcm);w.close()
    print('OK',b,len(pcm)/48000,'s',flush=True)
