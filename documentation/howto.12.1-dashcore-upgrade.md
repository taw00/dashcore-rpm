# HowTo: Upgrade from Dash Core version 12.0 to 12.1

> These instructions are specific to node, masternode, and wallet users running
> the software on Fedora, CentOS, or RHEL plugged into the `yum` or `dnf`
> install and update process described in other documentation found at
> <https://github.com/taw00/dashcore-rpm>.

The process for upgrade is actually rather trivial. But it is recommended that
you, especially masternode owners, get a testnet version running first as
closely configured to your production masternode as possible on a separate
system.

## The process

* Shut everything down
* Back everything up
* Enable new dashcore repository
* Upgrade Dash Core binaries from 12.0 to 12.1
* Verify configuration and start
  * Wallet...
    - Start wallet, and check balances
  * Node
    - Start node, and verify blockcount and operation
  * Masternode
    - Upgrade both your collateral-bearing wallet    
      and your masternode (see wallet and node upgrade steps)
    - Configure Sentinel
    - Issue masternode start command from wallet
    - Verify blockcounts, mnsync status, and ENABLE flag
* Monitor the configuration over time and adjust

### [0] Shut everything down

If running `dash-qt`, in your menus choose "File" and then "Exit"    
If running `dashd`, then issue a shutdown with `dash-cli stop`    
If running `dashd` as a systemd service (unlikely with version 12.0), then issue a shutdown command with `systemctl stop dash`

### [1] Backup everything up

Note: If you are just running a node with no funds associated, you don't really need to back it up. If disaster strikes, you can just rebuild it. A masternode can be similarly rebuilt, but a backup makes everything easier. And of course, with a wallet, a backup is critical for ensuring your funds are protected.

The easiest way to back up your wallet is to shut it down and then copy any configuration and wallet data files.

* Shut down your dash-qt or dashd -- You should have already done this
* Open up a terminal
* Create a tar-archive of your configuration and wallet data files

```
sudo tar cvzf dash-backup-$(date +%F).tar.gz /path/to/dash.conf $(find /path/to/dash-data-directory -name '*.conf' -or -name 'wallet.dat*')
```

For some that command may look just like this...
```
sudo tar cvzf dash-backup-$(date +%F).tar.gz /etc/dash/dash.conf $(find /var/lib/dash -name '*.conf' -or -name 'wallet.dat*')
```

For others, maybe...

```
tar cvzf dash-backup-$(date +%F).tar.gz $(find ~/.dash  -name '*.conf' -or -name 'wallet.dat*')
```

* Test your backup
```
mkdir x
cd x
cp ../dash-backup-*.tar.gz .
tar xvzf dash-backup-*.tar.gz
sha256sum wallet.dat /path/to/dash-data-directory/wallet.dat # The results should match
cd ..
rm -rf x
```
* If you ever need to restore your wallet, node, or masternode, set up a new
  one and just like in the test, extract the archive but this time replace
  all the new setup's files with the ones from the archive.
* Store that "tarball" somewhere safe.
* Repeat to yourself: _"I should have been doing this anyway!"_


### [2] Enable new dashcore repository

With Dash Core 12.1 we are moving to the Fedora COPR build system for delivery
of packaging in the future. To enable the new repository, just replace the
repository configuration file.


If you are running Fedora Linux...
```
cd /etc/yum.repos.d/
sudo curl -O https://raw.githubusercontent.com/taw00/dashcore-12.1/master/dashcore-fedora.repo
```

If you are running CentOS or Red Hat Enterprise Linux
```
cd /etc/yum.repos.d/
sudo curl -O https://raw.githubusercontent.com/taw00/dashcore-12.1/master/dashcore-centos.repo
```

Note, if you are familiar with COPR, you can use their process if you like.
Just browse to <https://copr.fedorainfracloud.org/coprs/taw/dashcore-12.1/> and
follow the enablement instructions.


### [3] Upgrade Dash Core binaries from 12.0 to 12.1

If you are running Fedora Linux...
```
sudo dnf upgrade -y
# Your system should upgrade all packages to include Dash Core
sudo reboot
```

If you are running CentOS or Red Hat Enterprise Linux
```
sudo yum update -y
# Your system should upgrade all packages to include Dash Core
sudo reboot
```


### [4] Move everything from old directory trees to new and remove cache data

The default data directory trees changed for 12.1

|                       | dash.conf               | data directory    |
|-----------------------|-------------------------|-------------------|
|12.0                   | ~/.dash/dash.conf       | ~/.dash           |
|-----------------------|-------------------------|-------------------|
|12.1 (systemd service) | /etc/dashcore/dash.conf | /var/lib/dashcore |
|12.1 run by user       | ~/.dashcore/dash.conf   | ~/.dashcore       |
|-----------------------|-------------------------|-------------------|


If your data directory was in `~/.dash`, do this...
```
cd ~
# Does .dashcore exist? It shouldn't. Did you run Dash too soon?
file .dashcore
rm -rf .dashcore
mv .dash .dashcore
# remove old data caches
cd .dashcore
sudo rm -f budget.dat debug.log fee_estimates.dat mncache.dat mnpayments.dat peers.dat
cd -
```

If not a GUI wallet you are configuring and you set up `dashd` as a systemd
service, your data directory probably resided in `/var/lib/dash`. With 12.1, we
_will_ have a `/var/lib/dashcore` created for you, owned by the `dashcore`
system user.
```
sudo cp /var/lib/dash/* /var/lib/dashcore/*
sudo mv /etc/dashcore/dash.conf /etc/dashcore/dash.conf.installed-by-rpm
sudo cp /path/to/dash.conf /etc/dashcore/dash.conf
chown dashcore:dashcore -R /etc/dashcore /var/lib/dashcore
```


### [5] Verify configuration and start

#### If this is a GUI wallet - `dash-qt`

Start it up via the desktop menuing system and check your balances.

#### If this is a node - `dashd`

Note: For the blockcount information below, it needs to match the current block
height as listed at <https://explorer.dash.org>.

If running as a normal user and not as a `systemd` service...
```
# Start Dash Core 12.1...
dashd # It will start and daemonize (give you the commandline prompt back)
# Watch the blockcount (CRTL-C to exit this loop)...
watch dash-cli getblockcount # CTRL-C to exit
# Watch the debug.log
tail -f ~/.dash/debug.log
```

If running node as a `systemd` service...
```
# Become root user
sudo su -
# Start Dash Core 12.1...
systemctl start dashd
# Watch the blockcount (CRTL-C to exit this loop)...
watch sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf getblockcount
# Watch the debug.log
tail -f /var/lib/dashcore/debug.log
```

#### If that node is also a masternode - `dashd`

Do all of the above. But also...


Start Dash Sentinel
```
# Become root user
sudo su -
# Edit dashcore's crontab - remove EDITOR="nano" if you work fine with vi
sudo -u dashcore EDITOR="nano" crontab -e
# ..and add this line...
*/5 * * * * cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py >/dev/null 2>&1
```

Start the masternode from the collateral-bearing wallet (that you have also
already upgraded) and watch the masternode record until the masternode becomes
"ENABLED" ... might take up to 15 minutes.
```
dash-cli start-alias <MASTERNODE_ALIAS>
# CTRL-C to exit this loop
dash-cli masternode list full |grep <IP ADDRESS OF THE MASTERNODE>
```

On the masternode, check the results of `mnsync status`. You may have to
perform a `mnsync reset`.
```
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf masternode mnsync reset
```


## Done.

It really isn't hard. If you read through this once or twice, you kinda get
what we are doing: _Update the RPM packages, copy over the data directories,
remove the old cache files, maybe move some things around, set up Sentinel if
you are a masternode and start everything up._ Easy peasy. If you foul
everything up. Just try again.

More configuration. At your convenient, you really should ensure your firewall
rules are rechecked (see `howto.secure-your-dash-masternode.md`).

## Good luck

Got a dash of feedback? *...har har...* Send it my way <t0dd@protonmail.com>    
