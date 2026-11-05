import re,wave,numpy as np,json
txt=open('copione_v2.txt').read();blocks={}
for m in re.finditer(r'### B(\d+) [^\n]*\n(.*?)(?=\n###|\Z)',txt,re.S):blocks[int(m.group(1))]=m.group(2).strip()
out={}
for b,t in blocks.items():
    ss=[s.strip() for s in re.split(r'(?<=[.!?])\s+',t) if s.strip()]
    # merge very short ones like "Chi?" kept
    w=wave.open('vo%02d.wav'%b);SR=w.getframerate();a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768;D=len(a)/SR
    hop=int(SR*.02);e=np.array([np.sqrt(np.mean(a[i:i+hop]**2)) for i in range(0,len(a)-hop,hop)]);thr=.12*np.percentile(e,90)
    sil=e<thr;cands=[];i=0
    while i<len(sil):
        if sil[i]:
            j=i
            while j<len(sil) and sil[j]:j+=1
            if (j-i)*.02>=.16 and i>5 and j<len(sil)-5:cands.append(((i+j)/2*.02,(j-i)*.02))
            i=j
        else:i+=1
    ch=np.cumsum([len(s) for s in ss]);exp=[ch[k]/ch[-1]*D for k in range(len(ss)-1)]
    n=len(exp);m_=len(cands);INF=1e9
    dp=np.full((n+1,m_+1),INF);dp[0,:]=0;bk={}
    for k in range(1,n+1):
        for j in range(1,m_+1):
            best=INF;bj=0
            for jj in range(0,j):
                c=dp[k-1,jj]
                if c<best:best=c;bj=jj
            dp[k,j]=best+abs(cands[j-1][0]-exp[k-1])-0.5*cands[j-1][1];bk[(k,j)]=bj
    j=int(np.argmin(dp[n,1:]))+1;pts=[]
    for k in range(n,0,-1):pts.append(cands[j-1][0]);j=bk[(k,j)]
    pts=pts[::-1];starts=[0.0]+pts;ends=pts+[D]
    out[b]=[dict(i=k,t0=round(starts[k],2),t1=round(ends[k],2),s=ss[k]) for k in range(len(ss))]
json.dump(out,open('sent.json','w'),ensure_ascii=False,indent=1)
for b in (2,5):
    for x in out[b]:print(b,x['t0'],x['t1'],x['s'][:70])
