# Overview: v12.1 Dash Masternode on Fedora, CentOS or RHEL

> The objective of this set of documents is to illustrate how you can operate a Dash Masternode which requires setting up a collateral-holding wallet on one system and a full node configured to be a masternode on a another.
>
> These instructions are specific to the Red Hat-family of linuxes.

## Wallets and Masternodes

_Note that there are two systems involved here, one for the wallet and the other for the masternode._

To run a masternode, you set up a small server running a masternode as a service. But the owner of the masternode has to have 1000 DASH as collateral. Ownership of that collateral is provable by having a specially configured wallet, separate from the masternode that is used to start the masternode once configured. This of that wallet with that particular 1000 DASH as the ignitiion key for the masternode.

> ***"I'm not tech savvy! Help!"***    
> *There are a number of services that will remove the headaches of managing a  masternode yourself, host one for you, and walk you through the process of  getting set up. [Here is a listing](ttps://dashpay.atlassian.net/wiki/pages/viewpage.action?pageId=1867885) of the current providers recommended by the Dash community.*


## The high-level process

0. Save up 1000 DASH
1. Install and populate a collateralized Wallet
   * [Instruction](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.12.1-dashcore-collateral-bearing-wallet-setup.gui.md) for GUI Wallets
   * Instruction &mdash; not done yet &mdash; for commandline only wallets
2. Install a Full Node and configure it as if it will operate as a Masternode
   * Part one of [this instruction](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.12.1-dashcore-masternode-setup.systemd.md)
3. Trigger the Full Node to operate as a Masternode via a command from the Wallet
   * Part two of [this instruction](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.12.1-dashcore-masternode-setup.systemd.md)
4. Install Sentinel on the same server as the Masternode
   * Part three of [this instruction](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.12.1-dashcore-masternode-setup.systemd.md)

Sounds easy, right? Well, on the whole, it is not complicated, just "tricky". Maybe "twitchy" is the right term.

# Good luck!

Got a dash of feedback? *...har har...* Send it my way [t0dd@protonmail.com](mailto:t0dd@protonmail.com)    
And of course, donations welcome: [XyxQq4qgp9B53QWQgSqSxJb4xddhzk5Zhh](dash:XyxQq4qgp9B53QWQgSqSxJb4xddhzk5Zhh)

