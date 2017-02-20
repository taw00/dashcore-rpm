# Dash RPM Packages<br />for Fedora, CentOS, and Red Hat Enterprise Linux<br />_...wallet, node, and masternode_

**Note1: If you are looking for the "blessed" binaries** (tested and runnable
versions) built from the the source RPM packages described below, you can find
information about them here: [Dash Core Binaries (pre-built) for Fedora Linux,
CentOS, and
RHEL](https://github.com/taw00/dashcore-rpm/blob/master/README-dashcore-binaries.md).
Please remember to shut down and backup your Dash wallet before installing
another version.

**Note2: If you are looking for instruction about how to set up a dash
masternode** with these packages, please refer to the "README.md" document in
the ["documentation"
folder](https://github.com/taw00/dashcore-rpm/tree/master/documentation) of
this git repository.

**Stable source packages: 0.12.1**    
dashcore - latest version is: 0.12.1.1-0.taw, aka v0.12.1.1-ge9e5a24
dashcore-sentinel - latest version: 1.0-2.taw

* Fedora Linux 26 (f26 is still considered unstable):
  - `dashcore-0.12.1.1-0.taw.fc25.src.rpm`
  - `dashcore-sentinel-1.0-2.taw.fc25.src.rpm`
* Fedora Linux 25:
  - `dashcore-0.12.1.1-0.taw.fc25.src.rpm`
  - `dashcore-sentinel-1.0-2.taw.fc25.src.rpm`
* Fedora Linux 24:
  - `dashcore-0.12.1.1-0.taw.fc24.src.rpm`
  - `dashcore-sentinel-1.0-2.taw.fc24.src.rpm`
* CentOS and RHEL 7:
  - `dashcore-0.12.1.1-0.taw.el7.centos.src.rpm`
  - `dashcore-sentinel-1.0-2.taw.el7.centos.src.rpm`

Sourced from:

* Tagged release builds: <https://github.com/dashpay/dash/tags>
* Test builds: <https://bamboo.dash.org/browse/DASHL-DEV/latestSuccessful>
* Documentation: <https://github.com/taw00/dashcore-rpm/tree/master/documentation>



**Deprecated source packages: 0.12.0.58**    
*Don't use these packages.*    
Version and git commit id: v0.12.0.58-g88f3370

Dashcore-0.12.0.58 is no longer usable by the mainnet. Provided here for
archival purposes.

* Fedora Linux 23: `dashcore-0.12.0.58-2.taw.fc23.src.rpm`
* CentOS and RHEL 7: `dashcore-0.12.0.58-2.taw.el7.centos.src.rpm`

----

**Dash (Digital Cash)** is an open source peer-to-peer cryptocurrency that
offers instant transactions ***(InstantSend)***, private transactions
***(PrivateSend)*** and token fungibility. Dash operates a decentralized
governance and budgeting system, making it the first decentralized autonomous
organization (DAO). Dash is also a platform for innovative decentralized
crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at https://www.dash.org/

Dash on github can be found here: https://github.com/dashpay

----

**This repository houses source (and links to binary) RPM packages for the
latest stable (and experimental) releases of Dash.** Using these SRPMs one
should be able to build binary RPMs for your specific linux variety and
architecture.

A source RPM (SRPM or .src.rpm) nicely packages up the source code of a
program/project and contains all the instruction needed to build (compile and
package) corresponding binary RPM packages. To include build requirements. In
the case of Dash, one source RPM will compile the code and generate all the
binary runnable RPM packages associated to the Dash project.

Important notes:

* In this github repo, we bucket the various versions into **stable**,
  **deprecated**, **unstable**, and **archive**.
  - "Stable" packages are in the root of the github repo and "archive"
  - "Deprecated" packages have their own folder in the "archive" folder.
  - "Unstable" packages in an "unstable" folder.    
    ...the tree looks like this...

dashcore-rpm (and the stable packages)
├── archive
│   └── deprecated
└── unstable

* Only use **stable** versions on the mainnet (`testnet=0`).
  - **Unstable** versions are test versions and great to play with on the
    testnet (`testnet=1`). Please don't use them on the mainnet.
  - **Deprecated** versions will simply not function anymore on the main or
    testnet. They are provided for archival purposes.



----


# Building from source RPM packages

#### [0] For RHEL and CentOS (*not Fedora*), you need to subscribe to special repositories

**RHEL 7 Specific Instructions**

Do this as root (or a sudo'er). Subscribe to all the appropriate repositories and add the EPEL repo. Note, RHEL7 has proven to be a challenging platform to build for. Be aware that CentOS7 RPMs should work just fine on RHEL7.

```
# As a normal user (not root)
sudo subscription-manager repos --enable rhel-7-server-rpms
sudo subscription-manager repos --enable rhel-7-server-extras-rpms
sudo subscription-manager repos --enable rhel-7-server-optional-rpms
sudo rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
# For the needed openssl-compat-bitcoin-libs RPM...
sudo rpm -ivh https://linux.ringingliberty.com/bitcoin/el7/x86_64/bitcoin-release-3-1.noarch.rpm
```

**CentOS 7 Specific Instructions**

```
# As a normal user (not root)
sudo yum install epel-release
# For the needed openssl-compat-bitcoin-libs RPM...
sudo rpm -ivh https://linux.ringingliberty.com/bitcoin/el7/x86_64/bitcoin-release-3-1.noarch.rpm
```


#### [1]  Set up your Build environment

RPM? How? What?: https://fedoraproject.org/wiki/How_to_create_an_RPM_package (read especially "Preparing your system")

In order to build from a source RPM, you first need to set up your environment. If you have not already, do this as your normal user (not root) from the commandline:

```
# As a normal user (not root)
# For RHEL and CentOS, it's the same, just don't include the "fedora-packager"
sudo dnf install @development-tools fedora-packager rpmdevtools rpm-sign
```

```
# As a normal user (not root)
# Create your working folder ~/rpmbuild/
rpmdev-setuptree
```


***If that fails,*** you need to read more about setting up your development
environment at the link that was provided earlier.

Note, it suggests using a separate user on your system to build RPMs… you can
do that, but for our examples, I am assuming you are doing it with whatever
user you want. I execute these commands from my personal normal user account
usually.


#### [2] Download a source RPM of your choosing

For example, at the time of this writing the latest Dash src.rpm of version
`0.12.0.58`, is considered "stable". For the purposes of this document, we are
going use version-release `0.12.0.58-2.taw` as our example. Download the one
specific to your linux distribution Fedora, RHEL, or CentOS. If you are
attempting to build in a different environment, download the source RPM that as
closely matches your platform and experiment away.


#### [3] Verify the RPM has not been tampered with

This is done in one of two ways: (1) with an sha256sum hash check and (2) with
a GPG signature check. Assuming the source RPM is digitally signed, GPG
signature verification is vastly more secure, but more complicated.

**Verification via sha256sum**

*Note, sha256 hashes are provided within this github repository.*

From the commandline...

```
sha256sum dashcore-0.12.0.58-2.taw.*.src.rpm
```

The result should match the hash for the RPM your downloaded, otherwise the
download was complete or the RPM is tampered with or I screwed something up in
this document.

**Verification of the source RPMs digital signature**

If I built these packages correctly, their appropriate sha256 hash should be
posted within the sha256sum.txt files included in this repository _and_ they should pass a gpg digital signature check signed by my public key.

(1) Import my GPG key into your RPM keyring if you have not already done so.
You have to do this as the root user.

```
# As a normal user (not root)
sudo rpm --import https://raw.githubusercontent.com/taw00/public-keys/master/taw-694673ED-public-2030-01-04.asc
# ...or (cuz some folks really prefer keybase)...
sudo rpm --import https://keybase.io/toddwarner/key.asc
```

Or navigate to http://github.com/taw00/public-keys and fetch the key manually
and import it locally.

(2) Check the signature

`$ rpm --checksig -v dashcore-0.12.0.58-2.taw.*.src.rpm` ...or...
`$ rpm -Kv dashcore-0.12.0.58-2.taw.*.src.rpm`

You should see something like: `dashcore-0.12.0.58-2.taw.fc23.src.rpm: rsa sha1 (md5) pgp md5 OK`<br />
*Notice the "pgp" and the "OK"*

And if you used the verbose flag, `-v`, then you should see my key ID: `694673ed`

If the output says something like
`(MISSING KEYS: RSA#694673ed (MD5) PGP#694673ed)`,
you did not successfully import my key in step 1.

Another way to look at this information is via...

`$ rpm -qpi dashcore-0.12.0.58-2.taw.*.src.rpm | grep 'Name\|\|Version\|Release\|Signature'`


#### [4] Install the source RPM

Again, from the command line as a normal user... First, move that source RPM into the source RPMs location in the rpmbuild build tree:

```
# As a normal user (not root)
mv dashcore-*.src.rpm ~/rpmbuild/SRPMS/
# Install the sucker (do not use sudo here!):
rpm -ivh ~/rpmbuild/SRPMS/dashcore-0.12.0.58-2.taw.fc23.src.rpm #Or whatever version you are installing.
```

That should explode source code and patch instruction into
~/rpmbuild/SOURCES/ and the build instructions into ~/rpmbuild/SPECS/.
Something likes this...

```
~/rpmbuild/SPECS/dashcore-0.12.0.58.spec
~/rpmbuild/SOURCES/dash-0.12.0.58.tar.gz
~/rpmbuild/SOURCES/dashcore-0.12.0.58-contrib-fedora.tar.gz
~/rpmbuild/SOURCES/dashcore-0.12.0.58-dashify.tar.gz
~/rpmbuild/SOURCES/dashcore-0.12.0.58-fedora.patch
```

#### [5] Build the binaries

One source RPM will often build multiple binary RPMs. In this case, six RPMs
are built (with the debuginfo RPM optionally built). See them listed later
in this document.

Actually building the binary RPMs is as easy as running the rpmbuild command
against a specfile. For example:

```
# As a normal user (not root)
cd ~/rpmbuild/SPECS
rpmbuild -ba dashcore-0.12.0.58.spec
```

Note, you may run into a failed build. Look at the BuildRequires in the .spec
file. For example, you may have to install a few RPMs first, like gcc-c++ and
and others. Or just note the output of the failed build and add the packages.
For example, I had to do something like this for a RHEL7 build...

**For Fedora:**
```
# As a normal user (not root) -- Note, this may not be comprehensive.
sudo dnf install gcc-c++ qt5-qtbase-devel qt5-linguist qrencode-devel miniupnpc-devel protobuf-devel openssl-devel desktop-file-utils autoconf automake boost-devel libdb4-cxx-devel libevent-devel libtool java python3-zmq zeromq-devel
```
**For CentOS7 and RHEL7:**
```
# As a normal user (not root) -- Note, this may not be comprehensive.
sudo yum install gcc-c++ qt5-qtbase-devel qt5-linguist qrencode-devel miniupnpc-devel protobuf-devel openssl-devel desktop-file-utils autoconf automake boost-devel libdb4-cxx-devel libevent-devel libtool java openssl-compat-bitcoin-libs python34
```


If all goes well, the build process may take 30+ minutes and nicely bog down
your computer. If the build succeeded, the build process will list the RPMS
that were created at the end of the terminal window output. The binary RPMs
will be saved in the _~/rpmbuild/RPMS/_ directory and a newly minted source RPM
will land in the _~/rpmbuild/SRPMS/_ directory. The binary RPMs will be
these...

* **dashcore-client** -- The dash-qt wallet and full node _(note, some older
  sources merely named this package "dash" and not "dashcore-client")_
* **dashcore-utils** -- dash-cli, a utility to communicate with and control a
  Dash server via its RPC protocol, and dash-tx, a utility to create custom
  Dash transactions.
* **dashcore-server** -- dashd, a peer-to-peer node and wallet server. It is
  the command line installation without a GUI.  It can be used as a commandline
  wallet and is typically used to run a Dash Masternode. Requires
  dashcore-utils to be installed as well.
* **dashcore-libs** -- provides libbitcoinconsensus, which is used by third
  party applications to verify scripts (and other functionality in the future).
* **dashcore-devel** -- provides the libraries and header files necessary to
  compile programs which use libbitcoinconsensus. Requires dashcore-libs to be
  installed as well.
* **dashcore-[version info].src.rpm** -- The source code -- the source RPM, or
  SRPM You want to build binaries for your RPM-based linux distribution? Use
  this source RPM to do so easily.
* **dashcore-debuginfo** -- debug information for package dash. Debug
  information is useful when developing applications that use this package or
  when debugging this package.  (99.999% of you do not need to install this)


***Are you impatient?*** Binaries for Dash Core have already been built for
these linux distributions. Again, reference the link provided at the beginning
of this document.

----


### Advanced: Creating your own monogrammed builds

If you are feeling a bit froggy, build and compile the binary RPM packages
specifically tagged with your name/initials.

Let's say your name is Barney Miller (initials "bm").

```
# As a normal user (not root)
cp dashcore-0.12.0.58.spec dashcore-0.12.58-2.bm.spec
```

* Edit `dashcore-0.12.0.58-2.bm.spec`
* Change the _bumptag_ value in that file from '.taw' to '.bm'
* Add a stanza in the changelog at the bottom reflective of what you did (copy
  the format)...

...and build your RPMs from that...


```
# As a normal user (not root)
rpmbuild -ba dashcore-0.12.0.58-2.bm.spec
```

If all goes to plan, in 30 or 40 minutes you should have a set of binary
packages, specifically built to your system with a release of '7.bm'.

If there is a significant problem where you have to, for example, fix the
`configure.ac` file in the `dash-0.12.0.58.tar.gz` archive (common issue)... you
will have to do something like this:

* Copy the archive to some working director and then extract it...

      tar xvzf dash-0.12.0.58.tar.gz

* Copy the resultant (the original pristine) folder…

      cp -a dash-0.12.0.58 dash-0.12.0.58.orig --

* Work on the `dash-0.12.0.58/configure.ac` file, build a new patch, and try to
  rebuild things (iterate iterate iterate). All that is a bit beyond this
  document, but this is a good place to start to understand RPMs:
  https://fedoraproject.org/wiki/How_to_create_an_RPM_package

Finally, once built and you are happy, instead of relying on sha256sum hash
verification, you can GPG sign your packages. For instruction, read these nice
summaries (hint, you will have to install the `rpm-sign` RPM first):

* http://fedoranews.org/tchung/gpg/
* http://blog.packagecloud.io/eng/2014/11/24/howto-gpg-sign-verify-rpm-packages-yum-repositories/

And if you are feeling really ambitious, you can set up a publicly facing dnf
(once called yum) repository and making your packages available through
super-automated means to the world (keep reading the Fedora documentation for
more information about yum and dnf).

## That should get you started! Good luck! -[Todd](https://keybase.io/toddwarner)

_And come say hello to me. I am **t0dd**, **taw**, **taw00**, or **agrarian**, in various forums:
[dash.org's forums](https://www.dash.org/forum/),
[#dash:chat.cryptochat.io (matrix network)](https://riot.im/app/#/room/#dash:chat.cryptochat.io), [#dashpay on
freenode IRC](http://freenode.net/), [Dash Knights 2.0 on
Telegram](https://web.telegram.org/#/im?p=@DashDigitalCash), and
[/r/dashpay/](https://www.reddit.com/r/dashpay) on Reddit._

...

_Special thanks go out to [Michael
Hampton](https://www.ringingliberty.com/bitcoin/) for his mature bitcoin spec
file from which I originally templated these dashcore spec files._
