# HowTo: Deploy and Configure a Dash Core Node as SystemD Service

_aka I want to run a Dash Core Node (or Masternode) like a SysAdmin!_

> This edition of these instructions is for those who wish to install and
> configure a Dash Node/Masternode running as a traditional `systemd` service. >
>
> A Dash Core Node (`dashd`) is a long-running daemon service, therefore it
> lends itself to the improved security and robustness that `systemd` provides.
> I.e., It really is the "right way" of running your node or masternode. Another
> "right way" would be to run it as a container. But that is beyond the scope of
> this document.

**Table of Content**

<!-- TOC START min:2 max:3 link:true update:true -->
- [FIRST: Install the operating systems](#first-install-the-operating-systems)
- [[1] Install Dash (and FirewallD)](#1-install-dash-and-firewalld)
- [[2] Configure Dash Server to be a Full Node](#2-configure-dash-server-to-be-a-full-node)
- [[3] Start up your Dash Core full node](#3-start-up-your-dash-core-full-node)
- [[4] Monitor the situation](#4-monitor-the-situation)
- [[5] Configure firewall rules](#5-configure-firewall-rules)
- [ALL DONE!](#all-done)
- [Email me when `dashd` starts or stops](#email-me-when-dashd-starts-or-stops)
- [Email the admin when the Masternode's status changes from "ENABLED"](#email-the-admin-when-the-masternodes-status-changes-from-enabled)
- [Super fancy crontab settings](#super-fancy-crontab-settings)
- [Improve SSD Write & Delete Performance for Linux Systems by Enabling ATA TRIM](#improve-ssd-write--delete-performance-for-linux-systems-by-enabling-ata-trim)

<!-- TOC END -->

## FIRST: Install the operating systems

Instruction for setting up, configuring, and securing a Fedora Linux system in preparation for deploying a Dash Core Node or Masternode can be found here: <https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.deploy-and-configure-operating-system.md>

Once completed, you may continue.

## [1] Install Dash (and FirewallD)

Because this is a Red Hat-based system, management of installed software is
trivial. This is how easy it is.

***Configure the Dash repositories (you only do this once)***

```bash
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/dashcore-rpm/master/toddpkgs-dashcore-repo.fedora.rpm
```
<!--
```
#sudo dnf config-manager --set-disabled dashcore-stable
#sudo dnf config-manager --set-enabled dashcore-testing
```
-->

<!--
...if this is CentOS or Red Hat Enterprise Linux

Note: You have to first ensure you have the EPEL repositories configured: `sudo yum repolist enabled`  
If you do not, browse to the [EPEL community page](https://fedoraproject.org/wiki/EPEL) and follow their installation instructions (it's easy).

Then...

```bash
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo yum install -y https://raw.githubusercontent.com/taw00/dashcore-rpm/master/toddpkgs-dashcore-repo.el7.rpm
```

```
#sudo yum-config-manager --disable dashcore-stable
#sudo yum-config-manager --enable dashcore-testing
```
-->

***Install Dash server***

```
sudo dnf install -y dashcore-server
```

<!--
...if this is CentOS or Red Hat Enterprise Linux

```
sudo yum install -y dashcore-server
```
-->

## [2] Configure Dash Server to be a Full Node

We are configuring this as a `systemd` service. Some of the process has been
done for you. Please note these differences from other instruction you may read
out there.

1. The default data directory will be `/var/lib/dashcore`
2. The default configuration file will be `/etc/dashcore/dash.conf`
3. Both are owned by system user (and group) `dashcore`
4. All elements in 1, 2, and 3 above were installed automatically by the dashcore-server RPM package.

Since the Dash service runs out of `dashcore` user owned directories and
configuration, many of our configuration and ongoing maintenance actions will
be performed by sudo'ing as that user. `dashcore` is a system user, as such that
user can't be logged into and has no home directory. What this means will
become self evident shortly.

A final note, since the default data directory and configuration file locations
are not traditional to the Dash Core upstream codebase, we will often have to
explicitly include them on the commandline when we perform actions.


***Edit `/etc/dashcore/dash.conf`***

In this example, we are going to get the dashcore server running as a node, but
not a masternode yet.

Log in as the normal user, `mnuser` in this example.

With your favorite editor &mdash; some use `nano`, I use `vim` &mdash; open up
`/etc/dashcore/dash.conf` and add the starting template shown below....

```
sudo -u dashcore nano /etc/dashcore/dash.conf
```

Edit that file and save this data in it...
```
# This is a Masternode Server configuration file
# 1 = run as testnet server (fake money), 0 = run as mainnet server (real money)
testnet=0
# Run dashd as a daemon (in the background)
daemon=1
# Listening mode, enabled by default except when 'connect' is being used
listen=1
logtimestamps=1
maxconnections=8

# Remote Procedure Call access configuration...
# server=1 tells Dash-QT and dashd to accept JSON-RPC commands
server=1
# You must set rpcuser and rpcpassword to secure the JSON-RPC api
rpcuser=<make_up_an_alphanumeric_username>
rpcpassword=<make_up_an_alphanumeric_password>
rpcport=9998
# A note about RPC connection control...
# Opening up the RPC port to hosts outside your local trusted network
# is NOT RECOMMENDED, because the rpcpassword is transmitted over the
# network unencrypted -- unless you set up SSL (beyond scope of this doc)
# Fortunately, as a small security measure, by default, only RPC connections
# from localhost are allowed. Specify as many rpcallowip= settings as you
# like to allow connections from other hosts, either as a single IPv4/IPv6
# or with a subnet specification.
rpcallowip=127.0.0.1

#masternode=1
#externalip=<results of "dig +short myip.opendns.com @resolver1.opendns.com">
#masternodeprivkey=<process addressed in separate document>
#masternodeblsprivkey=<new v0.13 process addressed in separate document>
```

Please take special note of `"testnet=1"` and `"testnet=0"`.

***Change your RPC (remote procedure call username and password)***

Edit `/etc/dashcore/dash.conf` and change...

```
rpcuser=<make_up_an_alphanumeric_username>
rpcpassword=<make_up_an_alphanumeric_password>
```
...to something else (this is an example)...
```
rpcuser=rpc_user_89752q340432
rpcpassword=this_is_a_random_password_984nf983n3o4n349nf9042nnfq3kgsdf898s
```

These are used by your on-system, internal commandline tools for the most part,
so you don't have to memorize them or use them outside of this masternode.

## [3] Start up your Dash Core full node

Log in as the normal user, `mnuser` in this example.

```
# Start the systemd services (as root) and enable to restart upon reboot
sudo systemctl start dashd
sudo systemctl enable dashd
```

> Now, if you have to reboot your system for whatever reason, the dash service
> will restart as well. It is worth remembering that a node, if configured as a
> masternode, does not need to be "restarted" (re-validated really) from a
> wallet unless it has been offline for some time (2 hours before it loses it's
> place in the queue and 3 hours before a "masternode start" from the wallet is
> required).


## [4] Monitor the situation

***SSH into two terminals and monitor the situation...***

...watch the logs in one terminal...

```
# ^C out of this tail feed when you are done...
sudo -u dashcore tail -f /var/lib/dashcore/debug.log # if mainnet
#sudo -u dashcore tail -f /var/lib/dashcore/testnet3/debug.log
```

...and watch the blockcount rise (hopefully) in the other terminal...

```
# ^C out of this loop when you are done
watch -n10 sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf getblockcount
```

You will know you have sync'ed the entire blockchain when it matches the current block-height:

* <https://insight.dashevo.org/insight/> &mdash; for mainnet
* <https://testnet-insight.dashevo.org/insight/> &mdash; for testnet

...or if you are comfortable on the commandline, these are helpful...

<!--
# Old URLs that prove to be unreliable
curl -o - https://explorer.dash.org/chain/Dash/q/getblockcount
curl -o - https://test.explorer.dash.org/chain/tDash/q/getblockcount
-->

```
# "mainnet" block height
_json=$(curl --silent -o - https://insight.dashevo.org/insight-api/status)
echo $_json | python3 -c "import sys, json; print(json.load(sys.stdin)['info']['blocks'])"

# "testnet" block height
_json=$(curl --silent -o - https://testnet-insight.dashevo.org/insight-api/status)
echo $_json | python3 -c "import sys, json; print(json.load(sys.stdin)['info']['blocks'])"

# These commands will spit out the block height for this network as your
# node sees it (ie. it could be wrong)
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf getchaintips |grep -m1 height | sed 's/[^0-9]*//g'
# ...or...
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf -conf=/etc/dashcore/dash.conf getblockcount
```



&nbsp;

---

***Once fully sync'ed your configuration as a full node is complete.***

---

&nbsp;

## [5] Configure firewall rules

You can follow the instruction in
[howto.dashcore-node-security.md](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.dashcore-node-security.md),
or just take these steps here. It's recommended that you review that document
though and perhaps implement some of the additional suggestions it may provide.


> _Note: Firewall rules can be a complicated topic. These are bare bones
> git-er-done instructions. You may want to investigate further refinement. It
> will get you started though._


```
# Is firewalld running?
# Turn on and enable firewalld if not already done...
sudo firewall-cmd --state
sudo systemctl start firewalld.service
sudo systemctl enable firewalld.service

# Determine what the default zone is.
# On vultr, for example, the default zone is FedoraServer (it is the assumption
# for this example)
sudo firewall-cmd --get-active-zone

# Whatever that default zone is, that is the starting conditions for your
# configuration. For this example, I am going to demonstrate how to edit my
# default configuration on my Fedora Linux system: FedoraServer. You _could_
# create your own zone definition, but for now, we will be editing the
# configuration that is in place.

# FedoraServer usually starts with ssh, dhcp6-client, and cockpit opened up
# I want to allow SSH and masternode traffic, but I don't want cockpit running
# all the time and by having a static IP, dhcpv6 service is unneccessary.
sudo firewall-cmd --permanent --add-service ssh
sudo firewall-cmd --permanent --add-service dashcore # mainnet
#sudo firewall-cmd --permanent --add-service dashcore-testnet
sudo firewall-cmd --permanent --remove-service dhcpv6-client
sudo firewall-cmd --permanent --remove-service cockpit

# Rate limit incoming ssh and cockpit (if configured on) traffic to 10 per minute
sudo firewall-cmd --permanent --add-rich-rule='rule service name=ssh limit value=10/m accept'
#sudo firewall-cmd --permanent --add-rich-rule='rule service name=cockpit limit value=10/m accept'

# Rate limit incoming dash node/masternode traffic to 100 requests/minute.
sudo firewall-cmd --permanent --add-rich-rule='rule service name=dashcore limit value=100/s accept'
#sudo firewall-cmd --permanent --add-rich-rule='rule service name=dashcore-testnet limit value=100/s accept'

# did it take?
sudo firewall-cmd --reload
sudo firewall-cmd --state
sudo firewall-cmd --list-all
```

_After you `--list-all`, if you see a service you do not wish to be available,
feel free to remove it following the pattern we demonstrated above._


**Some references:**

* FirewallD documentation: <https://fedoraproject.org/wiki/Firewalld>
* Rate limiting as we do above: <https://www.rootusers.com/how-to-use-firewalld-rich-rules-and-zones-for-filtering-and-nat/>
* More on rate limiting: <https://serverfault.com/questions/683671/is-there-a-way-to-rate-limit-connection-attempts-with-firewalld>
* And more: <https://itnotesandscribblings.blogspot.com/2014/08/firewalld-adding-services-and-direct.html>
* Interesting discussion on fighting DOS attacks on http: <https://www.certdepot.net/rhel7-mitigate-http-attacks/>
* Do some web searching for more about firewalld


&nbsp;

## ALL DONE!

If all went well, you have a working Dash Core Node that is working hard to help
secure the network by validating and propagating blocks and transactions.
Congratulations. I hope this was helpful.

Got a dash of feedback? *...har har...* Send it my way <https://keybase.io/toddwarner>    

&nbsp;

&nbsp;

---

# Appendix - Advanced Topics


## Email me when `dashd` starts or stops

SystemD makes it easy for your system to be configured to send you emails if
your masternode is rebooted, or systemd restarts dashd because it crashed, etc.

What takes a bit of doing is setting up your server to send emails in the first
place. That can be a bit tricky, but it is not rocket science. I wrote a whole
separate document on that here:
[Configure "send-only" Email via a 3rd Party SMTP Relay](https://github.com/taw00/howto/blob/master/howto-configure-send-only-email-via-smtp-relay.md)

Once sending email is set up on your server, configuring systemd to send notice
if dashd stops or starts is trivial.

* Edit `/etc/sysconfig/dashd`
* Configure these three settings: `EMAIL_FROM`, `EMAIL_TO`, `MASTERNODE_ALIAS`
  according to how your system is configured (see link above)

You can ultimately test the system by issuing a Masternode restart &mdash
`sudo systemctl restart dashd`. Folks are generally nervous about shutting down their
Masternodes unnecessarily and rightly so, but you will not be positive if your system truly
works without doing so. Just be aware that if you restart services, it may take
those emails a couple minutes to get to you (email is slow).

That's it. Not so hard, right?


## Email the admin when the Masternode's status changes from "ENABLED"

Not written yet. Stay tuned.


## Super fancy crontab settings

Remember to edit with `sudo -u dashcore crontab -e` if dashcore-sentinel is
installed with our RPM packages.

```
# Run Sentinel every minute; All messages are logged.
logfile=/var/log/dashcore/sentinel.log
* * * * * cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py >> $logfile 2>&1
```

```
# Run Sentinel every minute; dump COPIUS amounts of debug information to logfile
SENTINEL_DEBUG=1
logfile=/var/log/dashcore/sentinel.log
* * * * * cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py >> $logfile 2>&1
```

```
# Run Sentinel every minute; each run is time stamped in the logs
m0="----Sentinel job started --- pid:"
m1="----Sentinel job completed - pid:" # Not used in this example
t="%b %d %T UTC"
logfile=/var/log/dashcore/sentinel.log
* * * * * { cd /var/lib/dashcore/sentinel && date --utc +"$t $m0 $$" && venv/bin/python bin/sentinel.py ; } >> $logfile 2>&1
```


## Improve SSD Write & Delete Performance for Linux Systems by Enabling ATA TRIM

Because of the way SSDs (Solid State Drives) work, saving new data can impact performance. Namely, data marked as "deleted" have to be completely erased before write. With traditional magnetic drives, data marked for deletion is simply overwritten. Because SSDs have to take this extra step, performance can be impacted and slowly worsens over time.

If, on the other hand, you can alert the operating system that it needs to wipe deleted data in the background, writes (and deletes) can improve in performance.

To learn more, follow this link: <https://github.com/taw00/howto/blob/master/howto-enable-ssd-trim-for-linux.md>
