For Dash 0.17 there are three patches in play.

1. removes the About QT from the menus, because it is so not part of the application (and there is no licensing reason for it to be there, frankly).
2. fixes a lot of things associated to the newer version of boost (v1.73)
3. fixes an error associated to building against newer version of QT (v5.15)
4. addresses a build path issue (https://github.com/dashpay/dash/pull/4158)

These are all backward compatible for ... some number of versions of the Fedora OS. I am not sure how far back.

To replicate (example using dash-0.17.0.0-rc5):

0. explode the tarball and copy the original

```
tar xvzf dash-0.17.0.0-rc5.tar.gz
cp -a dash-0.17.0.0-rc5 dash-0.17.0.0-rc5-orig
```

1. First patch (About QT removal): copy, edit, and diff

We are going to be copying the tree successively. Copy --> make changes and diff --> copy --> make changes and diff, etc.

```
cp -a dash-0.17.0.0-rc5-orig dash-0.17.0.0-rc5-patch01-remove-about-qt-menu-item
```

File affected:
- src/qt/bitcoingui.cpp

Examine previous patch file associated to this and make the same changes. Then.

```
diff -ruN dash-0.17.0.0-rc5-orig dash-0.17.0.0-rc5-patch01-remove-about-qt-menu-item > dash-0.17-patch01-remove-about-qt-menu-item.patch
```

2. Second patch (bind issue): copy, edit, and diff

We are building upon the prior patch tree.

```
cp -a dash-0.17.0.0-rc5-patch01-remove-about-qt-menu-item dash-0.17.0.0-rc5-patch02-bind-namespace-errors
```

Files affected (one-liners):
- src/init.cpp
- src/scheduler.cpp
- src/test/scheduler_tests.cpp

Files affected (more complicated):
- src/qt/bitcoingui.cpp
- src/qt/clientmodel.cpp
- src/qt/splashscreen.cpp
- src/qt/trafficgraphwidget.cpp
- src/qt/transactiontablemodel.cpp
- src/qt/walletmodel.cpp
- src/rpc/server.cpp
- src/torcontrol.cpp
- src/validation.cpp
- src/validationinterface.cpp

Examine previous patch file associated to this and make the same changes. Then.

```
diff -ruN dash-0.17.0.0-rc5-patch01-remove-about-qt-menu-item dash-0.17.0.0-rc5-patch02-bind-namespace-errors > dash-0.17-patch02-bind-namespace-errors.patch
```

3. Third patch (QPainterPath issue): copy, edit, and diff

We are building upon the patch02 patch tree.

```
cp -a dash-0.17.0.0-rc5-patch02-bind-namespace-errors dash-0.17.0.0-rc5-patch03-QPainterPath-issue
```

File affected:
- src/qt/trafficgraphwidget.cpp

Examine previous patch file associated to this and make the same changes. Then.

```
diff -ruN dash-0.17.0.0-rc5-patch02-bind-namespace-errors dash-0.17.0.0-rc5-patch03-QPainterPath-issue > dash-0.17-patch03-QPainterPath-issue.patch
```

4. Fourth patch (bls-dash package make prefix): copy, edit, and diff

```
cp -a dash-0.17.0.0-rc5-orig dash-0.17.0.0-rc5-patch04-cmake-prefix-fix-for-bls-dash
```

File affected:
- depends/packages/bls-dash.mk

Examine previous patch file associated to this and make the same changes. Then.

```
diff -ruN dash-0.17.0.0-rc5-orig dash-0.17.0.0-rc5-patch04-cmake-prefix-fix-for-bls-dash> dash-0.17-patch04-cmake-prefix-fix-for-bls-dash.patch
```

