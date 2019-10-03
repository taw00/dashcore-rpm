# Dash Core for Fedora Linux<br />_...wallet, node, and masternode_

**Important notice:**
* Dash Core RPMs: EL7 and Fedora Linux 28 and older users need to migrate to
  Fedora Linux 29 or 30. EL8 is currently being tested (and fails). Fedora
  Linux 31 is currently in beta but things _seem_ to be stable.
* Dash Masternode Tool: DMT will remain Fedora-only! except for test builds.

Dash Core 0.14 was released on May 22, 2019.

* RHEL7/CentOS7 were dropped because the OS supplied libraries are simply far too
  dated.
* RHEL8/CentOS8 RPMs are currently being testing, but failing due to missing packages.
* Fedora Linux 27 and 28 are EOL (end-of-life).

Please move to the latest version of Fedora. Fedora upgrades are easy (see
available documentation in the "documentation" folder). RHEL/CentOS to Fedora
and El7 to EL8 (when available) migrations should be performed as fresh
installs.

---

**Dash (Digital Cash)** is an open source peer-to-peer cryptocurrency with an
emphasis on serving as an efficient platform for payments. Dash offers a form of
money that is portable, inexpensive, divisible and fast. It can be spent
securely both online and in person with minimal transaction fees. Dash offers
instant transactions **(InstantSend)**, private / more-fungible transactions
**(PrivateSend)**, and operates a self-governing and self-funding model. This
decentralized governance and budgeting system makes it the first ever successful
decentralized autonomous organization (DAO). Dash is also a platform for
innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at https://www.dash.org/

Dash on github can be found here: https://github.com/dashpay

---

This github repository is used to develop and maintain Dash natively built
and packaged for Fedora Linux.

The source packages are housed directly within this repository. For more about
the source packages and build instructions, please visit this link:
<https://github.com/taw00/dashcore-rpm/blob/master/README.source.md>

## Binary (executable) RPMs

**Binary (executable) RPMs are pre-built for you (from these sources) and are
available through external repositories that your packaging system can
understand.** This makes deploying and maintaining Dash on a Fedora, CentOS, or
RHEL system dependable, more secure, and oh so very simple. This is arguably
the simplest way to deploy and manage a Dash Wallet, Node, or Masternode. For
more about the available binary RPMs, please visit this link:
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

_Come say hello to me. I am **t0dd** or **taw** in various forums: [Dash Nation
on Discord](https://dashchat.org/), [Dash Talk on
Discord](http://staydashy.com/), [dash.org's
forum](https://www.dash.org/forum/), [#dashpay on freenode
IRC](http://freenode.net/), [Official Dash Chat on
Telegram](https://web.telegram.org/#/im?p=@dash_chat), and
[/r/dashpay/](https://www.reddit.com/r/dashpay) on Reddit._

_If you like my Dash stuff, also check out the packages I maintain for a couple
other projects. Namely [ZCash](https://github.com/taw00/zcash-rpm) and
[BEAM](https://github.com/taw00/beam-rpm). I'm most bullish on Dash and the
direction that project is taking, but I am a fan of what Zcash and the two
primary Mimblewimble implementation teams are doing. Don't troll me. :)_
