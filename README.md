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

Important notes:

0. There are versions considered **stable** and versions considered **experimental**. Versions with an "x" in their version number should be considered the most experimental.
0. These have all been developed and tested on Fedora 23 and x86_64. I welcome folks to experiment with other distributions and architectures and let me know how they go.

----

#### [1]  Set up your rpmbuild environment

RPM? How? What?: https://fedoraproject.org/wiki/How_to_create_an_RPM_package

Once your rpmbuild environment is set up...

#### [2] Download a source RPM of your choosing

For example, at the time of this writing, `dash-0.12.0.56-5.taw.src.rpm`, is considered "stable".

#### [3] Verify the RPM has not been tampered with

This is done in one of two ways: (1) with an sha256sum hash check and (2) with a GPG signature check. Assuming the source RPM is digitally signed, GPG signature verification is vastly more secure, but more complicated.

**Verification via sha256sum**

*Note, at the end of this document, a list of the source RPMs and the sha256sums that they should match, are listed.*

From the commandline...

    $ sha256sum dash-0.12.0.56-5.taw.src.rpm

The result will be something like this and it needs to match the posted hash.

`
297273f71b040ea2b683bf1e41e562598736fc53d6d5fdef2fb4a3eef8cc2bc8  dash-0.12.0.56-5.taw.fc23.src.rpm
`

**Verification of the source RPMs digital signature**

If I built these packages correctly, their appropriate sha256 hash should be posted below _and_ they should pass a gpg digital signature check signed by my public key.

(1) Import my GPG key into your RPM keyring if you have not already done so. You have to do this as the root user.

    $ sudo rpm --import https://raw.githubusercontent.com/taw00/public-keys/master/taw-694673ED-public-2030-01-04.asc

Or navigate to http://github.com/taw00/public-keys and fetch the key manually

(2) Check the signature

    $ rpm --checksig dash-0.12.0.56-5.taw.src.rpm

You should see something like: `dash-0.12.0.56-5.taw.fc23.src.rpm: rsa sha1 (md5) pgp md5 OK`

`dash-0.12.0.56-5.taw.src.rp: sha1 md5 OK`

If the package is not signed, or if the result is something less subsantial, like `sha1 md5 OK`, or no signature. Then, I would not recommend installing the source RPM. If it says `(MISSING KEYS: RSA#694673ed (MD5) PGP#694673ed)`, you did not successfully import my key in step 1.


#### [4] Install the source RPM

Again, from the commandline as a normal user... First, copy that source RPM into the source RPMs location in the rpmbuild build tree:

    $ cp -a dash-*.src.rpm ~/rpmbuild/SRPMS/
    $ # Install the sucker:
    $ rpm -ivh dash-*.src.rpm

That should explode it's source code and patch contents into ~/rpmbuild/SOURCES/ and the build instructions into ~/rpmbuild/SPECS/.


#### [5] Build the binaries

One source RPM will often build multiple binary RPMs. In this case, six RPMs are built (with the debuginfo RPM optionally built). See them listed furthin into this document.

Actually building the binary RPMs is as easy as running the rpmbuild command against a specfile. For example:

    $ cd ~/rpmbuild/SPECS
    $ rpmbuild -ba dash-0.12.0.56-5.taw.spec

If all goes well, the build process may take 30+ minutes and nicely bog down your computer. If the build succeeded, the build process will list the RPMS that were created at the end of the terminal window output. The binary RPMs will be saved in the _~/rpmbuild/RPMS/_ directory and a newly minted source RPM will land in the _~/rpmbuild/SRPMS/_ directory. The binary RPMs will be these...

* **dash** -- The dash-qt wallet and full node
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

`
5976b00c4bbd1a5d5527e871c793aac9e1f9f30e3144079cd1072a53c068f493  dash-0.12.0.56-0.taw0.fc23.src.rpm
4c43723393d42d7db33c8277dcf144afc2449b7bc87a1a5b45de65b89e67fe3f  dash-0.12.0.56-0.taw2.fc23.src.rpm
1951fa168f369aff3a93ada7b0c8bbdbf6521f2f44532b1508c17e510cb2265a  dash-0.12.0.56-3.taw.fc23.src.rpm
d6616a0bb468be5f316f7955653f131295204e5ef9d54166023c62dc9cf7de3a  dash-0.12.0.56-4.taw.fc23.src.rpm
70e01f95c7d57d06a51547a46bdb12fddd613d17872327b056e90a1791567a98  dash-0.12.0.56-5.taw.fc23.src.rpm
7580ac8548cb9eb62ddc50c44d382d8a8c7b4159f388fea5c5d0d292f9c96390  dash-0.12.1.x-20160405.0.taw.fc23.src.rpm
8932fa45899946f2775a7b7449dbcc86afa8a56b5e7f43916e81313177e3b1fe  dash-0.13.0.x-20160405.0.taw.fc23.src.rpm`
