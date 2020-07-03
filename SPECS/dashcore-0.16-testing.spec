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
# Enjoy. -t0dd

# Package (RPM) name-version-release.
# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]

%define _name_d dash
%define _name_dc dashcore
%define tld_vendor_product_id org.dash.Dashcore
Name: %{_name_dc}
Summary: A global payments network and decentralized application (dapp) platform: a peer-to-peer, fungible, digital currency, protocol, and platform.

%define targetIsProduction 0

# Leave these off.
# These settings are used if you wan to deliver packages where the application
# is developed from pre-built binaries instead of from source code. These are
# last resort settings if there are problems building the application
# appropriately. For example, we used to have a terrible time building to a
# EPEL/RHEL 7 target. That has since been fixed.
%define clientSourceIsBinary 0
%define serverSourceIsBinary 0

# Leave this on
# Building without leaning on the system libraries for the build of the build
# is currently not supported (I can't get it to do a full depends-based build
# yet). Please leave this on. It's poor packaging anyway to build from depends.
%define useSystemLibraries 1

# Use if the dev team includes things like rc3 in the filename
%undefine buildQualifier
%define buildQualifier rc2

# VERSION
%define vermajor 0.16
%define _verminor1 0
%define _verminor2 0
%define verminor %{_verminor1}.%{_verminor2}
Version: %{vermajor}.%{verminor}
%define versionqualified %{version}
%if 0%{?buildQualifier:1}
  %define versionqualified %{version}-%{buildQualifier}
%endif


# RELEASE
# package release (and for testing only, extrarel)
%define _pkgrel 1
%if ! %{targetIsProduction}
  %define _pkgrel 0.3
%endif

# MINORBUMP
%define minorbump taw
#%%undefine minorbump

#
# Build the release string - don't edit this
#

%define snapinfo testing
%if %{targetIsProduction}
  %undefine snapinfo
%endif
%if 0%{?buildQualifier:1}
  %define snapinfo %{buildQualifier}
%endif

%undefine _rp
%if %{clientSourceIsBinary} && %{serverSourceIsBinary}
  %define _rp rp
%else
  %if %{clientSourceIsBinary}
    %define _rp rpc
  %else
  %if %{serverSourceIsBinary}
    %define _rp rps
  %endif
  %endif
%endif

# have to use _variables because rpm spec macros are easily recursive and break.
%define _snapinfo THIS_VALUE_WILL_BE_REPLACED
%if 0%{?_rp:1}
  %if 0%{?snapinfo:1}
    %define _snapinfo %{snapinfo}.%{_rp}
  %else
    %define _snapinfo %{_rp}
  %endif
%else
  %if 0%{?snapinfo:1}
    %define _snapinfo %snapinfo
  %else
    %undefine _snapinfo
  %endif
%endif

# pkgrel will be defined, snapinfo and minorbump may not be
%define _release %{_pkgrel}
%if 0%{?_snapinfo:1}
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}.%{_snapinfo}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}.%{_snapinfo}%{?dist}
  %endif
%else
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}%{?dist}
  %endif
%endif

Release: %{_release}
# ----------- end of release building section

# (flags for experimentation)
# Don't manually edit these.
%define buildFromSource 0
%define testing_extras 0
%if ! %{clientSourceIsBinary} || ! %{serverSourceIsBinary}
  %define buildFromSource 1
  #%%define testing_extras 1 -- turn off for now
%endif

# (flag for experimentation)
# Don't disable the wallet build (leave it 0).
# Note, if you do disable it, an empty dashcore-client RPM will be built.
%define disable_wallet 0

# (flag for experimentation)
# Don't turn off the useExtraSources flag.
# The src.rpm includes pre-downloaded extra source archives that satisfy
# source expectations for the depends tree during the build. They are:
# bls-signatures (chia_bls) from https://github.com/codablock/bls-signatures
# libbacktrace (backtrace) from https://github.com/rust-lang-nursery/libbacktrace
# The next two are for EL8 builds only.
# miniupnpc from http://miniupnp.free.fr/files/miniupnpc-2.0.20170509.tar.gz
# bdb v4 from https://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz
%define useExtraSources 1

# the archive name and directory tree can have some variances
# v0.16.0.0
%define _archivename_alt1 v%{version}
# dash-0.16.0.0
%define _archivename_alt2 %{_name_d}-%{version}
# dashcore-0.16.0
%define _archivename_alt3 %{_name_dc}-%{vermajor}.%{_verminor1}
# dashcore-0.16.0.0
%define _archivename_alt4 %{_name_dc}-%{version}

# Extracted source tree structure (extracted in .../BUILD)
#   projectroot           dashcore-0.16.0
#      \_sourcetree         \_dash-0.16.0.0 or dash-0.16.0.0-rc1...
#      \_binarytree         \_dashcore-0.16.0
#      \_srccontribtree     \_dashcore-0.16.0-contrib
#      \_patch_files        \_dash-0.16.0-...patch
# Supplied but only "moved":
#   bls-signatures-20181101.tar.gz
#                           --> {sourcetree}/depends/sources/v20181101.tar.gz

# our selection for this build - edit this
%define _sourcearchivename %{_archivename_alt2}
%define _binaryarchivename %{_archivename_alt4}
%define _binarytree %{_archivename_alt3}

%if 0%{?buildQualifier:1}
  %define sourcearchivename %{_sourcearchivename}-%{buildQualifier}
  %define binaryarchivename %{_binaryarchivename}-%{buildQualifier}
  %define sourcetree %{_sourcearchivename}-%{buildQualifier}
  %define binarytree %{_binarytree}
%else
  %define sourcearchivename %{_sourcearchivename}
  %define binaryarchivename %{_binaryarchivename}
  %define sourcetree %{_sourcearchivename}
  %define binarytree %{_binarytree}
%endif
%define blsarchivedate 20181101
%define blsarchivename bls-signatures-%{blsarchivedate}
%define libbacktracearchiveversion rust-snapshot-2018-05-22
%define libbacktracearchivename libbacktrace-%{libbacktracearchiveversion}
%define miniupnpcversion 2.0.20170509
%define miniupnpcarchivename miniupnpc-%{miniupnpcversion}
%define bdbarchiveversion 4.8.30.NC
%define bdbarchivename db-%{bdbarchiveversion}

%define projectroot %{name}-%{vermajor}
%define srccontribtree %{name}-%{vermajor}-contrib


Source0: https://github.com/dashpay/dash/archive/v%{versionqualified}/%{sourcearchivename}.tar.gz
Source1: https://github.com/taw00/dashcore-rpm/blob/master/SOURCES/%{srccontribtree}.tar.gz
Source2: https://github.com/taw00/dashcore-rpm/blob/master/SOURCES/%{blsarchivename}.tar.gz
Source3: https://github.com/rust-lang-nursery/libbacktrace/archive/%{libbacktracearchiveversion}/%{libbacktracearchivename}.tar.gz
# Source4 and Source5 are for EL8 only
Source4: http://miniupnp.free.fr/files/%{miniupnpcarchivename}.tar.gz
Source5: https://download.oracle.com/berkeley-db/%{bdbarchivename}.tar.gz
%if %{clientSourceIsBinary} || %{serverSourceIsBinary}
Source6: https://github.com/dashpay/dash/archive/v%{versionqualified}/%{binaryarchivename}-x86_64-linux-gnu.tar.gz
%endif
%if %{buildFromSource}
# nuke "About QT" in the client source.
Patch0: https://github.com/taw00/dashcore-rpm/blob/master/SOURCES/%{_name_d}-%{vermajor}-remove-about-qt-menu-item.patch
%endif

%global selinux_variants mls strict targeted

# If you comment out "debug_package" RPM will create additional RPMs that can
# be used for debugging purposes. I am not an expert at this, BUT ".build_ids"
# are associated to debug packages, and I have lately run into packaging
# conflicts because of them. This is a topic I can't share a whole lot of
# wisdom about, but for now... I turn all that off.
#
# How debug info and build_ids managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
# ...flip-flop next two lines in order to disable (nil) or enable (1) debuginfo package build
%define debug_package 1
%define debug_package %{nil}
%define _unique_build_ids 1
%define _build_id_links alldebug

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_pie
%define _hardened_build 1

# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing
# https://spdx.org/licenses/
License: MIT
URL: http://dash.org/
# Note, for example, this will not build on ppc64le
# I'm ditching i386 and i686 platform choices. Sorry.
ExclusiveArch: x86_64

%if %{buildFromSource}
# As recommended by...
# https://github.com/dashpay/dash/blob/develop/doc/build-unix.md
BuildRequires: libtool make autoconf automake patch
BuildRequires: cmake libstdc++-static
BuildRequires: python3

%if %{useSystemLibraries}
# These avoid unneccessary fetching of libraries from the internet.
# Packaging is supposed to be performable with an airgapped system.
BuildRequires: gettext
BuildRequires: openssl-devel boost-devel libevent-devel
BuildRequires: ccache
# Added to satisfy chia_bls.
BuildRequires: gmp-devel
%if 0%{?fedora}
# Note, EL8 uses in-src.rpm dependencies since EL8 does not provide these pkgs.
BuildRequires: libdb4-cxx-devel miniupnpc-devel
%endif
%endif
%endif

# NOTE: other BuildRequires listed per package below

#t0dd: SELinux stuff that I just haven't addressed yet and probably never will...
#BuildRequires: checkpolicy selinux-policy-devel selinux-policy-doc

# tree, vim-enhanced, and less for mock build environment introspection
%if ! %{targetIsProduction}
BuildRequires: tree vim-enhanced less findutils
%endif


# dashcore-client
%package client
Summary: A global payments network and decentralized application (dapp) platform: a peer-to-peer, fungible, digital currency, protocol, and platform. (desktop reference client)
Requires: dashcore-utils = %{version}-%{release}
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
Requires: firewalld-filesystem
Requires(post): firewalld-filesystem
Requires(postun): firewalld-filesystem

%if 0%{?fedora} || 0%{?rhel} >= 8 || 0%{?centos_ver} >= 8
%if ! %{disable_wallet}
Requires: qt5-qtwayland
# Required for installing desktop applications on linux
BuildRequires: libappstream-glib desktop-file-utils
%endif

%if %{buildFromSource} && %{useSystemLibraries}
# These avoid unneccessary fetching of libraries from the internet.
# Packaging is supposed to be performable with an airgapped system.
BuildRequires: protobuf-devel
%if ! %{disable_wallet}
BuildRequires: qrencode-devel
BuildRequires: qt5-qtbase-devel qt5-linguist
BuildRequires: qt5-qtwayland-devel
%endif
# endif build from source and use system libraries
%endif
# endif fedora or el8
%endif

# dashcore-server
%package server
Summary: A global payments network and decentralized application (dapp) platform: a peer-to-peer, fungible, digital currency, protocol, and platform. (reference server)
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
Requires: firewalld-filesystem
Requires(post): firewalld-filesystem
Requires(postun): firewalld-filesystem
# As per https://docs.fedoraproject.org/en-US/packaging-guidelines/Systemd/
#Requires(post): systemd
#Requires(preun): systemd
#Requires(postun): systemd
BuildRequires: systemd
%{?systemd_requires}
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
Summary: A global payments network and decentralized application (dapp) platform: a peer-to-peer, fungible, digital currency, protocol, and platform. (consensus libraries)


# dashcore-devel
%package devel
Summary: A global payments network and decentralized application (dapp) platform: a peer-to-peer, fungible, digital currency, protocol, and platform. (dev libraries and headers)
Requires: dashcore-libs = %{version}-%{release}


# dashcore-utils
%package utils
Summary: A global payments network and decentralized application (dapp) platform: a peer-to-peer, fungible, digital currency, protocol, and platform. (commandline utilities)


# dashcore src.rpm
%description
Dash Core reference implementation. This is the source package for building
most of the Dash Core set of binary packages.  It will build
dashcore-{client,server,utils,libs,devel,debuginfo}.

Dash (Digital Cash) is a global payments network with its own cryptocurrency
offering businesses and individuals instant payments to anyone, anywhere in the
world. Payments are instant, easy and secure, with near-zero fees. Dash uses
peer-to-peer technology to operate with no central authority, managing
transactions and issuing money carried out collectively by the network.
Additionally, the Dash Network operates with a self-governing and self-funding
model. The Dash Network is the first ever successful decentralized autonomous
organizations (DAO). Dash Core is the name of the open source software which
enables the use of this currency. Dash has introduced many industry-first
innovations including masternodes, LLMQs, ChainLocks, and InstantSend. Dash is
digital cash that offers financial freedom to anyone.

Learn more at www.dash.org.


# dashcore-client
%description client
Dash is Digital Cash

Dash Core reference implementation. This package provides a user-friendly(er)
graphical wallet manager (dash-qt) for personal use. This package requires the
dashcore-utils RPM package to be installed as well.

Dash (Digital Cash) is a global payments network with its own cryptocurrency
offering businesses and individuals instant payments to anyone, anywhere in the
world. Payments are instant, easy and secure, with near-zero fees. Dash uses
peer-to-peer technology to operate with no central authority, managing
transactions and issuing money carried out collectively by the network.
Additionally, the Dash Network operates with a self-governing and self-funding
model. The Dash Network is the first ever successful decentralized autonomous
organizations (DAO). Dash Core is the name of the open source software which
enables the use of this currency. Dash has introduced many industry-first
innovations including masternodes, LLMQs, ChainLocks, and InstantSend. Dash is
digital cash that offers financial freedom to anyone.

Learn more at www.dash.org.


# dashcore-server
%description server
Dash Core reference implementation. This package provides dashd, a
peer-to-peer node and wallet server. It is the command line installation
without a graphical user interface. It can be used as a commandline wallet
but is typically used to run a full node or masternode. This package
requires the dashcore-utils and dashcore-sentinel RPM packages to be
installed.

Please refer to Dash Core documentation at dash.org for more information
about running a Masternode.

-

A Dash Full Node is a un-collatoralized member of a decentralized network of
servers that validate transactions and blocks. A Dash Masternode is a member
of a network of incentivized servers that perform expanded critical services
for the Dash cryptocurrency protocol.

Dash (Digital Cash) is a global payments network with its own cryptocurrency
offering businesses and individuals instant payments to anyone, anywhere in the
world. Payments are instant, easy and secure, with near-zero fees. Dash uses
peer-to-peer technology to operate with no central authority, managing
transactions and issuing money carried out collectively by the network.
Additionally, the Dash Network operates with a self-governing and self-funding
model. The Dash Network is the first ever successful decentralized autonomous
organizations (DAO). Dash Core is the name of the open source software which
enables the use of this currency. Dash has introduced many industry-first
innovations including masternodes, LLMQs, ChainLocks, and InstantSend. Dash is
digital cash that offers financial freedom to anyone.

Learn more at www.dash.org.



# dashcore-libs
%description libs
This package provides libdashconsensus, which is used by third party
applications to verify scripts (and other functionality in the future).

Dash (Digital Cash) is a global payments network with its own cryptocurrency
offering businesses and individuals instant payments to anyone, anywhere in the
world. Payments are instant, easy and secure, with near-zero fees. Dash uses
peer-to-peer technology to operate with no central authority, managing
transactions and issuing money carried out collectively by the network.
Additionally, the Dash Network operates with a self-governing and self-funding
model. The Dash Network is the first ever successful decentralized autonomous
organizations (DAO). Dash Core is the name of the open source software which
enables the use of this currency. Dash has introduced many industry-first
innovations including masternodes, LLMQs, ChainLocks, and InstantSend. Dash is
digital cash that offers financial freedom to anyone.

Learn more at www.dash.org.


# dashcore-devel
%description devel
This package provides the libraries and header files necessary to compile
programs which use libdashconsensus.

Dash (Digital Cash) is a global payments network with its own cryptocurrency
offering businesses and individuals instant payments to anyone, anywhere in the
world. Payments are instant, easy and secure, with near-zero fees. Dash uses
peer-to-peer technology to operate with no central authority, managing
transactions and issuing money carried out collectively by the network.
Additionally, the Dash Network operates with a self-governing and self-funding
model. The Dash Network is the first ever successful decentralized autonomous
organizations (DAO). Dash Core is the name of the open source software which
enables the use of this currency. Dash has introduced many industry-first
innovations including masternodes, LLMQs, ChainLocks, and InstantSend. Dash is
digital cash that offers financial freedom to anyone.

Learn more at www.dash.org.


# dashcore-utils
%description utils
Dash is Digital Cash

This package provides dash-cli, a utility to communicate with and control a
Dash server via its RPC protocol, and dash-tx, a utility to create custom
Dash transactions.

Dash (Digital Cash) is a global payments network with its own cryptocurrency
offering businesses and individuals instant payments to anyone, anywhere in the
world. Payments are instant, easy and secure, with near-zero fees. Dash uses
peer-to-peer technology to operate with no central authority, managing
transactions and issuing money carried out collectively by the network.
Additionally, the Dash Network operates with a self-governing and self-funding
model. The Dash Network is the first ever successful decentralized autonomous
organizations (DAO). Dash Core is the name of the open source software which
enables the use of this currency. Dash has introduced many industry-first
innovations including masternodes, LLMQs, ChainLocks, and InstantSend. Dash is
digital cash that offers financial freedom to anyone.

Learn more at www.dash.org.



%prep
# Prep section starts us in directory .../BUILD (aka {_builddir})

%if 0%{?suse_version:1}
  echo "======== OpenSUSE version: %{suse_version} %{sle_version}"
  echo "-------- Leap 15.1  will report as 1500 150100"
  echo "-------- Leap 15.2  will report as 1500 150200"
  echo "-------- Tumbleweed will report as 1550 undefined"
  %{error: "OpenSUSE (Leap or Tumbleweed) are not supported build targets."}
%endif

%if 0%{?rhel}
  echo "======== RHEL version: %{rhel}"
%endif
%if 0%{?centos}
  echo "======== Centos version — {centos}: %{centos} {centos_ver}: %{centos_ver}"
%endif
%if 0%{?fedora:1}
  echo "======== Fedora version: %{fedora}"
%endif

# Message if EL7 found (probably should check for other unsupported OSes as well)
%if 0%{?rhel} && 0%{?rhel} < 8
%{error: "EL7-based platforms (CentOS7/RHEL7) are not supported build targets."}
%endif
%if 0%{?centos} && 0%{?centos_ver} < 8
%{error: "EL7-based platforms (CentOS7/RHEL7) are not supported build targets."}
%endif

%define _disable_wallet --disable-wallet --without-gui
%if ! %{disable_wallet}
  %define _disable_wallet %{nil}
%endif

mkdir -p %{projectroot}

# Source0: dashcore (source)
# {_builddir}/dashcore-0.16/dash-0.16.0.0/
%if %{buildFromSource}
%setup -q -T -D -a 0 -n %{projectroot}

# Source6: dashcore (binary)
# {_builddir}/dashcore-0.16/dashcore-0.16.0/
%else
%setup -q -T -D -a 6 -n %{projectroot}
%endif

# Source1: contributions
# {_builddir}/dashcore-0.16.0/dashcore-0.16.0-contrib/
%setup -q -T -D -a 1 -n %{projectroot}

# Source2: bls (chai_bls) archive
# Source3: libbacktrace (backtrace) archive
# Source4: miniupnpc archive
# Source5: bdb archive
# {_sourcedir} == ../../SOURCES/ but rpmlint hates use of {_sourcedir}
# Moving the supplied tarballs from {_sourcedir} to their desired locations
%if %{buildFromSource} && %{useExtraSources}
mkdir -p %{sourcetree}/depends/sources/
mv ../../SOURCES/%{blsarchivename}.tar.gz %{sourcetree}/depends/sources/v%{blsarchivedate}.tar.gz
mkdir -p %{sourcetree}/depends/sources/
mv ../../SOURCES/%{libbacktracearchivename}.tar.gz %{sourcetree}/depends/sources/%{libbacktracearchiveversion}.tar.gz
%if 0%{?rhel:1} || 0%{?centos:1}
mkdir -p %{sourcetree}/depends/sources/
mv ../../SOURCES/%{miniupnpcarchivename}.tar.gz %{sourcetree}/depends/sources/%{miniupnpcarchivename}.tar.gz
mv ../../SOURCES/%{bdbarchivename}.tar.gz %{sourcetree}/depends/sources/%{bdbarchivename}.tar.gz
%endif
%endif

# Patch0: get rid of that annoying "About QT" menu option
%if ! %{clientSourceIsBinary}
cd %{sourcetree}
%patch0 -p1
cd ..
%endif

#t0dd: Prep SELinux policy -- NOT USED YET and probably never will
# Done here to prep for action taken in the build step
# At this moment, we are in the projectroot directory
mkdir -p selinux-tmp
cp -p %{srccontribtree}/linux/selinux/dash.{te,if,fc} selinux-tmp/

%if %{buildFromSource} && %{useSystemLibraries}
# Swap out packages.mk and chia_bls.mk makefiles in order to force usage of
# OS native devel libraries and tools.
cp -a %{srccontribtree}/build/depends/packages/*.mk %{sourcetree}/depends/packages/
%if 0%{?rhel:1} || 0%{?centos:1}
cp -a %{srccontribtree}/build/depends/packages/packages.mk--EL8 %{sourcetree}/depends/packages/packages.mk
%endif
%endif
# For debugging purposes...

%if ! %{targetIsProduction}
  cd %{_builddir} ; tree -df -L 1 %{projectroot} ; cd -
%endif


%build
# This section starts us in directory {_builddir}/{projectroot}
%if ! %{buildFromSource}
  exit 0
%endif

## A note about the _target_platform (RPM) and AC_CANONICAL_HOST (Makefile)
## macros.
## 
## _target_platform for Fedora/EL8 on X86_64 is x86_64-redhat-linux-gnu
## AC_CANONICAL_HOST in the makefile will result in x86_64-pc-linux-gnu.
## Regardless, config.sub in the depends directory will result in this
## target host being set as such (...pc-linux-gnu) unless we force it to
## something different.
##
## This is a bit baffling. If we don't add HOST= to the makefile, it will
## default to x86_64-pc-linux-gnu. RPM though wants us to use _target_platform.
## What is the "right way?" I don't know. I experiment with both.
##
## Read more:
## http://ftp.rpm.org/api/4.4.2.2/config_macros.html
## https://www.gnu.org/software/autoconf/manual/autoconf-2.69/html_node/Canonicalizing.html

cd %{sourcetree}

# build dependencies
cd depends
#%%define _target_platformX x86_64-pc-linux-gnu
%define _target_platformX %{_target_platform}
# example: make HOST=x86_64-redhat-linux-gnu -j4
make HOST=%{_target_platformX} -j$(nproc)
cd ..

# build code
%define _targettree %{_builddir}/%{projectroot}/%{sourcetree}/depends/%{_target_platformX}

%define _disable_tests --disable-tests --disable-gui-tests
%if %{testing_extras}
  %define _disable_tests %{nil}
%endif

./autogen.sh

## Notes for next step:
## - for building on ARM (which I do not do) you may have to add
##   --enable-reduce-exports
## - --enable-hardening is likely redundant since the RPM build instructions
##   sets it already, but adding anyway.
## - building without system libraries replacing most libraries represented in
##   the depends tree currently does not work. For whatever reason, the QT
##   libraries don't get picked up in the make step after the configure step.

%if %{useSystemLibraries}
  # old configuration
  #%%define _FLAGS CPPFLAGS="$CPPFLAGS -I%%{_targettree}/include -I%%{_includedir}" LDFLAGS="$LDFLAGS -L%%{_targettree}/lib -L%%{_libdir}"
  #%%{_FLAGS} ./configure --libdir=%%{_targettree}/lib --prefix=%%{_targettree} --enable-reduce-exports %%{_disable_tests} --disable-zmq
  # current configuration
  %define _FLAGS CXXFLAGS="-I%{_includedir} -I%{_targettree}/include $CXXFLAGS -O" CPPFLAGS="-I%{_includedir} -I%{_targettree}/include $CPPFLAGS" LDFLAGS="-L%{_libdir} -L%{_targettree}/lib $LDFLAGS"
  %{_FLAGS} ./configure --libdir=%{_targettree}/lib --includedir=%{_targettree}/include --prefix=%{_targettree} --enable-hardening %{_disable_tests} %{_disable_wallet}
  make
%else
  # NOTE!!! THIS METHOD NOT WORKING JUST YET.
  %define _FLAGS CXXFLAGS="-I%{_targettree}/include -I%{_includedir} $CXXFLAGS -O" CPPFLAGS="-I%{_targettree}/include -I%{_includedir} $CPPFLAGS" LDFLAGS="-L%{_targettree}/lib -L%{_libdir} $LDFLAGS"
  %define _PKGCONFIG PKG_CONFIG_PATH="%{_targettree}/lib/pkgconfig:%{_targettree}/share/pkgconfig:%{_libdir}/pkgconfig"
  %define _QTSTUFF "--with-qt-plugindir=%{_targettree}/plugins --with-qt-translationdir=%{_targettree}/translations --with-qt-libdir=%{_targettree}/lib --with-qt-incdir=%{_targettree}/include --with-qt-bindir=%{_targettree}/bin"
  # This does nothing, commenting out
  #cd %%{_targettree} && cp $(find ./plugins | grep "\.a$") ./lib/
  #cd ../..
  %{_FLAGS} %{_PKGCONFIG} ./configure --libdir=%{_targettree}/lib --includedir=%{_targettree}/include --with-boost-libdir=%{_targettree}/lib --prefix=%{_targettree} --enable-hardening %{_disable_tests} %{_disable_wallet} %{_QTSTUFF}
  %{_PKGCONFIG} make 
%endif

cd ..

#t0dd Not using for now. Probably will never get to this.
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
# This section starts us in directory {_builddir}/{projectroot}
%if ! %{buildFromSource}
  exit 0
%endif

cd %{sourcetree}
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
# This section starts us in directory {_builddir}/{projectroot}
%if %{buildFromSource}
  cd %{sourcetree}
  # make install deploys to {_targettree}/ (defined in build step)
  #make INSTALL="install -p" CP="cp -p" DESTDIR=%%{buildroot} install
  make install
  cd ..
%endif

# Cheatsheet for built-in RPM macros:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/
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
%define _rawlib lib
%define _usr_lib /usr/%{_rawlib}
# These three are already defined in newer versions of RPM, but not in el7
# Leaving here for posterity because EL7 is no longer being built.
%if 0%{?rhel} && 0%{?rhel} < 8
  %define _tmpfilesdir %{_usr_lib}/tmpfiles.d
  %define _unitdir %{_usr_lib}/systemd/system
  %define _metainfodir %{_datadir}/metainfo
%endif

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
install -d -m755 -p %{buildroot}%{_includedir}
install -d -m755 -p %{buildroot}%{_libdir}

%if %{buildFromSource}
  mv %{_targettree}/bin/dash* %{buildroot}%{_bindir}/
  mv %{_targettree}/include/dash* %{buildroot}%{_includedir}/
  mv %{_targettree}/lib/libdash* %{buildroot}%{_libdir}/
  install -d -m755 -p %{buildroot}%{_libdir}/pkgconfig
  mv %{_targettree}/lib/pkgconfig/libdash* %{buildroot}%{_libdir}/pkgconfig/
%endif

%if %{clientSourceIsBinary} && %{serverSourceIsBinary}
  mv %{binarytree}/bin/dash* %{buildroot}%{_bindir}/
  mv %{binarytree}/include/dash* %{buildroot}%{_includedir}/
  mv %{binarytree}/lib/libdash* %{buildroot}%{_libdir}/
%else
  %if %{clientSourceIsBinary}
    mv %{binarytree}/bin/dash-qt %{buildroot}%{_bindir}/
  %endif
  %if %{serverSourceIsBinary}
    mv %{binarytree}/bin/dashd %{buildroot}%{_bindir}/
  %endif
%endif

# Remove the test binaries if they are still floating around
%if ! %{testing_extras}
  rm -f %{buildroot}%{_bindir}/test_*
  rm -f %{buildroot}%{_bindir}/bench_dash
%endif

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

# Man Pages (from contrib) -- man5 documents now defunct
install -D -m644 %{srccontribtree}/linux/man/man1/* %{buildroot}%{_mandir}/man1/
#install -D -m644 %%{srccontribtree}/linux/man/man5/* %%{buildroot}%%{_mandir}/man5/
# Man Pages (from upstream) - likely to overwrite ones from contrib (which is fine)
%if %{buildFromSource}
install -D -m644 %{sourcetree}/doc/man/*.1* %{buildroot}%{_mandir}/man1/
%else
install -D -m644 %{binarytree}/share/man/man1/*.1* %{buildroot}%{_mandir}/man1/
%endif

%if %{clientSourceIsBinary} || %{serverSourceIsBinary}
  # probably the same as above. I haven't checked.
  install -D -m644 %{binarytree}/share/man/man1/*.1* %{buildroot}%{_mandir}/man1/
%endif

%if %{disable_wallet}
  rm -f %{buildroot}%{_mandir}/man1/dash-qt*
  rm -f %{buildroot}%{_bindir}/dash-qt
%endif

gzip -f %{buildroot}%{_mandir}/man1/*.1
#gzip -f %%{buildroot}%%{_mandir}/man5/*.5

# Bash completion
%if %{buildFromSource}
install -D -m644 %{sourcetree}/contrib/dash-cli.bash-completion %{buildroot}%{_datadir}/bash-completion/completions/dash-cli
install -D -m644 %{sourcetree}/contrib/dash-tx.bash-completion %{buildroot}%{_datadir}/bash-completion/completions/dash-tx
install -D -m644 %{sourcetree}/contrib/dashd.bash-completion %{buildroot}%{_datadir}/bash-completion/completions/dashd
%else
install -D -m644 %{srccontribtree}/linux/binary-build-contribs/bash-completion/dash-cli.bash-completion %{buildroot}%{_datadir}/bash-completion/completions/dash-cli
install -D -m644 %{srccontribtree}/linux/binary-build-contribs/bash-completion/dash-tx.bash-completion %{buildroot}%{_datadir}/bash-completion/completions/dash-tx
install -D -m644 %{srccontribtree}/linux/binary-build-contribs/bash-completion/dashd.bash-completion %{buildroot}%{_datadir}/bash-completion/completions/dashd
%endif

## DESKTOP STUFF
%if ! %{disable_wallet}
# Desktop elements - desktop file and kde protocol file (from contrib)
cd %{srccontribtree}/linux/desktop/
# org.dash.Dashcore.dash-qt.desktop
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_desktop_files
install -m755  dash-qt.wrapper.sh %{buildroot}%{_bindir}/
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{tld_vendor_product_id}.dash-qt.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{tld_vendor_product_id}.dash-qt.desktop
# org.dash.Dashcore.dash-qt.appdata.xml
# https://docs.fedoraproject.org/en-US/packaging-guidelines/AppData/
install -D -m644 -p %{tld_vendor_product_id}.dash-qt.appdata.xml %{buildroot}%{_metainfodir}/%{tld_vendor_product_id}.dash-qt.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml
cd ../../..

%if %{buildFromSource}
cd %{sourcetree}/share/pixmaps/
# Desktop elements - hicolor icons
install -D -m644 dash128.png                %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{tld_vendor_product_id}.dash-qt.png
install -D -m644 dash16.png                   %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{tld_vendor_product_id}.dash-qt.png
install -D -m644 dash256.png                %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{tld_vendor_product_id}.dash-qt.png
install -D -m644 dash32.png                   %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{tld_vendor_product_id}.dash-qt.png
install -D -m644 dash64.png                   %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{tld_vendor_product_id}.dash-qt.png
install -D -m644 dash-hicolor-scalable.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{tld_vendor_product_id}.dash-qt.svg
# Desktop elements - HighContrast icons
install -D -m644 dash-HighContrast-128.png       %{buildroot}%{_datadir}/icons/HighContrast/128x128/apps/%{tld_vendor_product_id}.dash-qt.png
install -D -m644 dash-HighContrast-16.png          %{buildroot}%{_datadir}/icons/HighContrast/16x16/apps/%{tld_vendor_product_id}.dash-qt.png
install -D -m644 dash-HighContrast-22.png          %{buildroot}%{_datadir}/icons/HighContrast/22x22/apps/%{tld_vendor_product_id}.dash-qt.png
install -D -m644 dash-HighContrast-24.png          %{buildroot}%{_datadir}/icons/HighContrast/24x24/apps/%{tld_vendor_product_id}.dash-qt.png
install -D -m644 dash-HighContrast-256.png       %{buildroot}%{_datadir}/icons/HighContrast/256x256/apps/%{tld_vendor_product_id}.dash-qt.png
install -D -m644 dash-HighContrast-32.png          %{buildroot}%{_datadir}/icons/HighContrast/32x32/apps/%{tld_vendor_product_id}.dash-qt.png
install -D -m644 dash-HighContrast-48.png          %{buildroot}%{_datadir}/icons/HighContrast/48x48/apps/%{tld_vendor_product_id}.dash-qt.png
install -D -m644 dash-HighContrast-scalable.svg %{buildroot}%{_datadir}/icons/HighContrast/scalable/apps/%{tld_vendor_product_id}.dash-qt.svg
cd -
%endif
%if %{clientSourceIsBinary}
cd %{srccontribtree}/linux/binary-build-contribs/desktop/
install -D -m644 dash-hicolor-scalable.svg           %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{tld_vendor_product_id}.dash-qt.svg
install -D -m644 dash-HighContrast-scalable.svg %{buildroot}%{_datadir}/icons/HighContrast/scalable/apps/%{tld_vendor_product_id}.dash-qt.svg
cd -
%endif
# endif not disabled wallet
%endif

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
logtimestamps=1
maxconnections=8

# A systemd managed masternode probably not going to be a wallet as well
# Set to 0 if you also want it to be a wallet.
disablewallet=1

# Only localhost allowed to connect to make RPC calls.
rpcallowip=127.0.0.1
" >> %{buildroot}%{_sysconfdir}/dashcore/dash.conf
install -D -m644 %{buildroot}%{_sysconfdir}/dashcore/dash.conf %{srccontribtree}/dash.conf.example

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
" >> %{srccontribtree}/dash.conf.example

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

#t0dd Not using for now. Probably will never get to this.
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
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
# the macro'ed reload is not working for some reason
#%%firewalld_reload
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

# Update the desktop database
# https://fedoraproject.org/wiki/NewMIMESystem
/usr/bin/update-desktop-database &> /dev/null || :

%postun client
# Update the desktop database
# https://fedoraproject.org/wiki/NewMIMESystem
/usr/bin/update-desktop-database &> /dev/null || :
# the macro'ed reload is not working for some reason
#%%firewalld_reload
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


# dashcore-server
%pre server
# This is for the case that you run dash core as a service (systemctl start dashd)
# _sharedstatedir is /var/lib
getent group dashcore >/dev/null || groupadd -r dashcore
getent passwd dashcore >/dev/null || useradd -r -g dashcore -d %{_sharedstatedir}/dashcore -s /sbin/nologin -c "System user 'dashcore' to isolate Dash Core execution" dashcore

# Notes:
#  _localstatedir is /var
#  _sharedstatedir is /var/lib
#  /var/lib/dashcore is the $HOME for the dashcore user
#  There is argument for moving all data to /srv/dashcore, and I may
#  do so in the future.

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
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
# the macro'ed reload is not working for some reason
#%%firewalld_reload
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

# Not using for now.
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
#TODO: Replace above with %%tmpfiles_create_package macro
#TODO: https://github.com/systemd/systemd/blob/master/src/core/macros.systemd.in


# dashcore-server
%preun server
%systemd_preun dashd.service


# dashcore-server
%postun server
%systemd_postun dashd.service
# the macro'ed reload is not working for some reason
#%%firewalld_reload
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

# Not using for now.
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
%if ! %{disable_wallet}
%if %{buildFromSource}
%license %{sourcetree}/COPYING
%doc %{sourcetree}/doc/*.md %{srccontribtree}/dash.conf.example
%else
%license %{srccontribtree}/linux/binary-build-contribs/license/COPYING
%doc %{srccontribtree}/linux/binary-build-contribs/doc/*.md %{srccontribtree}/dash.conf.example
%endif
%{_bindir}/dash-qt
%{_bindir}/dash-qt.wrapper.sh
%{_datadir}/applications/%{tld_vendor_product_id}.dash-qt.desktop
%{_metainfodir}/%{tld_vendor_product_id}.dash-qt.appdata.xml
# XXX Removing this unless someone gripes
#%%{_datadir}/kde4/services/dash-qt.protocol
%{_datadir}/icons/*
%{_mandir}/man1/dash-qt.1.gz
#%%{_mandir}/man5/masternode.conf.5.gz
%{_usr_lib}/firewalld/services/dashcore.xml
%{_usr_lib}/firewalld/services/dashcore-testnet.xml
%{_usr_lib}/firewalld/services/dashcore-rpc.xml
%{_usr_lib}/firewalld/services/dashcore-testnet-rpc.xml
#%%dir %%attr(750,dashcore,dashcore) %%{_sysconfdir}/dashcore
#%%config(noreplace) %%attr(640,dashcore,dashcore) %%{_sysconfdir}/dashcore/dash.conf
%if %{testing_extras}
  %{_bindir}/test_dash-qt
%endif
%endif


# dashcore-server
%files server
%defattr(-,root,root,-)
%if %{buildFromSource}
%license %{sourcetree}/COPYING
%doc %{sourcetree}/doc/*.md %{srccontribtree}/dash.conf.example
%else
%license %{srccontribtree}/linux/binary-build-contribs/license/COPYING
%doc %{srccontribtree}/linux/binary-build-contribs/doc/*.md %{srccontribtree}/dash.conf.example
%endif

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
%{_bindir}/dashd
%{_tmpfilesdir}/dashd.conf
%{_datadir}/bash-completion/completions/dashd
%{_mandir}/man1/dashd.1.gz
#%%{_mandir}/man5/dash.conf.5.gz
#%%{_mandir}/man5/masternode.conf.5.gz
#t0dd %%{_datadir}/selinux/*/dash.pp

%if %{testing_extras}
  %{_bindir}/test_dash
  %{_bindir}/bench_dash
%endif


# dashcore-libs
%files libs
%defattr(-,root,root,-)
%if %{buildFromSource}
%license %{sourcetree}/COPYING
%else
%license %{srccontribtree}/linux/binary-build-contribs/license/COPYING
%endif
%{_libdir}/*


# dashcore-devel
%files devel
%defattr(-,root,root,-)
%if %{buildFromSource}
%license %{sourcetree}/COPYING
%else
%license %{srccontribtree}/linux/binary-build-contribs/license/COPYING
%endif
%{_includedir}/*
%{_libdir}/*


# dashcore-utils
%files utils
%defattr(-,root,root,-)
%if %{buildFromSource}
%license %{sourcetree}/COPYING
%else
%license %{srccontribtree}/linux/binary-build-contribs/license/COPYING
%endif
%{_bindir}/dash-cli
%{_bindir}/dash-tx
%{_datadir}/bash-completion/completions/dash-cli
%{_datadir}/bash-completion/completions/dash-tx
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
#   * Announcement: https://www.dash.org/forum/threads/v14-0-testing.44047/
#   * Documentation:  
#     https://docs.dash.org/en/latest/developers/testnet.html
#     https://docs.dash.org/en/latest/masternodes/dip3-upgrade.html
#     https://thephez.github.io/en/developer-reference
#
# Source snapshots...
#     https://github.com/dashpay/dash/tags
#     https://github.com/dashpay/dash/releases
#     test example: dash-0.16.0.0-rc1.tar.gz
#     release example: dash-0.16.0.0.tar.gz
#
# Dash Core git repos...
#   * Dash: https://github.com/dashpay/dash
#   * Sentinel: https://github.com/dashpay/sentinel

%changelog
* Fri Jul 03 2020 Todd Warner <t0dd_at_protonmail.com> 0.16.0.0-0.3.rc2.taw
  - added CentOS distro checks, though to be frank, EPEL and CentOS have  
    matching macros. You can't tell if you are building for RHEL or CentOS by  
    evaluating RPM macros. Which is a PITA.
  - added some distro versioning output into the build log

* Thu Jul 02 2020 Todd Warner <t0dd_at_protonmail.com> 0.16.0.0-0.2.rc2.taw
  - 0.16 RC2 - https://github.com/dashpay/dash/releases/tag/v0.16.0.0-rc2

* Thu Jun 25 2020 Todd Warner <t0dd_at_protonmail.com> 0.16.0.0-0.2.rc1.taw
  - updated appdata.xml, .desktop files, and icons to desktop spec naming  
    and ID standards.

* Fri Jun 12 2020 Todd Warner <t0dd_at_protonmail.com> 0.16.0.0-0.1.rc1.taw
  - 0.16 RC1 — https://github.com/dashpay/dash/releases/tag/v0.16.0.0-rc1
  - Product brief: https://blog.dash.org/product-brief-dash-core-release-v0-16-0-now-on-testnet-55c7ac5ff768
  - Release highlights: Quorum Signing Optimizations, Network Threading Improvement, Minimum Protocol Check, Bitcoin Backports
  - Code cleanups: PrivateSend Code Refactoring, PrivateSend Create Denominations Improvement, Core Wallet Enhancements, many smaller updates.
  - spec: simply making EL8 packages from prebuilt binaries now. I am  
    tired of fighting.
  - spec: had to pull icons, bash-competion files, docs, and license from  
    the contribs archive when doing binary builds since the binary tarball    
    does not supply them. For icons, we're only suppling the SVGs in that case.
  - specfile: binary builds have been broken for awhile. Fixed.
  - spec: man pages refresh from upstream. May need to look back at old  
    manpages and PR some updates back upstream (e.g. description is lacking).
  - spec: updated package descriptions to more align with upstream messaging. 

* Wed Feb 19 2020 Todd Warner <t0dd_at_protonmail.com> 0.15.0.0-1.taw
* Wed Feb 19 2020 Todd Warner <t0dd_at_protonmail.com> 0.15.0.0-0.8.testing.taw
  - 0.15 — https://github.com/dashpay/dash/releases/tag/v0.15.0.0
  - changed how dash.conf.example is constructed. I don't like it, but it is  
    what it is.
  - removed contributed pixmaps (no longer needed -- provided by upstream)
  - package summaries were too long. Shortened.

* Sat Feb 15 2020 Todd Warner <t0dd_at_protonmail.com> 0.15.0.0-0.7.rc4.taw
  - 0.15 RC4

* Thu Feb 06 2020 Todd Warner <t0dd_at_protonmail.com> 0.15.0.0-0.6.rc3.taw
  - 0.15 RC3

* Fri Jan 31 2020 Todd Warner <t0dd_at_protonmail.com> 0.15.0.0-0.5.rc2.taw
  - 0.15 RC2
  - Using desktop icon images from the shipped tarball (instead of a  
    separate tarball) to be deployed with the desktop client. I.e. My  
    contributions were included in this release:  
    https://github.com/dashpay/dash/pull/3209

* Mon Dec 23 2019 Todd Warner <t0dd_at_protonmail.com> 0.15.0.0-0.4.rc1.taw
  - re-ordered how libraries and includes are examined upon build. Previous  
    ordering resulted in a missing libQT5Core.so.5 dependency. Fixed.  
    ...i.e...  
    nothing provides libQt5Core.so.5(Qt_5.13)(64bit) needed by dashcore-client...

* Sun Dec 22 2019 Todd Warner <t0dd_at_protonmail.com> 0.15.0.0-0.3.rc1.taw
  - Simplified the "extra sources" logic.
  - There is some discrepancy in the Makefile's version of the target  
    platform (x86_64-pc-linux-gnu) and the RPM specfile's result  
    (x86_64-redhat-linux-gnu). We will use RPM's version since we then don't  
    need to hardcode a value in the specfile.
  - Note: For the life of me, I CANNOT get the build to work with the depends  
    system completely. For whatever reason, libqminimal (and I am sure other  
    QT libraries simply no longer can be found. Why? I don't get it. RPM  
    washes the environment clean and I, apparently, can't seem to rebuild it  
    from  scratch. Additionally, things are lost from process to process during  
    a build. So . . . Moral of the story: We use system-supplied libraries for  
    builds except for a few particulars (miniupnpc, etc). This is how a package  
    should be built anyway.

* Wed Dec 18 2019 Todd Warner <t0dd_at_protonmail.com> 0.15.0.0-0.2.rc1.taw
* Wed Dec 18 2019 Todd Warner <t0dd_at_protonmail.com> 0.15.0.0-0.1.rc1.taw
  - 0.15.0.0-rc1
  - Tried to simplify the "is this a source build or not" logic
  - Added flag to tell the build system whether to use the system OS  
    libraries or not. Ie, . . .
  - Note, for 0.15, the dash core development team stressed that they do not  
    prefer packagers to depend on certain system libraries. Though I  
    sympathize with their position on this, I don't agree. HOWEVER, it's  
    their project and I will defer on this point for the moment. It just  
    means that dash will never ever be distributed by Fedora or RH proper.
  - We now supply libbacktrace source tarball as well.
  - We now supply miniupnpc and db4 source tarballs for EL8 builds.

* Mon Dec 9 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.5-1.taw
* Mon Dec 9 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.5-1.rp.taw
* Mon Dec 9 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.5-0.1.testing.taw
* Mon Dec 9 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.5-0.1.testing.rp.taw
  - 0.14.0.5 -- repackaged (rp) builds are EL8 only.

* Fri Nov 22 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.4-1.taw
* Fri Nov 22 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.4-0.1.testing.taw
* Fri Nov 22 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.4-0.1.testing.rp.taw
  - 0.14.0.4 -- repackaged (rp) builds are EL8 only.

* Thu Aug 15 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.3-1.taw
* Thu Aug 15 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.3-0.1.testing.rp.taw
* Thu Aug 15 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.3-0.1.testing.taw
  - 0.14.0.3 -- repackaged (rp) builds are EL8 only.

* Thu Jul 04 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.2-1.taw
* Thu Jul 04 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.2-0.1.testing.rp.taw
* Thu Jul 04 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.2-0.1.testing.taw
  - 0.14.0.2 -- repackaged (rp) builds are EL8 only.

* Fri May 31 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.1-1.taw
* Fri May 31 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.1-0.1.testing.taw
  - 0.14.0.1

* Wed May 22 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.0-1.taw
* Wed May 22 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.0-0.3.testing.taw
  - 0.14

* Sun May 19 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.0-0.2.rc6.taw
  - 0.14 rc6

* Thu May 09 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.0-0.2.rc5.taw
  - 0.14 rc5

* Sun Apr 14 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.0-0.2.rc4.taw
  - 0.14 rc4

* Fri Apr 05 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.0-0.2.rc3.taw
  - 0.14 rc3

* Thu Apr 04 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.0-0.2.rc2.taw
  - vermajor and verminor shifted a decimal point
  - specfile cleanup
  - patch management more correct in the case building client from binaries
  - minor changes to prep for EL8 testing
  - adjustments to allow rp (repackaged) binary builds to work again.

* Thu Apr 04 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.3.0-2.taw
* Thu Apr 04 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.3.0-1.1.testing.taw
  - adjustments to allow rp (repackaged) binary builds to work again.

* Thu Apr 04 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.3.0-1.taw
* Thu Apr 04 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.3.0-0.1.testing.taw
  - 0.13.3.0
  - vermajor and verminor shifted a decimal point
  - specfile cleanup
  - patch management more correct in the case building client from binaries
  - minor changes to prep for EL8 testing

* Mon Apr 01 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.0-0.1.rc2.taw
  - 0.14.0.0-rc2

* Thu Mar 28 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.0-0.1.rc1.taw
  - 0.14.0.0-rc1

* Sat Mar 16 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.2.0-1.taw
* Sat Mar 16 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.2.0-0.2.testing.taw
* Fri Mar 15 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.2.0-0.1.testing.taw
  - 0.13.2.0
  - Fixed a ./configure --libdir thing that caused rpmlint to whine
  - Fixed a {_sourcedir} thing that also caused rpmlint to whine
  - Fixed the date of this changelog entry. cut-n-paste error.
  - Updated the URLs to the sources. They pointed to an old location.

* Sun Feb 24 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.1.0-3.taw
* Sun Feb 24 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.1.0-2.1.testing.taw
  - I'm an idiot. Using x86_64 binaries now for the x86_64 builds. ;)

* Sun Feb 24 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.1.0-2.taw
* Sun Feb 24 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.1.0-1.2.testing.taw
* Sun Feb 24 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.1.0-1.1.testing.taw
  - issues with F29 builds of dash-qt  
    including prebuilt for that component for now
  - can selectively include our own builds or prebuilt for client and/or   
    server -- this is far more complicated than it needs to be.
  - including bls-signatures archive eliminating need to reach out to the  
    internet during builds

* Fri Feb 08 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.1.0-1.taw
* Fri Feb 08 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.1.0-0.1.testing.taw
  - 0.13.1

* Fri Jan 25 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-2.taw
* Fri Jan 25 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-1.1.testing.taw
  - Updated systemd configuration for dashd to kickoff only after network is  
    "online" (network-online.target). Suggested by dash-dude, xkcd, after  
    experimentation on low-powered devices, like the raspberry pi.
  - Updated systemd configuration for dashd adjusting OOM score to a priority  
    score favorable to dashd.

* Mon Jan 14 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-1.taw
* Mon Jan 14 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.14.testing.taw
* Mon Jan 14 2019 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.13.testing.taw
  - 0.13.0.0

* Sat Dec 22 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.12.rc11.taw
  - 0.13.0.0-rc11

* Sat Dec 22 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.12.rc10.taw
  - 0.13.0.0-rc10

* Tue Dec 18 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.12.rc9.taw
  - comment out About QT menu item in GUI client (for "production" builds)  
    It's an implementation detail and shouldn't be there.

* Mon Dec 17 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.11.rc9.taw
  - 0.13.0.0-rc9

* Wed Dec 12 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.11.rc8.taw
  - Added a wrapper script around dash-qt in order to work around  
    QT5+GNOME+Wayland issues. The wrapper sets environment variables.  
    Reference dashcore-0.13.0-contrib/linux/desktop/dash-qt.wrapper.sh

* Mon Dec 10 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.10.rc8.taw3
* Mon Dec 10 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.10.rc8.taw2
* Mon Dec 10 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.10.rc8.taw1
* Mon Dec 10 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.10.rc8.taw
  - 0.13.0.0-rc8
  - fixed firewalld scriptlet calls
    - firewalld_reload macro is mysteriously not working - yanked!
  - fixed some systemd scriplet calls

* Fri Dec 07 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.10.rc7.taw
  - cleaned up a lot of links
  - call desktop file refresh after install and uninstall
  - firewalld_reload rpm macro used
  - _tmpfilesdir, _unitdir, _metainfodir only need to be defined if the build  
    is EL7 (very old rpm)

* Thu Dec 06 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.9.rc7.taw
  - 0.13.0-rc7
  - Updated a lot of text as well.

* Mon Dec 03 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.8.rc6.taw
  - moved dashd from /usr/sbin to /usr/bin since it is user run as well as  
    run by a node admin. This goes against the convention of some other  
    cryptocurrency packagers (notably bitcoin), but it is "more correct"  
    IMHO and in the HO, according to my interpretation, of the good folks of  
    the Filesystem Hierarchical Standard

* Fri Nov 30 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.7.rc6.taw
  - v0.13.0.0 RC6 - Spork 15 related

* Thu Nov 29 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.6.rc5.taw
  - v0.13.0.0 RC5

* Fri Nov 23 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.5.rc4.taw3
* Fri Nov 23 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.5.rc4.taw2
* Fri Nov 23 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.5.rc4.taw1
* Tue Nov 20 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.5.rc4.taw0
  - made desktop configuration more compatible to KDA Plasma's dock  
    `Exec=env XDG_CURRENT_DESKTOP=Unity /usr/bin/dash-qt %u` instead of just  
    `Exec=dash-qt %u`
  - abandoning attempts to build EL7 rpms. CentOS7/RHEL7 libraries are just  
    too dated.
    

* Sat Nov 17 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.4.rc4.taw
  - refined building of testing bits
  - reduced cruft landing in the lib and include directory trees
  - through trickery I got rid of the "don't hardcode /usr/lib" error  
    (a warning really) that rpmlint of the specfile issues

* Fri Nov 16 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.3.rc4.taw
  - v0.13.0.0 - https://github.com/dashpay/dash/releases/tag/v0.13.0.0-rc4

* Wed Nov 14 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.2.rc1.taw
* Wed Nov 14 2018 Todd Warner <t0dd_at_protonmail.com> 0.13.0.0-0.1.rc1.taw
  - v0.13.0.0 - https://github.com/dashpay/dash/releases/tag/v0.13.0.0-rc1
  - simplified the spec-file release string building logic a bit
  - include man pages from upstream source
  - include bash-completion files from upstream source

* Wed Sep 19 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.3-1.taw
* Wed Sep 19 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.3-0.1.testing.taw
  - v0.12.3.3 - https://github.com/dashpay/dash/releases/tag/v0.12.3.3

* Wed Jul 11 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.2-1.taw
* Wed Jul 11 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.2-0.1.testing.taw
  - v0.12.3.2 - https://github.com/dashpay/dash/releases/tag/v0.12.3.2

* Tue Jul 03 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.1-1.taw
* Tue Jul 03 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.1-0.1.testing.taw
  - v0.12.3.1 - https://github.com/dashpay/dash/releases/tag/v0.12.3.1

* Thu Jun 21 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.10.testing.taw
  - v0.12.3.0 - https://github.com/dashpay/dash/releases/tag/v0.12.3.0

* Thu Jun 21 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.9.rc5.taw
  - v0.12.3-rc5 - https://github.com/dashpay/dash/releases/tag/v0.12.3.0-rc5

* Wed Jun 13 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.8.rc4.taw
  - v0.12.3-rc4 - https://github.com/dashpay/dash/releases/tag/v0.12.3.0-rc4

* Sun Jun 10 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.7.rc3.taw
  - v0.12.3-rc3 - https://github.com/dashpay/dash/releases/tag/v0.12.3.0-rc3

* Sun Jun 3 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.6.rc2.taw
  - v0.12.3-rc2 - https://github.com/dashpay/dash/releases/tag/v0.12.3.0-rc2
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
  - Another 0.12.3 test build (from github.com origin/develop)

* Sat Apr 28 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.3.testing.20180428.taw
  - Another 0.12.3 test build (from github.com origin/develop)

* Wed Apr 25 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.2.testing.taw
  - Major cleanup

* Sun Apr 8 2018 Todd Warner <t0dd_at_protonmail.com> 0.12.3.0-0.1.testing.taw
  - 0.12.3 test build
  - name-version-release more closely matches industry guidelines:  
    https://docs.fedoraproject.org/en-US/packaging-guidelines/Versioning/
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
  - Initial 0.12.2 test build

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
  - Release 0.12.1.0 - 56971f8
  - Announcement: https://github.com/dashpay/dash/releases/tag/v0.12.1.0
