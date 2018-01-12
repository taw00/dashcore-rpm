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
# * dashcore-debuginfo
#
# Note about edits within the spec: Any comments beginning with #t0dd are
# associated to future work or experimental elements of this spec file and
# build.
#
# Note about RPM and commented out defined variables/macros in this (or any)
# spec file. You MUST break up the define declaration. Commenting it out is
# not good enough because... it is a macro, more than a variable. So, if you
# want to have a macro linger around, but want to disable it, either nil it
# out, undefine it, or break up the define like this "% define your_macro..."
# RPM is weird.
#
# Enjoy. Todd Warner <t0dd@protonmail.com>

%global selinux_variants mls strict targeted
%define testing_extras 0

# Usually want a debug package available and built. If you do not want them
# built, reconstruct this nil'ifying define below. It is deconstructed because
# RPM recognizes certain things, like defines, even if they are in commments.
#% define debug _package % { n i l }

# https://fedoraproject.org/wiki/Changes/Harden_All_Packages
%define _hardened_build 0

%define _name1 dash
%define _name2 dashcore
%define _version_major 0.12.2
%define _version_minor 3

# Note: "bump" and "bumptag" are release-build identifiers.
# Often the bumptag is undefined, the builder's initials, a date, or whatever.
# To undefine, flip-flop the define/undefine ordering

%define bump 0
%undefine bumptag
%define bumptag taw

%if %{?bumptag}
%define _release %{bump}.%{bumptag}
%else
%define _release %{bump}
%endif


Name: %{_name2}
Version: %{_version_major}.%{_version_minor}
Release: %{_release}%{?dist}
Vendor: Dash.org
Packager: Todd Warner <t0dd@protonmail.com>
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency

# upstream bitcoin team convention - v0.12.2 ...for example v0.12.2.tar.gz
%define _archivebasename0 v%{version}
# upstream dash team convention, github - dash-0.12.2.0 ...for example dash-0.12.2.0.tar.gz
%define _archivebasename1 %{_name1}-%{version}
# upstream dash team convention, bamboo - dashcore-0.12.2 ...for example dashcore-0.12.2.tar.gz
%define _archivebasename2 %{_name2}-%{_version_major}

# ...flipflop these rules for the build type...
# testing and rc builds...
%define archivebasename %{_archivebasename2}
# stable builds...
%define archivebasename %{_archivebasename1}

%define archivebasename_contrib %{_archivebasename2}-contrib

# the exploded tree of code in rpmbuild/BUILD/
# sourcetree is top dir
# dashtree and contribtree hang off of it
%define sourcetree %{_name2}-%{_version_major}
%define contribtree %{_archivebasename2}

# ...flipflop these rules for the build type...
# testing and rc builds...
%define dashtree %{_archivebasename2}
# stable builds...
%define dashtree %{_archivebasename1}


Group: Applications/System
License: MIT
URL: http://dash.org/
# upstream
Source0: %{archivebasename}.tar.gz

# Source archive of contributions not yet in main upstream package.
# Icons, manpages, desktop stuff, systemd stuff, etc.
# includes some future SELinux policy stuff as well (.te, .if, .fc)
Source1: %{archivebasename_contrib}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: gcc-c++
BuildRequires: qt5-qtbase-devel qt5-linguist
BuildRequires: qrencode-devel miniupnpc-devel protobuf-devel openssl-devel
BuildRequires: desktop-file-utils autoconf automake
#BuildRequires: checkpolicy selinux-policy-devel selinux-policy-doc
BuildRequires: boost-devel libdb4-cxx-devel libevent-devel
BuildRequires: libtool java

# I don't think this check is needed anymore -comment out for now. -t0dd
## ZeroMQ not testable yet on RHEL due to lack of python3-zmq so
## enable only for Fedora
#%if 0%{?fedora}
#BuildRequires: python3-zmq zeromq-devel
#%endif

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
#t0dd Requires: selinux-policy
#t0dd Requires: policycoreutils-python
Requires: openssl-libs
Requires: dashcore-utils = %{version}-%{release}
Requires: dashcore-sentinel


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
This package provides libdashconsensus, which is used by third party
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
compile programs which use libdashconsensus.

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
#%setup -q -n %{sourcetree}
%setup -q -T -a 0 -c %{sourcetree}
# extra contributions - Source1
#%setup -q -T -D -b 1 -n %{sourcetree}
%setup -q -T -D -a 1
# Patch addressed by removing one dir path level (-p1)
#%patch0 -p1

# Install README files
#t0dd cp -p %{SOURCE8} %{SOURCE9} %{SOURCE10} .

# Prep SELinux policy -- XXX NOT USED YET
# Done here because action is taken in the %build step
#mkdir -p %{sourcetree}/SELinux
# At this moment, we are in the sourcetree directory
mkdir -p SELinux
cp -p %{contribtree}/contrib/linux/selinux/dash.{te,if,fc} SELinux

# We leave with this structure (for example)...
# ~/rpmbuild/BUILD/dashcore-0.12.2/dash-0.12.2.3/
# ~/rpmbuild/BUILD/dashcore-0.12.2/dashcore-0.12.2/contrib/...
# ...unless we are using the bamboo nomenclature...
# ~/rpmbuild/BUILD/dashcore-0.12.2/dashcore-0.12.2/
# ~/rpmbuild/BUILD/dashcore-0.12.2/dashcore-0.12.2/contrib/...


%build
# Building in dashcore-X.Y.Z
# But we need to cd into dashcore-X.Y.Z/dash-X.Y.Z.zz
# ...unless we are using the bamboo nomenclature...
# But we need to cd into dashcore-X.Y.Z/dashcore-X.Y.Z

# We start in sourcetree (dashcore-X.Y.Z)
# cd into dashcore-X.Y.Z/dash-X.Y.Z.zz
cd %{dashtree}
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

# Exit from sourcetree/<the dash tree>
cd ..


%check
cd %{dashtree}
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
rm -rf %{buildroot}
mkdir %{buildroot}

# We start in sourcetree, i.e. dashcore-0.12.2, we need to cd into the dashtree
cd %{dashtree}
make INSTALL="install -p" CP="cp -p" DESTDIR=%{buildroot} install
cd ..

# TODO: Upstream puts dashd in the wrong directory. Need to fix the
# upstream Makefiles to relocate it.
#mkdir -p -m755 %{buildroot}%{_sbindir}
#mv %{buildroot}%{_bindir}/dashd %{buildroot}%{_sbindir}/dashd
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

# Man Pages (from contrib)
cd %{contribtree}
install -d %{buildroot}%{_mandir}/man1
install -D -m644 ./contrib/linux/man/man1/* %{buildroot}%{_mandir}/man1/
gzip %{buildroot}%{_mandir}/man1/dashd.1
gzip %{buildroot}%{_mandir}/man1/dash-qt.1
install -d %{buildroot}%{_mandir}/man5
install -D -m644 ./contrib/linux/man/man5/* %{buildroot}%{_mandir}/man5/
gzip %{buildroot}%{_mandir}/man5/dash.conf.5
gzip %{buildroot}%{_mandir}/man5/masternode.conf.5
cd ..

# Desktop elements - desktop file and kde protocol file (from contrib)
cd %{contribtree}
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
cd ..

# Misc pixmaps - unsure if they are even used... (from contrib)
cd %{contribtree}
install -d %{buildroot}%{_datadir}/pixmaps
install -D -m644 ./contrib/extras/pixmaps/* %{buildroot}%{_datadir}/pixmaps/
cd ..

# TESTING ONLY: For test releases, uncomment the next line
#desktop-file-validate %{buildroot}%{_datadir}/applications/dash-qt.desktop

# Install that dated dash.conf.example document (from contrib)
cd %{contribtree}
# TODO: need masternode.conf example also... or just update the man page?
# Note: doesn't need to be in buildroot I don't think.
install -D -m644 ./contrib/extras/dash.conf.example doc/dash.conf.example
cd ..

# Install default configuration file (from contrib)
cd %{contribtree}
install -D -m640 ./contrib/linux/systemd/etc-dashcore_dash.conf %{buildroot}%{_sysconfdir}/dashcore/dash.conf
cd ..

# Install system services files (from contrib)
cd %{contribtree}
install -D -m600 -p ./contrib/linux/systemd/etc-sysconfig_dashd %{buildroot}%{_sysconfdir}/sysconfig/dashd
install -d %{buildroot}%{_sysconfdir}/sysconfig/dashd-scripts
install -D -m755 -p ./contrib/linux/systemd/etc-sysconfig-dashd-scripts_dashd.send-email.sh %{buildroot}%{_sysconfdir}/sysconfig/dashd-scripts/dashd.send-email.sh
install -D -m644 -p ./contrib/linux/systemd/usr-lib-systemd-system_dashd.service %{buildroot}%{_unitdir}/dashd.service
install -D -m644 -p ./contrib/linux/systemd/usr-lib-tmpfiles.d_dashd.conf %{buildroot}%{_tmpfilesdir}/dashd.conf
# ...logrotate file rules
install -D -m644 -p ./contrib/linux/logrotate/etc-logrotate.d_dashcore %{buildroot}/etc/logrotate.d/dashcore
# ...ghosting a log file - we have to own the log file
#install -d %{buildroot}%{_sharedstatedir}/dashcore # already created above
install -d %{buildroot}%{_sharedstatedir}/dashcore/testnet3
touch %{buildroot}%{_sharedstatedir}/dashcore/debug.log
touch %{buildroot}%{_sharedstatedir}/dashcore/testnet3/debug.log
cd ..


# Service definition files for firewalld for full nodes and masternodes (from contrib)
cd %{contribtree}
install -D -m644 -p ./contrib/linux/firewalld/usr-lib-firewalld-services_dashcore.xml %{buildroot}%{_prefix}/lib/firewalld/services/dashcore.xml
install -D -m644 -p ./contrib/linux/firewalld/usr-lib-firewalld-services_dashcore-testnet.xml %{buildroot}%{_prefix}/lib/firewalld/services/dashcore-testnet.xml
install -D -m644 -p ./contrib/linux/firewalld/usr-lib-firewalld-services_dashcore-rpc.xml %{buildroot}%{_prefix}/lib/firewalld/services/dashcore-rpc.xml
install -D -m644 -p ./contrib/linux/firewalld/usr-lib-firewalld-services_dashcore-testnet-rpc.xml %{buildroot}%{_prefix}/lib/firewalld/services/dashcore-testnet-rpc.xml
cd ..

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
%license %{dashtree}/COPYING
%doc %{dashtree}/doc/*.md %{contribtree}/contrib/extras/dash.conf.example
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
%config(noreplace) %attr(640,dashcore,dashcore) %{_sysconfdir}/dashcore/dash.conf

%if %{testing_extras}
%{_bindir}/test_dash-qt
%endif


# dashcore-server
%files server
%defattr(-,root,root,-)
%license %{dashtree}/COPYING
%doc %{dashtree}/doc/*.md %{contribtree}/contrib/extras/dash.conf.example
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore/testnet3
%dir %attr(750,dashcore,dashcore) %{_sysconfdir}/dashcore
%dir %attr(755,dashcore,dashcore) %{_sysconfdir}/sysconfig/dashd-scripts
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/sysconfig/dashd
%attr(755,root,root) %{_sysconfdir}/sysconfig/dashd-scripts/dashd.send-email.sh
%config(noreplace) %attr(640,dashcore,dashcore) %{_sysconfdir}/dashcore/dash.conf
# Log files - they don't initially exist, but we still own them
%ghost %{_sharedstatedir}/dashcore/debug.log
%ghost %{_sharedstatedir}/dashcore/testnet3/debug.log
%attr(644,root,root) /etc/logrotate.d/dashcore
%{_unitdir}/dashd.service
%{_prefix}/lib/firewalld/services/dashcore.xml
%{_prefix}/lib/firewalld/services/dashcore-testnet.xml
%{_prefix}/lib/firewalld/services/dashcore-rpc.xml
%{_prefix}/lib/firewalld/services/dashcore-testnet-rpc.xml
%doc SELinux/*
%{_sbindir}/dashd
%{_tmpfilesdir}/dashd.conf
%{_mandir}/man1/dashd.1.gz
%{_mandir}/man5/dash.conf.5.gz
%{_mandir}/man5/masternode.conf.5.gz
#t0dd %{_datadir}/selinux/*/dash.pp

%if %{testing_extras}
%{_bindir}/test_dash
%{_bindir}/bench_dash
%endif


# dashcore-libs
%files libs
%defattr(-,root,root,-)
%license %{dashtree}/COPYING
%{_libdir}/libdashconsensus.so*


# dashcore-devel
%files devel
%defattr(-,root,root,-)
%license %{dashtree}/COPYING
%{_includedir}/dashconsensus.h
%{_libdir}/libdashconsensus.a
%{_libdir}/libdashconsensus.la
%{_libdir}/pkgconfig/libdashconsensus.pc


# dashcore-utils
%files utils
%defattr(-,root,root,-)
%license %{dashtree}/COPYING
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
# Source snapshots...
#   * Tagged release builds: https://github.com/dashpay/dash/tags
#     dash-0.12.2.3.tar.gz
#   * Test builds...
#     dashcore-0.12.2.tar.gz
#     https://bamboo.dash.org/browse/DASHL-REL/latestSuccessful
#     Then > Artifacts > gitian-linux-dash-src > [download the tar.gz file]
#
# Dash Core git repos...
#   * Dash: https://github.com/dashpay/dash
#   * Sentinel: https://github.com/dashpay/sentinel
#
# The last testnet effort...
#   * Announcement: https://www.dash.org/forum/threads/v12-2-testing.17412/
#              old: https://www.dash.org/forum/threads/12.1-testnet-testing-phase-two-ignition.10818/
#   * Documentation: https://dashpay.atlassian.net/wiki/display/DOC/Testnet

%changelog
* Thu Jan 11 2018 Todd Warner <t0dd@protonmail.com> 0.12.2.3-0.taw
- Release - e596762
- 5347351483ce39d1dd0be4d93ee19aba1a6b02bc7f90948b4eea4466ad79d1c3 dash-0.12.2.3.tar.gz
- b09f09d847e02e1509dd157aca1655bbe5ca79106fe4cf2e4370228e0eab79e3 dashcore-0.12.2-contrib.tar.gz
- https://github.com/dashpay/dash/releases/tag/v0.12.2.3
-
* Tue Dec 19 2017 Todd Warner <t0dd@protonmail.com> 0.12.2.2-0.taw
- Release - 8506678
- fd5f1576bc8ef70e5823f665b86a334937813e300f037a03bcd127b83773d771 dash-0.12.2.2.tar.gz
- b09f09d847e02e1509dd157aca1655bbe5ca79106fe4cf2e4370228e0eab79e3 dashcore-0.12.2-contrib.tar.gz
- https://github.com/dashpay/dash/releases/tag/v0.12.2.2
-
* Sun Nov 12 2017 Todd Warner <t0dd@protonmail.com> 0.12.2.1-0.taw
- Release - 20bacfa
- ae2e96ea685d9aa3b442acff986b096659a1d2c6dfd2ef9deef84d75fe2cf2b0 dash-0.12.2.1.tar.gz
- b09f09d847e02e1509dd157aca1655bbe5ca79106fe4cf2e4370228e0eab79e3 dashcore-0.12.2-contrib.tar.gz
- https://github.com/dashpay/dash/releases/tag/v0.12.2.1
-
* Wed Nov 8 2017 Todd Warner <t0dd@protonmail.com> 0.12.2.0-0.taw
- Release 12.2 - ec8178c
- 2e0c20c64f5ccc392e51373761f16384642d224587f10c2fdcdbb4f17e185c04 dash-0.12.2.0.tar.gz
- b09f09d847e02e1509dd157aca1655bbe5ca79106fe4cf2e4370228e0eab79e3 dashcore-0.12.2-contrib.tar.gz
- https://github.com/dashpay/dash/releases/tag/v0.12.2.0
-
* Tue Apr 11 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.5-0.taw
- Fixes a watchdog propagation issue.
- 4e52b2427f1ea46f0ff5b31b0dd044478fba6a076611a97a9c2d3d345374459f  dash-0.12.1.5.tar.gz
- e3e4351656afda2ff23cb142d264af4b4d04d0bbe9f3326ce24019423f6adf94  dashcore-0.12.1-contrib.tar.gz
- https://github.com/dashpay/dash/releases/tag/v0.12.1.5
-
* Wed Mar 22 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.4-0.taw
- Added RPC port to available firewalld services.
- Renamed firewalld services to match bitcoin's firewalld service name taxonomies.
- 7218baaa1aa8052960ffc0c36904b6f5647256f9773c17e8506be37a2d3cc0cb  dash-0.12.1.4.tar.gz
- e3e4351656afda2ff23cb142d264af4b4d04d0bbe9f3326ce24019423f6adf94  dashcore-0.12.1-contrib.tar.gz
- https://github.com/dashpay/dash/releases/tag/v0.12.1.4
- 
* Sat Mar 04 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.3-1.taw
- Brought back the test scripts (most of them), made them conditional. Added
- back and adjusted build-requires for openssl-compat that uses our own
- openssl-compat builds. Test scripts / openssl-compat seem to only work for
- very old linux--CentOS7/RHEL7 Ie. I have more work to do to make them part of
- the build.
-
- "bumptag" now can be defined or undefined and we do the right thing.
- 
* Thu Mar 02 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.3-0.taw
- Release 0.12.1.3 - 119fe83
- Announcement: https://github.com/dashpay/dash/releases/tag/v0.12.1.3
- 1f6e6fb528151c8703019ed1511562b0c8bc91fe8c7ac6838a3811ffd1af288a  dash-0.12.1.3.tar.gz
- d4c0f01ea5fa017f6362269495d2cd32e724d9e4d2e584bf5e9a0057b493dfbb  dashcore-0.12.1-contrib.tar.gz
-
* Fri Feb 24 2017 Todd Warner <t0dd@protonmail.com> 0.12.1.2-0.taw
- Release 0.12.1.2 - a1ef547
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
