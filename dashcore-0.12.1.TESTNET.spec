# Dash (digital cash) cryptocurrency spec file
#
# Note, anything with #taw commenting it out is my attempt to block off
# troublesome, or inappropriate stuff that came over from the bitcoin.spec
# file that this is based off of. Some things, like the SELinux elements
# will likely be brought back in when I get a moment.
#
# Enjoy. -taw, aka Todd Warner, Fall 2016

%define _hardened_build 1
%global selinux_variants mls strict targeted
# Comment out the next line if you want to produce a dashcore-debuginfo package.
#% define debug_package % {nil}

# Release bump is the base release number - or it is a build identifier
# It's called a "bump" becoes we tend to "bump" this often.
# For experimental builds, just make it a date 20160405, or 20160405.0,
# 20160405.1, 20160405.2, 20160406.0, etc
# The DashCore builds tend to look something like this: b9bd116
%define bump b9bd116
# Release bumptag (builder's initials or a date or both or nil)
%define bumptag .taw_TESTNET20160926
#% define bumptag %{nil}
# ...the release bumptag is used to convey information about who built the
# package (or other extra information) and is really only useful during early
# spins of the RPMs. For example, ".taw" is a reference to the original
# packager, Todd Warner (his initials).
# For actual releases, you may want to NIL the value above
%define _release %{bump}%{bumptag}

%define _name dash
Name: dashcore
Version: 0.12.1
Release: %{_release}%{?dist}
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency

# upstream bitcoin team convention - v0.12.1
#%define archivebasename v%{version}
# upstream dash team convention - dash-0.12.1
%define archivebasename %{_name}-%{version}
%define sourcetree %{_name}-%{version}

# my convention
%define extrasbasename %{sourcetree}
# during experimental builds
%define pedanticfiletag -%{_release}
# for official releases, get rid of the pedanticfiletag
%define pedanticfiletag %{nil}

Group: Applications/System
License: MIT
URL: http://dash.org/
# upstream
Source0: http://github.com/dashpay/%{name}/archive/%{archivebasename}.tar.gz
#Source0: %{archivebasename}.tar.gz
# contrib/fedora/ dashd.tmpfiles, dash.sysconfig, dash.service, dash.init(never used?)
#                 includes some future SELinux policy stuff as well (.te, .if, .fc)
Source1: %{extrasbasename}%{pedanticfiletag}-contrib-fedora.tar.gz
#Source2 has a pile of stuff contributed by the debian community (XXX but not currently in the 0.12.1 tarball?)
Source2: %{extrasbasename}%{pedanticfiletag}-contrib-debian.tar.gz
# dash icons
Source3: %{extrasbasename}%{pedanticfiletag}-dashify-pixmaps.tar.gz
Source4: %{extrasbasename}%{pedanticfiletag}-dashify-extra-qt-icons.tar.gz
#taw Source8:  README.server.redhat
#taw Source9:  README.utils.redhat
#taw Source10: README.gui.redhat

#taw Dest change address patch for Lamassu Bitcoin machine
#taw Patch1: bitcoin-0.12.0-destchange.patch

# patch configure.ac (autoconf template) for fedora builds
#Patch0: %{extrasbasename}%{pedanticfiletag}-fedora.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  qrencode-devel miniupnpc-devel protobuf-devel openssl-devel
BuildRequires:	desktop-file-utils autoconf automake
#taw BuildRequires:	checkpolicy selinux-policy-devel selinux-policy-doc
BuildRequires:	boost-devel libdb4-cxx-devel libevent-devel
BuildRequires:	libtool java

#taw # Python tests still use OpenSSL for secp256k1, so we still need this to run
#taw # the testsuite on RHEL7, until Red Hat fixes OpenSSL on RHEL7. It has already
#taw # been fixed on Fedora. Dash itself no longer needs OpenSSL for secp256k1.
#taw %if 0%{?rhel}
#taw BuildRequires:	openssl-compat-dashcore-libs
#taw %endif



# dashcore-client
%package client
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (dash-qt client)
BuildRequires:	qt5-qtbase-devel qt5-linguist


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
#taw Requires: selinux-policy
#taw Requires: policycoreutils-python
Requires: openssl-libs
Requires: dashcore-utils%{_isa} = %{version}


# dashcore-libs
%package libs
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (consensus libraries)


# dashcore-devel
%package devel
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (dev libraries and headers)
Requires: bitcoin-libs%{?_isa} = %{version}-%{release}


# dashcore-utils
%package utils
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (commandline utils)



# dashcore SRPM
%description
This is the source package for building the Dash Core set of binary packages.
It will build dashcore-{client,server,utils,libs,devel,debuginfo}.

Dash (Digital Cash) is a privacy-centric digital currency that
enables instant transactions to anyone, anywhere in the world. It uses
peer-to-peer technology to operate with no central authority where
managing transactions and issuing money are carried out collectively
by the network. Dash is based on the Bitcoin software, but it has a
two tier network that improves upon it. Dash allows you to remain anonymous
while you make transactions, similar to cash.

Dash is also a platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at dash.org.


# dashcore-client
%description client
This package provides dash-qt, a user-friendly wallet manager for
personal use.

Dash (Digital Cash) is a privacy-centric digital currency that
enables instant transactions to anyone, anywhere in the world. It uses
peer-to-peer technology to operate with no central authority where
managing transactions and issuing money are carried out collectively
by the network. Dash is based on the Bitcoin software, but it has a
two tier network that improves upon it. Dash allows you to remain anonymous
while you make transactions, similar to cash.

Dash is also a platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at dash.org.


# dashcore-server
%description server
This package provides dashd, a peer-to-peer node and wallet server. It is the
command line installation without a GUI.  It can be used as a commandline wallet
and is typically used to run a masternode. Requires dashcore-utils to be
installed as well

Dash (Digital Cash) is a privacy-centric digital currency that
enables instant transactions to anyone, anywhere in the world. It uses
peer-to-peer technology to operate with no central authority where
managing transactions and issuing money are carried out collectively
by the network. Dash is based on the Bitcoin software, but it has a
two tier network that improves upon it. Dash allows you to remain anonymous
while you make transactions, similar to cash.

Dash is also a platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at dash.org.


# dashcore-libs
%description libs
This package provides libbitcoinconsensus, which is used by third party
applications to verify scripts (and other functionality in the future).

Dash (Digital Cash) is a privacy-centric digital currency that
enables instant transactions to anyone, anywhere in the world. It uses
peer-to-peer technology to operate with no central authority where
managing transactions and issuing money are carried out collectively
by the network. Dash is based on the Bitcoin software, but it has a
two tier network that improves upon it. Dash allows you to remain anonymous
while you make transactions, similar to cash.

Dash is also a platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at dash.org.


# dashcore-devel
%description devel
This package provides the libraries and header files necessary to
compile programs which use libbitcoinconsensus.

Dash (Digital Cash) is a privacy-centric digital currency that
enables instant transactions to anyone, anywhere in the world. It uses
peer-to-peer technology to operate with no central authority where
managing transactions and issuing money are carried out collectively
by the network. Dash is based on the Bitcoin software, but it has a
two tier network that improves upon it. Dash allows you to remain anonymous
while you make transactions, similar to cash.

Dash is also a platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at dash.org.


# dashcore-utils
%description utils
This package provides dash-cli, a utility to communicate with and
control a Dash server via its RPC protocol, and dash-tx, a utility
to create custom Dash transactions.

Dash (Digital Cash) is a privacy-centric digital currency that
enables instant transactions to anyone, anywhere in the world. It uses
peer-to-peer technology to operate with no central authority where
managing transactions and issuing money are carried out collectively
by the network. Dash is based on the Bitcoin software, but it has a
two tier network that improves upon it. Dash allows you to remain anonymous
while you make transactions, similar to cash.

Dash is also a platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at dash.org.



%prep
# dash upstream stuff
%setup -q -n %{sourcetree}
# fedora stuff Source1
%setup -q -T -D -b 1 -n %{sourcetree}
# debian stuff Source2
%setup -q -T -D -b 2 -n %{sourcetree}
# pixmaps icons Source3 
%setup -q -T -D -b 3 -n %{sourcetree}
# QT icons Source4 (must come after main sourcetree (overwrites))
#taw commented out because some core devs expressed displeasure at dark dash icons
#%setup -q -T -D -b 4 -n %{sourcetree}
# patch addressed by removing one dir path level (-p1)
#%patch0 -p1

# Install README files
#taw cp -p %{SOURCE8} %{SOURCE9} %{SOURCE10} .

# Prep SELinux policy -- NOT USED YET
# not sure why this is done here in particular -taw
mkdir -p SELinux
cp -p ./contrib/fedora/dash.{te,if,fc} SELinux

%build
# Build Dash
./autogen.sh
%configure --enable-reduce-exports --enable-glibc-back-compat

make %{?_smp_mflags}

#taw # Build SELinux policy
#taw pushd SELinux
#taw for selinuxvariant in %{selinux_variants}
#taw do
#taw # FIXME: Create and debug SELinux policy
#taw   make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
#taw   mv dash.pp dash.pp.${selinuxvariant}
#taw   make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
#taw done
#taw popd


%check
# Run all the tests
#taw make check
#taw # Run all the other tests
#taw pushd src
#taw srcdir=. test/dashcore-util-test.py
#taw popd
#taw LD_LIBRARY_PATH=/opt/openssl-compat-dash/lib PYTHONUNBUFFERED=1  qa/pull-tester/rpc-tests.py -extended


%install
rm -rf %{buildroot}
mkdir %{buildroot}

cp contrib/debian/examples/dash.conf dash.conf.example

make INSTALL="install -p" CP="cp -p" DESTDIR=%{buildroot} install

# TODO: Upstream puts dashd in the wrong directory. Need to fix the
# upstream Makefiles to relocate it.
mkdir -p -m 755 %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/dashd %{buildroot}%{_sbindir}/dashd

# Install ancillary files
mkdir -p -m 755 %{buildroot}%{_datadir}/pixmaps
install -D -m644 -p share/pixmaps/*.{png,xpm,ico,bmp} %{buildroot}%{_datadir}/pixmaps/
#XXXTAW install -D -m644 -p share/pixmaps/*.{ico,bmp} %{buildroot}%{_datadir}/pixmaps/
install -D -m644 -p contrib/debian/dash-qt.desktop %{buildroot}%{_datadir}/applications/dash-qt.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/dash-qt.desktop
install -D -m644 -p contrib/debian/dash-qt.protocol %{buildroot}%{_datadir}/kde4/services/dash-qt.protocol
install -D -m644 -p contrib/fedora/dashd.tmpfiles %{buildroot}%{_tmpfilesdir}/dash.conf
install -D -m600 -p contrib/fedora/dash.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/dash
install -D -m644 -p contrib/fedora/dash.service %{buildroot}%{_unitdir}/dash.service
install -d -m750 -p %{buildroot}%{_localstatedir}/lib/dash
install -d -m750 -p %{buildroot}%{_sysconfdir}/dash
install -D -m644 -p contrib/debian/manpages/dashd.1 %{buildroot}%{_mandir}/man1/dashd.1
install -D -m644 -p contrib/debian/manpages/dash-qt.1 %{buildroot}%{_mandir}/man1/dash-qt.1
install -D -m644 -p contrib/debian/manpages/dash.conf.5 %{buildroot}%{_mandir}/man5/dash.conf.5
gzip %{buildroot}%{_mandir}/man1/dashd.1
gzip %{buildroot}%{_mandir}/man1/dash-qt.1
gzip %{buildroot}%{_mandir}/man5/dash.conf.5

# Remove test files so that they aren't shipped. Tests have already been run.
rm -f %{buildroot}%{_bindir}/test_*

# We don't ship bench_dash right now
rm -f %{buildroot}%{_bindir}/bench_dash

#taw # Install SELinux policy
#taw for selinuxvariant in %{selinux_variants}
#taw do
#taw 	install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
#taw 	install -p -m 644 SELinux/dash.pp.${selinuxvariant} \
#taw 		%{buildroot}%{_datadir}/selinux/${selinuxvariant}/dash.pp
#taw done


%clean
rm -rf %{buildroot}


# dashcore-server
%pre server
getent group dash >/dev/null || groupadd -r dash
getent passwd dash >/dev/null ||
	useradd -r -g dash -d /var/lib/dash -s /sbin/nologin \
	-c "Dash wallet server" dash
exit 0


# dashcore-server
%post server
%systemd_post dash.service
#taw for selinuxvariant in %{selinux_variants}
#taw do
#taw 	/usr/sbin/semodule -s ${selinuxvariant} -i \
#taw 		%{_datadir}/selinux/${selinuxvariant}/dash.pp \
#taw 		&> /dev/null || :
#taw done
#taw # FIXME This is less than ideal, but until dwalsh gives me a better way...
#taw /usr/sbin/semanage port -a -t dash_port_t -p tcp 8332
#taw /usr/sbin/semanage port -a -t dash_port_t -p tcp 8333
#taw /usr/sbin/semanage port -a -t dash_port_t -p tcp 18332
#taw /usr/sbin/semanage port -a -t dash_port_t -p tcp 18333
#taw /sbin/fixfiles -R dashcore-server restore &> /dev/null || :
#taw /sbin/restorecon -R %{_localstatedir}/lib/dash || :


# dashcore-server
%posttrans server
/usr/bin/systemd-tmpfiles --create


# dashcore-server
%preun server
%systemd_preun dash.service


# dashcore-server
%postun server
%systemd_postun dash.service
#taw if [ $1 -eq 0 ] ; then
#taw 	# FIXME This is less than ideal, but until dwalsh gives me a better way...
#taw 	/usr/sbin/semanage port -d -p tcp 8332
#taw 	/usr/sbin/semanage port -d -p tcp 8333
#taw 	/usr/sbin/semanage port -d -p tcp 18332
#taw 	/usr/sbin/semanage port -d -p tcp 18333
#taw 	for selinuxvariant in %{selinux_variants}
#taw 	do
#taw 		/usr/sbin/semodule -s ${selinuxvariant} -r dash \
#taw 		&> /dev/null || :
#taw 	done
#taw 	/sbin/fixfiles -R dashcore-server restore &> /dev/null || :
#taw 	[ -d %{_localstatedir}/lib/dash ] && \
#taw 		/sbin/restorecon -R %{_localstatedir}/lib/dash \
#taw 		&> /dev/null || :
#taw fi



# dashcore-client
%files client
%defattr(-,root,root,-)
%license COPYING
#taw %doc README.md README.gui.redhat doc/assets-attribution.md doc/multiwallet-qt.md doc/release-notes.md doc/tor.md dash.conf.example
#taw 0.12.0.58 %doc README.md doc/assets-attribution.md doc/multiwallet-qt.md doc/release-notes.md doc/tor.md dash.conf.example
%doc doc/assets-attribution.md doc/multiwallet-qt.md doc/release-notes.md doc/tor.md
%{_bindir}/dash-qt
%{_datadir}/applications/dash-qt.desktop
%{_datadir}/kde4/services/dash-qt.protocol
%{_datadir}/pixmaps/*
%{_mandir}/man1/dash-qt.1.gz


# dashcore-server
%files server
%defattr(-,root,root,-)
%license COPYING
#taw %doc README.md README.server.redhat doc/dnsseed-policy.md doc/release-notes.md doc/tor.md dash.conf.example
#TAW 0.12.0.58 %doc README.md doc/dnsseed-policy.md doc/release-notes.md doc/tor.md dash.conf.example
%doc doc/dnsseed-policy.md doc/release-notes.md doc/tor.md
%dir %attr(750,dash,dash) %{_localstatedir}/lib/dash
%dir %attr(750,dash,dash) %{_sysconfdir}/dash
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/sysconfig/dash
%doc SELinux/*
%{_sbindir}/dashd
%{_unitdir}/dash.service
%{_tmpfilesdir}/dash.conf
%{_mandir}/man1/dashd.1.gz
%{_mandir}/man5/dash.conf.5.gz
#taw %{_datadir}/selinux/*/dash.pp


# dashcore-libs
%files libs
%defattr(-,root,root,-)
%license COPYING
#TAW 0.12.0.58 %doc README.md
%{_libdir}/libbitcoinconsensus.so*


# dashcore-devel
%files devel
%defattr(-,root,root,-)
%license COPYING
#TAW 0.12.0.58 %doc README.md
%{_includedir}/bitcoinconsensus.h
%{_libdir}/libbitcoinconsensus.a
%{_libdir}/libbitcoinconsensus.la
%{_libdir}/pkgconfig/libbitcoinconsensus.pc


# dashcore-utils
%files utils
%defattr(-,root,root,-)
%license COPYING
#taw %doc README.md README.utils.redhat dash.conf.example
#TAW 0.12.0.58 %doc README.md dash.conf.example
%{_bindir}/dash-cli
%{_bindir}/dash-tx



%changelog
* Mon Sep 26 2016 Todd Warner <toddwarner@protonmail.com> 0.12.1-b9bd116.taw_TESTNET20160926
- Testnet Testing Phase 2
- Sourced from: https://dashpay.atlassian.net/builds/browse/DASHL-DEV-644/artifact/JOB1/gitian-linux-dash-src/src
- Announcement message: https://www.dash.org/forum/threads/12-1-testnet-testing-phase-two-ignition.10818/
- Testnet documentation: https://dashpay.atlassian.net/wiki/display/DOC/Testnet
-
* Tue Sep 20 2016 Todd Warner <toddwarner@protonmail.com> 0.12.1-TESTNET20160920.taw
- Initial spec
- ALPHA QUALITY VERSION
- Testnet version of 12.1 -- nearing public beta-time.
- Note: all kinds of unnatural things done with contrib/debian and contrib/fedora copied over from 0.12.0.58
- Sourced from: https://dashpay.atlassian.net/builds/browse/DASHL-DEV/latestSuccessful
- ..and GitHub: https://github.com/dashpay/dash
-
-
-
