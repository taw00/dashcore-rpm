# Dash Masternode Sentinel spec file
#
# This is the source spec for building the Dash Masternode Sentinel toolchain
# required to operate a Dash Masternode. It will build the dashcore-sentinel
# package.
#
# Enjoy. Todd Warner <t0dd@protonmail.com>


# To produce a debuginfo package:
#   1. Comment out the debug package define
#   2. Even commented, it causes problems, so turn it into something like
#      this:  % define debug _ package % { n i l }
# To squelch debuginfo package creation, uncomment the line, and then
# reconstruct the debug package define as it should be
#% define debug _package % { n i l }
# https://fedoraproject.org/wiki/Changes/Harden_All_Packages
#%define _hardened_build 0

# "bump" refers to "release bump" and is a build identifier.
%define bump 2

# "bumptag" is used to indicate additional information, usually an identifier,
# like the builder's initials, or a date, or both, or nil.
# Note: If the value is not %{nil} there needs to be a . preceding this value.
%define bumptag taw
#% define bumptag %{nil}

%define _name sentinel 
%define _version_major 1
%define _version_minor 0
%define _release %{bump}.%{bumptag}

Name: dashcore-sentinel
Version: 1.0
Release: %{_release}%{?dist}
Vendor: Dash.org
Packager: Todd Warner <t0dd@protonmail.com>
Summary: Dash Masternode Sentinel - required toolset for Dash Masternodes

# dashcore-sentinel-1.0
# dashcore-sentinel-1.0-0.taw
%define namev %{name}-%{version}
%define namevr %{namev}-%{release}
# sentinel-1.0
# sentinel-1.0-0.taw
%define _srcname %{_name}
%define srcnamev %{_srcname}-%{version}
%define srcnamevr %{srcnamev}-%{release}
# sentinel-1.0
# sentinel-1.0
# dashcore-sentinel
# dashcore-sentinel-contrib
%define buildtree %{srcnamev}
%define archivebasename %{srcnamev}
%define contribtreename %{name}
%define contribarchivename %{contribtreename}-contrib

# during experimental builds
%define pedanticfiletag -%{_release}
# for official releases, get rid of the pedanticfiletag
%define pedanticfiletag %{nil}

Group: Applications/System
License: MIT
URL: http://dash.org/
# upstream
# sentinel-1.0.tar.gz
Source0: %{archivebasename}.tar.gz
#Source0: https://github.com/dashpay/sentinel
Source1: %{contribarchivename}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{namevr}-XXXXXX)
BuildRequires: /usr/bin/virtualenv

Requires: dashcore-server >= 0.12.1


# Nuke auto-requires that rpmbuild will generate because of the virtualenv
# things we do in the %build section. Note, this statement has to be placed
# here in the SPEC file (before we hit %description)
%global __requires_exclude .*/BUILD/.*/venv/bin/python


%description
Dash Core Sentinel is an autonomous agent for persisting, processing and
automating Dash v12.1 governance objects and tasks, and for expanded functions
in the upcoming Dash v13 release (Evolution).

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
#%setup -q -n %{buildtree}
## extra contributions - Source1
#%setup -q -T -D -b 1 -n %{buildtree}
# Upstream code exploded into sentinel-1.0/sentinel-1.0
%setup -q -T -a 0 -c %{buildtree}
# contrib stuff exploded into sentinel-1.0/dashcore-sentinel
#%setup -q -T -D -b 1 -n %{buildtree}
%setup -q -T -D -a 1

# We leave with this structure...
# ~/rpmbuild/BUILD/dashcore-sentinel-VERSION/sentinel-VERSION/
# ~/rpmbuild/BUILD/dashcore-sentinel-VERSION/dashcore-sentinel/



%build
# WARNING: This build process pulls down libraries from the internet.
#   This is less than ideal for many reasons.
#   TODO: Build from locally known and signed libraries -- a future endeavor.
# Note: We start in sentinel-1.0 (first level). Need to cd deeper...
cd %{archivebasename}
/usr/bin/virtualenv ./venv
./venv/bin/pip install -r ./requirements.txt


%check


%install
rm -rf %{buildroot}
mkdir %{buildroot}
%define varlibtarget %{_sharedstatedir}/dashcore/sentinel

#install -d %{buildroot}%{_sharedstatedir}
install -d %{buildroot}%{varlibtarget}
pwd
cp -a %{archivebasename}/* %{buildroot}%{varlibtarget}/
#rm -rf %{buildroot}%{varlibtarget}/contrib # Contrib files placed individually
#install -D -m640 ./* %{buildroot}%{varlibtarget}/

pwd
# Replace core sentinel configuration file with contributed configuration file
install -D -m640 %{contribtreename}/contrib/linux/var-lib-dashcore-sentinel_sentinel.conf %{buildroot}%{varlibtarget}/sentinel.conf

# Logrotate file rules
install -D -m644 %{contribtreename}/contrib/linux/etc-logrotate.d_dashcore-sentinel %{buildroot}/etc/logrotate.d/dashcore-sentinel

# Ghosting a log file - we have to own the directory and log file
install -d -m700 %{buildroot}%{_localstatedir}/log/dashcore
touch %{buildroot}%{_localstatedir}/log/dashcore/sentinel.log

# Right now, things are being run out of /var/lib/dashcore/sentinel
#
# Should this program live in /var/lib? Or should it live elsewhere? Good
# questions. The executable is ./bin/sentinel.py. It's an oddity. It probably
# should live in /usr/sbin. But it doesn't. The rest of the program should
# probably live in /var/lib.
#
# Consideration: Maybe punt and shove everything in /opt/dashcore/sentinel
# and call it a day. That's ugly packaging though. For now, it stays in /var/lib


%clean
rm -rf %{buildroot}


%pre
getent group dashcore >/dev/null || groupadd -r dashcore
# dashcore system user's home directory will be /var/lib/dashcore
getent passwd dashcore >/dev/null ||
  useradd -r -g dashcore -d %{_sharedstatedir}/dashcore -s /sbin/nologin \
  -c "System user 'dashcore' to isolate Dash Core execution" dashcore
exit 0


%post
## Reference: https://fedoraproject.org/wiki/Packaging:Scriptlets
## Always runs on install or upgrade
#if [$1 -gt 0 ] ; then
#  # Only runs on upgrades
#  if [$1 -gt 1 ] ; then
#  fi
#fi

%preun
# Nuke the database and then uninstall the thing. This will ensure the sentinel
# directory is properly cleaned up as well if need be.
/usr/bin/rm -f %{_sharedstatedir}/dashcore/sentinel/database/sentinel.db >> /dev/null 2>&1


%files
%defattr(-,dashcore,dashcore,-)
%license %attr(-,root,root) %{archivebasename}/LICENSE
%doc %attr(-,root,root) %{archivebasename}/README.md %{contribtreename}/contrib/linux/README.redhat.md
# Log directory and file
%dir %attr(700,dashcore,dashcore) %{_localstatedir}/log/dashcore
%ghost %{_localstatedir}/log/dashcore/sentinel.log
%attr(644,root,root) /etc/logrotate.d/dashcore-sentinel
# Code and Data Directories (combined, for now), includes config file
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore/sentinel
%{_sharedstatedir}/dashcore/sentinel/*
%config(noreplace) %{_sharedstatedir}/dashcore/sentinel/sentinel.conf



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
#   * https://bamboo.dash.org/browse/DASHL-DEV/latestSuccessful
#   * https://bamboo.dash.org/browse/DASHL-DEV-<BUILD_NUMBER>/artifact/JOB1/gitian-linux-dash-src/src
#   * https://bamboo.dash.org/artifact/DASHL-DEV/JOB1/build-<BUILD_NUMBER>/gitian-linux-dash-src/src/dashcore-0.12.1.tar.gz
#
# Dash Core git repos...
#   * Dash: https://github.com/dashpay/dash
#   * Sentinel: https://github.com/dashpay/sentinel

%changelog
* Fri Feb 10 2017 Todd Warner <t0dd@protonmail.com> 1.0-2.taw
- Building debuginfo RPMs as well now.
-
* Mon Feb 06 2017 Todd Warner <t0dd@protonmail.com> 1.0-1.taw
- Fixed a broken file in the contribs that hosed the sentinel.conf file.
- 
* Sun Feb 05 2017 Todd Warner <t0dd@protonmail.com> 1.0-0.taw
- v12.1 GA
- 

