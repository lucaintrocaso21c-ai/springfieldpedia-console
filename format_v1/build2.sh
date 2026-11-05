cd /tmp/claude-0/-home-claude/87164e15-4779-5c7a-be25-1e13b780e99b/scratchpad/v1
python3 cut2.py > cut2.log 2>&1
python3 broll.py 1 2 3 4 5 6 7 8 9 10 11 > broll2.log 2>&1
python3 -c "
import broll
for b in range(2,12):broll.split(b)
"
ORD="nbx01 sigla nbx02a m2 nbx02b c10 nbx03a m3 nbx03b c9 nbx04a m4 nbx04b c8 nbx05a m5 nbx05b c7 nbx06a m6 nbx06b c6 nbx07a m7 nbx07b c5 nbx08a m8 nbx08b c4 nbx09a m9 nbx09b c3 nbx10a m10 nbx10b c2 nbx11a m11 nbx11b c1 nb12"
IN="";FC="";k=0
for x in $ORD; do f=$x.mp4; [ -f clips/$x.mp4 ] && f=clips/$x.mp4; IN="$IN -i $f"; FC="$FC[$k:v]setsar=1,fps=30,format=yuv420p[v$k];[$k:a]aresample=48000,aformat=channel_layouts=stereo[a$k];"; k=$((k+1)); done
for ((i=0;i<k;i++)); do FC="$FC[v$i][a$i]"; done
FC="${FC}concat=n=$k:v=1:a=1[v][pa];[pa]asplit[pa1][pa2];[$k:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.55[mu];[mu][pa1]sidechaincompress=threshold=0.015:ratio=10:attack=30:release=500[du];[pa2][du]amix=inputs=2:normalize=0:duration=first[a]"
ffmpeg -v error -y $IN -i music.wav -filter_complex "$FC" -map "[v]" -map "[a]" -c:v libx264 -crf 23 -preset veryfast -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart video1_v3.mp4
echo done > v3done
