cd /tmp/claude-0/-home-claude/87164e15-4779-5c7a-be25-1e13b780e99b/scratchpad/v1
ORD="nbx01 sigla nbx02 c10 nbx03 c9 nbx04 c8 nbx05 c7 nbx06 c6 nbx07 c5 nbx08 c4 nbx09 c3 nbx10 c2 nbx11 c1 nb12"
IN="";FC="";k=0
for x in $ORD; do f=$x.mp4; [ -f clips/$x.mp4 ] && f=clips/$x.mp4; IN="$IN -i $f"; FC="$FC[$k:v]setsar=1,fps=30,format=yuv420p[v$k];[$k:a]aresample=48000,aformat=channel_layouts=stereo[a$k];"; k=$((k+1)); done
for ((i=0;i<k;i++)); do FC="$FC[v$i][a$i]"; done
FC="${FC}concat=n=$k:v=1:a=1[v][pa];[pa]asplit[pa1][pa2];[$k:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.55[mu];[mu][pa1]sidechaincompress=threshold=0.015:ratio=10:attack=30:release=500[du];[pa2][du]amix=inputs=2:normalize=0:duration=first[a]"
ffmpeg -v error -y $IN -i music.wav -filter_complex "$FC" -map "[v]" -map "[a]" -c:v libx264 -crf 22 -preset veryfast -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart video1_v2.mp4
