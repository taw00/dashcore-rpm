Name:		toddpkgs-dashcore-repo
Version:	1.0
Release:	1.1.testing%{?dist}.taw0
Summary:	Repository configuration to enable management of dashcore packages (Dash Cryptocurrency Core Wallet and Node)

Group:		System Environment/Base
License:	MIT
URL:		https://github.com/taw00/dashcore-rpm
Source0:	https://raw.githubusercontent.com/taw00/dashcore-rpm/master/source/SOURCES/toddpkgs-dashcore-repo-1.0.tar.gz
BuildArch:	noarch
#BuildRequires:  tree

# CentOS/RHEL/EPEL can't do "Suggests:"
%if 0%{?fedora:1}
Suggests:	distribution-gpg-keys-copr
%endif


%description
Todd (aka, taw, taw00, t0dd in various communities) packages applications for
Fedora Linux and RHEL/CentOS/EPEL. This package deploys the repository
configuration file necessary to enable on-going management of the (Dash
Cryptocurrency) Dash Core Wallet and Masternode/Full-node RPM package for
Fedora Linux and CentOS and RHEL.

Install this, then...

* For fedora:
  sudo dnf install dashcore -y --refresh
* For CentOS or RHEL:
  sudo yum clean expire-cache
  sudo yum install dashcore -y

You can edit /etc/yum.repos.d/dashcore.repo (as root) and 'enable=1' or '0'
whether you want the stable or the testing repositories.

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
  install -D -m644 dashcore-epel.repo %{buildroot}%{_sysconfdir}/yum.repos.d/dashcore.repo
%else
  #%%if 0%{?fedora:1}
  # Punt and assume dnf: Make this potentially useable beyond Fedora and CentOS/RHEL
  install -D -m644 dashcore-fedora.repo %{buildroot}%{_sysconfdir}/yum.repos.d/dashcore.repo
  #%%endif
%endif


%files
#%%config(noreplace) %%attr(644, root,root) %%{_sysconfdir}/yum.repos.d/dashcore.repo
%config %attr(644, root,root) %{_sysconfdir}/yum.repos.d/dashcore.repo
%attr(644, root,root) %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-todd-694673ED-public


%changelog
* Tue May 1 2018 Todd Warner <t0dd at protonmail.com> 1.0-1.1.testing.taw[n]
- Commented out the old 12.1 repo. It kept polluting the journal with error  
  messages about missing metadata.
- af7300b59589b0e93e411a64be433a9923e9c53b3314326d59566261db29a0c3  toddpkgs-dashcore-repo-1.0.tar.gz

* Mon Apr 16 2018 Todd Warner <t0dd at protonmail.com> 1.0-1.taw[n]
- GA release

* Mon Apr 16 2018 Todd Warner <t0dd at protonmail.com> 1.0-0.1.testing.taw[n]
- Initial test build
- 2bd69f2980df5985694a003159d202bbf6b7b01849d152c4bb10d8f42728017e  toddpkgs-dashcore-repo-1.0.tar.gz

