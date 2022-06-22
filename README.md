# Dash Core for Fedora Linux<br />_...wallet, node, and masternode_

> **EOL of Dash Core RPM development**  
>
> The Dash developer community will be moving towards containerized deployment  
> of nodes and masternodes. Therefore, I will cease building RPMs when v18
> rolls out (relatively soon). I appreciate all of you who have found my builds
> useful.
>
> Associated announcments:
> - https://www.dash.org/blog/introducing-dashmate-the-masternode-setup-tool-for-dash-platform/
> - https://www.dash.org/blog/dashcore-v18-0-product-brief/
> 
> ETA? Unknown at this time.


> OLD NEWS: IMPORTANT REPOSITORY NOTICE  
>   
> This repository will no longer host RPMs or SRPMs. Due to github quotas, I am
> ending storage of the `.src.rpm` convenience files in all (or most) of my
> build repositories. You can duplicate my builds with files provided within
> this repository and with upstream source `.tar.gz` files. If you can read an
> RPM spec file, you should be good to go.  
>   
> For the rest of you who simply want to use the application, follow the
> instructions for installation of the binary package and enjoy.

**Supported builds and other notices:**
* For both Dash Core and Dash Masternode Tool (DMT), I no longer supply packages for RHEL/CentOS.
* For Dash Core, use the provided systemd configuration. This makes nodes near bullet-proof, even on Fedora.
* Dash Masternode Tool: DMT will remain Fedora-only! except for test builds.
* Keep up with Fedora's release schedule: <https://fedoraproject.org/wiki/Releases>

Fedora upgrades are easy (see available documentation in the "documentation"
folder).

---

**Dash (Digital Cash)** is an open-source peer-to-peer cryptocurrency with an
emphasis on serving as an efficient platform for payments and decentralized
applications. Dash offers a form of money that is portable, inexpensive,
divisible and fast. It can be spent securely both online and in-person with
negligible transaction fees. Dash offers instant transactions by default
**(InstantSend)**, more-fungible transactions **(CoinJoin)**, and operates its
network with a model of self-governance and self-funding. This decentralized
governance and budgeting system makes it the first-ever successful
decentralized autonomous organization (DAO).

Dash is open source and the name of the overarching project. Learn more
at https://www.dash.org/

Dash on github can be found here: https://github.com/dashpay

---

This github repository is used to develop and maintain Dash natively built
and packaged for Fedora Linux.

For more about building from the sources provided here, please visit this link:
<https://github.com/taw00/dashcore-rpm/blob/master/README.source.md>

## Binary (executable) RPMs

**Binary (executable) RPMs are pre-built for you (from these sources) and are
available through external repositories that your packaging system can
understand.** This makes deploying and maintaining Dash on a Fedora system
dependable, more secure, and oh so very simple. This is arguably the simplest
way to deploy and manage a Dash Wallet, Node, or Masternode. For more about the
available binary RPMs, please visit this link:
<https://github.com/taw00/dashcore-rpm/blob/master/README.binaries.md>

---

### Disclaimer!

These packages have been successfully built and tested, but I lay no claim that
they are absolutely free of any bugs in the code, default configuration,
documented configuration, or in the builds or how those builds are
deployed/installed.

These packages have been used by myself and others for years at this point, but
in the end, users must assume the risks associated to both community built and
deployed packages and, of course, any cryptocurrency funds managed by this
software. I.e., These will probably work for you, but I can't be liable for any
loss of funds or damages associated to this software.

### Send comment and feedback - <https://keybase.io/toddwarner>

_Come say hello to me. I am **t0dd** in various forums: [Dash Talk on Discord](https://discord.com/invite/PXbUxJB),
[dash.org's forum](https://www.dash.org/forum/), and in various chat rooms on Matrix.org.

