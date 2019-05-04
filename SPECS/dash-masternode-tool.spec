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
%define sourceIsBinary 0
%define buildQualifier hotfix2
#%%undefine buildQualifier

# Package (RPM) name-version-release.
# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]

# VERSION
%define vermajor 0.9
%define verminor 23
Version: %{vermajor}.%{verminor}

# RELEASE
%define _pkgrel 3
%if ! %{targetIsProduction}
  %define _pkgrel 2.1
%endif

# MINORBUMP
%define minorbump taw
#%%undefine minorbump

#
# Build the release string - don't edit this
#

%define snapinfo testing
%if %{targetIsProduction}
  %undefine snapinfo
%endif
%if 0%{?buildQualifier:1}
  %define snapinfo %{buildQualifier}
%endif

# have to use _variables because rpm spec macros are easily recursive and break.
%define _snapinfo THIS_VALUE_WILL_BE_REPLACED
%if %{sourceIsBinary}
  %if 0%{?snapinfo:1}
    %define _snapinfo %{snapinfo}.rp
  %else
    %define _snapinfo rp
  %endif
%else
  %if 0%{?snapinfo:1}
    %define _snapinfo %snapinfo
  %else
    %undefine _snapinfo
  %endif
%endif

# pkgrel will be defined, snapinfo and minorbump may not be
%define _release %{_pkgrel}
%if 0%{?_snapinfo:1}
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}.%{_snapinfo}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}.%{_snapinfo}%{?dist}
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


# Extracted source tree structure (extracted in .../BUILD)
# (sourcetree and binaryarchivename will be mutually exclusive)
#   projectroot                      dash-masternode-tool-0.9
#      \_sourcetree                \_dash-masternode-tool-0.9.22
#      \_binaryarchivename         \_DashMasternodeTool (file)
#      \_sourcetree_btchip_python  \_btchip-python-SOME_VERSION
#      \_sourcetree_contrib        \_dash-masternode-tool-0.9-contrib
%define projectroot %{name}-%{vermajor}
%if 0%{?buildQualifier:1}
%define sourcetree %{name}-%{version}-%{buildQualifier}
%define binaryarchivename %{_name2}_%{version}.%{buildQualifier}.linux
%else
%define sourcetree %{name}-%{version}
%define binaryarchivename %{_name2}_%{version}.linux
%endif
#%%define btchip_python_version 0.1.26
%define btchip_python_vermajor master-branch
%define btchip_python_verminor 2019-03-08
%define btchip_python_version %{btchip_python_vermajor}-%{btchip_python_verminor}
#%%define sourcetree_btchip_python btchip-python-%%{btchip_python_version}
%define archivename_btchip_python btchip-python-%{btchip_python_version}
%define sourcetree_btchip_python btchip-python-%{btchip_python_vermajor}
%define sourcetree_contrib %{name}-%{vermajor}-contrib

# dash-masternode-tool-0.9.z
%if %{sourceIsBinary}
Source0: https://github.com/Bertrand256/dash-masternode-tool/archive/v%{version}/%{binaryarchivename}.tar.gz
%else
Source0: https://github.com/Bertrand256/dash-masternode-tool/archive/v%{version}/%{sourcetree}.tar.gz
%endif
# dash-masternode-tool-0.9-contrib
Source1: https://github.com/taw00/dashcore-rpm/blob/master/SOURCES/%{sourcetree_contrib}.tar.gz
# btchip-python-...
#Source2: https://github.com/Bertrand256/btchip-python/archive/v%%{btchip_python_version}/%%{sourcetree_btchip_python}.tar.gz
Source2: https://github.com/taw00/dashcore-rpm/blob/master/SOURCES/%{archivename_btchip_python}.tar.gz

%if ! %{sourceIsBinary}
Requires: zenity
BuildRequires: python3-devel python3-virtualenv
BuildRequires: libusbx-devel libudev-devel
BuildRequires: gcc-c++ cmake
# All these python requirements were an attempt to reduce the python upstream
# fetches by the build. Unfortunately, DMT doesn't attempt to use
# system-installed packages.
#BuildRequires: python2-qt5
#BuildRequires: python3-pyqtchart-devel
#BuildRequires: python3-simplejson python3-mnemonic python3-requests python3-paramiko python3-cryptography python3-more-itertools
%endif

# tree, vim-enhanced, and less for mock build environment introspection
%if ! %{targetIsProduction}
BuildRequires: tree vim-enhanced less findutils
%endif

# Required for desktop applications (validation of .desktop and .xml files)
BuildRequires: desktop-file-utils libappstream-glib

%if 0%{?rhel} && 0%{?rhel} < 8
  %{error: "EL7-based platforms (CentOS7/RHEL7) are not supportable build targets."}
%endif


License: MIT
URL: https://github.com/taw00/dashcore-rpm
ExclusiveArch: x86_64


# How debug info and build_ids are managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
# I turn everything off by default avoid any packaging conflicts. This
# is not correct packaging, but... it's what I do for now.
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
* Transfer any potential masternode earnings safely, without touching the 1000
  Dash funding transaction (assuming collatoral key and payout key are the
  same)
* Sign messages with a hardware wallet
* Vote on proposals (if HW maintains voting key)
* Initialize/recover hardware wallets seeds
* Update hardware wallets firmware (Trezor/KeepKey)
* Participate on Dash Testnet

Supported hardware wallets: Trezor (model One and T), KeepKey, Ledger Nano S


%prep
# Prep section starts us in directory .../BUILD -i.e.- {_builddir}
#
# I create a root dir and place the source and contribution trees under it.
# Extracted source tree structure (extracted in .../BUILD)
#   projectroot                 dash-masternode-tool-0.9
#      \_sourcetree               \_dash-masternode-tool-0.9.22
#      \_sourcetree_btchip_python \_btchip-python-SOME_VERSION
#      \_sourcetree_contrib       \_dash-masternode-tool-0.9-contrib

mkdir -p %{projectroot}
# sourcecode or DashMasternodeTool (binary)
%setup -q -T -D -a 0 -n %{projectroot}
# contrib
%setup -q -T -D -a 1 -n %{projectroot}
# btchip-python
%setup -q -T -D -a 2 -n %{projectroot}

# For debugging purposes...
%if ! %{targetIsProduction}
cd ../.. ; /usr/bin/tree -df -L 2 BUILD ; cd -
%endif

%if ! %{sourceIsBinary}
  # My modified requirements a tad since we use the native QT libraries
  # and include btchip-python
  cp %{sourcetree_contrib}/build/requirements.txt %{sourcetree}/

  [ -f /usr/bin/virtualenv-3 ] && /usr/bin/virtualenv-3 -p python3 ./venv || /usr/bin/virtualenv -p python3 ./venv
  . ./venv/bin/activate

  # Is it pip3? or pip? and does Fedora version matter?
  # Next pip3 command line is to address a bug in pyinstaller, see
  # https://github.com/pyinstaller/pyinstaller/issues/4003  
  # https://stackoverflow.com/questions/54338714/pip-install-pyinstaller-no-module-named-pyinstaller
  ./venv/bin/pip3 install pip==18.1
  ./venv/bin/pip3 install pyinstaller
  ./venv/bin/pip3 install --upgrade setuptools
  ./venv/bin/pip3 install ./%{sourcetree_btchip_python}
  cd %{sourcetree}
  ../venv/bin/pip3 install -r requirements.txt
  cd ..
%else
  mkdir -p %{sourcetree}
  mv DashMasternodeTool %{sourcetree}
%endif

# For debugging purposes...
%if ! %{targetIsProduction}
cd ../.. ; /usr/bin/tree -df -L 2 BUILD ; cd -
%endif



%build
# This section starts us in directory {_builddir}/{projectroot}

%if ! %{sourceIsBinary}
  cd %{sourcetree}
  ../venv/bin/pyinstaller --distpath=../dist/linux --workpath=../dist/linux/build dash_masternode_tool.spec
  cd ..
%endif


%install
# This section starts us in directory {_builddir}/{projectroot}

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
install -D -m755 -p %{sourcetree_contrib}/desktop/%{name}-desktop-script.sh %{buildroot}%{_datadir}/%{name}/
%if ! %{sourceIsBinary}
install -D -m755 -p ./dist/linux/%{_name2} %{buildroot}%{_datadir}/%{name}/%{_name2}
%else
install -D -m755 -p %{sourcetree}/%{_name2} %{buildroot}%{_datadir}/%{name}/%{_name2}
%endif
ln -s %{_datadir}/%{name}/%{_name2} %{buildroot}%{_bindir}/%{name}

# Most use LICENSE or COPYING... not LICENSE.txt
# Now using the copy in sourcetree_contrib
#install -D -p %%{sourcetree}/LICENSE.txt %%{sourcetree}/LICENSE

# Desktop
cd %{sourcetree_contrib}/desktop/
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


%files
%defattr(-,root,root,-)
#%%license %%{sourcetree}/LICENSE
%license %{sourcetree_contrib}/LICENSE
%doc %{sourcetree_contrib}/README.about-this-rpm.md
%doc %{sourcetree_contrib}/README.changelog.md
%if ! %{sourceIsBinary}
%doc %{sourcetree}/README.md
%else
%doc %{sourcetree_contrib}/build/README.md
%endif

# Binaries
%{_bindir}/%{name}
%{_datadir}/%{name}/%{_name2}
%{_datadir}/%{name}/%{name}-desktop-script.sh

## Desktop
%{_datadir}/icons/*
%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/%{name}.appdata.xml
#%%{_metainfodir}/%%{name}.metainfo.xml


%changelog
* Sat May 04 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.23-3.hotfix2.taw
* Sat May 04 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.23-2.1.hotfix2.taw
  - 0.9.23 hotfix2

* Sat Apr 27 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.23-2.taw
* Sat Apr 27 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.23-1.1.testing.taw
  - 0.9.23, but with a versioning fix (aka 0.9.23-a)

* Sat Apr 27 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.23-1.taw
* Sat Apr 27 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.23-0.1.testing.taw
  - 0.9.23

* Mon Apr 15 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.22-4.hotfix6.taw
* Mon Apr 15 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.22-3.1.hotfix6.taw
  - hotfix6

* Fri Mar 08 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.22-3.1.hotfix5.taw
  - hotfix5 - keepkey issue fix
  - refreshed btchip-python sourcetree
  - renamed some variables in the specfile

* Wed Mar 06 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.22-3.hotfix4.taw
* Wed Mar 06 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.22-2.1.hotfix4.taw
  - hotfix2, 3, 4 -- squashing a smattering of small or corner-case bugs

* Mon Feb 25 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.22-2.hotfix1.taw
* Mon Feb 25 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.22-1.1.hotfix1.taw
  - fixes vote results to csv bug

* Sun Feb 24 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.22-1.taw
* Sun Feb 24 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.22-0.1.testing.taw
  - v0.9.22

* Wed Feb 20 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.22-0.1.beta1.taw
  - v0.9.22 beta1

* Tue Feb 05 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.21-1.1.testing.taw
  - Fixed my broken config file sniffing logic in the .sh wrapper script
  - pyinstaller has a bug, therefore I had to add...  
      ./venv/bin/pip3 install pip==18.1  
    The bug is: https://github.com/pyinstaller/pyinstaller/issues/4003  
    Associated: https://stackoverflow.com/questions/54338714/pip-install-pyinstaller-no-module-named-pyinstaller

* Mon Jan 14 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.21-1.taw
* Mon Jan 14 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.21-1.taw
* Mon Jan 14 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.21-0.4.testing.taw
* Mon Jan 14 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.21-0.3.testing.taw
* Sun Jan 13 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.21-0.2.testing.taw
* Sun Jan 13 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.21-0.1.testing.taw
  - update in support of dashcore 0.13
  - spec file cleanup

* Wed Nov 14 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.20-3.1.testing.taw
  - updated for Fedora 29... -- this version never worked.
  - BuildRequires for virtualenv:  
    RHEL/CentOS: /usr/bin/virtualenv-3  (EL7 not supported anyway)  
    Fedora: python3-virtualenv
  - Executable used for virtualenv:
    RHEL/CentOS: /usr/bin/virtualenv-3  (EL7 not supported anyway)  
    Fedora < 29: /usr/bin/virtualenv-3  
    Fedora 29+: /usr/bin/virtualenv  

* Sun Aug 12 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.20-3.taw
* Sun Aug 12 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.20-2.1.testing.taw
  - attempting build from source again
  - added README.md back in

* Sun Aug 12 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.20-2.rp.taw
* Sun Aug 12 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.20-1.1.testing.rp.taw
  - repackaging binary build from upstream until I figure out why I am  
    getting a missing "coins.json" error.

* Tue Jul 03 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.20-1.taw
* Tue Jul 03 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.20-0.1.testing.taw
  - dashcore v12.3 support (protocol 70210)

* Tue Jun 5 2018 Todd Warner <t0dd_at_protonmail.com> 0.9.19-0.1.testing.taw
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

