BLS in this form was relevant for the v18 dashcore.
The dashcore build assumes your build system pulls from the internet and builds
all kinds of stuff that is already supplied (and tested) by the OS distributor.
In order to force the dash build to use the system builds, we need to change
the package.mk and bls-dash.mk (the chia_bls.mk file from 0.16 and older) files.
