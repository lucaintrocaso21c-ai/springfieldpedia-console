#!/usr/bin/env python3
"""Ritagli personaggi con sfondo trasparente (gpt-image). CHAR_DIR=covers/char python3 tools/char_openai.py [nomi]"""
import os,sys,glob,base64
from openai import OpenAI
cl=OpenAI(api_key=os.environ['OPENAI_API_KEY'])
root=os.environ.get('CHAR_DIR','covers/char');names=sys.argv[1:] or sorted(os.listdir(root))
for n in names:
    d=os.path.join(root,n);refs=sorted(glob.glob(d+'/ref/*.png'));p=open(d+'/prompt.txt',encoding='utf-8').read().strip();err=''
    for mod in ('gpt-image-2','gpt-image-1.5'):
        try:
            r=cl.images.edit(model=mod,image=[open(x,'rb') for x in refs],prompt=p,size='1024x1536',quality='high')
            open(d+'/raw.png','wb').write(base64.b64decode(r.data[0].b64_json));print(n,'ok',mod);break
        except Exception as e:err+='%s: %s\n'%(mod,str(e)[:300]);print('ERR',n,mod,str(e)[:200])
    else:open(d+'/errore.txt','w').write(err)
