#!/bin/sh

killall -9 ffmpeg
killall esvideompeg2pes
killall pesvideo2ts
killall esaudio2pes
killall pesaudio2ts
killall tscbrmuxer
killall tstdt
killall tsstamp

exit 0
