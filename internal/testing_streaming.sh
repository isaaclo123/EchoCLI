#!/bin/bash
# IMPORTANT NOTE! For some reason, sometimes the audio is on 100% static all the time. Reopen the connection until it is okay.
# Be careful of your ears, it can get really loud!
nc 10.0.0.97 8080 | aplay -vvv --rate 16000 --period-size=2000 -c 9 -f S24_3LE --buffer-size 8000
