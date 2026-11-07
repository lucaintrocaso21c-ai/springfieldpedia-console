#!/usr/bin/env python3
"""Console Telegram di Springfieldpedia. Gira a ogni esecuzione del workflow:
legge i nuovi messaggi, risponde, e a richiesta manda gli avvisi."""
import json,os,sys,datetime as dt,urllib.request,urllib.parse
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'data')
FASI=['script','voce','montaggio','miniatura','upload']
TOPICS=['comandi','idee','gestione','avvisi','diagnostica']
def load(n,default):
    try:return json.load(open(os.path.join(D,n),encoding='utf-8'))
    except Exception:return default
def save(n,v):json.dump(v,open(os.path.join(D,n),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
def oggi():return dt.datetime.now(dt.timezone(dt.timedelta(hours=1))).date()
class TG:
    def __init__(s,token,chat):s.t=(token or '').strip();s.chat=(chat or '').strip()
    def call(s,m,**p):
        req=urllib.request.Request('https://api.telegram.org/bot%s/%s'%(s.t,m),urllib.parse.urlencode({k:v for k,v in p.items() if v is not None}).encode())
        return json.load(urllib.request.urlopen(req,timeout=60))
    def send(s,text,thread=None,chat=None,markup=None):
        ps=[text[i:i+3900] for i in range(0,len(text),3900)] or ['(vuoto)']
        for j,p in enumerate(ps):
            s.call('sendMessage',chat_id=chat or s.chat,text=p,message_thread_id=thread,disable_web_page_preview='true',reply_markup=json.dumps(markup) if (markup and j==len(ps)-1) else None)
    def updates(s,offset,wait=0):return s.call('getUpdates',offset=offset,timeout=wait,allowed_updates=json.dumps(['message','callback_query']))['result']
def videos():
    cal=load('calendario.json',[]);prog=load('progress.json',{});out=[]
    for r in cal:
        if r['tipo']=='Video':
            p=prog.get(r['video'],{});r=dict(r);r['fasi']=[f for f in FASI if p.get(f)];r['manca']=[f for f in FASI if not p.get(f)];out.append(r)
    return out
def fmtv(v):
    done=''.join('x' if f in v['fasi'] else '-' for f in FASI)
    return '%s  %s %s  [%s]\n   %s'%(v['video'],v['data'][5:],v['ora'],done,v['titolo'])
def cmd_aiuto():
    return ("COMANDI\n/stato - situazione dei video\n/prossimo - prossime uscite\n/settimana - uscite dei prossimi 7 giorni\n"
    "/video V3 - dettaglio di un video\n/fatto V3 voce - segna una fase fatta (script, voce, montaggio, miniatura, upload)\n"
    "/annulla V3 voce - toglie la fase\n/idea testo - salva un'idea\n/idee - ultime 10 idee\n/costo 1.5 nota - registra una spesa\n/costi - totale spese\n"
    "/diagnostica - stato della console\n/id - mostra ID utente e ID chat (serve solo all'installazione)\n/avvisi - manda ora il riepilogo avvisi\n/qui nome - registra questo argomento (%s)\n\nLe fasi nello stato: %s"%(', '.join(TOPICS),' '.join(FASI)))
def cmd_stato():
    vs=videos();t=oggi();ok=sum(1 for v in vs if not v['manca']);rit=[v for v in vs if v['data']<t.isoformat() and v['manca']]
    nxt=[v for v in vs if v['data']>=t.isoformat()][:3]
    s='VIDEO: %d in calendario, %d completi, %d in ritardo\n'%(len(vs),ok,len(rit))
    if rit:s+='\nIN RITARDO\n'+'\n'.join(fmtv(v) for v in rit)+'\n'
    s+='\nPROSSIMI\n'+'\n'.join(fmtv(v) for v in nxt) if nxt else '\nNessun video futuro.'
    return s+'\n\nLegenda fasi: script voce montaggio miniatura upload (x = fatta)'
def cmd_prossimo():
    cal=load('calendario.json',[]);t=oggi().isoformat();nx=[r for r in cal if r['data']>=t][:6]
    return 'PROSSIME USCITE\n'+'\n'.join('%s %s  %s %s - %s'%(r['data'][5:],r['ora'],r['tipo'],r['video'],r['titolo'][:70]) for r in nx) if nx else 'Calendario finito.'
def cmd_settimana():
    cal=load('calendario.json',[]);a=oggi();b=a+dt.timedelta(days=7)
    nx=[r for r in cal if a.isoformat()<=r['data']<=b.isoformat()]
    return 'PROSSIMI 7 GIORNI\n'+'\n'.join('%s %s  %s %s - %s'%(r['data'][5:],r['ora'],r['tipo'],r['video'],r['titolo'][:70]) for r in nx) if nx else 'Niente in calendario nei prossimi 7 giorni.'
def cmd_video(a):
    if not a:return 'Uso: /video V3'
    k=a[0].upper();vs=[v for v in videos() if v['video']==k]
    if not vs:return 'Video %s non trovato.'%k
    v=vs[0];sh=[r for r in load('calendario.json',[]) if r['tipo']=='Short' and r['video']==k]
    s='%s - %s\nFormato: %s | uscita %s %s\nEpisodi: %s\nFasi fatte: %s\nMancano: %s\n\nShort derivati: %d\n'%(k,v['titolo'],v['formato'],v['data'],v['ora'],v['episodi'],', '.join(v['fasi']) or 'nessuna',', '.join(v['manca']) or 'niente',len(sh))
    return s+'\n'.join('  %s %s'%(r['data'][5:],r['titolo'][:60]) for r in sh)
def setfase(a,val):
    if len(a)<2:return 'Uso: /fatto V3 voce'
    k,f=a[0].upper(),a[1].lower()
    if f not in FASI:return 'Fase non valida. Scegli tra: '+', '.join(FASI)
    if not any(v['video']==k for v in videos()):return 'Video %s non trovato.'%k
    p=load('progress.json',{});p.setdefault(k,{})[f]=dt.datetime.now().isoformat(timespec='minutes') if val else None;save('progress.json',p)
    v=[v for v in videos() if v['video']==k][0]
    return '%s: fase "%s" %s.\nMancano: %s'%(k,f,'segnata fatta' if val else 'tolta',', '.join(v['manca']) or 'niente - video completo')
def cmd_idea(t):
    if not t.strip():return 'Uso: /idea testo dell\'idea'
    i=load('ideas.json',[]);i.append({'quando':dt.datetime.now().isoformat(timespec='minutes'),'testo':t.strip()});save('ideas.json',i);return 'Idea salvata (%d in tutto).'%len(i)
def cmd_idee():
    i=load('ideas.json',[])[-10:]
    return 'ULTIME IDEE\n'+'\n'.join('%s  %s'%(x['quando'][5:10],x['testo']) for x in i) if i else 'Nessuna idea salvata. Usa /idea testo.'
def cmd_costo(a):
    try:eu=float(a[0].replace(',','.'))
    except Exception:return 'Uso: /costo 1.5 nota (importo in euro)'
    c=load('costi.json',[]);c.append({'quando':dt.datetime.now().isoformat(timespec='minutes'),'euro':eu,'nota':' '.join(a[1:])});save('costi.json',c)
    return 'Registrati %.2f EUR. Totale: %.2f EUR.'%(eu,sum(x['euro'] for x in c))
def cmd_costi():
    c=load('costi.json',[])
    if not c:return 'Nessuna spesa registrata. Usa /costo 1.5 nota.'
    m={};[m.__setitem__(x['quando'][:7],m.get(x['quando'][:7],0)+x['euro']) for x in c]
    return 'SPESE\nTotale: %.2f EUR\n'%sum(x['euro'] for x in c)+'\n'.join('%s: %.2f EUR'%(k,v) for k,v in sorted(m.items()))+'\n\nUltime:\n'+'\n'.join('%s %.2f %s'%(x['quando'][5:10],x['euro'],x['nota']) for x in c[-5:])
def cmd_diag():
    st=load('state.json',{});cal=load('calendario.json',[])
    chk=[('calendario',len(cal)>0),('progress.json',os.path.exists(os.path.join(D,'progress.json'))),('argomenti registrati',all(t in st.get('topics',{}) for t in TOPICS))]
    s='DIAGNOSTICA\nUltima esecuzione: %s\nEsecuzioni totali: %d | messaggi gestiti: %d\nUltimo avviso: %s\n\n'%(st.get('last_run'),st.get('runs',0),st.get('processed',0),st.get('last_alert'))
    s+='\n'.join('%s %s'%('OK ' if ok else 'DA FARE',n) for n,ok in chk)
    mis=[t for t in TOPICS if t not in st.get('topics',{})]
    if mis:s+='\n\nArgomenti non registrati: %s\nScrivi /qui nome dentro ciascun argomento.'%', '.join(mis)
    return s
def cmd_oggi():
    t=oggi();cal=load('calendario.json',[]);pr=load('progress.json',{});fatto=pr.get('_fatto',{})
    ogg=[r for r in cal if r['data']==t.isoformat()]
    s='OGGI %s\n'%t.strftime('%d/%m')
    if ogg:s+='\n'.join('%s  %s - %s'%(r['ora'],'VIDEO' if r['tipo']=='Video' else 'Short',r['titolo'][:70]) for r in ogg)
    else:s+='Niente in uscita oggi.'
    dom=[r for r in cal if r['data']>t.isoformat()][:1]
    if dom:s+='\n\nPROSSIMO: %s %s - %s'%(dom[0]['data'][5:],dom[0]['ora'],dom[0]['titolo'][:60])
    if fatto.get(t.isoformat()):s+='\n\n✅ Segnato come fatto'
    return s
def avvisi():
    t=oggi();out=cmd_oggi()
    if t.weekday()==6:out+='\n\n'+cmd_settimana()
    return out
def kb_oggi():
    return {'inline_keyboard':[[{'text':'✅ Fatto','callback_data':'d:%s'%oggi().isoformat()},{'text':'🗓 Settimana','callback_data':'c:settimana'},{'text':'💡 Idee','callback_data':'c:idee'}]]}
COMANDI_MENU=[('oggi','Cosa esce oggi e cosa devi fare'),('settimana','Prossimi 7 giorni'),('idee','Le tue idee')]
def kb_menu():
    B=lambda t,d:{'text':t,'callback_data':d}
    return {'inline_keyboard':[[B('📌 Oggi','c:oggi'),B('🗓 Settimana','c:settimana'),B('💡 Idee','c:idee')]]}
def kb_videos():
    vs=[v for v in videos() if v['data']>=oggi().isoformat() or v['manca']][:8]
    rows=[[{'text':'%s %s - %s'%(v['video'],v['data'][5:],v['titolo'][:28]),'callback_data':'v:'+v['video']}] for v in vs]
    return {'inline_keyboard':rows+[[{'text':'⬅ Menu','callback_data':'c:menu'}]]}
def kb_video(k):
    v=[x for x in videos() if x['video']==k]
    if not v:return kb_menu()
    v=v[0];row=[{'text':('✅ ' if f in v['fasi'] else '⬜ ')+f,'callback_data':'f:%s:%s'%(k,f)} for f in FASI]
    return {'inline_keyboard':[row[:3],row[3:],[{'text':'⬅ Video','callback_data':'c:video'},{'text':'Menu','callback_data':'c:menu'}]]}
KB_REPLY={'keyboard':[[{'text':'📌 Oggi'},{'text':'🗓 Settimana'},{'text':'💡 Idee'}]],'resize_keyboard':True,'is_persistent':True}
LABELS={'oggi':'/oggi','stato':'/stato','prossimo':'/prossimo','settimana':'/settimana','video':'/video','idee':'/idee','costi':'/costi','diagnostica':'/diagnostica','avvisi':'/avvisi','aiuto':'/aiuto','menu':'/menu'}
def tastiera(tg,th):
    try:tg.send('Tastiera attiva: usa i pulsanti qui sotto.',thread=th,markup=KB_REPLY)
    except Exception as e:print('tastiera:',e)
def setup_menu(tg,st):
    if st.get('menu_v')==3:return
    cmds=json.dumps([{'command':c,'description':d} for c,d in COMANDI_MENU])
    try:
        for sc in ('default','all_private_chats','all_group_chats','all_chat_administrators'):
            tg.call('setMyCommands',commands=cmds,scope=json.dumps({'type':sc}))
        tg.call('setChatMenuButton',menu_button=json.dumps({'type':'commands'}))
        st['menu_v']=3
    except Exception as e:print('setup_menu:',e)
def dispatch_cb(data):
    p=data.split(':')
    if p[0]=='c':
        k=p[1]
        if k=='menu':return 'MENU - scegli:',kb_menu()
        if k=='oggi':return cmd_oggi(),kb_oggi()
        if k=='video':return 'Quale video?',kb_videos()
        return {'stato':cmd_stato,'prossimo':cmd_prossimo,'settimana':cmd_settimana,'idee':cmd_idee,'costi':cmd_costi,'diag':cmd_diag,'avvisi':avvisi,'aiuto':cmd_aiuto}[k](),kb_menu()
    if p[0]=='d':
        pr=load('progress.json',{});pr.setdefault('_fatto',{})[p[1]]=True;save('progress.json',pr);return 'Fatto, segnato per oggi.',kb_menu()
    if p[0]=='v':return cmd_video([p[1]]),kb_video(p[1])
    if p[0]=='f':
        k,f=p[1],p[2];v=[x for x in videos() if x['video']==k]
        fatto=bool(v) and f in v[0]['fasi'];r=setfase([k,f],not fatto)
        return r,kb_video(k)
    return 'Pulsante non riconosciuto.',kb_menu()
def handle_cb(tg,cb,allowed):
    u=cb.get('from',{}).get('id');m=cb.get('message') or {}
    if str(u)!=str(allowed):
        try:tg.call('answerCallbackQuery',callback_query_id=cb['id'],text='Non autorizzato')
        except Exception:pass
        return
    try:tg.call('answerCallbackQuery',callback_query_id=cb['id'])
    except Exception:pass
    try:text,kb=dispatch_cb(cb.get('data') or '')
    except Exception as e:text,kb='Errore: %s'%e,kb_menu()
    tg.send(text,thread=m.get('message_thread_id'),chat=m.get('chat',{}).get('id'),markup=kb)
def handle(tg,msg,allowed,st):
    u=msg.get('from',{}).get('id');text=(msg.get('text') or '').strip()
    if text.split(' ')[0].split('@')[0].lower()=='/id':
        tg.send('Il tuo ID utente: %s\nID di questa chat: %s'%(u,msg.get('chat',{}).get('id')),thread=msg.get('message_thread_id'),chat=msg.get('chat',{}).get('id'));return
    th0=msg.get('message_thread_id');ftc=(msg.get('reply_to_message') or {}).get('forum_topic_created')
    if th0 and ftc:
        nm=(ftc.get('name') or '').lower()
        for tn in TOPICS:
            if tn in nm and st['topics'].get(tn)!=th0:st['topics'][tn]=th0
    parts=text.split(' ',1)
    if len(parts)==2 and parts[1].strip().lower() in LABELS and not text.startswith('/'):text=LABELS[parts[1].strip().lower()]
    if str(u)!=str(allowed) or not text.startswith('/'):return
    th=msg.get('message_thread_id');cmd,_,rest=text.partition(' ');cmd=cmd.split('@')[0].lower();a=rest.split()
    R={'/oggi':cmd_oggi,'/aiuto':cmd_aiuto,'/stato':cmd_stato,'/prossimo':cmd_prossimo,'/settimana':cmd_settimana,'/idee':cmd_idee,'/costi':cmd_costi,'/diagnostica':cmd_diag,'/avvisi':avvisi}
    if cmd=='/qui':
        n=(a[0].lower() if a else '')
        if n not in TOPICS:reply='Uso: /qui nome, dove nome e uno tra: '+', '.join(TOPICS)
        else:st['topics'][n]=th;tg.send('Argomento "%s" registrato.'%n,thread=th);tg.send('MENU - scegli:',thread=th,markup=kb_menu());tastiera(tg,th);return
    elif cmd in('/menu','/start'):tg.send('MENU - scegli:',thread=th,markup=kb_menu());tastiera(tg,th);return
    elif cmd=='/video' and not a:tg.send('Quale video?',thread=th,markup=kb_videos());return
    elif cmd=='/video':tg.send(cmd_video(a),thread=th,markup=kb_video(a[0].upper()));return
    elif cmd=='/fatto':reply=setfase(a,True)
    elif cmd=='/annulla':reply=setfase(a,False)
    elif cmd=='/idea':reply=cmd_idea(rest)
    elif cmd=='/costo':reply=cmd_costo(a)
    elif cmd in R:reply=R[cmd]()
    else:reply='Comando sconosciuto. Scrivi /aiuto.'
    tg.send(reply,thread=th)
INTRO=("CONSOLE SPRINGFIELDPEDIA\n\nOgni mattina alle 8 ricevi un solo messaggio: cosa esce oggi e cosa devi fare. Il resto e nei 3 pulsanti: Oggi, Settimana, Idee. /idea testo salva un'idea.")
def run(tg,allowed,mode='poll'):
    st=load('state.json',{});st.setdefault('topics',{});n=0
    if mode=='poll':
        setup_menu(tg,st)
        if st.get('intro_v')!=3:
            try:tg.send(INTRO,markup=kb_menu());tastiera(tg,None);st['intro_v']=3
            except Exception as e:print('intro:',e)
        import time
        fine=time.time()+int(os.environ.get('LOOP_SECONDS') or 0)
        while True:
            try:ups=tg.updates(st.get('offset',0),25 if os.environ.get('LOOP_SECONDS') else 0)
            except Exception as e:
                print('getUpdates:',e);ups=[]
                if os.environ.get('LOOP_SECONDS'):time.sleep(3)
            for up in ups:
                st['offset']=up['update_id']+1
                try:
                    if 'message' in up:handle(tg,up['message'],allowed,st);n+=1
                    if 'callback_query' in up:handle_cb(tg,up['callback_query'],allowed);n+=1
                except Exception as e:print('errore update:',e)
                save('state.json',st)
            if time.time()>=fine:break
    if mode=='avvisi':
        a=avvisi();tg.send(a,thread=st['topics'].get('avvisi'),markup=kb_oggi());st['last_alert']=dt.datetime.now().isoformat(timespec='minutes')
    st['last_run']=dt.datetime.now().isoformat(timespec='minutes');st['runs']=st.get('runs',0)+1;st['processed']=st.get('processed',0)+n;save('state.json',st);return n
if __name__=='__main__':
    tok=os.environ.get('TELEGRAM_BOT_TOKEN');chat=os.environ.get('TELEGRAM_CHAT_ID');al=(os.environ.get('ALLOWED_USER_ID') or '').strip()
    if not (tok and chat and al):print('Mancano i segreti TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ALLOWED_USER_ID');sys.exit(1)
    print('messaggi gestiti:',run(TG(tok,chat),al,sys.argv[1] if len(sys.argv)>1 else 'poll'))
