# HowTo: v12.1 Dash Wallet as Collateral Holding Agent for a Dash Masternode<br />...on Fedora, CentOS or Red Hat Enterprise Linux

> This edition of the document is for GUI versions of the Dash Core Wallet (`dash-qt`).

Installing the Dash Core GUI client on linux in the Red Hat family is almost trivial.

## Install the operating system

I leave it as an excercise for the reader to install Fedora, CentOS, or even RHEL. For Fedora, go here - https://getfedora.org/ For CentOS, go here - https://www.centos.org/download/ For Fedora, I recommend the "Workstation" install.

As you walk through the installation wizard, you will be asked to create a normal user on the system. Do that. The wizard will also ask you if you want to allow this user to have system admin rights. You need to do that as well. Otherwise, you have to add those rights after the fact. Like this (the username in this example is `mnwalletuser`)...

```
# Log into the system as root user.
# If the user does not exist, do this...
useradd -G wheel mnwalletuser
passwd mnwalletuser

# If the user does exist, do this...
usermod -a -G wheel mnwalletuser
```

Once the operating system is installed, log onto the system as a normal user (not root), update the system, and reboot:

...if this is Fedora

```
sudo dnf upgrade -y
sudo reboot
```

...if this is CentOS or Red Hat Enterprise Linux

```
sudo yum install -y epel-release
sudo yum update -y
sudo reboot
```

## Install the Dash Core GUI Client

Log onto the system as a normal user (not root), install the Dash wallet:

...if using Fedora:

```
cd /etc/yum.repos.d/
sudo curl https://raw.githubusercontent.com/taw00/dashcore-rpm/master/dashcore-fedora.repo -o dashcore-fedora.repo
cd -
sudo dnf config-manager --set-disabled dashcore-stable
sudo dnf config-manager --set-enabled dashcore-unstable ## version 12.1 is currently "unstable"
sudo dnf install -y dashcore-client
```

...if using CentOS or RHEL

```
cd /etc/yum.repos.d/
sudo curl https://raw.githubusercontent.com/taw00/dashcore-rpm/master/dashcore-centos.repo -o dashcore-centos.repo
cd -
sudo yum-config-manager --disable dashcore-stable
sudo yum-config-manager --enable dashcore-unstable ## version 12.1 is currently "unstable"
sudo yum install -y dashcore-client
```

## Run the Dash Core GUI Wallet

If you are planning on running the wallet on the mainnet (versus testnet) you really need to just start it up, but let me be a little pedantic here since these instructions will work always.

Create a `.dashcore` directory, edit the `dash.conf` configuration (text) file, and set the testnet variable on or off:

```
cd ~
mkdir .dashcore
echo "testnet=1" >> .dashcore/dash.conf  # 1 for testnet, and 0 for mainnet
```

Click through your menus and click on the Dash icon, or right this from the commandline...

```
dash-qt
```

## Send 1000 Dash to the wallet


From your GUI wallet interface do this...

* Navigate the menus: Tools > Debug console
* Enter in that dialogue: `getnewaddress`
* After you hit enter, you should get a new address listed.
  - For testnet, it will begin with a "y", example: `yMArVugC51J6WRkAVJpAwi2x6ecr4xvazH`
  - For mainnet, it will begin with a "X", example: `XMArVugC51J6WRkAVJpAwi2x6ecr4xvazH`

You can do the same thing from the commandline with the `dash-cli` interface: `dash-cli getnewaddress`

From whatever other source has that 1000 Dash, send precisely 1000 Dash (or tDash if this is testnet) to that address. Important. It has to be precisely 1000 Dash; fees must be accounted for.

If you need tDash for testnet testing purposes, have it sent from https://test.faucet.dash.org/

Record this in some scratchpad somewhere, you will need it when you set up your masternode

## Generate Masternode private key (a key that only the masternode and the wallet share)

From your GUI wallet interface do this...

* Navigate the menus: Tools > Debug console
* Enter in that dialogue: `masternode genkey`
* After you hit enter, it will look something like this: `92yZY5b8bYD5G2Qh1C7Un6Tf3TG3mH4LUZha2rdj3QUDGHNg4W9`

Or from the commandline: `dash-cli masternode genkey`

Record this in some scratchpad somewhere, you will need it when you set up your masternode


## Get your funding transaction ID and index

From your GUI wallet interface do this...

* Navigate the menus: Tools > Debug console
* Enter in that dialogue: `masternode outputs`

Or from the commandline: `dash-cli masternode outputs`

Record this in some scratchpad somewhere, you will need it when you set up your masternode



## All done!

You have a functioning wallet set up with 1000 DASH or tDASH ready to serve as the collateralizing agent for a masternode.

Please send feedback and comments to t0dd@protonmail.com


