# Dash (Digital Cash) Cryptocurrency full node and wallet
# Dash Core reference implementation
# vim:tw=0:ts=2:sw=2:et:
#
# This is the rpm source spec for building a Dash Core Reference Desktop
# Wallet, Masternode, and Full Node. Dash Core Masternode Sentinel is built
# with another spec file.
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
# Enjoy. -t0dd

# Package (RPM) name-version-release.
# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]

%define _name_d dash
%define _name_dc dashcore
Name: %{_name_dc}
Summary: Peer-to-peer, privacy-centric, digital currency

%define targetIsProduction 0
%define includeMinorbump 1

# ie. if the dev team includes things like rc3 in the filename
%define archiveQualifier rc5
%define includeArchiveQualifier 0

# VERSION
%define vermajor 0.12.3
%define verminor 2
Version: %{vermajor}.%{verminor}

# dashcore source tarball file basename
# the archive name and directory tree can have some variances
# (dashcore, dash, somename-vvvv-rc2, etc)
# - github convention - v0.12.3.0 or dash-0.12.3.0 - e.g. dash-0.12.3.0.tar.gz
%define _archivename_github1 v%{version}
%define _archivename_github2 %{_name_d}-%{version}
%define _archivename_alt1 %{_name_dc}-%{vermajor}
%if %{includeArchiveQualifier}
  %define _archivename_github1 v%{version}-%{archiveQualifier}
  %define _archivename_github2 %{_name_d}-%{version}-%{archiveQualifier}
  %define _archivename_alt1 %{_name_dc}-%{vermajor}-%{archiveQualifier}
%endif
%define archivename %{_archivename_github2}
%define srccodetree %{_archivename_github2}

# RELEASE
# if production - "targetIsProduction 1"
%define pkgrel_prod 1

# if pre-production - "targetIsProduction 0"
# eg. 0.3.testing.201804 -- pkgrel_preprod should always equal pkgrel_prod-1
%define pkgrel_preprod 0
%define extraver_preprod 1

%define _snapinfo testing
%define snapinfo %{_snapinfo}
%if %{includeArchiveQualifier}
  %define snapinfo %{archiveQualifier}
%endif

# if includeMinorbump
%define minorbump taw0

#
# Build the release string (don't edit this)
#

# release numbers
%undefine _relbuilder_pt1
%if %{targetIsProduction}
  %define _pkgrel %{pkgrel_prod}
  %define _relbuilder_pt1 %{pkgrel_prod}
%else
  %define _pkgrel %{pkgrel_preprod}
  %define _extraver %{extraver_preprod}
  %define _relbuilder_pt1 %{_pkgrel}.%{_extraver}
%endif

# snapinfo and repackage (pre-built) indicator
%undefine _relbuilder_pt2
%if %{targetIsProduction}
  %undefine snapinfo
%endif
%if 0%{?sourceIsPrebuilt:1}
  %if ! %{sourceIsPrebuilt}
    %undefine snapinfo_rp
  %endif
%else
  %undefine snapinfo_rp
%endif
%if 0%{?snapinfo_rp:1}
  %if 0%{?snapinfo:1}
    %define _relbuilder_pt2 %{snapinfo}.%{snapinfo_rp}
  %else
    %define _relbuilder_pt2 %{snapinfo_rp}
  %endif
%else
  %if 0%{?snapinfo:1}
    %define _relbuilder_pt2 %{snapinfo}
  %endif
%endif

# put it all together
# pt1 will always be defined. pt2 and minorbump may not be
%define _release %{_relbuilder_pt1}
%if ! %{includeMinorbump}
  %undefine minorbump
%endif
%if 0%{?_relbuilder_pt2:1}
  %if 0%{?minorbump:1}
    %define _release %{_relbuilder_pt1}.%{_relbuilder_pt2}%{?dist}.%{minorbump}
  %else
    %define _release %{_relbuilder_pt1}.%{_relbuilder_pt2}%{?dist}
  %endif
%else
  %if 0%{?minorbump:1}
    %define _release %{_relbuilder_pt1}%{?dist}.%{minorbump}
  %else
    %define _release %{_relbuilder_pt1}%{?dist}
  %endif
%endif

Release: %{_release}
# ----------- end of release building section

# Extracted source tree structure (extracted in .../BUILD)
#   srcroot               dashcore-0.12.3
#      \_srccodetree        \_dash-0.12.3.0 or dashcore-0.12.3 or dash-0.12.3.0-rc2...
#      \_srccontribtree     \_dashcore-0.12.3-contrib
%define srcroot %{name}-%{vermajor}
%define srccontribtree %{name}-%{vermajor}-contrib
# srccodetree defined earlier

# Note, that ...
# https://github.com/dashpay/dash/archive/v0.12.3.0-rc2.tar.gz
# ...is the same as...
# https://github.com/dashpay/dash/archive/v0.12.3.0-rc2/dash-0.12.3.0-rc2.tar.gz
%if %{includeArchiveQualifier}
Source0: https://github.com/dashpay/dash/archive/v%{version}-%{archiveQualifier}/%{archivename}.tar.gz
%else
Source0: https://github.com/dashpay/dash/archive/v%{version}/%{archivename}.tar.gz
%endif

%if %{targetIsProduction}
#Source0: https://github.com/taw00/dashcore-rpm/blob/master/source/SOURCES/%%{archivename}.tar.gz
Source1: https://github.com/taw00/dashcore-rpm/blob/master/source/SOURCES/%{srccontribtree}.tar.gz
%else
#Source0: https://github.com/taw00/dashcore-rpm/blob/master/source/testing/SOURCES/%%{archivename}.tar.gz
Source1: https://github.com/taw00/dashcore-rpm/blob/master/source/testing/SOURCES/%{srccontribtree}.tar.gz
%endif

%global selinux_variants mls strict targeted
%define testing_extras 0

# If you comment out "debug_package" RPM will create additional RPMs that can
# be used for debugging purposes. I am not an expert at this, BUT ".build_ids"
# are associated to debug packages, and I have lately run into packaging
# conflicts because of them. This is a topic I can't share a whole lot of
# wisdom about, but for now... I turn all that off.
#
# How debug info and build_ids managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
#%%define debug_package %%{nil}
%define _unique_build_ids 1
%define _build_id_links alldebug

# https://fedoraproject.org/wiki/Changes/Harden_All_Packages
%define _hardened_build 1

License: MIT
URL: http://dash.org/
# Note, for example, this will not build on ppc64le
ExclusiveArch: x86_64 i686 i386

BuildRequires: gcc-c++ autoconf automake libtool
BuildRequires: openssl-devel boost-devel libevent-devel
BuildRequires: libdb4-cxx-devel
BuildRequires: miniupnpc-devel
# Other BuildRequires listed per package below

#BuildRequires: checkpolicy selinux-policy-devel selinux-policy-doc

#t0dd: I will often add tree, vim-enhanced, and less for mock environment
# introspection
#BuildRequires: tree vim-enhanced less

#t0dd: I don't think this check is needed anymore -comment out for now.
## ZeroMQ not testable yet on RHEL due to lack of python3-zmq so
## enable only for Fedora
#%%if 0%%{?fedora}
#BuildRequires: python3-zmq zeromq-devel
#%%endif

#t0dd: Python tests still use OpenSSL for secp256k1, so we still need this to
# run the testsuite on RHEL7, until Red Hat fixes OpenSSL on RHEL7. It has
# already been fixed on Fedora. Bitcoin itself no longer needs OpenSSL for
# secp256k1.
# To support this, we are tracking https://linux.ringingliberty.com/bitcoin/el7/SRPMS/
# ...aka: https://linux.ringingliberty.com/bitcoin/el$releasever/$basearch
# We bring it in-house, rebuild, and supply at https://copr.fedorainfracloud.org/coprs/taw/dashcore-openssl-compat/
# ...aka: https://copr-be.cloud.fedoraproject.org/results/taw/dashcore-openssl-compat/epel-$releasever-$basearch/
%if %{testing_extras} && 0%{?rhel}
BuildRequires: openssl-compat-dashcore-libs
%endif


# dashcore-client
%package client
Summary: Peer-to-peer; privacy-centric; digital currency, protocol, and platform for payments and dApps (dash-qt desktop reference client)
Requires: dashcore-utils = %{version}-%{release}
#BuildRequires: qt5-qtbase-devel qt5-linguist qt5-qttools-devel
BuildRequires: qrencode-devel protobuf-devel
BuildRequires: qt5-qtbase-devel qt5-linguist
BuildRequires: libappstream-glib desktop-file-utils


# dashcore-server
%package server
Summary: Peer-to-peer; privacy-centric; digital currency, protocol, and platform for payments and dApps (dashd reference server)
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
Requires(pre): shadow-utils
Requires(post): /usr/sbin/semodule, /sbin/restorecon, /sbin/fixfiles
Requires(postun): /usr/sbin/semodule, /sbin/restorecon, /sbin/fixfiles
Requires: openssl-libs
Requires: dashcore-utils = %{version}-%{release}
Requires: dashcore-sentinel
#t0dd Requires: selinux-policy
#t0dd Requires: policycoreutils-python


# dashcore-libs
%package libs
Summary: Peer-to-peer; privacy-centric; digital currency, protocol, and platform for payments and dApps (consensus libraries)


# dashcore-devel
%package devel
Summary: Peer-to-peer; privacy-centric; digital currency, protocol, and platform for payments and dApps (dev libraries and headers)
Requires: dashcore-libs = %{version}-%{release}


# dashcore-utils
%package utils
Summary: Peer-to-peer; privacy-centric; digital currency, protocol, and platform for payments and dApps (commandline utils)


# dashcore src.rpm
%description
Dash Core reference implementation. This is the source package for building
most of the Dash Core set of binary packages.  It will build
dashcore-{client,server,utils,libs,devel,debuginfo}.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a
strong focus on serving the payments industry. Dash offers a form of money
that is portable, inexpensive, divisible and fast. It can be spent securely
both online and in person with minimal transaction fees. Dash offers instant
transactions (InstantSend), private transactions (PrivateSend), and operates
a self-governing and self-funding model. This decentralized governance and
budgeting system makes it one of the first ever successful decentralized
autonomous organizations (DAO). Dash is also a platform for innovative
decentralized crypto-tech.

Learn more at www.dash.org.


# dashcore-client
%description client
Dash Core reference implementation. This package provides dash-qt, a
user-friendly-er graphical wallet manager for personal use. This package
requires the dashcore-utils RPM package to be installed as well.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a
strong focus on serving the payments industry. Dash offers a form of money
that is portable, inexpensive, divisible and fast. It can be spent securely
both online and in person with minimal transaction fees. Dash offers instant
transactions (InstantSend), private transactions (PrivateSend), and operates
a self-governing and self-funding model. This decentralized governance and
budgeting system makes it one of the first ever successful decentralized
autonomous organizations (DAO). Dash is also a platform for innovative
decentralized crypto-tech.

Learn more at www.dash.org.


# dashcore-server
%description server
Dash Core reference implementation. This package provides dashd, a
peer-to-peer node and wallet server. It is the command line installation
without a graphical user interface. It can be used as a commandline wallet
but is typically used to run a Dash Full Node or Masternode. This package
requires the dashcore-utils and dashcore-sentinel RPM packages to be
installed.

Please refer to Dash Core documentation at dash.org for more information
about running a Masternode.

-

A Dash Full Node is a un-collatoralized member of a decentralized network of
servers that validate transactions and blocks. A Dash Masternode is a member
of a network of incentivized servers that perform expanded critical services
for the Dash cryptocurrency protocol.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a
strong focus on serving the payments industry. Dash offers a form of money
that is portable, inexpensive, divisible and fast. It can be spent securely
both online and in person with minimal transaction fees. Dash offers instant
transactions (InstantSend), private transactions (PrivateSend), and operates
a self-governing and self-funding model. This decentralized governance and
budgeting system makes it one of the first ever successful decentralized
autonomous organizations (DAO). Dash is also a platform for innovative
decentralized crypto-tech.

Learn more at www.dash.org.



# dashcore-libs
%description libs
This package provides libdashconsensus, which is used by third party
applications to verify scripts (and other functionality in the future).

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a
strong focus on serving the payments industry. Dash offers a form of money
that is portable, inexpensive, divisible and fast. It can be spent securely
both online and in person with minimal transaction fees. Dash offers instant
transactions (InstantSend), private transactions (PrivateSend), and operates
a self-governing and self-funding model. This decentralized governance and
budgeting system makes it one of the first ever successful decentralized
autonomous organizations (DAO). Dash is also a platform for innovative
decentralized crypto-tech.

Learn more at www.dash.org.


# dashcore-devel
%description devel
This package provides the libraries and header files necessary to compile
programs which use libdashconsensus.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a
strong focus on serving the payments industry. Dash offers a form of money
that is portable, inexpensive, divisible and fast. It can be spent securely
both online and in person with minimal transaction fees. Dash offers instant
transactions (InstantSend), private transactions (PrivateSend), and operates
a self-governing and self-funding model. This decentralized governance and
budgeting system makes it one of the first ever successful decentralized
autonomous organizations (DAO). Dash is also a platform for innovative
decentralized crypto-tech.

Learn more at www.dash.org.


# dashcore-utils
%description utils
Dash is Digital Cash

This package provides dash-cli, a utility to communicate with and control a
Dash server via its RPC protocol, and dash-tx, a utility to create custom
Dash transactions.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a
strong focus on serving the payments industry. Dash offers a form of money
that is portable, inexpensive, divisible and fast. It can be spent securely
both online and in person with minimal transaction fees. Dash offers instant
transactions (InstantSend), private transactions (PrivateSend), and operates
a self-governing and self-funding model. This decentralized governance and
budgeting system makes it one of the first ever successful decentralized
autonomous organizations (DAO). Dash is also a platform for innovative
decentralized crypto-tech.

Learn more at www.dash.org.



%prep
# Prep section starts us in directory .../BUILD (aka {_builddir})
# process dashcore - Source0 - untars in:
# {_builddir}/dashcore-0.12.3/dashcore-0.12.3.0/
mkdir -p %{srcroot}
%setup -q -T -D -a 0 -n %{srcroot}
# contributions
# {_builddir}/dashcore-0.12.3/dashcore-0.12.3-contrib/
%setup -q -T -D -a 1 -n %{srcroot}

#t0dd: Prep SELinux policy -- NOT USED YET
# Done here to prep for action taken in the %%build step
# At this moment, we are in the srcroot directory
mkdir -p selinux-tmp
cp -p %{srccontribtree}/linux/selinux/dash.{te,if,fc} selinux-tmp/

cp -a %{srccontribtree}/extras/pixmaps/*.??? %{srccodetree}/share/pixmaps/



%build
# This section starts us in directory {_builddir}/{srcroot}
cd %{srccodetree}
./autogen.sh
%configure --enable-reduce-exports --enable-glibc-back-compat
make %{?_smp_mflags}
cd ..

# Man Pages (from contrib)
gzip %{srccontribtree}/linux/man/man1/*
gzip %{srccontribtree}/linux/man/man5/*


#t0dd Not using for now. Doubling up %%'s to stop macro expansion in comments.
#t0dd # Build SELinux policy
#t0dd pushd selinux-tmp
#t0dd for selinuxvariant in %%{selinux_variants}
#t0dd do
#t0dd   # FIXME: Create and debug SELinux policy
#t0dd   make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
#t0dd   mv dash.pp dash.pp.${selinuxvariant}
#t0dd   make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
#t0dd done
#t0dd popd



%check
# This section starts us in directory {_builddir}/{srcroot}
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
  #t0dd LD_LIBRARY_PATH=/opt/openssl-compat-dashcore/lib PYTHONUNBUFFERED=1 qa/pull-tester/rpc-tests.py -extended
%endif



%install
# This section starts us in directory {_builddir}/{srcroot}

cd %{srccodetree}
make INSTALL="install -p" CP="cp -p" DESTDIR=%{buildroot} install
cd ..

# Remove the test binaries if still floating around
%if ! %{testing_extras}
  rm -f %{buildroot}%{_bindir}/test_*
  rm -f %{buildroot}%{_bindir}/bench_dash
%endif

# Cheatsheet for built-in RPM macros:
# https://fedoraproject.org/wiki/Packaging:RPMMacros
#   _builddir = {_topdir}/BUILD
#   _buildrootdir = {_topdir}/BUILDROOT
#   buildroot = {_buildrootdir}/{name}-{version}-{release}.{_arch}
#   _bindir = /usr/bin
#   _sbindir = /usr/sbin
#   _datadir = /usr/share
#   _mandir = /usr/share/man
#   _sysconfdir = /etc
#   _localstatedir = /var
#   _sharedstatedir is /var/lib
#   _prefix or _usr = /usr
#   _libdir = /usr/lib or /usr/lib64 (depending on system)
# This is used to quiet rpmlint who can't seem to understand that /usr/lib is
# still used for certain things.
%define _usr_lib /usr/lib
# These three are defined in newer versions of RPM (Fedora not el7)
%define _tmpfilesdir %{_usr_lib}/tmpfiles.d
%define _unitdir %{_usr_lib}/systemd/system
%define _metainfodir %{_datadir}/metainfo

# Create directories
install -d %{buildroot}%{_datadir}
install -d %{buildroot}%{_datadir}/pixmaps
install -d %{buildroot}%{_mandir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_localstatedir}
install -d %{buildroot}%{_sharedstatedir}
install -d %{buildroot}%{_tmpfilesdir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_metainfodir}
install -d -m755 -p %{buildroot}%{_bindir}
install -d -m755 -p %{buildroot}%{_sbindir}

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

# Binaries - stick dashd into sbin instead of bin
install -D -m755 -p %{buildroot}%{_bindir}/dashd %{buildroot}%{_sbindir}/dashd
rm -f %{buildroot}%{_bindir}/dashd

# Symlinks
# debug.log: /var/lib/dashcore/debug.log -> /var/log/dashcore/debug.log
ln -s %{_localstatedir}/log/dashcore/debug.log %{buildroot}%{_sharedstatedir}/dashcore/debug.log
# debug.log:
# /var/lib/dashcore/testnet3/debug.log
#   -> /var/log/dashcore/testnet3/debug.log
ln -s %{_localstatedir}/log/dashcore/testnet3/debug.log %{buildroot}%{_sharedstatedir}/dashcore/testnet3/debug.log
# config:
# /var/lib/dashcore/.dashcore/dash.conf
#   -> /etc/dashcore/dash.conf (convenience symlink)
ln -s %{_sysconfdir}/dashcore/dash.conf %{buildroot}%{_sharedstatedir}/dashcore/.dashcore/dash.conf

# Man Pages (from contrib)
install -D -m644 %{srccontribtree}/linux/man/man1/* %{buildroot}%{_mandir}/man1/
install -D -m644 %{srccontribtree}/linux/man/man5/* %{buildroot}%{_mandir}/man5/

# Desktop elements - desktop file and kde protocol file (from contrib)
cd %{srccontribtree}/linux/desktop/
install -D -m644 dash-qt.desktop %{buildroot}%{_datadir}/applications/dash-qt.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/dash-qt.desktop
# dash-qt.appdata.xml
# https://fedoraproject.org/wiki/Packaging:AppData
install -D -m644 -p dash-qt.appdata.xml %{buildroot}%{_metainfodir}/dash-qt.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

# I think this is not used anymore --t0dd: Need to investigate
install -D -m644 usr-share-kde4-services_dash-qt.protocol %{buildroot}%{_datadir}/kde4/services/dash-qt.protocol

# Desktop elements - hicolor icons
install -D -m644 dash-hicolor-128.png      %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/dash.png
install -D -m644 dash-hicolor-16.png       %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/dash.png
install -D -m644 dash-hicolor-22.png       %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/dash.png
install -D -m644 dash-hicolor-24.png       %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/dash.png
install -D -m644 dash-hicolor-256.png      %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/dash.png
install -D -m644 dash-hicolor-32.png       %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/dash.png
install -D -m644 dash-hicolor-48.png       %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/dash.png
install -D -m644 dash-hicolor-scalable.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/dash.svg
# Desktop elements - HighContrast icons
install -D -m644 dash-HighContrast-128.png      %{buildroot}%{_datadir}/icons/HighContrast/128x128/apps/dash.png
install -D -m644 dash-HighContrast-16.png       %{buildroot}%{_datadir}/icons/HighContrast/16x16/apps/dash.png
install -D -m644 dash-HighContrast-22.png       %{buildroot}%{_datadir}/icons/HighContrast/22x22/apps/dash.png
install -D -m644 dash-HighContrast-24.png       %{buildroot}%{_datadir}/icons/HighContrast/24x24/apps/dash.png
install -D -m644 dash-HighContrast-256.png      %{buildroot}%{_datadir}/icons/HighContrast/256x256/apps/dash.png
install -D -m644 dash-HighContrast-32.png       %{buildroot}%{_datadir}/icons/HighContrast/32x32/apps/dash.png
install -D -m644 dash-HighContrast-48.png       %{buildroot}%{_datadir}/icons/HighContrast/48x48/apps/dash.png
install -D -m644 dash-HighContrast-scalable.svg %{buildroot}%{_datadir}/icons/HighContrast/scalable/apps/dash.svg
cd ../../..

# Misc pixmaps - unsure if they are even used... (from contrib)
#install -D -m644 %%{srccontribtree}/extras/pixmaps/*.??? %%{buildroot}%%{_datadir}/pixmaps/

# Config
# Install default configuration file (from contrib)
%if %{targetIsProduction}
%define testnet 0
%else
%define testnet 1
%endif
install -D -m640 %{srccontribtree}/linux/systemd/etc-dashcore_dash.conf %{buildroot}%{_sysconfdir}/dashcore/dash.conf
echo "\
# ---------------------------------------------------------------------------
# Example of a minimalistic configuration. Change the password. Additionally,
# some of these settings are more explicit than they need to be.

# Note, the RPM spec file sets dashcore user's homedir to be /var/lib/dashcore
# The datadir is also set to the same.
datadir=/var/lib/dashcore

testnet=%{testnet}
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
" >> %{buildroot}%{_sysconfdir}/dashcore/dash.conf
install -D -m644 %{buildroot}%{_sysconfdir}/dashcore/dash.conf %{srccontribtree}/extras/dash.conf.example

# Add the rpcuser name and rpcpassword, but really need to be different for the
# working dash.conf and the example, just in case the user decides to not
# change anything.
echo "\

# Example RPC username and password.
rpcuser=rpcuser-CHANGEME-`head -c 32 /dev/urandom | base64 | head -c 4`
rpcpassword=CHANGEME`head -c 32 /dev/urandom | base64`
" >> %{buildroot}%{_sysconfdir}/dashcore/dash.conf

echo "\

# Example RPC username and password.
rpcuser=rpcuser-CHANGEME-`head -c 32 /dev/urandom | base64 | head -c 4`
rpcpassword=CHANGEME`head -c 32 /dev/urandom | base64`
" >> %{srccontribtree}/extras/dash.conf.example

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

# System services
install -D -m600 -p %{srccontribtree}/linux/systemd/etc-sysconfig_dashd %{buildroot}%{_sysconfdir}/sysconfig/dashd
install -D -m755 -p %{srccontribtree}/linux/systemd/etc-sysconfig-dashd-scripts_dashd.send-email.sh %{buildroot}%{_sysconfdir}/sysconfig/dashd-scripts/dashd.send-email.sh
install -D -m644 -p %{srccontribtree}/linux/systemd/usr-lib-systemd-system_dashd.service %{buildroot}%{_unitdir}/dashd.service
install -D -m644 -p %{srccontribtree}/linux/systemd/usr-lib-tmpfiles.d_dashd.conf %{buildroot}%{_tmpfilesdir}/dashd.conf

# Log files
# ...logrotate file rules
install -D -m644 -p %{srccontribtree}/linux/logrotate/etc-logrotate.d_dashcore %{buildroot}/etc/logrotate.d/dashcore
# ...ghosted log files - need to exist in the installed buildroot
touch %{buildroot}%{_localstatedir}/log/dashcore/debug.log
touch %{buildroot}%{_localstatedir}/log/dashcore/testnet3/debug.log

# Service definition files for firewalld for full and master nodes
install -D -m644 -p %{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore.xml %{buildroot}%{_usr_lib}/firewalld/services/dashcore.xml
install -D -m644 -p %{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore-testnet.xml %{buildroot}%{_usr_lib}/firewalld/services/dashcore-testnet.xml
install -D -m644 -p %{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore-rpc.xml %{buildroot}%{_usr_lib}/firewalld/services/dashcore-rpc.xml
install -D -m644 -p %{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore-testnet-rpc.xml %{buildroot}%{_usr_lib}/firewalld/services/dashcore-testnet-rpc.xml

# Not using for now. Doubling up %%'s to stop macro expansion in comments.
#t0dd # Install SELinux policy
#t0dd for selinuxvariant in %%{selinux_variants}
#t0dd do
#t0dd   install -d %%{buildroot}%%{_datadir}/selinux/${selinuxvariant}
#t0dd   install -p -m 644 SELinux/dash.pp.${selinuxvariant} \
#t0dd     %%{buildroot}%%{_datadir}/selinux/${selinuxvariant}/dash.pp
#t0dd done



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
#  _localstatedir is /var
#  _sharedstatedir is /var/lib
#  /var/lib/dashcore is the $HOME for the dashcore user

# Fix the debug.log directory structure if it is not aligned to /var/log/
# standards.
# If /var/lib/dashcore/debug.log is not a symlink, we need to fix that.
#    /var/lib/dashcore/debug.log -> /var/log/dashcore/debug.log
#    /var/lib/dashcore/testnet3/debug.log -> /var/log/dashcore/testnet3/debug.log
%define vlibdc %{_sharedstatedir}/dashcore
%define vlibdc_dl %{vlibdc}/debug.log
%define vlibdc_tdl %{vlibdc}/testnet3/debug.log
%define vlogdc %{_localstatedir}/log/dashcore
%define vlogdc_dl %{vlogdc}/debug.log
%define vlogdc_tdl %{vlogdc}/testnet3/debug.log
# If either debug.log in /var/lib/dashcore is not a symlink, we need to move
# files and then fix the symlinks Hopefully this doesn't break because
# dashcore may have debug.log open
if [ -e %{vlibdc_dl} -a -f %{vlibdc_dl} -a ! -h %{vlibdc_dl} ]
then
   mv %{vlibdc_dl}* %{vlogdc}/
   ln -s %{vlogdc_dl} %{vlibdc_dl}
   chown dashcore:dashcore %{vlibdc_dl}
   chown -R dashcore:dashcore %{vlogdc}
   chmod 644 %{vlogdc_dl}*
fi
if [ -e %{vlibdc_tdl} -a -f %{vlibdc_tdl} -a ! -h %{vlibdc_tdl} ]
then
   mv %{vlibdc_tdl}* %{vlogdc}/testnet3/
   ln -s %{vlogdc_tdl} %{vlibdc_tdl}
   chown dashcore:dashcore %{vlibdc_tdl}
   chown -R dashcore:dashcore %{vlogdc}
   chmod 644 %{vlogdc_tdl}*
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
#t0dd   /usr/sbin/semodule -s ${selinuxvariant} -i \
#t0dd     %%{_datadir}/selinux/${selinuxvariant}/dash.pp \
#t0dd       &> /dev/null || :
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
#t0dd   # FIXME This is less than ideal, but until dwalsh gives me a better way...
#t0dd   /usr/sbin/semanage port -d -p tcp 9999
#t0dd   /usr/sbin/semanage port -d -p tcp 9998
#t0dd   /usr/sbin/semanage port -d -p tcp 19999
#t0dd   /usr/sbin/semanage port -d -p tcp 19998
#t0dd   for selinuxvariant in %%{selinux_variants}
#t0dd   do
#t0dd     /usr/sbin/semodule -s ${selinuxvariant} -r dash \
#t0dd       &> /dev/null || :
#t0dd   done
#t0dd   /sbin/fixfiles -R dashcore-server restore &> /dev/null || :
#t0dd     [ -d %%{_sharedstatedir}/dashcore ] && \
#t0dd     /sbin/restorecon -R %%{_sharedstatedir}/dashcore \
#t0dd     &> /dev/null || :
#t0dd fi



# dashcore-client
%files client
%defattr(-,root,root,-)
%license %{srccodetree}/COPYING
%doc %{srccodetree}/doc/*.md %{srccontribtree}/extras/dash.conf.example
%{_bindir}/dash-qt
%{_datadir}/applications/dash-qt.desktop
%{_metainfodir}/dash-qt.appdata.xml
%{_datadir}/kde4/services/dash-qt.protocol
#%%{_datadir}/pixmaps/*
%{_datadir}/icons/*
%{_mandir}/man1/dash-qt.1.gz
%{_mandir}/man5/masternode.conf.5.gz
%{_usr_lib}/firewalld/services/dashcore.xml
%{_usr_lib}/firewalld/services/dashcore-testnet.xml
%{_usr_lib}/firewalld/services/dashcore-rpc.xml
%{_usr_lib}/firewalld/services/dashcore-testnet-rpc.xml
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
%defattr(-,dashcore,dashcore,-)
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
%defattr(-,root,root,-)

%doc %{srccodetree}/doc/*.md %{srccontribtree}/extras/dash.conf.example
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/sysconfig/dashd
%attr(755,root,root) %{_sysconfdir}/sysconfig/dashd-scripts/dashd.send-email.sh

# The logs
%attr(644,root,root) /etc/logrotate.d/dashcore
# ...log files - they don't initially exist, but we still own them
%ghost %{_localstatedir}/log/dashcore/debug.log
%ghost %{_localstatedir}/log/dashcore/testnet3/debug.log
# ...the symlinks for log files...
%defattr(-,dashcore,dashcore,-)
#%%attr(777,dashcore,dashcore) %%{_sharedstatedir}/dashcore/debug.log
#%%attr(777,dashcore,dashcore) %%{_sharedstatedir}/dashcore/testnet3/debug.log
%{_sharedstatedir}/dashcore/debug.log
%{_sharedstatedir}/dashcore/testnet3/debug.log
%defattr(-,root,root,-)

# dash.conf
%config(noreplace) %attr(640,dashcore,dashcore) %{_sysconfdir}/dashcore/dash.conf
# ...convenience symlink:
#    /var/lib/dashcore/.dashcore/dash.conf -> /etc/dashcore/dash.conf
# ...this is probably really bad form.
%defattr(-,dashcore,dashcore,-)
#%%attr(777,dashcore,dashcore) %%{_sharedstatedir}/dashcore/.dashcore/dash.conf
%{_sharedstatedir}/dashcore/.dashcore/dash.conf
%defattr(-,root,root,-)
%attr(640,dashcore,dashcore) %{_sharedstatedir}/dashcore/.dashcore/README

%{_unitdir}/dashd.service
%{_usr_lib}/firewalld/services/dashcore.xml
%{_usr_lib}/firewalld/services/dashcore-testnet.xml
%{_usr_lib}/firewalld/services/dashcore-rpc.xml
%{_usr_lib}/firewalld/services/dashcore-testnet-rpc.xml
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
%{_mandir}/man1/dash-cli.1.gz
%{_mandir}/man1/dash-tx.1.gz


# Dash Core Information
#
# Dash...
#   * Project website: https://www.dash.org/
#   * Project documentation: https://docs.dash.org/
#   * Developer documentation: https://dash-docs.github.io/
#
# Dash Core on Fedora/CentOS/RHEL...
#   * Git Repo: https://github.com/taw00/dashcore-rpm
#   * Documentation: https://github.com/taw00/dashcore-rpm/tree/master/documentation
#
# The last major testnet effort...
#   * Announcement: https://www.dash.org/forum/threads/12-1-testnet-testing-phase-two-ignition.10818/
#   * Documentation: https://dashpay.atlassian.net/wiki/display/DOC/Testnet
#
# Source snapshots...
#     https://github.com/dashpay/dash/tags
#     https://github.com/dashpay/dash/releases
#     test example: dash-0.12.3.0-rc5.tar.gz
#     release example: dash-0.12.3.0.tar.gz
#
# Dash Core git repos...
#   * Dash: https://github.com/dashpay/dash
#   * Sentinel: https://github.com/dashpay/sentinel

%changelog
* Wed Jul 11 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.2-0.1.testing.taw
  - v12.3.2 - https://github.com/dashpay/dash/releases/tag/v0.12.3.2

* Tue Jul 03 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.1-1.taw
* Tue Jul 03 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.1-0.1.testing.taw
  - v12.3.1 - https://github.com/dashpay/dash/releases/tag/v0.12.3.1

* Thu Jun 21 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.10.testing.taw
  - v12.3.0 - https://github.com/dashpay/dash/releases/tag/v0.12.3.0

* Thu Jun 21 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.9.rc5.taw
  - v12.3-rc5 - https://github.com/dashpay/dash/releases/tag/v0.12.3.0-rc5

* Wed Jun 13 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.8.rc4.taw
  - v12.3-rc4 - https://github.com/dashpay/dash/releases/tag/v0.12.3.0-rc4

* Sun Jun 10 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.7.rc3.taw
  - v12.3-rc3 - https://github.com/dashpay/dash/releases/tag/v0.12.3.0-rc3

* Sun Jun 3 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.6.rc2.taw
  - v12.3-rc2 - https://github.com/dashpay/dash/releases/tag/v0.12.3.0-rc2
  - /etc/dashcore/dash.conf now has testnet=1 on by default if installing the  
    test RPMs. Note that dash.conf will be in an .rpmnew file though.

* Wed May 23 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.5.testing.20180510.taw
  - spec file: some cleanup, URL for sources
  - updated all contrib icons to new branding from dash.org/graphics
    - should really consider nuking the pixmaps directory. Modern linuxes don't use them.
  - updated man pages a smidge
  - locking down supported architectures w/ ExclusiveArch

* Thu May 10 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.4.testing.20180510.taw
  - spec file: mkdir -p not just mkdir
  - Another 12.3 test build (from github.com origin/develop)

* Sat Apr 28 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.3.testing.20180428.taw
  - Another 12.3 test build (from github.com origin/develop)

* Wed Apr 25 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.2.testing.taw
  - Major cleanup

* Sun Apr 8 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.1.testing.taw
  - 12.3 test build
  - name-version-release more closely matches industry guidelines:  
    https://fedoraproject.org/wiki/Packaging:Versioning
  - https://bamboo.dash.org/browse/DASHL-DEV-341

* Fri Apr 06 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.2.3-2.taw
  - Improved rpm text descriptions and some updated comments.

* Fri Apr 06 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.2.3-1.taw
  - spec file cleanup. dash.conf cleanup and improvements.
  - Create convenience symlink to /etc/dashcore/dash.conf so you don't have  
    to put -conf= on the commandline all the time.

* Tue Dec 19 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.2.2-0.taw
  - Release - 8506678

* Tue Dec 19 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.2.2-1.testing.taw
  - Release Candidate - 8506678

* Sat Dec 09 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.2.2-0.testing.taw
  - Release Candidate - f9f28e7

* Sun Nov 12 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.2.1-0.testing.taw
  - Release Candidate - 20bacfa

* Wed Nov 8 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.2.0-1.testing.taw
  - Release Candidate - ec8178c

* Fri Oct 20 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.2.0-0.testing.taw
  - Initial 12.2 test build

* Tue Apr 11 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.1.5-0.rc.taw
  - Fixes a watchdog propagation issue.

* Wed Mar 22 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.1.4-0.rc.taw
  - Added RPC port to available firewalld services.
  - Renamed firewalld services to match bitcoin's firewalld service name taxonomies.

* Fri Mar 10 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.1.3-2.rc.taw
  - Added RPC port to available firewalld services.

* Sat Mar 04 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.1.3-1.rc.taw
  - Brought back the test scripts (most of them), made them conditional. Added  
    back and adjusted build-requires for openssl-compat that uses our own  
    openssl-compat builds. Test scripts / openssl-compat seem to only work for  
    very old linux--CentOS7/RHEL7 Ie. I have more work to do to make them part of  
    the build.
  - "bumptag" now can be defined or undefined and we do the right thing.

* Thu Mar 02 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.1.3-0.rc.taw
  - Release 0.12.1.3 - 119fe83
  - Announcement: https://github.com/dashpay/dash/releases/tag/v0.12.1.3

* Fri Feb 24 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.1.2-0.rc.taw
  - Release 0.12.1.2 Release Candidate - a1ef547
  - Announcement: https://github.com/dashpay/dash/releases/tag/v0.12.1.2
  - Specfile change: Structure of build tree expansion changed allowing  
    flexibility in how the source is generated upstream (bamboo vs. github)
  - Specfile change: Added a bunch of documentation from the main tree.
  - dashd.init updated
  - dashd.send-email.sh with much clearer messaging.

* Mon Feb 20 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.1.1-1.taw
  - Still massaging systemd service and configuration settings.
  - Boosting startup timeout window significantly to avoid shooting ourselves  
    in the foot too quickly. Also PIDFile= is not necessary.
  - Reduced default maxconnections to 8 since we have so many masternodes.
  - Fixed a systemd-managed tmpfile perms issue.

* Sun Feb 19 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.1.1-0.taw
  - Release 0.12.1.1 - e9e5a24
  - Announcement: https://github.com/dashpay/dash/releases/tag/v0.12.1.1
  - Stability improvements. Governance object sync time improvements.
  - systemd service file and configuration tweaks.
  - lots of other bug fixes

* Fri Feb 17 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.1.0-2.taw
  - dashd.service can be configured to send email upon start, stop,  
    restart

* Fri Feb 10 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.1.0-1.taw
  - With Debuginfo Package built -- there have been segfaults. This should  
    help troubleshoot.

* Sun Feb 05 2017 Todd Warner <t0dd_at_protonmail.com> 0.12.1.0-0.taw
  - Release 12.1.0 - 56971f8
  - Announcement: https://github.com/dashpay/dash/releases/tag/v0.12.1.0
