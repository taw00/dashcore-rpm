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

testnet=0
config=/etc/dashcore/dash.conf
ip=93.184.216.34 # Your masternode IP address
logfile=
#logfile="/var/log/dashcore/mnstate.log" # If no logfile, only goes to stdout
noise=2 # 0=silence (except errors), 1=silent except timestamp of run, 2=loud

#username=dashcore
true_height=
my_height=
mn_enablement="ENABLED"
_network_string='[mainnet]'
_height_url="https://explorer.dash.org/chain/Dash/q/getblockcount"

if [[ testnet -eq 1 ]] ; then
  _network_string='[testnet]'
  _height_url="https://test.explorer.dash.org/chain/tDash/q/getblockcount"
fi

_d=$(date --utc +"%b %d %T UTC $_network_string")

if [[ noise -gt 0 ]] ; then
  m="$_d ---"
  echo $m
  if [[ $logfile ]] ; then echo $m >> $logfile ; fi
fi

true_height=$(curl --silent -o - $_height_url)
while [[ true_height -lt 1 ]] ; do
  m="$_d --- No results from $_height_url Trying again."
  echo $m
  if [[ $logfile ]] ; then echo $m >> $logfile ; fi
  sleep 3
  true_height=$(curl --silent -o - $_height_url)
done

my_height=$(dash-cli -conf=$config getblockcount)
while [[ my_height -lt 1 ]] ; do
  m="$_d --- No results from 'dash-cli getblockcount' Trying again."
  echo $m
  if [[ $logfile ]] ; then echo $m >> $logfile ; fi
  sleep 3
  my_height=$(dash-cli -conf=$config getblockcount)
done

msg1="$_d Current block height is $true_height"
if [[ $true_height -ne $my_height ]] ; then
  msg1="$_d WARNING! Height mismatch! Network height versus this node: $true_height : $my_height"
  echo $msg1
  if [[ $logfile ]] ; then echo $msg1 >> $logfile ; fi
  exit 1
elif [[ noise -gt 1 ]] ; then
  echo $msg1
  if [[ $logfile ]] ; then echo $msg1 >> $logfile ; fi
fi

# Get masternode status string
mn_enablement=$(dash-cli -conf=/etc/dashcore/dash.conf masternode list full | grep $ip)
# Convert all double-quotes to spaces -- and then squash all the spaces into 1 each
mn_enablement=$(echo -e "${mn_enablement}" | tr -d [\"]|tr -s [:space:])
# Trim off beginning and ending whitespace
mn_enablement=$(echo -e "${mn_enablement}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
# Snag the actual enablement value
mn_enablement=$(echo -e "${mn_enablement}" | cut -d ' ' -f2)
msg2="$_d Masternode enablement status: $mn_enablement"
if [[ $mn_enablement -ne "ENABLED" && $mn_enablement -ne "PRE_ENABLED" ]] ; then
  msg2="$_d WARNING! Masternode state is not reporting as 'ENABLED' or 'PRE_ENABLED'. Reporting as: $mn_enablement"
  echo $msg2
  if [[ $logfile ]] ; then echo $msg2 >> $logfile ; fi
  exit 2
elif [[ noise -gt 1 ]] ; then
  echo $msg2
  if [[ $logfile ]] ; then echo $msg2 >> $logfile ; fi
fi

exit 0
