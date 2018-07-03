# Dash Core Troubleshooting Guide

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

Watch these..
```
# General info
watch -n10 "sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf getnetworkinfo"
```

```
# Masternode sync status
watch -n10 "sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore mnsync status"
```

```
# What does the network think the status of your masternode is?
# "ENABLED" is good.
# WARNING: It's better to verify this with a fully-synced wallet or other node.
#   If you masternode is not fully synced and not communicating correctly, it
#   will likely give you false information.
sudo -u dashcore watch -n10 "dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore masternode list full | grep <MASTERNODE_IP_ADDRESS>"
```

Finally, watch the system journal. If `dashd` crashes, this is where you will really notice.

```
sudo journalctl -u dashd.service -f
```


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

Watch these..
```
# General info
watch dash-cli getnetworkinfo
```

```
# Masternode sync status
watch dash-cli mnsync status
```

```
# What does the network think the status of your masternode is?
# "ENABLED" is good.
# WARNING: It's better to verify this with a fully-synced wallet or other node.
#   If you masternode is not fully synced and not communicating correctly, it
#   will likely give you false information.
dash-cli masternode list full | grep <MASTERNODE_IP_ADDRESS>"
```

How many masternodes are enabled at the moment?
```
sudo -u dashcore watch -n15 "dash-cli -conf=/etc/dashcore/dash.conf masternode list full| grep ENABLED|grep -v PRE_ENABLED|wc -l"
```

---

### That's all for the moment. Stay tuned. -t0dd

Got a dash of feedback? Send it my way: <https://keybase.io/toddwarner>
