#!/bin/bash

# This is the bash script that will be run on the echo
# It will receive the value from the remote server, any of the following:
#
# - "mics-off_on"
# - "mics-off_start"
# - "mics-off_end"
# - "error"
# - "off"
# - "solid_blue"
# - "solid_cyan"
# - "solid_green"
# - "solid_orange"
# - "solid_red"
# - "solid_white
# - "zzz_disco"
# - "zzz_rainbow"
# - "zzz_turbo-boost"

iptables -P INPUT ACCEPT

PORT=8000
/data/local/tmp/socat -v tcp-l:$PORT,fork exec:'sh /data/local/tmp/led_server.sh'
