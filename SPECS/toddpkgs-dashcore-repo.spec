Name:       toddpkgs-dashcore-repo
Version:    1.0
Summary:    Repository configuration to enable management of dashcore packages (Dash Cryptocurrency Core Wallet and Node)

%define targetIsProduction 1

# RELEASE
%define _rel 8
%if ! %{targetIsProduction}
%define _rel 7.1
%endif

%define _snapinfo testing
%define _minorbump taw
%if %{targetIsProduction}
Release:    %{_rel}%{?dist}.%{_minorbump}
%else
Release:    %{_rel}.%{_snapinfo}%{?dist}.%{_minorbump}
%endif

License:    MIT
URL:        https://github.com/taw00/dashcore-rpm
Source0:    https://github.com/taw00/dashcore-rpm/raw/master/source/SOURCES/toddpkgs-dashcore-repo-1.0.tar.gz
BuildArch:  noarch
#BuildRequires:  tree

# CentOS/RHEL/EPEL can't do "Suggests:"
# Update: Don't use suggests. Ever.
#%%if 0%%{?fedora:1}
#Suggests: distribution-gpg-keys-copr
#%%endif


%description
Todd (aka, taw, taw00, t0dd in various communities) packages applications for
Fedora Linux and RHEL/CentOS/EPEL. This package deploys the repository
configuration file necessary to enable on-going management of the (Dash
Cryptocurrency) Dash Core Wallet and Masternode/Full-node RPM package for
Fedora Linux and CentOS and RHEL.

Install this, then...

* For fedora:
  sudo dnf list | dashcore
  sudo dnf install dashcore-client -y --refresh
  ...or...
  sudo dnf install dashcore-server -y --refresh
* For CentOS or RHEL:
  sudo yum clean expire-cache
  sudo yum install dashcore-client -y
  ...or...
  sudo yum install dashcore-server -y

You can edit /etc/yum.repos.d/dashcore.repo (as root) and 'enable=1' or '0'
whether you want the stable or the testing repositories.
...or better yet, for Fedora repos:
  sudo dnf repolist | grep dashcore
  sudo dnf config-manager --set-disabled dashcore-testing
  sudo dnf config-manager --set-enabled dashcore-stable
  sudo dnf repolist | grep dashcore
  sudo dnf list | grep dashcore
..and for CentOS7/RHEL7 (note, EL7 is not supported for Dash Core 0.13):
  sudo yum repolist | grep dashcore
  sudo yum-config-manager --enable dashcore-stable-12.3
  sudo yum-config-manager --disable dashcore-testing
  sudo yum repolist | grep dashcore
  sudo yum list | grep dashcore

Notes about GPG keys:
* An RPM signing key is included. It is used to sign RPMs that I build by
  hand. Namely any *.src.rpm found in github.com/taw00/dashcore-rpm
* RPMs from the copr repositories are signed by fedoraproject build system
  keys.


%prep
%setup -q
# For debugging purposes...
#cd .. ; tree -df -L 1  ; cd -


%build
# no-op


%install
# Builds generically. Will need a disto specific RPM though.
install -d %{buildroot}%{_sysconfdir}/yum.repos.d
install -d %{buildroot}%{_sysconfdir}/pki/rpm-gpg

install -D -m644 todd-694673ED-public-2030-01-04.2016-11-07.asc %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-todd-694673ED-public

%if 0%{?rhel:1}
  %if 0%{?rhel} < 8
    %if %{targetIsProduction}
      install -D -m644 dashcore-el7.repo %{buildroot}%{_sysconfdir}/yum.repos.d/dashcore.repo
    %else
      install -D -m644 dashcore-el7.repo-enabled-testing-repo %{buildroot}%{_sysconfdir}/yum.repos.d/dashcore.repo
    %endif
  %else
  %if 0%{?rhel} < 9
    %if %{targetIsProduction}
      install -D -m644 dashcore-el8.repo %{buildroot}%{_sysconfdir}/yum.repos.d/dashcore.repo
    %else
      install -D -m644 dashcore-el8.repo-enabled-testing-repo %{buildroot}%{_sysconfdir}/yum.repos.d/dashcore.repo
    %endif
  %endif
  %endif
%else
  %if %{targetIsProduction}
    install -D -m644 dashcore-fedora.repo %{buildroot}%{_sysconfdir}/yum.repos.d/dashcore.repo
  %else
    install -D -m644 dashcore-fedora.repo-enabled-testing-repo %{buildroot}%{_sysconfdir}/yum.repos.d/dashcore.repo
  %endif
%endif


%files
#%%config(noreplace) %%attr(644, root,root) %%{_sysconfdir}/yum.repos.d/dashcore.repo
%config %attr(644, root,root) %{_sysconfdir}/yum.repos.d/dashcore.repo
%attr(644, root,root) %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-todd-694673ED-public


%changelog
* Wed Mar 20 2019 Todd Warner <t0dd_at_protonmail.com> 1.0-8.taw
* Wed Mar 20 2019 Todd Warner <t0dd_at_protonmail.com> 1.0-7.1.testing.taw
  - fixed a EL lookup issue

* Thu Feb 07 2019 Todd Warner <t0dd_at_protonmail.com> 1.0-6.1.testing.taw
  - Repos default to 0.13 now
  - refreshed the instruction for enabling and disabling a bit

* Mon Jan 14 2019 Todd Warner <t0dd_at_protonmail.com> 1.0-6.taw
* Mon Jan 14 2019 Todd Warner <t0dd_at_protonmail.com> 1.0-5.1.testing.taw
  - updating the repos to include 0.13.0

* Mon Jan 7 2019 Todd Warner <t0dd_at_protonmail.com> 1.0-5.taw
* Mon Jan 7 2019 Todd Warner <t0dd_at_protonmail.com> 1.0-4.1.testing.taw
  - typo in the instructions in the specfile - doh!

* Mon Dec 17 2018 Todd Warner <t0dd_at_protonmail.com> 1.0-4.taw
* Mon Dec 17 2018 Todd Warner <t0dd_at_protonmail.com> 1.0-3.1.testing.taw
  - enabled_metadata needs to be set to 0 because COPR repos do not managed  
    appstream metadata correctly  
    <https://srvfail.com/packagekit-cant-find-file-in-var-cache-packagekit/>

* Tue Jul 03 2018 Todd Warner <t0dd_at_protonmail.com> 1.0-3.taw
* Tue Jul 03 2018 Todd Warner <t0dd_at_protonmail.com> 1.0-2.2.testing.taw
  - v12.3 repo flipped on

* Sun Jun 03 2018 Todd Warner <t0dd_at_protonmail.com> 1.0-2.1.testing.taw
  - testing repo turned on by default for testing repos ;)

* Tue May 1 2018 Todd Warner <t0dd_at_protonmail.com> 1.0-2.taw
* Tue May 1 2018 Todd Warner <t0dd_at_protonmail.com> 1.0-1.1.testing.taw
  - Commented out the old 12.1 repo. It kept polluting the journal with error  
    messages about missing metadata.

* Mon Apr 16 2018 Todd Warner <t0dd_at_protonmail.com> 1.0-1.taw
  - GA release

* Mon Apr 16 2018 Todd Warner <t0dd_at_protonmail.com> 1.0-0.1.testing.taw
  - Initial test build

