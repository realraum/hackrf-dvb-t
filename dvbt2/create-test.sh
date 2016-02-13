#!/bin/sh

gst-launch-1.0 videotestsrc ! video/x-raw,width=1920,height=1080,framerate=25/1 !                     \
               textoverlay text="realraum DVB-T2 Test" shaded-background=true font-desc="Ubuntu 20" ! \
               jpegenc ! queue ! mux.                                                                 \
               audiotestsrc ! audio/x-raw,channels=2,rate=48000 ! audioconvert !                      \
               vorbisenc bitrate=250000 ! queue ! mux.                                                \
               matroskamux name=mux ! filesink location=test.mkv
