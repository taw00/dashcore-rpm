# Dash Core Binary (pre-built) RPM Packages<br />for Fedora, CentOS, and Red Hat Enterprise Linux<br />_...wallet, node, and masternode_

This document describes what is available for Fedora, CentOS, and Red Hat
Enterprise Linux (RHEL) users seeking natively compiled Dash Core software. This
document will also guide those users through the process of configuring their
systems to easily install, verify, and update that software. Once configured,
updating Dash Core software will be just as trivial as updating the rest of
their system.

> What is Dash? [dash.org](https://dash.org/), [official documentation](https://dashpay.atlassian.net/wiki/display/DOC/Official+Documentation)<br />
> What is a Masternode? <https://dashpay.atlassian.net/wiki/display/DOC/Masternode><br />
> What are these Linuxes? [Fedora](https://getfedora.org/), [CentOS](https://www.centos.org/), [RHEL](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux)<br />
> ...<br />
> If you know your way around yum, dnf, and Dash Core, I could reduce this document to two lines...<br />
> **dashcore-fedora.repo:** <https://github.com/taw00/dashcore-rpm/blob/master/dashcore-feodra.repo><br />
> **dashcore-centos.repo:** <https://github.com/taw00/dashcore-rpm/blob/master/dashcore-centos.repo><br />
> Otherwise, keep reading.


## *"TL;DR -- I just want to install the Dash Core GUI Wallet!"*

Proper packaging and repositories make installation trivial. For this example,
and to keep things simple, let's assume are installing your wallet on a Fedora
23 linux desktop (the only Fedora version supported by the stable Dash Core
Wallet at the moment).

Assuming you are logging in as a normal user who has sudo priviledges.<br />
At the terminal command line...

```
cd /etc/yum.repos.d/
sudo curl https://raw.githubusercontent.com/taw00/dashcore-rpm/master/dashcore-fedora.repo -o dashcore-fedora.repo
cd -
sudo dnf install -y dash-qt
dash-qt
```

Boom! Done! You should now see a Dash Core GUI Wallet open up on your screen.

## *"Okay, I was overconfident, let's walk through it a bit."*

Configuration to automate install and update of Dash Core for your version of
linux can be found here...<br />
For Fedora: <https://github.com/taw00/dashcore-rpm/blob/master/dashcore-fedora.repo><br />
For CentOS and RHEL: <https://github.com/taw00/dashcore-rpm/blob/master/dashcore-centos.repo>

If you want to browse the actual repository, or manually download packages, they
can be found here:
<https://toddwarner.keybase.pub/repo/dashcore/>

All you have do to configure your Linux system is to download and copy the appropriate
`dashcore-*.repo` file into your package manager configuration directory and you
will be ready to rock-and-roll with the Dash Core software.

> #### Additional reference information
>
> If you are interested in building your own RPM packages from source, those can
be found here: <https://github.com/taw00/dashcore-rpm>
>
> If you are looking for Dash wallets for other platforms, those can be found here:
<https://www.dash.org/downloads/>
>
> **General Documentation:** <https://dashpay.atlassian.net/wiki/pages/><br />
  **Masternode Documentation:** <https://dashpay.atlassian.net/wiki/display/DOC/Masternode>


## Configuring your system to have access to the Dash Core RPM repositories

We are going to do this at the command line from an account that has `sudo`ers
access. Log into a terminal and do this...

*...if using Fedora:*

```
cd /etc/yum.repos.d/
sudo curl https://raw.githubusercontent.com/taw00/dashcore-rpm/master/dashcore-fedora.repo -o dashcore-fedora.repo
cd -
```

*...if using CentOS or RHEL*

```
cd /etc/yum.repos.d/
sudo curl https://raw.githubusercontent.com/taw00/dashcore-rpm/master/dashcore-centos.repo -o dashcore-centos.repo
cd -
```

That's it! You are now configured to install Dash Core through your package
manager.

## List what's available

Want to see what packages are available? Do this (Fedora) `sudo dnf list|grep
dashcore`, or again for CentOS or RHEL, `sudo yum list|grep dashcore`. You
should get a nice listing of all the packages available to your linux system.

## Stable versus Unstable

By default, those `*.repo` files configure your system to only pull from the
"stable" repository.

If you want install the "unstable" software instead, do this:<br />

*...fedora:*

```
sudo dnf config-manager --set-disabled dashcore-stable
sudo dnf config-manager --set-enabled dashcore-unstable
sudo dnf list|grep dashcore
```

*...centos or rhel:*

```
sudo yum-config-manager --disable dashcore-stable
sudo yum-config-manager --enable dashcore-unstable
sudo yum list|grep dashcore
```

The listing command at the end isn't required, but it is helpful to show that
the version of what software is available just changed.

> Critical: If you are just testing things, remember to enable testnet in your
`dash.conf` file. If testnet, ensure you have `testnet=1` set.

To switch back to the stable repositories, just flip-flop the enable/disable
command line switches above and re-run those commands.

## Installing or Upgrading Dash Core software

If you have configured things appropriately. Installation is truly this easy...

***To install the non-graphical version of the software: `dashd`***

*...fedora:*

```
sudo dnf install dashcore-server
```

*...centos or RHEL:*

```
sudo yum install dashcore-server
```

The operating system's package manager will automagically pull in any
dependencies, give you a list, and ask you if you are sure. You will see that
for `dashcore-server`, `dashcore-utils` will also be installed. It's a needed
dependency because it contains the `dash-cli` command line utility.

You want the GUI wallet instead? Say "N"o to that installation request, run the
same command as above, but choose `dashcore-client` instead. YUM and DNF also
automatically check to see if they packages are digitally signed appropriately
and if the files are corrupt. Fancy. If you are familiar with `apt-get`, it's
more or less the same thing.

**Future upgrades...**

Let's say you see on the <https://dash.org/forum> that a new version of Dash
Core was released. You want your system updated as soon as possible. Just do this...

*...fedora:*

```
sudo dnf upgrade
```

*...centos or RHEL:*

```
sudo yum update -y
```

Notice that `-y`? That means... "I choose YES! Update everything!"

Nothing listed? Try again in a couple days... Todd may have been visiting his
mother.

#### Good luck! Send me feedback.<br />
\-*t0dd@protonmail.com*

----

> *"Okay, let's talk about what's available and for what versions..."*

----

# Currently available

## Stable: **0.12.0.58**

**Dash Core 12.0 is supported on these linux versions: Fedora 23, CentOS7 / RHEL7**

Q: Fedora 23? Why not newer Fedora?<br />
A: There are library issues with the lastest (24+) versions of Fedora Linux for v0.12.0

Q: I see CentOS packages but nothing *specific* to RHEL, why is that?
A: Because CentOS packages will run just fine on RHEL.

**Default Dash data directory for v12.0:** `/home/<username>/.dash/`


## Unstable / Experimental: **0.12.1**

**Currently, the unstable Dash Core 12.1 builds are supported on these linux
versions: Fedora 24, 25 & CentOS7 / RHEL7**

This experimental version represents efforts surrounding current **Testnet
Testing** for the next major version of the software which should ship (become
the new "stable" version) on February 5, 2017.

**Default testnet Dash data directory for v12.1 (normal user):** `/home/<username>/.dashcore/`<br />
**Default testnet Dash data directory for v12.1 (`systemd` setup):** `/var/lib/dashcore/` _(see masternode setup below)_

**Announcement and getting started instruction:** <https://www.dash.org/forum/threads/12-1-testnet-testing-phase-two-ignition.10818/><br />
**Testnet documentation:** <https://dashpay.atlassian.net/wiki/display/DOC/Testnet><br />
**Testnet Masternode setup:** <https://github.com/taw00/dashcore-rpm/blob/master/documentation>

### An important note about `Sentinel`

A significant change for version 12.1 is the addition of new tooling called
**Sentinel**. If you are operating a v12.1 masternode, Sentinel needs to be
installed as well. Please reference the v12.1 **"Testnet Masternode setup"**
documentation linked above for more information.

----

> *"Holy cow! All that and... What the heck is Dash!?! And what are these packages in these Dash Core repositories!?!"*

----

## Dash is Digital Cash

**Dash (Digital Cash)** is an open source peer-to-peer cryptocurrency that
offers instant transactions ***(InstantSend)***, private transactions
***(PrivateSend)*** and token fungibility. Dash operates a decentralized
governance and budgeting system, making it ***the first Decentralized Autonomous
Organization (DAO)***. Dash is also a platform for innovative decentralized
crypto-tech. Dash is open source and the name of the overarching project. Learn
more at <http://www.dash.org>

The RPMs

* **dashcore-client** -- The dash-qt wallet and full node.

* **dashcore-utils** -- dash-cli, a utility to communicate with and control a
  Dash server via its RPC protocol, and dash-tx, a utility to create custom Dash
  transactions.

* **dashcore-server** -- dashd, a peer-to-peer node and wallet server. It is the
  command line installation without a GUI.  It can be used as a commandline
  wallet but is typically used to run a Dash Masternode (runs ideally as a
  serviced daemon). *Requires `dashcore-utils` to be installed as well.*

* **dashcore-libs** -- provides libbitcoinconsensus, which is used by third
  party applications to verify scripts (and other functionality in the future).

* **dashcore-devel** -- provides the libraries and header files necessary to
  compile programs which use libbitcoinconsensus. *Requires `dashcore-libs` to
  be installed as well.*

* **dashcore-[*version info*].src.rpm** -- The source code -- the source RPM, or
  SRPM. You want to build binaries for your RPM-based linux distribution? Use
  this source RPM to do so easily.

* **dashcore-debuginfo** -- debug information for package dash. Debug
  information is useful when developing applications that use this package or
  when debugging this package. (*99.999% of you do not need to install this*)


#### Acknowledgment

It is important to note and acknowledge that I referenced the good work that
Michael Hampton did with his Bitcoin packages. His work can be found here:
<https://www.ringingliberty.com/bitcoin/> His hard work helped me get to working
builds faster.

#### Good luck!

Got a dash of feedback? *...har har...* Send it my way <t0dd@protonmail.com>    
And of course, donations welcome: [XyxQq4qgp9B53QWQgSqSxJb4xddhzk5Zhh](dash:XyxQq4qgp9B53QWQgSqSxJb4xddhzk5Zhh)



----

| Changes |
| ------- |
| 2017-01: Rewrote Dash Masternode documentation and updated the reference to it here. |
| 2017-01: Moved this file from [here](https://gist.github.com/taw00/b2382aaabb321b0cf9ce104185e1b3b7) to here. |
| 2016-09 -through- 2017-01: Updated testnet/experimental packages. |
| 2016-12-03: Complete overhaul and simplification because we now have packages in a real repository |
| 2016-12-02: [Moved these instructions to github](https://gist.github.com/taw00/b2382aaabb321b0cf9ce104185e1b3b7) |
| 2016-11-28: Added [testnet masternode setup instruction](https://gist.github.com/taw00/e978f862ee1ad66722e16bcc8cf18ca5) |
| 2016-08-22: Built, packaged, signed, and uploaded RHEL7 and CentOS7 versions of 0.12.0.58 |
| 2016-06-17: 0.12.0.58 is now the most stable (built, signed, and provided) -- 0.12.0.56 deprecated. |
| 2016-04-13: dash-\*.rpm renamed to dashcore-\*.rpm - updated versions of all packages |
| 2016-04-10: updated versions of all packages |
| 2016-04-06: gpg signed all the packages |
| 2016-04-05: 0.12.0.56-4.taw and 0.12.0.56-5.taw and 0.12.1.x- and 0.13.0.x- (now removed) |
| 2016-04-04: 0.12.0.56-3.taw (now removed) |
| 2016-04-04: 0.12.0.56-0.taw2 (now removed) |
| 2016-04-02: 0.12.0.56-0.taw0 (now removed) |
