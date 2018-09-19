#!/usr/bin/bash

# Run this sudo'ed to the right username on your Dash Masternode
# Example: sudo -u dashcore /usr/bin/bash ./masternode-state.sh
#
# This utility will examine...
# * Block height of the network
# * Block height of the masternode
# * Masternode ENABLED state
#
# All gets logged to /var/log/dashcore/masternode-state.log and printed to the screen (stdout)
# If there seems something amiss, masternode-state.log will exit with a non-zero error code.
#
# Optionally send email if NEW_START_REQUIRED or WATCHDOG_EXPIRED state is hit.
#   - interally from the code
#   - or, set up a cronjob and react to the exit code
#   - HowTo set up your server to email? Check out https://github.com/taw00/howto
#   
#
# Exit codes...
# 0 = All seems well
# 1 = Block heights do not match
# 2 = Masternode not in ENABLED or PRE_ENABLED state
# 3 = Both 1 and 2

testnet=0
ip=93.184.216.34_CHANGEME # Your masternode IP address

email_me=0
email_from="burner-address@yahoo.com"
email_to="personal-address@protonmail.com"
subject_qualifier="[masternode alias]"
body_text=""

# Output settings
# noise - 0=silence (except errors), 1=silent except timestamp of run, 2=loud
# logfile - If no logfile, only goes to stdout
noise=2
logfile=
#logfile="/var/log/dashcore/masternode-state.log"

config=/etc/dashcore/dash.conf
datadir=/var/lib/dashcore

# ---- don't edit anything after this ----

#username=dashcore
true_height=
my_height=
mn_enablement="ENABLED"
_network_string='[mainnet]'
_height_url="https://explorer.dash.org/chain/Dash/q/getblockcount"
exit_code=0

if [[ testnet -eq 1 ]] ; then
  _network_string='[testnet]'
  _height_url="https://test.explorer.dash.org/chain/tDash/q/getblockcount"
fi

_d=$(date --utc +"%b %d %T UTC $_network_string")

if [[ $noise -gt 0 ]] ; then
  m="$_d ---"
  echo $m
  if [[ $logfile ]] ; then echo $m >> $logfile ; fi
fi

loopflag=0
true_height=$(curl --silent -o - $_height_url)
while [[ $true_height -lt 1 ]] ; do
  if [[ $(( ++loopflag )) -gt 5 ]] ; then exit -1 ; fi
  m="$_d --- No results from $_height_url Trying again."
  echo $m
  if [[ $logfile ]] ; then echo $m >> $logfile ; fi
  sleep 5
  true_height=$(curl --silent -o - $_height_url)
done

loopflag=0
my_height=$(dash-cli -conf=$config -datadir=$datadir getblockcount)
while [[ $my_height -lt 1 ]] ; do
  if [[ $(( ++loopflag )) -gt 5 ]] ; then exit -1 ; fi
  m="$_d --- No results from 'dash-cli getblockcount' Trying again."
  echo $m
  if [[ $logfile ]] ; then echo $m >> $logfile ; fi
  sleep 5
  my_height=$(dash-cli -conf=$config -datadir=$datadir getblockcount)
done

msg1="$_d Current block height is $true_height"
if [[ $true_height -ne $my_height ]] ; then
  msg1="$_d WARNING! Height mismatch! Network height versus this node: $true_height : $my_height"
  exit_code=$(($exit_code+1))
fi

# Get masternode status string
mn_enablement=$(dash-cli -conf=$config -datadir=$datadir masternode list full | grep $ip)
# Convert all double-quotes to spaces -- and then squash all the spaces into 1 each
mn_enablement=$(echo -e "${mn_enablement}" | tr -d [\"]|tr -s [:space:])
# Trim off beginning and ending whitespace
mn_enablement=$(echo -e "${mn_enablement}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
# Snag IP address
ip_address=$(echo -e "${mn_enablement}" | cut -d ' ' -f9 | cut -d ':' -f1 )
msg_ip1="$_d IP address configured: $ip"
msg_ip2="$_d IP address reported:   $ip_address"
# Snag Protocol
protocol=$(echo -e "${mn_enablement}" | cut -d ' ' -f3)
msg_proto="$_d Protocol: $protocol"
# Snag public key
pubkey=$(echo -e "${mn_enablement}" | cut -d ' ' -f4)
msg_pubkey="$_d pubkey: $pubkey"
# Snag public key
# Snag the actual enablement value
mn_enablement=$(echo -e "${mn_enablement}" | cut -d ' ' -f2)
msg2="$_d Masternode enablement status: $mn_enablement"

if [[ $mn_enablement -ne "ENABLED" && $mn_enablement -ne "PRE_ENABLED" ]] ; then
  msg2="$_d WARNING! Masternode state is not reporting as 'ENABLED' or 'PRE_ENABLED'. Reporting as: $mn_enablement"
  exit_code=$(($exit_code+2))
fi

if [[ $exit_code -gt 0 || $noise -gt 1 ]] ; then
  if [[ $logfile ]] ; then
    echo $msg1 >> $logfile
    echo $msg_ip1 >> $logfile
    echo $msg_ip2 >> $logfile
    echo $msg_proto >> $logfile
    echo $msg_pubkey >> $logfile
    echo $msg2 >> $logfile
  fi
  echo $msg1
  echo $msg_ip1
  echo $msg_ip2
  echo $msg_proto
  echo $msg_pubkey
  echo $msg2
fi

if [[ $email_me -ne 0 ]] ; then
  body_text="$msg1\n$msg2\n"
  case $mn_enablement in
    WATCHDOG_EXPIRED|NEW_START_REQUIRED )
      echo -e $body_text | mail -s "$subject_qualifier $mn_enablement - $_d" -r $email_from $email_to
      m="$_d Alert email sent to $email_to from $email_from"
      echo $m
      if [[ $logfile ]] ; then echo $m >> $logfile ; fi
    ;;
  esac
  # Other way of doing the same thing...
  #if [[ "$mn_enablement" =~ ^(WATCHDOG_EXPIRED|NEW_START_REQUIRED)$ ]] ; then
  #  cat $body_text | mail -s "$subject_qualifier $mn_enablement - $_d" -r $email_from $email_to
  #fi
fi


exit $exit_code
