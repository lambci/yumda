%bcond_without dane
Summary: A TLS protocol implementation
Name: gnutls
Version: 3.3.29
Release: 9%{?dist}
# The libraries are LGPLv2.1+, utilities are GPLv3+
License: GPLv3+ and LGPLv2+
Group: System Environment/Libraries
BuildRequires: p11-kit-devel >= 0.23.1, gettext
BuildRequires: zlib-devel, readline-devel, libtasn1-devel >= 3.8
BuildRequires: libtool, automake, autoconf, texinfo
BuildRequires: autogen-libopts-devel >= 5.18 autogen gettext-devel
BuildRequires: nettle-devel >= 2.7.1
BuildRequires: trousers-devel >= 0.3.11.2
BuildRequires: libidn-devel
BuildRequires: gperf
BuildRequires: fipscheck
BuildRequires: softhsm, net-tools
Requires: p11-kit-trust
# The automatic dependency on libtasn1 and p11-kit is insufficient,
Requires: libtasn1 >= 3.9
Requires: p11-kit >= 0.23.1
Requires: trousers >= 0.3.11.2
%if %{with dane}
BuildRequires: unbound-devel unbound-libs
%endif
URL: http://www.gnutls.org/
#Source0: ftp://ftp.gnutls.org/gcrypt/gnutls/%{name}-%{version}.tar.xz
#Source1: ftp://ftp.gnutls.org/gcrypt/gnutls/%{name}-%{version}.tar.xz.sig
# XXX patent tainted code removed.
Source0: %{name}-%{version}-hobbled.tar.xz
Source1: libgnutls-config
Source2: hobble-gnutls
Patch1: gnutls-3.2.7-rpath.patch
Patch2: gnutls-3.1.11-nosrp.patch
Patch4: gnutls-3.3.8-fips-key.patch
Patch5: gnutls-3.3.8-padlock-disable.patch
# In 3.3.8 we were shipping an early backport of a fix in GNUTLS_E_APPLICATION_DATA
# behavior, which was using 3.4.0 semantics. We continue shipping to support
# any applications depending on that.
Patch6: gnutls-3.3.22-eapp-data.patch
Patch7: gnutls-3.3.26-dh-params-1024.patch
# Backport serv --sni-hostname option support (rhbz#1444792)
Patch8: gnutls-3.3.29-serv-sni-hostname.patch
Patch9: gnutls-3.3.29-serv-unrec-name.patch
Patch10: gnutls-3.3.29-cli-sni-hostname.patch
Patch11: gnutls-3.3.29-tests-sni-hostname.patch
# Do not try to retrieve PIN from URI more than once
Patch12: gnutls-3.3.29-pkcs11-retrieve-pin-from-uri-once.patch
# Backport of fixes to address CVE-2018-10844 CVE-2018-10845 CVE-2018-10846
# (rhbz#1589708 rhbz#1589707 rhbz1589704)
Patch13: gnutls-3.3.29-dummy-wait-account-len-field.patch
Patch14: gnutls-3.3.29-dummy-wait-hash-same-amount-of-blocks.patch
Patch15: gnutls-3.3.29-cbc-mac-verify-ssl3-min-pad.patch
Patch16: gnutls-3.3.29-remove-hmac-sha384-sha256-from-default.patch
# Adjustment on tests
Patch17: gnutls-3.3.29-do-not-run-sni-hostname-windows.patch
# Backport testpkcs11 test. This test checks rhbz#1375307
Patch18: gnutls-3.3.29-testpkcs11.patch
# Disable failing PKCS#11 tests brought from master branch. The reasons are:
# - ECC key generation without login is not supported
# - Certificates are marked as private objects
# - "--load-pubkey" option is not supported
# - "--test-sign" option is not supported
# - Certificates do not inherit its ID from the private key
Patch19: gnutls-3.3.29-disable-failing-tests.patch
# Do not mark certificates as private objects and re-enable test for this
Patch20: gnutls-3.3.29-do-not-mark-object-as-private.patch
Patch21: gnutls-3.3.29-re-enable-check-cert-write.patch
# Increase the length of the RSA keys generated in testpkcs11 to 2048 bits.
# This allows the test to run in FIPS mode
Patch22: gnutls-3.3.29-tests-pkcs11-increase-RSA-gen-size.patch
# Enlarge buffer size to support resumption with large keys (rhbz#1542461)
Patch23: gnutls-3.3.29-serv-large-key-resumption.patch
# HMAC-SHA-256 cipher suites brought back downstream for compatibility
# The priority was set below AEAD
Patch24: gnutls-3.3.29-bring-back-hmac-sha256.patch
# Run KAT startup test for ECDSA (using secp256r1 curve) (rhbz#1673919)
Patch25: gnutls-3.3.29-fips140-fix-ecdsa-kat-selftest.patch
# Wildcard bundling exception https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib) = 20130424

Prefix: %{_prefix}

%description
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 

%package c++
Summary: The C++ interface to GnuTLS
Requires: %{name}%{?_isa} = %{version}-%{release}
Prefix: %{_prefix}

%description c++
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains the C++ interface for the GnuTLS library.

%package utils
License: GPLv3+
Summary: Command line tools for TLS protocol
Group: Applications/System
Requires: %{name}%{?_isa} = %{version}-%{release}
%if %{with dane}
Requires: %{name}-dane%{?_isa} = %{version}-%{release}
%endif
Prefix: %{_prefix}

%description utils
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains command line TLS client and server and certificate
manipulation tools.

%if %{with dane}
%package dane
Summary: A DANE protocol implementation for GnuTLS
Requires: %{name}%{?_isa} = %{version}-%{release}
Prefix: %{_prefix}

%description dane
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS 
protocols and technologies around them. It provides a simple C language 
application programming interface (API) to access the secure communications 
protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and 
other required structures. 
This package contains library that implements the DANE protocol for verifying
TLS certificates through DNSSEC.
%endif

%prep
%setup -q

%patch1 -p1 -b .rpath
%patch2 -p1 -b .nosrp
%patch4 -p1 -b .fips-key
%patch5 -p1 -b .padlock-disable
%patch6 -p1 -b .eapp-data
%patch7 -p1 -b .dh-1024
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1

sed 's/gnutls_srp.c//g' -i lib/Makefile.in
sed 's/gnutls_srp.lo//g' -i lib/Makefile.in
rm -f lib/minitasn1/*.c lib/minitasn1/*.h
rm -f src/libopts/*.c src/libopts/*.h src/libopts/compat/*.c src/libopts/compat/*.h 

# Touch man pages to avoid them to be regenerated after patches which change
# .def files
touch doc/manpages/gnutls-serv.1
touch doc/manpages/gnutls-cli.1

# Fix permissions for files brought by patches
chmod ugo+x %{_builddir}/%{name}-%{version}/tests/testpkcs11.sh
chmod ugo+x %{_builddir}/%{name}-%{version}/tests/sni-hostname.sh

%{SOURCE2} -e
autoreconf -if

%build
export LDFLAGS="-Wl,--no-add-needed"

%configure --with-libtasn1-prefix=%{_prefix} \
	   --with-default-trust-store-pkcs11="pkcs11:model=p11-kit-trust;manufacturer=PKCS%2311%20Kit" \
           --with-included-libcfg \
	   --with-arcfour128 \
	   --with-ssl3 \
           --disable-static \
           --disable-openssl-compatibility \
           --disable-srp-authentication \
	   --disable-non-suiteb-curves \
	   --with-trousers-lib=%{_libdir}/libtspi.so.1 \
	   --enable-fips140-mode \
           --disable-guile \
%if %{with dane}
	   --with-unbound-root-key-file=/var/lib/unbound/root.key \
           --enable-dane \
%else
           --disable-dane \
%endif
           --disable-rpath
# Note that the arm hack above is not quite right and the proper thing would
# be to compile guile with largefile support.
make %{?_smp_mflags}

%define __spec_install_post \
	%{?__debug_package:%{__debug_install_post}} \
	%{__arch_install_post} \
	%{__os_install_post} \
	fipshmac -d $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_libdir}/libgnutls.so.28.*.* \
	file=`basename $RPM_BUILD_ROOT%{_libdir}/libgnutls.so.28.*.hmac` && mv $RPM_BUILD_ROOT%{_libdir}/$file $RPM_BUILD_ROOT%{_libdir}/.$file && ln -s .$file $RPM_BUILD_ROOT%{_libdir}/.libgnutls.so.28.hmac \
%{nil}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_bindir}/srptool
rm -f $RPM_BUILD_ROOT%{_bindir}/gnutls-srpcrypt
cp -f %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/libgnutls-config
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/srptool.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/*srp*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libguile*.a
%if %{without dane}
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gnutls-dane.pc
%endif

%files
%defattr(-,root,root,-)
%license COPYING COPYING.LESSER
%{_libdir}/libgnutls.so.28*
%{_libdir}/.libgnutls.so.28*.hmac

%files c++
%{_libdir}/libgnutlsxx.so.*

%files utils
%defattr(-,root,root,-)
%{_bindir}/certtool
%{_bindir}/tpmtool
%{_bindir}/ocsptool
%{_bindir}/psktool
%{_bindir}/p11tool
%{_bindir}/crywrap
%if %{with dane}
%{_bindir}/danetool
%endif
%{_bindir}/gnutls*
%doc doc/certtool.cfg

%if %{with dane}
%files dane
%defattr(-,root,root,-)
%{_libdir}/libgnutls-dane.so.*
%endif

%exclude %{_bindir}/libgnutls*-config
%exclude %{_includedir}/*
%exclude %{_libdir}/libgnutls*.so
%exclude %{_libdir}/.libgnutls.so.*.hmac
%exclude %{_libdir}/pkgconfig
%exclude %{_mandir}
%exclude %{_infodir}
%exclude %{_datadir}/locale

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Feb 12 2019 Anderson Sasaki <ansasaki@redhat.com> 3.3.29-9
- Make sure the FIPS startup KAT selftest run for ECDSA (#1673919)

* Fri Jul 20 2018 Anderson Sasaki <ansasaki@redhat.com> 3.3.29-8
- Backported --sni-hostname option which allows overriding the hostname
  advertised to the peer (#1444792)
- Improved counter-measures in TLS CBC record padding for lucky13 attack
  (CVE-2018-10844, #1589704, CVE-2018-10845, #1589707)
- Added counter-measures for "Just in Time" PRIME + PROBE cache-based attack
  (CVE-2018-10846, #1589708)
- Address p11tool issue in object deletion in batch mode (#1375307)
- Backport PKCS#11 tests from master branch. Some tests were disabled due to
  unsupported features in 3.3.x (--load-pubkey and --test-sign options, ECC key
  generation without login, and certificates do not inherit ID from the private
  key)
- p11tool explicitly marks certificates and public keys as NOT private objects
  and private keys as private objects
- Enlarge buffer size to support resumption with large keys (#1542461)
- Legacy HMAC-SHA384 cipher suites were disabled by default
- Added DSA key generation to p11tool (#1464896)
- Address session renegotiation issue using client certificate (#1434091)
- Address issue when importing private keys into Atos HSM (#1460125)

* Fri May 26 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.26-9
- Address crash in OCSP status request extension, by eliminating the
  unneeded parsing (CVE-2017-7507, #1455828)

* Wed Apr 26 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.26-7
- Address interoperability issue with 3.5.x (#1388932)
- Reject CAs which are both trusted and blacklisted in trust module (#1375303)
- Added new functions to set issuer and subject ID in certificates (#1378373)
- Reject connections with less than 1024-bit DH parameters (#1335931)
- Fix issue that made GnuTLS parse only the first 32 extensions (#1383748)
- Mention limitations of certtool in manpage (#1375463)
- Read PKCS#8 files with HMAC-SHA256 -as generated by openssl 1.1 (#1380642)
- Do not link directly to trousers but instead use dlopen (#1379739)
- Fix incorrect OCSP validation (#1377569)
- Added support for pin-value in PKCS#11 URIs (#1379283)
- Added the --id option to p11tool (#1399232)
- Improved sanity checks in RSA key generation (#1444780)
- Addressed CVE-2017-5334, CVE-2017-5335, CVE-2017-5336, CVE-2017-5337,
  CVE-2017-7869

* Tue Jul 12 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.24-1
- Addressed issue with DSA public keys smaller than 2^1024 (#1238279)
- Addressed two-byte buffer overflow in the DTLS-0.9 protocol (#1209365)
- When writing certificates to smart cards write the CKA_ISSUER and
  CKA_SERIAL_NUMBER fields to allow NSS reading them (#1272179)
- Use the shared system certificate store (#1110750)
- Address MD5 transcript collision attacks in TLS key exchange (#1289888, 
  CVE-2015-7575)
- Allow hashing data over 2^32 bytes (#1306953)
- Ensure written PKCS#11 public keys are not marked as private (#1339453)
- Ensure secure_getenv() is called on all uses of environment variables
  (#1344591).
- Fix issues related to PKCS #11 private key listing on certain HSMs
  (#1351389)

* Fri Jun  5 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-13
- Corrected reseed and respect of max_number_of_bits_per_request in 
  FIPS140-2 mode. Also enhanced the initial tests. (#1228199)

* Mon Jan  5 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-12
- corrected fix of handshake buffer resets (#1153106)

* Thu Dec 11 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-11
- Applied fix for urandom FD in FIPS140 mode (#1165047)
- Applied fix for FIPS140-2 related regression (#1110696)

* Tue Dec  2 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-10
- Amended fix for urandom FD to avoid regression in FIPS140 mode (#1165047)

* Tue Nov 18 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-9
- Amended fix for FIPS enforcement issue (#1163848)
- Fixed issue with applications that close all file descriptors (#1165047)

* Thu Nov 13 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-8
- Applied fix for FIPS enforcement issue when only /etc/system-fips
  existed (#1163848)

* Fri Nov  7 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-7
- Applied fix for CVE-2014-8564 (#1161473)

* Wed Oct 29 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-6
- when generating test DH keys, enforce the q_bits.

* Tue Oct 21 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-5
- do not enforce FIPS140-2 policies in non-FIPS140 mode (#1154774)

* Thu Oct 16 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-4
- reverted change to use the p11-kit certificate storage (#1110750)
- added functions to test DH/ECDH in FIPS-140-2 mode and fixed
  RSA key generation (#1110696)
- added manual dependencies on libtasn1 3.8 as well as p11-kit 0.20.7
- fixed SHA224 in SSSE3 optimized code
- fixed issue with handshake buffer resets (#1153106)
- fixed issue in RSA key generation with specific seeds in FIPS140-2 mode

* Wed Oct 01 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-3
- added dependency on libtasn1 3.8 (#1110696)

* Thu Sep 18 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-2
- disabled padlock CPU support in FIPS140-2 mode

* Thu Sep 18 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-1
- updated to latest stable release

* Fri Sep 05 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8-1.b2
- updated with latest bug fixes for 3.3.x branch
- delete bundled files

* Thu Sep 04 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.8b1-1
- updated with latest bug fixes for 3.3.x branch

* Fri Aug 22 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.7-1
- new upstream release (#1110696)
- allow DSA/DH key generation with 1024 when not in FIPS140-2 mode (#1132705)

* Fri Aug 15 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.7b1-1
- updated with latest bug fixes for 3.3.x branch
- utilize the p11-kit trust store (#1110750)

* Tue Jul 29 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.6-2
- correct path of fipscheck links

* Wed Jul 23 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.3.6-1
- rebased to 3.3.6 and enabled fips mode (#1110696)

* Wed May 28 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.1.18-9
- fix session ID length check (#1102027)
- fixes null pointer dereference (#1101727)

* Tue Feb 25 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.1.18-8
- fixes CVE-2014-0092 (#1071815)

* Fri Feb 14 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.1.18-7
- fixes CVE-2014-1959

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.1.18-6
- Mass rebuild 2014-01-24

* Tue Jan 14 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.1.18-5
- Fixed issue with gnutls.info not being available (#1053487)

* Tue Jan 14 2014 Tomáš Mráz <tmraz@redhat.com> 3.1.18-4
- build the crywrap tool

* Thu Jan 02 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.1.18-3
- fixes crash in gnutls_global_deinit (#1047037)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.1.18-2
- Mass rebuild 2013-12-27

* Mon Dec 23 2013 Nikos Mavrogiannopoulos <nmav@redhat.com> 3.1.18-1
- new upstream release (#1040886)
- Use the correct root key for unbound

* Tue Nov  5 2013 Tomáš Mráz <tmraz@redhat.com> 3.1.16-1
- new upstream release
- fixes CVE-2013-4466 off-by-one in dane_query_tlsa()

* Tue Oct 29 2013 Tomáš Mráz <tmraz@redhat.com> 3.1.15-1
- new upstream release
- fixes CVE-2013-4466 buffer overflow in handling DANE entries

* Mon Jul 15 2013 Tomáš Mráz <tmraz@redhat.com> 3.1.13-1
- new upstream release

* Thu May 23 2013 Tomáš Mráz <tmraz@redhat.com> 3.1.11-1
- new upstream release
- enable ECC NIST Suite B curves

* Mon Mar 25 2013 Tomas Mraz <tmraz@redhat.com> 3.1.10-1
- new upstream release
- license of the library is back to LGPLv2.1+

* Fri Mar 15 2013 Tomas Mraz <tmraz@redhat.com> 3.1.9-1
- new upstream release

* Thu Mar  7 2013 Tomas Mraz <tmraz@redhat.com> 3.1.8-3
- drop the temporary old library

* Tue Feb 26 2013 Tomas Mraz <tmraz@redhat.com> 3.1.8-2
- don't send ECC algos as supported (#913797)

* Thu Feb 21 2013 Tomas Mraz <tmraz@redhat.com> 3.1.8-1
- new upstream version

* Wed Feb  6 2013 Tomas Mraz <tmraz@redhat.com> 3.1.7-1
- new upstream version, requires rebuild of dependencies
- this release temporarily includes old compatibility .so

* Tue Feb  5 2013 Tomas Mraz <tmraz@redhat.com> 2.12.22-2
- rebuilt with new libtasn1
- make guile bindings optional - breaks i686 build and there is
  no dependent package

* Tue Jan  8 2013 Tomas Mraz <tmraz@redhat.com> 2.12.22-1
- new upstream version

* Wed Nov 28 2012 Tomas Mraz <tmraz@redhat.com> 2.12.21-2
- use RSA bit sizes supported by libgcrypt in FIPS mode for security
  levels (#879643)

* Fri Nov  9 2012 Tomas Mraz <tmraz@redhat.com> 2.12.21-1
- new upstream version

* Thu Nov  1 2012 Tomas Mraz <tmraz@redhat.com> 2.12.20-4
- negotiate only FIPS approved algorithms in the FIPS mode (#871826)

* Wed Aug  8 2012 Tomas Mraz <tmraz@redhat.com> 2.12.20-3
- fix the gnutls-cli-debug manpage - patch by Peter Schiffer

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 Tomas Mraz <tmraz@redhat.com> 2.12.20-1
- new upstream version

* Fri May 18 2012 Tomas Mraz <tmraz@redhat.com> 2.12.19-1
- new upstream version

* Thu Mar 29 2012 Tomas Mraz <tmraz@redhat.com> 2.12.18-1
- new upstream version

* Thu Mar  8 2012 Tomas Mraz <tmraz@redhat.com> 2.12.17-1
- new upstream version
- fix leaks in key generation (#796302)

* Fri Feb 03 2012 Kevin Fenzi <kevin@scrye.com> - 2.12.14-3
- Disable largefile on arm arch. (#787287)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov  8 2011 Tomas Mraz <tmraz@redhat.com> 2.12.14-1
- new upstream version

* Mon Oct 24 2011 Tomas Mraz <tmraz@redhat.com> 2.12.12-1
- new upstream version

* Thu Sep 29 2011 Tomas Mraz <tmraz@redhat.com> 2.12.11-1
- new upstream version

* Fri Aug 26 2011 Tomas Mraz <tmraz@redhat.com> 2.12.9-1
- new upstream version

* Tue Aug 16 2011 Tomas Mraz <tmraz@redhat.com> 2.12.8-1
- new upstream version

* Mon Jul 25 2011 Tomas Mraz <tmraz@redhat.com> 2.12.7-2
- fix problem when using new libgcrypt
- split libgnutlsxx to a subpackage (#455146)
- drop libgnutls-openssl (#460310)

* Tue Jun 21 2011 Tomas Mraz <tmraz@redhat.com> 2.12.7-1
- new upstream version

* Mon May  9 2011 Tomas Mraz <tmraz@redhat.com> 2.12.4-1
- new upstream version

* Tue Apr 26 2011 Tomas Mraz <tmraz@redhat.com> 2.12.3-1
- new upstream version

* Mon Apr 18 2011 Tomas Mraz <tmraz@redhat.com> 2.12.2-1
- new upstream version

* Thu Mar  3 2011 Tomas Mraz <tmraz@redhat.com> 2.10.5-1
- new upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec  8 2010 Tomas Mraz <tmraz@redhat.com> 2.10.4-1
- new upstream version

* Thu Dec  2 2010 Tomas Mraz <tmraz@redhat.com> 2.10.3-2
- fix buffer overflow in gnutls-serv (#659259)

* Fri Nov 19 2010 Tomas Mraz <tmraz@redhat.com> 2.10.3-1
- new upstream version

* Thu Sep 30 2010 Tomas Mraz <tmraz@redhat.com> 2.10.2-1
- new upstream version

* Wed Sep 29 2010 jkeating - 2.10.1-4
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Tomas Mraz <tmraz@redhat.com> 2.10.1-3
- more patching for internal errors regression (#629858)
  patch by Vivek Dasmohapatra

* Tue Sep 21 2010 Tomas Mraz <tmraz@redhat.com> 2.10.1-2
- backported patch from upstream git hopefully fixing internal errors
  (#629858)

* Wed Aug  4 2010 Tomas Mraz <tmraz@redhat.com> 2.10.1-1
- new upstream version

* Wed Jun  2 2010 Tomas Mraz <tmraz@redhat.com> 2.8.6-2
- add support for safe renegotiation CVE-2009-3555 (#533125)

* Wed May 12 2010 Tomas Mraz <tmraz@redhat.com> 2.8.6-1
- upgrade to a new upstream version

* Mon Feb 15 2010 Rex Dieter <rdieter@fedoraproject.org> 2.8.5-4
- FTBFS gnutls-2.8.5-3.fc13: ImplicitDSOLinking (#564624)

* Thu Jan 28 2010 Tomas Mraz <tmraz@redhat.com> 2.8.5-3
- drop superfluous rpath from binaries
- do not call autoreconf during build
- specify the license on utils subpackage

* Mon Jan 18 2010 Tomas Mraz <tmraz@redhat.com> 2.8.5-2
- do not create static libraries (#556052)

* Mon Nov  2 2009 Tomas Mraz <tmraz@redhat.com> 2.8.5-1
- upgrade to a new upstream version

* Wed Sep 23 2009 Tomas Mraz <tmraz@redhat.com> 2.8.4-1
- upgrade to a new upstream version

* Fri Aug 14 2009 Tomas Mraz <tmraz@redhat.com> 2.8.3-1
- upgrade to a new upstream version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Tomas Mraz <tmraz@redhat.com> 2.8.1-1
- upgrade to a new upstream version

* Wed Jun  3 2009 Tomas Mraz <tmraz@redhat.com> 2.8.0-1
- upgrade to a new upstream version

* Mon May  4 2009 Tomas Mraz <tmraz@redhat.com> 2.6.6-1
- upgrade to a new upstream version - security fixes

* Tue Apr 14 2009 Tomas Mraz <tmraz@redhat.com> 2.6.5-1
- upgrade to a new upstream version, minor bugfixes only

* Fri Mar  6 2009 Tomas Mraz <tmraz@redhat.com> 2.6.4-1
- upgrade to a new upstream version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Tomas Mraz <tmraz@redhat.com> 2.6.3-1
- upgrade to a new upstream version

* Thu Dec  4 2008 Tomas Mraz <tmraz@redhat.com> 2.6.2-1
- upgrade to a new upstream version

* Tue Nov 11 2008 Tomas Mraz <tmraz@redhat.com> 2.4.2-3
- fix chain verification issue CVE-2008-4989 (#470079)

* Thu Sep 25 2008 Tomas Mraz <tmraz@redhat.com> 2.4.2-2
- add guile subpackage (#463735)
- force new libtool through autoreconf to drop unnecessary rpaths

* Tue Sep 23 2008 Tomas Mraz <tmraz@redhat.com> 2.4.2-1
- new upstream version

* Tue Jul  1 2008 Tomas Mraz <tmraz@redhat.com> 2.4.1-1
- new upstream version
- correct the license tag
- explicit --with-included-opencdk not needed
- use external lzo library, internal not included anymore

* Tue Jun 24 2008 Tomas Mraz <tmraz@redhat.com> 2.4.0-1
- upgrade to latest upstream

* Tue May 20 2008 Tomas Mraz <tmraz@redhat.com> 2.0.4-3
- fix three security issues in gnutls handshake - GNUTLS-SA-2008-1
  (#447461, #447462, #447463)

* Mon Feb  4 2008 Joe Orton <jorton@redhat.com> 2.0.4-2
- use system libtasn1

* Tue Dec  4 2007 Tomas Mraz <tmraz@redhat.com> 2.0.4-1
- upgrade to latest upstream

* Tue Aug 21 2007 Tomas Mraz <tmraz@redhat.com> 1.6.3-2
- license tag fix

* Wed Jun  6 2007 Tomas Mraz <tmraz@redhat.com> 1.6.3-1
- upgrade to latest upstream (#232445)

* Tue Apr 10 2007 Tomas Mraz <tmraz@redhat.com> 1.4.5-2
- properly require install-info (patch by Ville Skyttä)
- standard buildroot and use dist tag
- add COPYING and README to doc

* Wed Feb  7 2007 Tomas Mraz <tmraz@redhat.com> 1.4.5-1
- new upstream version
- drop libtermcap-devel from buildrequires

* Thu Sep 14 2006 Tomas Mraz <tmraz@redhat.com> 1.4.1-2
- detect forged signatures - CVE-2006-4790 (#206411), patch
  from upstream

* Tue Jul 18 2006 Tomas Mraz <tmraz@redhat.com> - 1.4.1-1
- upgrade to new upstream version, only minor changes

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.4.0-1.1
- rebuild

* Wed Jun 14 2006 Tomas Mraz <tmraz@redhat.com> - 1.4.0-1
- upgrade to new upstream version (#192070), rebuild
  of dependent packages required

* Tue May 16 2006 Tomas Mraz <tmraz@redhat.com> - 1.2.10-2
- added missing buildrequires

* Mon Feb 13 2006 Tomas Mraz <tmraz@redhat.com> - 1.2.10-1
- updated to new version (fixes CVE-2006-0645)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1.2.9-3
- rebuilt

* Fri Dec  9 2005 Tomas Mraz <tmraz@redhat.com> 1.2.9-2
- replaced *-config scripts with calls to pkg-config to
  solve multilib conflicts

* Wed Nov 23 2005 Tomas Mraz <tmraz@redhat.com> 1.2.9-1
- upgrade to newest upstream
- removed .la files (#172635)

* Sun Aug  7 2005 Tomas Mraz <tmraz@redhat.com> 1.2.6-1
- upgrade to newest upstream (rebuild of dependencies necessary)

* Mon Jul  4 2005 Tomas Mraz <tmraz@redhat.com> 1.0.25-2
- split the command line tools to utils subpackage

* Sat Apr 30 2005 Tomas Mraz <tmraz@redhat.com> 1.0.25-1
- new upstream version fixes potential DOS attack

* Sat Apr 23 2005 Tomas Mraz <tmraz@redhat.com> 1.0.24-2
- readd the version script dropped by upstream

* Fri Apr 22 2005 Tomas Mraz <tmraz@redhat.com> 1.0.24-1
- update to the latest upstream version on the 1.0 branch

* Wed Mar  2 2005 Warren Togami <wtogami@redhat.com> 1.0.20-6
- gcc4 rebuild

* Tue Jan  4 2005 Ivana Varekova <varekova@redhat.com> 1.0.20-5
- add gnutls Requires zlib-devel (#144069)

* Mon Nov 08 2004 Colin Walters <walters@redhat.com> 1.0.20-4
- Make gnutls-devel Require libgcrypt-devel

* Tue Sep 21 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-3
- rebuild with release++, otherwise unchanged.

* Tue Sep  7 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-2
- patent tainted SRP code removed.

* Sun Sep  5 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-1
- update to 1.0.20.
- add --with-included-opencdk --with-included-libtasn1
- add --with-included-libcfg --with-included-lzo
- add --disable-srp-authentication.
- do "make check" after build.

* Fri Mar 21 2003 Jeff Johnson <jbj@redhat.com> 0.9.2-1
- upgrade to 0.9.2

* Tue Jun 25 2002 Jeff Johnson <jbj@redhat.com> 0.4.4-1
- update to 0.4.4.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat May 25 2002 Jeff Johnson <jbj@redhat.com> 0.4.3-1
- update to 0.4.3.

* Tue May 21 2002 Jeff Johnson <jbj@redhat.com> 0.4.2-1
- update to 0.4.2.
- change license to LGPL.
- include splint annotations patch.

* Tue Apr  2 2002 Nalin Dahyabhai <nalin@redhat.com> 0.4.0-1
- update to 0.4.0

* Thu Jan 17 2002 Nalin Dahyabhai <nalin@redhat.com> 0.3.2-1
- update to 0.3.2

* Thu Jan 10 2002 Nalin Dahyabhai <nalin@redhat.com> 0.3.0-1
- add a URL

* Thu Dec 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- initial package
