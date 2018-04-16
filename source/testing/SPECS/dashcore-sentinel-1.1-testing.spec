# Dash Masternode Sentinel spec file
#
# This is the source spec for building the Dash Masternode Sentinel toolchain
# required to operate a Dash Masternode. It will build the dashcore-sentinel
# package.
#
# Note about edits within the spec: Any comments beginning with #t0dd are
# associated to future work or experimental elements of this spec file and
# build.
#
# Note commented out macros in this (or any) spec file. You MUST double up
# the %%'s or rpmbuild will yell at you. RPM is weird.
#
# Enjoy. -t0dd

# flip-flop next two lines if you don't want the minor bump
%undefine _release_minorbump
%define _release_minorbump taw0

# flip-flop next two lines if we are not testing
%undefine _release_minor_snapinfo
%define _release_minor_snapinfo 2.testing

# name-version-release
# ...where release is...
# <pkgrel>[.<extraver>][.<snapinfo>]%%{?dist}[.<minorbump>]
# ...for example...
# name: dashcore-server
# version: 1.1.0 (major=1.1 and minor=0)
# release: 1.1.testing.fc27.taw0
#   _release_major (pkgrel): 1 -- should never be 0 if not testing
#   _release_minor_snapinfo (extraver.snapinfo): 1.testing -- disappears
#     -- disappears (undefined) at GA and then _release_major is bumped
#   %%{?dist}: .fc27 -- includes the decimal point
#   _release_minorbump: initials+decimal - taw or taw0 or taw1 or etc.

%define _name_s sentinel
%define _name_dcs dashcore-sentinel
Name: %{_name_dcs}
%define _version_major 1.1
%define _version_minor 0
Version: %{_version_major}.%{_version_minor}
%define _release_major 1

# ---------------- end of commonly edited elements ----------------------------

# "Release" gets complicated...

%define _release_pt1 %{_release_major}%{?dist}
%if 0%{?_release_minor_snapinfo:1}
# extraver.snapinfo.[dist]...
%define _release_pt1 %{_release_major}.%{_release_minor_snapinfo}%{?dist}
%endif

### builder initials and incremental bumps go here!
### Examples: taw, taw0, taw1, etc.
#%%define _release_minorbump taw0 -- defined at top

%define _release %{_release_pt1}
%if %{?_release_minorbump}
%define _release %{_release_pt1}.%{_release_minorbump}
%endif
Release: %{_release}

Summary: Dash Masternode Sentinel - required toolset for Dash Masternodes

# how are debug info and build_ids managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
%define debug_package %{nil}
%define _unique_build_ids 1
%define _build_id_links alldebug


# https://fedoraproject.org/wiki/Changes/Harden_All_Packages
#%%define _hardened_build 0

# Various archive and tree naming conventions (for example)
# 1. sentinel-1.1.0
#    (upstream dash team convention, github, etc - eg. sentinel-1.0.1.tar.gz)
# 2. dashcore-sentinel-1.1
%define _srcarchive_github %{_name_s}-%{version}
%define srcarchive %{_srcarchive_github}
%define srccontribarchive %{_name_dcs}-%{_version_major}-contrib

# Unarchived source tree structure (extracted in .../BUILD)
#   srcroot               dashcore-sentinel-1.1
#      \_srccodetree        \_sentinel-1.1.0 (github tree example)
#      \_srccontribtree     \_dashcore-sentinel-1.1-contrib
%define _srccodetree_github %{_name_s}-%{version}
%define srcroot %{_name_dcs}-%{_version_major}
%define srccontribtree %{_name_dcs}-%{_version_major}-contrib
%define srccodetree %{_srccodetree_github}


Group: Applications/System
License: MIT
URL: http://dash.org/
Source0: %{srcarchive}.tar.gz
Source1: %{srccontribarchive}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: /usr/bin/virtualenv
Requires: dashcore-server >= 0.12.2


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

Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a strong
focus on serving the payments industry. Dash offers a form of money that is
portable, inexpensive, divisible and fast. It can be spent securely both online
and in person with minimal transaction fees. Dash offers instant transactions
(InstantSend), private transactions (PrivateSend), and operates a
self-governing and self-funding model. This decentralized governance and
budgeting system makes it one of the first ever successful decentralized
autonomous organizations (DAO). Dash is also a platform for innovative
decentralized crypto-tech.

Learn more at www.dash.org.



%prep
# Upstream code exploded into sentinel-1.0/sentinel-1.0
%setup -q -T -a 0 -c %{srcroot}
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
cd %{srccodetree}
/usr/bin/virtualenv ./venv
./venv/bin/pip install -r ./requirements.txt
cd ..


%check


%install
# This section starts us in directory .../BUILD/sentinel-1.1 (srcroot)
rm -rf %{buildroot} ; mkdir %{buildroot}

# Install / config ancillary files
# Cheatsheet for built-in RPM macros:
#   _datadir = /usr/share
#   _mandir = /usr/share/man
#   _sysconfdir = /etc
#   _localstatedir = /var
#   _sharedstatedir is /var/lib
#   _prefix = /usr
#   _libdir = /usr/lib or /usr/lib64 (depending on system)
#   https://fedoraproject.org/wiki/Packaging:RPMMacros
%define _tmpfilesdir /usr/lib/tmpfiles.d
%define _unitdir /usr/lib/systemd/system
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_sysconfdir}/dashcore
install -d %{buildroot}%{_localstatedir}
install -d %{buildroot}%{_localstatedir}/log
install -d -m700 %{buildroot}%{_localstatedir}/log/dashcore
install -d %{buildroot}%{_sharedstatedir}
install -d %{buildroot}%{_sharedstatedir}/dashcore
install -d %{buildroot}%{_sharedstatedir}/dashcore/sentinel
install -d %{buildroot}%{_prefix}
install -d %{buildroot}%{_tmpfilesdir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_mandir}/man1
#install -d -m755 -p %{buildroot}%{_sbindir}
#install -d -m755 -p %{buildroot}%{_bindir}
#install -d -m755 -p %{buildroot}%{_includedir}
#install -d -m755 -p %{buildroot}%{_libdir}

cp -a %{srccodetree}/* %{buildroot}%{_sharedstatedir}/dashcore/sentinel/

# Replace core sentinel configuration file with contributed configuration file
# Remove supplied sentinel configuration file
# Place contributed configuration file into /etc/dashcore
# Create symlink to that file...
#   /var/lib/dashcore/sentinel/sentinel.conf -> /etc/dashcore/sentinel.conf
rm -f %{buildroot}%{_sharedstatedir}/dashcore/sentinel/sentinel.conf
install -D -m640 %{srccontribtree}/linux/etc-dashcore_sentinel.conf %{buildroot}%{_sysconfdir}/dashcore/sentinel.conf
ln -s %{_sysconfdir}/dashcore/sentinel.conf %{buildroot}%{_sharedstatedir}/dashcore/sentinel/sentinel.conf

# Log files
# ...logrotate file rules
install -D -m644 -p %{srccontribtree}/linux/etc-logrotate.d_dashcore-sentinel %{buildroot}/etc/logrotate.d/dashcore-sentinel
# ...ghosted log files - need to exist in the installed buildroot
touch %{buildroot}%{_localstatedir}/log/dashcore/sentinel.log

# Right now, things are being run out of /var/lib/dashcore/sentinel
#
# Should this program live in /var/lib? Or should it live elsewhere? Good
# questions. The executable is ./bin/sentinel.py. It's an oddity. It probably
# should live in /usr/sbin. But it doesn't. The rest of the program should
# probably live in /var/lib.
#


%clean
rm -rf %{buildroot}


%pre
getent group dashcore >/dev/null || groupadd -r dashcore
# dashcore system user's home directory will be /var/lib/dashcore
getent passwd dashcore >/dev/null ||
  useradd -r -g dashcore -d %{_sharedstatedir}/dashcore -s /sbin/nologin \
  -c "System user 'dashcore' to isolate Dash Core execution" dashcore

# Fix the sentinel.conf configuration file location if it is in
# /var/lib/dashcore/sentinel. We want it in /etc/dashcore/
# Also if /var/lib/dashcore/sentinel/sentinel.conf is not a symlink, we need
# to fix that.
#    /var/lib/dashcore/sentinel/sentinel.conf -> /etc/dashcore/sentinel.conf
%define vlds %{_sharedstatedir}/dashcore/sentinel
%define etcd %{_sysconfdir}/dashcore
%define vlds_conf %{vlds}/sentinel.conf
%define etcd_conf %{etcd}/sentinel.conf
if [ -e %{vlds_conf} -a -f %{vlds_conf} -a ! -h %{vlds_conf} ]
then
   mv %{vlds_conf} %{etcd}/
   ln -s %{etcd_conf} %{vlds_conf}
   chown dashcore:dashcore %{vlds_conf}
   chown -R dashcore:dashcore %{etcd_conf}
   chmod 640 %{etcd_conf}*
fi

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
# This section starts us in directory .../BUILD/sentinel-1.1 (srcroot)
%defattr(-,dashcore,dashcore,-)
%license %attr(-,root,root) %{srccodetree}/LICENSE
%doc %attr(-,root,root) %{srccodetree}/README.md %{srccontribtree}/linux/README.redhat.md

# Directories
# /etc/dashcore
%dir %attr(750,dashcore,dashcore) %{_sysconfdir}/dashcore
# /var/lib/dashcore
# /var/lib/dashcore/sentinel
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore/sentinel
# /var/log/dashcore
%dir %attr(700,dashcore,dashcore) %{_localstatedir}/log/dashcore

# sentinel.conf
%config(noreplace) %{_sysconfdir}/dashcore/sentinel.conf
# ...convenience symlink - this is probably really bad form:
#    /var/lib/dashcore/sentinel/sentinel.conf -> /etc/dashcore/sentinel.conf
#%%{_sharedstatedir}/dashcore/sentinel/sentinel.conf --picked up by SPLAT below

# The logs
%attr(644,root,root) /etc/logrotate.d/dashcore-sentinel
%ghost %{_localstatedir}/log/dashcore/sentinel.log

# Code and data directories
%{_sharedstatedir}/dashcore/sentinel/*


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
# Dash Core git repos...
#   * Dash: https://github.com/dashpay/dash
#   * Sentinel: https://github.com/dashpay/sentinel

%changelog
* Mon Apr 9 2018 Todd Warner <t0dd@protonmail.com> 1.1.0-1.2.testing.taw0
- Remove .build_ids... because they conflict all the time.
- _tmpfilesdir and _unitdir don't exist on f25 - not a huge deal, but still.

* Sun Apr 8 2018 Todd Warner <t0dd@protonmail.com> 1.1.0-1.1.testing.taw0
- Refactor sentinel spec
- Versions use more canonical packaging standards.
- Configuration file is in /etc/dashcore/sentinel.conf now (but still symlinked  
  from /var/lib/dashcore/sentinel.conf)
- Contrib tree is restructured a bit to reduce redundancy.
- Updated some information in contrib README and other text.

* Tue Nov 14 2017 Todd Warner <t0dd@protonmail.com> 1.1.0-1.testing.taw
- Spec file tweaks so that this builds on Fedora 27. I don't know the real
- cause of the error, but it is related to debuginfo building. But Sentinel
- doesn't really need debuginfo packages built, so I am just going to nuke them.

* Tue Nov 7 2017 Todd Warner <t0dd@protonmail.com> 1.1.0-0.testing.taw
- Release 1.1 in support of dashcore 0.12.2
- 971aa5e5f4d06ba76e76c9c828402af56f28353254c8db15214ac7071d982de5 sentinel-1.1.0.tar.gz
- d1526682d6103e15f17a3298c76eda00cd0126903accc762ea7c1a3eb806b1f1 dashcore-sentinel-1.1-contrib.tar.gz

* Fri Feb 24 2017 Todd Warner <t0dd@protonmail.com> 1.0.1-0.rc.taw
- Release 1.0.1 - Release Candidate - 4ac8523
- 407c509cc00706645e899dc6fa5bdc1f6ea156381ab8b84d669ed59c1a070fad  sentinel-1.0.1.tar.gz

* Fri Feb 10 2017 Todd Warner <t0dd@protonmail.com> 1.0-2.taw
- Building debuginfo RPMs as well now.

* Mon Feb 06 2017 Todd Warner <t0dd@protonmail.com> 1.0-1.taw
- Fixed a broken file in the contribs that hosed the sentinel.conf file.

* Sun Feb 05 2017 Todd Warner <t0dd@protonmail.com> 1.0-0.taw
- Release 1.0 - d822f41 - in tandem with Dash Core 12.1 release

