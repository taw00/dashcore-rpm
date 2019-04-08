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
Summary: Peer-to-peer, fungible, digital currency, protocol, and platform for payments and decentralized applications

%define targetIsProduction 0
%define clientSourceIsPrebuilt 0
%define serverSourceIsPrebuilt 0

# ie. if the dev team includes things like rc3 in the filename
%undefine buildQualifier
%define buildQualifier rc3

# VERSION
%define vermajor 0.14
%define verminor1 0
%define verminor2 0
%define verminor %{verminor1}.%{verminor2}
Version: %{vermajor}.%{verminor}

# RELEASE
# package release, and, test-only, extrarel
%define _pkgrel 1
%if ! %{targetIsProduction}
  %define _pkgrel 0.2
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
%if %{clientSourceIsPrebuilt} && %{serverSourceIsPrebuilt}
  %define _rp rp
%else
  %if %{clientSourceIsPrebuilt}
    %define _rp rpc
  %else
  %if %{serverSourceIsPrebuilt}
    %define _rp rps
  %endif
  %endif
%endif

# have to use _variables because rpm spec macros are easily recursive and break.
%define _snapinfo THIS_WILL_BE_REPLACED
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

# the archive name and directory tree can have some variances
# v0.14.0.0.tar.gz
%define _archivename_alt1 v%{version}
# dash-0.14.0.0.tar.gz
%define _archivename_alt2 %{_name_d}-%{version}
# dashcore-0.14.0.tar.gz
%define _archivename_alt3 %{_name_dc}-%{vermajor}.%{verminor1}
# dashcore-0.14.0.0.tar.gz
%define _archivename_alt4 %{_name_dc}-%{version}

# Extracted source tree structure (extracted in .../BUILD)
#   srcroot               dashcore-0.14.0
#      \_sourcetree         \_dash-0.14.0.0 or dashcore-0.14.0 or dash-0.14.0.0-rc1...
#      \_binarytree         \_dashcore-0.14.0 or dash-0.14.0-rc1...
#      \_srccontribtree     \_dashcore-0.14.0-contrib
#      \_patch_files        \_dash-0.14.0-...patch
#      \_blsarchive         \_bls-signatures-20181101.tar.gz

# our selection for this build - edit this
%define _sourcearchivename %{_archivename_alt2}
%define _binaryarchivename %{_archivename_alt4}
%define _binarytree %{_archivename_alt3}

%if 0%{?buildQualifier:1}
  %define sourcearchivename %{_sourcearchivename}-%{buildQualifier}
  %define binaryarchivename %{_binaryarchivename}
  %define sourcetree %{_sourcearchivename}-%{buildQualifier}
  %define binarytree %{_binarytree}-%{buildQualifier}
%else
  %define sourcearchivename %{_sourcearchivename}
  %define binaryarchivename %{_binaryarchivename}
  %define sourcetree %{_sourcearchivename}
  %define binarytree %{_binarytree}
%endif
%define blsarchivedate 20181101
%define blsarchivename bls-signatures-%{blsarchivedate}

%define srcroot %{name}-%{vermajor}
%define srccontribtree %{name}-%{vermajor}-contrib


%if 0%{?buildQualifier:1}
Source0: https://github.com/dashpay/dash/archive/v%{version}-%{buildQualifier}/%{sourcearchivename}.tar.gz
%else
Source0: https://github.com/dashpay/dash/archive/v%{version}/%{sourcearchivename}.tar.gz
%endif

Source1: https://github.com/taw00/dashcore-rpm/blob/master/source/SOURCES/%{srccontribtree}.tar.gz
Source2: https://github.com/taw00/dashcore-rpm/blob/master/source/SOURCES/%{blsarchivename}.tar.gz

%if %{clientSourceIsPrebuilt} || %{serverSourceIsPrebuilt}
%if 0%{?buildQualifier:1}
Source3: https://github.com/dashpay/dash/archive/v%{version}-%{buildQualifier}/%{binaryarchivename}-x86_64-linux-gnu.tar.gz
%else
Source3: https://github.com/dashpay/dash/archive/v%{version}/%{binaryarchivename}-x86_64-linux-gnu.tar.gz
%endif
%endif

%if ! %{clientSourceIsPrebuilt}
Patch0: https://github.com/taw00/dashcore-rpm/blob/master/source/SOURCES/%{_name_d}-%{vermajor}-remove-about-qt-menu-item.patch
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

%if ! %{clientSourceIsPrebuilt} || ! %{serverSourceIsPrebuilt}
  %define buildFromSource 1
%endif


%if 0%{?buildFromSource:1}
# As recommended by...
# https://github.com/dashpay/dash/blob/develop/doc/build-unix.md
BuildRequires: libtool make autoconf automake patch
#BuildRequires: gcc-c++ >= 4.9 cmake libstdc++-static
BuildRequires: cmake libstdc++-static
BuildRequires: python3
BuildRequires: libdb4-cxx-devel gettext
BuildRequires: gettext
# t0dd: added to avoid unneccessary fetching of libraries from the internet
#       which is a packaging no-no
BuildRequires: openssl-devel boost-devel libevent-devel
BuildRequires: miniupnpc-devel ccache
#BuildRequires: python3-zmq zeromq-devel
# t0dd: added to satisfy chia_bls.
BuildRequires: gmp-devel
%endif
# Other BuildRequires listed per package below

#t0dd: SELinux stuff that I just haven't addressed yet...
#BuildRequires: checkpolicy selinux-policy-devel selinux-policy-doc

# tree, vim-enhanced, and less for mock build environment introspection
%if ! %{targetIsProduction}
BuildRequires: tree vim-enhanced less findutils
%endif


# dashcore-client
%package client
Summary: Peer-to-peer, fungible, digital currency, protocol, and platform for payments and decentralized applications (desktop reference client)
Requires: dashcore-utils = %{version}-%{release}
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
Requires: firewalld-filesystem
Requires(post): firewalld-filesystem
Requires(postun): firewalld-filesystem
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires: qt5-qtwayland
%endif
# Required for installing desktop applications on linux
BuildRequires: libappstream-glib desktop-file-utils
%if 0%{?buildFromSource:1}
# t0dd: added to avoid unneccessary fetching of libraries from the internet
#       which is a packaging no-no
BuildRequires: qrencode-devel protobuf-devel
BuildRequires: qt5-qtbase-devel qt5-linguist
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires: qt5-qtwayland-devel
%endif
%endif

# dashcore-server
%package server
Summary: Peer-to-peer, fungible, digital currency, protocol, and platform for payments and decentralized applications (reference server)
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
Summary: Peer-to-peer, fungible, digital currency, protocol, and platform for payments and decentralized applications (consensus libraries)


# dashcore-devel
%package devel
Summary: Peer-to-peer, fungible, digital currency, protocol, and platform for payments and decentralized applications (dev libraries and headers)
Requires: dashcore-libs = %{version}-%{release}


# dashcore-utils
%package utils
Summary: Peer-to-peer, fungible, digital currency, protocol, and platform for payments and decentralized applications (commandline utilities)


# dashcore src.rpm
%description
Dash Core reference implementation. This is the source package for building
most of the Dash Core set of binary packages.  It will build
dashcore-{client,server,utils,libs,devel,debuginfo}.

Dash (Digital Cash) is a digital currency that enables anonymous, instant
payments to anyone, anywhere in the world. Dash uses peer-to-peer technology to
operate with no central authority: managing transactions and issuing money are
carried out collectively by the network. Additionally, the Dash Network
operates with a self-governing and self-funding model. The Dash Network is the
first ever successful decentralized autonomous organizations (DAO). Dash Core
is the name of the open source software which enables the use of this currency.

Learn more at www.dash.org.


# dashcore-client
%description client
Dash is Digital Cash

Dash Core reference implementation. This package provides a user-friendly(er)
graphical wallet manager (dash-qt) for personal use. This package requires the
dashcore-utils RPM package to be installed as well.

Dash (Digital Cash) is a digital currency that enables anonymous, instant
payments to anyone, anywhere in the world. Dash uses peer-to-peer technology to
operate with no central authority: managing transactions and issuing money are
carried out collectively by the network. Additionally, the Dash Network
operates with a self-governing and self-funding model. The Dash Network is the
first ever successful decentralized autonomous organizations (DAO). Dash Core
is the name of the open source software which enables the use of this currency.

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

Dash (Digital Cash) is a digital currency that enables anonymous, instant
payments to anyone, anywhere in the world. Dash uses peer-to-peer technology to
operate with no central authority: managing transactions and issuing money are
carried out collectively by the network. Additionally, the Dash Network
operates with a self-governing and self-funding model. The Dash Network is the
first ever successful decentralized autonomous organizations (DAO). Dash Core
is the name of the open source software which enables the use of this currency.

Learn more at www.dash.org.



# dashcore-libs
%description libs
This package provides libdashconsensus, which is used by third party
applications to verify scripts (and other functionality in the future).

Dash (Digital Cash) is a digital currency that enables anonymous, instant
payments to anyone, anywhere in the world. Dash uses peer-to-peer technology to
operate with no central authority: managing transactions and issuing money are
carried out collectively by the network. Additionally, the Dash Network
operates with a self-governing and self-funding model. The Dash Network is the
first ever successful decentralized autonomous organizations (DAO). Dash Core
is the name of the open source software which enables the use of this currency.

Learn more at www.dash.org.


# dashcore-devel
%description devel
This package provides the libraries and header files necessary to compile
programs which use libdashconsensus.

Dash (Digital Cash) is a digital currency that enables anonymous, instant
payments to anyone, anywhere in the world. Dash uses peer-to-peer technology to
operate with no central authority: managing transactions and issuing money are
carried out collectively by the network. Additionally, the Dash Network
operates with a self-governing and self-funding model. The Dash Network is the
first ever successful decentralized autonomous organizations (DAO). Dash Core
is the name of the open source software which enables the use of this currency.

Learn more at www.dash.org.


# dashcore-utils
%description utils
Dash is Digital Cash

This package provides dash-cli, a utility to communicate with and control a
Dash server via its RPC protocol, and dash-tx, a utility to create custom
Dash transactions.

Dash (Digital Cash) is a digital currency that enables anonymous, instant
payments to anyone, anywhere in the world. Dash uses peer-to-peer technology to
operate with no central authority: managing transactions and issuing money are
carried out collectively by the network. Additionally, the Dash Network
operates with a self-governing and self-funding model. The Dash Network is the
first ever successful decentralized autonomous organizations (DAO). Dash Core
is the name of the open source software which enables the use of this currency.

Learn more at www.dash.org.



%prep
# Prep section starts us in directory .../BUILD (aka {_builddir})

# Message if EL7 found (probably should check for other unsupported OSes as well)
%if 0%{?rhel} && 0%{?rhel} < 8
  %{error: "EL7-based platforms (CentOS7/RHEL7) are not supportable build targets."}
%endif

mkdir -p %{srcroot}
# Source0: dashcore (source)
## {_builddir}/dashcore-0.14.0/dashcore-0.14.0.0/  ..or something like..
## {_builddir}/dash-0.14.0/dash-0.14.0.0-rc1/
%setup -q -T -D -a 0 -n %{srcroot}

# Source1: contributions
## {_builddir}/dashcore-0.14.0/dashcore-0.14.0-contrib/
%setup -q -T -D -a 1 -n %{srcroot}

# Source2: bls archive
# Original: https://github.com/codablock/bls-signatures
mkdir -p %{sourcetree}/depends/sources/
# ---- rpmlint hates the use of {_sourcedir}, therefore...
# OPTION 1 -- do it anyway...
#mv %%{_sourcedir}/%%{blsarchivename}.tar.gz %%{sourcetree}/depends/sources/v%%{blsarchivedate}.tar.gz
# OPTION 2 -- repack the archive...
# Man, there has to got be a better way.
#%%setup -q -T -D -a 2 -n %%{srcroot}
#tar czf %%{blsarchivename}.tar.gz %%{blsarchivename}
#mv %%{blsarchivename}.tar.gz %%{sourcetree}/depends/sources/v%%{blsarchivedate}.tar.gz
# Option 2 update: The build doesn't like me messing with the archive (it does
# an integrity check on the tarball). So, without editing the build scripts
# that's a no-go.
# OPTION 3 -- brute force method - so ugly...
# Moving the supplied tarball from SOURCES to the desired location
mv ../../SOURCES/%{blsarchivename}.tar.gz %{sourcetree}/depends/sources/v%{blsarchivedate}.tar.gz

# Source3: dashcore (binary)
%if %{clientSourceIsPrebuilt} || %{serverSourceIsPrebuilt}
%setup -q -T -D -a 3 -n %{srcroot}
%endif

%if ! %{clientSourceIsPrebuilt}
cd %{sourcetree}
%patch0 -p1
cd ..
%endif

#t0dd: Prep SELinux policy -- NOT USED YET
# Done here to prep for action taken in the %%build step
# At this moment, we are in the srcroot directory
mkdir -p selinux-tmp
cp -p %{srccontribtree}/linux/selinux/dash.{te,if,fc} selinux-tmp/

%if 0%{?buildFromSource:1}
  # pixmap contributions
  cp -a %{srccontribtree}/extras/pixmaps/*.??? %{sourcetree}/share/pixmaps/
  
  # Swap out packages.mk makefile in order to force usage of OS native devel
  # libraries and tools. Swap out chia_bls.mk because it asks for a dependency to
  # gmp that is satisfied via the OS (via BuildRequires) instead.
  cp -a %{srccontribtree}/build/depends/packages/*.mk %{sourcetree}/depends/packages/
%endif


%build
# This section starts us in directory {_builddir}/{srcroot}

%if %{clientSourceIsPrebuilt} && %{serverSourceIsPrebuilt}
  exit 0
%endif

cd %{sourcetree}

# build dependencies
cd depends
# example: make HOST=x86_64-redhat-linux-gnu -j4
make HOST=%{_target_platform} -j$(nproc)
cd ..

# build code
%define _targettree %{_builddir}/%{srcroot}/%{sourcetree}/depends/%{_target_platform}
%define _FLAGS CPPFLAGS="$CPPFLAGS -I%{_targettree}/include -I%{_includedir}" LDFLAGS="$LDFLAGS -L%{_targettree}/lib -L%{_libdir}"

%define _disable_tests --disable-tests --disable-gui-tests
%if %{testing_extras}
  %define _disable_tests %{nil}
%endif

./autogen.sh

%{_FLAGS} ./configure --libdir=%{_targettree}/lib --prefix=%{_targettree} --enable-reduce-exports %{_disable_tests} --disable-zmq
make 

cd ..

#t0dd Not using for now.
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
%if %{clientSourceIsPrebuilt} && %{serverSourceIsPrebuilt}
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
# This section starts us in directory {_builddir}/{srcroot}

%if 0%{?buildFromSource:1}
  cd %{sourcetree}
  # make install deploys to {_targettree}/ (defined in %%build)
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

%if 0%{?buildFromSource:1}
  mv %{_targettree}/bin/* %{buildroot}%{_bindir}/
  mv %{_targettree}/include/dash* %{buildroot}%{_includedir}/
  mv %{_targettree}/lib/libdash* %{buildroot}%{_libdir}/
  install -d -m755 -p %{buildroot}%{_libdir}/pkgconfig
  mv %{_targettree}/lib/pkgconfig/libdash* %{buildroot}%{_libdir}/pkgconfig/
%endif
%if %{clientSourceIsPrebuilt} && %{serverSourceIsPrebuilt}
  mv %{binarytree}/bin/* %{buildroot}%{_bindir}/
  mv %{binarytree}/include/dash* %{buildroot}%{_includedir}/
  mv %{binarytree}/lib/libdash* %{buildroot}%{_libdir}/
%else
  %if %{clientSourceIsPrebuilt}
    mv %{binarytree}/bin/dash-qt %{buildroot}%{_bindir}/
  %endif
  %if %{serverSourceIsPrebuilt}
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

# Man Pages (from contrib)
#install -D -m644 %%{srccontribtree}/linux/man/man1/* %%{buildroot}%%{_mandir}/man1/
install -D -m644 %{srccontribtree}/linux/man/man5/* %{buildroot}%{_mandir}/man5/
# Man Pages (from upstream) - likely to overwrite ones from contrib (which is fine)
install -D -m644 %{sourcetree}/doc/man/*.1* %{buildroot}%{_mandir}/man1/
%if %{clientSourceIsPrebuilt} || %{serverSourceIsPrebuilt}
  # probably the same. I haven't checked.
  install -D -m644 %{binarytree}/share/man/man1/*.1* %{buildroot}%{_mandir}/man1/
%endif
gzip -f %{buildroot}%{_mandir}/man1/*.1
gzip -f %{buildroot}%{_mandir}/man5/*.5

# Bash completion
install -D -m644 %{sourcetree}/contrib/dash-cli.bash-completion %{buildroot}%{_datadir}/bash-completion/completions/dash-cli
install -D -m644 %{sourcetree}/contrib/dash-tx.bash-completion %{buildroot}%{_datadir}/bash-completion/completions/dash-tx
install -D -m644 %{sourcetree}/contrib/dashd.bash-completion %{buildroot}%{_datadir}/bash-completion/completions/dashd

# Desktop elements - desktop file and kde protocol file (from contrib)
cd %{srccontribtree}/linux/desktop/
# dash-qt.desktop
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_desktop_files
install -m755  dash-qt.wrapper.sh %{buildroot}%{_bindir}/
desktop-file-install --dir=%{buildroot}%{_datadir}/applications dash-qt.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/dash-qt.desktop
# dash-qt.appdata.xml
# https://docs.fedoraproject.org/en-US/packaging-guidelines/AppData/
install -D -m644 -p dash-qt.appdata.xml %{buildroot}%{_metainfodir}/dash-qt.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

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
logtimestamps=1
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

# Not using for now.
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
%license %{sourcetree}/COPYING
%doc %{sourcetree}/doc/*.md %{srccontribtree}/extras/dash.conf.example
%{_bindir}/dash-qt
%{_bindir}/dash-qt.wrapper.sh
%{_datadir}/applications/dash-qt.desktop
%{_metainfodir}/dash-qt.appdata.xml
# XXX Removing this unless someone bitches
#%%{_datadir}/kde4/services/dash-qt.protocol
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
  %if 0%{?buildFromSource:1}
    %{_bindir}/test_dash-qt
  %endif
%endif


# dashcore-server
%files server
%defattr(-,root,root,-)
%license %{sourcetree}/COPYING
%doc %{sourcetree}/doc/*.md %{srccontribtree}/extras/dash.conf.example

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
%{_mandir}/man5/dash.conf.5.gz
%{_mandir}/man5/masternode.conf.5.gz
#t0dd %%{_datadir}/selinux/*/dash.pp

%if %{testing_extras}
  %if 0%{?buildFromSource:1}
    %{_bindir}/test_dash
    %{_bindir}/bench_dash
  %endif
%endif


# dashcore-libs
%files libs
%defattr(-,root,root,-)
%license %{sourcetree}/COPYING
%{_libdir}/*


# dashcore-devel
%files devel
%defattr(-,root,root,-)
%license %{sourcetree}/COPYING
%{_includedir}/*
%{_libdir}/*


# dashcore-utils
%files utils
%defattr(-,root,root,-)
%license %{sourcetree}/COPYING
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
#     test example: dash-0.14.0.0-rc1.tar.gz
#     release example: dash-0.14.0.0.tar.gz
#
# Dash Core git repos...
#   * Dash: https://github.com/dashpay/dash
#   * Sentinel: https://github.com/dashpay/sentinel

%changelog
* Fri Apr 05 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.0-0.2.rc3.taw
  - 0.14 rc3

* Thu Apr 04 2019 Todd Warner <t0dd_at_protonmail.com> 0.14.0.0-0.2.rc2.taw
  - vermajor and verminor shifted a decimal point
  - specfile cleanup
  - patch management more correct in the case building client from binaries
  - minor changes to prep for EL8 testing
  - adjustments to allow rp (repackaged) binary builds to work again.

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
