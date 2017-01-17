# Configure the Firewall on Masternode Server

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
# I want the first two, but not cockpit by default
sudo firewall-cmd --permanent --zone=FedoraServer --add-service ssh
sudo firewall-cmd --permanent --zone=FedoraServer --add-service dhcpv6-client
sudo firewall-cmd --permanent --zone FedoraServer --remove-service cockpit

# Open up the Masternode port (19999=Testnet, 9999=Live)
sudo firewall-cmd --permanent --zone=FedoraServer --add-port=19999/tcp
sudo firewall-cmd --permanent --zone=FedoraServer --add-port=9999/tcp

# Rate limit incoming ssh traffic to 10 per minute
sudo firewall-cmd --permanent --add-rich-rule='rule service name=ssh limit value=10/m accept'

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

# Configure fail2ban on a Dash Masternode server

Install `fail2ban`...
```
# If Fedora...
sudo dnf install -y fail2ban
# If CentOS or RHEL
sudo yum install epel-release # if not already installed
sudo yum install -y fail2ban
```

Lock-down ssh.... Edit `/etc/fail2ban/jail.local`

```
sudo nano /etc/fail2ban/jail.local
```
CUT-N-PASTE this and save...
```
[DEFAULT]
# Ban hosts for one hour:
bantime = 3600

# Override /etc/fail2ban/jail.d/00-firewalld.conf:
banaction = iptables-multiport

[sshd]
enabled = true
```

Start and enable `fail2ban`...

```
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

Watch the IP addresses slowly pile up by occassionally looking in the SSH jail...
```
sudo fail2ban status sshd
```
...and even...
```
sudo tail -F /var/log/fail2ban.log
```
