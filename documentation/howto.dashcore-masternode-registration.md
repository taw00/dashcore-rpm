# HowTo: Register a Dash Core version 0.13.0 Masternode

These instructions are specific to node, masternode, and wallet users running
the software on Fedora, ~~CentOS, or RHEL~~ (i386 and x86_64) plugged into the
~~`yum`~~ or `dnf` install and update process described in other documentation
found at <https://github.com/taw00/dashcore-rpm>. Dash Core builds for Fedora
27, RHEL7, or CentOS7 will no longer be available as of v0.13.0.

Version 0.13.0 merges two models of registering a masternode on the network. The old model (much of PART 2 below) will fall away eventually and make way for the new model alone (PART 3 below).

**The old model:** proof of 1000 dash and secret shared between wallet and node.

**The new model:** proof of 1000 dash; identification of dash addresses for reward payouts, operations, ownership, and voting; a shared secret; and registration of the configuration to the blockchain.

**SUMMARY OF STEPS:**

<!-- TOC START min:2 max:3 link:true update:true -->
- [PART 1: Install the software components](#part-1-install-the-software-components)
  - [[1] Install a Dash Core wallet (or use a hardware wallet)](#1-install-a-dash-core-wallet-or-use-a-hardware-wallet)
  - [[2] Deploy and configure a Dash Core node](#2-deploy-and-configure-a-dash-core-node)
- [PART 2: Configure the wallet and masternode (old school)](#part-2-configure-the-wallet-and-masternode-old-school)
  - [[3] Send 1000 Dash (the collateral) to the wallet](#3-send-1000-dash-the-collateral-to-the-wallet)
  - [[4] Generate a private "masternode key" via the wallet (a shared secret)](#4-generate-a-private-masternode-key-via-the-wallet-a-shared-secret)
  - [[5] Configure the wallet and the masternode](#5-configure-the-wallet-and-the-masternode)
  - [[6] Configure Dash Sentinel](#6-configure-dash-sentinel)
  - [[7] Issue a remote start command from the wallet to the masternode](#7-issue-a-remote-start-command-from-the-wallet-to-the-masternode)
  - [[8] Monitor masternode enablement status](#8-monitor-masternode-enablement-status)
- [PART 3: Configure the masternode (new 0.13.0 "DIP003" compatible)](#part-3-configure-the-masternode-new-0130-dip003-compatible)
  - [[9] Generate a BLS key-pair & configure the masternode with the secret key](#9-generate-a-bls-key-pair--configure-the-masternode-with-the-secret-key)
  - [[10] Determine owner address, voter address, and payout address](#10-determine-owner-address-voter-address-and-payout-address)
  - [[11] Prepare a "special transaction" that encapsulating masternode-relevant information (ownership, voting, payout)](#11-prepare-a-special-transaction-that-encapsulating-masternode-relevant-information-ownership-voting-payout)
  - [[12] Sign the "special transaction" message (generate signature hash)](#12-sign-the-special-transaction-message-generate-signature-hash)
  - [[13] Register the masternode on the blockchain (submit transaction and validating signature)](#13-register-the-masternode-on-the-blockchain-submit-transaction-and-validating-signature)
- [WHEW!!! ALL DONE!](#whew-all-done)

<!-- TOC END -->

> _**Credit:** Much of this documentation was inspired by the [good
work](<https://docs.dash.org/en/latest/masternodes/maintenance.html#generate-a-bls-key-pair>)
of the Dash Core documentation team._

---

## PART 1: Install the software components

### [1] Install a Dash Core wallet (or use a hardware wallet)

If you have already done this, skip this step. Obviously. Otherwise, read this document for more information: TODO_INSERT_LINK_HERE

### [2] Deploy and configure a Dash Core node

If you have one already set up, skip this step, or see [these instructions](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.dashcore-node-setup.systemd.md).


---


## PART 2: Configure the wallet and masternode (old school)

### [3] Send 1000 Dash (the collateral) to the wallet

If you have already done this, skip this step. Obviously. But keep the 1000 Dash transaction information handy and the address that received it.

If you have not done this already...

Send as a lump sum, 1000 DASH to a wallet (Dash Core or a hardware wallet). Save the receiving address somewhere. It should look something like: `XMArVugC51J6WRkAVJpAwi2x6ecr4xvazH` (and testnet addresses start with a `Y`).

Dash Core wallet instructions: Retrieve the transaction information associated
to that 1000 DASH...

- In the graphical client: Tools > Debug Console: `masternode outputs`
- On the commandline (wallet): `dash-cli masternode outputs`

The relevant output will look something like this:
```
b34ad623453453456423454643541325c98d2f8b7a967551f31dd7cefdd67457 1
```

Take note of (store somewhere) the receiving address, transaction ID, and index (usually a 1 or 0) for future use.


### [4] Generate a private "masternode key" via the wallet (a shared secret)

If this is an existing masternode, you already have this and it is configured
on the masternode as `masternodeprivkey=THE_KEY` and also exists in the wallet's `masternode.conf` file.

If this is a new masternode, this is generated by the graphical wallet via:
Tools > Debug Console: `masternode genkey`. The results will look something like this: `92yZY5b8bYD5G2Qh1C7Un6Tf3TG3mH4LUZha2rdj3QUDGHNg4W9`

### [5] Configure the wallet and the masternode

The relevant info you have (these are examples only, of course)...

- Masternode IP:PORT: `93.184.216.34:9999`
- `masternodeprivkey`: `92yZY5b8bYD5G2Qh1C7Un6Tf3TG3mH4LUZha2rdj3QUDGHNg4W9`
- Funding transaction ID: `b34ad623453453456423454643541325c98d2f8b7a967551f31dd7cefdd67457`
- Funding transaction index: `1`

**Wallet:** Create a file called `masternode.conf` in the `~/.dashcore/`
directory (or for testnet the `~/.dashcore/testnet3/` directory) with contents:
```
# <alias> <ip:port> <masternodeprivkey> <collateralHash> <collateralIndex>
mn1 93.184.216.34:9999 92yZY5b8bYD5G2Qh1C7Un6Tf3TG3mH4LUZha2rdj3QUDGHNg4W9 b34ad623453453456423454643541325c98d2f8b7a967551f31dd7cefdd67457 1
```

That "alias" can be anything you want it to be. It's a label.

*Restart your wallet after configuration.*

**Masternode:**

Edit the node's `dash.conf` file. That file is found either in the `~/.dashcore/` directory (running `dashd` as a normal user) or the `/etc/dashcore/` (running `dashd` as a `systemd` service).

Uncomment and set these values: `masternode`, `externalip`, and `masternodeprivkey`:
```
masternode=1
externalip=93.184.216.34
masternodeprivkey=92yZY5b8bYD5G2Qh1C7Un6Tf3TG3mH4LUZha2rdj3QUDGHNg4W9
```

Save the file and then *restart the node*...
- If running as a normal user: `dash-cli stop ; pause 5 ; dashd`
- If running as a `systemd` service: `sudo systemctl restart dashd`

### [6] Configure Dash Sentinel

There are really two services associated to a masternode, the node itself and a
"sentinel" that performs certain actions and manages expanded processes for the
network. It was already installed when your dashcore-server package was
installed. You just have to turn it on and edit crontab for the `dash` system
user so that it executes every five minutes...

_**Configure it to run on testnet or mainnet...**_

Edit the `/var/lib/dashcore/sentinel/sentinel.conf` file and set either
`network=testnet` or `network=mainnet`

_**Run it for the first time...**_

```
sudo -u dashcore -- bash -c "cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py"
```

It should create a database and populate it.

Run it again...
```
sudo -u dashcore -- bash -c "cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py"
```

There should be no output.

> Note, if something seems to be going wrong, set SENTINEL_DEBUG=1 and try to
> make sense of the output
>
> ```
> sudo -u dashcore -- bash -c "cd /var/lib/dashcore/sentinel && SENTINEL_DEBUG=1 venv/bin/python bin/sentinel.py
> ```

_**Edit cron and add a "run it every minute" entry**_

On the commandline, edit `crontab` &mdash; notice, that we, like in most
commands, are doing it as the `dashcore` system user...

```
sudo -u dashcore EDITOR="nano" crontab -e
```

...add these lines, save and exit...

```
#SENTINEL_DEBUG=1
* * * * * { cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py ; } >> /var/log/dashcore/sentinel.log 2>&1
```

### [7] Issue a remote start command from the wallet to the masternode

You aren't starting the node. You are triggering a start of that node operating
as a masternode.

In the graphical wallet:
- Navigate the menus: Tools > Debug console
- Issue the start command (if "mn1" is your masternode alias):
  `masternode start-alias mn1`

If on the commandline: `dash-cli masternode start-alias mn1`

Alternatively, you can start all masternodes (if you have multiple) with:
  `masternode start-missing`

If the command was sent successfully, you should see... "successful" or
something similar. This means the command was sent successfully, not that the
masternode was truly started.

**Recommendation: Once you have issued this command, SHUT DOWN YOUR WALLET.
There is 1000 DASH associated to that wallet. There is no reason to keep it
online for very long. Shut it down.**

### [8] Monitor masternode enablement status

Do this on the masternode itself...

What you are looking for is ENABLED to be displayed. This can take up to 15
minutes or so. You can really do this from the wallet _or_ the masternode
itself.

From the commandline do this (this is an example; use your masternode's IP
address)...
```
sudo -u dashcore watch -n10 "dash-cli -conf=/etc/dashcore/dash.conf masternode list full | grep 93.184.216.34"
```

Continue to monitor the enablement status. The status should start as
`PRE_ENABLED`, maybe move to `SENTINEL_PING_EXPIRED`, but finally it should
settle on `ENABLED`. If your wallet failed to restart it, it will say something
like `NEW_START_REQUIRED`

&nbsp;

While that is going on in one terminal, open up another terminal and...

---

## PART 3: Configure the masternode (new 0.13.0 "DIP003" compatible)

### [9] Generate a BLS key-pair & configure the masternode with the secret key

As of version 0.13.0, a new signature mechanism is used to manage masternodes. It uses a cryptographic scheme called [BLS signatures](https://en.wikipedia.org/wiki/Boneh%E2%80%93Lynn%E2%80%93Shacham). The public key is used to sign a message that contains all that configuration information and the private key is added to the masternode's configuration file.

Note: The BLS key pair is generated independently of the wallet or masternode. You can generate it from either. You use the `bls` command option in the wallet "Tools > Debug console" or via the `dash-cli` on either wallet or node...

Example using graphical wallet debug console (Tools > Debug console): `bls
generate`

Example using `dash-cli` on the commandline on a masternode (systemd configuration): `sudo -u dashcore dash-cli bls generate`

Example using `dash-cli` on the commandline on a masternode (dashd run as normal user configuration): `dash-cli bls generate`

Example output:
```
{
  "secret": "565950700d7bdc6a9dbc9963920bc756551b02de6e4711eff9ba6d4af59c0101",
  "public": "01d2c43f022eeceaaf09532d84350feb49d7e72c183e56737c816076d0e803d4f86036bd4151160f5732ab4a461bd127"
}
```

These are the `masternodeblsprivkey` (the secret/private key) and `operatorPubKey` (public key) respectively.

Edit the masternode's `dash.conf` file (ether `~/.dashcore/dash.conf` or
`/etc/dashcore/dash.conf` -- see "PART 2" above). Add this line to that file
and restart the masternode:
```
masternodeblsprivkey=565950700d7bdc6a9dbc9963920bc756551b02de6e4711eff9ba6d4af59c0101
```

Don't forget to restart the masternode service (see "PART 2" for an example).

**Store those keys somewhere safe**
These keys are not stored for you, per ce. Secure them in a safe place, along with the rest of this data. That is the only place the secret/private key is
used.

### [10] Determine owner address, voter address, and payout address

This is where things can get confusing. You need values for these concepts...

- `ownerKeyAddr`: the owner of that 1000 dash (but not the collateral address
  from step 1) -- generated from the wallet
- `votingKeyAddr`: the person who has the power to vote. Often the same value as
  `ownerKeyAddr`. If different than `ownerKeyAddr` the address can be generated from another wallet (a voting delegate).
- `payoutAddress`: the dash address for the masternode rewards -- any dash
  address.

It gets even more complicated, but for now, let's focus on those values.

1. Generate `ownerKeyAddr`. In the wallet: `getnewaddress` or on the
   commandline: `dash-cli getnewaddress`
2. Get a `votingKeyAddr` from your voting delegate (they will do a
  `getnewaddress`) **...or (for old behavior)...** If you want to continue
  voting, plan to keep `votingKeyAddr` the same as `ownerKeyAddr`.
3. Determine a `payoutAddress`. This can be any address. Generate a new one,
   **...or (for old behavior)...** use the collateral address from top-level
   step [1].

**Information we have thus far (and will need!)...**
- `operatorPubKey`: `01d2c43f022eeceaaf09532d84350feb49d7e72c183e56737c816076d0e803d4f86036bd4151160f5732ab4a461bd127`
- `masternodeprivkey`: `92yZY5b8bYD5G2Qh1C7Un6Tf3TG3mH4LUZha2rdj3QUDGHNg4W9`
- Masternode IP:PORT: `93.184.216.34:9999`
- Collateral information:
  - Receiving address: `XMArVugC51J6WRkAVJpAwi2x6ecr4xvazH`
  - `collateralHash` or Transaction ID: `b34ad623453453456423454643541325c98d2f8b7a967551f31dd7cefdd67457`
  - `collateralIndex` or Transaction (Tx) Output Index: `1`

**Three use cases...**

*Use case 1: I want to continue the old behavior:*

- `ownerKeyAddr`: `getnewaddress`  
  Example result: `XoVAtG8tW6hwcbqVJp1A9caKwqWMpg9oB2`
- `votingKeyAddr`: use the same address  
  Example result: `XoVAtG8tW6hwcbqVJp1A9caKwqWMpg9oB2`
- `payoutAddress`: use collateral receiving address from before  
  Example: `XMArVugC51J6WRkAVJpAwi2x6ecr4xvazH`

*Use case 2: I want to pay to a different address, but for now _not_ delegate my vote:*

- `ownerKeyAddr`: `getnewaddress`  
  Example result: `XoVAtG8tW6hwcbqVJp1A9caKwqWMpg9oB2`
- `votingKeyAddr`: use the same address  
  Example result: `XoVAtG8tW6hwcbqVJp1A9caKwqWMpg9oB2`
- `payoutAddress`: use new address ... `getnewaddress` (or any wallet address)  
  Example: `XwSrNFimUZbY58Sx17YiSLPAvPToxitZr1`

*Use case 3: I want to pay to a different address, and delegate my vote:*  
... the same as above, but change out that voter's address.

- `ownerKeyAddr`: `getnewaddress`  
  Example result: `XoVAtG8tW6hwcbqVJp1A9caKwqWMpg9oB2`
- `votingKeyAddr`: address of voter who `getnewaddress`'ed from their wallet  
  Example result: `XbV8Xc4CfQwRhY3cYHaGMxiyxzciP49BB`
- `payoutAddress`: use new address ... `getnewaddress` (or any wallet address)  
  Example: `XwSrNFimUZbY58Sx17YiSLPAvPToxitZr1`

Note: There is also an optional `feeSourceAddress` value ... but we're going to
ignore that for now and maybe revisit that at a later date. -- TODO


### [11] Prepare a "special transaction" that encapsulating masternode-relevant information (ownership, voting, payout)

Now we use just about all those keys and data we have been hanging onto.

(1) Prepare a ["special
transaction"](https://github.com/dashpay/dips/blob/master/dip-0002.md) that
encapsulates all that data...

We will now prepare an unsigned ProRegTx special transaction using the `protx
register_prepare` command. This command has the following syntax:

```
protx register_prepare collateralHash collateralIndex ipAndPort ownerKeyAddr
  operatorPubKey votingKeyAddr operatorReward payoutAddress (feeSourceAddress)
```

**Example from use case 1 above:**  
*...format it all on one line (remove the "\'s" and newlines)*
```
protx register_prepare \
b34ad623453453456423454643541325c98d2f8b7a967551f31dd7cefdd67457 \
1 \
93.184.216.34:9999 \
XoVAtG8tW6hwcbqVJp1A9caKwqWMpg9oB2 \
01d2c43f022eeceaaf09532d84350feb49d7e72c183e56737c816076d0e803d4f86036bd4151160f5732ab4a461bd127 \
XoVAtG8tW6hwcbqVJp1A9caKwqWMpg9oB2 \
0 \
XMArVugC51J6WRkAVJpAwi2x6ecr4xvazH
```

All on one line, it would look like this:
```
protx register_prepare b34ad623453453456423454643541325c98d2f8b7a967551f31dd7cefdd67457 1 93.184.216.34:9999 XoVAtG8tW6hwcbqVJp1A9caKwqWMpg9oB2 01d2c43f022eeceaaf09532d84350feb49d7e72c183e56737c816076d0e803d4f86036bd4151160f5732ab4a461bd127 XoVAtG8tW6hwcbqVJp1A9caKwqWMpg9oB2 0 XMArVugC51J6WRkAVJpAwi2x6ecr4xvazH
```

**Example from use case 3 above:**
```
protx register_prepare \
b34ad623453453456423454643541325c98d2f8b7a967551f31dd7cefdd67457 \
1 \
93.184.216.34:9999 \
XoVAtG8tW6hwcbqVJp1A9caKwqWMpg9oB2 \
01d2c43f022eeceaaf09532d84350feb49d7e72c183e56737c816076d0e803d4f86036bd4151160f5732ab4a461bd127 \
XbV8Xc4CfQwRhY3cYHaGMxiyxzciP49BB \
0 \
XwSrNFimUZbY58Sx17YiSLPAvPToxitZr1
```

...

**The output would looks something like this (use case 3):**

```
{
  "tx": "030001000191def1f8bb265861f92e9984ac25c5142ebeda44901334e304c447dad5adf6070000000000feffffff0121dff505000000001976a9149e2deda2452b57e999685cb7dabdd6f4c3937f0788ac00000000d1010000000000c7fd27022913dd8505ae701e0fd56625c3fa9d2ff47802225faae562389e492c0100000000000000000000000000ffff8c523b334e1fad8e6259e14db7d05431ef4333d94b70df1391c601d2c43f022eeceaaf09532d84350feb49d7e72c183e56737c816076d0e803d4f86036bd4151160f5732ab4a461bd127ad8e6259e14db7d05431ef4333d94b70df1391c600001976a914adf50b01774202a184a2c7150593442b89c212e788acf8d42b331ae7a29076b464e61fdbcfc0b13f611d3d7f88bbe066e6ebabdfab7700",
  "collateralAddress": "XPd75LrstM268Sr4hD7RfQe5SHtn9UMSEG",
  "signMessage": "XwSrNFimUZbY58Sx17YiSLPAvPToxitZr1|0|XbV8Xc4CfQwRhY3cYHaGMxiyxzciP49BB|XoVAtG8tW6hwcbqVJp1A9caKwqWMpg9oB2|54e34b8b996839c32f91e28a9e5806ec5ba5a1dadcffe47719f5b808219acf84"
}
```

### [12] Sign the "special transaction" message (generate signature hash)

Next we will use the `collateralAddress` and `signMessage` fields to sign the message: `signmessage <collateralAddress> <signMessage>` ...or...

```
signmessage \
XPd75LrstM268Sr4hD7RfQe5SHtn9UMSEG \
XwSrNFimUZbY58Sx17YiSLPAvPToxitZr1|0|XbV8Xc4CfQwRhY3cYHaGMxiyxzciP49BB|XoVAtG8tW6hwcbqVJp1A9caKwqWMpg9oB2|54e34b8b996839c32f91e28a9e5806ec5ba5a1dadcffe47719f5b808219acf84
```
*...again, remove the \\'s and newlines and put it all in one line.*

Example output of the signature hash:
```
IMf5P6WT60E+QcA5+ixors38umHuhTxx6TNHMsf9gLTIPcpilXkm1jDglMpK+JND0W3k/Z+NzEWUxvRy71NEDns=
```

### [13] Register the masternode on the blockchain (submit transaction and validating signature)

Create a "ProRegTx" special transaction (using the `protx` command) to register the masternode on the blockchain. _**This command must be sent from a Dash Core wallet holding a balance,**_ since a standard transaction fee is involved.

The command takes the following syntax: `protx register_submit tx sig`

Where:
- tx: The serialized transaction previously returned in the "tx" output field from protx register_prepare in the "Prepare transaction" step
- sig: The signed message from the previous step

Example:
```
protx register_submit \
030001000191def1f8bb265861f92e9984ac25c5142ebeda44901334e304c447dad5adf6070000000000feffffff0121dff505000000001976a9149e2deda2452b57e999685cb7dabdd6f4c3937f0788ac00000000d1010000000000c7fd27022913dd8505ae701e0fd56625c3fa9d2ff47802225faae562389e492c0100000000000000000000000000ffff8c523b334e1fad8e6259e14db7d05431ef4333d94b70df1391c601d2c43f022eeceaaf09532d84350feb49d7e72c183e56737c816076d0e803d4f86036bd4151160f5732ab4a461bd127ad8e6259e14db7d05431ef4333d94b70df1391c600001976a914adf50b01774202a184a2c7150593442b89c212e788acf8d42b331ae7a29076b464e61fdbcfc0b13f611d3d7f88bbe066e6ebabdfab7700 \
IMf5P6WT60E+QcA5+ixors38umHuhTxx6TNHMsf9gLTIPcpilXkm1jDglMpK+JND0W3k/Z+NzEWUxvRy71NEDns=
```
*...again, remove the \\'s and newlines and put it all in one line.*

Example result: `9f5ec7540baeefc4b7581d88d236792851f26b4b754684a31ee35d09bdfb7fb6`

Your masternode is now upgraded to
*[DIP003](https://github.com/dashpay/dips/blob/master/dip-0003.md)* and will
appear on the Deterministic Masternode List after the transaction is mined to a
block. You can view this list on the "Masternodes" > "DIP3 Masternodes" tab of
the Dash Core wallet, or in the console using the command `protx list valid`,
where the txid of the final `protx register_submit` transaction identifies your
DIP003 masternode. Note again that all functions related to *DIP003* will only
take effect once *Spork 15* is enabled on the network. You can view the spork
status using the spork active command and the ENABLED status using the monitoring techniques as described in PART 2.


&nbsp;

## WHEW!!! ALL DONE!

Continue to monitor the enablement and dip3 status as described above.

If all went well, you have a working Dash Masternode! Congratulations. I hope
this was helpful.

Got a dash of feedback? *...har har...* Send it my way <https://keybase.io/toddwarner>    

> _**Credit:** Much of this documentation was inspired by the [good
work](<https://docs.dash.org/en/latest/masternodes/maintenance.html#generate-a-bls-key-pair>)
of the Dash Core documentation team._

---

## Appendix - Advanced Topics

### Email the admin when the Masternode's status changes from "ENABLED"

Not written yet. Stay tuned. For general automated email setup, see the
"Appendix" in the [node
setup](https://github.com/taw00/dashcore-rpm/blob/master/documentation/howto.dashcore-node-setup.systemd.md)
documentation.

### Super fancy crontab settings

Remember to edit with `sudo -u dashcore crontab -e` if dashcore-sentinel is
installed with our RPM packages.

```
# Run Sentinel every minute; All messages are logged.
logfile=/var/log/dashcore/sentinel.log
* * * * * cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py >> $logfile 2>&1
```

```
# Run Sentinel every minute; dump COPIUS amounts of debug information to logfile
SENTINEL_DEBUG=1
logfile=/var/log/dashcore/sentinel.log
* * * * * cd /var/lib/dashcore/sentinel && venv/bin/python bin/sentinel.py >> $logfile 2>&1
```

```
# Run Sentinel every minute; each run is time stamped in the logs
m0="----Sentinel job started --- pid:"
m1="----Sentinel job completed - pid:" # Not used in this example
t="%b %d %T UTC"
logfile=/var/log/dashcore/sentinel.log
* * * * * { cd /var/lib/dashcore/sentinel && date --utc +"$t $m0 $$" && venv/bin/python bin/sentinel.py ; } >> $logfile 2>&1
```




