# Dash Masternode Sentinel spec file
#
# This is the source spec for building the Dash Core Masternode Sentinel
# toolchain required to operate a Dash Core Masternode. It will build the
# dashcore-sentinel package.
#
# Enjoy. Todd Warner <t0dd@protonmail.com>


# To produce a debuginfo package:
#   1. Comment out this define
#   2. Separate the %'s from their variable (this screws things up)
# Otherwise, leave it uncommented
%define debug_package %{nil}
# https://fedoraproject.org/wiki/Changes/Harden_All_Packages
#%define _hardened_build 0

# "bump" refers to "release bump" and is a build identifier For full releases,
# one will often just name this a numberal for every build: 1, 2, 3, etc. For
# more experimental builds, one will often just make it a date 20160405, or a
# date with a numeral, like 20160405.0, 20160405.1, etc.
# Use whatever is meaningful to you. Just remember if you are iterating, it needs
# to be consistent an progress in version (so that upgrades work)
%define bump test.0

# "bumptag" is used to indicate additional information, usually an identifier,
# like the builder's initials, or a date, or both, or nil.
# Example, the original builder was "taw" or "Todd Warner", so he would use .taw
# Note: If the value is not %{nil} there needs to be a . preceding this value
# For final releases, one will often opt to nil-out this value.
%define bumptag .taw
#% define bumptag %{nil}

%define _release %{bump}%{bumptag}

%define _name sentinel
Name: dashcore-sentinel
Version: 0.12.1
Release: %{_release}%{?dist}
Vendor: Dash.org
Packager: Todd Warner <t0dd@protonmail.com>
Summary: Dash Masternode Sentinel - required toolset for Dash Masternodes

#%define archivebasename %{_name}-%{version}
%define archivebasename %{name}
#%define sourcetree %{_name}-%{version}
%define sourcetree %{name}

# during experimental builds
%define pedanticfiletag -%{_release}
# for official releases, get rid of the pedanticfiletag
%define pedanticfiletag %{nil}

Group: Applications/System
License: MIT
URL: http://dash.org/
# upstream
Source0: %{archivebasename}.tar.gz
#Source0: https://github.com/nmarley/sentinel
Source1: %{archivebasename}-contrib.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: /usr/bin/virtualenv

Requires: dashcore-server >= %{version}


# Nuke auto-requires that rpmbuild will generate because of the virtualenv
# things we do in the %build section. Note, this statement has to be placed
# here in the SPEC file (before we hit %description)
%global __requires_exclude .*/BUILD/.*/venv/bin/python


%description
Dash Core Sentinel is an autonomous agent for persisting, processing and
automating Dash v12.1 governance objects and tasks, and for expanded functions
in the upcoming Dash V13 release (Evolution).

Sentinel is implemented as a Python application that binds to a local version
12.1 dashd instance on each Dash v12.1 Masternode.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.


%prep
%setup -q -n %{sourcetree}
# extra contributions - Source1
%setup -q -T -D -b 1 -n %{sourcetree}


%build
# WARNING: This build process pulls down libraries from the internet.
#   This is less than ideal for many reasons.
#   TODO: Build from locally known and signed libraries -- a future endeavor.
/usr/bin/virtualenv ./venv
./venv/bin/pip install -r ./requirements.txt


%check


%install
rm -rf %{buildroot}
mkdir %{buildroot}
%define varlibtarget %{_sharedstatedir}/dashcore-sentinel

#install -d %{buildroot}%{_sharedstatedir}
install -d %{buildroot}%{varlibtarget}
cp -a ./* %{buildroot}%{varlibtarget}/
#install -D -m640 ./* %{buildroot}%{varlibtarget}/

# Replace core sentinel configuration file with contributed configuration file
install -D -m640 ./contrib/linux/sentinel.conf %{buildroot}%{varlibtarget}/sentinel.conf

# Right now, things are being run out of /var/lib/dashcore-sentinel
#
# Should this program live in /var/lib? Or should it live elsewhere? Good
# questions. The executable is ./scripts/crontab.py. It's an oddity, and oddly
# named. It probably should be named sentinel or sentinel.py and live in
# /usr/sbin. But it doesn't. The rest of the program should probably live in
# /var/lib.
#
# Consideration: Maybe punt and shove everything in /opt/dashcore-sentinel
# and call it a day. That's ugly packaging though. For now, it stays in /var/lib


%clean
rm -rf %{buildroot}


%pre
getent group dash >/dev/null || groupadd -r dash
getent passwd dash >/dev/null ||
	useradd -r -g dash -d /var/lib/dash -s /sbin/nologin \
	-c "System user 'dash' to isolate Dash Core execution" dash
exit 0


%post


%files
%defattr(-,dash,dash,-)

%define varlibtarget %{_sharedstatedir}/dashcore-sentinel

%license %attr(-,root,root) LICENSE
%doc %attr(-,root,root) README.md contrib/linux/README.redhat.md

%dir %{varlibtarget}
%{varlibtarget}/*
%config(noreplace) %{_sharedstatedir}/dashcore-sentinel/sentinel.conf


#%files
#%defattr(-,root,root,-)
#%define varlibtarget %{_sharedstatedir}/dashcore-sentinel
#%license %attr(-,root,root) LICENSE
#%doc %attr(-,root,root) README.md contrib/linux/README.redhat.md
#%dir %attr(750,dash,dash) %{varlibtarget}
#%attr(-,dash,dash) %{varlibtarget}/*
#%config(noreplace) %attr(660,dash,dash) %{_sharedstatedir}/dashcore-sentinel/sentinel.conf


# Testnet test phase 2
# 
# Announcement message: https://www.dash.org/forum/threads/12-1-testnet-testing-phase-two-ignition.10818/
# Testnet documentation: https://dashpay.atlassian.net/wiki/display/DOC/Testnet
# Testnet masternode documentation: https://gist.github.com/taw00/e978f862ee1ad66722e16bcc8cf18ca5
#
# GitHub for RPM builds: https://github.com/taw00/dashcore-rpm
# GitHub for original source: https://github.com/nmarley/sentinel


%changelog
* Sun Jan 22 2017 Todd Warner <t0dd@protonmail.com> 0.12.1-test.0
- initial build
-

