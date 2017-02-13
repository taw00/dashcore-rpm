# HowTo: v12.1 Dash Masternode as SystemD Service<br />_...on Fedora, CentOS or Red Hat Enterprise Linux_

> This edition of these instructions is for those who wish to install and
> configure a Dash Masternode running as a traditional `systemd` service.
>
> A Dash Masternode is a server service, therefore it lends itself to the
> improved security and robustness that `systemd` offers. I.e., It really is
> the "right way" of running your masternode. Another "right way" would be
> to run it as a container. But that is beyond the scope of this document.
>
> These instructions are specific to the Red Hat-family of linuxes.
>
> These instructions should work for all supported linuxes found at the link
> above. As of this writing that is Fedora Linux 24 and 25, CentOS 7, and RHEL 7.
> I did most of my testing on Fedora 24. I tested with the masternode running on a
> local virtual instance as well as a VPS cloud instance.


## FIRST: Set up your collateral-bearing wallet

For a general overview of what a masternode is and how it is set up at a high
level, please refer to the overview document found
[here](https://github.com/taw00/dashcore-rpm/blob/master/documentation/README.md).

As of this writing (early 2017), before setting up a masternode, you need to
acquire 1000 DASH and hold it in a specially configured wallet. Do that first.
You can find instruction for how to set that up here:
[howto.12.1-dashcore-collateral-bearing-wallet-setup.gui.md](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.12.1-dashcore-collateral-bearing-wallet-setup.gui.md)

Once completed, you may continue.

## [0] Install the operating system

There are two primary means to install the operating system that will covered
here. (1) Via a cloud service, like Vultr.com, or (2) via a traditional
bare-metal blade, server, white-box, whatever.

The objectives are straight-forward:

1. Install a minimal OS
2. Ensure there is enough swap-space configured
3. Configure SSH so you can log in without a password into root and a normal user who has sudo'ers rights
4. Fully update and reboot

> A note about minimum requirements. Masternodes are no longer "glorified full
> nodes". They are doing more and more things and they will need beefier specs
> over time. The old, 1G RAM and 1G Swap shorthand may not cut it anymore. To
> read more, please visit this page:
> <https://dashpay.atlassian.net/wiki/display/DOC/Masternode+Update>

### A cloud service installation, for example Vultr

#### Install to Vultr
  - Browse to https://my.vultr.com/
  - Create an account and login.
  - Click the ( + ) button.
  - Choose: 64 bit OS and Fedora
  - Choose: 2048MB RAM, 2CPU 45GB SSD (you may be able to have a cheaper offering limp along, but I don't recommend it.
  - Set up SSH keys. It will make your life more pleasant. Vult.com provides pretty solid instruction on this process.
  - Pick a hostname, `master00`, or whatever.
  - Deploy!

#### Post install on Vultr
  - **Test and troubleshoot your SSH settings** &mdash; ssh into your Vultr
    instance: `ssh root@<IP ADDRESS OF YOUR INSTANCE>` If you set up ssh keys
    right, it should just log you right in. If not, log in using your root
    password and troubleshoot why your ssh key setup is not working right and get
    it working (see above) so that you don't need a password to ssh into your
    system.
  - **Change your root password** &mdash; `passwd` &mdash; to something longer
    and ideally random. I use Lastpass to generate passwords.
  - **[optional] Change your timezone settings** &mdash; The default is set to
    UTC. If you prefer times listed in your local timezone, change it. FYI:
    Some time-date stamps are always listed in UTC, like many log files.

```
# As root user
# Find and cut-n-paste your timezone...
timedatectl list-timezones # arrow keys to navigate, "q" to quit
# Change it (example, eastern time, USA)...
timedatectl set-timezone 'America/New_York'
# Don't like that? Change it back...
timedatectl set-timezone 'UTC'
# Test it...
date
```

  - **Add swap space** to give your system memory some elbow room...

Vulr mysteriously starts you with no swap. A good [rule of thumb](https://gist.github.com/taw00/f6dc6040a86e3bbe434dab4c1ab23b2b) is to configure swap to be that is twice the size of your RAM.

```
# As root...
sudo su -

bs=2048 # Twice the size of RAM -- recommended
#bs=1024 # One times the size of RAM
#bs=1536 # 1.5 times the size of RAM

# Create a swap file 2x size as your existing RAM (TOTAL_MEM * 1024 * 2)
TOTAL_MEM=$(free -k|grep Mem|awk '{print $2}')
dd if=/dev/zero of=/swapfile bs=$bs count=$TOTAL_MEM
chmod 0600 /swapfile
mkswap /swapfile

# Turn it on
swapon /swapfile

# You can see it running with a "swapon -s" or "free" command
free -h

# Enable even after reboot
cp -a /etc/fstab /etc/fstab.mybackup # backup your fstab file
echo '/swapfile swap swap defaults 0 0' >> /etc/fstab
cat /etc/fstab # double check your fstab file looks fine
```

  - Log out and log back in using your new _ssh_ credentials

Finally, try logging back in with ssh (see above). If you had to use a
password, the ssh key setup isn't right. Troubleshoot and fix it. If you can't
log in at all... destroy the instance and start over.


### A traditional bare-metal server installation

I leave it as an exercise for the reader to perform a bare-metal installation
of  Fedora, CentOS, or even RHEL. For Fedora, go here - https://getfedora.org/
For CentOS, go here - https://www.centos.org/download/ For Fedora, I recommend
the "Server" install. You need only a minimum configuration. Dependency
resolution of installed RPM packages per these instructions will bring in
anything you need.

Ensure that your bare-metal server meets at least these requirements:<br />
_Again, revisit this page for more information: <https://dashpay.atlassian.net/wiki/display/DOC/Masternode+Update>_

* 2GB RAM
* 40 GB disk

As you walk through the installation process, choose to enable swap, it needs
to be at least equal to the size of RAM, 2GB and ideally twice that, 4GB.

Once installed, follow similar process as the Vultr VPS example for SSH configuration.


### Post OS installation: create user...

During the installation process using the wizard you will likely be asked to
create a user. Do that if you like. Additionally, you can choose to give this
user administration rights (they will be able to `sudo`).

While you can do that during the set up process, included here is the
post-installation instruction for doing the same thing. The username in this
example is `mnuser`...

```
# Log into the system as root user.
# If the user does not exist, do this...
useradd -G wheel mnuser
passwd mnuser

# If the user already exists, do this...
usermod -a -G wheel mnuser
```

Again, work through the SSH instructions (see Vultr example) and set it up so
you can ssh into the system without a password from your desktop system.


> ***Recommendation:***
> Choose a difficult scrambled password for both `root` and your `mnuser` user.
> Then ensure ssh keys are set up so you can ssh to the instance without having
> to type passwords. And finally, edit the `/etc/sudoers` configuration file
> and uncomment the `%wheel` line that includes the `NOPASSWD` qualifier. This
> will allow you to `sudo` as the `mnuser` user without having to cut-n-paste a
> password all the time.



### Post OS installation: fully update the system and reboot

Log in as `mnuser` and...

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



## [1] Install Dash and FirewallD

Because this is a Red Hat -based system, management of installed software is
trivial. This is how easy it is.

#### Configure the Dash Core repositories (you only do this once)

...if this is Fedora

```
cd /etc/yum.repos.d/
sudo curl -O https://raw.githubusercontent.com/taw00/dashcore-rpm/master/dashcore-fedora.repo
cd -
```
<!--
```
#sudo dnf config-manager --set-disabled dashcore-stable
#sudo dnf config-manager --set-enabled dashcore-unstable
```
-->


...if this is CentOS or Red Hat Enterprise Linux

```
cd /etc/yum.repos.d/
sudo curl -O https://raw.githubusercontent.com/taw00/dashcore-rpm/master/dashcore-centos.repo
cd -
```

<!--
```
#sudo yum-config-manager --disable dashcore-stable
#sudo yum-config-manager --enable dashcore-unstable
```
-->

#### Install Dash Core server and FirewallD

...if this is Fedora

```
sudo dnf install -y dashcore-server firewalld
```

...if this is CentOS or Red Hat Enterprise Linux

```
sudo yum install -y dashcore-server firewalld
```


## [2] Configure Dash Core Server to be a Full Node

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
explicitely include them on the commandline when we perform actions.


### Edit `/etc/dashcore/dash.conf`

Log in as the normal user, `mnuser` in this example.

With your favorited editor &mdash; some use `nano`, I use `vim` &mdash; open up
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
maxconnections=256

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
#masternodeprivkey=<results of "dash-cli masternode genkey" in wallet>
#externalip=<results of "curl https://icanhazip.com">
```

Please take special note of `"testnet=1"` and `"testnet=0"`.

### Change your RPC (remote procedure call username and password)

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

### Start up your Dash Core full node (it isn't a masternode yet)

Log in as the normal user, `mnuser` in this example.

```
# You kick off systemd services as root
sudo systemctl start dashd
```

#### SSH into two terminals and watch the logs in one...

```
# ^C out of this tail feed when you are done...
sudo -u dashcore tail -f /var/lib/dashcore/debug.log # if mainnet
#sudo -u dashcore tail -f /var/lib/dashcore/testnet3/debug.log
```

#### ...and watch the blockcount rise (hopefully) in the other...

```
# ^C out of this loop when you are done
watch -n10 sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf getblockcount
```

You will know you have sync'ed the entire blockchain when it matches the current block-heigth:

* <https://explorer.dash.org/> &mdash; for mainnet
* <https://test.explorer.dash.org/> &mdash; for testnet

...or if you are comfortable on the commandline, these are helpful...
```
# "mainnet" block height
curl -o - https://explorer.dash.org/chain/Dash/q/getblockcount
# "testnet" block height
curl -o - https://test.explorer.dash.org/chain/tDash/q/getblockcount
# This command will spit out the block height for this network as your
# masternode sees it (ie, it could be wrong)
sudo -u dashcore dash-cli -conf=/etc/dashcore/dash.conf getchaintips |grep -m1 height | sed 's/[^0-9]*//g'
```


#### Once fully sync'ed your configuration as a full node is complete.


## [3] Edit `/etc/dashcore/dash.conf` and finish those masternode settings

First, write down the value of `curl https://icanhazip.com` that you get at the
commandline of this masternode server. For this example, we are going to use
`93.184.216.34` (yours will be different, of course).

Then take the data you gathered from setting up your wallet in
[howto.12.1-dashcore-collateral-bearing-wallet-setup.gui.md](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.12.1-dashcore-collateral-bearing-wallet-setup.gui.md)
and reconfigured `/etc/dashcore/dash.conf`

```
# Use your favorite editor, in this example, "nano"
sudo -u dashcore nano /etc/dashcore/dash.conf
```

Convert these lines from...
```
#masternode=1
#masternodeprivkey=<results of "dash-cli masternode genkey" in wallet>
#externalip=<results of "curl https://icanhazip.com">
```

...to (and this is example data from the prior wallet exercise)...
```
masternode=1
masternodeprivkey=92yZY5b8bYD5G2Qh1C7Un6Tf3TG3mH4LUZha2rdj3QUDGHNg4W9
externalip=93.184.216.34
```

## [4] Restart the `dash` systemd service and enable it for restart upon boot

```
sudo systemctl restart dashd
# there will be a 15 to 30 second pause as systemd allows dashd to shut down properly
sudo systemctl enable dashd
```

Now, if you have to reboot your system for whatever reason, the dash service
will restart as well. It is worth remembering that a masternode does not need
to be "restarted" (re-validated really) from a wallet unless it has been
offline for some time (I believe something like 75 minutes -- that quote needs
to be verified).


## [5] Configure firewall rules

You can follow the instruction in
[howto.12.1-dashcore-collateral-bearing-wallet-setup.gui.md](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.12.1-dashcore-collateral-bearing-wallet-setup.gui.md),
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

# FedoraServer usually starts with ssh, dhcp6-client, and cockpit opened up
# I want to allow SSH and masternode traffic, but I don't want cockpit running
# all the time and by having a static IP, dhcpv6 service is unneccessary.
sudo firewall-cmd --permanent --zone=FedoraServer --add-service ssh
sudo firewall-cmd --permanent --zone=FedoraServer --add-service dashcore-node # mainnet
sudo firewall-cmd --permanent --zone=FedoraServer --add-service dashcore-node-testnet
sudo firewall-cmd --permanent --zone=FedoraServer --remove-service dhcpv6-client
sudo firewall-cmd --permanent --zone=FedoraServer --remove-service cockpit

# Rate limit incoming ssh and cockpit (if configured on) traffic to 10 per minute
sudo firewall-cmd --permanent --add-rich-rule='rule service name=ssh limit value=10/m accept'
sudo firewall-cmd --permanent --add-rich-rule='rule service name=cockpit limit value=10/m accept'
# Rate limit incoming dash node/masternode traffic to ??? per second?
#TODO: Figure this out.
#sudo firewall-cmd --permanent --add-rich-rule='rule service name=dashcore-node limit value=100/s accept'
#sudo firewall-cmd --permanent --add-rich-rule='rule service name=dashcore-node-testnet limit value=100/s accept'

# did it take?
sudo firewall-cmd --reload
sudo firewall-cmd --state
sudo firewall-cmd --list-all
```

_NOTE1: you may want to comment out the `--add-service` line for testnet or
mainnet depending on your setup._

_NOTE2: at this time, I do not have rich rules for rate managing the 9999 or
19999 ports (dashcore-node and dashcore-node-testnet)_

**Some references:**

* Rate limiting as we do above:
  <https://www.rootusers.com/how-to-use-firewalld-rich-rules-and-zones-for-filtering-and-nat/>
* More on rate limiting:
  <https://serverfault.com/questions/683671/is-there-a-way-to-rate-limit-connection-attempts-with-firewalld>
* And more:
  <https://itnotesandscribblings.blogspot.com/2014/08/firewalld-adding-services-and-direct.html>
* Interesting discussion on fighting DOS attacks on http:
  <https://www.certdepot.net/rhel7-mitigate-http-attacks/>
* Do some web searching for more about firewalld


## [6] ON WALLET: Add masternode IP address

Go back to your wallet (see
[howto.12.1-dashcore-collateral-bearing-wallet-setup.gui.md](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.12.1-dashcore-collateral-bearing-wallet-setup.gui.md))
and edit the `masternode.conf` file referenced there and replace the example IP
address with the IP address of this masternode as found in prior steps above.

Following our examples, that line in the `masternode.conf` file will look
something like this...
```
mn1 93.184.216.34:9999 92yZY5b8bYD5G2Qh1C7Un6Tf3TG3mH4LUZha2rdj3QUDGHNg4W9 b34ad623453453456423454643541325c98d2f8b7a967551f31dd7cefdd67457 1
```

_**Notice that port number. Choose 9999 for mainnet and 19999 for testnet.**_


## [7] ON WALLET: Trigger a start of your masternode

This is it! Flip that bit! This is really a "validation" step that connects
that 1000 DASH collateral to this masternode and says "Okay, full node, you can
now operate on the network as a masternode!"

Go back to your wallet (see
[howto.12.1-dashcore-collateral-bearing-wallet-setup.gui.md](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.12.1-dashcore-collateral-bearing-wallet-setup.gui.md)).

* Navigate the menus: Tools > Debug console
* Enter in that dialogue: `masternode start-alias mn1`<br />
  Alternatively, you can start all masternodes (if you have multiple) with: `masternode start-missing`

Remember `mn1` is our example alias.

Or from the commandline: `dash-cli masternode start-alias mn1`<br />
...optionally: `dash-cli masternode start-missing`

If the command was sent successfully, you should see... "successful" or
something similar. This means the command was sent successfully, not that the
masternode was truly started.

**Recommendation: Once you have issued this command, SHUT DOWN YOUR WALLET.
There is 1000 DASH associated to that wallet. There is no reason to keep it
online for very long. Shut it down.**

## [8] ON MASTERNODE: Monitor masternode enablement status

What you are looking for is ENABLED to be displayed. This can take up to 15
minutes or so. You can really do this from the wallet _or_ the masternode
itself.

From the commandline do this (this is an example; use your masternode's IP
address)...
```
sudo -u dashcore watch -n10 "dash-cli -conf=/etc/dashcore/dash.conf masternode list full | grep 93.184.216.34"
```

While that is going on in one terminal, open up another terminal and...

## [9] Set up Dash Sentinel

There are really two services associated to a masternode, the node itself and a
"sentinel" that performs certain actions and manages expanded processes for the
network. It was already installed when your dashcore-server package was
installed. You just have to turn it on and edit crontab for the `dash` system
user so that it executes every five minutes...

<!-- if you installed from an RPM package, this step goes away
### Turn off testnet/mainnet checking in `sentinel.conf`

Edit the /var/lib/dashcore/sentinel/sentinel.conf file and comment out
`network=testnet` and `network=mainnet` if one of them is set in there. Your
`dash.conf` file properly sets that and the Sentinel default configuration file
may wronging override your `dash.conf` file. At least it does in the earlier
versions of Sentinel.
-->

### Run it for the first time...
```
sudo -u dashcore -- bash -c "cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py
```

It should create a database and populate it.

Run it again...
```
sudo -u dashcore -- bash -c "cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py
```

There should be no output.

> Note, if something seems to be going wrong, set SENTINEL_DEBUG=1 and try to
> make sense of the output
> ```
> sudo -u dashcore -- bash -c "cd /var/lib/dashcore/sentinel && SENTINEL_DEBUG=1 venv/bin/python bin/sentinel.py >> /var/log/dashcore/sentinel.log 2>&1"
> less /var/log/dashcore/sentinel.log
> ```

### Edit cron and add a "run it every five minutes" entry

On the commandline, edit `crontab` &mdash; notice, that we, like in most
commands, are doing it as the `dashcore` system user...
```
sudo -u dashcore EDITOR="nano" crontab -e
```

...and add these lines, save and exit...

```
#SENTINEL_DEBUG=1
#*/5 * * * * cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py > /dev/null 2>&1
*/5 * * * * cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py >> /var/log/dashcore/sentinel.log 2>&1
```

## YOU ARE DONE!

Continue to monitor the enablement status as illustrated in step 8. The status
should start as `PRE_ENABLED`, maybe move to `WATCHDOG_EXPIRED`, but finally is
should settled on `ENABLED`. If your wallet failed to restart it, it will say
something like `NEW_START_REQUIRED`

If all went well, you have a working Dash Masternode! Congratulations. I hope
this was helpful.

Got a dash of feedback? *...har har...* Send it my way <t0dd@protonmail.com>    
And of course, donations welcome: [XyxQq4qgp9B53QWQgSqSxJb4xddhzk5Zhh](dash:XyxQq4qgp9B53QWQgSqSxJb4xddhzk5Zhh)

---

---

## Addendum - Advanced...


#### Super fancy crontab settings

Remember to edit with `sudo -u dashcore crontab -e` if dashcore-sentinel is installed with
our RPM packages.

```
# Run Sentinel every five minutes; no extra information sent to the log files.
*/5 * * * * cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py > /dev/null 2>&1
```

```
# Run Sentinel every five minutes; dump copious amounts of debug information to logfile
SENTINEL_DEBUG=1
*/5 * * * * cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py > /dev/null 2>&1
```

```
# Run Sentinel every five minutes; each run is time stamped in the logs
m0="----Sentinel job started --- pid:"
m1="----Sentinel job completed - pid:" # Not used in this example
t="%b %d %T UTC"
logfile=/var/log/dashcore/sentinel.log

*/5 * * * * cd /var/lib/dashcore/sentinel && date --utc +"$t $m0 $$" >> $logfile && venv/bin/python bin/sentinel.py >> $logfile 2>&1
```

```
# Run Sentinel every 5 to 7 minutes (adding a bit of randomization); each run is time stamped in the logs
m0="----Sentinel job started --- pid:"
m1="----Sentinel job completed - pid:"
t="%b %d %T UTC"
r2min="RANDOM % 121"
r3min="RANDOM % 181"
logfile=/var/log/dashcore/sentinel.log
*/5 * * * * r=$(($r2min)) ; sleep ${r}s ; cd /var/lib/dashcore/sentinel ; date --utc +"$t $m0 $$" >> $logfile && venv/bin/python bin/sentinel.py >> $logfile 2>&1 && date --utc +"$t $m1 $$"
```


#### Turn on TRIM discards for SSD drive mounts

Because of the way SSDs (Solid State Drives) work, saving new data can impact performance. Namely, data marked as "deleted" have to be completely erased before write. With traditional magnetic drives thusly marked data is simply overwritten. Because SSDs have to take this extra step, performance can be impacted.

If, on the other hand, you can alert the operating system that it needs to wipe deleted data in the background, wipes (and deletes) can improve in performance.

Caveats, not all SSDs can support this as of this writing, nor do all variety of filesystem format, and you have to be using a newer linux kernel...

* Am I running at least Linux kernel 3.2?: `uname -a`
* Are my disks formatted as ext4?: `mount | grep ext4`    
  This shows (on my laptop) that `/` (root), `/boot`, and `/home` are formatted as ext4
* Can my SSD support this functionality?:`lsblk --discard`    
  This shows you two things, (1) what devices are at play and (2) do they, and their partitions support TRIM. If you see 0 values under DISC-GRAN and DISC-MAX, then don't continue, your SSD does not support TRIM.    
  On my laptop, I see...
  - 512B for the first and 2G for the second values for all mount points listed above and swap
  - that they are all "luks" encrypted
  - and that there is only one SSD called device "sda". Since I know it is one device "sda" I should also see a filed called "discard_granularity" in "/sys/block/sda/queue/": `ls -l /sys/block/sda/queue/discard_granularity # Does this file exist?`
* Some have noted that LUKS-encrypted mounts may have weakened encryption if    you enable TRIM. I honestly don't know what this means or why, so do further research if this is a concern.

> _Special note: Those the swap partition may be listed for TRIM capable, do not
> set it to take extra action here. The way swap works makes this a non-issue._

Okay. Do you meet those criteria? Continue on..

Read more about this topic here...

* Generally: _[Opensource.com: Solid state drives in Linux: Enabling TRIM for SSDs](https://opensource.com/article/17/1/solid-state-drives-linux-enabling-trim-ssds)_
* Better detail that also addresses LUKS encrypted drives: _[Blog: How to TRIM your encrypted SSD in Fedora 19
](https://lukas.zapletalovi.com/2013/11/how-to-trim-your-ssd-in-fedora-19.html)_


There are three routes you can take to enable TRIMing. (1) add "discard" to you mount settings, and/or (2) set up a cronjob to perform periodic TRIM cleanup of
deleted files, and/or (3) turn on systemd-managed periodic TRIM cleanup. Method 1 can cause undo deletion performance loss (always wiping on every delete) so that is not recommended, instead focus on method 2 or method 3 because they will clean up deleted data periodically as a background process.

**Method 1: "discard" in mount settings**

Described here in order to be complete. This will tell the OS to wipe
upon delete instead of just marking the data. Downside: There is a performance
loss upon deletion.

Edit _fstab_ and add a "discard" parameter to the settings....

```
sudo nano /etc/fstab
```

Replace the line that looks like this (this is an example)...    
`UUID=2865a236-ab20-4bdf-b15b-ffdb5ae60a93 /                       ext4    defaults        1 1`    
...with one that looks like this...    
`UUID=2865a236-ab20-4bdf-b15b-ffdb5ae60a93 /                       ext4    defaults,discard        1 1`


**Method 2: cron job that periodically reaps data marked for deletion**

For performance reasons, this is the recommended method UNLESS you have the TRIM systemd service available to you.

Do you have the systemd service available? `sudo systemctl status fstrim.timer` If your computer says "what the heck is that?" then continue on. If that service is available, you should probably use that (see Method 3).

For my example, I am going to TRIM my `/` and `/home` partitions. My `/boot` partition is read-only 99.999% of the time so write/delete performance is not a consideration.

Edit a new weekly cron job: `sudo nano /etc/cron.weekly/01-fstrim` as such and save...

```
#!/bin/sh
fstrim /
fstrim /home
```

Then make that job executable: `sudo chmod +x /etc/cron.weekly/01-fstrim`

**Method 3: systemd-managed service that periodically reaps data marked for deletion**

For performance reasons, this is the recommended method unless the service is simply unavailable to you. If it is not available, choose "method 2" above.

Do you have the systemd service available? `sudo systemctl status fstrim.timer` If your computer says "what the heck is that?" then choose "method 2" described above.

This is simple to enable...
```
sudo systemctl enable fstrim.timer
sudo systemctl start fstrim.service
```

**Extra step for LUKS-encrypted partitions***

Again, noted: There have been reports that enabling TRIM decreases encryption strength for LUKS encrypted mountpoints. I honestly don't know what this means or why, so do further research if this is a concern.

Take a look at your block device again with `lsblk --discard`. Mine looks like this...

```
[taw@rh ~]$ lsblk --discard
NAME                                          DISC-ALN DISC-GRAN DISC-MAX DISC-ZERO
sda                                                  0      512B       2G         0
├─sda2                                               0      512B       2G         0
│ └─luks-a97ccef7-619b-4cee-8b2c-478f1f96e8e5        0      512B       2G         0
│   ├─fedora_rh-root                                 0      512B       2G         0
│   ├─fedora_rh-swap                                 0      512B       2G         0
│   └─fedora_rh-home                                 0      512B       2G         0
└─sda1                                               0      512B       2G         0
```

And let's take a look at that luks partition with `sudo cat /etc/crypttab`...

```
[taw@rh ~]$ sudo cat /etc/crypttab
luks-a97ccef7-619b-4cee-8b2c-478f1f96e8e5 UUID=a97ccef7-619b-4cee-8b2c-478f1f96e8e5 none
```

...and `sudo cryptsetup status luks-a97ccef7-619b-4cee-8b2c-478f1f96e8e5`...

```
[taw@rh ~]$ sudo cryptsetup status luks-a97ccef7-619b-4cee-8b2c-478f1f96e8e5
/dev/mapper/luks-a97ccef7-619b-4cee-8b2c-478f1f96e8e5 is active and is in use.
  type:    LUKS1
  cipher:  aes-xts-plain64
  keysize: 512 bits
  device:  /dev/sda2
  offset:  4096 sectors
  size:    999184384 sectors
  mode:    read/write
```

You will need to add a `discard` value to that "crypttab" configuration: `sudo nano /etc/crypttab` (edit and save -- a reboot to enable)...

```
luks-a97ccef7-619b-4cee-8b2c-478f1f96e8e5 UUID=a97ccef7-619b-4cee-8b2c-478f1f96e8e5 none discard
```

All done! Good luck. Comments and feedback to <t0dd@protonmail.com>
