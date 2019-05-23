# Dash Core Troubleshooting Guide

**NOTE:** 0.13.0 has been released. This troubleshooting guide has not
reflected this just yet. Thank you for your patience. -t0dd

There are a zillion ways your wallet or masternode can get in a state that is
non-operational. Often what is truly wrong is difficult to determine and/or
poorly messages. This guide will help you examine and correct some of the most
common issues.

> NOTE: THIS IS A WORK IN PROGRESS -- more to come


## Tail this; watch that

There are a number of log files and watch commands you can issue to monitor the health of your masternode, wallet, node, etc.

> I just show you the commands for now without explaination.

### On a masternode

#### If configured and operated as a `systemd` service

Watch Sentinel's activity - silence is good. Make sure you check your crontab
settings to see if you are actually loging to this file, by default, you will
be if you install with our RPM packages.
```
sudo tail -f /var/log/dashcore/sentinel.log
```

```
# mainnet
sudo tail -f /var/lib/dashcore/debug.log
# testnet
sudo tail -f /var/lib/dashcore/testnet3/debug.log
```

Watch this..
```
# Masternode sync status
watch -n10 "sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore mnsync status"
```

<!--
```
# What does the network think the status of your masternode is?
# "ENABLED" is good.
# WARNING: It's better to verify this with a fully-synced wallet or other node.
#   If you masternode is not fully synced and not communicating correctly, it
#   will likely give you false information.
sudo -u dashcore watch -n10 "dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore masternode list full | grep <MASTERNODE_IP_ADDRESS>"
```
-->

General info
```
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf getnetworkinfo
```

General masternode status
```
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf masternode status
```


Is your masternode "valid?"
```
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf protx list valid | grep <the 'proTxHash' value from 'dash-cli masternode status'>
```

More info on your masternode
```
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf protx info <the 'proTxHash' value from 'dash-cli masternode status'>
```

How many masternodes are valid at the moment?
```
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf protx list valid | wc -l
```

Finally, watch the system journal. If `dashd` crashes, this is where you will really notice.

```
sudo journalctl -u dashd.service -f
```

> **PROTIP:**  
> Tired of typing that long `sudo -u dashcore` string? Add this to your `~/.bashrc` file:  
> `alias dashcli="sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore"`  
> . . Do that, logout and log back in, and you can then do things like `dashcli masternode status`  
> :)


#### If configured for and operated by a "normal" user on the system...

I.e., Your data directory is in ~/.dashcore and configuration file is
~/.dashcore/dash.conf

Watch Sentinel's activity - silence is good. Make sure you check your crontab
settings to see if you are actually loging to this file, by default, you will
be if you install with our RPM packages.
```
sudo tail -f /var/log/dashcore/sentinel.log
```

```
# mainnet
tail -f ~/.dashcore/debug.log
# testnet
tail -f ~/.dashcore/testnet3/debug.log
```

Watch this..
```
# Masternode sync status
watch dash-cli mnsync status
```

<!--
What does the network think the status of your masternode is?  
"ENABLED" is good.
```
# WARNING: It's better to verify this with a fully-synced wallet or other node.
#   If you masternode is not fully synced and not communicating correctly, it
#   will likely give you false information.
dash-cli masternode list full | grep <MASTERNODE_IP_ADDRESS>"
```

How many masternodes are enabled at the moment?
```
sudo -u dashcore watch -n15 "dash-cli -conf=/etc/dashcore/dash.conf masternode list full| grep ENABLED|grep -v PRE_ENABLED|wc -l"
```
-->

General info
```
dash-cli getnetworkinfo
```

Masternode general status
```
dash-cli masternode status
```

Is your masternode "valid?"
```
dash-cli protx list valid | grep <the 'proTxHash' value from 'dash-cli masternode status'>
```

How many masternodes are valid at the moment?
```
dash-cli protx list valid | wc -l
```

---

### That's all for the moment. Stay tuned. -t0dd

Got a dash of feedback? Send it my way: <https://keybase.io/toddwarner>
