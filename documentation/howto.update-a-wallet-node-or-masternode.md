# HowTo: Update the Dash Wallet, Node, or Masternode Software

If you have installed your Dash wallet, node, or masternode using the supplied
RPM packages, updating is super super simple.

_Note1: Major upgrades where there are protocol shifts (for example, the 12.1 to
12.2 was an upgrade not an update). will have their own howto documents
associated. This document only describes less-invasive updates and upgrades._

_Note2: If you need to upgrade your operating system, read this document
instead: [How to Upgrade Your Masternode's Operating System](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.upgrade-the-operating-system.md) 

## How do I know there is a new version available?

If you are interfacing the operating system with a UI (GNOME, for example), it
will tell you within a day or two of a release whether new packages are
available. If you are operating headless though (like most Masternodes), this
is how you check...

```
sudo dnf upgrade --refresh
```

...let's assume there is a new version of the software available...

## Scenario: I have a wallet installed...

Order is not really important in the first two case steps...

* Shut down your wallet
* Update your system...

```
sudo dnf upgrade -y --refresh
```

* Start up your wallet again.
* Done!

## Scenario: I have a node or masternode running as a systemd service

```
# Update the whole operating system along with dash. And then reboot.
sudo dnf upgrade -y --refresh && sudo reboot
```

...or...

```
# Just update. Reboot if you want separately.
sudo dnf upgrade -y --refresh && sudo systemctl restart dashd
```

If you set up email triggers you should have received a shutdown email and a
startup email.

Done!


## Scenario: I have a node or masternode running from my /home/username/.dashcore directory

```
dash-cli stop dashd
sleep 20
sudo dnf upgrade -y --refresh
dashd
```

Done!

---

### Yes, it is that simple.

That's it. That's the power of of good packaging, permissions, and
integration with the operating system.

Got a dash of feedback? Send it my way: <https://keybase.io/toddwarner>
