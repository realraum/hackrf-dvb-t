#!/bin/sh

VFIFO=$1
AFIFO=$2

if [ -z $VFIFO ] || [ -z $AFIFO ]; then
  echo "Usage: $0 <video-fifo> <audio-fifo>"
  exit 1
fi

exec ffmpeg -f alsa -i pulse -f video4linux2 -s 1024x576 -i /dev/video0 -pix_fmt yuv420p \
     -vcodec mpeg2video -s 720x576 -r 25 -flags cgop+ilme -sc_threshold 1000000000 -g 25 -bf 2 -b:v 4M -minrate 4M -maxrate 4M -bufsize 2M -f mp2 -map 1 pipe:3 \
     -acodec mp2 -ac 2 -b:a 192k -f mp2 -map 0 pipe:4   3> "$VFIFO" 4> "$AFIFO"
