# HowTo: Deploy and Configure a Fedora Linux Operating System
***...to serve as a platform for a Dash Core Node or Masternode***

**Table of Content**

<!-- TOC START min:2 max:3 link:true update:true -->
- [Install the operating system](#install-the-operating-system)
- [Install and Configure FirewallD](#install-and-configure-firewalld)
- [Further secure the operating system](#further-secure-the-operating-system)
- [ALL DONE!](#all-done)
- [Improve SSD Write & Delete Performance for Linux Systems by Enabling ATA TRIM](#improve-ssd-write--delete-performance-for-linux-systems-by-enabling-ata-trim)

<!-- TOC END -->


## Install the operating system

There are two primary means to install the operating system that will covered
here. (1) Via a cloud service, like Vultr.com, or (2) via a traditional
bare-metal blade, server, white-box, whatever.

The objectives are straight-forward:

1. Install a minimal OS
2. Ensure there is enough swap-space configured
3. Configure SSH so you can log in without a password into root and a normal
   user who has sudo'ers rights
4. Fully update and reboot

> A note about minimum requirements. Masternodes are no longer "glorified full
> nodes". They are doing more and more things and they will need beefier specs
> over time. I recommend at least 2G RAM and 4G swap (twice ram-size) today.
> This will increase over time. 4G RAM is not a bad idea either.

***A cloud service installation, for example Vultr***

**Install to Vultr**
  - Browse to https://my.vultr.com/
  - Create an account and login.
  - Click the ( + ) button.
  - Choose: 64 bit OS and Fedora
  - Choose: 2048MB RAM, 2CPU 45GB SSD (consider a 4GB RAM system).
  - Set up SSH keys. It will make your life more pleasant.
    [Vultr.com provides pretty solid instruction](https://www.vultr.com/docs/how-do-i-generate-ssh-keys)
    on this process.
  - Pick a hostname, `master00`, or whatever.
  - Deploy!

**Post install on Vultr**

  - **Test and troubleshoot your SSH settings** &mdash; ssh into your Vultr
    instance: `ssh root@<IP ADDRESS OF YOUR INSTANCE>` If you set up ssh keys
    right, it should just log you right in. If not, log in using your root
    password and troubleshoot why your ssh key setup is not working right and get
    it working (see above) so that you don't need a password to ssh into your
    system.
  - **Change your root password** &mdash; `passwd` &mdash; to something longer
    and ideally random. I use [Lastpass](https://www.lastpass.com/) to generate
    passwords.
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

Vulr mysteriously starts you with no swap. A reasonable
[rule of thumb](https://github.com/taw00/howto/blob/master/howto-configure-swap-file-on-linux.md)
is to configure swap to be twice the size of your RAM. Swap-size is more art
than science, but your system will be brutalized occassionally... 2-times your
RAM is a good choice.

```
# As root...
sudo su -

# Each "bs" setting below corresponds to a swapfile size based on a multiple.
# I.e., If you want a swapfile 2-times the size of your RAM, choose 2048:
#bs=512  # 1/2 times the size of RAM
#bs=1024 # One times the size of RAM
bs=2048  # Twice the size of RAM -- recommended if you are in doubt
#bs=1536 # 1.5 times the size of RAM

# Create the swapfile
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


***A traditional bare-metal server installation***

I leave it as an exercise for the reader to perform a bare-metal installation
of  Fedora, CentOS, or even RHEL. For Fedora, go here - https://getfedora.org/
For CentOS, go here - https://www.centos.org/download/ For Fedora, I recommend
the "Server" install. You need only a minimum configuration. Dependency
resolution of installed RPM packages per these instructions will bring in
anything you need.

Ensure that your bare-metal server meets at least these requirements:

* 2GB RAM
* 40 GB disk

As you walk through the installation process, choose to enable swap, it needs
to be at least equal to the size of RAM, 2GB and ideally twice that, 4GB.

Once installed, follow similar process as the Vultr VPS example for SSH configuration.


***Post OS installation: create user...***

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

# If you are using ubuntu instead of a Red Hat derivative, replace 'wheel' with 'sudoers'
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



***Post OS installation: fully update the system and reboot***

Log in as `mnuser` and...

...if this is Fedora

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


## Install and Configure FirewallD

**Install**

```
sudo dnf install -y firewalld
```

<!--
...if this is CentOS or Red Hat Enterprise Linux

```
sudo yum install -y dashcore-server firewalld
```
-->

**Configure**

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

# Whatever that default zone is, that is the starting conditions for your
# configuration. For this example, I am going to demonstrate how to edit my
# default configuration on my Fedora Linux system: FedoraServer. You _could_
# create your own zone definition, but for now, we will be editing the
# configuration that is in place.

# FedoraServer usually starts with ssh, dhcp6-client, and cockpit opened up
# I want to allow SSH and masternode traffic, but I don't want cockpit running
# all the time and by having a static IP, dhcpv6 service is unneccessary.
sudo firewall-cmd --permanent --add-service ssh
sudo firewall-cmd --permanent --remove-service dhcpv6-client
sudo firewall-cmd --permanent --remove-service cockpit

# Rate limit incoming ssh and cockpit (if configured on) traffic to 10/minute
sudo firewall-cmd --permanent --add-rich-rule='rule service name=ssh limit value=10/m accept'
#sudo firewall-cmd --permanent --add-rich-rule='rule service name=cockpit limit value=10/m accept'

# did it take?
sudo firewall-cmd --reload
sudo firewall-cmd --state
sudo firewall-cmd --list-all
```

_After you `--list-all`, if you see a service you do not wish to be available,
feel free to remove it following the pattern we demonstrated above._


**Some references:**

* FirewallD documentation: <https://fedoraproject.org/wiki/Firewalld>
* Rate limiting as we do above: <https://www.rootusers.com/how-to-use-firewalld-rich-rules-and-zones-for-filtering-and-nat/>
* More on rate limiting: <https://serverfault.com/questions/683671/is-there-a-way-to-rate-limit-connection-attempts-with-firewalld>
* And more: <https://itnotesandscribblings.blogspot.com/2014/08/firewalld-adding-services-and-direct.html>
* Interesting discussion on fighting DOS attacks on http: <https://www.certdepot.net/rhel7-mitigate-http-attacks/>
* Do some web searching for more about firewalld


## Further secure the operating system

Review [Configure FirewallD and Fail2Ban on a Dash Masternode](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.secure-your-dashcore-node.md). From experience, I can tell you that your node will be under regular attack. Make it more difficult for people.


&nbsp;

## ALL DONE!

If all went well, you have an efficient, working, and secure system prepared to
run a Dash Core Node or Masternode, or really any workload. I hope this was
helpful.

Got a dash of feedback? *...har har...* Send it my way <https://keybase.io/toddwarner>    

&nbsp;

&nbsp;

---

# Appendix - Advanced Topics

## Improve SSD Write & Delete Performance for Linux Systems by Enabling ATA TRIM

Because of the way SSDs (Solid State Drives) work, saving new data can impact performance. Namely, data marked as "deleted" have to be completely erased before write. With traditional magnetic drives, data marked for deletion is simply overwritten. Because SSDs have to take this extra step, performance can be impacted and slowly worsens over time.

If, on the other hand, you can alert the operating system that it needs to wipe deleted data in the background, writes (and deletes) can improve in performance.

To learn more, follow this link: <https://github.com/taw00/howto/blob/master/howto-enable-ssd-trim-for-linux.md>
