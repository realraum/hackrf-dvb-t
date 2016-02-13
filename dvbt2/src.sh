#!/bin/sh

OUT=$1
IN=$2

if [ -z "$2" ]; then
  rm -f "$OUT"
  mkfifo "$OUT"
#  exec ffmpeg -f alsa -i pulse -f video4linux2 -s 640x480 -i /dev/video0 -vcodec mpeg2video -s 640x480 -r 25 -vb 4000000 -acodec mp2 -ar 48000 -ab 192000 -ac 2 \
#     -metadata service_provider="realraum" \
#     -metadata service_name="realraum DVB-T Test" \
#     -f mpegts -y "$OUT"
else
#  exec ffmpeg -i "$IN" -vcodec mpeg2video -s 1920x1080 -r 25 -flags cgop+ilme -sc_threshold 1000000000 -g 25 -bf 2 -b:v 4M -minrate 4M -maxrate 4M -bufsize 2.3M -acodec mp2 -ac 2 -b:a 256k \
#        -metadata service_provider="realraum" -metadata service_name="realraum DVB-T2 Test" -f mpegts -y "$OUT"
  exec ffmpeg -i "$IN" -vcodec copy -acodec copy -copyts \
        -metadata service_provider="realraum" -metadata service_name="realraum DVB-T2 Test" -f mpegts -y "$OUT"

fi
