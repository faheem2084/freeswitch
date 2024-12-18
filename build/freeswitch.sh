#!/bin/sh
echo "Welcome to Freeswitch";
/usr/bin/freeswitch  "$@"
/usr/bin/freeswitch -nc -nf -nonat & pid="$!"

wait $pid
exit 0
# /usr/bin/freeswitch -ncwait -nonat  "$@"
