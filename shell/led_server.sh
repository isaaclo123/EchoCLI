#!/bin/bash
while read REPLY
do
    ledctrl -c &>/dev/null
    ledctrl -s $REPLY &>/dev/null
    echo $?
done
