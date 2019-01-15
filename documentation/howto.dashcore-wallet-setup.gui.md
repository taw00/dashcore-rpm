# HowTo: Install a Dash Core Wallet

> This edition of the document is for GUI versions of the Dash Core Wallet
(`dash-qt`).
>
> These instructions are specific to the Red Hat-family of linuxes.

> If you wish to use a hardware wallet instead (recommended)
and you are running Fedora Linux, install the `dash-masternode-tool` instead on
your workstation, and follow the guidelines found here:
<https://github.com/Bertrand256/dash-masternode-tool/blob/master/README.md>.

<!-- TOC START min:2 max:3 link:true update:true -->
- [[0] Install the operating system](#0-install-the-operating-system)
- [[1] Install the Dash Core Graphical Client and FirewallD](#1-install-the-dash-core-graphical-client-and-firewalld)
- [[2] Configure firewall rules to better secure your wallet](#2-configure-firewall-rules-to-better-secure-your-wallet)
- [[3] Create and edit your `dash.conf` configuration file](#3-create-and-edit-your-dashconf-configuration-file)
  - [Change your RPC (remote procedure call username and password)](#change-your-rpc-remote-procedure-call-username-and-password)
- [[4] Run the Dash Core Graphical Wallet client](#4-run-the-dash-core-graphical-wallet-client)
- [[5] BACKUP YOUR WALLET](#5-backup-your-wallet)
  - [Encrypt your wallet...](#encrypt-your-wallet)
  - [Backup your wallet...](#backup-your-wallet)
  - [Store your wallet somewhere securely](#store-your-wallet-somewhere-securely)
- [All done!](#all-done)

<!-- TOC END -->

## [0] Install the operating system

I leave it as an exercise for the reader to install Fedora Linux. For Fedora,
go here - https://getfedora.org/ I recommend the "Workstation" install.

<!-- For CentOS, go here - https://www.centos.org/download/ -->

***Sudoers access...***

As you walk through the operating system installation wizard, you will be asked
to create a normal user on the system. Do that. The wizard will also ask you if
you want to allow this user to have system admin rights. You need to do that as
well. Otherwise, you have to add those rights after the fact.

To add sudo (admin) rights after the fact (didn't make the choice during OS
installation, do this (the username in this example is `mnwalletuser`)...

```
# Log into the system as root user.
# If the user does not exist, do this...
useradd -G wheel mnwalletuser
passwd mnwalletuser

# If the user does exist, do this...
usermod -a -G wheel mnwalletuser
```

Once the operating system is installed, log onto the system as a normal user
(not root), update the system, and reboot:

```
sudo dnf upgrade -y
sudo reboot
```

<!--
...if this is CentOS or Red Hat Enterprise Linux

```
sudo yum install -y epel-release
sudo yum update -y
sudo reboot
```
-->

## [1] Install the Dash Core Graphical Client and FirewallD

Log onto the system as a normal user (not root), install the Dash Core wallet and the firewalld service:

```bash
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/dashcore-rpm/master/toddpkgs-dashcore-repo.fedora.rpm
sudo dnf install -y dashcore-client firewalld
```

<!--
```
#sudo dnf config-manager --set-disabled dashcore-stable
#sudo dnf config-manager --set-enabled dashcore-testing
```
-->

<!--
...if using CentOS or RHEL

Note: You have to first ensure you have the EPEL repositories configured:
`sudo yum repolist enabled`  
If you do not, browse to the
[EPEL community page](https://fedoraproject.org/wiki/EPEL) and follow their
installation instructions (it's easy).

Then...

```bash
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo yum install -y https://raw.githubusercontent.com/taw00/dashcore-rpm/master/toddpkgs-dashcore-repo.el7.rpm
sudo yum install -y dashcore-client firewalld
```
-->
<!--
```
#sudo yum-config-manager --disable dashcore-stable
#sudo yum-config-manager --enable dashcore-testing
```
-->


## [2] Configure firewall rules to better secure your wallet

You are about to transfer 1000 DASH to your wallet. That's a lot of money. You want to both save and backup your wallet, but also reduce the odds of someone hacking into your system.

You can glean a lot of information by reviewing the instructions in
[howto.dashcore-node-security.md](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.dashcore-node-security.md),
or just take these steps here. It's recommended that you review that document
and perhaps implement some of the additional suggestions it provides.

> _Note: Firewall rules can be a complicated topic. These are bare bones
> git-er-done instructions. You may want to investigate further refinement. This
> will get you started though._


```
# Is firewalld running?
# Turn on and enable firewalld if not already done...
sudo firewall-cmd --state
sudo systemctl start firewalld.service
sudo systemctl enable firewalld.service

# Determine what the default zone is.
# On vultr, for example, the default zone is FedoraWorkstation (it is the
# assumption for this example)
sudo firewall-cmd --get-active-zone

# FedoraWorkstation usually starts with ssh, dhcp6-client, and samba-client opened up
# Review your needs, but I don't want samba-client enabled and I want to
# rate limit ssh traffic
sudo firewall-cmd --permanent --add-service ssh
sudo firewall-cmd --permanent --remove-service samba-client

# Rate limit incoming ssh traffic to 10 per minute
sudo firewall-cmd --permanent --add-rich-rule='rule service name=ssh limit value=10/m accept'

# did it take?
sudo firewall-cmd --reload
sudo firewall-cmd --state
sudo firewall-cmd --list-all
```

_After you `--list-all`, if you see a service you do not wish to be available,
feel free to remove it following the pattern we demonstrated above._


## [3] Create and edit your `dash.conf` configuration file

Create a `.dashcore` directory, edit the `dash.conf` configuration (text) file.
A good default editor is `nano`, or you can use `gedit` if it install, or
whatever you are familiar with.

```
cd ~
mkdir .dashcore
nano ~/.dashcore/dash.conf
```

Cut-n-paste this template...
```
# This is a Masternode Collateral-bearing Wallet configuration file
# Run on the test network (testnet=1) or the main network (testnet=0)
testnet=0
# Run dashd as a daemon (in the background) - only relevant for advanced users
#daemon=1
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
```

Choose whether you are running on the testnet or not and alter the setting
above as necessary. If you are planning to work with real money and/or run a
production, mainnet masternode, that setting needs to be `testnet=0`.

### Change your RPC (remote procedure call username and password)

Edit `/etc/dashcore/dash.conf` and change...

```
rpcuser=<make_up_an_alphanumeric_username>
rpcpassword=<make_up_an_alphanumeric_password>
```
...to something else (these are examples)...
```
rpcuser=rpc_user_9084042423423
rpcpassword=this_is_a_random_password_98u22n982nf98562334n329vmasdfg
```
These are used by your on-system, internal commandline tools for the most part,
so you don't have to memorize them or use them outside of this wallet.


## [4] Run the Dash Core Graphical Wallet client

Click through your menus and click on the Dash icon, or start it directly from
the commandline...

```
dash-qt
```

> Hint! If you are running on the testnet, the initial splash screen will be
> orange themed. If you are running on the mainnet, the initial splash screen
> will be blue themed.


***Wait for everything to sync completely***

Once sync'ed, your wallet is then ready for the next steps. This can take
awhile.


## [5] BACKUP YOUR WALLET

### Encrypt your wallet...

Don't put this off. Do it.

* Navigate the menus: Settings > Encrypt wallet
* Set the password
* Write that password down on two pieces of paper and store them somewhere
  securely. A firebox is one good option.

### Backup your wallet...

* Navigate the menus: File > Backup Wallet

You'll be asked to pick a name for the backup file and where to save it. Call
it what you will, `my-dash-wallet.dat` is an example.

### Store your wallet somewhere securely

Personally, I would copy that to two different USB keys and throw them in a
firebox. Maybe even two different fireboxes. Again. This is a lot of money.
Don't skimp on your safety practices.


## All done!

You now have a functioning wallet ready to send and receive payment and maybe
even serve as a collateralization agent for a masternode.

***Comments and Feedback...***

Got a dash of feedback? Send it my way: <https://keybase.io/toddwarner>
