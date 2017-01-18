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
# If Debian or Ubuntu
sudo apt install -y firewalld
```

Configure firewall

```
# Is firewalld running?
# Turn on and enable firewalld if not already done...
sudo firewall-cmd --state
sudo systemctl start firewalld.service
sudo systemctl enable firewalld.service

# Determine what the default zone is.
# On vultr, for example, default zone is "FedoraServer" (it is the assumption for this example)
# On Ubuntu, it will often be "public", just replace "FedoraServer" with what you are using below.
sudo firewall-cmd --get-active-zone

# FedoraServer usually starts with ssh, dhcp6-client, and cockpit opened up
# I want ssh. dhcpv6 should be unneccessary for a static IP host, and cockpit is something used intermittently.
# And of course, we want the dash full node/masternode ports available.
sudo firewall-cmd --permanent --zone=FedoraServer --add-service ssh
sudo firewall-cmd --permanent --zone=FedoraServer --remove-service dhcpv6-client
#sudo firewall-cmd --permanent --zone=FedoraServer --add-service cockpit
sudo firewall-cmd --permanent --zone=FedoraServer --remove-service cockpit
# Open up the Mastnernode port
sudo firewall-cmd --permanent --zone=FedoraServer --add-service dash-node
#sudo firewall-cmd --permanent --zone=FedoraServer --add-service dash-node-testnet
# If you are running and older masternode or a masternode that was not installed via RPM, you must do things manually
#sudo firewall-cmd --permanent --zone=FedoraServer --add-port=19999/tcp
#sudo firewall-cmd --permanent --zone=FedoraServer --add-port=9999/tcp

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
# If Debian or Ubuntu
sudo apt install -y fail2ban
```

0
