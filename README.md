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

RPM? How? What?: https://fedoraproject.org/wiki/How_to_create_an_RPM_package

Once your rpmbuild environment is set up and a source RPM is downloaded, **install your source RPM** like this:

    $ rpm -ivh dash-*.src.rpm
    # ...and if you like...
    $ cp -a dash-*.src.rpm ~/rpmbuild/SRPMS/

That should explode it's source code and patch contents into ~/rpmbuild/SOURCES/ and the build instruction into ~/rpmbuild/SPECS/.

**Building binaries** is as easy as running the rpmbuild command against a specfile. For example:

    $ cd ~/rpmbuild/SPECS
    $ rpmbuild -ba dash.spec # or whatever the specfile name is

Wait 30+ minutes for it to complete and the build process will list the RPMS that were created at the end of the terminal window output. The binary RPMs will be saved in the _~/rpmbuild/RPMS/_ directory and a newly minted source RPM will land in the _~/rpmbuild/RPMS/_ directory. The binary RPMs will be these...

* **dash** -- The dash-qt wallet and full node
* **dash-utils** -- dash-cli, a utility to communicate with and control a Dash server via its RPC protocol, and dash-tx, a utility to create custom Dash transactions.
* **dash-server** -- dashd, a peer-to-peer node and wallet server. It is the command line installation without a GUI.  It can be used as a commandline wallet and is typically used to run a Dash Masternode. Requires dash-utils to be installed as well.
* **dash-libs** -- provides libbitcoinconsensus, which is used by third party applications to verify scripts (and other functionality in the future).
* **dash-devel** -- provides the libraries and header files necessary to compile programs which use libbitcoinconsensus. Requires dash-libs to be installed as well.
* **dash-[version info].src.rpm** -- The source code -- the source RPM, or SRPM
You want to build binaries for your RPM-based linux distribution? Use this source RPM to do so easily.
* **dash-debuginfo** -- debug information for package dash. Debug information is useful when developing applications that use this package or when debugging this package.
(99.999% of you do not need to install this)


Note: Binaries for Dash have already been built for Fedora 23 on x86_64 and can be found here: https://drive.google.com/folderview?id=0B0BT-eTEFVLOdWJjWGRybW1tMjQ
