#!/bin/bash
# usage: fbvar.sh in.mp4 track.wav music_offset out.mp4 [trim_start] [tint]
v=$1; a=$2; s=$3; o=$4; ts=${5:-0.5}; tint=${6:-"colorbalance=rs=0.04:gs=0.0:bs=-0.04:rm=0.03:bm=-0.03"}
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
d=$(python3 -c "print(round($d-$ts,2))"); fo=$(python3 -c "print(max(0,$d-0.7))")
ffmpeg -y -v error -ss $ts -i "$v" -ss $s -t $d -i "$a" -map 0:v:0 -map 1:a:0 \
 -vf "scale=iw*1.08:ih*1.08,crop=1080:1920,eq=saturation=1.15:contrast=1.05,${tint},format=yuv420p" \
 -c:v libx264 -preset slow -crf 19 -r 30 \
 -af "afade=t=in:st=0:d=0.15,afade=t=out:st=$fo:d=0.7,loudnorm=I=-14:TP=-1.5:LRA=11" \
 -ar 48000 -c:a aac -b:a 192k -t $d -movflags +faststart "$o"
