#!/usr/bin/bash

# Run this sudo'ed to the right username on your Dash Masternode
# Example: sudo -u dashcore /usr/bin/bash ./mnstate.sh
#
# This utility will examine...
# * Block height of the network
# * Block height of the masternode
# * Masternode ENABLED state
#
# All gets logged to /var/log/dashcore/mnstate.log and printed to the screen (stdout)
# If there seems something amiss, mnstate.log will exit with a non-zero error code.
#
# Exit codes...
# 0 = All seems well
# 1 = Block heights do not match
# 2 = Masternode not in ENABLED or PRE_ENABLED state



testnet=1
config=/etc/dashcore/dash.conf
# USE YOUR MN IP ADDRESS HERE
ip=93.184.216.34
logfile=/var/log/dashcore/mnstate.log

#username=dashcore
true_height=-1
my_height=-1
mn_enablement="ENABLED"
_network_string='[mainnet]'

if [[ testnet -eq 1 ]] ; then
  true_height=$(curl --silent -o - https://test.explorer.dash.org/chain/tDash/q/getblockcount)
  _network_string='[testnet]'
else
  true_height=$(curl --silent -o - https://explorer.dash.org/chain/Dash/q/getblockcount)
fi

_d=$(date --utc +"%b %d %T UTC $_network_string")
echo "$_d ---"
echo "$_d ---" >> $logfile

my_height=$(dash-cli -conf=$config getblockcount)
mn_enablement=$(dash-cli -conf=/etc/dashcore/dash.conf masternode list full | grep $ip | tr -s [:space:] | cut -d ' ' -f4)

msg1="$_d Current block height is $true_height"


if [[ $true_height -ne $my_height ]] ; then
  msg1="$_d WARNING! Height mismatch! Network height versus this node: $true_height : $my_height"
  echo $msg1
  echo $msg1 >> $logfile
  exit 1
else
  echo $msg1
  echo $msg1 >> $logfile
fi


msg2="$_d Masternode enablement status: $mn_enablement"
if [[ $mn_enablement -ne "ENABLED" && $mn_enablement -ne "PRE_ENABLED" ]] ; then
  msg2="$_d WARNING! Masternode state is not reporting as 'ENABLED' or 'PRE_ENABLED'. Reporting as: $mn_enablement"
  echo $msg2
  echo $msg2 >> $logfile
  exit 2
else
  echo $msg2
  echo $msg2 >> $logfile
fi

exit 0
