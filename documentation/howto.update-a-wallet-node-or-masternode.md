# HowTo: Update the Dash Wallet, Node, or Masternode Software

Since you have installed your Dash wallet, node, or masternode using the supplied
RPM packages, upgrading is super super simple.

## How do I know there is a new version available?

The operating system will tell you within a day or two of a release whether new
packages are available. Or you can check with a...

```
sudo dnf upgrade --refresh
```

...let's assume there is a new version of the software available...

## I have a wallet installed...

Order is not really important in the first two case steps...

* Shut down your wallet
* Update your system...

```
sudo dnf upgrade -y --refresh
```

* Start up your wallet again.

## I have a node or masternode running as a systemd service

```
# I certainly have other updates. Let's update everything and reboot.
sudo dnf upgrade -y --refresh && sudo reboot
```

...or...

```
# I have updates, but I don't want to reboot right now.
sudo dnf upgrade -y --refresh && sudo systemctl restart dashd
```

If you set up email triggers you should have received a shutdown email and a
startup email.


## I have a node or masternode running from my /home/username/.dashcore directory

```
dash-cli stop dashd
sleep 20
# If you don't want to reboot, stop the command at --refresh
sudo dnf upgrade -y --refresh && sudo reboot
```

...and then after update and reboot...

```
dashd
```

---

### Yes, it is that simple.

Yup. That's it. That's the power of of good packaging, permissions, and
integration with the operating system.

Comments, questions, donations - <https://keybase.io/toddwarner>
