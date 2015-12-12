#!/bin/sh

gst-launch-1.0 videotestsrc ! video/x-raw,width=1024,height=576,framerate=25/1 !                      \
               textoverlay text="realraum DVB-T Test" shaded-background=true font-desc="Ubuntu 20" !  \
               videoscale ! video/x-raw,width=720,height=576 ! jpegenc ! queue ! mux.                 \
               audiotestsrc ! audio/x-raw,channels=2,rate=48000 ! audioconvert !                      \
               vorbisenc bitrate=250000 ! queue ! mux.                                                \
               matroskamux name=mux ! filesink location=test.mkv
