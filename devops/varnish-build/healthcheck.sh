#!/bin/bash

ps_state=$(grep 'varnishd' /proc/[0-9]*/status | awk -F: '{split($1,a,/\//); print a[3] $3}')
echo ${ps_state}
ps_state=$(echo $ps_state | grep "$1")
if [[ "$ps_state" != " " ]]; then
        echo ".... running"
        exit 0
else
        echo ".... not running"
        exit 1
fi
