#!/bin/bash

HOST="http://192.168.1.81"  # Replace with the local IP of the machine running the server script.
PORT="10902"

# ledctrl -s mics-off_start -b 100
# ledctrl -s mics-off_on -b 100


while true; do
    # Kill mixer process which takes control of audio interfaces
    killall mixer
    nohup tinycap -- -D 0 -d 24 -r 16000 -b 24 -c 9 -p 512 -n 5 | stdbuf -i0 nc -u $HOST $PORT &
done

# while true; do
#     # Kill mixer process which takes control of audio interfaces
#     killall mixer
# 
#     # Record audio
#     nohup tinycap /data/local/tmp/out.wav -- -D 0 -d 24 -r 16000 -b 24 -c 9 -p 512 -n 5 | nc -u $HOST $PORT &
#     sleep 60
#     killall tinycap
# 
#     send_request
#     status_code=$?
# 
#     if [[ $status_code -ne 0 ]]; then
#         echo "Request failed. Retrying..."
#         handle_unsuccessful_req
#     fi
# 
#     rm -f out.wav
# done
