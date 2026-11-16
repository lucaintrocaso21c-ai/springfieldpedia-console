# L04 spec: blocks of beats. kind: n=Nico on screen (VO), c=clip under VO, o=orig clip with original audio (no VO)
# c: (ep, t0) ; o: (ep, t0, dur, [(t_off0,t_off1,'CAPTION'),...])
B=[]
B.append(dict(id=1,title='INTRO',chip='TELESPALLA BOB · LA STORIA COMPLETA',beats=[
 ('o','S05E02',868.0,7.0,[(0.2,2.2,'AHI! AHI! AHI!'),(2.2,4.5,'AHI! AHI!')]),
 ('n',"Questo è Telespalla Bob. Ha un dottorato, una voce da teatro e un solo obiettivo nella vita: eliminare Bart Simpson."),
 ('c','S06E05',801,"In questo video ripercorriamo ogni suo piano, ogni ritorno e ogni sconfitta, con le scene originali, in ordine cronologico."),
 ('c','S19E08',592,"E alla fine ti dico se Bob è un genio sfortunato, oppure il peggior nemico di sé stesso."),
]))
B.append(dict(id=2,title='1990 · IL PRIMO COLPO',chip='CAPITOLO 1 · 1990 · S01E12',ep='S01E12 · Krusty Gets Busted',beats=[
 ('n',"Capitolo uno, millenovecentonovanta. Bob è la spalla di Krusty, e ogni giorno, in diretta, si prende torte in faccia."),
 ('c','S01E12',104,"Il pubblico lo ignora, il padrone lo umilia. Ma Bob ha un piano: si traveste da Krusty e rapina il minimarket di Apu."),
 ('c','S01E12',470,"Le telecamere riprendono tutto, e Springfield è convinta che il colpevole sia il clown. Krusty viene arrestato, processato e condannato."),
 ('c','S01E12',1073,"E Bob? Prende il suo posto in televisione, con un programma tutto suo. Un colpo perfetto, tranne per un dettaglio."),
 ('c','S01E12',1205,"Bart sente la frase, scarpe grandi da riempire, e capisce: Krusty ha i piedi piccoli, Bob li ha enormi."),
 ('o','S01E12',1237.0,12.0,[(0.3,2.5,'KRUSTY HA I PIEDI PICCOLI,'),(2.5,5.5,'COME TUTTE LE BRAVE PERSONE!'),(5.5,8.5,'BOB HA PIEDI ENORMI!'),(8.5,11.5,'ECCO PERCHÉ HO INCASTRATO KRUSTY!')]),
 ('c','S01E12',1283,"Bob finisce in prigione. È la sua prima sconfitta, ma non sarà l'ultima, e Bart è ormai il suo bersaglio preferito."),
]))
B.append(dict(id=3,title='1993 · LA VENDETTA',chip='CAPITOLO 2 · 1993 · S05E02',ep='S05E02 · Cape Feare',beats=[
 ('n',"Capitolo due, millenovecentonovantatré. Dopo qualche anno in cella, Bob vuole una cosa sola: far sapere a Bart che non lo ha dimenticato."),
 ('c','S05E02',141,"Bart comincia a ricevere lettere minatorie, e capisce subito chi le scrive."),
 ('c','S05E02',529,"Intanto Bob convince la commissione per la libertà vigilata. Quel tatuaggio sul petto, die Bart die? Per lui è tedesco: vie, Bart, vie."),
 ('c','S05E02',702,"Quando arriva a casa Simpson, Bob legge una lista dei vicini che non ucciderà. Bart, naturalmente, non c'è."),
 ('c','S05E02',728,"La famiglia entra nel programma protezione testimoni e si trasferisce lontano, con nuovi nomi."),
 ('c','S05E02',986,"Ma Bob li trova, e per Bart arriva la resa dei conti su una houseboat."),
 ('c','S05E02',1171,"Bart ottiene un ultimo desiderio: ascoltare l'intera opera H.M.S. Pinafore. E Bob, che ama il teatro più di ogni altra cosa, accetta di cantarla."),
 ('o','S05E02',1257.0,6.0,[(0.2,2.6,'FERMO LÌ, TELESPALLA BOB!'),(2.6,5.5,'SEI IN ARRESTO!')]),
 ('c','S05E02',1263,"Il tempo guadagnato basta alla polizia per arrivare. Bob perde perché ha scelto lo spettacolo al posto del colpo."),
]))
B.append(dict(id=4,title='1994 · IL SINDACO',chip='CAPITOLO 3 · 1994 · S06E05',ep='S06E05 · Sideshow Bob Roberts',beats=[
 ('n',"Capitolo tre, millenovecentonovantaquattro. Questa volta Bob lascia stare Bart e punta più in alto: il municipio di Springfield."),
 ('c','S06E05',270,"Dal carcere telefona a una radio conservatrice e si presenta come prigioniero politico."),
 ('c','S06E05',379,"La campagna funziona: Bob viene liberato e annuncia che si candida contro il sindaco Quimby."),
 ('c','S06E05',713,"Nel dibattito è brillante, e il vecchio sindaco sembra un dilettante."),
 ('c','S06E05',787,"Il risultato è schiacciante: Bob diventa sindaco di Springfield."),
 ('c','S06E05',911,"Ma Lisa nota un dettaglio: troppi voti, e alcuni arrivano da persone defunte. Perfino il cimitero degli animali ha votato per Bob."),
 ('o','S06E05',1054.0,9.0,[(0.3,2.5,'OH, MIO DIO!'),(2.5,5.0,'I MORTI SONO RISORTI!'),(5.0,8.5,'I MORTI NON POSSONO VOTARE!')]),
 ('c','S06E05',1142,"Bart e Lisa gli tendono una trappola: dicono che sia solo un burattino. E Bob, offeso, confessa da solo la sua opera d'arte."),
 ('o','S06E05',1209.5,12.0,[(0.3,3.0,'SOLO IO POTEVO ESEGUIRE'),(3.0,6.0,'UN CAPOLAVORO DI FRODE ELETTORALE'),(6.0,9.0,'E HO LE PROVE!')]),
 ('c','S06E05',1270,"Arrestato di nuovo, giura vendetta. La vanità lo ha tradito."),
]))
B.append(dict(id=5,title='1997 · IL FRATELLO',chip='CAPITOLO 4 · 1997 · S08E16',ep='S08E16 · Brother From Another Series',beats=[
 ('n',"Capitolo quattro, millenovecentonovantasette. Bob arriva con un nuovo alleato: suo fratello Cecil."),
 ('c','S08E16',227,"In prigione Bob sembra un detenuto modello, e Cecil va a trovarlo. Nessuno immagina cosa stia davvero succedendo."),
 ('c','S08E16',776,"Bart e Lisa sospettano un nuovo piano, e in un cantiere trovano progetti, fatture e milioni di dollari."),
 ('c','S08E16',880,"Il calcestruzzo mancante svela la truffa: la diga è vuota. Bob dice che il responsabile è Cecil, ma nessuno gli crede."),
 ('o','S08E16',957.0,13.0,[(0.3,4.0,'È UNA CAUSA PERSA, TOTALMENTE PERSA.'),(4.0,8.0,'QUANDO È UN MIO PIANO NON LO FERMATE IN FRETTA,'),(8.0,12.5,'MA QUANDO È CECIL...')]),
 ('c','S08E16',1026,"Per la prima volta Bob sta dalla parte di Bart, e insieme vanno a fermare Cecil sulla diga."),
 ('c','S08E16',1122,"Cecil finisce arrestato, ma c'è un colpo di scena: il capo Wiggum rimanda in cella Bob. Senza nemmeno un piano, perde comunque."),
 ('o','S08E16',1198.0,28.0,[(0.3,3.5,'ECCO IL TUO UOMO, CAPO!'),(3.5,7.0,'CECIL? NON CREDO.'),(7.0,12.0,'SEMBRA OPERA DEL VECCHIO PAZZO TELESPALLA BOB.'),(12.0,17.0,'CECIL HA APPENA CONFESSATO, CAPO.'),(17.0,22.0,'BOB TORNA IN PRIGIONE.')]),
]))
B.append(dict(id=6,title='2007 · IL FUNERALE',chip='CAPITOLO 5 · 2007 · S19E08',ep='S19E08 · Funeral for a Fiend',beats=[
 ('n',"Capitolo cinque, duemilasette. Bob è in forma, e vuole un'uscita di scena degna del teatro."),
 ('c','S19E08',395,"Attira i Simpson in un ristorante finto con uno spot televisivo, e annuncia di averli in trappola."),
 ('c','S19E08',466,"Prima però vuole raccontare il suo piano con le diapositive: Slideshow Bob."),
 ('o','S19E08',551.0,20.0,[(0.3,3.5,'HAI FATTO UN ERRORE.'),(3.5,7.5,'SHAKESPEARE DISSE DAVVERO:'),(7.5,12.0,'LO FACCIAMO PRESTO.'),(12.0,17.0,'MACBETH, ATTO PRIMO, SCENA SETTIMA.')]),
 ('c','S19E08',581,"Mentre cerca la citazione online, il portatile esplode e Bob finisce in custodia."),
 ('c','S19E08',724,"Al processo crolla a terra: sembra morto, e tutta Springfield accusa Bart."),
 ('c','S19E08',792,"Al funerale c'è tutta la famiglia di Bob, e anche suo fratello Cecil, uscito di prigione per l'occasione."),
 ('c','S19E08',1037,"Bart va a chiedergli scusa, e Bob scatta fuori dalla bara."),
 ('c','S19E08',1072,"Ma i Simpson hanno capito tutto: il padre di Bob gli ha iniettato un farmaco che simula la morte."),
 ('o','S19E08',1184.0,15.0,[(0.3,4.0,'COME HAI ALLENTATO LE PIASTRELLE DEL MIO MOSAICO DI MORTE?'),(4.0,9.5,'HO SOSPETTATO QUANDO HO VISTO CHE LA BARA AVEVA SPAZIO EXTRA PER I TUOI PIEDI.')]),
 ('c','S19E08',1210,"A tradirlo, ancora una volta, sono i suoi piedi."),
]))
B.append(dict(id=7,title='2010 · IL VICINO',chip='CAPITOLO 6 · 2010 · S21E22',ep='S21E22 · The Bob Next Door',beats=[
 ('n',"Capitolo sei, duemiladieci. Questa volta Bob non si nasconde: si trasferisce nella casa accanto."),
 ('c','S21E22',128,"Un'amnistia svuota le prigioni, e Bob esce con la faccia di un altro: quella di Walt Warren."),
 ('o','S21E22',313.0,17.0,[(0.3,2.5,'CIAO, BART.'),(2.5,5.0,'CIAO, BART.'),(5.0,8.0,'SIDESHOW BOB!'),(8.0,12.0,'MA CHI? COSA?')]),
 ('c','S21E22',350,"Bart lo riconosce subito dalla voce, ma nessuno gli crede."),
 ('c','S21E22',409,"Per dimostrarlo prova a farlo cantare: Bob non resiste a un'operetta di Gilbert e Sullivan."),
 ('c','S21E22',840,"Poi Bob ammette tutto: ha preso la faccia del vero Walt, e ora deve uccidere Bart per vendere la casa."),
 ('c','S21E22',1055,"Lo porta in un altro stato per aggirare la legge. Ma Bart non si era mai fidato."),
 ('c','S21E22',1138,"Aveva avvisato Wiggum, che li rintraccia grazie al sistema di localizzazione dell'auto."),
 ('o','S21E22',1160.0,26.0,[(0.3,3.0,'MI SPIACE, NON HAI GIURISDIZIONE QUI.'),(3.0,7.0,'BENVENUTO NELLA MIA GIURISDIZIONE!'),(7.0,13.0,'AVETE IL DIRITTO DI RIMANERE IN SILENZIO...'),(13.0,19.0,'ORA VI PORTIAMO DENTRO!')]),
 ('c','S21E22',1193,"Bob finisce ancora in manette, e a Springfield resta il ricordo del peggior vicino di sempre."),
]))
B.append(dict(id=8,title='VERDETTO',chip='IL VERDETTO',beats=[
 ('n',"Eccoci al verdetto. Sei capitoli, sei sconfitte. E la cosa curiosa è che quasi mai Bob viene battuto da un piano migliore: viene battuto dalla sua vanità."),
 ('c','S01E12',1270,"Si vanta del furto. Ricorda male una citazione. Canta un'operetta invece di colpire. Confessa la sua opera d'arte."),
 ('n',"Il mio verdetto: Telespalla Bob non è un fallito, è un genio che non sa tacere. Se ti è piaciuto, iscriviti al canale. E scrivimi nei commenti: qual è, secondo te, il suo piano più elegante?"),
]))
