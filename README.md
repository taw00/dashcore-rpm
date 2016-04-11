# Dash Source RPMs

**Dash (Digital Cash)** is a privacy-centric digital currency that
enables instant transactions to anyone, anywhere in the world. It uses
peer-to-peer technology to operate with no central authority where
managing transactions and issuing money are carried out collectively
by the network. Dash is based on the Bitcoin software, but it has a
two tier network that improves it. Dash allows you to remain anonymous
while you make transactions, similar to cash.

Dash is also a platform for innovative decentralized crypto-tech.

More about Dash can be found here: https://dash.org
Dash on github can be found here: https://github.com/dashpay/dash

----

**This repository houses source RPMs for the latest stable (and experimental) releases of Dash.** Using these SRPMs one should be able to build binary RPMs for your specific linux variety and architecture.

A source RPM (SRPM or .src.rpm) nicely packages up the source code of a program/project and contains all the instruction needed to build (compile and package) corresponding binary RPMs. In the case of Dash, one source RPM will compile the code and generate all the binary runnable RPMs associated to the Dash project.

Important notes:

0. There are versions considered **stable** and versions considered **experimental**. Versions with an "x" in their version number should be considered the most experimental.
0. These have all been developed and tested on Fedora 23 and x86_64. I welcome folks to experiment with other distributions and architectures and let me know how they go.

----

#### [1]  Set up your rpmbuild environment

RPM? How? What?: https://fedoraproject.org/wiki/How_to_create_an_RPM_package

In order to build from a source RPM, you first need to set up your environment. If you have not already, do this as your normal user (not root) from the commandline:

```
$ rpmdev-setuptree
```

That will set up a working folder tree at `~/rpmbuild/`

_If that fails,_ you need to set up your development environment, which is beyond the scope of this document. For setting up a Fedora system, check this out: https://fedoraproject.org/wiki/How_to_create_an_RPM_package

Note, it suggests using a separate user on your system to build RPMs… you can do that, but for our examples, I am assuming you are doing it with whatever user you want. I execute these commands from my personal normal user account usually.


#### [2] Download a source RPM of your choosing

For example, at the time of this writing the latest dash src.rpm of version  `0.12.0.56`, is considered "stable". For the purposes of this document, we are going use version-release `0.12.0.56-6.taw` as our example.

#### [3] Verify the RPM has not been tampered with

This is done in one of two ways: (1) with an sha256sum hash check and (2) with a GPG signature check. Assuming the source RPM is digitally signed, GPG signature verification is vastly more secure, but more complicated.

**Verification via sha256sum**

*Note, at the end of this document, a list of the source RPMs and the sha256sums that they should match, are listed.*

From the commandline...

    $ sha256sum dash-0.12.0.56-6.taw.src.rpm

The result will be something like this and it needs to match the posted hash _(this example may be incorrect)_.

`
93a64f9c2633c2790c67e5a982802d5e266124695cb914281f75331528cf9a63  dash-0.12.0.56-6.taw.fc23.src.rpm
`

**Verification of the source RPMs digital signature**

If I built these packages correctly, their appropriate sha256 hash should be posted below _and_ they should pass a gpg digital signature check signed by my public key.

(1) Import my GPG key into your RPM keyring if you have not already done so. You have to do this as the root user.

    $ sudo rpm --import https://raw.githubusercontent.com/taw00/public-keys/master/taw-694673ED-public-2030-01-04.asc

Or navigate to http://github.com/taw00/public-keys and fetch the key manually

(2) Check the signature

    $ rpm --checksig dash-0.12.0.56-6.taw.src.rpm

You should see something like: `dash-0.12.0.56-6.taw.fc23.src.rpm: rsa sha1 (md5) pgp md5 OK`

If the package is not signed, or if the result is something less subsantial, like just `sha1 md5 OK`, or no signature. Then, I would not recommend installing the source RPM. If it says `(MISSING KEYS: RSA#694673ed (MD5) PGP#694673ed)`, you did not successfully import my key in step 1.


#### [4] Install the source RPM

Again, from the commandline as a normal user... First, copy that source RPM into the source RPMs location in the rpmbuild build tree:

    $ cp -a dash-*.src.rpm ~/rpmbuild/SRPMS/
    $ # Install the sucker:
    $ rpm -ivh dash-0.12.0.56-6.taw.src.rpm

That should explode it's source code and patch contents into ~/rpmbuild/SOURCES/ and the build instructions into ~/rpmbuild/SPECS/. Something likes this...

```
~/rpmbuild/SPECS/dash-0.12.0.56.spec
~/rpmbuild/SOURCES/v0.12.0.56.tar.gz
~/rpmbuild/SOURCES/dash-0.12.0.56-contrib-fedora.tar.gz
~/rpmbuild/SOURCES/dash-0.12.0.56-fedora.patch
```

#### [5] Build the binaries

One source RPM will often build multiple binary RPMs. In this case, six RPMs are built (with the debuginfo RPM optionally built). See them listed furthin into this document.

Actually building the binary RPMs is as easy as running the rpmbuild command against a specfile. For example:

    $ cd ~/rpmbuild/SPECS
    $ rpmbuild -ba dash-0.12.0.56-6.taw.spec

If all goes well, the build process may take 30+ minutes and nicely bog down your computer. If the build succeeded, the build process will list the RPMS that were created at the end of the terminal window output. The binary RPMs will be saved in the _~/rpmbuild/RPMS/_ directory and a newly minted source RPM will land in the _~/rpmbuild/SRPMS/_ directory. The binary RPMs will be these...

* **dash-client** -- The dash-qt wallet and full node _(note, some older sources merely named this package "dash" and not "dash-client")_
* **dash-utils** -- dash-cli, a utility to communicate with and control a Dash server via its RPC protocol, and dash-tx, a utility to create custom Dash transactions.
* **dash-server** -- dashd, a peer-to-peer node and wallet server. It is the command line installation without a GUI.  It can be used as a commandline wallet and is typically used to run a Dash Masternode. Requires dash-utils to be installed as well.
* **dash-libs** -- provides libbitcoinconsensus, which is used by third party applications to verify scripts (and other functionality in the future).
* **dash-devel** -- provides the libraries and header files necessary to compile programs which use libbitcoinconsensus. Requires dash-libs to be installed as well.
* **dash-[version info].src.rpm** -- The source code -- the source RPM, or SRPM
You want to build binaries for your RPM-based linux distribution? Use this source RPM to do so easily.
* **dash-debuginfo** -- debug information for package dash. Debug information is useful when developing applications that use this package or when debugging this package.
(99.999% of you do not need to install this)


***Are you impatient?*** Binaries for Dash have already been built for Fedora 23 on x86_64 and can be found here: https://drive.google.com/folderview?id=0B0BT-eTEFVLOdWJjWGRybW1tMjQ

----

### The sha256 verification hashes:

```
726f86097fbac3ddd0b0465b5dc0ef6300cde1be294481677ebf82b35a32282e  dash-0.12.0.56-0.taw0.fc23.src.rpm
d1a080a5ab42137ab9d8485dfd65c3f2b8a34f5f7d0966c8e2d06fe65714e11e  dash-0.12.0.56-0.taw2.fc23.src.rpm
91dbd7cded28c88aa85154913e73798cb7c25d278ea700a97e2b7fc2dd63b4bb  dash-0.12.0.56-3.taw.fc23.src.rpm
72a3940f47e60bab2145e5546eae4f7c6034ef61adb1d3eda55e6d5d23ea267b  dash-0.12.0.56-4.taw.fc23.src.rpm
297273f71b040ea2b683bf1e41e562598736fc53d6d5fdef2fb4a3eef8cc2bc8  dash-0.12.0.56-5.taw.fc23.src.rpm
93a64f9c2633c2790c67e5a982802d5e266124695cb914281f75331528cf9a63  dash-0.12.0.56-6.taw.fc23.src.rpm
6e303f3196f7431152b6f14ca5f9774aa67e53cfe0a1a5dad401fb15834b3a04  dash-0.12.1.x-20160405.0.taw.fc23.src.rpm
beeb67fcc7f67d0a9b93b7df0f393c6044a489bcfcfc734bc4de0a7e1ef7f6ae  dash-0.12.1.x-20160410.taw.fc23.src.rpm
123d350149bc0d8c5735a76b095f23425e2e3e255cf58fab0db723c6b634b615  dash-0.13.0.x-20160405.0.taw.fc23.src.rpm
c18adccfcbba110cd7fd490243f1d46f78498cc98129f31bd7de6ba36ee098f9  dash-0.13.0.x-20160410.taw.fc23.src.rpm
```
----

### Advanced: Creating your own tagged builds

If you are feeling a bit froggy, build and compile the binary RPMs specific to your name.

Let's say your name is Barney Miller (initials "bm").

```
cp dash-0.12.56.spec dash-0.12.56-6.bm.spec
```

* Edit `dash-0.12.56-6.bm.spec`
* Change the _bumptag_ value in that file from '.taw' to '.bm'
* Add a stanza in the changelog at the bottom reflective of what you did (copy the format)...

...and build your RPMs from that...


```
rpmbuild -ba dash-0.12.0.56-6.bm.spec
```

If all goes to plan, in 30 or 40 minutes you should have a set of binary packages, specifically built to your system with a release of '6.bm'.

If there is a significant problem where you have to, for example, fix the `configure.ac` file in the `v0.12.0.56.tar.gz` archive (common issue)... you will have to do something like this:

* Copy the archive to some working director and then extract it...

      tar xvzf v0.12.0.56.tar.gz

* Copy the resultant (the original pristine) folder…

      cp -a dash-0.12.0.56 dash-0.12.0.56.orig --

* Work on the `dash-0.12.0.56/configure.ac` file, build a new patch, and try to rebuild things (iterate iterate iterate). All that is a bit beyond this document, but this is a good place to start to understand RPMs: https://fedoraproject.org/wiki/How_to_create_an_RPM_package

Finally, once built and you are happy, instead of relying on sha256sum hash verification, you can GPG sign your packages. For instruction, read these nice summaries:

* http://fedoranews.org/tchung/gpg/
* http://blog.packagecloud.io/eng/2014/11/24/howto-gpg-sign-verify-rpm-packages-yum-repositories/

And if you are feeling really ambitious, you can set up a publicly facing dnf (once called yum) repository and making your packages available through super-automated means to the world (keep reading the Fedora documentation for more information about yum and dnf).

## Good Luck

That should get you started! Good luck! -todd _(dagrarian on dashtalk and slack, taw, or taw00 in various other venues)_
