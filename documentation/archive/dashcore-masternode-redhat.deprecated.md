----


# Deprecated

#### Please visit...<br /><https://github.com/taw00/dashcore-rpm> for new documentation efforts. In particular, as of this writing,<br /><https://github.com/taw00/dashcore-rpm/blob/master/documentation/overview.12.1-dashcore-masternode-setup.md><br />...for current and updated documenation.

----

# Dash Core Masternode Installation and Configuration on Fedora, CentOS or RHEL<br />v12.1 Testnet Edition

**These instructions are explicitly written for the Testnet environment and
blockchain.**

This document will guide you through the setup process for the two systems
required to operate a Dash Masternode: The masternode and the wallet. These
instructions are explicitly written for those who want to run these services on
Fedora, CentOS, or Red Hat Enterprise Linux (RHEL).

> What is Dash? [dash.org](https://dash.org/), [official documentation](https://dashpay.atlassian.net/wiki/display/DOC/Official+Documentation)<br />
> What is a Masternode? <https://dashpay.atlassian.net/wiki/display/DOC/Masternode><br />
What are these Linuxes? [Fedora](https://getfedora.org/), [CentOS](https://www.centos.org/), [RHEL](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux)

----

***Acknowledgments***    
*A number of other guides contributed to this one. In particular,
[moocowmoo's](https://gist.github.com/moocowmoo/66049a781f8eaa1021306072f19363d4)
and [nmarley's](https://github.com/nmarley/sentinel/blob/master/README.md) and
others. Also check out [this
one](https://github.com/dashcommunity/guides/blob/master/set_up_masternode.md)
from the [Dash Community](https://dashcommunity.github.io/) github page and the
[general masternode
section](https://dashpay.atlassian.net/wiki/display/DOC/Masternode) of the Dash
wiki. If you are looking for general testnet documentation, start
[here](https://dashpay.atlassian.net/wiki/display/DOC/Testnet).*

***"I'm not tech savvy! Help!"***    
*There are a number of services that will remove the headaches of managing a
masternode yourself, host one for you, and walk you through the process of
getting set up. [Here is a
listing](https://dashpay.atlassian.net/wiki/pages/viewpage.action?pageId=1867885)
of the current providers recommended by the Dash community.*

***"I'm ready to get my hands dirty!"*** Okay, then, let's get started...

----

### Document Conventions

For this document, I will use the shorthand **[Mn]** when referring to the
server that houses the masternode and sentinel servers, and **[W]** when
referring to the system where the wallet resides. When setting things up That
should help you best understand which machine you are working on at the moment
when walking through this document.

### Platforms

These instructions use version 12.1 of Dash Core on Fedora Linux, CentOS, or
RHEL. Binary packages can be found at the dnf/yum repositories
[here](https://toddwarner.keybase.pub/repo/dashcore/). **But, you don't need to
download anything. Let the package manager do the work for you. Read on!**

These instructions should work for all supported linuxes found at the link
above. As of this writing that is Fedora Linux 24 and 25, CentOS 7, and RHEL 7.
I did most of my testing on Fedora 24. I tested with the masternode running on a
local virtual instance as well as a VPS cloud instance.

### OS Requirements

You will be setting up two linux systems. One for the masternode and sentinel
server, the other for the supporting wallet that contains the 1000 tDash
collateral.

**[Mn] OS requirements for the masternode and sentinel server:**

* *Minimal* Linux OS installed: Fedora, CentOS, or RHEL
* git
* python-virtualenv
* firewalld
* dashcore repo configuration file

***Assumptions:***

 * `mn0` is the username on the masternode server used as an example throughout

**[W] OS requirements for the wallet**

***Why do we need a wallet?*** It holds the 1000 tDash (t=TEST) collateral
supporting the masternode. It serves not only to hold that collateral, but also
to interact with and activate the masternode server.

 * Linux OS installed: Fedora, CentOS, or RHEL
 * dashcore repo configuration file
 * Optional: Xorg and QT and whole GUI environment (if running graphical wallet
   client - out of scope for this instruction)

***Assumptions:***

* `mnwallet` is the username on the wallet server used as an example throughout

# Summary of the Steps

1. Linux: Set up your two linux systems.    
One for the masternode and sentinel server, and one for the collateral-holding wallet.
2. Masternode Server: Initial install and configuration
3. Masternode Server: Firewall configuration
4. Wallet: Install and configuration of wallet holding 1000 tDash in collateral
5. Masternode Server: Final configuration of Dash Core masternode proper
6. Wallet: Final configuration of Dash Core wallet
7. Sentinel Server: Install and configuration of Sentinel on the Masternode Server


# 1. Linux Setup

The following assumes fresh linux OS installs with no dash core components
installed.

Install two Linux systems. UI is irrelevant and consumes disk space and RAM. We
do not need a GUI front end for these instructions. "Minimal" install works. The
correct dependent requirements will be pulled in via the RPM and DNF/YUM systems --
hence the power of using properly built RPM packages.

[Mn] Many use light virtual cloud systems for their masternodes. Example
services may be [Vultr](https://www.vultr.com/),
[Dreamhost](https://www.dreamhost.com/), [Digital
Ocean](https://www.digitalocean.com/), [Amazon AWS](https://aws.amazon.com/),
etc. Setting a server up is fairly simple in most cases, but you should be
cognizant of the hardware requirements for running a masternode. That can be
found
[here](https://dashpay.atlassian.net/wiki/display/DOC/Hardware+Requirements). I
include an example for setting one up on Vultr below...

----

## [Mn] The Vultr.com Example

### [Mn] Initial Vultr instance deployment...

* Browse to <https://my.vultr.com/>
* Create an account and login.
* Click the ( + ) button.
* Choose: 64 bit OS and Fedora
* Choose: 15 GB SSD (cheapest offering) with supposedly 768MB RAM (which is actually 740MB)
* Set up SSH keys... it will make your life more pleasant. Vult.com provides
  pretty solid instruction on this process.
* Pick a hostname, `master00`, or whatever.
* Deploy!

### [Mn] Post Vultr instance deployment...

* **Test and troubleshoot your SSH settings** &mdash; ssh into your Vultr instance: `ssh root@<IP ADDRESS OF YOUR INSTANCE>` If you set up ssh keys right, it should just log you right in. If not, log in using your root password and troubleshoot why your ssh key setup is not working right and get it working (see above) so that you don't need a password to ssh into your system.
* **Change your root password** &mdash; `passwd` &mdash; to something longer and ideally random. I use Lastpass to generate passwords.
* **Add swap space** to give your system memory some elbow room (Vultr mysteriously starts you with none)...<br />
```
# As root...
# Make swap the same size as your existing RAM
XMEM=$(free -k|grep Mem|awk '{print $2}')
# Create a swapfile
dd if=/dev/zero of=/swapfile bs=1024 count=$XMEM
mkswap /swapfile
chmod 0600 /swapfile
# Turn it on
swapon /swapfile
# You can see it running with a "swapon -s" or "top" command
# Enable even after reboot
cp -a /etc/fstab /etc/fstab.mybackup # just in case
echo '/swapfile swap swap defaults 0 0' >> /etc/fstab
cat /etc/fstab # double check your fstab file looks fine
```

* Fully **update the system and reboot**...
```
dnf upgrade -y
reboot
```

* Finally, try logging back in with ssh (see above). If you had to use a
  password, the ssh key setup isn't right. Troubleshoot and fix it. If you can't
  log in at all... destroy the instance and start over.

----

### Install Prerequisites

#### [Mn] [W] Create two normal (non-root) user accounts, one on each linux system

*Note1, you can technically use your masternode server as a wallet as well and
have it collateralize itself. But that is very bad practice (sure, this is
testnet, but...). Just don't do it unless you become more expert and then you
can make that decision for yourself. **For a production masternode setup, a
separate wallet is a must.***

*Note2, these usernames are arbitrary (you can pick your own username)*

    # On linux system #1, the Masternode Server
    sudo useradd -G wheel mn0
    sudo passwd mn0

    # On linux system #2, the Masternode Collateral-bearing Wallet
    sudo useradd -G wheel mnwallet
    sudo passwd mnwallet

#### [Mn] As user `mn0`, install dashcore, update, reboot

...if using Fedora:

```
cd /etc/yum.repos.d/
sudo curl https://raw.githubusercontent.com/taw00/dashcore-rpm/master/dashcore-fedora.repo -o dashcore-fedora.repo
cd -
sudo dnf config-manager --set-disabled dashcore-stable
sudo dnf config-manager --set-enabled dashcore-unstable
sudo dnf install -y dashcore-server dashcore-utils
sudo dnf upgrade -y
```

...if using CentOS or RHEL

```
cd /etc/yum.repos.d/
sudo curl https://raw.githubusercontent.com/taw00/dashcore-rpm/master/dashcore-centos.repo -o dashcore-centos.repo
cd -
sudo yum-config-manager --disable dashcore-stable
sudo yum-config-manager --enable dashcore-unstable
sudo yum install -y dashcore-server dashcore-utils
sudo yum update -y
```

***Recommendation:***
Choose a difficult scrambled password for both `root` and your `mn0` user. Then
ensure ssh keys are set up so you can ssh to the instance without having to type
passwords. And finally, edit the `/etc/sudoers` configuration file and uncomment
the `%wheel` line that includes the `NOPASSWD` qualifier. This will allow you to
`sudo` as the `mn0` user without having to cut-n-paste a password all the time.

...once fully updated, reboot

```
sudo reboot
```

#### [W] As user `mnwallet`, repeat the same install, update, and reboot
*see above -- again, this assumes the wallet is running on a similarly
minimalistic and fresh system.*

----

# 2. [Mn] Set up Dash Core Masternode Server

Perform these steps as user `mn0` in a terminal (from the command line)

### [Mn] Create your Dash Core working/configuration directory
*If it doesn't exist yet.*

```
mkdir ~/.dashcore
```

### [Mn] Dash Core Masternode Server configuration part 1: Create testnet `dash.conf` [initial template]

*You can read more about the `dash.conf` file [here](https://github.com/dashpay/dash/blob/master/contrib/debian/examples/dash.conf)*

```
echo '# This is a Masternode Server configuration file
# Run on the test network instead of the real dash network.
testnet=1
# Run dashd as a daemon (in the background)
daemon=1
# Listening mode, enabled by default except when 'connect' is being used
listen=1
logtimestamps=1
maxconnections=256

# Remote Procedure Call access configuration...
# server=1 tells Dash-QT and dashd to accept JSON-RPC commands
server=1
# You must set rpcuser and rpcpassword to secure the JSON-RPC api
rpcuser=<make_up_an_rpc_username>
rpcpassword=<anything_you_like_but_make_it_not_obvious>
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
#masternodeprivkey=<results of "dash-cli masternode genkey" in wallet>
#externalip=<results of "dig +short myip.opendns.com @resolver1.opendns.com">
' >> ~/.dashcore/dash.conf
```

### [Mn] Start up your Dash Core Masternode Server (`dashd`)

    dashd

Check its status...

    dash-cli getinfo

### [Mn] Watch blockchain sync status...
Watch progress of synchronization of the testnet blockchain. Browse to
https://test.explorer.dash.org/ or http://test-insight.dev.dash.org/ look at the
current block count and wait until it is achieved (will take a few minutes
dependent on speed of internet connection).

```
# CTRL-C to exit this loop when block count is caught up
#watch "dash-cli getinfo | grep blocks"
watch dash-cli getblockcount
```

### [Mn] Shut 'er down for now while we work on other step...

```
# Wait until caught up then... Shut her down.
dash-cli stop ; sleep 15
```

----

# 3. [Mn] Configure the Firewall on Masternode Server

*Note: Firewall rules can be a complicated topic. These are bare bones
git-er-done instructions. You may want to investigate further refinement. It
will get you started though.*

Install `firewalld`

```
# If Fedora...
sudo dnf install -y firewalld # Probably already installed
# If CentOS or RHEL...
sudo yum install -y firewalld # Probably already installed
```

Configure firewall

```
# Is firewalld running?
# Turn on and enable firewalld if not already done...
sudo firewall-cmd --state
sudo systemctl start firewalld.service
sudo systemctl enable firewalld.service

# Determine what the default zone is.
# On vultr, for example, default zone is FedoraServer (it is the assumption for this example)
sudo firewall-cmd --get-active-zone

# FedoraServer usually starts with ssh, dhcp6-client, and cockpit opened up
# I want to allow SSH and masternode traffic, but I don't want cockpit running
# all the time and by having a static IP, dhcpv6 service is unneccessary.
sudo firewall-cmd --permanent --zone=FedoraServer --add-service ssh
sudo firewall-cmd --permanent --zone=FedoraServer --add-service dashcore-node
#sudo firewall-cmd --permanent --zone=FedoraServer --add-service dashcore-node-testnet
sudo firewall-cmd --permanent --zone=FedoraServer --remove-service dhcpv6-client
sudo firewall-cmd --permanent --zone=FedoraServer --remove-service cockpit

# Open up the Masternode port (19999=Testnet, 9999=Live)
sudo firewall-cmd --permanent --zone=FedoraServer --add-port=19999/tcp
sudo firewall-cmd --permanent --zone=FedoraServer --add-port=9999/tcp

# Rate limit incoming ssh and cockpit (if configured on) traffic to 10 per minute
sudo firewall-cmd --permanent --add-rich-rule='rule service name=ssh limit value=10/m accept'
sudo firewall-cmd --permanent --add-rich-rule='rule service name=cockpit limit value=10/m accept'
# Rate limit incoming dash node/masternode traffic to ??? per second? TODO: Figure this out.
#sudo firewall-cmd --permanent --add-rich-rule='rule service name=dashcore-node limit value=100/s accept'
#sudo firewall-cmd --permanent --add-rich-rule='rule service name=dashcore-node-testnet limit value=100/s accept'

# did it take?
sudo firewall-cmd --reload
sudo firewall-cmd --state
sudo firewall-cmd --list-all
```

**Some references:**

* Rate limiting as we do above: <https://www.rootusers.com/how-to-use-firewalld-rich-rules-and-zones-for-filtering-and-nat/>
* More on rate limiting: <https://serverfault.com/questions/683671/is-there-a-way-to-rate-limit-connection-attempts-with-firewalld>
* And more: <https://itnotesandscribblings.blogspot.com/2014/08/firewalld-adding-services-and-direct.html>
* Interesting discussion on fighting DOS attacks on http: <https://www.certdepot.net/rhel7-mitigate-http-attacks/>
* Do some web searching for more about firewalld

----

# 4. [W] Set up the Dash Core Collateral-bearing Wallet

Perform these steps from the command line (a terminal) as user `mnwallet`. You
will end up with a wallet reserving 1000 tDash in collateral and linked to a
masternode.

*Note, you installed dashcore-server` and `dashcore-utils` a few steps back.
They provide the `dashd` wallet daemon and `dash-cli` utility. You could install
`dashcore-client` instead and use that (the pretty `dash-qt` GUI wallet), but
instruction for that is not included here). The `dashd` server (Dash Core
daemon) can serve as a node, a masternode, or a wallet.*

### [W] Create your Dash Core configuration directory
*If it doesn't exist yet.*

*Note: Older (12.0) Dash Core wallets used the `~/.dash/` directory structure.
This was changed for 12.1 and newer to `~/.dashcore/`.*

```
mkdir ~/.dashcore
```

### [W] Configuration: Create testnet `dash.conf` [initial template]

```
echo '# This is a Masternode Collateral-bearing Wallet configuration file
# Run on the test network instead of the real dash network.
testnet=1
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
rpcuser=<make_up_an_rpc_username>
rpcpassword=<anything_you_like_but_make_it_not_obvious>
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
' >> ~/.dashcore/dash.conf
```

### [W] Start up your Dash Core Wallet Server (dashd) and check status

    dashd

Check it's status...

    dash-cli getinfo

### [W] Watch blockchain sync status...
Watch progress of synchronization of the testnet blockchain. Browse to
https://test.explorer.dash.org/ or http://test-insight.dev.dash.org/ look at the
current block count and wait until it is achieved (will take a few minutes
dependent on speed of internet connection).

```
# CTRL-C to exit this loop when block count is caught up
watch "dash-cli getinfo | grep blocks"
```

### [W] Get masternode funding address from wallet

```
dash-cli getnewaddress
# used in the next step...
```

### [W] Send *exactly* 1000 tDash to that address from a testnet faucet:

 * https://test.faucet.dash.org/
 * http://test.faucet.masternode.io/mn/

*Note: If sending from another wallet, (a) make sure you are attempting to send
tDash (testnet) and (b) send exactly 1000 tDash which may mean you have to
account for miner fees.*

### [W] Generate masternode privkey (private key from wallet to support masternode)

```
dash-cli masternode genkey
# Record this in some scratch notepad for the moment
```

### [W] Get your funding transaction id and index

```
dash-cli masternode outputs
# Record this in some scratch notepad for the moment
```

----

# 5. [Mn] Finish Configuration of the Dash Core Masternode Server

Perform these steps as user `mn0` in a terminal (from the command line)

Set IP and Key configuration...

### [Mn] Get public IP address

```
dig +short myip.opendns.com @resolver1.opendns.com
```

### [Mn] Update `~/.dashcore/dash.conf`

* uncomment all masternode and externalip lines (remove #'s)
* add "`dash-cli masternode genkey`" result from wallet to end of `masternodeprivkey=` line
* optionally add public IP address to `externalip=` line<br />*(really only needed if the masternode is tucked inside a router)*
* Note: `nano` is a good default editor you can use, eg. `nano ~/.dashcore/dash.conf`. Personally I use `vim`, but ... `vim` is not for n00bs. :)

*It should look something like this snippet (example values)...*

```
masternode=1
masternodeprivkey=936kTs5ms123453455632345PEHKfJefiA26XcmLzR8cJooVn2
externalip=110.111.112.113
```

### [Mn] Restart the Dash Core Masternode and make sure it it up and running

```
# If not already shut down, shut the server down
dash-cli stop ; sleep 15
dashd
sleep 15; dash-cli getinfo
```

----

# 6. [W] Finish Configuration of the Collateral-bearing Wallet

Perform these steps as user `mnwallet` in a terminal (from the command line)

### [W] Add masternode values to `masternode.conf`

*Note: `~/.dashcore/testnet3/` is a directory for this testnet effort.<br />
**TODO: Is this hardcoded? I am not sure. Just do it this way. -t0dd***

Configuring `~/.dashcore/testnet3/masternode.conf`...

```
echo '# add the following line to the end of the conf, replacing your values from above
#`mn0` <externalip>:<PORT> <masternodeprivkey> <funding_txid> <funding_index>
# it should look something like this (9999 for live net, and 19999 for testnet)
`mn0` 110.111.112.113:19999 936kTs5ms123453455632345PEHKfJefiA26XcmLzR8cJooVn2 b34ad623453453456423454643541325c98d2f8b7a967551f31dd7cefdd67457 1' >> ~/.dashcore/testnet3/masternode.conf
```

### [W] Restart dashd on wallet system

```
dash-cli stop ; sleep 15
dashd
```

### [W] Start masternode from wallet interface

Wait a few minutes after restart to allow full synchronization, then

```
dash-cli masternode start-missing # or dash-cli masternode start-alias <alias>
```

### [Mn, W] Check that the masternode is started

```
dash-cli masternode list full |grep <IP ADDRESS OF MASTERNODE>
```

You should get output that looks something like (example values)...    
*Note, it may take some time to go from PRE_ENABLED to ENABLED.*    
The fields are: "transaction_id": "status protocol payee lastseen activeseconds
lastpaidtime lastpaidblock MASTERNODE_IP:PORT"

```
"b34ad623453453456423454643541325c98d2f8b7a967551f31dd7cefdd67457-1": "        ENABLED 70203 yRGhc4fL54345ggds5486U2i4CamTaV6N7 1480332513     1606 1480329609 110222 110.111.112.113:19999"
```

Also check out these commands...

```
dash-cli masternode debug
dash-cli masternode status
```

----

# 7. [Mn] Set up Sentinel on Masternode Server

*From the introduction in nmarley's document (see below)...*

Sentinel is an all-powerful toolset for Dash.

Sentinel is an autonomous agent for persisting, processing and automating Dash
V12.1 governance objects and tasks, and for expanded functions in the upcoming
Dash V13 release (Evolution).

Sentinel is implemented as a Python application that binds to a local version
12.1 dashd instance on each Dash V12.1 Masternode.

...

### [Mn] Install Sentinel

I include instruction here, from nmarley's [excellent
document](https://github.com/nmarley/sentinel/blob/master/README.md). You can
follow that, or just plow right on ahead below.

*Perform these steps as user `mn0` in a terminal (from the command line)*

...if Fedora:

    sudo dnf upgrade -y # you did this earlier actually
    sudo dnf install -y git python-virtualenv

...if CentOS or RHEL:

    sudo yum upgrade -y # you did this earlier actually
    sudo yum install -y git python-virtualenv

Continue for either Fedora or CentOS/RHEL:

```
git clone https://github.com/nmarley/sentinel.git
cd sentinel
virtualenv venv
#source venv/bin/activate
#pip install -r requirements.txt
./venv/bin/pip install -r requirements.txt
```

### [Mn] Install crontab script

#### [Mn] Verify crontab script works

The following command should show creation of tables.

    ./venv/bin/python scripts/crontab.py

The following command (repeated) should show **NO** output.

    ./venv/bin/python scripts/crontab.py

The following command is used to see more debug information if you like.

    SENTINEL_DEBUG=1 ./venv/bin/python scripts/crontab.py

If your masternode is not fully sync'ed yet, you will see this message until it has caught up with the blockchain:

    dashd not synced with network! Awaiting full sync before running Sentinel.

#### [Mn] Configure crontab

    crontab -e

Insert the following line into crontab to invoke sentinel every two minutes.    
*ASSUMPTION: `mn0` is still the username you chose*

    `*/2 * * * * cd /home/mn0/sentinel && venv/bin/python scripts/crontab.py >/dev/null 2>&1`

### [Mn] Run sentinel tests (should show passing tests)

    venv/bin/py.test test

----

# Celebrate! You're done!

I hope this was helpful    
Got a dash of feedback? *...har har...* Send it my way [t0dd@protonmail.com](mailto:t0dd@protonmail.com)

----

----

# == Addenda =========

## Addendum 1: Advanced configuration: Running `dashd` as a system service

> Note: This will likely become the default instruction for dash set up in the futur. Let me know what you think. -t0dd

> Assumption: You are utterly familiar with `systemd`, `systemctl`, the concept of a system user, etc. The ideas of firewalls and using the commandline are not alien to you.

Configuring to run your masternode as a service is very similar to running it directly as a user. In the end, a masternode is a daemon service. It begs to be run using specific system users and locked down with SELinux (SELinux configuration not done yet -t0dd).

When you install `dashcore-server`, a system user is created called, as one might expect, `dash`. A data directory is created `/var/lib/dashcore/` and a configuration directory `/etc/dashcore/`. There are two system service configuration files that you don't touch, but are worth looking at to learn out things work: `/usr/lib/systemd/system/dash.service` and `/etc/sysconfig/dash`.

To set things up, you follow all the instructions of this document, but here are the differences:

1. Edit your configuration file in `/etc/dashcore/dash.conf`
2. Starting and stopping `dashd`...
   - Starting: `sudo systemctl start dash`
   - Stopping: `sudo systemctl stop dash`
3. You perform most actions as the system user `dash` when setting things up and root or dash otherwise. And you must reference -conf and -datadir, for example:    
   `sudo dash-cli -conf=/etc/dashcore/dash.conf -datadir=/var/lib/dashcore getinfo`

Finish setting up the masternode, and wallet configuration, and when ready, start the service (if you have not done so already) and make that service persistent with...
```
sudo systemctl start dash
sudo systemctl enable dash
```
XXX TO BE CONTINUED XXX GO STEELERS!

### Time to set up Sentinel...

Setting up Sentinel is different (and manual since I have not built RPMs yet for it)...

Become root:
```
sudo su -
```

Check out Sentinel from github as the `dash` system user in the `/var/lib` directory:
```
cd /var/lib
sudo -u dash git clone https://github.com/nmarley/sentinel
cd /var/lib/sentinel
```

Edit `sentinel.conf` and set the configuration file appropriately: `dash_conf=/etc/dashcore/dash.conf`

Finish setting things up, again, as system user `dash`:
```
cd /var/lib/sentinel
sudo -u dash virtualenv venv
sudo -u dash ./venv/bin/pip install -r requirements.txt
```

Create database tables...
```
SENTINEL_DEBUG=1 /var/lib/sentinel && sudo -u ./venv/bin/python scripts/crontab.py
```

Run that command again, it should be silent if everything went well...
```
SENTINEL_DEBUG=1 /var/lib/sentinel && sudo -u ./venv/bin/python scripts/crontab.py
```

Edit crontab with `sudo -u dash crontab -e` and add this line...
```
*/2 * * * * cd /var/lib/sentinel && ./venv/bin/python scripts/crontab.py >/dev/null 2>&1
```

Now go back to your wallet check that everything is enabled with...
```
dash-cli masternode list full|grep <IP ADDRESS OF MASTERNODE>
```

That's it. Not too hard. You now have a service daemon, running as a service daemon should.


----

## Addendum 2: Masternode Troubleshooting guide

### NOT WRITTEN YET...
