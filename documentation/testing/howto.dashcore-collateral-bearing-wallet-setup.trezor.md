## Dash Masternode Tool

IGNORE THESE INSTRUCTIONS FOR NOW. THEY ARE A MESS AND WRONG.

These instructions mirror, mostly the instructions found at
<https://github.com/Bertrand256/dash-masternode-tool>. This exists as a summary
and commentary, as I attempt to run this on Fedora.

0. Install GDK Pixbuf2 and some libraries

```
# This will also install gdk-pixbuf2 and a pile of other packages
sudo dnf install libcanberra-gtk-module.so libpk-gtk-module.so -y
```

1. Download binary tar.gz file from <https://github.com/Bertrand256/dash-masternode-tool/releases>
2. Copy to `~/.local/bin` and open up the archive (the tarball)

```
cp ~/Download/DashMasternodeTool*.tar.gz ~/.local/bin/
tar xvzf DashMasternodeTool*.tar.gz
```

3. Run it...

Note: This will create a configuration directory in your home directory.
`~/DashMasterNode/...`

```
cd DashMasternodeTool
./DashMasternodeTool
```

  * If you see this error...

```
(DashMasternodeTool:6539): GdkPixbuf-WARNING **: Cannot open pixbuf loader module file '/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache': No such file or directory

This likely means that your installation is broken.
Try running the command
  gdk-pixbuf-query-loaders > /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders.cache
to make things work again for the time being.
```

    ...exit the GUI and implement this workaround **(UPDATE: This does not
    work, not really, so don't do it until I figure things out)**...

```
#sudo mkdir /usr/lib/x86_64-linux-gnu
#sudo ln -s /usr/lib64/gdk-pixbuf-2.0 /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0
#sudo rm -rf /usr/lib/x86_64-linux-gnu
```



4. Click... Configure > Miscellaneous

   * Select "Trezor"

6. Click... Dash Network

   * Highlight each connection listed and "Test connection"
   * If one errors out, consider removing it (unchecking it) from the list. If
     they all fail, something else is wrong -- check your network connection,
     etc.
   * Apply > OK

--------------------------------------------------------------------------------

### New Masternode? Or Existing Masternode?


#### Existing Masternode

Assumption: You have a masternode set up as per
<https://github.com/taw00/dashcore-rpm/tree/master/documentation>

We are following the instructions found here: <https://github.com/Bertrand256/dash-masternode-tool/blob/master/doc/config-masternodes-a.md>

***Important:*** Though you can time this very cleverly, I don't recommend it.
Don't proceed any further until your masternode recieves a dividend from the
network.  Then continue.


1. Open your Trezor: <https://wallet.trezor.io>

2. Switch to "Dash (DASH)" and select "Account #1" and "Receive"

   *Note: Have a password and pin set up. Use a password that leads to an empty
    Dash wallet and were you will have no other crypto currencies stored.*

   The trezor wallet should state "Fresh address: /0 Xljsdfsasdflkjasdlfkjasdlkfjsdlkfj"
   (that's a poor example of an address, but you get the idea).

3. Open your collateralizing `dash-qt` wallet (Dash Core Wallet) and send your
   1000 Dash to that receiving address. 

   * Oops! Need to move the `masternode.conf` file out of the way first.
     - Shut down `dash-qt` wallet and move that file temporarily
     
     ```
     cd ~/.dashcore/
     mv masternode.conf ~/
     ```

   * Start up `dash-qt` wallet again
   * Settings > Unlock wallet
   * Settings > Options > Wallet
   * Turn off "Enable coin control features" and click "OK"
   * Click the "Send" tab
   * Paste the address that you copied from your Trezor Hardware Wallet into
     the "Pay To" field (review carefully that you have the right address)
   * Ammount: 1000 DASH
   * DO NOT select "Subtract fee from amount". You need that full 1000 DASH to
     land.

     ***Important note:*** This will only work if you have more than 1000 Dash
     in your Dash Core wallet. If you do not, stop what you are doing and send
     some dash to that wallet. Once complete, you can complete these steps.
   
   * SEND IT! ... _Hold your breath, this is a lot of money_ :)


4. Switch to or Open up the `DashMasternodeTool` application again

   Click "New"

5. Copy from your `masternode.conf` file and fill out the form with the first
   three values from that file:

   * Masternode Name (can be anything really; it is just a label)
   * IP address (the port is seperated in the port field)
   * Private key

6. The "Collateral" value is your receiving address from your Trezor. I.e., The
   address you sent that Dash to.

7. Click the green arrow to the right of that address in order to auto-populate
   the BIP32 path. It should look something like... 44'/5'/0'/0/0

   Note: This will query your Trezor to collect the right information.

8. For the Transaction ID, click the "Lookup" button. The DMTool will reach out
   to the network and fetch the right values for you. Select the result and
   click "OK". Note: The transaction will have to have been confirmed in order
   for this to work.

   You should now see the Collateral TX ID and TX index fields filled with the
   relevant data.

9. Click "Save configuration" (the button is at the top).

10. Click "Edit" again. Click on "Lookup" and note the number of confirmations.
    You must wait until there are 15 before restarting your masternode.

11. 15 Confirmations or more??? Click "Start Masternode using Hardware Wallet"

...

#### New Masternode

TODO: Write this!
