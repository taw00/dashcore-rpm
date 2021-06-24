# Dash Core Sentinel Engine (for Masternodes) spec file
# Dash Core reference implementation
# vim:tw=0:ts=2:sw=2:et:
#
# This is the source spec for building the Dash Core Masternode Sentinel
# toolchain required to operate a Dash Masternode. It will build the
# dashcore-sentinel package.
#
# Note about edits within the spec: Any comments beginning with #t0dd are
# associated to future work or experimental elements of this spec file and
# build.
#
# Enjoy. -t0dd

# Package (RPM) name-version-release.
# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]

%define _name_s sentinel
%define _name_dcs dashcore-sentinel
Name: %{_name_dcs}
Summary: A required helper agent for Dash Core Masternodes

%define targetIsProduction 1


# VERSION
%define vermajor 1.6
%define verminor 0
Version: %{vermajor}.%{verminor}

# RELEASE
%define _pkgrel 1
%if ! %{targetIsProduction}
  %define _pkgrel 0.1
%endif

# MINORBUMP
%define minorbump taw

#
# Build the release string (don't edit this)
#

%define snapinfo testing
%if %{targetIsProduction}
  %undefine snapinfo
%endif

# pkgrel will also be defined, snapinfo and minorbump may not be
%define _release %{_pkgrel}
%define includeMinorbump 1
%if ! %{includeMinorbump}
  %undefine minorbump
%endif
%if 0%{?snapinfo:1}
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}
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

# Unarchived source tree structure (extracted in .../BUILD)
#   projectroot              dashcore-sentinel-1.4
#      \_sourcetree            \_sentinel-1.4.0 (github tree example)
#      \_sourcetree_contrib    \_dashcore-sentinel-1.4-contrib
%define projectroot %{_name_dcs}-%{vermajor}
%define sourcetree %{_name_s}-%{version}
%define sourcetree_contrib %{_name_dcs}-%{vermajor}-contrib

Source0: https://github.com/taw00/dashcore-rpm/blob/master/SOURCES/%{sourcetree}.tar.gz
Source1: https://github.com/taw00/dashcore-rpm/blob/master/SOURCES/%{sourcetree_contrib}.tar.gz
Patch0: https://github.com/taw00/dashcore-rpm/blob/master/SOURCES/%{_name_s}-%{vermajor}-fix-SyntaxWarning.patch

# Most of the time, the build system can figure out the requires.
# But if you need something specific...
Requires: dashcore-server >= 0.17.0

# Force Python3 as __python default even if Python2 is present (and it usually is).
# Note, this is going away as an advised path.
%global __python %{__python3}

# For mock environments I sometimes add vim and less so I can introspect
#BuildRequires: tree vim-enhanced less
BuildRequires: findutils sed
%if 0%{?fedora}
BuildRequires: python3-virtualenv
%else
BuildRequires: /usr/bin/virtualenv-3
%endif

# Nuke the auto-requires that rpmbuild will generate because of the
# virtualenv things we do in the build section.
%global __requires_exclude .*/BUILD/.*/venv/bin/python

# If you comment out "debug_package" RPM will create additional RPMs that can
# be used for debugging purposes. I am not an expert at this, BUT ".build_ids"
# are associated to debug packages, and I have lately run into packaging
# conflicts because of them. This is a topic I can't share a whole lot of
# wisdom about, but for now... I turn all that off.
#
# How debug info and build_ids managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
%define debug_package %{nil}
%define _unique_build_ids 1
%define _build_id_links alldebug

# https://fedoraproject.org/wiki/Changes/Harden_All_Packages
%define _hardened_build 1

License: MIT
URL: http://dash.org/
# Note, for example, this will not build on ppc64le
ExclusiveArch: x86_64 i686 i386


%description
Dash Core reference implementation. Dash Core Sentinel Engine is an autonomous
agent for persisting, processing and automating Dash governance objects and
tasks, and for expanded functions in the upcoming Dash release (codename
Evolution).

Sentinel is implemented as a Python application that binds to a local version
dashd instance on each Dash Masternode.

Dash (Digital Cash) is an open-source peer-to-peer cryptocurrency with an
emphasis on serving as an efficient platform for payments and decentralized
applications. Dash offers a form of money that is portable, inexpensive,
divisible and fast. It can be spent securely both online and in-person with
negligible transaction fees. Dash offers instant transactions by default
(InstantSend), more-fungible transactions (CoinJoin), and operates its network
with a model of self-governance and self-funding. This decentralized governance
and budgeting system makes it the first-ever successful decentralized
autonomous organization (DAO).

Learn more at www.dash.org.


%prep
# .../BUILD/dashcore-sentinel-x.y/sentinel-x.y.z/
mkdir -p %{projectroot}
# sourcecode
%setup -q -T -D -a 0 -n %{projectroot}
# contrib
%setup -q -T -D -a 1 -n %{projectroot}
# patch
cd %{sourcetree}
%patch0 -p1
cd ..



%build
# WARNING: This build process pulls down libraries from the internet.
#   This is less than ideal for many reasons.
#   TODO: Build from locally known and signed libraries -- a future endeavor.
#         pyp2rpm looks promising for this.
cd %{sourcetree}
[ -f /usr/bin/virtualenv-3 ] && /usr/bin/virtualenv-3 ./venv || /usr/bin/virtualenv ./venv
./venv/bin/pip3 install -r ./requirements.txt
# Fix paths within various python scripts where they were auto-generated by pip3 install
# Idea stolen from https://github.com/kushaldas/rpm-macros-virtualenv
find . -type f -print0 | xargs -0 sed -i '~s~%{_builddir}/%{projectroot}/%{sourcetree}~%{_sharedstatedir}/dashcore/sentinel~'
# Nuke all the __pycache__ directories as they will create errors once moved
find . -name __pycache__ -type d -print0 | xargs -0 rm -r --
cd ..


%install
# This section starts us in directory .../BUILD/dashcore-sentinel-x.y (projectroot)

# Install / config ancillary files
# Cheatsheet for built-in RPM macros:
# https://fedoraproject.org/wiki/Packaging:RPMMacros
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
# These two are defined in newer versions of RPM (Fedora not el7)
%define _tmpfilesdir %{_usr_lib}/tmpfiles.d
%define _unitdir %{_usr_lib}/systemd/system

# Create directories
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_sysconfdir}/dashcore
install -d %{buildroot}%{_localstatedir}
install -d %{buildroot}%{_localstatedir}/log
install -d -m700 %{buildroot}%{_localstatedir}/log/dashcore
install -d %{buildroot}%{_sharedstatedir}
install -d %{buildroot}%{_sharedstatedir}/dashcore
install -d %{buildroot}%{_sharedstatedir}/dashcore/sentinel
install -d %{buildroot}%{_tmpfilesdir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_mandir}/man1
#install -d -m755 -p %%{buildroot}%%{_sbindir}
#install -d -m755 -p %%{buildroot}%%{_bindir}
#install -d -m755 -p %%{buildroot}%%{_includedir}
#install -d -m755 -p %%{buildroot}%%{_libdir}

cp -a %{sourcetree}/* %{buildroot}%{_sharedstatedir}/dashcore/sentinel/

# Replace core sentinel configuration file with contributed configuration file
# Remove supplied sentinel configuration file
# Place contributed configuration file into /etc/dashcore
# Create symlink to that file...
#   /var/lib/dashcore/sentinel/sentinel.conf -> /etc/dashcore/sentinel.conf
mv %{buildroot}%{_sharedstatedir}/dashcore/sentinel/sentinel.conf %{buildroot}%{_sharedstatedir}/dashcore/sentinel/sentinel.conf.orig-upstream
install -D -m640 %{sourcetree_contrib}/linux/etc-dashcore_sentinel.conf %{buildroot}%{_sysconfdir}/dashcore/sentinel.conf
ln -s %{_sysconfdir}/dashcore/sentinel.conf %{buildroot}%{_sharedstatedir}/dashcore/sentinel/sentinel.conf

# Log files
# ...logrotate file rules
install -D -m644 -p %{sourcetree_contrib}/linux/etc-logrotate.d_dashcore-sentinel %{buildroot}/etc/logrotate.d/dashcore-sentinel
# ...ghosted log files - need to exist in the installed buildroot
touch %{buildroot}%{_localstatedir}/log/dashcore/sentinel.log

# Right now, things are being run out of /var/lib/dashcore/sentinel
#
# Should this program live in /var/lib? Or should it live elsewhere? Good
# questions. The executable is /var/lib/dashcore/sentinel/bin/sentinel.py It's
# an oddity. It probably should live in /usr/sbin (only a
# sysadmin/masternode-admin would run it). But it doesn't. The rest of the
# program should probably live in /var/lib.
#


%files
# This section starts us in directory .../BUILD/dashcore-sentinel-x.y (projectroot)
%defattr(-,dashcore,dashcore,-)
%license %attr(-,root,root) %{sourcetree}/LICENSE
%doc %attr(-,root,root) %{sourcetree}/README.md %{sourcetree_contrib}/linux/README.redhat.md

# Directories
# /etc/dashcore
%dir %attr(750,dashcore,dashcore) %{_sysconfdir}/dashcore
# /var/lib/dashcore
# /var/lib/dashcore/sentinel
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore
%dir %attr(750,dashcore,dashcore) %{_sharedstatedir}/dashcore/sentinel
# /var/log/dashcore
%dir %attr(700,dashcore,dashcore) %{_localstatedir}/log/dashcore

# Code and data directories
%{_sharedstatedir}/dashcore/sentinel/*

# sentinel.conf
# ...convenience symlink - this is probably really bad form:
#    /var/lib/dashcore/sentinel/sentinel.conf -> /etc/dashcore/sentinel.conf
%config(noreplace) %{_sysconfdir}/dashcore/sentinel.conf
# already picked up by %%{_sharedstatedir}/dashcore/sentinel/* directive
#%%{_sharedstatedir}/dashcore/sentinel/sentinel.conf
#%%{_sharedstatedir}/dashcore/sentinel/sentinel.conf.orig-upstream

# The logs
%attr(644,root,root) /etc/logrotate.d/dashcore-sentinel
%ghost %{_localstatedir}/log/dashcore/sentinel.log


%pre
# the venv directory is problematic. Let's forcibly clean it up before an upgrade.
# About scriptlets: https://fedoraproject.org/wiki/Packaging:Scriptlets
# Installs ($1 == 1) and upgrades ($1 == 2)
if [ "$1" -gt 0 ] ; then
  if [ "$1" = 1 ] ; then
    :
  elif [ "$1" = 2 ] ; then
    /usr/bin/rm -rf %{_sharedstatedir}/dashcore/sentinel/venv >> /dev/null 2>&1
  fi
fi

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
if [ -e %{vlds_conf} -a -f %{vlds_conf} -a ! -h %{vlds_conf} ] ; then
   mv %{vlds_conf} %{etcd}/
   ln -s %{etcd_conf} %{vlds_conf}
   chown dashcore:dashcore %{vlds_conf}
   chown -R dashcore:dashcore %{etcd_conf}
   chmod 640 %{etcd_conf}*
fi

exit 0


%post
# About scriptlets: https://fedoraproject.org/wiki/Packaging:Scriptlets
if [ "$1" -gt 0 ] ; then
  # Runs on install ($1 == 1) or upgrade ($1 == 2)
  if   [ "$1" = 1 ] ; then
    # Only runs on install
    :
  elif [ "$1" = 2 ] ; then
    # Only runs on upgrades
    :
  fi
fi

%preun
# Nuke the database and then uninstall the thing. This will ensure the sentinel
# directory is properly cleaned up as well if need be.
# About scriptlets: https://fedoraproject.org/wiki/Packaging:Scriptlets
/usr/bin/rm -f %{_sharedstatedir}/dashcore/sentinel/database/sentinel.db >> /dev/null 2>&1


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
# Dash Core git repos...
#   * Dash: https://github.com/dashpay/dash
#   * Sentinel: https://github.com/dashpay/sentinel

%changelog
* Thu Jun 24 2021 Todd Warner <t0dd_at_protonmail.com> 1.6.0-1.taw
* Thu Jun 24 2021 Todd Warner <t0dd_at_protonmail.com> 1.6.0-0.1.testing.taw
  - 1.6.0 includes a fix for 0.17 masternodes

* Sun May 23 2021 Todd Warner <t0dd_at_protonmail.com> 1.5.1-2.taw
* Sun May 23 2021 Todd Warner <t0dd_at_protonmail.com> 1.5.1-1.1.testing.taw
  - experimenting with cleaning up venv during upgrades. Something conflicts at  
    times and it is not cleaned up properly.  
    Reference https://github.com/taw00/dashcore-rpm/issues/5
  - updated description text

* Wed May 19 2021 Todd Warner <t0dd_at_protonmail.com> 1.5.1-1.taw
* Thu May 6 2021 Todd Warner <t0dd_at_protonmail.com> 1.5.1-0.1.testing.taw
  - https://github.com/dashpay/sentinel/releases/tag/v1.5.1

* Fri Jan 22 2021 Todd Warner <t0dd_at_protonmail.com> 1.5.0-3.taw
* Fri Jan 22 2021 Todd Warner <t0dd_at_protonmail.com> 1.5.0-2.1.testing.taw
  - remove broken rm command in the preun -- it wasn't the right solution

* Thu Jan 21 2021 Todd Warner <t0dd_at_protonmail.com> 1.5.0-2.taw
* Thu Jan 21 2021 Todd Warner <t0dd_at_protonmail.com> 1.5.0-1.1.testing.taw
  - fix prior release date in this spec file (2020, not 2019)
  - cleanup a little more directly the venv tree upon uninstall and upgrades
  - hopefully resolving https://github.com/taw00/dashcore-rpm/issues/5
  - UPDATE: turns out, this version of the RPM was seriously broken because I screwed up a shell scriptlet

* Thu Oct 1 2020 Todd Warner <t0dd_at_protonmail.com> 1.5.0-1.taw
* Thu Oct 1 2020 Todd Warner <t0dd_at_protonmail.com> 1.5.0-0.1.testing.taw
  - 1.5 in support of dashcore 0.16

* Wed May 22 2019 Todd Warner <t0dd_at_protonmail.com> 1.4.0-1.taw
* Wed May 22 2019 Todd Warner <t0dd_at_protonmail.com> 1.4.0-0.1.testing.taw
  - 1.4 in support of dashcore 0.14 and 0.15

* Mon Jan 14 2019 Todd Warner <t0dd_at_protonmail.com> 1.3.0-2.1.testing.taw
  - some minor-ish specfile cleanup

* Mon Dec 03 2018 Todd Warner <t0dd_at_protonmail.com> 1.3.0-2.taw
* Mon Dec 03 2018 Todd Warner <t0dd_at_protonmail.com> 1.3.0-1.1.testing.taw
  - specfile: fixed the source URLs
  - specfile: employed trickery to mute rpmlint's griping about /usr/lib

* Sun Nov 18 2018 Todd Warner <t0dd_at_protonmail.com> 1.3.0-1.taw
* Sun Nov 18 2018 Todd Warner <t0dd_at_protonmail.com> 1.3.0-0.5.testing.taw
  - Nuke all the __pycache__ directories as they will create errors once moved

* Sun Nov 18 2018 Todd Warner <t0dd_at_protonmail.com> 1.3.0-0.4.testing.taw
  - use find and sed to strip the build directory from python scripts  
    generated by the pip install process

* Fri Nov 16 2018 Todd Warner <t0dd_at_protonmail.com> 1.3.0-0.3.testing.taw
  - v1.3.0 official release - updated for dashcore v0.13.0 and v0.12.z
  - https://www.dash.org/forum/threads/sentinel-v1-3-0-release.42068/

* Wed Nov 14 2018 Todd Warner <t0dd_at_protonmail.com> 1.3.0-0.2.testing.taw
* Wed Nov 14 2018 Todd Warner <t0dd_at_protonmail.com> 1.3.0-0.1.testing.taw
  - v1.3.0 - updated for dashcore v0.13.0
  - BuildRequires for virtualenv...  
    RHEL/CentOS: /usr/bin/virtualenv-3  
    Fedora: python3-virtualenv
  - Executable used for virtualenv...  
    RHEL/CentOS: /usr/bin/virtualenv-3  
    Fedora < 29: /usr/bin/virtualenv-3  
    Fedora 29+: /usr/bin/virtualenv  
  - SPEC file: simplified the NVRE building logic

* Tue Jul 03 2018 Todd Warner <t0dd_at_protonmail.com> 1.2.0-1.taw
* Tue Jul 03 2018 Todd Warner <t0dd_at_protonmail.com> 1.2.0-0.4.testing.taw
  - v1.2.0 - updated for dashcore v0.12.3

* Sun Jun 03 2018 Todd Warner <t0dd_at_protonmail.com> 1.2.0-0.3.testing.taw
  - updated for dashcore v0.12.3-rc2

* Wed May 23 2018 Todd Warner <t0dd_at_protonmail.com> 1.2.0-0.2.testing.taw
  - minor spec file changes
  - python3-isms
  - locking down supported architectures w/ ExclusiveArch

* Sat Apr 28 2018 Todd Warner <t0dd_at_protonmail.com> 1.2.0-0.1.testing.taw
  - Test build 1.2.0

* Mon Apr 9 2018 Todd Warner <t0dd_at_protonmail.com> 1.1.0-1.2.testing.taw
  - Remove .build_ids... because they conflict all the time.
  - _tmpfilesdir and _unitdir don't exist on f25 - not a huge deal, but still.

* Sun Apr 8 2018 Todd Warner <t0dd_at_protonmail.com> 1.1.0-1.1.testing.taw
  - Refactor sentinel spec
  - Versions use more canonical packaging standards.
  - Configuration file is in /etc/dashcore/sentinel.conf now (but still symlinked  
    from /var/lib/dashcore/sentinel.conf)
  - Contrib tree is restructured a bit to reduce redundancy.
  - Updated some information in contrib README and other text.

* Tue Nov 14 2017 Todd Warner <t0dd_at_protonmail.com> 1.1.0-1.testing.taw
  - Spec file tweaks so that this builds on Fedora 27. I don't know the real
  - cause of the error, but it is related to debuginfo building. But Sentinel
  - doesn't really need debuginfo packages built, so I am just going to nuke them.

* Tue Nov 7 2017 Todd Warner <t0dd_at_protonmail.com> 1.1.0-0.taw
  - Release 1.1 in support of dashcore 0.12.2

* Tue Nov 7 2017 Todd Warner <t0dd_at_protonmail.com> 1.1.0-0.testing.taw
  - Release 1.1 in support of dashcore 0.12.2 - testing

* Fri Feb 24 2017 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.rc.taw
  - Release 1.0.1 - Release Candidate - 4ac8523

* Fri Feb 10 2017 Todd Warner <t0dd_at_protonmail.com> 1.0-2.taw
  - Building debuginfo RPMs as well now.

* Mon Feb 06 2017 Todd Warner <t0dd_at_protonmail.com> 1.0-1.taw
  - Fixed a broken file in the contribs that hosed the sentinel.conf file.

* Sun Feb 05 2017 Todd Warner <t0dd_at_protonmail.com> 1.0-0.taw
  - Release 1.0 - d822f41 - in tandem with Dash Core 12.1 release

