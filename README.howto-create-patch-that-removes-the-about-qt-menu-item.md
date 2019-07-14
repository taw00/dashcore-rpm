## Remove "About QT" from GUI Wallet (dash-qt)

I like to remove the "About QT" menu-item from from GUI wallet. It is
frivolous and takes away from the "user experience".

This is how you create the patch to do it (see dash.spec for RPM build
instructions). I only do it in the testing version of dash right now.

NOTE: I really should make a script of this.

```
mkdir x ; cd x
# Download dash-<version>.tar.gz
tar -xvzf dash-<version>.tar.gz
cp -a dash-<version> dash-<version>.orig
```

Edit the file with the stupid menu item...
```
vim dash-<version>/src/qt/bitcoingui.cpp
```

Then, find and replace this `addAction` method call and replace it...
```
-    help->addAction(aboutQtAction);
+    // "About QT" is "implementation detail" -- commenting out -t0dd
+    //help->addAction(aboutQtAction);
```

Create the patch...
```
diff -urN dash-<version>.orig dash-<version> > dash-<vermajor>-remove-about-qt-menu-item.patch
```

Copy patch to `~/git/taw00/dashcore-rpm/SOURCES/`
