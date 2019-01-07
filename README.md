# Dash for Fedora, CentOS, and Red Hat Enterprise Linux<br />_...wallet, node, and masternode_

---

**Important notice (as of 2018-11-28):<br />EL7 and Fedora Linux 27 users need
to migrate to Fedora Linux 29:**

Dash Core 0.13.0 is coming out soon. As of that version, I will not be building
Dash Core for EL7-based linuxes (CentOS7 and RHEL7) nor for Fedora Linux 27.

* EL7 is being dropped because the OS supplied libraries are simply far too
  dated. Once EL8 comes out (May-ish 2019), Dash Core builds should be
  available on those platforms.
* As for Fedora Linux 27, it's EOL (end-of-life) date is November 30th, 2018.
  Generally I continue to build and test packages on dated platforms for some
  time, but since Dash Core 0.13.0 will be out after the EOL date and is such a
  significant upgrade, I will not be making builds availabe for Fedora Linux 27.

Please move to the latest version of Fedora (as of today, that is Fedore Linux
29). Fedora upgrades are easy (see available documentation in the
"documentation" folder). RHEL/CentOS to Fedora migrations should be performed
as fresh installs.

---

**Dash (Digital Cash)** is an open source peer-to-peer cryptocurrency with a
strong focus on serving as a superior means of payment. Dash offers a form of
money that is portable, inexpensive, divisible and incredibly fast. It can be
spent securely both online and in person with minimal transaction fees. Dash
offers instant transactions **(InstantSend)**, fungible transactions
**(PrivateSend)**, and, as a network, is self-governing and self-funding. This
decentralized governance and budgeting system makes is the first ever
successful decentralized autonomous organization (DAO). Dash is also a platform
for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at https://www.dash.org/

Dash on github can be found here: https://github.com/dashpay

---

This github repository is used to develop and maintain Dash natively built
and packaged for Fedora, CentOS, and Red Hat Enterprise Linux.

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

_Come say hello to me. I am **t0dd** or **taw** in various forums:
[Dash Nation on Discord](https://dashchat.org/), [Dash Talk on Discord](http://staydashy.com/),
[dash.org's forum](https://www.dash.org/forum/),
[#dashpay on freenode IRC](http://freenode.net/),
[Official Dash Chat on Telegram](https://web.telegram.org/#/im?p=@dash_chat), and
[/r/dashpay/](https://www.reddit.com/r/dashpay) on Reddit._

_If you like my Dash stuff, also check out my Zcash builds which I maintain for
the [Zcash](https://z.cash) Project: <https://github.com/taw00/zcash-rpm>. I
am a huge fan of both endeavors; don't troll me. :)_

