#!/bin/bash

PORT="8080"

iptables -P INPUT ACCEPT

cd /data/local/tmp
/data/local/tmp/busybox mkfifo /data/local/tmp/audio_fifo

# tinycap file.wav [-D card] [-d device] [-c channels] [-r rate] [-b bits] [-p period_size] [-n n_periods] [-t duration] [-f]
# tinymix | grep "Input Gain" | cut -f1

killall tinycap
killall mixer
tinycap /data/local/tmp/audio_fifo -D 0 -d 24 -r 16000 -c 9 -b 24 -p 512 -n 5 -f &

echo "run socat"

/data/local/tmp/socat -u - TCP-LISTEN:$PORT,forever,fork < /data/local/tmp/audio_fifo
