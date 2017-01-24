# Overview: v12.1 Dash Masternode on Fedora, CentOS or RHEL

> The objective of this set of documents is to illustrate how you can operate a Dash Masternode which requires setting up a collateral-holding wallet on one system and a full node configured to be a masternode on a another.
>
> These instructions are specific to the Red Hat-family of linuxes.

## Wallets and Masternodes

_Note that there are two systems involved here, one for the wallet and the other for the masternode._

To run a masternode, you set up a small server running a masternode as a service. But the owner of the masternode has to have 1000 DASH as collateral. Ownership of that collateral is provable by having a specially configured wallet, separate from the masternode that is used to start the masternode once configured. This of that wallet with that particular 1000 DASH as the ignitiion key for the masternode.

## The high-level process

1. Install and populate a collateralized Wallet
   * [Instruction](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.12.1-dashcore-wallet-setup.gui.md) for GUI Wallets
   * [Instruction](https://not_done_yet) for commandline only wallets
2. Install a Full Node and configure it as if it will operate as a Masternode
   * Part one of [this instruction](https://not_done_yet)
3. Trigger the Full Node to operate as a Masternode via a command from the Wallet
   * Part two of [this instruction](https://not_done_yet)
4. Install Sentinel on the same server as the Masternode
   * Part three of [this instruction](https://not_done_yet)

Sounds easy, right? Well, on the whole, it is not complicated, just "tricky". Maybe "twitchy" is the right term.

# Good luck!

Please send feedback and comments to t0dd@protonmail.com

