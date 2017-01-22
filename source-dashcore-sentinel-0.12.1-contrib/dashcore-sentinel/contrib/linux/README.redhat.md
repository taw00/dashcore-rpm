# About Sentinel and this RPM package

Dash Core Sentinel is a companion service adding functionality to Dash Core
Masternodes. If you are running the GUI client, or the Dash Core server as a
full node and not a masternode, then Sentinel and this document are irrelevant.

This packaged version of Sentinel assumes a few things about your masternode
configuration.

0. That the masternode is running as a systemd managed service. And therefore,
1. The masternode's `datadir` is located in /var/lib/dashcore
2. The masternode's configuration file, `dash.conf`, is found in
   /etc/dashcore/dash.conf
3. That Sentinel will run as system user `dash`

Therefore, if you intend to run multiple masternodes on one system. Or if you
are operating your masternode from a different data-directory and different
configuration file, this README does not articulate those scenarios.

----

# Using Sentinel

After setting up, configuring, and _fully syncing_ your masternode, you need to.

0. Start the masternode from your collaterolized wallet
1. Edit `/var/lib/dashcore-sentinel/sentinel.conf`
2. Ensure `dash_conf` points at your `dashd`'s `dash.conf` file
   * `dash_conf=$HOME/.dashcore/dash.conf` is the upstream default
   * `dash_conf=/etc/dashcore/dash.conf` is the packaged default and recommended
     for `dashd` running as a systemd managed daemon.
3. Ensure `network=testnet` (or mainnet) dependent on which network you are operating.    
   _**Default right now is testnet** - I believe dash.conf overrides this._
3. Once edited and saved, do this...

Verify everything works (do this as root user) - _note: your masternode must be fully
sync'ed and started by the managing wallet_...
```
SENTINEL_DEBUG=1 cd /var/lib/sentinel && sudo -u dash ./venv/bin/python scripts/crontab.p
```

Then edit the dash system user's crontab...
```
sudo -u dash crontab -e
```

And within that editor, add this line:
```
*/2 * * * * cd /var/lib/dashcore-sentinel && ./venv/bin/python scripts/crontab.py >/dev/null 2>&1
```

Happy Masternoding! -t0dd
