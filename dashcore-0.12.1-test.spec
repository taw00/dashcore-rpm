# Dash (digital cash) cryptocurrency spec file
# Dash Core QT wallet, masternode, full node, and more.
#
# Note about edits within the spec: Any comments beginning with #taw is my
# attempt to block off troublesome, or inappropriate stuff that came over from
# the bitcoin.spec file that this is based off of. Some things, like the SELinux
# elements will likely be brought back in when I get a moment.
#
# Enjoy. Todd Warner <t0dd@protonmail.com>, Fall 2016

%define _hardened_build 1
%global selinux_variants mls strict targeted

# To produce a dashcore-debuginfo package:
#   1. Comment out this define
#   2. Separate the %'s from their variable (this screws things up)
# Otherwise, leave it uncommented
%define debug_package %{nil}

# "bump" refers to "release bump" and is a build identifier For full releases,
# one will often just name this a numberal for every build: 1, 2, 3, etc. For
# more experimental builds, one will often just make it a date 20160405, or a
# date with a numeral, like 20160405.0, 20160405.1, etc.
# Use whatever is meaningful to you. Just remember if you are iterating, it needs
# to be consistent and progress in version (so that upgrades work)
%define bump test.b00700.0

# "bumptag" is used to indicate additional information, usually an identifier,
# like the builder's initials, or a date, or both, or nil.
# Example, the original builder was "taw" or "Todd Warner", so he would use .taw
# Note: If the value is not %{nil} there needs to be a . preceding this value
# For final releases, one will often opt to nil-out this value.
%define bumptag .taw
#% define bumptag %{nil}

%define _release %{bump}%{bumptag}

%define _name dashcore
Name: dashcore
Version: 0.12.1
Release: %{_release}%{?dist}
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency

# upstream bitcoin team convention - v0.12.1
#%define archivebasename v%{version}
# upstream dash team convention - dashcore-0.12.1
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

BuildRequires: autoconf automake
BuildRequires: boost-devel gcc-c++ java
BuildRequires: libdb4-cxx-devel libevent-devel libtool miniupnpc-devel openssl-devel protobuf-devel qrencode-devel
BuildRequires: qt5-linguist qt5-qtbase-devel
BuildRequires: desktop-file-utils
#taw BuildRequires:	checkpolicy selinux-policy-devel selinux-policy-doc

#taw # Python tests still use OpenSSL for secp256k1, so we still need this to run
#taw # the testsuite on RHEL7, until Red Hat fixes OpenSSL on RHEL7. It has already
#taw # been fixed on Fedora. Dash itself no longer needs OpenSSL for secp256k1.
#taw %if 0%{?rhel}
#taw BuildRequires:	openssl-compat-dashcore-libs
#taw %endif



# dashcore-client
%package client
Summary: Dash - Digital Cash - Peer-to-peer, privacy-centric, digital currency (dash-qt client)
BuildRequires: qt5-qtbase-devel qt5-linguist


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

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.



# dashcore-client
%description client
This package provides dash-qt, a user-friendly wallet manager for
personal use.

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
command line installation without a GUI.  It can be used as a commandline wallet
and is typically used to run a Dash Masternode. Requires the dashcore-utils RPM
package to be installed.

If you are running this as a masternode, it is highly recommended that you also
install Sentinel. Read more here: https://github.com/nmarley/sentinel Please refer
to Dash documentation at dash.org for more information about running a Masternode.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

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

# The test binaries
#rm -f %{buildroot}%{_bindir}/test_*
#rm -f %{buildroot}%{_bindir}/bench_dash


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
%doc doc/assets-attribution.md doc/multiwallet-qt.md doc/release-notes.md doc/tor.md doc/keepass.md
%{_bindir}/dash-qt
# XXX COMMENT OUT TEST BINARY IF THIS IS A PRODUCTION RELEASE
%{_bindir}/test_dash-qt
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
%doc doc/dnsseed-policy.md doc/release-notes.md doc/tor.md doc/multiwallet-qt.md doc/guide-startmany.md doc/reduce-traffic.md doc/zmq.md
%dir %attr(750,dash,dash) %{_localstatedir}/lib/dash
%dir %attr(750,dash,dash) %{_sysconfdir}/dash
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/sysconfig/dash
%doc SELinux/*
%{_sbindir}/dashd
# XXX COMMENT OUT TEST BINARIES IF THIS IS A PRODUCTION RELEASE
%{_bindir}/test_dash
%{_bindir}/bench_dash
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


# More information about Testnet DashCore:
# Announcement message: https://www.dash.org/forum/threads/12-1-testnet-testing-phase-two-ignition.10818/
# Testnet documentation: https://dashpay.atlassian.net/wiki/display/DOC/Testnet
# Masternode setup: https://gist.github.com/moocowmoo/66049a781f8eaa1021306072f19363d4
#
# Latest source builds: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-latestSuccessful/
# GitHub: https://github.com/dashpay/dash
# GitHub for Sentinel (complimentary to dashd): https://github.com/nmarley/sentinel

%changelog
* Tue Nov 15 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00700.0
- Testnet - Testing Phase 2 -- From build 00700, v0.12.1.0-g714f9a4
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00700
- SHA256: a338d9692ea0e73a5201586df4f01986ce29fd689383c1196475a62f4ae25696 dashcore-0.12.1.tar.gz
-
* Sun Nov 13 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00699.0
- Testnet - Testing Phase 2 -- From build 00699, v0.12.1.0-gc31ba8b
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00699
- SHA256: 58ef36c35e7d6d7fb8c0bb626ec8e7fadc7b8938f9673bef74311c542b5e154d dashcore-0.12.1.tar.gz
-
* Sat Nov 12 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00698.0
- Testnet - Testing Phase 2 -- From build 00698, v0.12.1.0-g82ca5fd
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00698
- SHA256: 566b4aac1d361da7797a115c7a2c7f4769f1fbf73cc1f14f581a870e6cc4423a dashcore-0.12.1.tar.gz
-
* Fri Nov 11 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00697.0
- Testnet - Testing Phase 2 -- From build 00697, v0.12.1.0-gd2f1fd2 
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00697
- SHA256: 556f4e5e6c8b4c11a67d2dc6d0c3bb57112f1cde75b3b9d77c179869d8fd979d dashcore-0.12.1.tar.gz
-
* Tue Nov 08 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00696.0
- Testnet - Testing Phase 2 -- From build 00696, v0.12.1.0-gf21c7cc
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00696
- SHA256: 98442787d35037ac7d211253c10f8d3b7b9935103bce162c450aab98f4f56a10 dashcore-0.12.1.tar.gz
-
* Mon Nov 07 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00695.0
- Testnet - Testing Phase 2 -- From build 00695, v0.12.1.0-gb11cc8f
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00695
- SHA256: 9032cbbe55a8832a32d8313657b31ce816302736a4aca0df6c93ed728d15af5f dashcore-0.12.1.tar.gz
-
* Sun Nov 06 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00694.0
- Testnet - Testing Phase 2 -- From build 00694
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00694
- SHA256: 26502c21a0c01f4838fa0062c7be1ad95d6d238d10d2b9fa6ebba5a2e8c7dad1 dashcore-0.12.1.tar.gz
-
* Wed Nov 02 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00691.0
- Testnet - Testing Phase 2 -- From build 00691
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00691
- SHA256: 933d6b9f1fdbff336ff19955ba7ceabc915dc760a0d7cd8dce43fbb3fd75bfd1  dashcore-0.12.1.tar.gz
-
* Mon Oct 31 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00688.0
- Testnet - Testing Phase 2 -- From build 00688
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00688
- Upstream packaging change dash-0.12.1.tar.gz becomes... dashcore-0.12.1.tar.gz
- SHA256: 7044b80c0a7254c1780c057cd69fbc5d2bfc53293f4eb86b1c87a9abb8af8d42  dashcore-0.12.1.tar.gz
- Loads of merges.
-
* Thu Oct 27 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00679.0
- Testnet - Testing Phase 2 -- From build 00679
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00679
-
* Wed Oct 26 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00676.0
- Testnet - Testing Phase 2 -- From build 00676
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00676
-
* Mon Oct 24 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00672.0
- Testnet - Testing Phase 2 -- From build 00672
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00672
-
* Sun Oct 23 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00671.0
- Testnet - Testing Phase 2 -- From build 00671
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00671
- PrivateSend mixing works once again in this release.
-
* Sun Oct 23 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00670.0
- Testnet - Testing Phase 2 -- From build 00670
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00670
-
* Fri Oct 21 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00668.0
- Testnet - Testing Phase 2 -- From build 00668
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00668
-
* Fri Oct 21 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00667.0
- Testnet - Testing Phase 2 -- From build 00667
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00667
-
* Tue Oct 18 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00666.0
- Testnet - Testing Phase 2 -- From build 00666
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00666
-
* Thu Oct 13 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00662.0
- Testnet - Testing Phase 2 -- From build 00662
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00662
-
* Sat Oct 08 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-test.b00655.0
- Testnet - Testing Phase 2 -- From build 00655
- Source: https://dashpay.atlassian.net/builds/artifact/DASHL-DEV/JOB1/build-00655
- Apologies for the changing versioning scheme. I can't seem to settle on something I like.
-
* Sun Oct 02 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-1test
- Testnet - Testing Phase 2 -- From the September 30, 2016 build
-
* Thu Sep 29 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-0test
- Testnet - Testing Phase 2 -- From the September 27, 2016 build
- Updated build requirements. Updated descriptions. Updated versioning (yet again).
- Added test binaries.
-
* Mon Sep 26 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-b9bd116.taw_TESTNET20160926
- Testnet Testing Phase 2 - don't use this version
-
* Tue Sep 20 2016 Todd Warner <t0dd@protonmail.com> 0.12.1-TESTNET20160920.taw
- Initial spec - don't use this version
- Note: all kinds of unnatural things done with contrib/debian and contrib/fedora copied over from 0.12.0.58
-
