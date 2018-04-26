# HowTo: Upgrade from Dash Core version 12.1 to 12.2

> These instructions are specific to node, masternode, and wallet users running
> the software on Fedora, CentOS, or RHEL plugged into the `yum` or `dnf`
> install and update process described in other documentation found at
> <https://github.com/taw00/dashcore-rpm>.

The process for upgrade is actually rather trivial. You may also want to review
the dash.org official documentation found here:
<https://dashpay.atlassian.net/wiki/spaces/DOC/pages/124092516/Dash+v12.2+-+2017-11-07>

**WARNING: If you are upgrading a Masternode, it will require a wallet-driven
restart due to a protocol bump, so time your upgrade to happen soon after your
normal Masternode payout.**

## The process

#### _...summary..._
* Shut everything down
* Back everything up
* Upgrade Dash Core binary packages from 12.1 to 12.2
* Start everything back up
* Send start command from wallet to Masternode (Masternodes only)
* Monitor the configuration over time and adjust

### [0] Shut everything down

* If running `dash-qt`, in your menus choose "File" and then "Exit"
* If running `dashd`, then issue a shutdown with `dash-cli stop`
* If running `dashd` as a systemd service, then issue a shutdown command with `systemctl stop dash`

### [1] Back everything up

Note: If you are just running a node with no funds associated, you don't really need to back it up. If disaster strikes, you can just rebuild it. A masternode can be similarly rebuilt, but a backup makes everything easier. And of course, with a wallet, a backup is critical for ensuring your funds are protected.

The easiest way to back up your wallet is to shut it down and then copy any configuration and wallet data files.

* Shut down your dash-qt or dashd -- You should have already done this
* Open up a terminal
* Create a tar-archive of your configuration and wallet data files<br />
  _Note: If these are overly complicated for you, just be sure to copy `wallet.dat` and any `.conf` files somewhere and you will be fine._

This is the general scheme...
```
sudo tar cvzf dash-backup-$(date +%F).tar.gz /path/to/dash.conf $(find /path/to/dash-data-directory -name '*.conf' -or -name 'wallet.dat*')
```

Scenario: Running dash as a `systemd` service...
```
sudo tar cvzf dashcore-backup-$(date +%F).tar.gz /etc/dashcore/dash.conf $(find /var/lib/dashcore -name '*.conf' -or -name 'wallet.dat*')
```

Scenario: Running dash from your home directory...
```
tar cvzf dashcore-backup-$(date +%F).tar.gz $(find ~/.dashcore  -name '*.conf' -or -name 'wallet.dat*')
```

* Test your backup
```
mkdir x
cd x
cp ../dashcore-backup-*.tar.gz .
tar xvzf dashcore-backup-*.tar.gz
sha256sum wallet.dat /path/to/dash-data-directory/wallet.dat # The results should match
cd ..
rm -rf x
```
* If you ever need to restore your wallet, node, or masternode, set up a new
  one and just like in the test, extract the archive but this time replace
  all the new setup's files with the ones from the archive.
* Store that "tarball" somewhere safe.
* Repeat to yourself: _"I should have been doing this anyway!"_


### [2] Upgrade Dash Core binary packages

*...if using Fedora:*
```
# Update your DNF/YUM repository configuration file:
cd /etc/yum.repos.d/
sudo curl -O https://raw.githubusercontent.com/taw00/dashcore-rpm/master/dashcore-fedora.repo
cd -
# Upgrade Dash Core and Sentinel
sudo dnf upgrade -y
```

*...if using CentOS or RHEL*
```
# Update your YUM repository configuration file:
cd /etc/yum.repos.d/
sudo curl -O https://raw.githubusercontent.com/taw00/dashcore-rpm/master/dashcore-centos.repo
cd -
# Upgrade Dash Core and Sentinel
sudo yum update -y
```


### [3] Start everything back up

#### If this is a GUI wallet - `dash-qt`

Start it up via the desktop menuing system. It _might_ ask if you want to
re-index the blockchain. If it does, choose "YES". When complete, check your
balances.


#### If this is a node (or masternode) - `dashd`

Note: For the blockcount information below, it needs to match the current block
height as listed at <https://explorer.dash.org>.


If running `dashd` as a normal user and not as a systemd managed service...
```
# Start Dash 12.2:
dashd # It will start and daemonize (give you the commandline prompt back)
# Watch the blockcount (CRTL-C to exit this loop)...
watch dash-cli getblockcount # CTRL-C to exit
# Watch the debug.log
tail -f ~/.dashcore/debug.log
```

If running node (or masternode) as a `systemd` service...
```
# Start dashd
sudo systemctl start dashd
# Watch the blockcount (CRTL-C to exit this loop)...
watch sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf getblockcount
# Watch the debug.log
sudo -u dashcore tail -f /var/lib/dashcore/debug.log
```

If this is a masternode...
```
# Check the results of `mnsync status`. If the status never # syncs fully, you
# may have to perform a `mnsync reset`. Note that the syncing process can take 15
# to 30 minutes.
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf masternode mnsync reset
```

### [4] Masternode upgrade only: Send start command from Wallet to Masternode

***WARNING: Upgrade after a Masternode payout. You have to restart the
Masternode from your collateralizing wallet. Here's how...***

1. Ensure you have upgraded your wallet as well.
2. Open your wallet, you can either...
   * Masternode tab > right click on masternode > Start alias
   * Tools menu > Debug console > _masternode start <MN Alias>_
   * From command line: _dash-cli masternode start <MN Alias>_  ---TODO: Need to test this. 

### Masternode upgrade in particular: Monitor your status

```
# For systemd run masternodes...
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore getinfo
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore mnsync status
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore masternode debug
```



## Done.

It really isn't hard. If you read through this once or twice, you kinda get
what we are doing: _Update the RPM packages, restart everything._ Easy peasy.
If you foul everything up. Just try again.

More configuration. At your convenient, you really should ensure your firewall
rules are rechecked (see `howto.secure-your-dash-masternode.md`).

---

### Good luck! Comments and Feedback...

Got a dash of feedback? Send it my way: <https://keybase.io/toddwarner><br />
