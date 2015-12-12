#!/bin/sh

OUT=$1

rm -f "$IN_FIFO"
mkfifo $IN_FIFO

#exec avconv -f alsa -i pulse -f video4linux2 -s 640x480 -i /dev/video0 -vf drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf:text="XXXXXX":x=440:y=420:fontsize=48:fontcolor=white@0.6:box=1:boxcolor=black@0.2 -vcodec mpeg2video -s 640x480 -r 60 -b 4000000 -acodec mp2 -ar 48000 -ab 192000 -ac 2 -muxrate 4524064 -mpegts_transport_stream_id 1025 -mpegts_service_id 1 -mpegts_pmt_start_pid 0x162 -mpegts_start_pid 0x0121 -f mpegts -y "$IN_FIFO"

exec avconv -f alsa -i pulse -f video4linux2 -s 640x480 -i /dev/video0 -vcodec mpeg2video -s 640x480 -r 25 -b 4000000 -acodec mp2 -ar 48000 -ab 192000 -ac 2 \
     -metadata service_provider="realraum" \
     -metadata service_name="realraum DVB-T Test" \
     -f mpegts -y "$OUT"
