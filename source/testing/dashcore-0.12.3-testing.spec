# Dash (Digital Cash) Cryptocurrency full node and wallet
#
# This is the rpm source spec for building a Dash GUI Wallet, Masternode, and
# Full Node. Dash Masternode Sentinel is built with another spec file.
#
# Consumer facing...
# * dashcore-client
# * dashcore-server
# * dashcore-utils
#
# Specialized...
# * dashcore-libs
# * dashcore-devel
# * dashcore-debuginfo
#
# Note about edits within the spec: Any comments beginning with #t0dd are
# associated to future work or experimental elements of this spec file and
# build.
#
# Note commented out macros in this (or any) spec file. You MUST double up the
# %%'s or rpmbuild will yell at you. RPM is weird.
#
# Enjoy. Todd Warner <t0dd@protonmail.com>

%global selinux_variants mls strict targeted
%define testing_extras 0

# We usually want a debug package available and built. If you DO NOT want them
# built, un-double the %%'s and uncomment the line.
#%%define debug_package %%{nil}

# https://fedoraproject.org/wiki/Changes/Harden_All_Packages
%define _hardened_build 0

%define _name_d dash
%define _name_dc dashcore
%define _version_major 0.12.3
%define _version_minor 0

# Note: "bump" and "bumptag" are release-build identifiers.
# Often the bumptag is undefined, the builder's initials, a date, or whatever.
# To undefine, flip-flop the define/undefine ordering

%define bump 0.testing
%undefine bumptag
%define bumptag taw

%if %{?bumptag}
%define _release %{bump}.%{bumptag}
%else
%define _release %{bump}
%endif


Name: %{_name_dc}
Version: %{_version_major}.%{_version_minor}
Release: %{_release}%{?dist}
Vendor: Dash.org
Packager: Todd Warner <t0dd@protonmail.com>
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency

%define _nmv_d %{_name_d}-%{_version_major}
%define _nmv_dc %{_name_dc}-%{_version_major}
%define _nv_d %{_name_d}-%{version}
%define _nv_dc %{_name_dc}-%{version}
%define _nvr_d %{_name_d}-%{version}-%{_release}
%define _nvr_dc %{_name_dc}-%{version}-%{_release}

# dashcore source tarball file basename
# Set srcarchive value to the appropriate on for this build.
# github or from bamboo (the team build system).
#   - github convention - dash-0.12.3.0 - e.g. dash-0.12.3.0.tar.gz
#   - bamboo - dashcore-0.12.3 - e.g. dashcore-0.12.3.tar.gz
%define _srcarchive_github %{_name_d}-%{version}
%define _srcarchive_bamboo %{_name_dc}-%{_version_major}

%define srcarchive %{_srcarchive_github}
%define srccontribarchive %{_name_dc}-%{_version_major}-contrib

# Unarchived source tree structure (extracted in .../BUILD)
#   srcroot               dascore-0.12.3
#      \_srccodetree        \_dash-0.12.3.0
#      \_srccontribtree     \_dashcore-0.12.3-contrib
%define srcroot %{_name_dc}-%{_version_major}
%define srccodetree %{_name_d}-%{version}
%define srccontribtree %{_name_dc}-%{_version_major}-contrib


Group: Applications/System
License: MIT
URL: http://dash.org/
# upstream
Source0: %{srcarchive}.tar.gz

# Source archive of contributions not yet in main upstream package.
# Icons, manpages, desktop stuff, systemd stuff, etc.
# includes some future SELinux policy stuff as well (.te, .if, .fc)
Source1: %{srccontribarchive}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: gcc-c++
BuildRequires: qt5-qtbase-devel qt5-linguist
BuildRequires: qrencode-devel miniupnpc-devel protobuf-devel openssl-devel
BuildRequires: desktop-file-utils autoconf automake
BuildRequires: boost-devel libdb4-cxx-devel libevent-devel
BuildRequires: libtool java
#BuildRequires: checkpolicy selinux-policy-devel selinux-policy-doc

# I don't think this check is needed anymore -comment out for now. -t0dd
## ZeroMQ not testable yet on RHEL due to lack of python3-zmq so
## enable only for Fedora
#%%if 0%%{?fedora}
#BuildRequires: python3-zmq zeromq-devel
#%%endif

# Python tests still use OpenSSL for secp256k1, so we still need this to run
# the testsuite on RHEL7, until Red Hat fixes OpenSSL on RHEL7. It has already
# been fixed on Fedora. Bitcoin itself no longer needs OpenSSL for secp256k1.
# To support this, we are tracking https://linux.ringingliberty.com/bitcoin/el7/SRPMS/
# ...aka: https://linux.ringingliberty.com/bitcoin/el$releasever/$basearch
# We bring it in-house, rebuild, and supply at https://copr.fedorainfracloud.org/coprs/taw/dashcore-openssl-compat/
# ...aka: https://copr-be.cloud.fedoraproject.org/results/taw/dashcore-openssl-compat/epel-$releasever-$basearch/
%if %{testing_extras} && 0%{?rhel}
BuildRequires: openssl-compat-dashcore-libs
%endif


# dashcore-client
%package client
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (dash-qt GUI client)
Requires: dashcore-utils = %{version}-%{release}


# dashcore-server
%package server
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (dashd server)
Requires(post):	systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
Requires(pre): shadow-utils
Requires(post):	/usr/sbin/semodule, /sbin/restorecon, /sbin/fixfiles
Requires(postun): /usr/sbin/semodule, /sbin/restorecon, /sbin/fixfiles
Requires: openssl-libs
Requires: dashcore-utils = %{version}-%{release}
Requires: dashcore-sentinel
#t0dd Requires: selinux-policy
#t0dd Requires: policycoreutils-python


# dashcore-libs
%package libs
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (consensus libraries)


# dashcore-devel
%package devel
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (dev libraries and headers)
Requires: dashcore-libs = %{version}-%{release}


# dashcore-utils
%package utils
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (commandline utils)


# dashcore src.rpm
%description
This is the source package for building most of the Dash Core set of binary
packages.  It will build dashcore-{client,server,utils,libs,devel,debuginfo}.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a strong
focus on serving the payments industry. Dash offers a form of money that is
portable, inexpensive, divisible and fast. It can be spent securely both online
and in person with minimal transaction fees. Dash offers instant transactions
(InstantSend), private transactions (PrivateSend), and operates a
self-governing and self-funding model. This decentralized governance and
budgeting system makes it one of the first ever successful decentralized
autonomous organizations (DAO). Dash is also a platform for innovative
decentralized crypto-tech.

Learn more at www.dash.org.


# dashcore-client
%description client
This package provides dash-qt, a user-friendly-er GUI wallet manager for
personal use. This package requires the dashcore-utils RPM package to be
installed as well.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a strong
focus on serving the payments industry. Dash offers a form of money that is
portable, inexpensive, divisible and fast. It can be spent securely both online
and in person with minimal transaction fees. Dash offers instant transactions
(InstantSend), private transactions (PrivateSend), and operates a
self-governing and self-funding model. This decentralized governance and
budgeting system makes it one of the first ever successful decentralized
autonomous organizations (DAO). Dash is also a platform for innovative
decentralized crypto-tech.

Learn more at www.dash.org.


# dashcore-server
%description server
This package provides dashd, a peer-to-peer node and wallet server. It is the
command line installation without a GUI. It can be used as a commandline wallet
but is typically used to run a Dash Full Node or Masternode. This package
requires the dashcore-utils and dashcore-sentinel RPM packages to be installed.

Please refer to Dash Core documentation at dash.org for more information about
running a Masternode.

-

A Dash Full Node is a un-collatoralized member of a decentralized network of
servers that validate transactions and blocks. A Dash Masternode is a member of
a network of incentivized servers that perform expanded critical services for
the Dash cryptocurrency protocol.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a strong
focus on serving the payments industry. Dash offers a form of money that is
portable, inexpensive, divisible and fast. It can be spent securely both online
and in person with minimal transaction fees. Dash offers instant transactions
(InstantSend), private transactions (PrivateSend), and operates a
self-governing and self-funding model. This decentralized governance and
budgeting system makes it one of the first ever successful decentralized
autonomous organizations (DAO). Dash is also a platform for innovative
decentralized crypto-tech.

Learn more at www.dash.org.



# dashcore-libs
%description libs
This package provides libdashconsensus, which is used by third party
applications to verify scripts (and other functionality in the future).

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a strong
focus on serving the payments industry. Dash offers a form of money that is
portable, inexpensive, divisible and fast. It can be spent securely both online
and in person with minimal transaction fees. Dash offers instant transactions
(InstantSend), private transactions (PrivateSend), and operates a
self-governing and self-funding model. This decentralized governance and
budgeting system makes it one of the first ever successful decentralized
autonomous organizations (DAO). Dash is also a platform for innovative
decentralized crypto-tech.

Learn more at www.dash.org.


# dashcore-devel
%description devel
This package provides the libraries and header files necessary to compile
programs which use libdashconsensus.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a strong
focus on serving the payments industry. Dash offers a form of money that is
portable, inexpensive, divisible and fast. It can be spent securely both online
and in person with minimal transaction fees. Dash offers instant transactions
(InstantSend), private transactions (PrivateSend), and operates a
self-governing and self-funding model. This decentralized governance and
budgeting system makes it one of the first ever successful decentralized
autonomous organizations (DAO). Dash is also a platform for innovative
decentralized crypto-tech.

Learn more at www.dash.org.


# dashcore-utils
%description utils
This package provides dash-cli, a utility to communicate with and control a
Dash server via its RPC protocol, and dash-tx, a utility to create custom Dash
transactions.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a strong
focus on serving the payments industry. Dash offers a form of money that is
portable, inexpensive, divisible and fast. It can be spent securely both online
and in person with minimal transaction fees. Dash offers instant transactions
(InstantSend), private transactions (PrivateSend), and operates a
self-governing and self-funding model. This decentralized governance and
budgeting system makes it one of the first ever successful decentralized
autonomous organizations (DAO). Dash is also a platform for innovative
decentralized crypto-tech.

Learn more at www.dash.org.



%prep
# Prep section starts us in directory .../BUILD
# process dashcore - Source0 - untars in:
# .../BUILD/dashcore-0.12.3/dashcore-0.12.3.0/
mkdir %{srcroot}
%setup -q -T -D -a 0 -n %{srcroot}
#%%setup -q -T -a 0 -c -n %{srcroot}
# extra contributions - Source1 - untars in:
# .../BUILD/dashcore-0.12.3/dashcore-0.12.3-contrib/
%setup -q -T -D -a 1 -n %{srcroot}

# Prep section now moves us into .../BUILD/%{srcroot}
# .../BUILD/dashcore-0.12.3/

# Install README files
#t0dd cp -p %%{SOURCE8} %%{SOURCE9} %%{SOURCE10} .

# Prep SELinux policy -- NOT USED YET
# Done here to prep for action taken in the %%build step
# At this moment, we are in the srcroot directory
mkdir -p selinux-tmp
cp -p %{srccontribtree}/linux/selinux/dash.{te,if,fc} selinux-tmp/

# We leave with this structure (for example)...
# ~/rpmbuild/BUILD/dashcore-0.12.3/dash-0.12.3.0/
# ~/rpmbuild/BUILD/dashcore-0.12.3/dashcore-0.12.3-contrib/...
# ...unless we are using the bamboo nomenclature...
# ~/rpmbuild/BUILD/dashcore-0.12.3/dashcore-0.12.3/
# ~/rpmbuild/BUILD/dashcore-0.12.3/dashcore-0.12.3-contrib/...


%build
# This section starts us in directory .../BUILD/dashcore-0.12.3
# So, we're in srcroot. We need to cd into srccodetree, the codetree.
# cd into dashcore-X.Y.Z/dash-X.Y.Z.zz
cd %{srccodetree}
./autogen.sh
%configure --enable-reduce-exports --enable-glibc-back-compat

make %{?_smp_mflags}

# Not using for now. Doubling up %%'s to stop macro expansion in comments.
#t0dd # Build SELinux policy
#t0dd pushd selinux-tmp
#t0dd for selinuxvariant in %%{selinux_variants}
#t0dd do
#t0dd # FIXME: Create and debug SELinux policy
#t0dd   make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
#t0dd   mv dash.pp dash.pp.${selinuxvariant}
#t0dd   make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
#t0dd done
#t0dd popd

# Exit from srccodetree back into the root of the tree
cd ..


%check
# This section starts us in directory .../BUILD/dashcore-0.12.3
# So, we start in that root tree structure cd in to the code tree and the contrib tree and in and out installing things to the buildroot.
cd %{srccodetree}
%if %{testing_extras}
# Run all the tests
make check
# Run all the other tests
#t0dd COMMENTED OUT FOR NOW -- Requires https://github.com/dashpay/dash_hash
#t0dd incorporated into the builds and that is not done yet.
#t0dd pushd src
#t0dd srcdir=. test/bitcoin-util-test.py
#t0dd popd
#t0dd LD_LIBRARY_PATH=/opt/openssl-compat-dashcore/lib PYTHONUNBUFFERED=1  qa/pull-tester/rpc-tests.py -extended
%endif
cd ..


%install
rm -rf %{buildroot} ; mkdir %{buildroot}
# This section starts us in directory .../BUILD/dashcore-0.12.3
# First, cd into the code tree and do stuff...
cd %{srccodetree}
make INSTALL="install -p" CP="cp -p" DESTDIR=%{buildroot} install
cd ..

# TODO: Upstream puts dashd in the wrong directory. Need to fix the
# upstream Makefiles to relocate it. Someday.
install -d -m755 -p %{buildroot}%{_sbindir}
install -D -m755 -p %{buildroot}%{_bindir}/dashd %{buildroot}%{_sbindir}/dashd
rm -f %{buildroot}%{_bindir}/dashd

%if ! %{testing_extras}
# Remove the test binaries if still floating around
rm -f %{buildroot}%{_bindir}/test_*
rm -f %{buildroot}%{_bindir}/bench_dash
%endif


# Install / config ancillary files
# Cheatsheet for macros:
#   _datadir = /usr/share
#   _mandir = /usr/share/man
#   _sysconfdir = /etc
#   _localstatedir = /var
#   _sharedstatedir is /var/lib
#   _prefix = /usr
#   _tmpfilesdir = /usr/lib/tmpfiles.d
#   _unitdir = /usr/lib/systemd/system
#   _libdir = /usr/lib or /usr/lib64 (depending on system)
#   https://fedoraproject.org/wiki/Packaging:RPMMacros
install -d %{buildroot}%{_datadir}
install -d %{buildroot}%{_mandir}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_localstatedir}
install -d %{buildroot}%{_sharedstatedir}
install -d %{buildroot}%{_prefix}
install -d %{buildroot}%{_tmpfilesdir}
install -d %{buildroot}%{_unitdir}

# Application as systemd service directory structure
# /etc/dashcore/
install -d -m750 -p %{buildroot}%{_sysconfdir}/dashcore
# /var/lib/dashcore/...
install -d -m750 -p %{buildroot}%{_sharedstatedir}/dashcore
install -d -m750 -p %{buildroot}%{_sharedstatedir}/dashcore/testnet3
install -d %{buildroot}%{_sharedstatedir}/dashcore/.dashcore
# /var/log/dashcore/...
install -d -m700 %{buildroot}%{_localstatedir}/log/dashcore
install -d -m700 %{buildroot}%{_localstatedir}/log/dashcore/testnet3
# /etc/sysconfig/dashd-scripts/
install -d %{buildroot}%{_sysconfdir}/sysconfig/dashd-scripts

# Symlinks needed
# debug.log: /var/lib/dashcore/debug.log -> /var/log/dashcore/debug.log
ln -s %{_localstatedir}/log/dashcore/debug.log %{buildroot}%{_sharedstatedir}/dashcore/debug.log
# debug.log: /var/lib/dashcore/testnet3/debug.log -> /var/log/dashcore/testnet3/debug.log
ln -s %{_localstatedir}/log/dashcore/testnet3/debug.log %{buildroot}%{_sharedstatedir}/dashcore/testnet3/debug.log
# config: /var/lib/dashcore/.dashcore/dash.conf -> /etc/dashcore/dash.conf (convenience symlink)
ln -s %{_sysconfdir}/dashcore/dash.conf %{buildroot}%{_sharedstatedir}/dashcore/.dashcore/dash.conf

# Man Pages (from contrib)
cd %{srccontribtree}
install -d %{buildroot}%{_mandir}/man1
install -D -m644 ./linux/man/man1/* %{buildroot}%{_mandir}/man1/
gzip %{buildroot}%{_mandir}/man1/dashd.1
gzip %{buildroot}%{_mandir}/man1/dash-qt.1
install -d %{buildroot}%{_mandir}/man5
install -D -m644 ./linux/man/man5/* %{buildroot}%{_mandir}/man5/
gzip %{buildroot}%{_mandir}/man5/dash.conf.5
gzip %{buildroot}%{_mandir}/man5/masternode.conf.5
cd ..

# Desktop elements - desktop file and kde protocol file (from contrib)
cd %{srccontribtree}
install -D -m644 ./linux/desktop/dash-qt.desktop %{buildroot}%{_datadir}/applications/dash-qt.desktop
install -D -m644 ./linux/desktop/usr-share-kde4-services_dash-qt.protocol %{buildroot}%{_datadir}/kde4/services/dash-qt.protocol
# Desktop elements - hicolor icons
install -D -m644 ./linux/desktop/dash-hicolor-128.png      %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/dash.png
install -D -m644 ./linux/desktop/dash-hicolor-16.png       %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/dash.png
install -D -m644 ./linux/desktop/dash-hicolor-22.png       %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/dash.png
install -D -m644 ./linux/desktop/dash-hicolor-24.png       %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/dash.png
install -D -m644 ./linux/desktop/dash-hicolor-256.png      %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/dash.png
install -D -m644 ./linux/desktop/dash-hicolor-32.png       %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/dash.png
install -D -m644 ./linux/desktop/dash-hicolor-48.png       %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/dash.png
install -D -m644 ./linux/desktop/dash-hicolor-scalable.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/dash.svg
# Desktop elements - HighContrast icons
install -D -m644 ./linux/desktop/dash-HighContrast-128.png      %{buildroot}%{_datadir}/icons/HighContrast/128x128/apps/dash.png
install -D -m644 ./linux/desktop/dash-HighContrast-16.png       %{buildroot}%{_datadir}/icons/HighContrast/16x16/apps/dash.png
install -D -m644 ./linux/desktop/dash-HighContrast-22.png       %{buildroot}%{_datadir}/icons/HighContrast/22x22/apps/dash.png
install -D -m644 ./linux/desktop/dash-HighContrast-24.png       %{buildroot}%{_datadir}/icons/HighContrast/24x24/apps/dash.png
install -D -m644 ./linux/desktop/dash-HighContrast-256.png      %{buildroot}%{_datadir}/icons/HighContrast/256x256/apps/dash.png
install -D -m644 ./linux/desktop/dash-HighContrast-32.png       %{buildroot}%{_datadir}/icons/HighContrast/32x32/apps/dash.png
install -D -m644 ./linux/desktop/dash-HighContrast-48.png       %{buildroot}%{_datadir}/icons/HighContrast/48x48/apps/dash.png
install -D -m644 ./linux/desktop/dash-HighContrast-scalable.svg %{buildroot}%{_datadir}/icons/HighContrast/scalable/apps/dash.svg
cd ..

# Misc pixmaps - unsure if they are even used... (from contrib)
cd %{srccontribtree}
install -d %{buildroot}%{_datadir}/pixmaps
install -D -m644 ./extras/pixmaps/* %{buildroot}%{_datadir}/pixmaps/
cd ..

# TESTING ONLY: For test releases, uncomment the next line
#desktop-file-validate %%{buildroot}%%{_datadir}/applications/dash-qt.desktop

# Config
# Install default configuration file (from contrib)
cd %{srccontribtree}
install -D -m640 ./linux/systemd/etc-dashcore_dash.conf %{buildroot}%{_sysconfdir}/dashcore/dash.conf
install -D -m644 ./linux/systemd/etc-dashcore_dash.conf ./extras/dash.conf.example
echo "\
# ---------------------------------------------------------------------------
# Example of a minimalistic configuration. Change the password. Additionally,
# some of these settings are more explicit than they need to be.

# Note, the RPM spec file sets dashcore user's homedir to be /var/lib/dashcore
# The datadir is also set to the same.
datadir=/var/lib/dashcore

testnet=0
daemon=1
# We allow RPC calls
server=1
# We participate peer-to-peer
listen=1
maxconnections=8

# A systemd managed masternode probably not going to be a wallet as well
# Set to 0 if you also want it to be a wallet.
disablewallet=1

# Only localhost allowed to connect to make RPC calls.
rpcallowip=127.0.0.1

# Example RPC username and password.
rpcuser=rpcuser-CHANGEME-`head -c 32 /dev/urandom | base64 | head -c 4`
rpcpassword=CHANGEME`head -c 32 /dev/urandom | base64`
" >> %{buildroot}%{_sysconfdir}/dashcore/dash.conf

echo "\
# ---------------------------------------------------------------------------
# Example of a minimalistic configuration. Change the password if you use
# this. Additionally, some of these settings are more explicit than they need
# to be.

# Commented out means datadir is ~/.dashcore
#datadir=/var/lib/dashcore

testnet=0
daemon=0
# We allow RPC calls
server=1
# We participate peer-to-peer
listen=1
maxconnections=8

# Set to 0 if you also want this to be a wallet.
disablewallet=0

# Only localhost allowed to connect to make RPC calls.
rpcallowip=127.0.0.1

# Example RPC username and password.
rpcuser=rpcuser-CHANGEME-`head -c 32 /dev/urandom | base64 | head -c 4`
rpcpassword=CHANGEME`head -c 32 /dev/urandom | base64`
" >> ./extras/dash.conf.example

# ...message about the convenience symlink:
echo "\
This directory and symlink only exist as a convenience so that you don't
have to type -conf=/etc/dashcore/dash.conf all the time on the commandline.

The dashcore user home dir is here: /var/lib/dashcore
The dash config file is housed here: /etc/dashcore/dash.conf
The systemd managed dash datadir is here: /var/lib/dashcore

Therefore, if -conf= is not specified on the commandline, dash will look for
the configuration file in /var/lib/dashcore/.dashcore/dash.conf
" > %{buildroot}%{_sharedstatedir}/dashcore/.dashcore/README
cd ..

# Install system services files (from contrib)
cd %{srccontribtree}
install -D -m600 -p ./linux/systemd/etc-sysconfig_dashd %{buildroot}%{_sysconfdir}/sysconfig/dashd
install -D -m755 -p ./linux/systemd/etc-sysconfig-dashd-scripts_dashd.send-email.sh %{buildroot}%{_sysconfdir}/sysconfig/dashd-scripts/dashd.send-email.sh
install -D -m644 -p ./linux/systemd/usr-lib-systemd-system_dashd.service %{buildroot}%{_unitdir}/dashd.service
install -D -m644 -p ./linux/systemd/usr-lib-tmpfiles.d_dashd.conf %{buildroot}%{_tmpfilesdir}/dashd.conf
# ...logrotate file rules
install -D -m644 -p ./linux/logrotate/etc-logrotate.d_dashcore %{buildroot}/etc/logrotate.d/dashcore
# ...ghosting a log file - we have to own the log file
touch %{buildroot}%{_sharedstatedir}/dashcore/debug.log
touch %{buildroot}%{_sharedstatedir}/dashcore/testnet3/debug.log
cd ..


# FirewallD service definition files for full and master -nodes (from contrib)
cd %{srccontribtree}
install -D -m644 -p ./linux/firewalld/usr-lib-firewalld-services_dashcore.xml %{buildroot}%{_prefix}/lib/firewalld/services/dashcore.xml
install -D -m644 -p ./linux/firewalld/usr-lib-firewalld-services_dashcore-testnet.xml %{buildroot}%{_prefix}/lib/firewalld/services/dashcore-testnet.xml
install -D -m644 -p ./linux/firewalld/usr-lib-firewalld-services_dashcore-rpc.xml %{buildroot}%{_prefix}/lib/firewalld/services/dashcore-rpc.xml
install -D -m644 -p ./linux/firewalld/usr-lib-firewalld-services_dashcore-testnet-rpc.xml %{buildroot}%{_prefix}/lib/firewalld/services/dashcore-testnet-rpc.xml
cd ..

# Not using for now. Doubling up %%'s to stop macro expansion in comments.
#t0dd # Install SELinux policy
#t0dd for selinuxvariant in %%{selinux_variants}
#t0dd do
#t0dd 	install -d %%{buildroot}%%{_datadir}/selinux/${selinuxvariant}
#t0dd 	install -p -m 644 SELinux/dash.pp.${selinuxvariant} \
#t0dd 		%%{buildroot}%%{_datadir}/selinux/${selinuxvariant}/dash.pp
#t0dd done


%clean
rm -rf %{buildroot}


# dashcore-client
%post client
# firewalld only partially picks up changes to its services files without this
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

# dashcore-server
%pre server
# This is for the case that you run dash core as a service (systemctl start dash)
# _sharedstatedir is /var/lib
getent group dashcore >/dev/null || groupadd -r dashcore
getent passwd dashcore >/dev/null || useradd -r -g dashcore -d %{_sharedstatedir}/dashcore -s /sbin/nologin -c "System user 'dashcore' to isolate Dash Core execution" dashcore

# Notes:
#  _sharedstatedir is /var/lib
#  /var/lib/dashcore is the $HOME for the dashcore user

# Fix the debug.log directory structure if it is not aligned to /var/log/ standards.
# If /var/lib/dashcore/debug.log is not a symlink, we need to fix that.
%define vlibdc %{_sharedstatedir}/dashcore
%define vlibdc_dl %{vlibdc}/debug.log
%define vlibdc_tdl %{vlibdc}/testnet3/debug.log
%define vlogdc %{_localstatedir}/log/dashcore
%define vlogdc_dl %{vlogdc}/debug.log
%define vlogdc_tdl %{vlogdc}/testnet3/debug.log
# If either debug.log is not a symlink, we need to move files and then fix the symlinks
# Hopefully this doesn't break because dashcore may have debug.log open
if [ -e %{vlibdc_dl} -a -f %{vlibdc_dl} -a ! -h %{vlibdc_dl} ]
then
   mv %{vlibdc_dl}* %{vlogdc}/
   ln -s %{vlogdc_dl} %{vlibdc_dl}
   chown dashcore:dashcore %{vlogdc_dl}*
   chmod 644 %{vlogdc_dl}*
  fi
fi
if [ -e %{vlibdc_tdl} -a -f %{vlibdc_tdl} -a ! -h %{vlibdc_tdl} ]
then
   mv %{vlibdc_tdl}* %{vlogtdc}/
   ln -s %{vlogdc_tdl} %{vlibdc_tdl}
   chown dashcore:dashcore %{vlogdc_tdl}*
   chmod 644 %{vlogdc_tdl}*
  fi
fi



exit 0


# dashcore-server
%post server
%systemd_post dashd.service
# firewalld only partially picks up changes to its services files without this
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

# Not using for now. Doubling up %%'s to stop macro expansion in comments.
#t0dd for selinuxvariant in %%{selinux_variants}
#t0dd do
#t0dd 	/usr/sbin/semodule -s ${selinuxvariant} -i \
#t0dd 		%%{_datadir}/selinux/${selinuxvariant}/dash.pp \
#t0dd 		&> /dev/null || :
#t0dd done
#t0dd # FIXME This is less than ideal, but until dwalsh gives me a better way...
#t0dd /usr/sbin/semanage port -a -t dash_port_t -p tcp 9999
#t0dd /usr/sbin/semanage port -a -t dash_port_t -p tcp 9998
#t0dd /usr/sbin/semanage port -a -t dash_port_t -p tcp 19999
#t0dd /usr/sbin/semanage port -a -t dash_port_t -p tcp 19998
#t0dd /sbin/fixfiles -R dashcore-server restore &> /dev/null || :
#t0dd /sbin/restorecon -R %%{_sharedstatedir}/dashcore || :


# dashcore-server
%posttrans server
/usr/bin/systemd-tmpfiles --create


# dashcore-server
%preun server
%systemd_preun dashd.service


# dashcore-server
%postun server
%systemd_postun dashd.service
# Not using for now. Doubling up %%'s to stop macro expansion in comments.
#t0dd# Do this upon uninstall (not upgrades)
#t0dd if [ $1 -eq 0 ] ; then
#t0dd 	# FIXME This is less than ideal, but until dwalsh gives me a better way...
#t0dd 	/usr/sbin/semanage port -d -p tcp 9999
#t0dd 	/usr/sbin/semanage port -d -p tcp 9998
#t0dd 	/usr/sbin/semanage port -d -p tcp 19999
#t0dd 	/usr/sbin/semanage port -d -p tcp 19998
#t0dd 	for selinuxvariant in %%{selinux_variants}
#t0dd 	do
#t0dd 		/usr/sbin/semodule -s ${selinuxvariant} -r dash \
#t0dd 		&> /dev/null || :
#t0dd 	done
#t0dd 	/sbin/fixfiles -R dashcore-server restore &> /dev/null || :
#t0dd 	[ -d %%{_sharedstatedir}/dashcore ] && \
#t0dd 		/sbin/restorecon -R %%{_sharedstatedir}/dashcore \
#t0dd 		&> /dev/null || :
#t0dd fi



# dashcore-client
%files client
%defattr(-,root,root,-)
%license %{srccodetree}/COPYING
%doc %{srccodetree}/doc/*.md %{srccontribtree}/extras/dash.conf.example
%{_bindir}/dash-qt
%{_datadir}/applications/dash-qt.desktop
%{_datadir}/kde4/services/dash-qt.protocol
%{_datadir}/pixmaps/*
%{_datadir}/icons/*
%{_mandir}/man1/dash-qt.1.gz
%{_mandir}/man5/masternode.conf.5.gz
%{_prefix}/lib/firewalld/services/dashcore.xml
%{_prefix}/lib/firewalld/services/dashcore-testnet.xml
%{_prefix}/lib/firewalld/services/dashcore-rpc.xml
%{_prefix}/lib/firewalld/services/dashcore-testnet-rpc.xml
#%%dir %%attr(750,dashcore,dashcore) %%{_sysconfdir}/dashcore
#%%config(noreplace) %%attr(640,dashcore,dashcore) %%{_sysconfdir}/dashcore/dash.conf

%if %{testing_extras}
%{_bindir}/test_dash-qt
%endif


# dashcore-server
%files server
%defattr(-,root,root,-)
%license %{srccodetree}/COPYING

# Application as systemd service directory structure
# /etc/dashcore/
%dir %attr(750,dashcore,dashcore) %{_sysconfdir}/dashcore
# /var/lib/dashcore/...
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore/testnet3
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore/.dashcore
# /var/log/dashcore/...
%dir %attr(700,dashcore,dashcore) %{_localstatedir}/log/dashcore
%dir %attr(700,dashcore,dashcore) %{_localstatedir}/log/dashcore/testnet3
# /etc/sysconfig/dashd-scripts/
%dir %attr(755,dashcore,dashcore) %{_sysconfdir}/sysconfig/dashd-scripts

%doc %{srccodetree}/doc/*.md %{srccontribtree}/extras/dash.conf.example
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/sysconfig/dashd
%attr(755,root,root) %{_sysconfdir}/sysconfig/dashd-scripts/dashd.send-email.sh
# ...log files - they don't initially exist, but we still own them
%ghost %{_localstatedir}/log/dashcore/debug.log
%ghost %{_localstatedir}/log/dashcore/testnet3/debug.log
# ...the symlinks for log files...
#%%attr(777,dashcore,dashcore) %%{_sharedstatedir}/dashcore/debug.log
#%%attr(777,dashcore,dashcore) %%{_sharedstatedir}/dashcore/testnet3/debug.log
%{_sharedstatedir}/dashcore/debug.log
%{_sharedstatedir}/dashcore/testnet3/debug.log
%attr(644,root,root) /etc/logrotate.d/dashcore

# dash.conf
%config(noreplace) %attr(640,dashcore,dashcore) %{_sysconfdir}/dashcore/dash.conf
# ...convenience symlink:
#    /var/lib/dashcore/.dashcore/dash.conf -> /etc/dashcore/dash.conf
# ...this is probably really bad form.
%attr(640,dashcore,dashcore) %{_sharedstatedir}/dashcore/.dashcore/README
#%%attr(777,dashcore,dashcore) %%{_sharedstatedir}/dashcore/.dashcore/dash.conf
%{_sharedstatedir}/dashcore/.dashcore/dash.conf

%{_unitdir}/dashd.service
%{_prefix}/lib/firewalld/services/dashcore.xml
%{_prefix}/lib/firewalld/services/dashcore-testnet.xml
%{_prefix}/lib/firewalld/services/dashcore-rpc.xml
%{_prefix}/lib/firewalld/services/dashcore-testnet-rpc.xml
%doc selinux-tmp/*
%{_sbindir}/dashd
%{_tmpfilesdir}/dashd.conf
%{_mandir}/man1/dashd.1.gz
%{_mandir}/man5/dash.conf.5.gz
%{_mandir}/man5/masternode.conf.5.gz
#t0dd %%{_datadir}/selinux/*/dash.pp

%if %{testing_extras}
%{_bindir}/test_dash
%{_bindir}/bench_dash
%endif


# dashcore-libs
%files libs
%defattr(-,root,root,-)
%license %{srccodetree}/COPYING
%{_libdir}/libdashconsensus.so*


# dashcore-devel
%files devel
%defattr(-,root,root,-)
%license %{srccodetree}/COPYING
%{_includedir}/dashconsensus.h
%{_libdir}/libdashconsensus.a
%{_libdir}/libdashconsensus.la
%{_libdir}/pkgconfig/libdashconsensus.pc


# dashcore-utils
%files utils
%defattr(-,root,root,-)
%license %{srccodetree}/COPYING
%{_bindir}/dash-cli
%{_bindir}/dash-tx


# Dash Core Information
#
# Dash...
#   * Project website: https://www.dash.org
#   * Project documentation: https://docs.dash.org
#
# Dash Core on Fedora/CentOS/RHEL...
#   * Git Repo: https://github.com/taw00/dashcore-rpm
#   * Documentation: https://github.com/taw00/dashcore-rpm/tree/master/documentation
#
# Source snapshots...
#   * Tagged release builds: https://github.com/dashpay/dash/tags
#     dash-0.12.3.0.tar.gz
#   * Test builds...
#     https://bamboo.dash.org/browse/DASHL-REL/latestSuccessful
#     Then > Artifacts > gitian-linux-dash-src > [download the tar.gz file]
#     dashcore-0.12.3.tar.gz
#
# Dash Core git repos...
#   * Dash: https://github.com/dashpay/dash
#   * Sentinel: https://github.com/dashpay/sentinel

%changelog
* Fri Apr 6 2018 Todd Warner <t0dd@protonmail.com> 0.12.3.0-0.testing.taw
- PLACEHOLDER ENTRY
- Release - PLACEHOLDER
- PLACEHOLDER-HASH dashcore-0.12.3.tar.gz
- 329c49b034c601e082f815a5aa12d9f865de17343809d3e9f01b10f7eaa619f8 dashcore-0.12.3-contrib.tar.gz
- https://github.com/dashpay/dash/releases/tag/v0.12.3.0
-
* Tue Dec 19 2017 Todd Warner <t0dd@protonmail.com> 0.12.2.2-1.testing.taw
- Release Candidate - 8506678
- 2ce4cc76540be3760ebb7c31a81ede67b9682924da68d905fbbad58273d33b2f dashcore-0.12.2.tar.gz
- b09f09d847e02e1509dd157aca1655bbe5ca79106fe4cf2e4370228e0eab79e3 dashcore-0.12.2-contrib.tar.gz
-
* Sat Dec 09 2017 Todd Warner <t0dd@protonmail.com> 0.12.2.2-0.testing.taw
- Release Candidate - f9f28e7
- fb8b023836b2cbe81b437e867b6b1176edbd7220435cf4620acc1417a5111b0d dashcore-0.12.2.tar.gz
- b09f09d847e02e1509dd157aca1655bbe5ca79106fe4cf2e4370228e0eab79e3 dashcore-0.12.2-contrib.tar.gz
-
* Sun Nov 12 2017 Todd Warner <t0dd@protonmail.com> 0.12.2.1-0.testing.taw
- Release Candidate - 20bacfa
- c1522e62ed3117639e84b757af43ed06d8ea202e25e3f62b20c7d9ee5337cc36 dashcore-0.12.2.tar.gz
- b09f09d847e02e1509dd157aca1655bbe5ca79106fe4cf2e4370228e0eab79e3 dashcore-0.12.2-contrib.tar.gz
-
* Wed Nov 8 2017 Todd Warner <t0dd@protonmail.com> 0.12.2.0-1.testing.taw
- Release Candidate - ec8178c
- 8faccdeb2d56e398f336705730039aea26f86eaa6a34bbd7a11bb2896f68cb84 dashcore-0.12.2.tar.gz
- b09f09d847e02e1509dd157aca1655bbe5ca79106fe4cf2e4370228e0eab79e3 dashcore-0.12.2-contrib.tar.gz
-
* Fri Oct 20 2017 Todd Warner <t0dd@protonmail.com> 0.12.2.0-0.testing.taw
- 824fb78820094053a0db7cdf9f883e66bd69114c1bf3517f1638bbd1971233b9 dashcore-0.12.2.tar.gz
- b09f09d847e02e1509dd157aca1655bbe5ca79106fe4cf2e4370228e0eab79e3 dashcore-0.12.2-contrib.tar.gz
-
* Tue Apr 11 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.5-0.rc.taw
- Fixes a watchdog propagation issue.
- 4e52b2427f1ea46f0ff5b31b0dd044478fba6a076611a97a9c2d3d345374459f  dash-0.12.1.5.tar.gz
- e3e4351656afda2ff23cb142d264af4b4d04d0bbe9f3326ce24019423f6adf94  dashcore-0.12.1-contrib.tar.gz
-
* Wed Mar 22 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.4-0.rc.taw
- Added RPC port to available firewalld services.
- Renamed firewalld services to match bitcoin's firewalld service name taxonomies.
- 7218baaa1aa8052960ffc0c36904b6f5647256f9773c17e8506be37a2d3cc0cb  dash-0.12.1.4.tar.gz
- e3e4351656afda2ff23cb142d264af4b4d04d0bbe9f3326ce24019423f6adf94  dashcore-0.12.1-contrib.tar.gz
- 
* Fri Mar 10 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.3-2.rc.taw
- Added RPC port to available firewalld services.
- 1f6e6fb528151c8703019ed1511562b0c8bc91fe8c7ac6838a3811ffd1af288a  dash-0.12.1.3.tar.gz
- 15d74665442062bce83e0c5d309d7c0d26de7cbd485a838b0d3630e3ad6855b2  dashcore-0.12.1-contrib.tar.gz
- 
* Sat Mar 04 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.3-1.rc.taw
- Brought back the test scripts (most of them), made them conditional. Added
- back and adjusted build-requires for openssl-compat that uses our own
- openssl-compat builds. Test scripts / openssl-compat seem to only work for
- very old linux--CentOS7/RHEL7 Ie. I have more work to do to make them part of
- the build.
-
- "bumptag" now can be defined or undefined and we do the right thing.
- 
* Thu Mar 02 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.3-0.rc.taw
- Release 0.12.1.3 - 119fe83
- Announcement: https://github.com/dashpay/dash/releases/tag/v0.12.1.3
- 1f6e6fb528151c8703019ed1511562b0c8bc91fe8c7ac6838a3811ffd1af288a  dash-0.12.1.3.tar.gz
- d4c0f01ea5fa017f6362269495d2cd32e724d9e4d2e584bf5e9a0057b493dfbb  dashcore-0.12.1-contrib.tar.gz
-
* Fri Feb 24 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.2-0.rc.taw
- Release 0.12.1.2 Release Candidate - a1ef547
- Announcement: https://github.com/dashpay/dash/releases/tag/v0.12.1.2
- 8a99d35dd7b87c42efa698d2ac36f2cca98aa501ce2f7dcb5e8d27b749efb72d  dash-0.12.1.2.tar.gz
- 04335cbef729480e6b7c11243a0613a34c128f3388f97e80b255bd05fd27cae3  dashcore-0.12.1-contrib.tar.gz
-
- Specfile change: Structure of build tree expansion changed allowing
- flexibility in how the source is generated upstream (bamboo vs. github)
- Specfile change: Added a bunch of documentation from the main tree.
- dashd.init updated
- dashd.send-email.sh with much clearer messaging.
-
* Mon Feb 20 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.1-1.taw
- Still massaging systemd service and configuration settings.
- Boosting startup timeout window significantly to avoid shooting ourselves
- in the foot too quickly. Also PIDFile= is not necessary.
- Reduced default maxconnections to 8 since we have so many masternodes.
- Fixed a systemd-managed tmpfile perms issue.
-
* Sun Feb 19 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.1-0.taw
- Release 0.12.1.1 - e9e5a24
- Announcement: https://github.com/dashpay/dash/releases/tag/v0.12.1.1
- Stability improvements. Governance object sync time improvements.
- systemd service file and configuration tweaks.
- lots of other bug fixes
-
* Fri Feb 17 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.0-2.taw
- dashd.service can be configured to send email upon start, stop,
- restart
-
* Fri Feb 10 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.0-1.taw
- With Debuginfo Package built -- there have been segfaults. This
- should help troubleshoot.
-
* Sun Feb 05 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.0-0.taw
- Release 12.1.0 - 56971f8
- Announcement: https://github.com/dashpay/dash/releases/tag/v0.12.1.0
-
