#!/usr/bin/env python3
"""Genera copertine con le API di OpenAI (gpt-image-1).
Uso (dal workflow): COVER_DIR=covers/openai/L01 python3 tools/cover_openai.py
Nella cartella servono: prompt_A.txt, prompt_B.txt, prompt_C.txt (uno per variante) e,
facoltative, immagini di riferimento in ref/ (png/jpg: pose di Nico, fotogrammi, brand).
Output: out_A.jpg, out_B.jpg, out_C.jpg a 1280x720 (<2 MB, formato YouTube)."""
import os,sys,glob,base64,io
from openai import OpenAI
from PIL import Image
DIRS=(os.environ.get('COVER_DIR') or sys.argv[1]).replace(',',' ').split()
key=os.environ.get('OPENAI_API_KEY','').strip()
if not key:sys.exit('OPENAI_API_KEY mancante: va impostata nei secrets di GitHub')
cl=OpenAI(api_key=key)
for d in DIRS:
    VERT=os.path.exists(os.path.join(d,'verticale'))
    SZ='1024x1536' if VERT else '1536x1024'
    refs=sorted(glob.glob(os.path.join(d,'ref','*.png'))+glob.glob(os.path.join(d,'ref','*.jpg')))
    for v in 'ABC':
        pf=os.path.join(d,'prompt_%s.txt'%v)
        if not os.path.exists(pf):continue
        prompt=open(pf,encoding='utf-8').read().strip()
        r=None;err=''
        for mod in os.environ.get('COVER_MODELS','gpt-image-2,gpt-image-1.5,gpt-image-1').split(','):
            try:
                if refs:
                    r=cl.images.edit(model=mod,image=[open(p,'rb') for p in refs],prompt=prompt,size=SZ,quality='high')
                else:
                    r=cl.images.generate(model=mod,prompt=prompt,size=SZ,quality='high')
                print('modello',mod);break
            except Exception as e:
                err+='%s: %s\n'%(mod,str(e)[:300]);print('ERRORE',v,mod,str(e)[:300])
        if r is None:
            open(os.path.join(d,'errore_%s.txt'%v),'w').write(err);continue
        im=Image.open(io.BytesIO(base64.b64decode(r.data[0].b64_json))).convert('RGB')
        w,h=im.size
        if VERT:
            tw=int(h*9/16);left=(w-tw)//2
            im=im.crop((left,0,left+tw,h)).resize((1080,1920),Image.LANCZOS)
        else:
            th=int(w*9/16);top=(h-th)//2
            im=im.crop((0,top,w,top+th)).resize((1280,720),Image.LANCZOS)
        q=92
        while True:
            b=io.BytesIO();im.save(b,'JPEG',quality=q)
            if b.tell()<1900000 or q<60:break
            q-=6
        open(os.path.join(d,'out_%s.jpg'%v),'wb').write(b.getvalue());print('ok',v,b.tell())
