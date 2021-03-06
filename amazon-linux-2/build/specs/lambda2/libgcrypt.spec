Name: libgcrypt
Version: 1.5.3
Release: 14%{?dist}.0.2
URL: http://www.gnupg.org/
Source0: libgcrypt-%{version}-hobbled.tar.xz
# The original libgcrypt sources now contain potentially patented ECC
# cipher support. We have to remove it in the tarball we ship with
# the hobble-libgcrypt script.
#Source0: ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2
#Source1: ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2.sig
Source2: wk@g10code.com
Source3: hobble-libgcrypt
# do not run the ecc curves test
Patch1: libgcrypt-1.5.0-noecc.patch
# make FIPS hmac compatible with fipscheck - non upstreamable
Patch2: libgcrypt-1.5.0-use-fipscheck.patch
# fix tests in the FIPS mode, fix the FIPS-186-3 DSA keygen
Patch5: libgcrypt-1.5.0-tests.patch
# make the FIPS-186-3 DSA CAVS testable
Patch7: libgcrypt-1.5.3-fips-cavs.patch
# fix for memory leaks an other errors found by Coverity scan
Patch9: libgcrypt-1.5.0-leak.patch
# use poll instead of select when gathering randomness
Patch11: libgcrypt-1.5.1-use-poll.patch
# compile rijndael with -fno-strict-aliasing
Patch12: libgcrypt-1.5.2-aliasing.patch
# slight optimalization of mpicoder.c to silence Valgrind (#968288)
Patch13: libgcrypt-1.5.2-mpicoder-gccopt.patch
# pbkdf2 speedup - upstream
Patch15: libgcrypt-1.5.3-pbkdf-speedup.patch
# fix bug in whirlpool implementation (for backwards compatibility
# with files generated with buggy version set environment
# varible GCRYPT_WHIRLPOOL_BUG
Patch16: libgcrypt-1.5.3-whirlpool-bug.patch
# FIPS DRBG
Patch17: libgcrypt-1.5.3-drbg.patch
# Run the FIPS mode initialization in the shared library constructor
Patch18: libgcrypt-1.5.3-fips-ctor.patch
# Make it possible to run the test suite in the FIPS mode
Patch19: libgcrypt-1.5.3-fips-test.patch
# Make the FIPS RSA keygen to be FIPS 186-4 compliant
Patch20: libgcrypt-1.5.3-rsa-fips-keygen.patch
# add configurable source of RNG seed and seed by default
# from /dev/urandom in the FIPS mode
Patch21: libgcrypt-1.5.3-fips-cfgrandom.patch
# update the selftests for new FIPS requirements
Patch22: libgcrypt-1.5.3-fips-reqs.patch
# use only urandom if /dev/random cannot be opened
Patch24: libgcrypt-1.5.3-urandom-only.patch
# fix predictable PRNG output
Patch26: libgcrypt-1.5.3-rng-predictable.patch
# add drgb cavs test
Patch27: libgcrypt-1.5.3-drbg-cavs.patch
# allow reinitialization of ath in the FIPS mode
Patch28: libgcrypt-1.5.3-ath-reinstall.patch
# allow auto-initialization of drbg
Patch29: libgcrypt-1.5.3-drbg-init.patch

# Technically LGPLv2.1+, but Fedora's table doesn't draw a distinction.
# Documentation and some utilities are GPLv2+ licensed. These files
# are in the devel subpackage.
License: LGPLv2+
Summary: A general-purpose cryptography library
BuildRequires: gawk, libgpg-error-devel >= 1.4, pkgconfig
BuildRequires: fipscheck
# This is needed only when patching the .texi doc.
BuildRequires: texinfo
Group: System Environment/Libraries

Prefix: %{_prefix}

%description
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This is a development version.

%prep
%setup -q
%{SOURCE3}
%patch1 -p1 -b .noecc
%patch2 -p1 -b .use-fipscheck
%patch5 -p1 -b .tests
%patch7 -p1 -b .cavs
%patch9 -p1 -b .leak
%patch11 -p1 -b .use-poll
%patch12 -p1 -b .aliasing
%patch13 -p1 -b .gccopt
%patch15 -p1 -b .pbkdf-speedup
%patch16 -p1 -b .whirlpool-bug
%patch17 -p1 -b .drbg
%patch18 -p1 -b .fips-ctor
%patch19 -p1 -b .fips-test
%patch20 -p1 -b .fips-keygen
%patch21 -p1 -b .cfgrandom
%patch22 -p1 -b .fips-reqs
%patch24 -p1 -b .urandom-only
%patch26 -p1 -b .rng-predictable
%patch27 -p1 -b .drbg-cavs
%patch28 -p1 -b .ath-reinstall
%patch29 -p1 -b .drbg-init

%build
%configure --disable-static \
     --enable-noexecstack \
     --enable-hmac-binary-check \
     --enable-pubkey-ciphers='dsa elgamal rsa' \
     --disable-O-flag-munging
make %{?_smp_mflags}

# Add generation of HMAC checksums of the final stripped binaries 
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    fipshmac $RPM_BUILD_ROOT%{_libdir}/*.so.?? \
%{nil}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir ${RPM_BUILD_ROOT}/%{_libdir}/*.la
/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_libdir}

# Create /etc/gcrypt (hardwired, not dependent on the configure invocation) so
# that _someone_ owns it.
mkdir -p -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/gcrypt

%files
%defattr(-,root,root,-)
%license COPYING.LIB
%dir %{_sysconfdir}/gcrypt
%{_libdir}/libgcrypt.so.*
%{_libdir}/.libgcrypt.so.*.hmac

%exclude %{_includedir}
%exclude %{_infodir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}
%exclude %{_bindir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Feb 28 2017 Tomáš Mráz <tmraz@redhat.com> 1.5.3-14
- add DRBG CAVS driver and other necessary CAVS driver updates (#1172568)
- allow ath reinitialization in FIPS mode
- allow for auto-initialization of DRBG

* Tue Oct 25 2016 Tomáš Mráz <tmraz@redhat.com> 1.5.3-13.1
- fix CVE-2016-6313 - predictable PRNG output (#1366105)

* Fri Apr 10 2015 Tomáš Mráz <tmraz@redhat.com> 1.5.3-13
- touch only urandom in the selftest and when /dev/random is
  unavailable for example by SELinux confinement
- fix the RSA selftest key (p q swap)

* Wed Jan 14 2015 Tomáš Mráz <tmraz@redhat.com> 1.5.3-12
- use macros instead of inline functions in the public header

* Fri Dec 12 2014 Tomáš Mráz <tmraz@redhat.com> 1.5.3-11
- do not initialize secure memory during the selftest

* Fri Nov 14 2014 Tomáš Mráz <tmraz@redhat.com> 1.5.3-10
- update the selftests for the new FIPS requirements

* Fri Oct 31 2014 Tomáš Mráz <tmraz@redhat.com> 1.5.3-9
- apply the fips-cfgrandom change also to the drbg seeding

* Tue Oct 21 2014 Tomáš Mráz <tmraz@redhat.com> 1.5.3-7
- make the RSA keygen to be compliant to FIPS 186-4 in
  FIPS mode

* Fri Sep 26 2014 Tomáš Mráz <tmraz@redhat.com> 1.5.3-5
- add FIPS DRBG implementation
- run the FIPS POST tests in shared library constructor
- make it possible to run the test suite in the FIPS mode

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.5.3-4
- Mass rebuild 2014-01-24

* Tue Jan 21 2014 Tomáš Mráz <tmraz@redhat.com> 1.5.3-3
- fix a bug in the Whirlpool hash implementation
- speed up the PBKDF2 computation

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.5.3-2
- Mass rebuild 2013-12-27

* Fri Jul 26 2013 Tomáš Mráz <tmraz@redhat.com> 1.5.3-1
- new upstream version fixing cache side-channel attack on RSA private keys

* Thu Jun 20 2013 Tomáš Mráz <tmraz@redhat.com> 1.5.2-3
- silence false error detected by valgrind (#968288)

* Thu Apr 25 2013 Tomáš Mráz <tmraz@redhat.com> 1.5.2-2
- silence strict aliasing warning in Rijndael
- apply UsrMove
- spec file cleanups

* Fri Apr 19 2013 Tomáš Mráz <tmraz@redhat.com> 1.5.2-1
- new upstream version

* Wed Mar 20 2013 Tomas Mraz <tmraz@redhat.com> 1.5.1-1
- new upstream version

* Tue Mar  5 2013 Tomas Mraz <tmraz@redhat.com> 1.5.0-11
- use poll() instead of select() when gathering randomness (#913773)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan  3 2013 Tomas Mraz <tmraz@redhat.com> 1.5.0-9
- allow empty passphrase in PBKDF2 needed for cryptsetup (=891266)

* Mon Dec  3 2012 Tomas Mraz <tmraz@redhat.com> 1.5.0-8
- fix multilib conflict in libgcrypt-config
- fix minor memory leaks and other bugs found by Coverity scan

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr  5 2012 Tomas Mraz <tmraz@redhat.com> 1.5.0-5
- Correctly rebuild the info documentation

* Wed Apr  4 2012 Tomas Mraz <tmraz@redhat.com> 1.5.0-4
- Add GCRYCTL_SET_ENFORCED_FIPS_FLAG command

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 15 2011 Kalev Lember <kalevlember@gmail.com> 1.5.0-2
- Rebuilt for rpm bug #728707

* Thu Jul 21 2011 Tomas Mraz <tmraz@redhat.com> 1.5.0-1
- new upstream version

* Mon Jun 20 2011 Tomas Mraz <tmraz@redhat.com> 1.4.6-4
- Always xor seed from /dev/urandom over /etc/gcrypt/rngseed

* Mon May 30 2011 Tomas Mraz <tmraz@redhat.com> 1.4.6-3
- Make the FIPS-186-3 DSA implementation CAVS testable
- add configurable source of RNG seed /etc/gcrypt/rngseed
  in the FIPS mode (#700388)

* Fri Feb 11 2011 Tomas Mraz <tmraz@redhat.com> 1.4.6-1
- new upstream version with minor changes

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Tomas Mraz <tmraz@redhat.com> 1.4.5-6
- fix a bug in the fips-186-3 dsa parameter generation code

* Tue Feb  1 2011 Tomas Mraz <tmraz@redhat.com> 1.4.5-5
- use /dev/urandom for seeding in the FIPS mode
- make the tests to pass in the FIPS mode also fixing
  the FIPS-186-3 DSA keygen

* Sun Feb 14 2010 Rex Dieter <rdieter@fedoraproject.org> 1.4.5-4
- FTBFS libgcrypt-1.4.5-3.fc13: ImplicitDSOLinking (#564973)

* Wed Feb  3 2010 Tomas Mraz <tmraz@redhat.com> 1.4.5-3
- drop the S390 build workaround as it is no longer needed
- additional spec file cleanups for merge review (#226008)

* Mon Dec 21 2009 Tomas Mraz <tmraz@redhat.com> 1.4.5-1
- workaround for build on S390 (#548825)
- spec file cleanups
- upgrade to new minor upstream release

* Tue Aug 11 2009 Tomas Mraz <tmraz@redhat.com> 1.4.4-8
- fix warning when installed with --excludedocs (#515961)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Tomas Mraz <tmraz@redhat.com> 1.4.4-6
- and now really apply the padlock patch

* Wed Jun 17 2009 Tomas Mraz <tmraz@redhat.com> 1.4.4-5
- fix VIA padlock RNG inline assembly call (#505724)

* Thu Mar  5 2009 Tomas Mraz <tmraz@redhat.com> 1.4.4-4
- with the integrity verification check the library needs to link to libdl
  (#488702)

* Tue Mar  3 2009 Tomas Mraz <tmraz@redhat.com> 1.4.4-3
- add hmac FIPS integrity verification check

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Tomas Mraz <tmraz@redhat.com> 1.4.4-1
- update to 1.4.4
- do not abort when the fips mode kernel flag is inaccessible
  due to permissions (#470219)
- hobble the library to drop the ECC support

* Mon Oct 20 2008 Dennis Gilmore <dennis@ausil.us> 1.4.3-2
- disable asm on sparc64

* Thu Sep 18 2008 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-1
- update to 1.4.3
- own /etc/gcrypt

* Mon Sep 15 2008 Nalin Dahyabhai <nalin@redhat.com>
- invoke make with %%{?_smp_mflags} to build faster on multi-processor
  systems (Steve Grubb)

* Mon Sep  8 2008 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-1
- update to 1.4.2

* Tue Apr 29 2008 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-1
- update to 1.4.1
- bump libgpgerror-devel requirement to 1.4, matching the requirement enforced
  by the configure script

* Thu Apr  3 2008 Joe Orton <jorton@redhat.com> 1.4.0-3
- add patch from upstream to fix severe performance regression
  in entropy gathering

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.0-2
- Autorebuild for GCC 4.3

* Mon Dec 10 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.4.0-1
- update to 1.4.0

* Tue Oct 16 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.4-6
- use ldconfig to build the soname symlink for packaging along with the
  shared library (#334731)

* Wed Aug 22 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.4-5
- add missing gawk buildrequirement
- switch from explicitly specifying the /dev/random RNG to just verifying
  that the non-LGPL ones were disabled by the configure script

* Thu Aug 16 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.4-4
- clarify license
- force use of the linux /dev/random RNG, to avoid accidentally falling back
  to others which would affect the license of the resulting library

* Mon Jul 30 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.4-3
- disable static libraries (part of #249815)

* Fri Jul 27 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.4-2
- move libgcrypt shared library to /%%{_lib} (#249815)

* Tue Feb  6 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.4-1
- update to 1.2.4

* Mon Jan 22 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.3-2
- make use of install-info more failsafe (Ville Skyttä, #223705)

* Fri Sep  1 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.2.3-1
- update to 1.2.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-3.1
- rebuild

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> 1.2.2-3
- Added missing buildreq pkgconfig

* Tue May 16 2006 Nalin Dahyabhai <nalin@redhat.com> 1.2.2-2
- remove file conflicts in libgcrypt-config by making the 64-bit version
  think the libraries are in /usr/lib (which is wrong, but which it also
  prunes from the suggest --libs output, so no harm done, hopefully)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Oct  5 2005 Nalin Dahyabhai <nalin@redhat.com> 1.2.2-1
- update to 1.2.2

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 1.2.1-1
- update to 1.2.1

* Fri Jul 30 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- another try to package the symlink

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun May  2 2004 Bill Nottingham <notting@redhat.com> - 1.2.0-1
- update to official 1.2.0

* Fri Apr 16 2004 Bill Nottingham <notting@redhat.com> - 1.1.94-1
- update to 1.1.94

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Feb 21 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlinks to shared libs at compile time

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Mar 20 2003 Jeff Johnson <jbj@redhat.com> 1.1.12-1
- upgrade to 1.1.12 (beta).

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Jeff Johnson <jbj@redhat.com>
- update to 1.1.7
- change license to LGPL.
- include splint annotations patch.
- install info pages.

* Tue Apr  2 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.6-1
- update to 1.1.6

* Thu Jan 10 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.5-1
- fix the Source tag so that it's a real URL

* Thu Dec 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- initial package
