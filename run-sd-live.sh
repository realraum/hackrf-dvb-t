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

BRUTTO_RATE="4976470" #  `./dvbt-bitrate.py --short`

VIDEO_RATE=4200000
AUDIO_RATE=188000
PAT_RATE=3008
PMT_RATE=3008
SDT_RATE=1500
NIT_RATE=1400
EIT_RATE=2000
TDT_RATE=2000

NETTO_RATE=$(($VIDEO_RATE + $AUDIO_RATE + $PAT_RATE + $PMT_RATE + $SDT_RATE + $NIT_RATE + $EIT_RATE + $TDT_RATE))
NULL_RATE=$(($BRUTTO_RATE - $NETTO_RATE))


./src-decklink.sh "$RAW_VIDEO_FIFO" "$RAW_AUDIO_FIFO" &
#./src-rtp.sh "$RAW_VIDEO_FIFO" "$RAW_AUDIO_FIFO" &
#./src-rtp.sh "$RAW_VIDEO_FIFO" /dev/null &
#./src-rtp.sh  /dev/null "$RAW_AUDIO_FIFO" &

## Video (tutorial page: 69)
esvideompeg2pes "$RAW_VIDEO_FIFO" > "$PES_VIDEO_FIFO" &
pesvideo2ts 2064 25 112 $VIDEO_RATE 0 "$PES_VIDEO_FIFO" > "$TS_VIDEO_FIFO" &

## Audio  (tutorial page: 70)
esaudio2pes "$RAW_AUDIO_FIFO" 1152 48000 384 0 > "$PES_AUDIO_FIFO" &
#esaudio2pes "$RAW_AUDIO_FIFO" 1152 48000 384 0 7200 > "$PES_AUDIO_FIFO" &
pesaudio2ts 2068 1152 48000 384 0 "$PES_AUDIO_FIFO" > "$TS_AUDIO_FIFO" &


#tsloop video.ts > "$TS_VIDEO_FIFO" &
#tsloop audio.ts > "$TS_AUDIO_FIFO" &


#tsloop clock-video.ts > "$TS_VIDEO_FIFO" &
#tsloop clock-audio.ts > "$TS_AUDIO_FIFO" &


## Mux  (tutorial page: 31)
tscbrmuxer b:$VIDEO_RATE "$TS_VIDEO_FIFO" b:$AUDIO_RATE "$TS_AUDIO_FIFO"                              \
            b:$PAT_RATE opencaster/pat.ts b:$PMT_RATE opencaster/pmt.ts b:$SDT_RATE opencaster/sdt.ts \
            b:$NIT_RATE opencaster/nit.ts b:$EIT_RATE opencaster/eit.ts b:$TDT_RATE opencaster/tdt.ts \
            b:$NULL_RATE opencaster/null.ts > "$MUXED_FIFO" &

tstdt "$MUXED_FIFO" > "$TDT_FIFO" &
tsstamp "$TDT_FIFO" $BRUTTO_RATE > "$STAMP_FIFO" &

#cat "$STAMP_FIFO" > all.ts
#./dvbt-hackrf.py "$STAMP_FIFO"
../tsrfsend-nosvn/tsrfsend "$STAMP_FIFO" 0 498000 8000 4 1/2 1/4 2 0 3


exit 0
