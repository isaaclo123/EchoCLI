#!/bin/bash
nc 10.0.0.97 8080 | aplay -vvv --rate 16000 --period-size=2000 -c 9 -f S24_3LE --buffer-size 8000
