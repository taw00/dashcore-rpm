# Dash Masternode Sentinel spec file
#
# This is the source spec for building the Dash Masternode Sentinel toolchain
# required to operate a Dash Masternode. It will build the dashcore-sentinel
# package.
#
# Enjoy. Todd Warner <t0dd@protonmail.com>

# Note: "bump" and "bumptag" are release-build identifiers.
# For sentinel, bumptag will be either testing.taw, rc.taw, or just taw
# depending on whether this is a test, release candidate, or release build. taw
# are the builder's initials.
%define bump 1
%define bumptag taw
%define _release %{bump}.%{bumptag}

%define _name1 sentinel 
%define _name2 dashcore-sentinel 

%define _version_major 1.1
%define _version_minor 0


Name: %{_name2}
Version: %{_version_major}.%{_version_minor}
Release: %{_release}%{?dist}
Vendor: Dash.org
Packager: Todd Warner <t0dd@protonmail.com>
Summary: Dash Masternode Sentinel - required toolset for Dash Masternodes

# Various archive and tree naming conventions (for example)
# 1. sentinel-1.0.1 (upstream dash team convention, github, etc - eg. sentinel-1.0.1.tar.gz)
# 2. sentinel-1.0.1-1
# 3. dashcore-sentinel-1.0
# 4. dashcore-sentinel
%define _basename1 %{_name1}-%{version}
%define _basename2 %{_name1}-%{version}-%{bump}
%define _basename3 %{_name2}-%{_version_major}
%define _basename4 %{_name2}

# archivebasename is a "symlink" to whichever source tarball we are using
%define archivebasename %{_basename1}
%define archivebasename_contrib %{_basename3}-contrib

# the exploded tree of code in BUILD
# sourcetree is top dir: dashcore-sentinel-1.0
# sentineltree and contribtree hang off of it
%define sourcetree %{_basename3}
%define sentineltree %{_basename1}
%define contribtree %{_basename3}


Group: Applications/System
License: MIT
URL: http://dash.org/
Source0: %{archivebasename}.tar.gz
Source1: %{archivebasename_contrib}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: /usr/bin/virtualenv
Requires: dashcore-server >= 0.12.2

# How debug info and build_ids managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
%define debug_package %{nil}
%define _unique_build_ids 1
%define _build_id_links alldebug

# https://fedoraproject.org/wiki/Changes/Harden_All_Packages
%define _hardened_build 1

# Nuke auto-requires that rpmbuild will generate because of the virtualenv
# things we do in the %build section. Note, this statement has to be placed
# here in the SPEC file (before we hit %description)
%global __requires_exclude .*/BUILD/.*/venv/bin/python


%description
Dash Core Sentinel is an autonomous agent for persisting, processing and
automating Dash governance objects and tasks, and for expanded functions in the
upcoming Dash release (codename Evolution).

Sentinel is implemented as a Python application that binds to a local version
dashd instance on each Dash Masternode.

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency that offers
instant transactions (InstantSend), private transactions (PrivateSend) and token
fungibility. Dash operates a decentralized governance and budgeting system,
making it the first decentralized autonomous organization (DAO). Dash is also a
platform for innovative decentralized crypto-tech.

Dash is open source and the name of the overarching project. Learn more
at www.dash.org.


%prep
# Upstream code exploded into sentinel-1.0/sentinel-1.0
%setup -q -T -a 0 -c %{sourcetree}
# contrib stuff exploded into sentinel-1.0/dashcore-sentinel
%setup -q -T -D -a 1

# We leave with this structure...
# ~/rpmbuild/BUILD/dashcore-sentinel-X.Y/sentinel-X.Y.Z/
# ~/rpmbuild/BUILD/dashcore-sentinel-X.Y/dashcore-sentinel-X.Y/



%build
# WARNING: This build process pulls down libraries from the internet.
#   This is less than ideal for many reasons.
#   TODO: Build from locally known and signed libraries -- a future endeavor.
# Building in dashcore-sentinel-X.Y
# cd into dashcore-sentinel-X.Y/sentinel-X.Y.Z
cd %{sentineltree}
/usr/bin/virtualenv ./venv
./venv/bin/pip install -r ./requirements.txt
cd ..


%check


%install
rm -rf %{buildroot}
mkdir %{buildroot}
%define varlibtarget %{_sharedstatedir}/dashcore/sentinel

#install -d %{buildroot}%{_sharedstatedir}
install -d %{buildroot}%{varlibtarget}
pwd
cp -a %{sentineltree}/* %{buildroot}%{varlibtarget}/
#rm -rf %{buildroot}%{varlibtarget}/contrib # Contrib files placed individually
#install -D -m640 ./* %{buildroot}%{varlibtarget}/

pwd
# Replace core sentinel configuration file with contributed configuration file
install -D -m640 %{contribtree}/contrib/linux/var-lib-dashcore-sentinel_sentinel.conf %{buildroot}%{varlibtarget}/sentinel.conf

# Logrotate file rules
install -D -m644 %{contribtree}/contrib/linux/etc-logrotate.d_dashcore-sentinel %{buildroot}/etc/logrotate.d/dashcore-sentinel

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

%license %attr(-,root,root) %{sentineltree}/LICENSE
%doc %attr(-,root,root) %{sentineltree}/README.md %{contribtree}/contrib/linux/README.redhat.md

# Log directory and file
%dir %attr(700,dashcore,dashcore) %{_localstatedir}/log/dashcore
%ghost %{_localstatedir}/log/dashcore/sentinel.log
%attr(644,root,root) /etc/logrotate.d/dashcore-sentinel

# Code and Data Directories (combined, for now), includes config file
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore/sentinel
%config(noreplace) %{_sharedstatedir}/dashcore/sentinel/sentinel.conf
%{_sharedstatedir}/dashcore/sentinel/bin
%{_sharedstatedir}/dashcore/sentinel/database
%{_sharedstatedir}/dashcore/sentinel/lib
%{_sharedstatedir}/dashcore/sentinel/share
%{_sharedstatedir}/dashcore/sentinel/test
%{_sharedstatedir}/dashcore/sentinel/venv
%{_sharedstatedir}/dashcore/sentinel/README.md
%{_sharedstatedir}/dashcore/sentinel/LICENSE
%{_sharedstatedir}/dashcore/sentinel/requirements.txt


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
* Tue May 1 2018 Todd Warner <t0dd@protonmail.com> 1.1.0-1.taw
- Build failing on Fedora 28 due to pedantic spec file checks. Fixed!

* Tue Nov 7 2017 Todd Warner <t0dd@protonmail.com> 1.1.0-0.taw
- Release 1.1 in support of dashcore 0.12.2.0 - b21bb6c
- 971aa5e5f4d06ba76e76c9c828402af56f28353254c8db15214ac7071d982de5 sentinel-1.1.0.tar.gz
- d1526682d6103e15f17a3298c76eda00cd0126903accc762ea7c1a3eb806b1f1 dashcore-sentinel-1.1-contrib.tar.gz
-
* Fri Feb 24 2017 Todd Warner <t0dd@protonmail.com> 1.0.1-0.rc.taw
- Release 1.0.1 - Release Candidate - 4ac8523
- 407c509cc00706645e899dc6fa5bdc1f6ea156381ab8b84d669ed59c1a070fad  sentinel-1.0.1.tar.gz
-
* Fri Feb 10 2017 Todd Warner <t0dd@protonmail.com> 1.0-2.taw
- Building debuginfo RPMs as well now.
-
* Mon Feb 06 2017 Todd Warner <t0dd@protonmail.com> 1.0-1.taw
- Fixed a broken file in the contribs that hosed the sentinel.conf file.
- 
* Sun Feb 05 2017 Todd Warner <t0dd@protonmail.com> 1.0-0.taw
- Release 1.0 - d822f41 - in tandem with Dash Core 12.1 release
- 

