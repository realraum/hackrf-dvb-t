#!/bin/sh

VFIFO=$1
AFIFO=$2

if [ -z $VFIFO ] || [ -z $AFIFO ]; then
  echo "Usage: $0 <video-fifo> <audio-fifo>"
  exit 1
fi

#exec ffmpeg -i rtp://89.106.211.60:5000 \
exec ../../bmdtools/bmdcapture -C 0 V 3 -A 2 -m 9 -F nut -f pipe:1 | ffmpeg -vsync passthrough -i pipe:0 \
     -vcodec mpeg2video -s 720x576 -r 25 -g 25 -pix_fmt yuv420p -bf 2 -b:v 3550k -minrate 3550k -maxrate 3550k -bufsize 2000k -f mp2 -map 0:0 pipe:3 \
     -acodec mp2 -ac 2 -b:a 128k -f mp2 -map 0:1 pipe:4   3> "$VFIFO" 4> "$AFIFO"
