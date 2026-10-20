#!/bin/bash
cd /home/claude/music
H(){ python3 hook.py "final/$1" "tus_tmp/$2" "$3" "$4" $5 $6 775 $7 >/dev/null; }
H reel-halloween-8s.mp4 halloween.mp4 "Last-minute costumes" "for the whole family" 1.0 3.0 3.0 &
H reel-vpn-8s.mp4 vpn.mp4 "Stop using hotel Wi-Fi" "until you see this" 0.2 3.55 0 &
H brand-2-travel.mp4 travel.mp4 "Planning a 2027 trip?" "Book in this order" 0.2 2.8 0 &
H brand-3-sidehustle.mp4 sidehustle.mp4 "Free AI can do this" "12 tasks, zero cost" 0.2 2.8 0 &
wait
H reel-europe-8s.mp4 europe.mp4 "Fly to Europe for less" "pick the right month" 0.2 3.55 0 &
H brand-4-home.mp4 herbs.mp4 "Grow herbs indoors" "even in winter" 0.2 2.8 0 &
H brand-5-family.mp4 family.mp4 "No-screen family night?" "20 easy ideas" 0.2 2.8 0 &
wait
T2="colorbalance=rs=-0.03:bs=0.04:gm=0.02"; T3="colorbalance=rs=0.02:gs=0.03:bs=-0.02"; T4="colorbalance=rs=0.05:gs=0.01:bs=-0.05"
./fbvar.sh tus_tmp/halloween.mp4 tracks/halloween.wav 8 tus/tt-us-17-halloween.mp4 0.15 "$T4" &
./fbvar.sh tus_tmp/vpn.mp4 tracks/phonk.wav 44 tus/tt-us-18-vpn.mp4 0.15 "$T3" &
./fbvar.sh tus_tmp/travel.mp4 tracks/phonk.wav 24 tus/tt-us-19-travel.mp4 0.15 "$T2" &
./fbvar.sh tus_tmp/sidehustle.mp4 tracks/lofi.wav 20 tus/tt-us-20-sidehustle.mp4 0.15 "$T4" &
wait
./fbvar.sh tus_tmp/europe.mp4 tracks/lofi.wav 26 tus/tt-us-21-europe.mp4 0.15 "$T3" &
./fbvar.sh tus_tmp/herbs.mp4 tracks/phonk.wav 5 tus/tt-us-22-herbs.mp4 0.15 "$T2" &
./fbvar.sh tus_tmp/family.mp4 tracks/lofi.wav 2 tus/tt-us-23-family.mp4 0.15 "$T4" &
wait
