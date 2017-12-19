# How To Upgrade Your Masternode's Operating System

***Introduction***

RHEL/CentOS: If you are using Red Hat Enterprise Linux, or CentOS as your base
operating system, I recommend you switch to Fedora Linux. RHEL and CentOS are
less bleeding edge, but, they are also significantly dated. Dash is a leading
edge technology and Fedora is plenty stable and bullet proof. In order to
migrate from RHEL or CentOS to Fedora, I would recommend backing up your
masternode configuration and then just rebuilding the system from the ground
up. Trying to do any kind of fancy automation may lead to mixed results.

Fedora: Fedora releases a new version roughly every 6 months. That means you
need to upgrade it periodically. If you are running a Fedora Linux machine two
versions behind the latest, you need to upgrade pronto, otherwise, the next
discovered security vulnerability will leave you at risk. Plus, I will stop
building for those old platforms not long after. For example, Fedora 27 is the
lastest version, and Fedora 25 is now out of service. If you are running a
Masternode on a Fedora Linux 25 system... upgrade. If you are running a
Masternode on top of a Fedora Linux 26 system, you have some time, but consider
keeping up with the latest.

***Assumptions:***

1. You have backed up your Masternode configuration and can respond to
   catastrophe
2. You have installed and manage your Masternode using the instructions
   provided by this github repository: <https://github.com/taw00/dashcore-rpm/>


### Upgrading Fedora Linux is exceedingly simple

Upgrading the operating system takes me roughly 5 minutes to perform (speed of
internet connection dependent). And the instructions can't be much simpler.
This example uses Fedora 27 as the target version of the upgrade.

1. Update your current version of Fedora to all it's latest packages.

```
# Update everything and clean up any cruft...
# (you may not have the flatpak command or any flatpaks installed)
sudo dnf upgrade --refresh -y
sudo flatpak update
sudo dnf clean packages
```

2. Perform the upgrade.

```
# Download upgrade package.
sudo dnf install dnf-plugin-system-upgrade -y
# Download upgraded packages (using F27 as the example target OS version)
sudo dnf system-upgrade download --refresh -y --releasever=27
# Upgrade!
sudo dnf system-upgrade reboot
```

3. Log back in and check the status.

```
# We should be on Fedora 27 for this example...
sudo rpm -qa | grep release
sudo rpm -qa | grep dashcore
```

Your Dash Masternode should be up and running just fine, but examine it and
watch it until satisfied. Troubleshooting guidance can be found here:
<https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.dashcore-troubleshooting.md>

That's it! Your done.
