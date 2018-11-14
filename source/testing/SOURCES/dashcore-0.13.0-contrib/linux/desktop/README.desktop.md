# Desktop elements for the Dash Core reference implementation

In this directory, you will find images and metadata files that are used to
make the linux desktop exerience (dash-qt) more standardized and complete. The
images are used by most linux desktops to display icons in menuing systems and
for icons on the desktop itself. The icons are created with a breadth of detail
and include high-contrast versions to assist those who are visually impaired.

The metadata files conform to standards that are used by most windowing systems
(example GNOME) in order to find and describe the dash-qt application for the
user.

These images and files are to be installed by a package management system, for
example RPM/DNF or DEB/APT.

For more information about "the standards" please check out these pages...
<https://fedoraproject.org/wiki/Packaging:Guidelines?rd=PackagingGuidelines#Desktop_files>
<https://fedoraproject.org/wiki/Packaging:AppData>
<https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard>

Please note this is not Fedora specific (other distributions should all follow
the standards), but they have some rather decent documentation and those
documents will lead you to many others to include the original specs from many
years ago.

## Installation...

The desktop images are all installed in these file trees...
```
/usr/share/icons/hicolor/
/usr/share/icons/HighContrast/
```

And they will follow this pattern...
```
/usr/share/icons/hicolor/128x128/apps/dash.png
/usr/share/icons/hicolor/64x64/apps/dash.png
/usr/share/icons/hicolor/48x48/apps/dash.png
/usr/share/icons/hicolor/scalable/apps/dash.svg
```

The HighContrast icons follow the same pattern.

The images are named things like dash-hicolor-48.png and need to be copied to
the appropriate place and renamed to pattern application-name.png or .svg. The
application name corresponds to whatever you name the application in the given
metadata files. The system reads the metadata files and knows where to find the
images.

**Metadata Files**

The metadata files are used to link the application to the desktop. They have
ability to be widely translated as well, link to screenshot images and more.
They also tell the desktop how to kick off a default execution of the
application.

To properly install the metadata files, linux distributions come with a
validation script that will lint-check these files for glaring errors.

For the dash.desktop file (it may be called dash-qt.desktop) you do this...
```
cp dash.desktop /usr/share/applications/
desktop-file-validate /usr/share/applications/dash.desktop
```

For the dash.appdata.xml file (it may be called dash-qt.appdata.xml) you do this...
```
cp dash.appdata.xml /usr/share/metainfo/
appstream-util validate-relax --nonet /usr/share/metainfo/dash.appdata.xml
```

Note to packagers: Translators are needed. Editors of the text are needed. And
the .xml file links to URLs for screenshots. Those need to be kept current, but
they do fall back gracefully to showing nothing if the links are problematic.

## That's it!

The Dash GUI can now be more professionally deployed. Once you do this, if you
search in your desktop for the Dash GUI wallet, it should show up and have
appropriate desktop icons, translated descriptions, and more available to you.
On my GNOME desktop, I hit the magic windows key and type "Da..." and there it
is. Or just browse for it. Add it to my favorites, etc.
