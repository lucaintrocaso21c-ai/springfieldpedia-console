import subprocess,glob,os
R='/mnt/user-data/uploads/Simpson/'
C=[ # n, ep, s0, d, caps
(10,'S02E15',1101.2,10.5,[(1101.2,1102.5,"Niente male, eh?"),(1102.5,1105.4,"Voglio un clacson qui, qui e qui."),(1105.4,1109.0,"Non trovi mai il clacson quando sei arrabbiato"),(1109.0,1110.7,"e devono suonare tutti «La Cucaracha»."),(1110.7,1111.7,"Come desidera, signor S.")]),
(9,'S04E03',568.5,9.6,[(569.4,570.8,"DIO?"),(570.8,574.2,"HAI ABBANDONATO LA MIA CHIESA!"),(574.3,576.4,"Beh, più o meno... ma..."),(576.5,577.8,"MA COSA?")]),
(8,'S02E11',375.0,10.0,[(375.3,376.9,"Concentrati."),(376.9,378.9,"Voglio il fugu!"),(381.5,384.6,"Mmm. Fan-fugu-tastico.")]),
(7,'S04E09',467.0,12.5,[(467.0,469.2,"CARO SIGNORE, NELLA TUA INFINITA SAGGEZZA"),(469.2,471.5,"SAI QUAL È IL NUMERO DA CHIAMARE PER UNO SPAZZANEVE"),(471.5,474.5,"È KLONDIKE 5-3226."),(474.5,476.3,"HOMER, QUESTO È DAVVERO BASSO."),(476.3,479.3,"NON QUANTO I MIEI BASSI, BASSI PREZZI.")]),
(6,'S07E07',187.6,8.4,[(188.3,191.3,"SE PRENDO 61 LIBBRE, MI FANNO LAVORARE DA CASA?"),(191.3,193.0,"QUESTO È L'ACCORDO."),(193.0,194.4,"NIENTE PIÙ PROGRAMMA DI ESERCIZI."),(194.5,195.7,"NIENTE PIÙ TRAFFICO.")]),
(5,'S06E12',554.7,13.0,[(554.7,556.6,"PENSO CHE DOVREBBE FARE UN GIURAMENTO DIVERSO."),(556.6,558.8,"TUTTI FANNO LO STESSO GIURAMENTO."),(558.8,560.8,"BENVENUTO NEL CLUB, NUMERO 908."),(560.8,564.1,"SEI ENTRATO NEL SACRO ORDINE DEI TAGLIAPIETRE"),(564.1,567.6,"CHE DAI TEMPI ANTICHI SPEZZANO LE ROCCE DELL'IGNORANZA")]),
(4,'S06E09',263.7,12.8,[(263.7,265.3,"Cos'è?"),(265.3,267.7,"È la Gummi più rara di tutte."),(267.7,269.3,"La Venere di Milo di Gummi."),(269.3,271.1,"Scolpita da artigiani Gummi"),(271.1,274.4,"che lavorano solo nel mezzo del Gummi."),(274.4,276.3,"Volete smettere di dire Gummi?")]),
(3,'S03E17',514.7,11.5,[(514.7,516.0,"Il nostro nuovo, ehm..."),(516.0,518.6,"inventeremo dei ruoli per questi ragazzi più tardi."),(518.6,521.7,"Salutate Steve Sax, Don Mattingly, Darryl Strawberry,"),(521.7,524.1,"Ozzie Smith, Mike Scioscia e José Canseco."),(524.1,526.0,"Ooh. Accidenti. Wow.")]),
(2,'S05E15',402.5,11.0,[(402.5,405.1,"SIGNORE E SIGNORI, MEMBRI DELLA STAMPA,"),(405.2,409.0,"VORREI PRESENTARE LA NUOVA GENERAZIONE DI ASTRONAUTI NASA:"),(409.1,410.9,"L'AMERICANO MEDIO.")]),
(1,'S01E01',730.1,12.0,[(730.1,732.3,"E TU COSA VUOI, BAMBINO?"),(732.4,734.2,"NON SEI BABBO NATALE, CICCIONE."),(734.2,735.8,"COME TI PERMETTI... EHI, NO, HOMER!"),(735.8,737.5,"SE SI PRESENTA UN'EMERGENZA"),(737.5,740.2,"DI' PURE CHE BABBO NATALE È MOLTO OCCUPATO IN QUEST'ERA"),(740.2,742.1,"E TU SEI UNO DEI SUOI AIUTANTI.")]),
]
def ts(x):
    h=int(x//3600);m=int(x%3600//60);s=x%60;return '%d:%02d:%05.2f'%(h,m,s)
procs=[]
for n,ep,s0,d,caps in C:
    f=[p for p in glob.glob(R+'*/Season */*%s - *.mkv'%ep)][0]
    ass='[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Italic,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV\nStyle: D,Baloo 2 ExtraBold,64,&H00FFFFFF,&H00000000,&H80000000,0,0,1,5,2,2,120,120,70\n[Events]\nFormat: Layer,Start,End,Style,Text\n'
    for a,b,t in caps:ass+='Dialogue: 0,%s,%s,D,%s\n'%(ts(a-s0),ts(b-s0),t)
    open('clips/c%d.ass'%n,'w').write(ass)
    cmd=['ffmpeg','-v','error','-y','-ss',str(s0),'-i',f,'-t',str(d),'-vf',"scale=1920:1080,ass=clips/c%d.ass:fontsdir=/tmp/claude-0/-home-claude/87164e15-4779-5c7a-be25-1e13b780e99b/scratchpad"%n,'-af','aresample=48000,pan=stereo|c0=FL+0.7*FC|c1=FR+0.7*FC' if False else 'aresample=48000','-ac','2','-c:v','libx264','-crf','21','-preset','veryfast','-r','30','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','clips/c%d.mp4'%n]
    procs.append(cmd)
import concurrent.futures as cf
with cf.ThreadPoolExecutor(2) as ex:
    for r in ex.map(lambda c:subprocess.run(c,capture_output=True,text=True),procs):print(r.returncode,r.stderr[:300])
