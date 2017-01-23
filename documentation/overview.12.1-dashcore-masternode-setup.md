# Overview: v12.1 Dash Masternode as SystemD Service on Fedora, CentOS or RHEL

:::info
The objective of these set of documents is to illustrate how you can operate a Dash Masternode using the sof as a systemd service on one of the a Red Hat-family of Linuxes. Viewing a Masternode as a server service lends itself to ensuring that it is enabled as a properly configured systemd-managed service. This has advantages in general robustness of the service as well as how the service is secured.
:::

## Wallets and Masternodes

_Note that there are two systems involved here, one for the wallet and the other for the masternode._

To run a masternode, you set up a small server running a masternode as a service. But the owner of the masternode has to have 1000 DASH as collateral. Ownership of that collateral is provable by having a specially configured wallet, separate from the masternode that is used to start the masternode once configured. This of that wallet with that particular 1000 DASH as the ignitiion key for the masternode.

## The high-level process

1. Install and populate a collateralized Wallet
2. Install a Full Node and configure it as if it will operate as a Masternode
3. Trigger the Full Node to operate as a Masternode via a command from the Wallet
4. Install Sentinel on the same server as the Masternode


# Good luck!

Please send feedback and comments to t0dd@protonmail.com

