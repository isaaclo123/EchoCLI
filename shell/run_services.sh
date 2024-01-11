#!/bin/bash

adb shell "nohup sh /data/local/tmp/led.sh &"
adb shell "nohup sh /data/local/tmp/stream_audio.sh &"
