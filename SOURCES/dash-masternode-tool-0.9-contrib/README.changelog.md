# %changelog
* Thu Oct 03 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.26-4.hotfix2.taw
* Thu Oct 03 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.26-3.1.hotfix2.taw
  - updated requirements.txt
  - version.txt file is always unreliable so I update it manually with this  
    version build. In the future, I need to edit this in place with sed. But  
    not today.

* Thu Oct 03 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.26-3.hotfix2.taw
* Thu Oct 03 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.26-2.1.hotfix2.taw
* Thu Aug 22 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.26-2.hotfix1.taw
* Thu Aug 22 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.26-1.1.hotfix1.taw
* Tue Aug 20 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.26-1.taw
* Tue Aug 20 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.26-0.1.testing.taw
  - 0.9.26

* Thu Jul 18 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.25-3.hotfix2.taw
* Thu Jul 18 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.25-2.1.hotfix2.taw
  - 0.9.25 hotfix2

* Fri Jul 12 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.25-2.hotfix1.taw
* Fri Jul 12 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.25-1.1.hotfix1.taw
  - 0.9.25 hotfix1

* Tue Jul 02 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.25-1.taw
* Tue Jul 02 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.25-0.1.taw
  - 0.9.25

* Fri May 24 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.24-1.taw
* Fri May 24 2019 Todd Warner <t0dd_at_protonmail.com> 0.9.24-0.1.taw
  - 0.9.24 (using 0.9.24a source tarball)

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
* Sun Apr 29 2018 Todd Warner <t0dd@protonmail.com> 0.9.18-3.2.testing.taw[n]
- Using zenity for the dialogue box.
- Will choose between ~/.config/dmt or ~/.dmt
- Logic all fixed. Finally.

* Sat Apr 28 2018 Todd Warner <t0dd@protonmail.com> 0.9.18-3.1.testing.taw[n]
- I broke things with the data-dir... fixing!
- Added missing .appdata.xml file (required for desktop applications in linux)

* Sat Apr 28 2018 Todd Warner <t0dd@protonmail.com> 0.9.18-3.taw[n]
- Updated stable build.

* Sat Apr 28 2018 Todd Warner <t0dd@protonmail.com> 0.9.18-2.1.testing.taw[n]
- Default --data-dir is now ~/.config/dmt  
- Upstream default is moving to ~/.dmt, so I am more closely mirroring this.

* Thu Apr 26 2018 Todd Warner <t0dd@protonmail.com> 0.9.18-2.taw[n]
- Updated stable build.

* Thu Apr 26 2018 Todd Warner <t0dd@protonmail.com> 0.9.18-1.1.testing.taw[n]
- specfile: cleaned up the version and release building logic
- code: updated btchip-python source
- Pushed the desktop script into /usr/share/ and added a symlink to the actual  
  binary so that a user can call dmt from the commandline and change the  
  default data dir.

* Wed Apr 25 2018 Todd Warner <t0dd@protonmail.com> 0.9.18-1.taw[n]
- Initial build.

* Wed Apr 25 2018 Todd Warner <t0dd@protonmail.com> 0.9.18-0.2.testing.taw[n]
- Fix the default config file issues of non-existence and permissions.

* Tue Apr 24 2018 Todd Warner <t0dd@protonmail.com> 0.9.18-0.1.testing.taw[n]
- Initial test package.

