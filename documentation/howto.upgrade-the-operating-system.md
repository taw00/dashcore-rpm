# How To Upgrade Your Masternode's Operating System

_**Introduction**_

**RHEL/CentOS:**  
If you are using Red Hat Enterprise Linux, or CentOS as your base operating
system, as of Dash Core 0.13.0, you _must_ migrate to Fedora Linux. RHEL7 and
CentOS7 are incredibly stable, but, they are also significantly dated to the
point that they can no longer be maintained as target platforms for v0.13.

Dash is a leading edge technology and Fedora is plenty stable and reasonably
bullet proof. In order to migrate from RHEL or CentOS to Fedora, I would
recommend backing up your masternode configuration and then just rebuilding the
system from the ground up. Trying to do any kind of fancy automation may lead to
mixed results.

**Fedora:**  
A new version of Fedora is released approximately every 6 months and is patched
almost nightly. That means you need to upgrade it regularly. If you are running
a Fedora Linux machine two full versions behind the latest, you need to upgrade
pronto, otherwise, the next discovered security vulnerability will likely leave
you at risk. Plus, I will stop building for those old platforms (two releases
back) not long after new a release is rolled out. If you are running a
Masternode on a dated Fedora Linux system... upgrade. If you are running a
Masternode on top of a version one release back, you may have some time, but
schedule time to upgrade keeping up with the latest.

***Assumptions:***

1. You have backed up your Masternode configuration and can respond in case of
   catastrophe
2. You have installed and manage your Masternode using the instructions
   provided by this github repository: <https://github.com/taw00/dashcore-rpm/>


### Upgrading Fedora Linux is exceedingly simple

Upgrading the operating system from one major version to the next takes me
approximately 5 minutes to perform (speed of internet connection dependent). And
the instructions can't be much simpler. This example uses Fedora 31 as the
target version of the upgrade.

1. Update your current version of Fedora to all its latest packages.

```
# Update everything and clean up any cruft...
# (you may not have the flatpak command or any flatpaks installed)
sudo dnf upgrade --refresh -y
sudo flatpak update
sudo dnf clean packages
```

2. Perform the upgrade (Example: upgrading to Fedora Linux 31)

```
# Download upgrade package.
sudo dnf install dnf-plugin-system-upgrade -y
# Download upgraded packages (using F31 as the example target OS version)
sudo dnf system-upgrade download --refresh -y --releasever=31
# Upgrade (after stopping the masternode (pedantic and not required))
#sudo systemctl stop dashcore
sudo dnf system-upgrade reboot
```

3. Log back in and check the status.

```
# Check that we are running the latest versions of the operating system and
# dashcore
sudo rpm -qa | grep release
sudo rpm -qa | grep dashcore
```

4. Clean up cached upgrade data

```
# Once you are ready (not that you can go back), clean up all the cached data
# from the upgrade process
sudo dnf system-upgrade clean
sudo dnf clean packages
```


Your Dash Masternode should be up and running just fine, but examine it and
monitor until satisfied. Troubleshooting guidance can be found here:
[Dash Core Troubleshooting Guide](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.dashcore-troubleshooting.md)

That's it! Your done.
