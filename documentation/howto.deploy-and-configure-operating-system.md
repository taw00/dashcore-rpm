# HowTo: Deploy and Configure a Fedora Linux Operating System
***...to serve as a platform for a Dash Core Node or Masternode***

Note: These are instruction for deploying a base- or minimal- system. No dash
related configurations are made here. We describe those elsewhere.

## Summary -- the objectives are straight-forward:

<!-- TOC START min:2 max:2 link:true update:true -->
- [Summary -- the objectives are straight-forward:](#summary----the-objectives-are-straight-forward)
- [[1] Deploy a minimal operating system](#1-deploy-a-minimal-operating-system)
- [[2] Fully update the system and reboot](#2-fully-update-the-system-and-reboot)
- [[3] Create user, setup SSH and sudo access...](#3-create-user-setup-ssh-and-sudo-access)
- [[4] Minimize root user exposure](#4-minimize-root-user-exposure)
- [[5] Install and Configure FirewallD](#5-install-and-configure-firewalld)
- [[6] Install and Configure Fail2Ban](#6-install-and-configure-fail2ban)
- [ALL DONE!](#all-done)
- [Appendix - Advanced Topics](#appendix---advanced-topics)

<!-- TOC END -->

> A note about minimum requirements. Masternodes are no longer "glorified full
> nodes". They are doing more and more things and they will need beefier specs
> over time. I recommend at least 2G RAM and 4G swap (twice ram-size) today.
> This will increase over time. 4G RAM is not a bad idea either.

## [1] Deploy a minimal operating system

There are two primary means to install the operating system that will covered
here. (1) Via a cloud service, like Vultr.com, or (2) via a traditional
bare-metal blade, server, white-box, whatever.

### Example: A cloud service installation, for example Vultr

**Deploy to Vultr**
  - Browse to https://my.vultr.com/
  - Create an account and login.
  - Click the ( + ) button.
  - Choose: 64 bit OS and Fedora
  - Choose: 2048MB RAM, 2CPU 45GB SSD (consider a 4GB RAM system).
  - Set up SSH keys. This will make your life more pleasant and secure.
    [Vultr.com provides pretty solid instruction](https://www.vultr.com/docs/how-do-i-generate-ssh-keys)
    on this process.
  - Pick a hostname, `master00`, or whatever.
  - Deploy!

**Post initial deployment to Vultr**

  - **Test and troubleshoot your root SSH settings** &mdash; ssh into your Vultr
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


### Example: A traditional bare-metal server installation

I leave it as an exercise for the reader to perform a bare-metal installation
of  Fedora, CentOS, or even RHEL. For Fedora, go here - https://getfedora.org/
For CentOS, go here - https://www.centos.org/download/ For Fedora, I recommend
the "Server" install. You need only a minimum configuration. Dependency
resolution of installed RPM packages per these instructions will bring in
anything you need.

Ensure that your bare-metal server meets at least these requirements:

* 2GB RAM
* 40 GB disk
* 4GB (or 2x RAMsize) Swap

As you walk through the installation process, choose to enable swap, it needs
to be at least equal to the size of RAM, 2GB and ideally twice that, 4GB.

Once installed, follow similar process as the Vultr VPS example for SSH configuration.



## [2] Fully update the system and reboot

Log in as `mnuser` and...

```
# If Fedora...
dnf upgrade -y
reboot

# If CentOS7 or RHEL7...
#yum install -y epel-release
#yum update -y
#reboot
```


## [3] Create user, setup SSH and sudo access...

During the installation process using the wizard you will likely be asked to
create a user. Do it. Additionally, choose to give this user administration
rights (they will be able to `sudo`).

While you can do that during the set up process, included here is the
post-installation instruction for doing the same thing. The username in this
example is `mnuser`...

```
# Log into the system as root user.
# If the user does not exist, do this...
useradd -G wheel mnuser
passwd mnuser

# If the user already exists, do this...
# Fedora/CentOS/RHEL example
usermod -a -G wheel mnuser
# Ubuntu example
#usermod -a -G sudoers mnuser
```

**IMPORTANT:** Work through the SSH instructions (see Vultr example) and set it
up so you can ssh into the system as your normal user without a password from
your desktop system.


> ***Recommendation1:***
> Choose a difficult scrambled password for both `root` and your `mnuser` user.
> Then ensure ssh keys are set up so you can ssh to the instance without having
> to type passwords.

> ***Recommendation2:***
> Edit the `/etc/sudoers` configuration file and uncomment the `%wheel` line
> that includes the `NOPASSWD` qualifier. This will allow you to `sudo` as the
> `mnuser` user without having to cut-n-paste a password all the time.



## [4] Minimize root user exposure

***Turn off SSH logins for root...***

Attackers _love_ to attempt to login to root via SSH. Turn that off.

* Edit `/etc/ssh/sshd_config` and either add or edit these lines (add only if
  these settings do not yet exist)

```
# Note: "mnuser" is our example user. You can/should list any usernames for
# which you have enabled sudo access and set up a ssh
PermitRootLogin no
AllowUsers mnuser
```
* Restart sshd: `sudo systemctl restart sshd`



## [5] Install and Configure FirewallD

As a normal user (example `mnuser`)...

**Install**

```
# If Fedora...
sudo dnf install -y firewalld

# If CentOS7 or RHEL7...
sudo yum install -y dashcore-server firewalld
```


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


## [6] Install and Configure Fail2Ban

### Install `fail2ban`...

```
# If Fedora...
sudo dnf install -y fail2ban fail2ban-systemd

# If CentOS or RHEL
#sudo yum install epel-release # if not already installed
#sudo yum install -y fail2ban fail2ban-systemd

# If Debian or Ubuntu
#sudo apt install -y fail2ban
```

If you are not using FirewallD, and instead are using IPTables for your
firewall, uninstall fail2ban-firewalld (for the Red Hat-based systems only).

```
# If Fedora...
sudo dnf remove -y fail2ban-firewalld

# If CentOS or RHEL
#sudo yum remove -y fail2ban-firewalld
```

### Configure `fail2ban`...

Edit `/etc/fail2ban/jail.d/local.conf` _(Optionally `/etc/fail2ban/jail.local`
instead)_


Copy this; paste; then save...

```
[DEFAULT]
# Ban hosts for one hour:
bantime = 3600

# Flip the comments here if you use iptables instead of firewalld
#banaction = iptables-multiport
banaction = firewallcmd-ipset

# Enable logging to the systemd journal
backend = systemd

# Email settings - Optional - Configure this only after send-only email is
# enabled and functional at the system-level.
#destemail = youremail+fail2ban@example.com
#sender = burner_email_address@yahoo.com
#action = %(action_mwl)s


[sshd]
enabled = true
```

For more about setting up "send-only email", read
[this](https://github.com/taw00/howto/blob/master/howto-configure-send-only-email-via-smtp-relay.md).


### Enable `fail2ban` and restart...

```
sudo systemctl enable fail2ban
sudo systemctl restart fail2ban
```

### Monitor / Analyze

Watch the IP addresses slowly pile up by occasionally looking in the SSH jail...

```
sudo fail2ban-client status sshd
```

Also watch...

```
sudo journalctl -u fail2ban.service -f
```

...and...

```
sudo tail -F /var/log/fail2ban.log
```

### Reference:

* <https://fedoraproject.org/wiki/Fail2ban_with_FirewallD>
* <https://en.wikipedia.org/wiki/Fail2ban>
* <http://www.fail2ban.org/>



&nbsp;

---

## ALL DONE!

If all went well, you have an efficient, working, and secure system prepared to
run a Dash Core Node or Masternode, or really any workload. I hope this was
helpful.

Got a dash of feedback? *...har har...* Send it my way <https://keybase.io/toddwarner>    

&nbsp;

&nbsp;

---

## Appendix - Advanced Topics

### Improve SSD Write & Delete Performance for Linux Systems by Enabling ATA TRIM

Because of the way SSDs (Solid State Drives) work, saving new data can impact performance. Namely, data marked as "deleted" have to be completely erased before write. With traditional magnetic drives, data marked for deletion is simply overwritten. Because SSDs have to take this extra step, performance can be impacted and slowly worsens over time.

If, on the other hand, you can alert the operating system that it needs to wipe deleted data in the background, writes (and deletes) can improve in performance.

To learn more, follow this link: <https://github.com/taw00/howto/blob/master/howto-enable-ssd-trim-for-linux.md>
