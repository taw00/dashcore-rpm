# Dash (digital cash) cryptocurrency spec file
#
# This is the source spec for building Dash GUI Wallet, Masternode, and Full
# Node. Dash Masternode Sentinel is built with another spec file.
#
# Consumer facing...
# * dashcore-client
# * dashcore-server
# * dashcore-utils
#
# Specialized...
# * dashcore-libs
# * dashcore-devel
# 
# Note about edits within the spec: Any comments beginning with #t0dd are
# associated to future work or experimental elements of this spec file and
# build.
#
# Enjoy. Todd Warner <t0dd@protonmail.com>

%global selinux_variants mls strict targeted

# To produce a dashcore-debuginfo package:
#   1. Comment out this define
#   2. Separate the %'s from their variable (this screws things up)
# Otherwise, leave it uncommented
%define debug_package %{nil}
# https://fedoraproject.org/wiki/Changes/Harden_All_Packages
#%define _hardened_build 0

# "bump" refers to "release bump" and is a build identifier.
%define bump 0

# "bumptag" is used to indicate additional information, usually an identifier,
# like the builder's initials, or a date, or both, or nil.
%define bumptag taw
#% define bumptag %{nil}

%define _name dashcore
%define _version_major 0.12.1
%define _version_minor 0
%define _release %{bump}.%{bumptag}

Name: %{_name}
Version: %{_version_major}.%{_version_minor}
Release: %{_release}%{?dist}
Vendor: Dash.org
Packager: Todd Warner <t0dd@protonmail.com>
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency

# upstream bitcoin team convention - v0.12.1
# upstream dash team convention - dashcore-0.12.1
#%define archivebasename v%{version}
%define archivebasename %{_name}-%{_version_major}
%define sourcetree %{_name}-%{_version_major}

Group: Applications/System
License: MIT
URL: http://dash.org/
# upstream
Source0: %{archivebasename}.tar.gz

# Source archive of contributions not yet in main upstream package.
# dashd.tmpfiles, dash.sysconfig, dash.service, dash.init(never used?), etc.
# Icons, manpages, desktop stuff, etc.
# includes some future SELinux policy stuff as well (.te, .if, .fc)
Source1: %{archivebasename}-contrib.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: gcc-c++
BuildRequires: qt5-qtbase-devel qt5-linguist
BuildRequires: qrencode-devel miniupnpc-devel protobuf-devel openssl-devel
BuildRequires: desktop-file-utils autoconf automake
#BuildRequires: checkpolicy selinux-policy-devel selinux-policy-doc
BuildRequires: boost-devel libdb4-cxx-devel libevent-devel
BuildRequires: libtool java

# ZeroMQ not testable yet on RHEL due to lack of python3-zmq so
# enable only for Fedora
%if 0%{?fedora}
BuildRequires: python3-zmq zeromq-devel
%endif

# Python tests still use OpenSSL for secp256k1, so we still need this to run
# the testsuite on RHEL7, until Red Hat fixes OpenSSL on RHEL7. It has already
# been fixed on Fedora. Bitcoin itself no longer needs OpenSSL for secp256k1.
%if 0%{?rhel}
# via the bitcoin repos, see https://linux.ringingliberty.com/bitcoin/
BuildRequires: openssl-compat-bitcoin-libs
BuildRequires: python34
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
#t0dd Requires: selinux-policy
#t0dd Requires: policycoreutils-python
Requires: openssl-libs
#Requires: dashcore-utils%{?_isa} = %{version}-%{_release}
#Requires: dashcore-utils = %{version}-%{_release}
#Requires: dashcore-utils = %{version}
Requires: dashcore-utils = %{version}-%{release}
Requires: dashcore-sentinel


# dashcore-libs
%package libs
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (consensus libraries)


# dashcore-devel
%package devel
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (dev libraries and headers)
#Requires: dashcore-libs%{?_isa} = %{version}-%{_release}
#Requires: dashcore-libs = %{version}-%{_release}
Requires: dashcore-libs = %{version}-%{release}


# dashcore-utils
%package utils
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (commandline utils)



# dashcore SRPM
%description
This is the source package for building most of the Dash Core set of binary
packages.  It will build dashcore-{client,server,utils,libs,devel,debuginfo}.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.



# dashcore-client
%description client
This package provides dash-qt, a user-friendly GUI wallet manager for personal
use. This package requires the dashcore-utils RPM package to be installed as
well.


Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.


# dashcore-server
%description server
This package provides dashd, a peer-to-peer node and wallet server. It is the
command line installation without a GUI. It can be used as a commandline wallet
but is typically used to run a Dash Full Node or Masternode. This package
requires the dashcore-utils and dashcore-sentinel RPM packages to be installed.

Please refer to Dash Core documentation at dash.org for more information about
running a Masternode.

-

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

A Dash Full Node is a un-collatoralized member of a decentralized network of
servers that validate transactions and blocks. A Dash Masternode is a member
of a network of incentivized servers that perform expanded critical services
for the Dash cryptocurrency protocol.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.


# dashcore-libs
%description libs
This package provides libbitcoinconsensus, which is used by third party
applications to verify scripts (and other functionality in the future).

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.


# dashcore-devel
%description devel
This package provides the libraries and header files necessary to
compile programs which use libbitcoinconsensus.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.


# dashcore-utils
%description utils
This package provides dash-cli, a utility to communicate with and
control a Dash server via its RPC protocol, and dash-tx, a utility
to create custom Dash transactions.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.



%prep
# dash upstream stuff
%setup -q -n %{sourcetree}
# extra contributions - Source1
%setup -q -T -D -b 1 -n %{sourcetree}
# Patch addressed by removing one dir path level (-p1)
#%patch0 -p1

# Install README files
#t0dd cp -p %{SOURCE8} %{SOURCE9} %{SOURCE10} .

# Prep SELinux policy -- XXX NOT USED YET
# Done here because action is taken in the %build step
mkdir -p SELinux
cp -p ./contrib/linux/selinux/dash.{te,if,fc} SELinux

%build
# Build Dash
./autogen.sh
%configure --enable-reduce-exports --enable-glibc-back-compat

make %{?_smp_mflags}

#t0dd # Build SELinux policy
#t0dd pushd SELinux
#t0dd for selinuxvariant in %{selinux_variants}
#t0dd do
#t0dd # FIXME: Create and debug SELinux policy
#t0dd   make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
#t0dd   mv dash.pp dash.pp.${selinuxvariant}
#t0dd   make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
#t0dd done
#t0dd popd


%check
# Run all the tests
#t0dd make check
#t0dd # Run all the other tests
#t0dd pushd src
#t0dd srcdir=. test/dashcore-util-test.py
#t0dd popd
#t0dd LD_LIBRARY_PATH=/opt/openssl-compat-dash/lib PYTHONUNBUFFERED=1  qa/pull-tester/rpc-tests.py -extended


%install
rm -rf %{buildroot}
mkdir %{buildroot}

make INSTALL="install -p" CP="cp -p" DESTDIR=%{buildroot} install

# TODO: Upstream puts dashd in the wrong directory. Need to fix the
# upstream Makefiles to relocate it.
#mkdir -p -m755 %{buildroot}%{_sbindir}
#mv %{buildroot}%{_bindir}/dashd %{buildroot}%{_sbindir}/dashd
install -d -m755 -p %{buildroot}%{_sbindir}
install -D -m755 -p %{buildroot}%{_bindir}/dashd %{buildroot}%{_sbindir}/dashd
rm -f %{buildroot}%{_bindir}/dashd

# Remove the test binaries
# TESTING ONLY: For test releases, comment the next two lines
rm -f %{buildroot}%{_bindir}/test_*
rm -f %{buildroot}%{_bindir}/bench_dash


# Install / config ancillary files
# Cheatsheet for macros:
#   %{_datadir} = /usr/share
#   %{_mandir} = /usr/share/man
#   %{_sysconfdir} = /etc
#   %{_localstatedir} = /var
#   %{_sharedstatedir} is /var/lib
#   %{_prefix} = /usr
#   %{_tmpfilesdir} = /usr/lib/tmpfiles.d
#   %{_unitdir} = /usr/lib/systemd/system
#   %{_libdir} = /usr/lib or /usr/lib64 (depending on system)
#   https://fedoraproject.org/wiki/Packaging:RPMMacros
install -d %{buildroot}%{_datadir}
install -d %{buildroot}%{_mandir}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_localstatedir}
install -d %{buildroot}%{_sharedstatedir}
install -d %{buildroot}%{_prefix}
install -d %{buildroot}%{_tmpfilesdir}
install -d %{buildroot}%{_unitdir}

install -d -m750 -p %{buildroot}%{_sysconfdir}/dashcore
install -d -m750 -p %{buildroot}%{_sharedstatedir}/dashcore

# Man Pages
install -d %{buildroot}%{_mandir}/man1
install -D -m644 ./contrib/linux/man/man1/* %{buildroot}%{_mandir}/man1/
gzip %{buildroot}%{_mandir}/man1/dashd.1
gzip %{buildroot}%{_mandir}/man1/dash-qt.1
install -d %{buildroot}%{_mandir}/man5
install -D -m644 ./contrib/linux/man/man5/* %{buildroot}%{_mandir}/man5/
gzip %{buildroot}%{_mandir}/man5/dash.conf.5
gzip %{buildroot}%{_mandir}/man5/masternode.conf.5

# Desktop elements - desktop file and kde protocol file
install -D -m644 ./contrib/linux/desktop/dash-qt.desktop %{buildroot}%{_datadir}/applications/dash-qt.desktop
install -D -m644 ./contrib/linux/desktop/usr-share-kde4-services_dash-qt.protocol %{buildroot}%{_datadir}/kde4/services/dash-qt.protocol
# Desktop elements - hicolor icons
install -D -m644 ./contrib/linux/desktop/dash-hicolor-128.png      %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-hicolor-16.png       %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-hicolor-22.png       %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-hicolor-24.png       %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-hicolor-256.png      %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-hicolor-32.png       %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-hicolor-48.png       %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-hicolor-scalable.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/dash.svg
# Desktop elements - HighContrast icons
install -D -m644 ./contrib/linux/desktop/dash-HighContrast-128.png      %{buildroot}%{_datadir}/icons/HighContrast/128x128/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-HighContrast-16.png       %{buildroot}%{_datadir}/icons/HighContrast/16x16/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-HighContrast-22.png       %{buildroot}%{_datadir}/icons/HighContrast/22x22/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-HighContrast-24.png       %{buildroot}%{_datadir}/icons/HighContrast/24x24/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-HighContrast-256.png      %{buildroot}%{_datadir}/icons/HighContrast/256x256/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-HighContrast-32.png       %{buildroot}%{_datadir}/icons/HighContrast/32x32/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-HighContrast-48.png       %{buildroot}%{_datadir}/icons/HighContrast/48x48/apps/dash.png
install -D -m644 ./contrib/linux/desktop/dash-HighContrast-scalable.svg %{buildroot}%{_datadir}/icons/HighContrast/scalable/apps/dash.svg

# Misc pixmaps - unsure if they are even used...
install -d %{buildroot}%{_datadir}/pixmaps
install -D -m644 ./contrib/extras/pixmaps/* %{buildroot}%{_datadir}/pixmaps/

# TESTING ONLY: For test releases, uncomment the next line
#desktop-file-validate %{buildroot}%{_datadir}/applications/dash-qt.desktop

# Install that dated dash.conf.example document
# TODO: need masternode.conf example also... or just update the man page?
# Note: doesn't need to be in buildroot I don't think.
install -D -m644 ./contrib/extras/dash.conf.example doc/dash.conf.example

# Install default configuration file
install -D -m640 ./contrib/linux/systemd/etc-dashcore_dash.conf %{buildroot}%{_sysconfdir}/dashcore/dash.conf

# Install system services files
install -D -m600 -p ./contrib/linux/systemd/etc-sysconfig_dashd %{buildroot}%{_sysconfdir}/sysconfig/dashd
install -D -m644 -p ./contrib/linux/systemd/usr-lib-systemd-system_dashd.service %{buildroot}%{_unitdir}/dashd.service
install -D -m644 -p ./contrib/linux/systemd/usr-lib-tmpfiles.d_dashcore.conf %{buildroot}%{_tmpfilesdir}/dashcore.conf
# ...logrotate file rules
install -D -m644 -p ./contrib/linux/logrotate/etc-logrotate.d_dashcore %{buildroot}/etc/logrotate.d/dashcore
# ...ghosting a log file - we have to own the log file
#install -d %{buildroot}%{_sharedstatedir}/dashcore # already created above
install -d %{buildroot}%{_sharedstatedir}/dashcore/testnet3
touch %{buildroot}%{_sharedstatedir}/dashcore/debug.log
touch %{buildroot}%{_sharedstatedir}/dashcore/testnet3/debug.log


# Service definition files for firewalld for full nodes and masternodes
install -D -m644 -p ./contrib/linux/firewalld/usr-lib-firewalld-services_dashcore-node.xml %{buildroot}%{_prefix}/lib/firewalld/services/dashcore-node.xml
install -D -m644 -p ./contrib/linux/firewalld/usr-lib-firewalld-services_dashcore-node-testnet.xml %{buildroot}%{_prefix}/lib/firewalld/services/dashcore-node-testnet.xml

#t0dd # Install SELinux policy
#t0dd for selinuxvariant in %{selinux_variants}
#t0dd do
#t0dd 	install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
#t0dd 	install -p -m 644 SELinux/dash.pp.${selinuxvariant} \
#t0dd 		%{buildroot}%{_datadir}/selinux/${selinuxvariant}/dash.pp
#t0dd donex


%clean
rm -rf %{buildroot}


# dashcore-client
%post client
# firewalld only partially picks up changes to its services files without this
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

# dashcore-server
%pre server
# This is for the case that you run dash core as a service (systemctl start dash)
# %{_sharedstatedir} is /var/lib
getent group dashcore >/dev/null || groupadd -r dashcore
getent passwd dashcore >/dev/null || useradd -r -g dashcore -d %{_sharedstatedir}/dashcore -s /sbin/nologin -c "System user 'dashcore' to isolate Dash Core execution" dashcore
exit 0


# dashcore-server
%post server
%systemd_post dashd.service
# firewalld only partially picks up changes to its services files without this
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

#t0dd for selinuxvariant in %{selinux_variants}
#t0dd do
#t0dd 	/usr/sbin/semodule -s ${selinuxvariant} -i \
#t0dd 		%{_datadir}/selinux/${selinuxvariant}/dash.pp \
#t0dd 		&> /dev/null || :
#t0dd done
#t0dd # FIXME This is less than ideal, but until dwalsh gives me a better way...
#t0dd /usr/sbin/semanage port -a -t dash_port_t -p tcp 8332
#t0dd /usr/sbin/semanage port -a -t dash_port_t -p tcp 8333
#t0dd /usr/sbin/semanage port -a -t dash_port_t -p tcp 18332
#t0dd /usr/sbin/semanage port -a -t dash_port_t -p tcp 18333
#t0dd /sbin/fixfiles -R dashcore-server restore &> /dev/null || :
#t0dd /sbin/restorecon -R %{_sharedstatedir}/dashcore || :


# dashcore-server
%posttrans server
/usr/bin/systemd-tmpfiles --create


# dashcore-server
%preun server
%systemd_preun dashd.service


# dashcore-server
%postun server
%systemd_postun dashd.service
#t0dd# Do this upon uninstall (not upgrades)
#t0dd if [ $1 -eq 0 ] ; then
#t0dd 	# FIXME This is less than ideal, but until dwalsh gives me a better way...
#t0dd 	/usr/sbin/semanage port -d -p tcp 8332
#t0dd 	/usr/sbin/semanage port -d -p tcp 8333
#t0dd 	/usr/sbin/semanage port -d -p tcp 18332
#t0dd 	/usr/sbin/semanage port -d -p tcp 18333
#t0dd 	for selinuxvariant in %{selinux_variants}
#t0dd 	do
#t0dd 		/usr/sbin/semodule -s ${selinuxvariant} -r dash \
#t0dd 		&> /dev/null || :
#t0dd 	done
#t0dd 	/sbin/fixfiles -R dashcore-server restore &> /dev/null || :
#t0dd 	[ -d %{_sharedstatedir}/dashcore ] && \
#t0dd 		/sbin/restorecon -R %{_sharedstatedir}/dashcore \
#t0dd 		&> /dev/null || :
#t0dd fi



# dashcore-client
%files client
%defattr(-,root,root,-)
%license COPYING
#t0dd %doc README.md README.server.redhat 
%doc doc/assets-attribution.md doc/multiwallet-qt.md doc/release-notes.md doc/tor.md doc/keepass.md contrib/extras/dash.conf.example
%{_bindir}/dash-qt
%{_datadir}/applications/dash-qt.desktop
%{_datadir}/kde4/services/dash-qt.protocol
%{_datadir}/pixmaps/*
%{_datadir}/icons/*
%{_mandir}/man1/dash-qt.1.gz
%{_mandir}/man5/masternode.conf.5.gz
%{_prefix}/lib/firewalld/services/dashcore-node.xml
%{_prefix}/lib/firewalld/services/dashcore-node-testnet.xml
%config(noreplace) %attr(640,dashcore,dashcore) %{_sysconfdir}/dashcore/dash.conf

# TESTING ONLY: For test releases, uncomment the test binaries.
#%{_bindir}/test_dash-qt


# dashcore-server
%files server
%defattr(-,root,root,-)
%license COPYING
#t0dd %doc README.md README.server.redhat 
%doc doc/dnsseed-policy.md doc/release-notes.md doc/tor.md doc/multiwallet-qt.md doc/guide-startmany.md doc/reduce-traffic.md doc/zmq.md doc/dash.conf.example
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore/testnet3
%dir %attr(750,dashcore,dashcore) %{_sysconfdir}/dashcore
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/sysconfig/dashd
%config(noreplace) %attr(640,dashcore,dashcore) %{_sysconfdir}/dashcore/dash.conf
# Log files - they don't initially exist, but we still own them
%ghost %{_sharedstatedir}/dashcore/debug.log
%ghost %{_sharedstatedir}/dashcore/testnet3/debug.log
%attr(644,root,root) /etc/logrotate.d/dashcore
%{_unitdir}/dashd.service
%{_prefix}/lib/firewalld/services/dashcore-node.xml
%{_prefix}/lib/firewalld/services/dashcore-node-testnet.xml
%doc SELinux/*
%{_sbindir}/dashd
%{_tmpfilesdir}/dashcore.conf
%{_mandir}/man1/dashd.1.gz
%{_mandir}/man5/dash.conf.5.gz
%{_mandir}/man5/masternode.conf.5.gz
#t0dd %{_datadir}/selinux/*/dash.pp

# TESTING ONLY: For test releases, uncomment the test binaries.
#%{_bindir}/test_dash
#%{_bindir}/bench_dash


# dashcore-libs
%files libs
%defattr(-,root,root,-)
%license COPYING
#t0dd %doc README.md
%{_libdir}/libbitcoinconsensus.so*


# dashcore-devel
%files devel
%defattr(-,root,root,-)
%license COPYING
#t0dd %doc README.md
%{_includedir}/bitcoinconsensus.h
%{_libdir}/libbitcoinconsensus.a
%{_libdir}/libbitcoinconsensus.la
%{_libdir}/pkgconfig/libbitcoinconsensus.pc


# dashcore-utils
%files utils
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/dash-cli
%{_bindir}/dash-tx


# Dash Core Information
# 
# Dash...
#   * Project website: https://www.dash.org
#
# Dash Core on Fedora/CentOS/RHEL...
#   * Git Repo: https://github.com/taw00/dashcore-rpm
#   * Documentation: https://github.com/taw00/dashcore-rpm/tree/master/documentation
#
# The last testnet effort...
#   * Announcement: https://www.dash.org/forum/threads/12-1-testnet-testing-phase-two-ignition.10818/
#   * Documentation: https://dashpay.atlassian.net/wiki/display/DOC/Testnet
#
# Source snapshots...
#   * Tagged release builds: https://github.com/dashpay/dash/tags
#   * Test builds...
#     https://bamboo.dash.org/browse/DASHL-DEV/latestSuccessful
#     https://bamboo.dash.org/browse/DASHL-DEV-<BUILD_NUMBER>/artifact/JOB1/gitian-linux-dash-src/src
#     https://bamboo.dash.org/artifact/DASHL-DEV/JOB1/build-<BUILD_NUMBER>/gitian-linux-dash-src/src/dashcore-0.12.1.tar.gz
#
# Dash Core git repos...
#   * Dash: https://github.com/dashpay/dash
#   * Sentinel: https://github.com/dashpay/sentinel

%changelog
* Sun Feb 05 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.0-0.taw
- v12.1 GA
-
