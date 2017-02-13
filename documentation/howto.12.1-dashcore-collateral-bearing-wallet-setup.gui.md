# HowTo: v12.1 Dash Wallet as Collateral Holding Agent for a Dash Masternode
# ...on Fedora, CentOS or Red Hat Enterprise Linux

> This edition of the document is for GUI versions of the Dash Core Wallet (`dash-qt`).
>
> These instructions are specific to the Red Hat-family of linuxes.

## Masternode?

For a general overview of Dash Masternode setup, please refer to the overview document found
[here](https://github.com/taw00/dashcore-rpm/blob/master/documentation/README.md).

This document chronicals the first step in the process: Setting up a
collateral-bearing dash wallet. This document describes one way of doing it. There are other ways, but we will focus on simplicity here.

Once you complete all the steps in this document, you may continue with the to the masternode setup process. Refer to the masternode setup guide referenced in the overview document above.

## [0] Install the operating system

I leave it as an excercise for the reader to install Fedora, CentOS, or even
RHEL. For Fedora, go here - https://getfedora.org/ For CentOS, go here -
https://www.centos.org/download/ For Fedora, I recommend the "Workstation"
install.

As you walk through the installation wizard, you will be asked to create a
normal user on the system. Do that. The wizard will also ask you if you want to
allow this user to have system admin rights. You need to do that as well.
Otherwise, you have to add those rights after the fact. Like this (the username
in this example is `mnwalletuser`)...

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

...if this is Fedora

```
sudo dnf upgrade -y
sudo reboot
```

...if this is CentOS or Red Hat Enterprise Linux

```
sudo yum install -y epel-release
sudo yum update -y
sudo reboot
```

## [1] Install the Dash Core GUI Client and FirewallD

Log onto the system as a normal user (not root), install the Dash wallet:

...if using Fedora:

```
cd /etc/yum.repos.d/
sudo curl -O  https://raw.githubusercontent.com/taw00/dashcore-rpm/master/dashcore-fedora.repo
cd -
sudo dnf install -y dashcore-client firewalld
```

<!--
```
#sudo dnf config-manager --set-disabled dashcore-stable
#sudo dnf config-manager --set-enabled dashcore-unstable
```
-->


...if using CentOS or RHEL

```
cd /etc/yum.repos.d/
sudo curl -O  https://raw.githubusercontent.com/taw00/dashcore-rpm/master/dashcore-centos.repo
cd -
sudo yum install -y dashcore-client firewalld
```
<!--
```
#sudo yum-config-manager --disable dashcore-stable
#sudo yum-config-manager --enable dashcore-unstable
```
-->


## [2] Configure firewall rules to better secure your wallet

You are about to transfer 1000 DASH to your wallet. That's a lot of money. You want to both save and backup your wallet, but also reduce the odds of someone hacking into your system.

You can glean a lot of information by reviewing the instruction in
[howto.secure-your-dash-masternode.md](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.secure-your-dash-masternode.md),
or just take these steps here. It's recommended that you review that document
and perhaps implement some of the additional suggestions it may provide.

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
# On vultr, for example, the default zone is FedoraWorkstation (it is the
# assumption for this example)
sudo firewall-cmd --get-active-zone

# FedoraWorkstation usually starts with ssh, dhcp6-client, and samba-client opened up
# Review your needs, but I don't want samba-client enabled and I want to
# rate limit ssh traffic
sudo firewall-cmd --permanent --zone=FedoraServer --add-service ssh
sudo firewall-cmd --permanent --zone=FedoraServer --remove-service samba-client

# Rate limit incoming ssh traffic to 10 per minute
sudo firewall-cmd --permanent --add-rich-rule='rule service name=ssh limit value=10/m accept'

# did it take?
sudo firewall-cmd --reload
sudo firewall-cmd --state
sudo firewall-cmd --list-all
```



## [2] Create and edit your `dash.conf` configuration file

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
above as necessary. If you are planning to work with real money and run a
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


## [4] Run the Dash Core GUI Wallet

Click through your menus and click on the Dash icon, or right this from the
commandline...

```
dash-qt
```

> Hint! If you are running on the testnet, the initial splash screen will be
> orange themed. If you are running on the mainnet, the initial splash screen
> will be blue themed.


### **Wait for everything to sync completely**

Once sync'ed your wallet is then ready for the next steps. This can take awhile.


## [5] Send 1000 Dash to the wallet

### Get the receiving address

From your GUI wallet interface do this...

* Navigate the menus: Tools > Debug console
* Enter in that dialogue: `getnewaddress`
* After you hit enter, you should get a new address listed.
  - For testnet, it will begin with a "y", example: `yMArVugC51J6WRkAVJpAwi2x6ecr4xvazH`
  - For mainnet, it will begin with a "X", example: `XMArVugC51J6WRkAVJpAwi2x6ecr4xvazH`

You can do the same thing from the commandline with the `dash-cli` interface: `dash-cli getnewaddress`

### Send the 1000 DASH

From whatever other source has that 1000 Dash, send precisely 1000 Dash (or
tDash if this is testnet) to that address. Important. It has to be precisely
1000 Dash; fees must be accounted for.

If you need tDash for testnet testing purposes, have it sent from
https://test.faucet.dash.org/


## [6] SAVE YOUR WALLET

### Consider encrypting your wallet...

* Navigate the menus: Settings > Encrypt wallet
* Set the password

### Backup your wallet...

* Navigate the menus: File > Backup Wallet

You'll be asked to pick a name for the backup file and where to save it. Call
it what you will, `my-masternode-collateral-wallet.dat` is an example.

### Store your wallet somewhere securely

Personally, I would copy that to two different USB keys and throw them in a
firebox. Maybe even two different fireboxes. Again. This is a lot of money.
Don't skimp on your safety practices.


## [7] Generate Masternode private key (a key that only the masternode and the wallet share)

From your GUI wallet interface do this...

* Navigate the menus: Tools > Debug console
* Enter in that dialogue: `masternode genkey`
* After you hit enter, it will look something like this: `92yZY5b8bYD5G2Qh1C7Un6Tf3TG3mH4LUZha2rdj3QUDGHNg4W9`

Or from the commandline: `dash-cli masternode genkey`

Record this in some scratchpad somewhere, you will need it when you set up your
masternode


## [8] Get your funding transaction ID and index for that 1000 DASH transfer

From your GUI wallet interface do this...

* Navigate the menus: Tools > Debug console
* Enter in that dialogue: `masternode outputs`

Or from the commandline: `dash-cli masternode outputs`

You'll get a transaction ID and index value (usually a 1 or a 0). Record these.
You will need these values. They will look something like this (these are
examples):

`b34ad623453453456423454643541325c98d2f8b7a967551f31dd7cefdd67457 1`

Record this in some scratchpad somewhere, you will need it when you set up your
masternode


## [9] Configured your `masternode.conf`

The wallet needs to know what masternode it is communicating with and needs to
be able to send proof of that 1000 DASH (or tDASH) to the network. It does this
with a properly configured `masternode.conf` file.

This file is located in...

* ~/.dashcore/ if operating on the mainnet
* ~/.dashcore/testnet3/ if operating on the testnettestnet

If you are using the testnet that `testnet3` directory should have been created for you when you started your GUI wallet.

### Edit `masternode.conf` (again use `nano` or some other text editor)

```
nano ~/.dashcore/masternoode.conf # if mainnet
# ...or...
nano ~/.dashcore/testnet3/masternode.conf # if testnet
```

Pick an alias for your masternode. It can be anything. It's a label in this
configuration file that is used in reference to the masternode by the wallet
when communicating with the masternode. Since this is our first masternode, I
labled it `mn1`. But if could be `bob` or `my_masternode` or whatever you want.

**Note 1: I filled in the masternode private key, the funding transaction ID
and the funding index from the values received earlier. The IP address will be
added later after I set up the masternode. _These are examples only!_**

**Note 2: The port is set to 9999 for mainnet and 19999 for testnet.**

Fill in this template and save the file...
```
# add the following line to the end of the conf, replacing your values from above
# ALIAS <externalip>:<PORT> <masternodeprivkey> <funding_txid> <funding_index>
# it should look something like this (9999 for live net, and 19999 for testnet)
mn1 110.111.112.113:9999 92yZY5b8bYD5G2Qh1C7Un6Tf3TG3mH4LUZha2rdj3QUDGHNg4W9 b34ad623453453456423454643541325c98d2f8b7a967551f31dd7cefdd67457 1
```


## All (mostly) done!

You have a functioning wallet set up with 1000 DASH or tDASH ready to serve as
the collateralizing agent for a masternode.

Next steps to completion are...

1. Set up your masternode
2. Configure your masternode with wallet identifying information
3. Configure your wallet with the masternode IP address
4. Start your masternode server as a full node
5. Use your wallet to tell the full node it is really a masternode
6. Configure Sentinel

These steps are covered in another set of documents

Got a dash of feedback? *...har har...* Send it my way <t0dd@protonmail.com>    
And of course, donations welcome: [XyxQq4qgp9B53QWQgSqSxJb4xddhzk5Zhh](dash:XyxQq4qgp9B53QWQgSqSxJb4xddhzk5Zhh)
