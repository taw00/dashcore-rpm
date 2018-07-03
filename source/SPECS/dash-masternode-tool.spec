# dash-masternode-tool.spec
#
# This SPEC file serves to configure standard RPM builds for
# dash-masternode-tool (aka DashMasternodeTool).
#
# A Dash Masternode is a Dash cryptocurrency full node with specialized
# features that enable it to operate as a member of the 2nd tier of
# functionality on the Dash Network. Dash Masternode operators collateralize a
# masternode with 1000 dash in a seperate wallet in order to prove ownership.
# This 1000 dash must be held in a full-node wallet (Dash Core reference
# wallet) or in a supported hardware wallet --supported the DashMasternodeTool
# software.
#
# Therefore if Masternode operators wish to hold their 1000 dash in a hardware
# wallet, they must use the DashMastenodeTool software in order to manage the
# wallet interaction with their masternode.
#
# Read more here:
# https://github.com/Bertrand256/dash-masternode-tool/blob/master/README.md
#
# Source - this SPEC file references source archives found here and here:
# https://taw00.github.com/dashcore-rpm
#  - dash-masternode-tool-<version>.tar.gz
#  - dash-masternode-tool-<version-major>-contrib.tar.gz
# ...and here:
# https://github.com/Bertrand256/dash-masternode-tool
#  - dash-masternode-tool-<version>.tar.gz



Name: dash-masternode-tool
%define _name2 DashMasternodeTool
Summary: Manage and collateralize a Dash Masternode with a hardware wallet
#BuildArch: noarch

%define targetIsProduction 1
%define includeMinorbump 1

# Package (RPM) name-version-release.
# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]

# VERSION
%define vermajor 0.9
%define verminor 20
Version: %{vermajor}.%{verminor}

# RELEASE
# if production - "targetIsProduction 1"
%define pkgrel_prod 1

# if pre-production - "targetIsProduction 0"
# eg. 3.1.testing -- pkgrel_preprod should always equal pkgrel_prod-1
%define pkgrel_preprod 0
%define extraver_preprod 1
%define snapinfo testing

# if includeMinorbump
%define minorbump taw0

# Building the release string (don't edit this)...

# release numbers
%undefine _relbuilder_pt1
%if %{targetIsProduction}
  %undefine snapinfo
  %define _pkgrel %{pkgrel_prod}
  %define _relbuilder_pt1 %{pkgrel_prod}
%else
  %define _pkgrel %{pkgrel_preprod}
  %define _extraver %{extraver_preprod}
  %define _relbuilder_pt1 %{_pkgrel}.%{_extraver}
%endif

# snapinfo and repackage (pre-built) qualifier
%undefine _relbuilder_pt2
%if 0%{?sourceIsPrebuilt:1}
  %if ! %{sourceIsPrebuilt}
    %undefine snapinfo_rp
  %endif
%else
  %undefine snapinfo_rp
%endif
%if 0%{?snapinfo_rp:1}
  %if 0%{?snapinfo:1}
    %define _relbuilder_pt2 %{snapinfo}.%{snapinfo_rp}
  %else
    %define _relbuilder_pt2 %{snapinfo_rp}
  %endif
%else
  %if 0%{?snapinfo:1}
    %define _relbuilder_pt2 %{snapinfo}
  %endif
%endif

# put it all together
# pt1 will always be defined. pt2 and minorbump may not be
%define _release %{_relbuilder_pt1}
%if ! %{includeMinorbump}
  %undefine minorbump
%endif
%if 0%{?_relbuilder_pt2:1}
  %if 0%{?minorbump:1}
    %define _release %{_relbuilder_pt1}.%{_relbuilder_pt2}%{?dist}.%{minorbump}
  %else
    %define _release %{_relbuilder_pt1}.%{_relbuilder_pt2}%{?dist}
  %endif
%else
  %if 0%{?minorbump:1}
    %define _release %{_relbuilder_pt1}%{?dist}.%{minorbump}
  %else
    %define _release %{_relbuilder_pt1}%{?dist}
  %endif
%endif

Release: %{_release}
# ----------- end of release building section


# Extracted source tree structure (extracted in .../BUILD)
#   srcroot               dash-masternode-tool-0.9
#      \_srccodetree        \_dash-masternode-tool-0.9.18
#      \_srccodetree2       \_btchip-python-0.1.21
#      \_srccontribtree     \_dash-masternode-tool-0.9-contrib
%define srcroot %{name}-%{vermajor}
%define srccodetree %{name}-%{version}
%define btchip_python_version 0.1.26
%define srccodetree2 btchip-python-%{btchip_python_version}
%define srccontribtree %{name}-%{vermajor}-contrib

# You should use URLs for sources.
# https://fedoraproject.org/wiki/Packaging:SourceURL
# dash-masternode-tool-0.9.z
Source0: https://github.com/Bertrand256/dash-masternode-tool/archive/v%{version}/%{srccodetree}.tar.gz
# dash-masternode-tool-0.9-contrib
%if %{targetIsProduction}
Source1: https://github.com/taw00/dashcore-rpm/blob/master/source/SOURCES/%{srccontribtree}.tar.gz
%else
Source1: https://github.com/taw00/dashcore-rpm/blob/master/source/testing/SOURCES/%{srccontribtree}.tar.gz
%endif
# btchip-python-0.1.z
Source2: https://github.com/Bertrand256/btchip-python/archive/v%{btchip_python_version}/%{srccodetree2}.tar.gz

# Most of the time, the build system can figure out the requires.
# But if you need something specific...
Requires: zenity

# BuildRequires indicates everything you need to build the RPM
BuildRequires: python3-devel python3-virtualenv libusbx-devel libudev-devel
# For debugging purposes...
BuildRequires: tree
# So I can introspect the mock build environment...
#BuildRequires: tree vim-enhanced less
# Required for desktop applications (validation of .desktop and .xml files)
BuildRequires: desktop-file-utils libappstream-glib

# CentOS/RHEL/EPEL can't do "Suggests:"
%if 0%{?fedora:1}
#Suggests:
%endif
%if 0%{?rhel:1}
  %{error:"CENTOS and RHEL are not supported."}
%endif

# obsolete fictitious previous version of package after a rename
#Provides: spec-pattern = 0.9
#Obsoletes: spec-pattern < 0.9

License: MIT
URL: https://github.com/taw00/dashcore-rpm
# Group is deprecated. Don't use it. Left here as a reminder...
# https://fedoraproject.org/wiki/RPMGroups
#Group: Unspecified
# Note, for example, this will not build on ppc64le or any 32bit machines or...
ExclusiveArch: x86_64


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
# https://fedoraproject.org/wiki/Packaging:Guidelines#PIE
%define _hardened_build 1


%description
DashMasternodeTool (aka dash-masternode-tool) enables Dash Masternode owners
to manage their Masternodes from a collateralize-holding hardware wallet.

This tool will allow you to..

* Send the start masternode command if the collateral is controlled by a
  hardware wallet
* Transfer masternode earnings safely, without touching the 1000 Dash
  funding transaction
* Sign messages with a hardware wallet
* Vote on proposals
* Initialize/recover hardware wallets seeds
* Update hardware wallets firmware (Trezor/KeepKey)
* Participate on Dash Testnet

Supported hardware wallets: Trezor (model One and T), KeepKey, Ledger Nano S


%prep
# Prep section starts us in directory .../BUILD -i.e.- {_builddir}
#
# I create a root dir and place the source and contribution trees under it.
# Extracted source tree structure (extracted in .../BUILD)
#   srcroot               dash-masternode-tool-0.9
#      \_srccodetree        \_dash-masternode-tool-0.9.18
#      \_srccodetree2       \_btchip-python-0.1.21
#      \_srccontribtree     \_dash-masternode-tool-0.9-contrib

mkdir %{srcroot}
# sourcecode
%setup -q -T -D -a 0 -n %{srcroot}
# contrib
%setup -q -T -D -a 1 -n %{srcroot}
# btchip-python
%setup -q -T -D -a 2 -n %{srcroot}

cp %{srccontribtree}/build/requirements.txt %{srccodetree}/

/usr/bin/virtualenv-3 -p python3 venv \
 && . venv/bin/activate \
 && pip3 install --upgrade setuptools \
 && pip3 install ./%{srccodetree2}

cd %{srccodetree}
pip3 install -r requirements.txt
cd ..
# For debugging purposes...
cd ../.. ; /usr/bin/tree -df -L 2 BUILD ; cd -



%build
# This section starts us in directory {_builddir}/{srcroot}

## Man Pages - not used as of yet
#gzip %%{buildroot}%%{_mandir}/man1/*.1

cd %{srccodetree}
../venv/bin/pyinstaller --distpath=../dist/linux --workpath=../dist/linux/build dash_masternode_tool.spec
cd ..


%install
# CREATING RPM:
# - install step (comes before files step)
# - This step moves anything needing to be part of the package into the
#   {buildroot}, therefore mirroring the final directory and file structure of
#   an installed RPM.
#
# This section starts us in directory {_builddir}/{srcroot}

# Cheatsheet for built-in RPM macros:
#   _bindir = /usr/bin
#   _sbindir = /usr/sbin
#   _datadir = /usr/share
#   _mandir = /usr/share/man
#   _sysconfdir = /etc
#   _localstatedir = /var
#   _sharedstatedir is /var/lib
#   _prefix = /usr
#   _libdir = /usr/lib or /usr/lib64 (depending on system)
%define _usr_lib /usr/lib
#   https://fedoraproject.org/wiki/Packaging:RPMMacros
# These three are defined in newer versions of RPM (Fedora not el7)
%define _tmpfilesdir %{_usr_lib}/tmpfiles.d
%define _unitdir %{_usr_lib}/systemd/system
%define _metainfodir %{_datadir}/metainfo

# Create directories
install -d %{buildroot}%{_libdir}/%{name}
install -d -m755 -p %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_datadir}/%{name}

# Binaries
install -D -m755 -p %{srccontribtree}/desktop/%{name}-desktop-script.sh %{buildroot}%{_datadir}/%{name}/
install -D -m755 -p ./dist/linux/%{_name2} %{buildroot}%{_datadir}/%{name}/%{_name2}
ln -s %{_datadir}/%{name}/%{_name2} %{buildroot}%{_bindir}/%{name}

# Most use LICENSE or COPYING... not LICENSE.txt
install -D -p %{srccodetree}/LICENSE.txt %{srccodetree}/LICENSE

# Desktop
cd %{srccontribtree}/desktop/
install -D -m644 -p %{name}.hicolor.16x16.png        %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -D -m644 -p %{name}.hicolor.22x22.png        %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
install -D -m644 -p %{name}.hicolor.24x24.png        %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
install -D -m644 -p %{name}.hicolor.32x32.png        %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -D -m644 -p %{name}.hicolor.48x48.png        %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -D -m644 -p %{name}.hicolor.128x128.png      %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
install -D -m644 -p %{name}.hicolor.256x256.png      %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
install -D -m644 -p %{name}.hicolor.512x512.png      %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
install -D -m644 -p %{name}.hicolor.svg              %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

install -D -m644 -p %{name}.highcontrast.16x16.png   %{buildroot}%{_datadir}/icons/HighContrast/16x16/apps/%{name}.png
install -D -m644 -p %{name}.highcontrast.22x22.png   %{buildroot}%{_datadir}/icons/HighContrast/22x22/apps/%{name}.png
install -D -m644 -p %{name}.highcontrast.24x24.png   %{buildroot}%{_datadir}/icons/HighContrast/24x24/apps/%{name}.png
install -D -m644 -p %{name}.highcontrast.32x32.png   %{buildroot}%{_datadir}/icons/HighContrast/32x32/apps/%{name}.png
install -D -m644 -p %{name}.highcontrast.48x48.png   %{buildroot}%{_datadir}/icons/HighContrast/48x48/apps/%{name}.png
install -D -m644 -p %{name}.highcontrast.128x128.png %{buildroot}%{_datadir}/icons/HighContrast/128x128/apps/%{name}.png
install -D -m644 -p %{name}.highcontrast.256x256.png %{buildroot}%{_datadir}/icons/HighContrast/256x256/apps/%{name}.png
install -D -m644 -p %{name}.highcontrast.512x512.png %{buildroot}%{_datadir}/icons/HighContrast/512x512/apps/%{name}.png
install -D -m644 -p %{name}.highcontrast.svg         %{buildroot}%{_datadir}/icons/HighContrast/scalable/apps/%{name}.svg

# dash-masternode-tool.desktop
# https://fedoraproject.org/wiki/Packaging:Guidelines?rd=PackagingGuidelines#Desktop_files
#install -D -m644 -p %%{name}.desktop %%{buildroot}%%{_datadir}/applications/%%{name}.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications/ %{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

# dash-masternode-tool.appdata.xml
# https://fedoraproject.org/wiki/Packaging:AppData
install -D -m644 -p %{name}.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml
cd ../../

## Man Pages - not used as of yet
#install -d %%{buildroot}%%{_mandir}
#install -D -m644 %%{srccodetree}/share/man/man1/* %%{buildroot}%%{_mandir}/man1/

## Bash completion
#install -D -m644 %%{srccontribtree}/bash/%%{name}.bash-completion  %%{buildroot}%%{_datadir}/bash-completion/completions/%%{name}
#install -D -m644 %%{srccontribtree}/bash/%%{name}d.bash-completion %%{buildroot}%%{_datadir}/bash-completion/completions/%%{name}d


%files
# CREATING RPM:
# - files step (final step)
# - This step makes a declaration of ownership of any listed directories
#   or files
# - The install step should have set permissions and ownership correctly,
#   but of final tweaking is often done in this section
#
%defattr(-,root,root,-)
%license %{srccodetree}/LICENSE
%doc %{srccontribtree}/README.about-this-rpm.md
%doc %{srccontribtree}/README.changelog.md
%doc %{srccodetree}/README.md

# Binaries
%{_bindir}/%{name}
%{_datadir}/%{name}/%{_name2}
%{_datadir}/%{name}/%{name}-desktop-script.sh

## Desktop
%{_datadir}/icons/*
%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/%{name}.appdata.xml
#%%{_metainfodir}/%%{name}.metainfo.xml



%pre
# INSTALLING THE RPM:
# - pre section (runs before the install process)
# - system users are added if needed. Any other roadbuilding.
#
# This section starts us in directory .../BUILD/<srcroot>
#


%post
# INSTALLING THE RPM:
# - post section (runs after the install process is complete)
#
#umask 007
## refresh library context
#/sbin/ldconfig > /dev/null 2>&1
## refresh systemd context
#test -e %%{_sysconfdir}/%%{name}/%%{name}.conf && %%systemd_post %%{name}d.service
## refresh firewalld context
#test -f %%{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


%postun
# UNINSTALLING THE RPM:
# - postun section (runs after an RPM has been removed)
#
#umask 007
## refresh library context
#/sbin/ldconfig > /dev/null 2>&1
## refresh firewalld context
#test -f %%{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


%changelog
* Tue Jul 03 2018 Todd Warner <todd_at_protonmail.com> 0.9.20-1.taw
* Tue Jul 03 2018 Todd Warner <todd_at_protonmail.com> 0.9.20-0.1.testing.taw
  - dashcore v12.3 support (protocol 70210)

* Tue Jun 05 2018 Todd Warner <todd_at_protonmail.com> 0.9.19-0.1.testing.taw
  - Updated upstream source: v0.9.19
  - Updated branding for desktop icons.
  - Fixed SourceN URLs to be more RPM standards compliant.
  - Removed some spec file cruft.

* Sun Apr 29 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.18-4.taw
* Sun Apr 29 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.18-3.2.testing.taw
  - Using zenity for the dialogue box.
  - Will choose between ~/.config/dmt or ~/.dmt
  - Logic all fixed. Finally.

* Sat Apr 28 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.18-3.1.testing.taw
  - I broke things with the data-dir... fixing!
  - Added missing .appdata.xml file (required for desktop applications in linux)

* Sat Apr 28 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.18-3.taw
  - Updated stable build.

* Sat Apr 28 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.18-2.1.testing.taw
  - Default --data-dir is now ~/.config/dmt  
  - Upstream default is moving to ~/.dmt, so I am more closely mirroring this.

* Thu Apr 26 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.18-2.taw
  - Updated stable build.

* Thu Apr 26 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.18-1.1.testing.taw
  - specfile: cleaned up the version and release building logic
  - code: updated btchip-python source
  - Pushed the desktop script into /usr/share/ and added a symlink to the actual  
    binary so that a user can call dmt from the commandline and change the  
    default data dir.

* Wed Apr 25 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.18-1.taw
  - Initial stable build.

* Wed Apr 25 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.18-0.2.testing.taw
  - Fix the default config file issues of non-existence and permissions.

* Tue Apr 24 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.18-0.1.testing.taw
  - Initial test package.

