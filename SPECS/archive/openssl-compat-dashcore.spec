%define compat_prefix /opt/openssl-compat-dashcore

# For the curious:
# 0.9.5a soversion = 0
# 0.9.6  soversion = 1
# 0.9.6a soversion = 2
# 0.9.6c soversion = 3
# 0.9.7a soversion = 4
# 0.9.7ef soversion = 5
# 0.9.8ab soversion = 6
# 0.9.8g soversion = 7
# 0.9.8jk + EAP-FAST soversion = 8
# 1.0.0 soversion = 10
%define soversion 10

# Number of threads to spawn when testing some threading fixes.
%define thread_test_threads %{?threads:%{threads}}%{!?threads:1}

# Arches on which we need to prevent arch conflicts on opensslconf.h, must
# also be handled in opensslconf-new.h.
%define multilib_arches %{ix86} ia64 ppc %{power64} s390 s390x sparcv9 sparc64 x86_64

%global _performance_build 1

Summary: Utilities from the general purpose cryptography library with TLS implementation
Name: openssl-compat-dashcore
Version: 1.0.2f
Release: 1.taw%{?dist}
Epoch: 1
Source: openssl-%{version}.tar.gz
Source2: Makefile.certificate
Source6: make-dummy-cert
Source7: renew-dummy-cert
Source8: openssl-thread-test.c
Source9: opensslconf-new.h
Source10: opensslconf-new-warning.h
Source11: README.FIPS
# Build changes
Patch1: openssl-1.0.2f-rpmbuild.patch
Patch2: openssl-1.0.2a-defaults.patch
Patch4: openssl-1.0.2a-enginesdir.patch
Patch5: openssl-1.0.2a-no-rpath.patch
Patch6: openssl-1.0.2a-test-use-localhost.patch
Patch7: openssl-1.0.0-timezone.patch
Patch8: openssl-1.0.1c-perlfind.patch
Patch9: openssl-1.0.1c-aliasing.patch
# Bug fixes
Patch23: openssl-1.0.2f-default-paths.patch
Patch24: openssl-1.0.2a-issuer-hash.patch
# Functionality changes
Patch33: openssl-1.0.0-beta4-ca-dir.patch
Patch34: openssl-1.0.2a-x509.patch
Patch35: openssl-1.0.2a-version-add-engines.patch
Patch39: openssl-1.0.2a-ipv6-apps.patch
Patch45: openssl-1.0.2a-env-zlib.patch
Patch47: openssl-1.0.2a-readme-warning.patch
Patch49: openssl-1.0.1i-algo-doc.patch
Patch50: openssl-1.0.2a-dtls1-abi.patch
Patch51: openssl-1.0.2a-version.patch
Patch60: openssl-1.0.2a-apps-dgst.patch
Patch63: openssl-1.0.2a-xmpp-starttls.patch
Patch65: openssl-1.0.2a-chil-fixes.patch
Patch66: openssl-1.0.2a-pkgconfig-krb5.patch
Patch68: openssl-1.0.2a-secure-getenv.patch
Patch71: openssl-1.0.2f-manfix.patch
Patch74: openssl-1.0.2a-no-md5-verify.patch
Patch77: openssl-1.0.2a-weak-ciphers.patch
Patch90: openssl-1.0.2a-enc-fail.patch
Patch92: openssl-1.0.2a-system-cipherlist.patch
Patch93: openssl-1.0.2a-disable-sslv2v3.patch
# Backported fixes including security fixes
Patch80: openssl-1.0.2f-wrap-pad.patch
Patch81: openssl-1.0.2a-padlock64.patch
Patch84: openssl-1.0.2f-trusted-first-doc.patch
Patch87: openssl-1.0.2a-cc-reqs.patch

License: OpenSSL
Group: System Environment/Libraries
URL: http://www.openssl.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: coreutils, krb5-devel, perl, sed, zlib-devel, /usr/bin/cmp
BuildRequires: /usr/bin/rename
Requires: coreutils, make
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package libs
Summary: A general purpose cryptography library with TLS implementation
Group: System Environment/Libraries
Requires: ca-certificates >= 2008-5

%description libs
OpenSSL is a toolkit for supporting cryptography. The openssl-libs
package contains the libraries that are used by various applications which
support cryptographic algorithms and protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Group: Development/Libraries
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: krb5-devel%{?_isa}, zlib-devel%{?_isa}
Requires: pkgconfig

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%package static
Summary:  Libraries for static linking of applications which will use OpenSSL
Group: Development/Libraries
Requires: %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}

%description static
OpenSSL is a toolkit for supporting cryptography. The openssl-static
package contains static libraries needed for static linking of
applications which support various cryptographic algorithms and
protocols.

%package perl
Summary: Perl scripts provided with OpenSSL
Group: Applications/Internet
Requires: perl
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description perl
OpenSSL is a toolkit for supporting cryptography. The openssl-perl
package provides Perl scripts for converting certificates and keys
from other formats to the formats used by the OpenSSL toolkit.

%prep
%setup -q -n openssl-%{version}

#cp %{SOURCE12} %{SOURCE13} crypto/ec/

%patch1 -p1 -b .rpmbuild
%patch2 -p1 -b .defaults
%patch4 -p1 -b .enginesdir %{?_rawbuild}
%patch5 -p1 -b .no-rpath
%patch6 -p1 -b .use-localhost
%patch7 -p1 -b .timezone
%patch8 -p1 -b .perlfind %{?_rawbuild}
%patch9 -p1 -b .aliasing

%patch23 -p1 -b .default-paths
%patch24 -p1 -b .issuer-hash

%patch33 -p1 -b .ca-dir
%patch34 -p1 -b .x509
%patch35 -p1 -b .version-add-engines
%patch39 -p1 -b .ipv6-apps
%patch45 -p1 -b .env-zlib
%patch47 -p1 -b .warning
%patch49 -p1 -b .algo-doc
%patch50 -p1 -b .dtls1-abi
%patch51 -p1 -b .version
%patch60 -p1 -b .dgst
%patch63 -p1 -b .starttls
%patch65 -p1 -b .chil
%patch66 -p1 -b .krb5
%patch68 -p1 -b .secure-getenv
%patch71 -p1 -b .manfix
%patch74 -p1 -b .no-md5-verify
%patch77 -p1 -b .weak-ciphers
%patch90 -p1 -b .enc-fail
%patch92 -p1 -b .system
%patch93 -p1 -b .v2v3

%patch80 -p1 -b .wrap
%patch81 -p1 -b .padlock64
%patch84 -p1 -b .trusted-first
%patch87 -p1 -b .cc-reqs

sed -i 's/SHLIB_VERSION_NUMBER "1.0.0"/SHLIB_VERSION_NUMBER "%{version}"/' crypto/opensslv.h

# Modify the various perl scripts to reference perl in the right location.
perl util/perlpath.pl `dirname %{__perl}`

# Generate a table with the compile settings for my perusal.
touch Makefile
make TABLE PERL=%{__perl}

%build
# Figure out which flags we want to use.
# default
sslarch=%{_os}-%{_target_cpu}
%ifarch %ix86
sslarch=linux-elf
if ! echo %{_target} | grep -q i686 ; then
	sslflags="no-asm 386"
fi
%endif
%ifarch sparcv9
sslarch=linux-sparcv9
sslflags=no-asm
%endif
%ifarch sparc64
sslarch=linux64-sparcv9
sslflags=no-asm
%endif
%ifarch alpha alphaev56 alphaev6 alphaev67
sslarch=linux-alpha-gcc
%endif
%ifarch s390 sh3eb sh4eb
sslarch="linux-generic32 -DB_ENDIAN"
%endif
%ifarch s390x
sslarch="linux64-s390x"
%endif
%ifarch %{arm}
sslarch=linux-armv4
%endif
%ifarch sh3 sh4
sslarch=linux-generic32
%endif
%ifarch ppc64 ppc64p7
sslarch=linux-ppc64
%endif
%ifarch ppc64le
sslarch="linux-ppc64le"
%endif

# ia64, x86_64, ppc are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.
./Configure \
	--prefix=%{compat_prefix} --openssldir=%{compat_prefix}/ssl ${sslflags} \
	zlib enable-camellia enable-seed enable-tlsext enable-rfc3779 \
	enable-cms enable-md2 \
	--with-krb5-flavor=MIT --enginesdir=%{compat_prefix}/lib/openssl/engines \
	--with-krb5-dir=/usr shared  ${sslarch}

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"
make depend
make all

# Generate hashes for the included certs.
make rehash

# Overwrite FIPS README
cp -f %{SOURCE11} .

%check
# Verify that what was compiled actually works.

# We must revert patch33 before tests otherwise they will fail
patch -p1 -R < %{PATCH33}

LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LD_LIBRARY_PATH
OPENSSL_ENABLE_MD5_VERIFY=
export OPENSSL_ENABLE_MD5_VERIFY
make -C test apps tests
%{__cc} -o openssl-thread-test \
	`krb5-config --cflags` \
	-I./include \
	$RPM_OPT_FLAGS \
	%{SOURCE8} \
	-L. \
	-lssl -lcrypto \
	`krb5-config --libs` \
	-lpthread -lz -ldl
./openssl-thread-test --threads %{thread_test_threads}

# Add generation of HMAC checksum of the final stripped library
#%define __spec_install_post \
#    %{?__debug_package:%{__debug_install_post}} \
#    %{__arch_install_post} \
#    %{__os_install_post} \
#    crypto/fips/fips_standalone_hmac $RPM_BUILD_ROOT%{_libdir}/libcrypto.so.%{version} >$RPM_BUILD_ROOT%{_libdir}/.libcrypto.so.%{version}.hmac \
#    ln -sf .libcrypto.so.%{version}.hmac $RPM_BUILD_ROOT%{_libdir}/.libcrypto.so.%{soversion}.hmac \
#    crypto/fips/fips_standalone_hmac $RPM_BUILD_ROOT%{_libdir}/libssl.so.%{version} >$RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{version}.hmac \
#    ln -sf .libssl.so.%{version}.hmac $RPM_BUILD_ROOT%{_libdir}/.libssl.so.%{soversion}.hmac \
#%{nil}

%define __provides_exclude_from %{_libdir}/openssl

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
install -d $RPM_BUILD_ROOT%{compat_prefix}/{bin,include,lib,share/man,lib/openssl}
make INSTALL_PREFIX=$RPM_BUILD_ROOT install
make INSTALL_PREFIX=$RPM_BUILD_ROOT install_docs
mv $RPM_BUILD_ROOT%{compat_prefix}/lib/engines $RPM_BUILD_ROOT%{compat_prefix}/lib/openssl
mv $RPM_BUILD_ROOT%{compat_prefix}/ssl/man/* $RPM_BUILD_ROOT%{compat_prefix}/share/man
rmdir $RPM_BUILD_ROOT%{compat_prefix}/ssl/man
rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{compat_prefix}/lib/*.so.%{soversion}
mkdir -p $RPM_BUILD_ROOT/%{compat_prefix}/lib
for lib in $RPM_BUILD_ROOT%{compat_prefix}/lib/*.so.%{version} ; do
    chmod 755 ${lib}
    ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{compat_prefix}/lib/`basename ${lib} .%{version}`
    ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{compat_prefix}/lib/`basename ${lib} .%{version}`.%{soversion}
done

# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
mkdir -p $RPM_BUILD_ROOT%{compat_prefix}/ssl/certs
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{compat_prefix}/ssl/certs/Makefile
install -m755 %{SOURCE6} $RPM_BUILD_ROOT%{compat_prefix}/ssl/certs/make-dummy-cert
install -m755 %{SOURCE7} $RPM_BUILD_ROOT%{compat_prefix}/ssl/certs/renew-dummy-cert

# Make sure we actually include the headers we built against.
for header in $RPM_BUILD_ROOT%{compat_prefix}/include/openssl/* ; do
	if [ -f ${header} -a -f include/openssl/$(basename ${header}) ] ; then
		install -m644 include/openssl/`basename ${header}` ${header}
	fi
done

# Rename man pages so that they don't conflict with other system man pages.
pushd $RPM_BUILD_ROOT%{compat_prefix}/share/man
ln -s -f config.5 man5/openssl.cnf.5
for manpage in man*/* ; do
	if [ -L ${manpage} ]; then
		TARGET=`ls -l ${manpage} | awk '{ print $NF }'`
		ln -snf ${TARGET}ssl ${manpage}ssl
		rm -f ${manpage}
	else
		mv ${manpage} ${manpage}ssl
	fi
done
for conflict in passwd rand ; do
	rename ${conflict} ssl${conflict} man*/${conflict}*
done
popd

# Pick a CA script.
pushd  $RPM_BUILD_ROOT%{compat_prefix}/ssl/misc
mv CA.sh CA
popd

mkdir -m755 $RPM_BUILD_ROOT%{compat_prefix}/ssl/CA
mkdir -m700 $RPM_BUILD_ROOT%{compat_prefix}/ssl/CA/private
mkdir -m755 $RPM_BUILD_ROOT%{compat_prefix}/ssl/CA/certs
mkdir -m755 $RPM_BUILD_ROOT%{compat_prefix}/ssl/CA/crl
mkdir -m755 $RPM_BUILD_ROOT%{compat_prefix}/ssl/CA/newcerts

# Ensure the openssl.cnf timestamp is identical across builds to avoid
# mulitlib conflicts and unnecessary renames on upgrade
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{compat_prefix}/ssl/openssl.cnf

# Determine which arch opensslconf.h is going to try to #include.
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif
%ifarch sparcv9
basearch=sparc
%endif
%ifarch sparc64
basearch=sparc64
%endif

%ifarch %{multilib_arches}
# Do an opensslconf.h switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, and they each need
# their own correct-but-different versions of opensslconf.h to be usable.
install -m644 %{SOURCE10} \
	$RPM_BUILD_ROOT/%{compat_prefix}/include/openssl/opensslconf-${basearch}.h
cat $RPM_BUILD_ROOT/%{compat_prefix}/include/openssl/opensslconf.h >> \
	$RPM_BUILD_ROOT/%{compat_prefix}/include/openssl/opensslconf-${basearch}.h
install -m644 %{SOURCE9} \
	$RPM_BUILD_ROOT/%{compat_prefix}/include/openssl/opensslconf.h
%endif

# Remove unused files from upstream fips support
rm -rf $RPM_BUILD_ROOT/%{_bindir}/openssl_fips_fingerprint
rm -rf $RPM_BUILD_ROOT/%{_libdir}/fips_premain.*
rm -rf $RPM_BUILD_ROOT/%{_libdir}/fipscanister.*

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%doc FAQ NEWS README README.FIPS LICENSE
%{compat_prefix}/ssl/certs/make-dummy-cert
%{compat_prefix}/ssl/certs/renew-dummy-cert
%{compat_prefix}/ssl/certs/Makefile
%{compat_prefix}/ssl/misc/CA
%dir %{compat_prefix}/ssl/CA
%dir %{compat_prefix}/ssl/CA/private
%dir %{compat_prefix}/ssl/CA/certs
%dir %{compat_prefix}/ssl/CA/crl
%dir %{compat_prefix}/ssl/CA/newcerts
%{compat_prefix}/ssl/misc/c_*
%attr(0755,root,root) %{compat_prefix}/bin/openssl
%attr(0644,root,root) %{compat_prefix}/share/man/man1*/[ABD-Zabcd-z]*
%attr(0644,root,root) %{compat_prefix}/share/man/man5*/*
%attr(0644,root,root) %{compat_prefix}/share/man/man7*/*

%files libs
%doc LICENSE
%dir %{compat_prefix}/ssl
%dir %{compat_prefix}/ssl/certs
%dir %{compat_prefix}/ssl/misc
%dir %{compat_prefix}/ssl/private
%config(noreplace) %{compat_prefix}/ssl/openssl.cnf
%attr(0755,root,root) %{compat_prefix}/lib/libcrypto.so.%{version}
%attr(0755,root,root) %{compat_prefix}/lib/libcrypto.so.%{soversion}
%attr(0755,root,root) %{compat_prefix}/lib/libssl.so.%{version}
%attr(0755,root,root) %{compat_prefix}/lib/libssl.so.%{soversion}
#%attr(0644,root,root) %{compat_prefix}/lib/.libcrypto.so.*.hmac
#%attr(0644,root,root) %{compat_prefix}/lib/.libssl.so.*.hmac
%attr(0755,root,root) %{compat_prefix}/lib/openssl

%files devel
%doc doc/c-indentation.el doc/openssl.txt CHANGES
%{compat_prefix}/include/openssl
%attr(0755,root,root) %{compat_prefix}/lib/*.so
%attr(0644,root,root) %{compat_prefix}/share/man/man3*/*
%attr(0644,root,root) %{compat_prefix}/lib/pkgconfig/*.pc

%files static
%attr(0644,root,root) %{compat_prefix}/lib/*.a

%files perl
%attr(0755,root,root) %{compat_prefix}/bin/c_rehash
%attr(0644,root,root) %{compat_prefix}/share/man/man1*/*.pl*
%{compat_prefix}/ssl/misc/*.pl
%{compat_prefix}/ssl/misc/tsget

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%changelog
* Fri Mar 03 2017 Todd Warner <t0dd@protonmail.com> 1.0.2f-1.taw
- In-housed version for the Dash project

* Thu Jan 28 2016 Michael Hampton <bitcoin@ringingliberty.com> 1.0.2f-1
- Rebase to 1.0.2f

* Mon Apr 27 2015 Michael Hampton <bitcoin@ringingliberty.com> 1.0.2a-2
- Side-port to bitcoin

* Thu Apr 23 2015 Tomáš Mráz <tmraz@redhat.com> 1.0.2a-1
- rebase to 1.0.2 branch

* Thu Apr  9 2015 Tomáš Mráz <tmraz@redhat.com> 1.0.1k-7
- drop the AES-GCM restriction of 2^32 operations because the IV is
  always 96 bits (32 bit fixed field + 64 bit invocation field)

* Thu Mar 19 2015 Tomáš Mráz <tmraz@redhat.com> 1.0.1k-6
- fix CVE-2015-0209 - potential use after free in d2i_ECPrivateKey()
- fix CVE-2015-0286 - improper handling of ASN.1 boolean comparison
- fix CVE-2015-0287 - ASN.1 structure reuse decoding memory corruption
- fix CVE-2015-0289 - NULL dereference decoding invalid PKCS#7 data
- fix CVE-2015-0293 - triggerable assert in SSLv2 server

* Mon Mar 16 2015 Tomáš Mráz <tmraz@redhat.com> 1.0.1k-5
- fix bug in the CRYPTO_128_unwrap()

* Fri Feb 27 2015 Tomáš Mráz <tmraz@redhat.com> 1.0.1k-4
- fix bug in the RFC 5649 support (#1185878)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1:1.0.1k-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Jan 15 2015 Tomáš Mráz <tmraz@redhat.com> 1.0.1k-2
- test in the non-FIPS RSA keygen for minimal distance of p and q
  similarly to the FIPS RSA keygen

* Fri Jan  9 2015 Tomáš Mráz <tmraz@redhat.com> 1.0.1k-1
- new upstream release fixing multiple security issues

* Thu Nov 20 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1j-3
- disable SSLv3 by default again (mail servers and possibly
  LDAP servers should probably allow it explicitly for legacy
  clients)

* Tue Oct 21 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1j-2
- update the FIPS RSA keygen to be FIPS 186-4 compliant

* Thu Oct 16 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1j-1
- new upstream release fixing multiple security issues

* Fri Oct 10 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1i-5
- copy negotiated digests when switching certs by SNI (#1150032)

* Mon Sep  8 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1i-4
- add support for RFC 5649

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.1i-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1i-2
- drop RSA X9.31 from RSA FIPS selftests
- add Power 8 optimalizations

* Thu Aug  7 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1i-1
- new upstream release fixing multiple moderate security issues
- for now disable only SSLv2 by default

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> 1.0.1h-6
- fix license handling

* Mon Jun 30 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1h-5
- disable SSLv2 and SSLv3 protocols by default (can be enabled
  via appropriate SSL_CTX_clear_options() call)

* Wed Jun 11 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1h-4
- use system profile for default cipher list

* Tue Jun 10 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1h-3
- make FIPS mode keygen bit length restriction enforced only when
  OPENSSL_ENFORCE_MODULUS_BITS is set
- fix CVE-2014-0224 fix that broke EAP-FAST session resumption support

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.1h-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun  5 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1h-1
- new upstream release 1.0.1h

* Sat May 31 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.1g-2
- Drop obsolete and irrelevant docs
- Move devel docs to appropriate package

* Wed May  7 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1g-1
- new upstream release 1.0.1g
- do not include ECC ciphersuites in SSLv2 client hello (#1090952)
- fail on hmac integrity check if the .hmac file is empty

* Mon Apr 07 2014 Dennis Gilmore <dennis@ausil.us> - 1.0.1e-44
- pull in upstream patch for CVE-2014-0160
- removed CHANGES file portion from patch for expediency

* Thu Apr  3 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-43
- add support for ppc64le architecture (#1072633)

* Mon Mar 17 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-42
- properly detect encryption failure in BIO
- use 2048 bit RSA key in FIPS selftests

* Fri Feb 14 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-41
- use the key length from configuration file if req -newkey rsa is invoked

* Thu Feb 13 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-40
- print ephemeral key size negotiated in TLS handshake (#1057715)
- add DH_compute_key_padded needed for FIPS CAVS testing

* Thu Feb  6 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-39
- make expiration and key length changeable by DAYS and KEYLEN
  variables in the certificate Makefile (#1058108)
- change default hash to sha256 (#1062325)

* Wed Jan 22 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-38
- make 3des strength to be 128 bits instead of 168 (#1056616)

* Tue Jan  7 2014 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-37
- fix CVE-2013-4353 - Invalid TLS handshake crash
- fix CVE-2013-6450 - possible MiTM attack on DTLS1

* Fri Dec 20 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-36
- fix CVE-2013-6449 - crash when version in SSL structure is incorrect
- more FIPS validation requirement changes

* Wed Dec 18 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-35
- drop weak ciphers from the default TLS ciphersuite list
- add back some symbols that were dropped with update to 1.0.1 branch
- more FIPS validation requirement changes

* Tue Nov 19 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-34
- fix locking and reseeding problems with FIPS drbg

* Fri Nov 15 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-33
- additional changes required for FIPS validation

* Wed Nov 13 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-32
- disable verification of certificate, CRL, and OCSP signatures
  using MD5 if OPENSSL_ENABLE_MD5_VERIFY environment variable
  is not set

* Fri Nov  8 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-31
- add back support for secp521r1 EC curve
- add aarch64 to Configure (#969692)

* Tue Oct 29 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-30
- fix misdetection of RDRAND support on Cyrix CPUS (from upstream) (#1022346)

* Thu Oct 24 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-29
- do not advertise ECC curves we do not support (#1022493)

* Wed Oct 16 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-28
- only ECC NIST Suite B curves support
- drop -fips subpackage

* Mon Oct 14 2013 Tom Callaway <spot@fedoraproject.org> - 1.0.1e-27
- resolve bugzilla 319901 (phew! only took 6 years & 9 days)

* Fri Sep 27 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-26
- make DTLS1 work in FIPS mode
- avoid RSA and DSA 512 bits and Whirlpool in 'openssl speed' in FIPS mode

* Mon Sep 23 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-25
- avoid dlopening libssl.so from libcrypto (#1010357)

* Fri Sep 20 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-24
- fix small memory leak in FIPS aes selftest

* Thu Sep 19 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-23
- fix segfault in openssl speed hmac in the FIPS mode

* Thu Sep 12 2013 Tomáš Mráz <tmraz@redhat.com> 1.0.1e-22
- document the nextprotoneg option in manual pages
  original patch by Hubert Kario

* Tue Sep 10 2013 Kyle McMartin <kyle@redhat.com> 1.0.1e-21
- [arm] use elf auxv to figure out armcap.c instead of playing silly
  games with SIGILL handlers. (#1006474)

* Wed Sep  4 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-20
- try to avoid some races when updating the -fips subpackage

* Mon Sep  2 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-19
- use version-release in .hmac suffix to avoid overwrite
  during upgrade

* Thu Aug 29 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-18
- allow deinitialization of the FIPS mode

* Thu Aug 29 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-17
- always perform the FIPS selftests in library constructor
  if FIPS module is installed

* Tue Aug 27 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-16
- add -fips subpackage that contains the FIPS module files

* Fri Aug 16 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-15
- fix use of rdrand if available
- more commits cherry picked from upstream
- documentation fixes

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1:1.0.1e-14
- Perl 5.18 rebuild

* Fri Jul 26 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-13
- additional manual page fix
- use symbol versioning also for the textual version

* Thu Jul 25 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-12
- additional manual page fixes

* Fri Jul 19 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-11
- use _prefix macro

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:1.0.1e-10
- Perl 5.18 rebuild

* Thu Jul 11 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-9
- add openssl.cnf.5 manpage symlink to config.5

* Wed Jul 10 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-8
- add relro linking flag

* Wed Jul 10 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-7
- add support for the -trusted_first option for certificate chain verification

* Fri May  3 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-6
- fix build of manual pages with current pod2man (#959439)

* Sun Apr 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.1e-5
- Enable ARM optimised build

* Mon Mar 18 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-4
- fix random bad record mac errors (#918981)

* Tue Feb 19 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-3
- fix up the SHLIB_VERSION_NUMBER

* Tue Feb 19 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-2
- disable ZLIB loading by default (due to CRIME attack)

* Tue Feb 19 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1e-1
- new upstream version

* Wed Jan 30 2013 Tomas Mraz <tmraz@redhat.com> 1.0.1c-12
- more fixes from upstream
- fix errors in manual causing build failure (#904777)

* Fri Dec 21 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1c-11
- add script for renewal of a self-signed cert by Philip Prindeville (#871566)
- allow X509_issuer_and_serial_hash() produce correct result in
  the FIPS mode (#881336)

* Thu Dec  6 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1c-10
- do not load default verify paths if CApath or CAfile specified (#884305)

* Tue Nov 20 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1c-9
- more fixes from upstream CVS
- fix DSA key pairwise check (#878597)

* Thu Nov 15 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1c-8
- use 1024 bit DH parameters in s_server as 512 bit is not allowed
  in FIPS mode and it is quite weak anyway

* Mon Sep 10 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1c-7
- add missing initialization of str in aes_ccm_init_key (#853963)
- add important patches from upstream CVS
- use the secure_getenv() with new glibc

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.1c-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1c-5
- use __getenv_secure() instead of __libc_enable_secure

* Fri Jul 13 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1c-4
- do not move libcrypto to /lib
- do not use environment variables if __libc_enable_secure is on
- fix strict aliasing problems in modes

* Thu Jul 12 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1c-3
- fix DSA key generation in FIPS mode (#833866)
- allow duplicate FIPS_mode_set(1)
- enable build on ppc64 subarch (#834652)

* Wed Jul 11 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1c-2
- fix s_server with new glibc when no global IPv6 address (#839031)
- make it build with new Perl

* Tue May 15 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1c-1
- new upstream version

* Thu Apr 26 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1b-1
- new upstream version

* Fri Apr 20 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1a-1
- new upstream version fixing CVE-2012-2110

* Wed Apr 11 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1-3
- add Kerberos 5 libraries to pkgconfig for static linking (#807050)

* Thu Apr  5 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1-2
- backports from upstream CVS
- fix segfault when /dev/urandom is not available (#809586)

* Wed Mar 14 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1-1
- new upstream release

* Mon Mar  5 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1-0.3.beta3
- add obsoletes to assist multilib updates (#799636)

* Wed Feb 29 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1-0.2.beta3
- epoch bumped to 1 due to revert to 1.0.0g on Fedora 17
- new upstream release from the 1.0.1 branch
- fix s390x build (#798411)
- versioning for the SSLeay symbol (#794950)
- add -DPURIFY to build flags (#797323)
- filter engine provides
- split the libraries to a separate -libs package
- add make to requires on the base package (#783446)

* Tue Feb  7 2012 Tomas Mraz <tmraz@redhat.com> 1.0.1-0.1.beta2
- new upstream release from the 1.0.1 branch, ABI compatible
- add documentation for the -no_ign_eof option

* Thu Jan 19 2012 Tomas Mraz <tmraz@redhat.com> 1.0.0g-1
- new upstream release fixing CVE-2012-0050 - DoS regression in
  DTLS support introduced by the previous release (#782795)

* Thu Jan  5 2012 Tomas Mraz <tmraz@redhat.com> 1.0.0f-1
- new upstream release fixing multiple CVEs

* Tue Nov 22 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0e-4
- move the libraries needed for static linking to Libs.private

* Thu Nov  3 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0e-3
- do not use AVX instructions when osxsave bit not set
- add direct known answer tests for SHA2 algorithms

* Wed Sep 21 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0e-2
- fix missing initialization of variable in CHIL engine

* Wed Sep  7 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0e-1
- new upstream release fixing CVE-2011-3207 (#736088)

* Wed Aug 24 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0d-8
- drop the separate engine for Intel acceleration improvements
  and merge in the AES-NI, SHA1, and RC4 optimizations
- add support for OPENSSL_DISABLE_AES_NI environment variable
  that disables the AES-NI support

* Tue Jul 26 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0d-7
- correct openssl cms help output (#636266)
- more tolerant starttls detection in XMPP protocol (#608239)

* Wed Jul 20 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0d-6
- add support for newest Intel acceleration improvements backported
  from upstream by Intel in form of a separate engine

* Thu Jun  9 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0d-5
- allow the AES-NI engine in the FIPS mode

* Tue May 24 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0d-4
- add API necessary for CAVS testing of the new DSA parameter generation

* Thu Apr 28 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0d-3
- add support for VIA Padlock on 64bit arch from upstream (#617539)
- do not return bogus values from load_certs (#652286)

* Tue Apr  5 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0d-2
- clarify apps help texts for available digest algorithms (#693858)

* Thu Feb 10 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0d-1
- new upstream release fixing CVE-2011-0014 (OCSP stapling vulnerability)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0c-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0c-3
- add -x931 parameter to openssl genrsa command to use the ANSI X9.31
  key generation method
- use FIPS-186-3 method for DSA parameter generation
- add OPENSSL_FIPS_NON_APPROVED_MD5_ALLOW environment variable
  to allow using MD5 when the system is in the maintenance state
  even if the /proc fips flag is on
- make openssl pkcs12 command work by default in the FIPS mode

* Mon Jan 24 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0c-2
- listen on ipv6 wildcard in s_server so we accept connections
  from both ipv4 and ipv6 (#601612)
- fix openssl speed command so it can be used in the FIPS mode
  with FIPS allowed ciphers

* Fri Dec  3 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0c-1
- new upstream version fixing CVE-2010-4180

* Tue Nov 23 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0b-3
- replace the revert for the s390x bignum asm routines with
  fix from upstream

* Mon Nov 22 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0b-2
- revert upstream change in s390x bignum asm routines

* Tue Nov 16 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0b-1
- new upstream version fixing CVE-2010-3864 (#649304)

* Tue Sep  7 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0a-3
- make SHLIB_VERSION reflect the library suffix

* Wed Jun 30 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0a-2
- openssl man page fix (#609484)

* Fri Jun  4 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0a-1
- new upstream patch release, fixes CVE-2010-0742 (#598738)
  and CVE-2010-1633 (#598732)

* Wed May 19 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0-5
- pkgconfig files now contain the correct libdir (#593723)

* Tue May 18 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0-4
- make CA dir readable - the private keys are in private subdir (#584810)

* Fri Apr  9 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0-3
- a few fixes from upstream CVS
- move libcrypto to /lib (#559953)

* Tue Apr  6 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0-2
- set UTC timezone on pod2man run (#578842)
- make X509_NAME_hash_old work in FIPS mode

* Tue Mar 30 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0-1
- update to final 1.0.0 upstream release

* Tue Feb 16 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.22.beta5
- make TLS work in the FIPS mode

* Fri Feb 12 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.21.beta5
- gracefully handle zero length in assembler implementations of
  OPENSSL_cleanse (#564029)
- do not fail in s_server if client hostname not resolvable (#561260)

* Wed Jan 20 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.20.beta5
- new upstream release

* Thu Jan 14 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.19.beta4
- fix CVE-2009-4355 - leak in applications incorrectly calling
  CRYPTO_free_all_ex_data() before application exit (#546707)
- upstream fix for future TLS protocol version handling

* Wed Jan 13 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.18.beta4
- add support for Intel AES-NI

* Thu Jan  7 2010 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.17.beta4
- upstream fix compression handling on session resumption
- various null checks and other small fixes from upstream
- upstream changes for the renegotiation info according to the latest draft

* Mon Nov 23 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.16.beta4
- fix non-fips mingw build (patch by Kalev Lember)
- add IPV6 fix for DTLS

* Fri Nov 20 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.15.beta4
- add better error reporting for the unsafe renegotiation

* Fri Nov 20 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.14.beta4
- fix build on s390x

* Wed Nov 18 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.13.beta4
- disable enforcement of the renegotiation extension on the client (#537962)
- add fixes from the current upstream snapshot

* Fri Nov 13 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.12.beta4
- keep the beta status in version number at 3 so we do not have to rebuild
  openssh and possibly other dependencies with too strict version check

* Thu Nov 12 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.11.beta4
- update to new upstream version, no soname bump needed
- fix CVE-2009-3555 - note that the fix is bypassed if SSL_OP_ALL is used
  so the compatibility with unfixed clients is not broken. The
  protocol extension is also not final.

* Fri Oct 16 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.10.beta3
- fix use of freed memory if SSL_CTX_free() is called before
  SSL_free() (#521342)

* Thu Oct  8 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.9.beta3
- fix typo in DTLS1 code (#527015)
- fix leak in error handling of d2i_SSL_SESSION()

* Wed Sep 30 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.8.beta3
- fix RSA and DSA FIPS selftests
- reenable fixed x86_64 camellia assembler code (#521127)

* Fri Sep  4 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.7.beta3
- temporarily disable x86_64 camellia assembler code (#521127)

* Mon Aug 31 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.6.beta3
- fix openssl dgst -dss1 (#520152)

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.5.beta3
- drop the compat symlink hacks

* Sat Aug 22 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.4.beta3
- constify SSL_CIPHER_description()

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.3.beta3
- fix WWW:Curl:Easy reference in tsget

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.2.beta3
- enable MD-2

* Thu Aug 20 2009 Tomas Mraz <tmraz@redhat.com> 1.0.0-0.1.beta3
- update to new major upstream release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8k-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Bill Nottingham <notting@redhat.com>
- do not build special 'optimized' versions for i686, as that's the base
  arch in Fedora now

* Tue Jun 30 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8k-6
- abort if selftests failed and random number generator is polled
- mention EVP_aes and EVP_sha2xx routines in the manpages
- add README.FIPS
- make CA dir absolute path (#445344)
- change default length for RSA key generation to 2048 (#484101)

* Thu May 21 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8k-5
- fix CVE-2009-1377 CVE-2009-1378 CVE-2009-1379
  (DTLS DoS problems) (#501253, #501254, #501572)

* Tue Apr 21 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8k-4
- support compatibility DTLS mode for CISCO AnyConnect (#464629)

* Fri Apr 17 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8k-3
- correct the SHLIB_VERSION define

* Wed Apr 15 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8k-2
- add support for multiple CRLs with same subject
- load only dynamic engine support in FIPS mode

* Wed Mar 25 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8k-1
- update to new upstream release (minor bug fixes, security
  fixes and machine code optimizations only)

* Thu Mar 19 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8j-10
- move libraries to /usr/lib (#239375)

* Fri Mar 13 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8j-9
- add a static subpackage

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8j-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8j-7
- must also verify checksum of libssl.so in the FIPS mode
- obtain the seed for FIPS rng directly from the kernel device
- drop the temporary symlinks

* Mon Jan 26 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8j-6
- drop the temporary triggerpostun and symlinking in post
- fix the pkgconfig files and drop the unnecessary buildrequires
  on pkgconfig as it is a rpmbuild dependency (#481419)

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8j-5
- add temporary triggerpostun to reinstate the symlinks

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8j-4
- no pairwise key tests in non-fips mode (#479817)

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8j-3
- even more robust test for the temporary symlinks

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8j-2
- try to ensure the temporary symlinks exist

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> 0.9.8j-1
- new upstream version with necessary soname bump (#455753)
- temporarily provide symlink to old soname to make it possible to rebuild
  the dependent packages in rawhide
- add eap-fast support (#428181)
- add possibility to disable zlib by setting
- add fips mode support for testing purposes
- do not null dereference on some invalid smime files
- add buildrequires pkgconfig (#479493)

* Sun Aug 10 2008 Tomas Mraz <tmraz@redhat.com> 0.9.8g-11
- do not add tls extensions to server hello for SSLv3 either

* Mon Jun  2 2008 Joe Orton <jorton@redhat.com> 0.9.8g-10
- move root CA bundle to ca-certificates package

* Wed May 28 2008 Tomas Mraz <tmraz@redhat.com> 0.9.8g-9
- fix CVE-2008-0891 - server name extension crash (#448492)
- fix CVE-2008-1672 - server key exchange message omit crash (#448495)

* Tue May 27 2008 Tomas Mraz <tmraz@redhat.com> 0.9.8g-8
- super-H arch support
- drop workaround for bug 199604 as it should be fixed in gcc-4.3

* Mon May 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.8g-7
- sparc handling

* Mon Mar 10 2008 Joe Orton <jorton@redhat.com> 0.9.8g-6
- update to new root CA bundle from mozilla.org (r1.45)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.8g-5
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Tomas Mraz <tmraz@redhat.com> 0.9.8g-4
- merge review fixes (#226220)
- adjust the SHLIB_VERSION_NUMBER to reflect library name (#429846)

* Thu Dec 13 2007 Tomas Mraz <tmraz@redhat.com> 0.9.8g-3
- set default paths when no explicit paths are set (#418771)
- do not add tls extensions to client hello for SSLv3 (#422081)

* Tue Dec  4 2007 Tomas Mraz <tmraz@redhat.com> 0.9.8g-2
- enable some new crypto algorithms and features
- add some more important bug fixes from openssl CVS

* Mon Dec  3 2007 Tomas Mraz <tmraz@redhat.com> 0.9.8g-1
- update to latest upstream release, SONAME bumped to 7

* Mon Oct 15 2007 Joe Orton <jorton@redhat.com> 0.9.8b-17
- update to new CA bundle from mozilla.org

* Fri Oct 12 2007 Tomas Mraz <tmraz@redhat.com> 0.9.8b-16
- fix CVE-2007-5135 - off-by-one in SSL_get_shared_ciphers (#309801)
- fix CVE-2007-4995 - out of order DTLS fragments buffer overflow (#321191)
- add alpha sub-archs (#296031)

* Tue Aug 21 2007 Tomas Mraz <tmraz@redhat.com> 0.9.8b-15
- rebuild

* Fri Aug  3 2007 Tomas Mraz <tmraz@redhat.com> 0.9.8b-14
- use localhost in testsuite, hopefully fixes slow build in koji
- CVE-2007-3108 - fix side channel attack on private keys (#250577)
- make ssl session cache id matching strict (#233599)

* Wed Jul 25 2007 Tomas Mraz <tmraz@redhat.com> 0.9.8b-13
- allow building on ARM architectures (#245417)
- use reference timestamps to prevent multilib conflicts (#218064)
- -devel package must require pkgconfig (#241031)

* Mon Dec 11 2006 Tomas Mraz <tmraz@redhat.com> 0.9.8b-12
- detect duplicates in add_dir properly (#206346)

* Thu Nov 30 2006 Tomas Mraz <tmraz@redhat.com> 0.9.8b-11
- the previous change still didn't make X509_NAME_cmp transitive

* Thu Nov 23 2006 Tomas Mraz <tmraz@redhat.com> 0.9.8b-10
- make X509_NAME_cmp transitive otherwise certificate lookup
  is broken (#216050)

* Thu Nov  2 2006 Tomas Mraz <tmraz@redhat.com> 0.9.8b-9
- aliasing bug in engine loading, patch by IBM (#213216)

* Mon Oct  2 2006 Tomas Mraz <tmraz@redhat.com> 0.9.8b-8
- CVE-2006-2940 fix was incorrect (#208744)

* Mon Sep 25 2006 Tomas Mraz <tmraz@redhat.com> 0.9.8b-7
- fix CVE-2006-2937 - mishandled error on ASN.1 parsing (#207276)
- fix CVE-2006-2940 - parasitic public keys DoS (#207274)
- fix CVE-2006-3738 - buffer overflow in SSL_get_shared_ciphers (#206940)
- fix CVE-2006-4343 - sslv2 client DoS (#206940)

* Tue Sep  5 2006 Tomas Mraz <tmraz@redhat.com> 0.9.8b-6
- fix CVE-2006-4339 - prevent attack on PKCS#1 v1.5 signatures (#205180)

* Wed Aug  2 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-5
- set buffering to none on stdio/stdout FILE when bufsize is set (#200580)
  patch by IBM

* Fri Jul 28 2006 Alexandre Oliva <aoliva@redhat.com> - 0.9.8b-4.1
- rebuild with new binutils (#200330)

* Fri Jul 21 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-4
- add a temporary workaround for sha512 test failure on s390 (#199604)

* Thu Jul 20 2006 Tomas Mraz <tmraz@redhat.com>
- add ipv6 support to s_client and s_server (by Jan Pazdziora) (#198737)
- add patches for BN threadsafety, AES cache collision attack hazard fix and
  pkcs7 code memleak fix from upstream CVS

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.9.8b-3.1
- rebuild

* Wed Jun 21 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-3
- dropped libica and ica engine from build

* Wed Jun 21 2006 Joe Orton <jorton@redhat.com>
- update to new CA bundle from mozilla.org; adds CA certificates
  from netlock.hu and startcom.org

* Mon Jun  5 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-2
- fixed a few rpmlint warnings
- better fix for #173399 from upstream
- upstream fix for pkcs12

* Thu May 11 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8b-1
- upgrade to new version, stays ABI compatible
- there is no more linux/config.h (it was empty anyway)

* Tue Apr  4 2006 Tomas Mraz <tmraz@redhat.com> - 0.9.8a-6
- fix stale open handles in libica (#177155)
- fix build if 'rand' or 'passwd' in buildroot path (#178782)
- initialize VIA Padlock engine (#186857)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.9.8a-5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.9.8a-5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Dec 15 2005 Tomas Mraz <tmraz@redhat.com> 0.9.8a-5
- don't include SSL_OP_NETSCAPE_REUSE_CIPHER_CHANGE_BUG
  in SSL_OP_ALL (#175779)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 29 2005 Tomas Mraz <tmraz@redhat.com> 0.9.8a-4
- fix build (-lcrypto was erroneusly dropped) of the updated libica
- updated ICA engine to 1.3.6-rc3

* Tue Nov 22 2005 Tomas Mraz <tmraz@redhat.com> 0.9.8a-3
- disable builtin compression methods for now until they work
  properly (#173399)

* Wed Nov 16 2005 Tomas Mraz <tmraz@redhat.com> 0.9.8a-2
- don't set -rpath for openssl binary

* Tue Nov  8 2005 Tomas Mraz <tmraz@redhat.com> 0.9.8a-1
- new upstream version
- patches partially renumbered

* Fri Oct 21 2005 Tomas Mraz <tmraz@redhat.com> 0.9.7f-11
- updated IBM ICA engine library and patch to latest upstream version

* Wed Oct 12 2005 Tomas Mraz <tmraz@redhat.com> 0.9.7f-10
- fix CAN-2005-2969 - remove SSL_OP_MSIE_SSLV2_RSA_PADDING which
  disables the countermeasure against man in the middle attack in SSLv2
  (#169863)
- use sha1 as default for CA and cert requests - CAN-2005-2946 (#169803)

* Tue Aug 23 2005 Tomas Mraz <tmraz@redhat.com> 0.9.7f-9
- add *.so.soversion as symlinks in /lib (#165264)
- remove unpackaged symlinks (#159595)
- fixes from upstream (constant time fixes for DSA,
  bn assembler div on ppc arch, initialize memory on realloc)

* Thu Aug 11 2005 Phil Knirsch <pknirsch@redhat.com> 0.9.7f-8
- Updated ICA engine IBM patch to latest upstream version.

* Thu May 19 2005 Tomas Mraz <tmraz@redhat.com> 0.9.7f-7
- fix CAN-2005-0109 - use constant time/memory access mod_exp
  so bits of private key aren't leaked by cache eviction (#157631)
- a few more fixes from upstream 0.9.7g

* Wed Apr 27 2005 Tomas Mraz <tmraz@redhat.com> 0.9.7f-6
- use poll instead of select in rand (#128285)
- fix Makefile.certificate to point to /etc/pki/tls
- change the default string mask in ASN1 to PrintableString+UTF8String

* Mon Apr 25 2005 Joe Orton <jorton@redhat.com> 0.9.7f-5
- update to revision 1.37 of Mozilla CA bundle

* Thu Apr 21 2005 Tomas Mraz <tmraz@redhat.com> 0.9.7f-4
- move certificates to _sysconfdir/pki/tls (#143392)
- move CA directories to _sysconfdir/pki/CA
- patch the CA script and the default config so it points to the
  CA directories

* Fri Apr  1 2005 Tomas Mraz <tmraz@redhat.com> 0.9.7f-3
- uninitialized variable mustn't be used as input in inline
  assembly
- reenable the x86_64 assembly again

* Thu Mar 31 2005 Tomas Mraz <tmraz@redhat.com> 0.9.7f-2
- add back RC4_CHAR on ia64 and x86_64 so the ABI isn't broken
- disable broken bignum assembly on x86_64

* Wed Mar 30 2005 Tomas Mraz <tmraz@redhat.com> 0.9.7f-1
- reenable optimizations on ppc64 and assembly code on ia64
- upgrade to new upstream version (no soname bump needed)
- disable thread test - it was testing the backport of the
  RSA blinding - no longer needed
- added support for changing serial number to
  Makefile.certificate (#151188)
- make ca-bundle.crt a config file (#118903)

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 0.9.7e-3
- libcrypto shouldn't depend on libkrb5 (#135961)

* Mon Feb 28 2005 Tomas Mraz <tmraz@redhat.com> 0.9.7e-2
- rebuild

* Mon Feb 28 2005 Tomas Mraz <tmraz@redhat.com> 0.9.7e-1
- new upstream source, updated patches
- added patch so we are hopefully ABI compatible with upcoming
  0.9.7f

* Thu Feb 10 2005 Tomas Mraz <tmraz@redhat.com>
- Support UTF-8 charset in the Makefile.certificate (#134944)
- Added cmp to BuildPrereq

* Thu Jan 27 2005 Joe Orton <jorton@redhat.com> 0.9.7a-46
- generate new ca-bundle.crt from Mozilla certdata.txt (revision 1.32)

* Thu Dec 23 2004 Phil Knirsch <pknirsch@redhat.com> 0.9.7a-45
- Fixed and updated libica-1.3.4-urandom.patch patch (#122967)

* Fri Nov 19 2004 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-44
- rebuild

* Fri Nov 19 2004 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-43
- rebuild

* Fri Nov 19 2004 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-42
- rebuild

* Fri Nov 19 2004 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-41
- remove der_chop, as upstream cvs has done (CAN-2004-0975, #140040)

* Tue Oct 05 2004 Phil Knirsch <pknirsch@redhat.com> 0.9.7a-40
- Include latest libica version with important bugfixes

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 14 2004 Phil Knirsch <pknirsch@redhat.com> 0.9.7a-38
- Updated ICA engine IBM patch to latest upstream version.

* Mon Jun  7 2004 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-37
- build for linux-alpha-gcc instead of alpha-gcc on alpha (Jeff Garzik)

* Tue May 25 2004 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-36
- handle %%{_arch}=i486/i586/i686/athlon cases in the intermediate
  header (#124303)

* Thu Mar 25 2004 Joe Orton <jorton@redhat.com> 0.9.7a-35
- add security fixes for CAN-2004-0079, CAN-2004-0112

* Tue Mar 16 2004 Phil Knirsch <pknirsch@redhat.com>
- Fixed libica filespec.

* Thu Mar 11 2004 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-34
- ppc/ppc64 define __powerpc__/__powerpc64__, not __ppc__/__ppc64__, fix
  the intermediate header

* Wed Mar 10 2004 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-33
- add an intermediate <openssl/opensslconf.h> which points to the right
  arch-specific opensslconf.h on multilib arches

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Phil Knirsch <pknirsch@redhat.com> 0.9.7a-32
- Updated libica to latest upstream version 1.3.5.

* Tue Feb 17 2004 Phil Knirsch <pknirsch@redhat.com> 0.9.7a-31
- Update ICA crypto engine patch from IBM to latest version.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Phil Knirsch <pknirsch@redhat.com> 0.9.7a-29
- rebuilt

* Wed Feb 11 2004 Phil Knirsch <pknirsch@redhat.com> 0.9.7a-28
- Fixed libica build.

* Wed Feb  4 2004 Nalin Dahyabhai <nalin@redhat.com>
- add "-ldl" to link flags added for Linux-on-ARM (#99313)

* Wed Feb  4 2004 Joe Orton <jorton@redhat.com> 0.9.7a-27
- updated ca-bundle.crt: removed expired GeoTrust roots, added
  freessl.com root, removed trustcenter.de Class 0 root

* Sun Nov 30 2003 Tim Waugh <twaugh@redhat.com> 0.9.7a-26
- Fix link line for libssl (bug #111154).

* Fri Oct 24 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-25
- add dependency on zlib-devel for the -devel package, which depends on zlib
  symbols because we enable zlib for libssl (#102962)

* Fri Oct 24 2003 Phil Knirsch <pknirsch@redhat.com> 0.9.7a-24
- Use /dev/urandom instead of PRNG for libica.
- Apply libica-1.3.5 fix for /dev/urandom in icalinux.c
- Use latest ICA engine patch from IBM.

* Sat Oct  4 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-22.1
- rebuild

* Wed Oct  1 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-22
- rebuild (22 wasn't actually built, fun eh?)

* Tue Sep 30 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-23
- re-disable optimizations on ppc64

* Tue Sep 30 2003 Joe Orton <jorton@redhat.com>
- add a_mbstr.c fix for 64-bit platforms from CVS

* Tue Sep 30 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-22
- add -Wa,--noexecstack to RPM_OPT_FLAGS so that assembled modules get tagged
  as not needing executable stacks

* Mon Sep 29 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-21
- rebuild

* Thu Sep 25 2003 Nalin Dahyabhai <nalin@redhat.com>
- re-enable optimizations on ppc64

* Thu Sep 25 2003 Nalin Dahyabhai <nalin@redhat.com>
- remove exclusivearch

* Wed Sep 24 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-20
- only parse a client cert if one was requested
- temporarily exclusivearch for %%{ix86}

* Tue Sep 23 2003 Nalin Dahyabhai <nalin@redhat.com>
- add security fixes for protocol parsing bugs (CAN-2003-0543, CAN-2003-0544)
  and heap corruption (CAN-2003-0545)
- update RHNS-CA-CERT files
- ease back on the number of threads used in the threading test

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 0.9.7a-19
- rebuild to fix gzipped file md5sums (#91211)

* Mon Aug 25 2003 Phil Knirsch <pknirsch@redhat.com> 0.9.7a-18
- Updated libica to version 1.3.4.

* Thu Jul 17 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-17
- rebuild

* Tue Jul 15 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-10.9
- free the kssl_ctx structure when we free an SSL structure (#99066)

* Fri Jul 11 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-16
- rebuild

* Thu Jul 10 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-15
- lower thread test count on s390x

* Tue Jul  8 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-14
- rebuild

* Thu Jun 26 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-13
- disable assembly on arches where it seems to conflict with threading

* Thu Jun 26 2003 Phil Knirsch <pknirsch@redhat.com> 0.9.7a-12
- Updated libica to latest upstream version 1.3.0

* Wed Jun 11 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-9.9
- rebuild

* Wed Jun 11 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-11
- rebuild

* Tue Jun 10 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-10
- ubsec: don't stomp on output data which might also be input data

* Tue Jun 10 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-9
- temporarily disable optimizations on ppc64

* Mon Jun  9 2003 Nalin Dahyabhai <nalin@redhat.com>
- backport fix for engine-used-for-everything from 0.9.7b
- backport fix for prng not being seeded causing problems, also from 0.9.7b
- add a check at build-time to ensure that RSA is thread-safe
- keep perlpath from stomping on the libica configure scripts

* Fri Jun  6 2003 Nalin Dahyabhai <nalin@redhat.com>
- thread-safety fix for RSA blinding

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 0.9.7a-8
- rebuilt

* Fri May 30 2003 Phil Knirsch <pknirsch@redhat.com> 0.9.7a-7
- Added libica-1.2 to openssl (featurerequest).

* Wed Apr 16 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-6
- fix building with incorrect flags on ppc64

* Wed Mar 19 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-5
- add patch to harden against Klima-Pokorny-Rosa extension of Bleichenbacher's
  attack (CAN-2003-0131)

* Mon Mar 17 2003 Nalin Dahyabhai <nalin@redhat.com>  0.9.7a-4
- add patch to enable RSA blinding by default, closing a timing attack
  (CAN-2003-0147)

* Wed Mar  5 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-3
- disable use of BN assembly module on x86_64, but continue to allow inline
  assembly (#83403)

* Thu Feb 27 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-2
- disable EC algorithms

* Wed Feb 19 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7a-1
- update to 0.9.7a

* Wed Feb 19 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7-8
- add fix to guard against attempts to allocate negative amounts of memory
- add patch for CAN-2003-0078, fixing a timing attack

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> 0.9.7-7
- Add openssl-ppc64.patch

* Mon Feb 10 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7-6
- EVP_DecryptInit should call EVP_CipherInit() instead of EVP_CipherInit_ex(),
  to get the right behavior when passed uninitialized context structures
  (#83766)
- build with -mcpu=ev5 on alpha family (#83828)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Jan 17 2003 Phil Knirsch <pknirsch@redhat.com> 0.9.7-4
- Added IBM hw crypto support patch.

* Wed Jan 15 2003 Nalin Dahyabhai <nalin@redhat.com>
- add missing builddep on sed

* Thu Jan  9 2003 Bill Nottingham <notting@redhat.com> 0.9.7-3
- debloat
- fix broken manpage symlinks

* Wed Jan  8 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7-2
- fix double-free in 'openssl ca'

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.7-1
- update to 0.9.7 final

* Tue Dec 17 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.7-0
- update to 0.9.7 beta6 (DO NOT USE UNTIL UPDATED TO FINAL 0.9.7)

* Wed Dec 11 2002 Nalin Dahyabhai <nalin@redhat.com>
- update to 0.9.7 beta5 (DO NOT USE UNTIL UPDATED TO FINAL 0.9.7)

* Tue Oct 22 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-30
- add configuration stanza for x86_64 and use it on x86_64
- build for linux-ppc on ppc
- start running the self-tests again

* Wed Oct 02 2002 Elliot Lee <sopwith@redhat.com> 0.9.6b-29hammer.3
- Merge fixes from previous hammer packages, including general x86-64 and
  multilib

* Tue Aug  6 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-29
- rebuild

* Thu Aug  1 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-28
- update asn patch to fix accidental reversal of a logic check

* Wed Jul 31 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-27
- update asn patch to reduce chance that compiler optimization will remove
  one of the added tests

* Wed Jul 31 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-26
- rebuild

* Mon Jul 29 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-25
- add patch to fix ASN.1 vulnerabilities

* Thu Jul 25 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-24
- add backport of Ben Laurie's patches for OpenSSL 0.9.6d

* Wed Jul 17 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-23
- own {_datadir}/ssl/misc

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-20
- free ride through the build system (whee!)

* Thu May 16 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-19
- rebuild in new environment

* Thu Apr  4 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-17, 0.9.6b-18
- merge RHL-specific bits into stronghold package, rename

* Tue Apr 02 2002 Gary Benson <gbenson@redhat.com> stronghold-0.9.6c-2
- add support for Chrysalis Luna token

* Tue Mar 26 2002 Gary Benson <gbenson@redhat.com>
- disable AEP random number generation, other AEP fixes

* Fri Mar 15 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-15
- only build subpackages on primary arches

* Thu Mar 14 2002 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-13
- on ia32, only disable use of assembler on i386
- enable assembly on ia64

* Mon Jan  7 2002 Florian La Roche <Florian.LaRoche@redhat.de> 0.9.6b-11
- fix sparcv9 entry

* Mon Jan  7 2002 Gary Benson <gbenson@redhat.com> stronghold-0.9.6c-1
- upgrade to 0.9.6c
- bump BuildArch to i686 and enable assembler on all platforms
- synchronise with shrimpy and rawhide
- bump soversion to 3

* Wed Oct 10 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- delete BN_LLONG for s390x, patch from Oliver Paukstadt

* Mon Sep 17 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-9
- update AEP driver patch

* Mon Sep 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- adjust RNG disabling patch to match version of patch from Broadcom

* Fri Sep  7 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-8
- disable the RNG in the ubsec engine driver

* Tue Aug 28 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-7
- tweaks to the ubsec engine driver

* Fri Aug 24 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-6
- tweaks to the ubsec engine driver

* Thu Aug 23 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-5
- update ubsec engine driver from Broadcom

* Fri Aug 10 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-4
- move man pages back to %%{_mandir}/man?/foo.?ssl from
  %%{_mandir}/man?ssl/foo.?
- add an [ engine ] section to the default configuration file

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- add a patch for selecting a default engine in SSL_library_init()

* Mon Jul 23 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-3
- add patches for AEP hardware support
- add patch to keep trying when we fail to load a cert from a file and
  there are more in the file
- add missing prototype for ENGINE_ubsec() in engine_int.h

* Wed Jul 18 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-2
- actually add hw_ubsec to the engine list

* Tue Jul 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- add in the hw_ubsec driver from CVS

* Wed Jul 11 2001 Nalin Dahyabhai <nalin@redhat.com> 0.9.6b-1
- update to 0.9.6b

* Thu Jul  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- move .so symlinks back to %%{_libdir}

* Tue Jul  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- move shared libraries to /lib (#38410)

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- switch to engine code base

* Mon Jun 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- add a script for creating dummy certificates
- move man pages from %%{_mandir}/man?/foo.?ssl to %%{_mandir}/man?ssl/foo.?

* Thu Jun 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add s390x support

* Fri Jun  1 2001 Nalin Dahyabhai <nalin@redhat.com>
- change two memcpy() calls to memmove()
- don't define L_ENDIAN on alpha

* Wed May 23 2001 Joe Orton <jorton@redhat.com> stronghold-0.9.6a-1
- Add 'stronghold-' prefix to package names.
- Obsolete standard openssl packages.

* Wed May 16 2001 Joe Orton <jorton@redhat.com>
- Add BuildArch: i586 as per Nalin's advice.

* Tue May 15 2001 Joe Orton <jorton@redhat.com>
- Enable assembler on ix86 (using new .tar.bz2 which does
  include the asm directories).

* Tue May 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- make subpackages depend on the main package

* Tue May  1 2001 Nalin Dahyabhai <nalin@redhat.com>
- adjust the hobble script to not disturb symlinks in include/ (fix from
  Joe Orton)

* Fri Apr 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- drop the m2crypo patch we weren't using

* Tue Apr 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- configure using "shared" as well

* Sun Apr  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 0.9.6a
- use the build-shared target to build shared libraries
- bump the soversion to 2 because we're no longer compatible with
  our 0.9.5a packages or our 0.9.6 packages
- drop the patch for making rsatest a no-op when rsa null support is used
- put all man pages into <section>ssl instead of <section>
- break the m2crypto modules into a separate package

* Tue Mar 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- use BN_LLONG on s390

* Mon Mar 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix the s390 changes for 0.9.6 (isn't supposed to be marked as 64-bit)

* Sat Mar  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- move c_rehash to the perl subpackage, because it's a perl script now

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 0.9.6
- enable MD2
- use the libcrypto.so and libssl.so targets to build shared libs with
- bump the soversion to 1 because we're no longer compatible with any of
  the various 0.9.5a packages circulating around, which provide lib*.so.0

* Wed Feb 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change hobble-openssl for disabling MD2 again

* Tue Feb 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- re-disable MD2 -- the EVP_MD_CTX structure would grow from 100 to 152
  bytes or so, causing EVP_DigestInit() to zero out stack variables in
  apps built against a version of the library without it

* Mon Feb 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- disable some inline assembly, which on x86 is Pentium-specific
- re-enable MD2 (see http://www.ietf.org/ietf/IPR/RSA-MD-all)

* Thu Feb 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix s390 patch

* Fri Dec 8 2000 Than Ngo <than@redhat.com>
- added support s390

* Mon Nov 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove -Wa,* and -m* compiler flags from the default Configure file (#20656)
- add the CA.pl man page to the perl subpackage

* Thu Nov  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- always build with -mcpu=ev5 on alpha

* Tue Oct 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- add a symlink from cert.pem to ca-bundle.crt

* Wed Oct 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- add a ca-bundle file for packages like Samba to reference for CA certificates

* Tue Oct 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove libcrypto's crypt(), which doesn't handle md5crypt (#19295)

* Mon Oct  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- add unzip as a buildprereq (#17662)
- update m2crypto to 0.05-snap4

* Tue Sep 26 2000 Bill Nottingham <notting@redhat.com>
- fix some issues in building when it's not installed

* Wed Sep  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- make sure the headers we include are the ones we built with (aaaaarrgh!)

* Fri Sep  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- add Richard Henderson's patch for BN on ia64
- clean up the changelog

* Tue Aug 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix the building of python modules without openssl-devel already installed

* Wed Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- byte-compile python extensions without the build-root
- adjust the makefile to not remove temporary files (like .key files when
  building .csr files) by marking them as .PRECIOUS

* Sat Aug 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- break out python extensions into a subpackage

* Mon Jul 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak the makefile some more

* Tue Jul 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable MD2 support

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable MDC2 support

* Sun Jul  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak the disabling of RC5, IDEA support
- tweak the makefile

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- strip binaries and libraries
- rework certificate makefile to have the right parts for Apache

* Wed Jun 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- use %%{_perl} instead of /usr/bin/perl
- disable alpha until it passes its own test suite

* Fri Jun  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- move the passwd.1 man page out of the passwd package's way

* Fri Jun  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 0.9.5a, modified for U.S.
- add perl as a build-time requirement
- move certificate makefile to another package
- disable RC5, IDEA, RSA support
- remove optimizations for now

* Wed Mar  1 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- Bero told me to move the Makefile into this package

* Wed Mar  1 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- add lib*.so symlinks to link dynamically against shared libs

* Tue Feb 29 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 0.9.5
- run ldconfig directly in post/postun
- add FAQ

* Sat Dec 18 1999 Bernhard Rosenkrdnzer <bero@redhat.de>
- Fix build on non-x86 platforms

* Fri Nov 12 1999 Bernhard Rosenkrdnzer <bero@redhat.de>
- move /usr/share/ssl/* from -devel to main package

* Tue Oct 26 1999 Bernhard Rosenkrdnzer <bero@redhat.de>
- inital packaging
- changes from base:
  - Move /usr/local/ssl to /usr/share/ssl for FHS compliance
  - handle RPM_OPT_FLAGS
