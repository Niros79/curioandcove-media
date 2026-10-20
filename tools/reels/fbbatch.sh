#!/bin/bash
cd /home/claude/music
T1="colorbalance=rs=0.04:bs=-0.04:rm=0.03:bm=-0.03"; T2="colorbalance=rs=-0.03:bs=0.04:gm=0.02"; T3="colorbalance=rs=0.02:gs=0.03:bs=-0.02"
./fbvar.sh hook/reel-halloween.mp4 tracks/halloween.wav 13.5 fb2/fb-17-halloween.mp4 0.3 "$T1" &
./fbvar.sh hook/reel-vpn.mp4 tracks/phonk.wav 37 fb2/fb-18-vpn.mp4 0.3 "$T2" &
./fbvar.sh hook/brand-2-travel.mp4 tracks/pop.wav 22 fb2/fb-19-travel.mp4 0.3 "$T3" &
./fbvar.sh hook/brand-3-sidehustle.mp4 tracks/phonk.wav 18.5 fb2/fb-20-sidehustle.mp4 0.3 "$T2" &
wait
./fbvar.sh hook/reel-europe.mp4 tracks/lofi.wav 46 fb2/fb-21-europe.mp4 0.3 "$T1" &
./fbvar.sh hook/brand-4-home.mp4 tracks/lofi.wav 10 fb2/fb-22-herbs.mp4 0.3 "$T3" &
./fbvar.sh hook/brand-5-family.mp4 tracks/lofi.wav 52 fb2/fb-23-family.mp4 0.3 "$T1" &
wait
