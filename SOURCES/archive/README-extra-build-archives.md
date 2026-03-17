We pre-download four dependencies and include them in the source tarball.  
- bls-signatures and libbacktrace are not supplied by the OS vendor for Fedora or EL8.
- miniupnpc and bdb (v4) are not supplied by the EL8 OS.

1. chia_bls: `bls-signatures-20181101.tar.gz` aka `v20181101.tar.gz`  
   <https://github.com/taw00/dashcore-rpm/blob/master/SOURCES/bls-signatures-20181101.tar.gz>  
   or  
   <https://github.com/codablock/bls-signatures/archive/v20181101.tar.gz>  
   or  
   <https://github.com/codablock/bls-signatures/archive/v20181101/bls-signatures-20181101.tar.gz>
2. backtrace: `libbacktrace-rust-snapshot-2018-05-22.tar.gz` aka `rust-snapshot-2018-05-22.tar.gz`  
   <https://github.com/rust-lang-nursery/libbacktrace/archive/rust-snapshot-2018-05-22.tar.gz>  
   or  
   <https://github.com/rust-lang-nursery/libbacktrace/archive/rust-snapshot-2018-05-22/libbacktrace-rust-snapshot-2018-05-22.tar.gz>
3. miniupnpc: `miniupnpc-2.0.20170509.tar.gz` (RHEL8 only)  
   <http://miniupnp.free.fr/files/download.php?file=miniupnpc-2.0.20170509.tar.gz>
4. bdb: `db-4.8.30.NC.tar.gz` (RHEL8 only)  
   <https://download.oracle.com/berkeley-db/db-4.8.30.NC.tar.gz>

