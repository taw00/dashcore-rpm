# Overview: Dash Masternode<br />_...on Fedora, CentOS or Red Hat Enterprise Linux_

> The objective of this set of documents is to illustrate how you can operate a
> Dash Masternode which requires setting up a collateral-bearing wallet on one
> system and a full node configured to be a masternode on a another.
>
> These instructions are specific to the Red Hat-family of linuxes.


## The Documents

* All documents:<br /><https://github.com/taw00/dashcore-rpm/tree/master/documentation>
* The overview (this document):<br /><https://github.com/taw00/dashcore-rpm/edit/master/documentation/README.md>

* Wallet setup: [Set up a Dash Wallet in support of a Dash Masternode](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.12.1-dashcore-collateral-bearing-wallet-setup.gui.md)
* Masternode setup: [Configure and Run a Dash Masternode as SystemD Service](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.12.1-dashcore-masternode-setup.systemd.md)
* Discussion about security: [Configure FirewallD and Fail2Ban on a Dash Masternode](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.secure-your-dash-masternode.md)
* Troubleshooting: [Dash Core Troubleshooting Guide](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.12.1-dashcore-troubleshooting.md)
* Updating: [HowTo Update your Wallet, Node, or Masternode](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.update-a-wallet-node-or-masternode.md)

&nbsp;

---

## What is Dash and what is a Dash Masternode?

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

A Dash Full Node is a un-collatoralized member of a decentralized network of
servers that validate transactions and blocks.

A Dash Masternode is a member of a network of incentivized servers that perform
expanded critical services for the Dash cryptocurrency protocol above an beyond
the services of a full node.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.


## Wallets and Masternodes

_Note that there are two systems involved here, one for the wallet and the other for the masternode._

To run a masternode, you set up a small server running a masternode as a service. But the owner of the masternode has to have 1000 DASH as collateral. Ownership of that collateral is provable by having a specially configured wallet, separate from the masternode that is used to start the masternode once configured. This of that wallet with that particular 1000 DASH as the ignitiion key for the masternode.

> ***"I'm not tech savvy! Help!"***    
> *There are a number of services that will remove the headaches of managing a  masternode yourself, host one for you, and walk you through the process of  getting set up. [Here is a listing](https://dashpay.atlassian.net/wiki/pages/viewpage.action?pageId=1867885) of the current providers recommended by the Dash community.*

> **I was really looking for a guide for a different platform. Help!"***    
> _Check out the countless guides that can be found starting here: <https://dashpay.atlassian.net/wiki/display/DOC/Masternode>_


## Setting up a Dash Masternode: The high-level process

0. Save up 1000 DASH
1. Install and populate a collateralized Wallet
2. Install a Dash Full Node with dreams of being a Masternode
3. Bind the wallet to the node and have it "start" the Masternode
4. Install Sentinel on the same server as the Masternode
5. DONE!

Sounds easy, right? Well, on the whole, it is not complicated, just "tricky". Maybe "twitchy" is the right term.

## A note about Testnet versus Mainnet

There are two Dash networks. Two blockchains, separate sets of miners, wallets,
nodes, and masternodes. Testnet exists to as a proving grounds for new code and
new ideas. You too can use it to get familiar with Dash and how all these
pieces fit together. It uses freely available testnet Dash (tDash) which can be
acquired [here](https://test.explorer.dash.org). Mainnet is the network that
secures, mines, and transacts real Dash of real value.

You can actually switch freely between Mainnet and Testnet. It's almost like a
shadow network. Always there... just beyond our ability to see clearly... ;)

There are a number of places where you tell all the various Dash Core
executables that you are operating on the testnet or not.

`dash.conf` - for `dashd`, `dash-qt`, and tools like `dash.cli`

* `testnet=1` or `testnet=0` &mdash; Default is usually `testnet=0` for stable releases.

Data directory: Usually either `/var/lib/dashcore` or `$HOME/.dashcore`

* If `testnet=1`, your data-directory becomes your data-directory/testnet3
* `dash.conf` is independent of this, even if you choose to store it in your data-directory.

`sentinel.conf`

* `network=testnet` or `network=mainnet` &mdash; Leave this commented out and allow `dash.conf` to determine Sentinel's operating posture.

---

### Good luck! Comments and Feedback...

Got a dash of feedback? *...har har...* Send it my way <https://keybase.io/toddwarner>    
And of course, donations welcome: <a href="dash:XyxQq4qgp9B53QWQgSqSxJb4xddhzk5Zhh">XyxQq4qgp9B53QWQgSqSxJb4xddhzk5Zhh</a>

All documents in this directory tree are
[CC-BY-SA](https://github.com/taw00/dashcore-rpm/blob/master/documentation/LICENSE.cc-by-sa.md)
