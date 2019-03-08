# %changelog
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

