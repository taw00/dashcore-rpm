# Desktop elements for the Dash Core reference implementation

In this directory, you will find various artifacts that are used to flesh out
the linux desktop exerience for the Dash Core Wallet.

UPDATE: Upstream source now includes (most of) the necessary icons. Upstream
binary builds do not though, so the contrib archive still includes the svg
source / scalable icons.

The metadata files conform to the freedesktop.org appstream standards in order
to find and describe the Dash Core applications to the
user.

These images and files are to be installed by a package management system, for
example RPM/DNF or DEB/APT.

For more information about "the standards" please check out these pages...
* <https://www.freedesktop.org/software/appstream/docs/>
* <https://docs.fedoraproject.org/en-US/packaging-guidelines/#_desktop_files>
* <https://docs.fedoraproject.org/en-US/packaging-guidelines/AppData/>
* <https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard>

## Installation...

The desktop images are all installed to these file trees...
```
/usr/share/icons/hicolor/
/usr/share/icons/HighContrast/
```

And they will follow this pattern...
```
/usr/share/icons/hicolor/XXXxYYY/apps/org.dash.dash_core.png
/usr/share/icons/hicolor/scalable/apps/org.dash.dash_core.svg
/usr/share/icons/HighContrast/XXXxYYY/apps/org.dash.dash_core.png
/usr/share/icons/HighContrast/scalable/apps/org.dash.dash_core.svg
```

**Metadata Files**

The metadata files (`.desktop` and `.metainfo.xml`) are used to link the
application to the desktop and operating system in general. They have ability
to be widely translated as well, link to screenshot images and more.  They also
tell the desktop how to kick off a default execution of the application.

Note: The `.desktop` file directs the desktop to call a wrapper script that
sets some needed environment variables instead of just calling the raw wallet
executable.

Note to packagers: Translators are needed. Editors of the text are needed. And
the .xml file links to URLs for screenshots. Those need to be kept current, but
they do fall back gracefully to showing nothing if the links are problematic.

## That's it!

Dash Core, in particular the desktop wallet, can thus be more professionally
deployed. Once you do this, if you search in your desktop for the Dash Core
Wallet wallet, it should show up and have appropriate desktop icons, translated
descriptions, and more available to you.  On my GNOME desktop, I hit the magic
windows key and type "Da..." and there it is. Or just browse for it. Add it to
my favorites, etc.
