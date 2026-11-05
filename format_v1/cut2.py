import subprocess,glob,concurrent.futures as cf
R='/mnt/user-data/uploads/Simpson/'
def ts(x):
    h=int(x//3600);m=int(x%3600//60);s=x%60;return '%d:%02d:%05.2f'%(h,m,s)
M=[ # name, ep, s0, d, caps
('m2','S02E15',995.0,8.3,[(995.1,996.6,"Lavoro bene con gli altri?"),(996.6,997.8,"No, no, no."),(997.8,1000.0,"Homer, ti ho dato questo lavoro perché sei un tipo qualunque!"),(1000.0,1001.2,"Ah, fantastico."),(1001.2,1003.2,"Ti serve solo un po' di fiducia in te stesso.")]),
('m3','S04E03',218.4,9.5,[(220.4,224.4,"* Chi indossa i pantaloncini corti?"),(224.4,227.5,"* IO INDOSSO I PANTALONCINI CORTI.")]),
('m4','S02E11',438.4,10.8,[(438.6,441.5,"e da quanto mi ha detto il cuoco, è molto probabile..."),(441.5,444.9,"Le restano 24 ore di vita."),(444.9,446.1,"24 ore!"),(446.2,449.1,"Anzi, 22. Mi scusi se l'ho fatta aspettare così tanto.")]),
('m5','S04E09',592.0,9.0,[(592.0,593.0,"ZITTO, RAGAZZO."),(594.0,595.1,"QUINDI RICORDATE..."),(595.2,596.7,"* CHIAMA MR. PLOW"),(596.7,598.0,"* È IL MIO NOME"),(598.0,600.8,"* RIPETO: MR. PLOW.")]),
('m6','S07E07',187.6,8.4,[(188.3,191.3,"SE PRENDO 61 LIBBRE, MI FANNO LAVORARE DA CASA?"),(191.3,193.0,"QUESTO È L'ACCORDO."),(193.0,194.4,"NIENTE PIÙ PROGRAMMA DI ESERCIZI."),(194.5,195.7,"NIENTE PIÙ TRAFFICO.")]),
('m7','S06E12',446.6,12.0,[(446.9,448.6,"CI CHIAMIAMO PER NUMERO, NON PER NOME."),(448.6,450.5,"CARL È IL 14. IO SONO IL 12."),(450.5,452.0,"BURNSIE È IL 29."),(452.0,453.6,"TU SEI SUPERIORE AL SIGNOR BURNS?"),(453.6,455.4,"CERTO, GUARDA."),(455.4,458.1,"EHI, 29, VIENI QUI.")]),
('m8','S06E09',596.0,8.4,[(596.1,597.6,"Lo faccio!"),(597.6,599.7,"Qualcuno doveva riportare a casa la babysitter."),(599.7,602.5,"Poi ho notato che era seduta sulla Venere di Gummi"),(602.5,604.2,"così gliel'ho strappata di dosso."),(604.2,606.5,"Oh, solo a pensare a quella dolce caramella...")]),
('m9','S03E17',735.0,11.5,[(735.1,736.5,"Prendo José Canseco."),(736.5,737.9,"D'oh!"),(737.9,740.9,"Mattingly, tagliati quelle basette."),(740.9,741.9,"Quali basette?"),(741.9,743.3,"Hai capito, hippie."),(743.3,745.3,"Questi non sono così forti."),(745.3,746.5,"Io ho Wonderbat.")]),
('m10','S05E15',262.6,10.4,[(262.7,265.8,"LI ODIANO. E ALLORA, CHI AMANO?"),(265.8,269.5,"ECCO LE PERSONALITÀ PIÙ POPOLARI IN TV:"),(269.5,272.9,"CE L'HO FATTA! HO POTENZIATO IL MIO TAGLIAERBA!")]),
('m11','S01E01',1251.5,9.0,[(1252.0,1253.5,"AW, POSSIAMO TENERLO, PAPÀ?"),(1253.5,1254.5,"PER FAVORE?"),(1254.5,1256.5,"MA È UN PERDENTE."),(1256.5,1258.0,"È PATETICO."),(1258.0,1259.9,"È..."),(1259.9,1262.0,"UN SIMPSON.")]),
('c6','S07E07',304.3,11.4,[(304.7,307.3,"È UN SOGNO CHE SI AVVERA, RAGAZZI."),(307.3,309.4,"POSSO, ANZI, DEVO"),(309.4,311.2,"MANGIARE TUTTO QUELLO CHE HO SEMPRE VOLUTO."),(311.2,312.7,"ORA SU!"),(312.7,315.3,"OGNI SECONDO FUORI DAL LETTO BRUCIO CALORIE PREZIOSE.")]),
]
FD='/tmp/claude-0/-home-claude/87164e15-4779-5c7a-be25-1e13b780e99b/scratchpad'
def one(x):
    n,ep,s0,d,caps=x
    f=glob.glob(R+'*/Season */*%s - *.mkv'%ep)[0]
    ass='[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\n[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,Bold,Italic,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV\nStyle: D,Baloo 2 ExtraBold,64,&H00FFFFFF,&H00000000,&H80000000,0,0,1,5,2,2,120,120,70\n[Events]\nFormat: Layer,Start,End,Style,Text\n'
    for a,b,t in caps:ass+='Dialogue: 0,%s,%s,D,%s\n'%(ts(a-s0),ts(b-s0),t)
    open('clips/%s.ass'%n,'w').write(ass)
    cmd=['ffmpeg','-v','error','-y','-ss',str(s0),'-i',f,'-t',str(d),'-vf','scale=1920:1080,ass=clips/%s.ass:fontsdir=%s'%(n,FD),'-af','aresample=48000','-ac','2','-c:v','libx264','-crf','21','-preset','veryfast','-r','30','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','clips/%s.mp4'%n]
    r=subprocess.run(cmd,capture_output=True,text=True);print(n,r.returncode,r.stderr[:200],flush=True)
if __name__=='__main__':
    with cf.ThreadPoolExecutor(2) as ex:list(ex.map(one,M))
