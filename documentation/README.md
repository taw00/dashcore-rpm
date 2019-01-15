**NOTE:** version 0.13.0 [has been
released](https://blog.dash.org/dash-core-v0-13-on-mainnet-dc9609b0f6f9). RPM
builds are available from the appropriate repositories, but the documentation
here is a bit behind. If you know what you are doing, carry on. If not... wait
for this note to disappear for the documentation to be updated.

# Overview: Dash Core Wallet, Node or Masternode<br />_...on Fedora, CentOS or Red Hat Enterprise Linux_

***Manage a Dash Node or Masternode like a systems administrator.***

Though the complete objective of this set of documents is to illustrate how you can operate a Dash Core Masternode, they also provide valuable information if
you merely want to install and manage a Wallet or Node.

Setting up a Masternode requires setting up a collateral-bearing wallet on one
system and a full node configured to be a masternode on a another. Using this
guidance, you can manage a robust Node or Masternode deployment (or wallet for
that matter) that once set up, requires little maintenance except the occasional
update or upgrade. These instructions are specific to the Red Hat-family of
linuxes.


## The Documents

- All documents:<br /><https://github.com/taw00/dashcore-rpm/tree/master/documentation>
- The overview (this document):<br /><https://github.com/taw00/dashcore-rpm/edit/master/documentation/README.md>

---

### The Masternode Deployment Process

- [Install a Dash Core Wallet](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.dashcore-wallet-setup.gui.md)
- [Deploy a VPS System to be Used as a Dash Core Node/Masternode](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.deploy-and-configure-operating-system.md)
- [Deploy a Dash Masternode as SystemD Service](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.dashcore-node-setup.systemd.md)
- Turn a Node into a Masternode: [Configure and Register Node as a Masternode](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.dashcore-masternode-registration.md)

<!---
- Advanced topics:
  - Configure alert emails for Dash Core Node starts and stops
  - Switch on debug-mode for Dash Core Sentinel
-->
---

### Advanced and Followon Topics

- Discussion about security: [Configure FirewallD and Fail2Ban on a Dash Masternode](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.dashcore-node-security.md)
- Troubleshooting: [Dash Core Troubleshooting Guide](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.dashcore-troubleshooting.md)
- Updating: [How to Update your Wallet, Node, or Masternode](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.update-a-wallet-node-or-masternode.md)
- Upgrading Major Versions: [How to Upgrade from Version 0.12.3 to 0.13.0](https://github.com/taw00/dashcore-rpm/blob/master/documentation/testing/howto.dashcore-upgrade-from-0.12.3-to-0.13.0.md)
- Upgrading OS: [How to Upgrade Your Masternode's Operating System](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.upgrade-the-operating-system.md)


&nbsp;

---

## What is Dash and what is a Dash Core Node and Masternode?

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with an
emphasis on serving as an efficient platform for payments. Dash offers a form of
money that is portable, inexpensive, divisible and fast. It can be spent
securely both online and in person with minimal transaction fees. Dash offers
instant transactions (InstantSend), private / more-fungible transactions
(PrivateSend), and operates a self-governing and self-funding model. This
decentralized governance and budgeting system makes it the first ever successful
decentralized autonomous organization (DAO). Dash is also a platform for
innovative decentralized crypto-tech.

A Dash Core Full Node is a un-collatoralized member of a decentralized network
of servers that validate transactions and blocks.

A Dash Masternode is a member of a network of incentivized Dash Core Nodes that
perform expanded critical services for the Dash protocol above and beyond the
services of a full node.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.


## "I'm not tech savvy! Help!"

There are a number of services that will remove the headaches of managing a  masternode yourself, host a masternode for you, and walk you through the process of  getting set up. [Here is a listing](https://docs.dash.org/en/latest/masternodes/hosting.html) of the current providers recommended by the Dash community.*

## I was really looking for a guide for a different platform. Help!"    

Check out the guidance found in the official dash core documentation: <https://docs.dash.org/en/latest/masternodes/index.html>


## A note about Testnet versus Mainnet

There are two Dash networks (actually more). Two blockchains, separate sets of
miners, wallets, nodes, and masternodes. Testnet exists to as a proving grounds
for new code and new ideas. You too can use it to get familiar with Dash and how
all these pieces fit together. It uses freely available testnet DASH (tDASH)
which can be acquired
[here](https://docs.dash.org/en/stable/developers/testnet.html#faucets). Mainnet
is the network that secures, mines, and transacts real DASH of real value.

You can actually switch freely between Mainnet and Testnet. It's almost like a
shadow network. Always there... just beyond our ability to see clearly... ;)

There are a number of places where you tell all the various Dash Core
executables that you are operating on the testnet or not.

`dash.conf` - for `dashd`, `dash-qt`, and tools like `dash-cli`

* `testnet=1` or `testnet=0` &mdash; Default is usually `testnet=0` for stable releases.

Data directory: Usually either `/var/lib/dashcore` or `$HOME/.dashcore`

* If `testnet=1`, your data-directory becomes your `<data-directory>/testnet3`
* `dash.conf` is independent of this, even if you choose to store it in your data-directory.

`sentinel.conf`

* `network=testnet` or `network=mainnet`

---

### Disclaimer!

These packages are built and tested. But just like with and cryptocurrency, you
must assume the risk associated to this space. I only claim that I made a best
effort to build packages that work and function as expected. They may not in
your context. Additionally, these packages are built from code provided by the
Dash community. I have zero control over any vulnerabilities that code may
contain. Please test your configuration thoroughly before associating
significant sums of money. Dash carefully!


### Good luck! Comments and Feedback...

Got a dash of feedback? *...har har...* Send it my way <https://keybase.io/toddwarner>    

All documents in this directory tree are
[CC-BY-SA](https://github.com/taw00/dashcore-rpm/blob/master/documentation/LICENSE.cc-by-sa.md)
