# HowTo: Upgrade from Dash Core version 0.13 to 0.14

These instructions are specific to node, masternode, and wallet users running
the software on Fedora Linux (x86_64) plugged into the `dnf` install and update
process described in the documentation found at
<https://github.com/taw00/dashcore-rpm>. Dash Core builds for Fedora 27, RHEL7,
or CentOS7 are no longer be available as of v0.13, and Fedora 28 as of v0.14.

The process for upgrade of the Dash Core application software is rather trivial
compared to previous upgrades.

## The process

*Assumption1:<br />The operating system (OS) has already been upgraded or
installed to match an available version: Fedora 29 or 30 (x86_64).<br
/>The operating system upgrade process can be found
[here](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.upgrade-the-operating-system.md).*

*Assumption2:<br />You have installed the repository configuration RPM. If you have not done so already, do this:*

```
# Fedora...
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/dashcore-rpm/master/toddpkgs-dashcore-repo.fedora.rpm
sudo dnf list --refresh | grep dashcore
```

#### _...summary..._
<!-- TOC START min:3 max:3 link:true update:true -->
- [[0] Shut everything down](#0-shut-everything-down)
- [[1] Back everything up](#1-back-everything-up)
- [[2] Update your repo configuration - switch to the new "stable" repo](#2-update-your-repo-configuration---switch-to-the-new-stable-repo)
- [[3] Upgrade Dash Core binary packages](#3-upgrade-dash-core-binary-packages)
- [[4] Start everything back up](#4-start-everything-back-up)
- [[5] Masternodes: Monitor your status](#7-masternodes-monitor-your-status)
- [Good luck! Comments and Feedback...](#good-luck-comments-and-feedback)

<!-- TOC END -->

### [0] Shut everything down

- If running `dash-qt` (the graphical client application), in your menus choose
  "File" and then "Exit"
- If running `dashd` manually (not as a `systemd` service), then issue a
  shutdown with `dash-cli stop`
- If running `dashd` as a `systemd` service, then issue a shutdown command with
  `sudo systemctl stop dash`

### [1] Back everything up

Note: If you are just running a node with no funds associated, you don't really
need to back it up. If disaster strikes, you can just rebuild it. A masternode
can be similarly rebuilt, but a backup makes everything easier. And of course,
with a wallet, a backup is critical for ensuring your funds are protected.

The easiest way to back up your wallet is to shut it down and then copy any
configuration and wallet data files.

- Shut down -- You should have already done this in step [0]
- Open up a terminal
- Create a tar-archive (like zip, but better) of your configuration and wallet
  data files<br />
  _Note: If these are overly complicated for you, just be sure to copy `wallet.dat` and any `.conf` files somewhere and you will be fine._

_This is the general pattern of creating a backup tar-archive..._

**Backup Scenario1:** The dashd server is run as a systemd service:
```
sudo tar cvzf dash-backup-$(date +%F).tar.gz /etc/dashcore/dash.conf $(sudo find /var/lib/dashcore -name '*.conf' -or -name 'wallet.dat*')
```

&nbsp;

**Backup Scenario2:** The graphical client or dashd is run from the user's home directory:
```
cd ~
tar cvzf dash-backup-$(date -%F).tar.gz .dashcore/dash.conf $(find .dashcore/ -name '*.conf' -or -name 'wallet.dat*')
```

&nbsp;


Verify the integrity of your backup

```
mkdir x
cd x
cp ../dashcore-backup-*.tar.gz .
tar xvzf dashcore-backup-*.tar.gz
sha256sum wallet.dat /path/to/dash-data-directory/wallet.dat # The results should match
cd ..
rm -rf x
```
- If you ever need to restore your wallet, node, or masternode, set up a new
  one and just like in the test, extract the archive but this time replace
  all the new setup's files with the ones from the archive.
- Store that "tarball" somewhere safe.
- Repeat to yourself: _"I should have been doing this all along!"_


### [2] Update your repo configuration - switch to the new "stable" repo

*On May 22, 2019:* The repository RPM (`toddpkgs-dashcore-repo`) will have been
updated to include the new "stable" repository that ships 0.14. It **will**
automatically switch to that repository for you. It will because a MN restart
is not required. 0.13 to 0.14, unlike previous upgrades, operates more like a
point release.

```
# Fedora...
sudo dnf upgrade toddpkgs-dashcore-repo --refresh -y
sudo dnf list | grep dashcore
```

If the above commands did not show 0.14 packages listed, do this:
```
sudo dnf config-manager --set-disabled dashcore-stable-0.13
sudo dnf config-manager --set-enabled dashcore-stable
sudo dnf list --refresh | grep dashcore
```

If the above commands did not show 0.14 packages listed, you probably manually
edited the repo configurations in the past and the new configurations are in a
`.rpmnew` file. Investigate your `/etc/yum.repos.d/` directory. If you find an
`.rpmnew` file or some such, manually move it with the `mv` command and then
repeat the "config-manager" instructions shown above. Still a problem? Then come
talk to me.


### [3] Upgrade Dash Core binary packages

```
# Upgrade Dash Core and Sentinel
sudo dnf upgrade -y
```

### [4] Start everything back up

#### If this is the graphical wallet - `dash-qt`

Start it up via the desktop menuing system. It _might_ ask if you want to
re-index the blockchain. If it does, choose "YES". When complete, check your
balances.


#### If this is a node (or masternode) - `dashd`

Note: For the blockcount information below, it needs to match the current block
height as listed at <https://insight.dashevo.org/insight/> (or one of the
explorers listed at [here](https://docs.dash.org/en/stable/introduction/information.html?highlight=explorers#tools).
If you are using TESTNET, check out one of the explorers found
[here](https://docs.dash.org/en/stable/developers/testnet.html#explorers).


If running `dashd` as a normal user and not as a systemd managed service...
```
# Start the Dash Core server...
dashd # It will start and daemonize (give you the commandline prompt back)
# Watch the blockcount (CRTL-C to exit this loop)...
watch dash-cli getblockcount # CTRL-C to exit
# Watch the debug.log
tail -f ~/.dashcore/debug.log
```

If running node (or masternode) as a `systemd` managed service...
```
# Start dashd.service...
sudo systemctl start dashd
# Watch the blockcount (CRTL-C to exit this loop)...
watch sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore getblockcount
# Watch the debug.log...
sudo -u dashcore tail -f /var/lib/dashcore/debug.log
```

If this is a masternode...
```
# Check the results of `mnsync status`. If the status never syncs fully, you
# may have to perform a `mnsync reset`. Note that the syncing process can take
# 15 to 30 minutes.

# check status
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore masternode mnsync status

# reset sync - only if needed
#sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore masternode mnsync reset
```

### [5] Masternodes: Monitor your status

```
# On masternode (systemd managed in these examples)...
sudo systemctl status dashd
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore getnetworkinfo
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore mnsync status
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore masternode debug
sudo tail -f /var/log/dashcore/sentinel.log
sudo tail -f /var/log/dashcore/debug.log
```

```
# On collateralizing wallet (open Tools > Debug console)...
protx list
protx list valid
protx info "<value of 'protx list'>"
masternode list-conf
```


## Done.

It really isn't hard. It's all about attention to detail. If you mess up. Just
try again.

---

### Good luck! Comments and Feedback...

Got a dash of feedback? Send it my way: <https://keybase.io/toddwarner><br />
