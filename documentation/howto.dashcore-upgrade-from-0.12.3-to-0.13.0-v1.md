# HowTo: Upgrade from Dash Core version 0.12.3 to 0.13.0

These instructions are specific to node, masternode, and wallet users running
the software on Fedora, ~~CentOS, or RHEL~~ (x86_64) plugged into the
~~`yum`~~ or `dnf` install and update process described in other documentation
found at <https://github.com/taw00/dashcore-rpm>. Dash Core builds for Fedora
27, RHEL7, or CentOS7 will no longer be available as of v0.13.0.

The process for upgrade of Dash Core is actually rather trivial, ***but it does
require attention to detail***. Read on...

> **BIG UGLY WARNING #1**<br />Because of the extremely dated version of cmake
> in Red Hat Enterprise Linux 7 (and CentOS 7), these platforms will no longer
> be supplied functional builds. EL8 is in beta at the moment, but won't be
> released until something like mid-May 2019. Until then, if you want to run a
> node or masternode, you will have to switch to Fedora. Fedora 29 is as stable
> as a rock though so... RECOMMEND!

> **WARNING #2**<br />If you are upgrading a Masternode, 0.13.0 will require a
> wallet-driven restart *and additonal configuration*, so time your upgrade to
> happen soon after your normal Masternode payout.

## The process

*Assumption1:<br />The operating system (OS) has already been upgraded or
installed to match an available version: Fedora 28 or 29 (x86_64).<br
/>The operating system upgrade process can be found
[here](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.upgrade-the-operating-system.md).*

*Assumption2:<br />You have installed the repository configuration RPM. If you have not done so already, do this:*

```
# Fedora...
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/dashcore-rpm/master/toddpkgs-dashcore-repo.fedora.rpm
sudo dnf list --refresh | grep dashcore
```

<!--
```
## CentOS/RHEL (NO LONGER SUPPORTED AS OF v0.13.0!)...
#sudo rpm --import https://keybase.io/toddwarner/key.asc
#sudo yum install -y https://raw.githubusercontent.com/taw00/dashcore-rpm/master/toddpkgs-dashcore-repo.el7.rpm
#sudo yum clean expire-cache
#sudo yum list | grep dashcore
```
-->

#### _...summary..._
* [0] Shut everything down
* [1] Back everything up
* [2] Update your repo configuration
* [3] Upgrade Dash Core binary packages from 0.12.3 to 0.13.0
* [4] Start everything back up
* [5] Masternodes only: Send start command from wallet to Masternode
* [6] Masternodes only: Deploy new v0.13 configurations to support Deterministic Masternode Lists
* [7] Monitor the configuration over time and adjust

<!-- TOC START min:3 max:3 link:true update:true -->
- [[0] Shut everything down](#0-shut-everything-down)
- [[1] Back everything up](#1-back-everything-up)
- [[2] Update your repo configuration - switch to the new "stable" repo](#2-update-your-repo-configuration---switch-to-the-new-stable-repo)
- [[3] Upgrade Dash Core binary packages](#3-upgrade-dash-core-binary-packages)
- [[4] Start everything back up](#4-start-everything-back-up)
- [[5] Generate NEW (as of 0.13) "BLS" public/private key-pair](#5-generate-new-as-of-013-bls-publicprivate-key-pair)
- [[6] Masternode upgrade only: Send start command from Wallet to Masternode](#6-masternode-upgrade-only-send-start-command-from-wallet-to-masternode)
- [[6] Masternode upgrades only:<br />Deploy new v0.13 configurations to support Deterministic Masternode Lists](#6-masternode-upgrades-onlydeploy-new-v013-configurations-to-support-deterministic-masternode-lists)
- [[7] Masternode upgrade in particular: Monitor your status](#7-masternode-upgrade-in-particular-monitor-your-status)
- [Good luck! Comments and Feedback...](#good-luck-comments-and-feedback)

<!-- TOC END -->

### [0] Shut everything down

* If running `dash-qt` (the graphical client program), in your menus choose "File" and then "Exit"
* If running `dashd` manually (not as a systemd service), then issue a shutdown with `dash-cli stop`
* If running `dashd` as a systemd service, then issue a shutdown command with `sudo systemctl stop dash`

### [1] Back everything up

Note: If you are just running a node with no funds associated, you don't really
need to back it up. If disaster strikes, you can just rebuild it. A masternode
can be similarly rebuilt, but a backup makes everything easier. And of course,
with a wallet, a backup is critical for ensuring your funds are protected.

The easiest way to back up your wallet is to shut it down and then copy any
configuration and wallet data files.

* Shut down -- You should have already done this in step [0]
* Open up a terminal
* Create a tar-archive (like zip, but better) of your configuration and wallet data files<br />
  _Note: If these are overly complicated for you, just be sure to copy `wallet.dat` and any `.conf` files somewhere and you will be fine._

*This is the general pattern of creating a backup tar-archive...*

Backing up, Scenario1: The dashd server is run as a systemd service:
```
sudo tar cvzf dash-backup-$(date +%F).tar.gz /etc/dashcore/dash.conf $(sudo find /var/lib/dashcore -name '*.conf' -or -name 'wallet.dat*')
```

&nbsp;

Backing up, Scenario2: The graphical client or dashd is run from the user's home directory:
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
* If you ever need to restore your wallet, node, or masternode, set up a new
  one and just like in the test, extract the archive but this time replace
  all the new setup's files with the ones from the archive.
* Store that "tarball" somewhere safe.
* Repeat to yourself: _"I should have been doing this all along!"_


### [2] Update your repo configuration - switch to the new "stable" repo

*On January 14, 2019:* The repository RPM (`toddpkgs-dashcore-repo`) will have
been updated to include the new "stable" repository that ships 0.13.0. It will
not automatically switch to that repository for you.

*On January 21, 2019:* The repository RPM (`toddpkgs-dashcore-repo`) will have
been updated to include the new "stable" repository that ships 0.13.0 **AND**
it will be configured to automatically switch you from the 0.12 repository to
the 0.13 repository.

```
# Fedora...
sudo dnf upgrade toddpkgs-dashcore-repo --refresh -y
sudo dnf list | grep dashcore
```
<!--
```
# CentOS/RHEL (NO LONGER SUPPORTED AS OF v0.13.0!)...
sudo yum clean expire-cache
sudo yum update toddpkgs-dashcore-repo -y
sudo yum list | grep dashcore
```
-->

If the above commands did not show 0.13.0 packages listed, do this:
```
sudo dnf config-manager --set-disabled dashcore-stable-12.3
sudo dnf config-manager --set-enabled dashcore-stable
sudo dnf list --refresh | grep dashcore
```

If the above commands did not show 0.13.0 packages listed, you probably manually
edited the repo configurations in the past and the new configurations are in a
`.rpmnew` file. Investigate your `/etc/yum.repos.d/` directory. If you find an
`.rpmnew` file or some such, manually move it with the `mv` command and then
repeat the "config-manager" instructions shown above. Still a problem? Then come
talk to me.


### [3] Upgrade Dash Core binary packages

```
# Fedora...
# Upgrade Dash Core and Sentinel
sudo dnf upgrade -y
```

<!--
```
## CentOS/RHEL (NO LONGER SUPPORTED AS OF v0.13.0!)...
## Upgrade Dash Core and Sentinel
#sudo yum update -y
```
-->

### [4] Start everything back up

#### If this is a GUI wallet - `dash-qt`

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

### [5] Generate NEW (as of 0.13) "BLS" public/private key-pair

Much of these instructions were taken from the excellent documentation found at dash.org: <https://docs.dash.org/en/stable/masternodes/dip3-upgrade.html#masternode-registration-from-dash-core>

As of version 0.13.0, a new signature mechanism is used to manage masternodes. It uses a cryptographic scheme we are calling [BLS signatures](https://en.wikipedia.org/wiki/Boneh%E2%80%93Lynn%E2%80%93Shacham).

Note: Both your wallet (if you installed the Dash Core wallet) and your Dash node (soon to be a masternode) include the ability to generate BLS keys. The keys are generated independently. I.e., it doesn't matter on which system you generate them.

For each of these examples, they are either executed in the debug console in the graphical Dash Core wallet software as shown or from the commandline and proceeded with the `dash-cli` command.

**Generate a BLS key-pair (example in wallet debug console)**
```
bls generate
{
  "secret": "565950700d7bdc6a9dbc9963920bc756551b02de6e4711eff9ba6d4af59c0101",
  "public": "01d2c43f022eeceaaf09532d84350feb49d7e72c183e56737c816076d0e803d4f86036bd4151160f5732ab4a461bd127"
}
```

Example using `dash-cli` on the commandline on a masternode (systemd configuration)...
```
sudo -u dashcore dash-cli bls generate
{
  "secret": "565950700d7bdc6a9dbc9963920bc756551b02de6e4711eff9ba6d4af59c0101",
  "public": "01d2c43f022eeceaaf09532d84350feb49d7e72c183e56737c816076d0e803d4f86036bd4151160f5732ab4a461bd127"
}
```

Example using `dash-cli` on the commandline on a masternode (dashd run as normal user configuration)...
```
dash-cli bls generate
{
  "secret": "565950700d7bdc6a9dbc9963920bc756551b02de6e4711eff9ba6d4af59c0101",
  "public": "01d2c43f022eeceaaf09532d84350feb49d7e72c183e56737c816076d0e803d4f86036bd4151160f5732ab4a461bd127"
}
```

**Store those keys somewhere safe**
These keys are not stored for you, per ce. Secure them in a safe place.

The "secret" key is used in the next step.

**Edit your Masternode's `dash.conf` and configure the `masternodeblsprivkey` setting**

If running your Masternode (dashd) as a normal user:
```
nano ~/.dashcore/dash.conf
```

If running your Masternode (dashd) configured as a systemd service:
```
sudo nano /etc/dashcore/dash.conf
```

Set the `masternodeblsprivkey` value in that file to the secret key as such:
```
masternodeblsprivkey=565950700d7bdc6a9dbc9963920bc756551b02de6e4711eff9ba6d4af59c0101
```



### [6] Masternode upgrade only: Send start command from Wallet to Masternode

*This only has to happen for major releases, like 0.12.3 to 0.13.0. You
usually don't have send the restart command for minor releases (eg. 0.13.0 to
0.13.1). The protocol change from 0.12.3 to 0.13.0 was `70210` to `70213`*

***You have to restart the Masternode from your collateralizing wallet. Here's
how...***

1. Ensure you have upgraded your wallet as well (IMPORTANT).
2. Open your wallet, you can either...
   * Masternode tab > right click on masternode > Start alias
   * Tools menu > Debug console > _masternode start-alias <MN Alias>_
   * From command line: _dash-cli masternode start-alias <MN Alias>_


### [6] Masternode upgrades only:<br />Deploy new v0.13 configurations to support Deterministic Masternode Lists

Follow these instructions (*"Software update"* is what you already just
performed, so please skip to section *"Generate BLS key pair"*):
<https://docs.dash.org/en/latest/masternodes/maintenance.html#generate-a-bls-key-pair>


### [7] Masternode upgrade in particular: Monitor your status

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
