#!/bin/bash
# mux.sh video.mp4 track.wav start out.mp4
v=$1; a=$2; s=$3; o=$4
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
fo=$(python3 -c "print(max(0,$d-0.7))")
ffmpeg -y -v error -i "$v" -ss $s -t $d -i "$a" -map 0:v:0 -map 1:a:0 -c:v copy \
 -af "afade=t=in:st=0:d=0.15,afade=t=out:st=$fo:d=0.7,loudnorm=I=-14:TP=-1.5:LRA=11" \
 -ar 48000 -c:a aac -b:a 192k -shortest -movflags +faststart "$o" && echo "ok $o"
