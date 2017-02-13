#!/usr/bin/bash

# run this with 'watch -n15 . ./masternode-count.sh'

# If systemd-managed...
LF="sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf masternode list full"

# If "normal user" deployed..
#LF="dash-cli masternode list full"

F=/tmp/tmp-count.txt
$LF > $F

total=$(cat $F | wc -l )
total_old=$(cat $F | grep 70103 | wc -l)
percent_old=`python -c "print round($total_old.0 / $total * 100, 2)"`

total_new=$(cat $F | grep 70206 | wc -l)
percent_new=`python -c "print round($total_new.0 / $total * 100, 2)"`

total_enabled=$(cat $F | grep ENABLED | grep -v PRE_ENABLED | wc -l)
percent_enabled=`python -c "print round($total_enabled.0 / $total * 100, 2)"`

total_enabled_old=$(cat $F | grep ENABLED | grep -v PRE_ENABLED | grep 70103 | wc -l)
percent_enabled_old=`python -c "print round($total_enabled_old.0 / $total_enabled * 100, 2)"`

total_enabled_new=$(cat $F | grep ENABLED | grep -v PRE_ENABLED | grep 70206 | wc -l)
percent_enabled_new=`python -c "print round($total_enabled_new.0 / $total_enabled * 100, 2)"`

echo "Masternodes...."
echo " [old]   70103: $total_old or $percent_old%"
echo " [new]   70206: $total_new or $percent_new%"
echo "         Total: $total"
echo
echo " [old] ENABLED: $total_enabled_old or $percent_enabled_old%"
echo " [new] ENABLED: $total_enabled_new or $percent_enabled_new%"
echo "         Total: $total_enabled or $percent_enabled%"
rm $F

