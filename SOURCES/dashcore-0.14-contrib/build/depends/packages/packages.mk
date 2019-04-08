# Replaces packages.mk in core depends tree.
# E.g. dash-0.13.0.0/depends/packages/packages.mk
# We are attempting to force the build to use OS supplied packages.
#t0dd: we replace all packages with OS delivered packages except for chia_bls
packages := chia_bls
native_packages := 

qt_native_packages = 
qt_packages = 

qt_x86_64_linux_packages := 
qt_i686_linux_packages:=$(qt_x86_64_linux_packages)

wallet_packages =

upnp_packages = 

