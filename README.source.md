# Dash Core for Fedora Linux<br />_...wallet, node, and masternode_

The most current source packages can be found in this directory:
<https://github.com/taw00/dashcore-rpm/tree/master/SRPMS>

From these source packages, Dash Core has been successfully built and
maintained for Fedora and RHEL/CentOS for years (starting with Fedora 23 or 24
and CentOS7). Build on the latest versions of Fedora please.

The original components used to build these packages come from:

* Tagged release builds / source archives:
  - Dash <https://github.com/dashpay/dash/releases>
  - Sentinel <https://github.com/dashpay/sentinel/releases>
  - Dash Masternode Tool  <https://github.com/Bertrand256/dash-masternode-tool/releases>

* Directly from the build system and non-tagged repositories:
  - Dash <https://bamboo.dash.org/browse/DASHL-DEV/latestSuccessful>
  - Sentinel <https://github.com/dashpay/sentinel>
  - Dash Masternode Tool  <https://github.com/Bertrand256/dash-masternode-tool>

Each RPM contains my own contributed imagery and configuration. If you wish to
browse my contributions, browse to this link and explore the directories ending
in `-contrib`:

<https://github.com/taw00/dashcore-rpm/tree/master/SOURCES/>

----

With these SRPMs one should be able to build binary RPMs for your
specific linux variety and architecture.

A source RPM (SRPM or .src.rpm) nicely packages up the source code of a
program/project and contains all the instruction needed to build (compile and
package) corresponding binary RPM packages. To include build requirements. In
the case of Dash, one source RPM will compile the code and generate all the
binary runnable RPM packages associated to the Dash project.

Important notes:

- All source is organized in directories named just like `rpmbuild` organizes
  things: `SOURCES/`, `SRPMS/`, `SPECS/`. The finalized RPMS are housed in the
  COPR repositories (Fedora Project) and not here (see repo configuration in the
  installation section).
- In this github repo, everything directly in the `source/` directory is
  **stable** and, of course, everything found in the `source/testing/` is
  experimental.
- Source archives with filenames ending in `-contrib.tar.gz` are my
  contributions and contain desktop icons and configuration; firewalld,
  systemd, and logrotation configuration; and more.

```bash
dashcore-rpm
 ├── SOURCES   ← stable code and contrib archive files
 ├── SRPMS     ← stable src.rpm packages
 │   └── archive
 └── SPECS     ← stable rpm spec files
    └── archive
```

- Only use **stable** versions on the mainnet (`testnet=0`).<br />
  **Testing** versions are test versions and great to play with on the testnet
  (`testnet=1`). Please don't use them on the mainnet.


----


# Building from source RPM packages

#### [1]  Set up your Build environment

RPM? How? What?:
* <https://fedoraproject.org/wiki/How_to_create_an_RPM_package>  
  (read especially "Preparing your system")
* <https://github.com/rpm-software-management/mock/wiki>
* <https://fedoraproject.org/wiki/Packaging:Versioning>

In order to build from a source RPM, you first need to set up your environment.
If you have not already, _**do this as your normal user (not root)**_ from the
commandline:

```bash
# Install needed packages
sudo dnf dnf-utils install @development-tools rpmdevtools rpm-sign fedora-packager
# create your working folder ~/rpmbuild/{SOURCES,SRPMS,SPECS,RPMS}
rpmdev-setuptree

# Add yourself to the mock group
# mock group membership allows you to build in mock build # environments
sudo usermod -a -G mock $USER
# refresh your login so that the new group shows up for this user
# (not as reliable as logging out and logging back in again)
newgrp -
```

***If that fails,*** you need to read more about setting up your development
environment at the link that was provided earlier.

Note, it suggests using a separate user on your system to build RPMs… you can
do that, but for our examples, I am assuming you are doing it with whatever
user you want. I execute these commands from my personal normal user account
usually.

**Configure mock**

Copy `/etc/mock/site-defaults.cfg` to `~/.config/mock.cfg`
```sh
mkdir -p ~/.config
cp -i /etc/mock/site-defaults.cfg ~/.config/mock.cfg
```
and then edit `~/.config/mock.cfg` and configure it similarly to this (this is
what I have uncommented and configured in mine.

```sh
# ~/.config/mock.cfg
config_opts['basedir'] = '/var/lib/mock/'
config_opts['cache_topdir'] = '/var/cache/mock'
config_opts['rpmbuild_networking'] = True
config_opts['bootstrap_module_enable'] = []
config_opts['bootstrap_module_install'] = []
config_opts['environment']['LANG'] = os.environ.setdefault('LANG', 'en_US.UTF-8')
# This is something I do. I use 'tree', 'vim', 'less' in my testing
config_opts['chroot_additional_packages'] = ['tree', 'vim-enhanced', 'less']
# I turn off "cleanup" when doing a lot of testing.
#config_opts['cleanup_on_success'] = 0
#config_opts['cleanup_on_failure'] = 0
```


#### [2] Download a source RPM of your choosing

For example, at the time of this writing the latest Dash Core (dashcore) src.rpm of version
`0.14`, is considered "stable". For the purposes of this document, we are
going use version-release `0.14.0.5-1.taw` as our example. Download the lastest
version that is specific to your linux distribution Fedora, CentOS, or RHEL. If
you are attempting to build in a different environment, download the source RPM
that as closely matches your platform and experiment away.

#### [3] Verify the RPM has not been tampered with

This is done with a GPG signature check.

**Verification of the source RPM's digital signature**

(1) Import my GPG key into your RPM keyring if you have not already done so.
You have to do this as the root user.

```bash
# As a normal user (not root)
sudo rpm --import https://keybase.io/toddwarner/key.asc
```

(2) Check the signature

`$ rpm --checksig -v dashcore-0.14.0.*.src.rpm` ...or...
`$ rpm -Kv dashcore-0.14.0.*.src.rpm`

You should see something like: `dashcore-0.14.0.5-1.taw.fc30.src.rpm: rsa sha1 (md5) pgp md5 OK`<br />
*Notice the "pgp" and the "OK"*

And if you used the verbose flag, `-v`, then you should see my key ID: `694673ed`

If the output says something like
`(MISSING KEYS: RSA#694673ed (MD5) PGP#694673ed)`,
you did not successfully import my key in step 1.

Another way to look at this information is via...

`$ rpm -qpi dashcore-0.14.0.5-1.taw.*.src.rpm | grep 'Name\|\|Version\|Release\|Signature'`


#### [4] Install the source RPM

Again, from the command line as a normal user... First, move that source RPM into the source RPMs location in the rpmbuild build tree:

```bash
# As a normal user (not root)
mv dashcore-*.src.rpm ~/rpmbuild/SRPMS/
# Install the sucker (do not use sudo here!):
rpm -ivh ~/rpmbuild/SRPMS/dashcore-0.14.0.5-1.taw.fc30.src.rpm #Or whatever version you are installing.
```

That should explode source code and patch instruction into
~/rpmbuild/SOURCES/ and the build instructions into ~/rpmbuild/SPECS/.
Something like this...

```bash
~/rpmbuild/SPECS/dashcore.spec
~/rpmbuild/SOURCES/dash-0.14.0.5.tar.gz
~/rpmbuild/SOURCES/dashcore-0.14.0-contrib.tar.gz
```

#### [5] Build the binaries

One source RPM will often build multiple binary RPMs. In this case, six RPMs
are built (if you also build the optional debuginfo RPM). See them listed later
in this document.

_**mock and rpmbuild:**_ There are two ways to build RPMs, (1) by using `mock`
which is a wrapper around `rpmbuild` that creates an isolated build environment
(chroot) using a special use system user (mockbuild of the mock group) and
installs any needed BuildRequires into that environment without effecting your
workstation, or (2) directly with `rpmbuild` which requires you to install all
build requirements unisolated from your workstation environment.  _**We
recommend you use mock.** Mock is cool. Mock is awesome. Mock will change your
life._

**&#11835; Method 1: mock (recommended)**

Reconstruct the source rpm.

```bash
# As a normal user (not root)
mock --buildsrpm --spec ~/rpmbuild/SPECS/dashcore.spec --sources ~/rpmbuild/SOURCES/ --resultdir ~/rpmbuild/SRPMS/
```

This will create a source package and place it in `~/rpmbuild/SRPMS/`. For
example `~/rpmbuild/SRPMS/dashcore-0.14.0.5-1.taw.fc30.src.rpm`

Now build it...

```bash
# As a normal user (not root)
# Hint hint: With mock you can build for targets that are not your OS version
#            and architecture!
mock -r fedora-31-x86_64 ~/rpmbuild/SRPMS/dashcore-0.14.0.5-1.taw.fc30.src.rpm --resultdir ~/rpmbuild/RPMS/
```

This will build packages in `~/rpmbuild/RPMS/` Note, if you did not add
`--resultdir`, mock would build the packages in the mock chroot tree, like
perhaps `/var/lib/mock/fedora-31-x86_64/root/builddir/build/RPMS/`. That chroot
tree gets blown away by default nearly every time you use mock (a good thing),
so... just fair warning.

If you want to noodle around the mock chroot, (a) add `--no-clean` to your mock commands above and (b) use the built in mock shell to look around...
```bash
mock --shell
# you will be "fakeroot" in that chroot, login as the mockbuild user...
su -l mockbuild
ll
pwd
```

When you are satisfied with the build, cleanup the mock environment and set it
back to it's original state...
```bash
# As a normal user (not root)
mock --scrub all
```


**&#11835; Method 2: rpmbuild (works but not recommended)**

With this method, you use `rpmbuild` to execute the process. For example:

```bash
# As a normal user (not root)
cd ~/rpmbuild/SPECS
rpmbuild -ba dashcore.spec
```

Note, you may run into a failed build. Look at the BuildRequires in the .spec
file. For example, you may have to install a few RPMs first, like gcc-c++ and
and others. Or just note the output of the failed build and add the packages.
For example, I had to do something like this for a RHEL7 build...

**For Fedora:**
```bash
# As a normal user (not root) -- Note, this may not be comprehensive.
sudo dnf install gcc-c++ qt5-qtbase-devel qt5-linguist qrencode-devel miniupnpc-devel protobuf-devel openssl-devel desktop-file-utils autoconf automake boost-devel libdb4-cxx-devel libevent-devel libtool java python3-zmq zeromq-devel
```
**For CentOS7 and RHEL7:**
```bash
# As a normal user (not root) -- Note, this may not be comprehensive.
sudo yum install gcc-c++ qt5-qtbase-devel qt5-linguist qrencode-devel miniupnpc-devel protobuf-devel openssl-devel desktop-file-utils autoconf automake boost-devel libdb4-cxx-devel libevent-devel libtool java openssl-compat-bitcoin-libs python34
```

Manually adding those BuildRequires is a PITA and pollutes your sytem. This is
why I highly recommend you use `mock` instead of `rpmbuild`.

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

Let's say your name is Barney Miller (initials "bm0").

```bash
# As a normal user (not root)
cp dashcore.spec dashcore.bm0.spec
```

* Edit `dashcore.bm0.spec`
* Change the _minorbump_ value in that file from 'taw' to 'bm0'  
* Add a stanza in the changelog at the bottom reflective of what you did (copy
  the format)...

...and build your RPMs from that...


```bash
# versions are just examples...
# As a normal user (not root) -- rpmbuild method
#rpmbuild -ba dashcore.bm0.spec
# As a normal user (not root) -- mock method (recommended)
rpmbuild -bs dashcore.bm0.spec
mock -r fedora-31-x86_64 ~/rpmbuild/SRPMS/dashcore-0.14.0.5-1.bm0.fc30.src.rpm
```

If all goes to plan, in 30 or 40 minutes you should have a set of binary
packages, specifically built to your system with a release of '1.bm0'.

If there is a significant problem where you have to, for example, fix the
`configure.ac` file in the `dash-0.14.0.5.tar.gz` archive (common issue)... you
will have to do something like this:

* Copy the archive to some working director and then extract it...

      tar xvzf dash-0.14.0.5.tar.gz

* Copy the resultant (the original pristine) folder…

      cp -a dash-0.14.0.5 dash-0.14.0.5.orig --

* Work on the `dash-0.14.0.5/configure.ac` file, build a new patch, and try to
  rebuild things (iterate iterate iterate). All that is a bit beyond this
  document, but this is a good place to start to understand RPMs:
  <https://fedoraproject.org/wiki/How_to_create_an_RPM_package>

Finally, once built and you are happy, instead of relying on sha256sum hash
verification, you can GPG sign your packages. For instruction, read these nice
summaries (hint, you will have to install the `rpm-sign` RPM first):

* http://fedoranews.org/tchung/gpg/
* http://blog.packagecloud.io/eng/2014/11/24/howto-gpg-sign-verify-rpm-packages-yum-repositories/

And if you are feeling really ambitious, you can set up a publicly facing dnf
(once called yum) repository and making your packages available through
super-automated means to the world (keep reading the Fedora documentation for
more information about yum and dnf).

---

### That should get you started! Good luck!

Got a dash of feedback? Send it my way: <https://keybase.io/toddwarner>
