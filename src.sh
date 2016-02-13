#!/bin/sh

OUT=$1
RATE=$2
IN=$3

if [ -z $OUT ] || [ -n $RATE ]; then
  echo "Usage: $0 <output> <bitrate> [ <input> ]"
fi

if [ -z "$IN" ]; then
  exec ffmpeg -f alsa -i pulse -f video4linux2 -s 1024x576 -i /dev/video0 -pix_fmt yuv420p \
     -vcodec mpeg2video -s 720x576 -r 25 -flags cgop+ilme -sc_threshold 1000000000 -g 25 -bf 2 -b:v 4M -minrate 4M -maxrate 4M -bufsize 2M \
     -acodec mp2 -ac 2 -b:a 192k -muxrate $RATE \
     -metadata service_provider="realraum" \
     -metadata service_name="realraum DVB-T Test" \
     -f mpegts pipe: > "$OUT"
else
  exec ffmpeg -i "$IN" \
     -vcodec mpeg2video -s 720x576 -r 25 -flags cgop+ilme -sc_threshold 1000000000 -g 25 -bf 2 -b:v 4M -minrate 4M -maxrate 4M -bufsize 2M \
     -acodec mp2 -ac 2 -b:a 192k -muxrate $RATE \
     -metadata service_provider="realraum" \
     -metadata service_name="realraum DVB-T Test" \
     -f mpegts pipe: > "$OUT"
fi
