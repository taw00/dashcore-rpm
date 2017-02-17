# Configure FirewallD and Fail2Ban on a Masternode Server

## FirewallD

*Note: Firewall rules can be a complicated topic. These are bare bones
git-er-done instructions. You may want to investigate further refinement. It
will get you started though.*

#### Install `firewalld`

```
# If Fedora...
sudo dnf install -y firewalld # Probably already installed
# If CentOS or RHEL...
sudo yum install -y firewalld # Probably already installed
# If Debian or Ubuntu
sudo apt install -y firewalld
```

#### Configure `firewalld`

```
# Is firewalld running? If not, turn it on
sudo firewall-cmd --state
sudo systemctl start firewalld.service
```

```
# Enable firewalld to start upon boot
sudo systemctl enable firewalld.service
```

```
# Determine what the default zone is.
# On vultr, for example, default zone is "FedoraServer"
# On Ubuntu, it will often be "public", just replace "FedoraServer" with what you are using below.
sudo firewall-cmd --get-default-zone
sudo firewall-cmd --get-active-zone
```

Whatever zone, came up, that is the starting conditions for your configuration.
For this example, I am going to demonstrate how to edit my default configuration
on my Fedora Linux system: FedoraServer. You _could_ create your own zone
definition, but for now, we will be editing the configuration that is in place.

```
# FedoraServer usually starts with ssh, dhcp6-client, and cockpit opened up
# I want ssh. dhcpv6 should be unneccessary for a static IP host, and cockpit
# is something used intermittently. And of course, we want the dash full
# node/masternode ports available.
sudo firewall-cmd --permanent --add-service ssh
sudo firewall-cmd --permanent --remove-service dhcpv6-client
#sudo firewall-cmd --permanent --add-service cockpit
sudo firewall-cmd --permanent --remove-service cockpit

# Open up the Mastnernode port (service files provided by our RPM packages)
sudo firewall-cmd --permanent --add-service dashcore-node
#sudo firewall-cmd --permanent --add-service dashcore-node-testnet

# If you are running a masternode that was not installed via our RPM packages,
# you must be explicit in your port configuration - if dashcore-node can be
# done above, just delete these lines.
#sudo firewall-cmd --permanent --add-port=19999/tcp
#sudo firewall-cmd --permanent --add-port=9999/tcp

# Rate limit incoming ssh and cockpit (if configured) traffic to 10 requests per minute
sudo firewall-cmd --permanent --add-rich-rule='rule service name=ssh limit value=10/m accept'
sudo firewall-cmd --permanent --add-rich-rule='rule service name=cockpit limit value=10/m accept'
# Rate limit incoming dash node (and masternode) traffic to 10 requests per second
# TODO: Need to find a good setting for this yet. For now... keep it unset.
#sudo firewall-cmd --permanent --add-rich-rule='rule service name=dashcore-node limit value=10/s accept'
#sudo firewall-cmd --permanent --add-rich-rule='rule service name=dashcore-node-testnet limit value=10/s accept'

# did it take?
sudo firewall-cmd --reload
sudo firewall-cmd --state
sudo firewall-cmd --list-all
```

#### Some references:

* FirewallD documentation: <https://fedoraproject.org/wiki/Firewalld>
* Rate limiting as we do above: <https://www.rootusers.com/how-to-use-firewalld-rich-rules-and-zones-for-filtering-and-nat/>
* More on rate limiting: <https://serverfault.com/questions/683671/is-there-a-way-to-rate-limit-connection-attempts-with-firewalld>
* And more: <https://itnotesandscribblings.blogspot.com/2014/08/firewalld-adding-services-and-direct.html>
* Interesting discussion on fighting DOS attacks on http: <https://www.certdepot.net/rhel7-mitigate-http-attacks/>
* Do some web searching for more about firewalld

----

## Fail2Ban

Fail2ban analyzes log files for folks trying to do bad things on your system.
It doesn't have a lot of breadth of functionality, but it can be very
effective, especially against folks poking SSH.

#### Install `fail2ban`...
```
# If Fedora...
sudo dnf install -y fail2ban
# If CentOS or RHEL
sudo yum install epel-release # if not already installed
sudo yum install -y fail2ban
# If Debian or Ubuntu
sudo apt install -y fail2ban
```

#### Configure `fail2ban`...

Edit `/etc/fail2ban/jail.local`
```
sudo nano /etc/fail2ban/jail.local
```

COPY-AND-PASTE this and save...
```
[DEFAULT]
# Ban hosts for one hour:
bantime = 3600

# Override /etc/fail2ban/jail.d/00-firewalld.conf:
banaction = iptables-multiport

[sshd]
enabled = true
```

#### Enable `fail2ban` and reboot...

_Note: If you don't reboot, a socket doesn't get created correctly. I am not sure why._

```
sudo systemctl enable fail2ban
sudo reboot
```

#### Monitor / Analyze

Watch the IP addresses slowly pile up by occassionally looking in the SSH jail...
```
sudo fail2ban-client status sshd
```

...and even...
```
sudo tail -F /var/log/fail2ban.log
```

#### Reference:

* https://en.wikipedia.org/wiki/Fail2ban
* http://www.fail2ban.org/

----

## Done!

Good luck! Comments and feedback to <t0dd@protonmail.com>
