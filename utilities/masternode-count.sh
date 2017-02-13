#!/usr/bin/bash

# run this with 'watch -n15 . ./masternode-count.sh'

# If systemd-managed...
LF="sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf masternode list full"

# If "normal user" deployed..
#LF="dash-cli masternode list full"

F=/tmp/tmp-count.txt
$LF > $F

total=$(cat $F | wc -l )

total_old=$(cat $F | grep " 70103 " | wc -l)
percent_old=$(printf '%6.2f' `python -c "print round($total_old.0 / $total * 100, 2)"`)

total_new=$(cat $F | grep " 70206 " | wc -l)
percent_new=$(printf '%6.2f' `python -c "print round($total_new.0 / $total * 100, 2)"`)

total_enabled=$(cat $F | grep ENABLED | grep -v PRE_ENABLED | wc -l)
percent_enabled=$(printf '%6.2f' `python -c "print round($total_enabled.0 / $total * 100, 2)"`)
total_not_enabled=$(($total-$total_enabled))
percent_not_enabled=$(printf '%6.2f' `python -c "print round($total_not_enabled.0 / $total * 100, 2)"`)

total_enabled_old=$(cat $F | grep ENABLED | grep -v PRE_ENABLED | grep " 70103 " | wc -l)
total_not_enabled_old=$(($total_old-$total_enabled_old))
percent_enabled_old=$(printf '%6.2f' `python -c "print round($total_enabled_old.0 / $total_enabled * 100, 2)"`)
total_percent_enabled_old=$(printf '%6.2f' `python -c "print round($total_enabled_old.0 / $total * 100, 2)"`)
percent_not_enabled_old=$(printf '%6.2f' `python -c "print round($total_not_enabled_old.0 / $total_enabled * 100, 2)"`)
total_percent_not_enabled_old=$(printf '%6.2f' `python -c "print round($total_not_enabled_old.0 / $total * 100, 2)"`)

total_enabled_new=$(cat $F | grep ENABLED | grep -v PRE_ENABLED | grep " 70206 " | wc -l)
total_not_enabled_new=$(($total_new-$total_enabled_new))
percent_enabled_new=$(printf '%6.2f' `python -c "print round($total_enabled_new.0 / $total_enabled * 100, 2)"`)
total_percent_enabled_new=$(printf '%6.2f' `python -c "print round($total_enabled_new.0 / $total * 100, 2)"`)
percent_not_enabled_new=$(printf '%6.2f' `python -c "print round($total_not_enabled_new.0 / $total_enabled * 100, 2)"`)
total_percent_not_enabled_new=$(printf '%6.2f' `python -c "print round($total_not_enabled_new.0 / $total * 100, 2)"`)

percent_not_enabled_old_of_total_old=$(printf '%6.2f' `python -c "print round($total_not_enabled_old.0 / $total_old * 100, 2)"`)
percent_not_enabled_new_of_total_new=$(printf '%6.2f' `python -c "print round($total_not_enabled_new.0 / $total_new * 100, 2)"`)
percent_enabled_old_of_total_old=$(printf '%6.2f' `python -c "print round($total_enabled_old.0 / $total_old * 100, 2)"`)
percent_enabled_new_of_total_new=$(printf '%6.2f' `python -c "print round($total_enabled_new.0 / $total_new * 100, 2)"`)

echo "Masternodes...."
echo -e " [old]    70103: $(printf '%4s' $total_old) - $percent_old%"
echo -e " [new]    70206: $(printf '%4s' $total_new) - $percent_new%"
echo "          Total: $(printf '%4s' $total)"
echo
echo -e " [old] !ENABLED: $(printf '%4s' $total_not_enabled_old) - $percent_not_enabled_old% (of !enabled) . $percent_not_enabled_old_of_total_old% (of total old) . $total_percent_not_enabled_old% (of total)"
echo -e " [new] !ENABLED: $(printf '%4s' $total_not_enabled_new) - $percent_not_enabled_new% (of !enabled) . $percent_not_enabled_new_of_total_new% (of total new) . $total_percent_not_enabled_new% (of total)"
echo -e "          Total: $(printf '%4s' $total_not_enabled) - $percent_not_enabled%"
echo
echo -e " [old]  ENABLED: $(printf '%4s' $total_enabled_old) - $percent_enabled_old%  (of enabled) . $percent_enabled_old_of_total_old% (of total old) . $total_percent_enabled_old% (of total)"
echo -e " [new]  ENABLED: $(printf '%4s' $total_enabled_new) - $percent_enabled_new%  (of enabled) . $percent_enabled_new_of_total_new% (of total new) . $total_percent_enabled_new% (of total)"
echo -e "          Total: $(printf '%4s' $total_enabled) - $percent_enabled%"
rm $F
