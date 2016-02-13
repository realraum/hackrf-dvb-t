#!/bin/sh

FIFO_D="fifos"

RAW_VIDEO_FIFO="$FIFO_D/video.raw"
PES_VIDEO_FIFO="$FIFO_D/video.pes"
TS_VIDEO_FIFO="$FIFO_D/video.ts"

RAW_AUDIO_FIFO="$FIFO_D/audio.raw"
PES_AUDIO_FIFO="$FIFO_D/audio.pes"
TS_AUDIO_FIFO="$FIFO_D/audio.ts"

MUXED_FIFO="$FIFO_D/muxed.ts"
TDT_FIFO="$FIFO_D/tdt.ts"
STAMP_FIFO="$FIFO_D/stamp.ts"

####

./killall.sh

##

mkdir -p "$FIFO_D"
rm -f "$RAW_VIDEO_FIFO"
rm -f "$PES_VIDEO_FIFO"
rm -f "$TS_VIDEO_FIFO"
rm -f "$RAW_AUDIO_FIFO"
rm -f "$PES_AUDIO_FIFO"
rm -f "$TS_AUDIO_FIFO"
rm -f "$MUXED_FIFO"
rm -f "$TDT_FIFO"
rm -f "$STAMP_FIFO"

mkfifo "$RAW_VIDEO_FIFO"
mkfifo "$PES_VIDEO_FIFO"
mkfifo "$TS_VIDEO_FIFO"
mkfifo "$RAW_AUDIO_FIFO"
mkfifo "$PES_AUDIO_FIFO"
mkfifo "$TS_AUDIO_FIFO"
mkfifo "$MUXED_FIFO"
mkfifo "$TDT_FIFO"
mkfifo "$STAMP_FIFO"

BRUTTO_BITRATE=`./dvbt-bitrate.py --short`
#NETTO_BITRATE=4140916
NETTO_BITRATE=4196916
#NETTO_BITRATE=2496916
NULL_BITRATE=$(($BRUTTO_BITRATE - $NETTO_BITRATE))

#./src.sh "$RAW_VIDEO_FIFO" "$RAW_AUDIO_FIFO" &
#./src.sh "$RAW_VIDEO_FIFO" /dev/null &
#./src.sh  /dev/null "$RAW_AUDIO_FIFO" &

## Video (tutorial page: 69)
#esvideompeg2pes "$RAW_VIDEO_FIFO" > "$PES_VIDEO_FIFO" &
#pesvideo2ts 2064 25 112 4000000 0 "$PES_VIDEO_FIFO" > "$TS_VIDEO_FIFO" &

## Audio  (tutorial page: 70)
#esaudio2pes "$RAW_AUDIO_FIFO" 1152 48000 384 -1 3600 > "$PES_AUDIO_FIFO" &
#esaudio2pes "$RAW_AUDIO_FIFO" 1152 48000 384 -1 > "$PES_AUDIO_FIFO" &
#pesaudio2ts 2068 1152 48000 384 0 "$PES_AUDIO_FIFO" > "$TS_AUDIO_FIFO" &

## Mux  (tutorial page: 31)
# tscbrmuxer b:4000000 "$TS_VIDEO_FIFO" b:128000 "$TS_AUDIO_FIFO"                       \
#            b:3008 opencaster/pat.ts b:3008 opencaster/pmt.ts b:1500 opencaster/sdt.ts \
#            b:1400 opencaster/nit.ts b:2000 opencaster/eit.ts b:2000 opencaster/tdt.ts \
#            b:$NULL_BITRATE opencaster/null.ts > "$MUXED_FIFO" &


#tsloop opencaster/firstvideo.ts > "$TS_VIDEO_FIFO" &
#tsloop opencaster/firstaudio.ts > "$TS_AUDIO_FIFO" &

tsloop video.ts > "$TS_VIDEO_FIFO" &
tsloop audio.ts > "$TS_AUDIO_FIFO" &

tscbrmuxer b:4000000 "$TS_VIDEO_FIFO" b:188000 "$TS_AUDIO_FIFO"                               \
            b:3008 opencaster/firstpat.ts b:3008 opencaster/firstpmt.ts b:1500 opencaster/firstsdt.ts \
            b:1400 opencaster/firstnit.ts b:$NULL_BITRATE opencaster/null.ts > "$MUXED_FIFO" &

# while true; do sleep 1; done

#tstdt "$MUXED_FIFO" > "$TDT_FIFO" &
tsstamp "$MUXED_FIFO" $BRUTTO_BITRATE > "$STAMP_FIFO" &

cat "$STAMP_FIFO" > all.ts

#./dvbt-hackrf.py "$STAMP_FIFO"

exit 0
