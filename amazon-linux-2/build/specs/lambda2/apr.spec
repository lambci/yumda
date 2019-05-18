%define aprver 1

# Arches on which the multilib apr.h hack is needed:
%define multilib_arches %{ix86} ia64 ppc ppc64 s390 s390x x86_64

Summary: Apache Portable Runtime library
Name: apr
Version: 1.6.3
Release: 5%{?dist}.0.2
# ASL 2.0: everything
# ISC: network_io/apr-1.4.6/network_io/unix/inet_?to?.c
# BSD with advertising: strings/apr_snprintf.c, strings/apr_fnmatch.c,
#                   include/apr_fnmatch.h, misc/unix/getopt.c,
#                   file_io/unix/mktemp.c, strings/apr_strings.c
# BSD (3-clause): strings/apr_strnatcmp.c, include/apr_strings.h
License: ASL 2.0 and BSD with advertising and ISC and BSD
Group: System Environment/Libraries
URL: http://apr.apache.org/
Source0: http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
Source1: apr-wrapper.h
Patch2: apr-1.2.2-locktimeout.patch
Patch3: apr-1.2.2-libdir.patch
Patch4: apr-1.2.7-pkgconf.patch
Patch5: apr-rh1539844.patch
BuildRequires: autoconf, libtool, libuuid-devel, python
# To enable SCTP support
BuildRequires: lksctp-tools-devel

Prefix: %{_prefix}

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines, forming a system
portability layer to as many operating systems as possible,
including Unices, MS Win32, BeOS and OS/2.

%prep
%setup -q
%patch2 -p1 -b .locktimeout
%patch3 -p1 -b .libdir
%patch4 -p1 -b .pkgconf
%patch5 -p1 -b .rh1539844

%build
# regenerate configure script etc.
./buildconf

# Forcibly prevent detection of shm_open (which then picks up but
# does not use -lrt).
export ac_cv_search_shm_open=no

%configure --with-devrandom=/dev/urandom --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/libapr-%{aprver}.so.*

%exclude %{_includedir}
%exclude %{_bindir}/apr-%{aprver}-config
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/*.exp
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Florian Weimer <fweimer@redhat.com> - 1.6.3-4
- Fix FTBFS in test/teststr.c with GCC 8 (#1539844)

* Mon Jan 29 2018 Florian Weimer <fweimer@redhat.com> - 1.6.3-3
- Rebuild with new redhat-rpm-config build flags

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.6.3-2
- Rebuilt for switch to libxcrypt

* Wed Oct 25 2017 Luboš Uhliarik <luhliari@redhat.com> - 1.6.3-1
- new version 1.6.3

* Tue Sep 19 2017 Joe Orton <jorton@redhat.com> - 1.6.2-4
- re-enable test suite

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sat Jul 29 2017 Florian Weimer <fweimer@redhat.com> - 1.6.2-2
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Joe Orton <jorton@redhat.com> - 1.6.2-1
- update to 1.6.2 (#1460830)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 1.5.2-4
- rebuild for ICU 57.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Jan Kaluza <jkaluza@redhat.com> - 1.5.2-1
- update to 1.5.2 (#1217012)

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Jan Kaluza <jkaluza@redhat.com> - 1.5.1-1
- update to 1.5.1 (#1089917)

* Tue Nov 26 2013 Joe Orton <jorton@redhat.com> - 1.5.0-2
- update to 1.5.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Joe Orton <jorton@redhat.com> - 1.4.8-1
- update to 1.4.8 (#976972)

* Wed May 29 2013 Joe Orton <jorton@redhat.com> - 1.4.6-7
- update config.* for aarch64 (#925009)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 12 2012 Jan Kaluza <jkaluza@redhat.com> - 1.4.6-5
- fix strict-aliasing gcc warning
- remove unused SHA384 and SHA512 code

* Thu Nov 22 2012 Joe Orton <jorton@redhat.com> - 1.4.6-4
- update license

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul  6 2012 Joe Orton <jorton@redhat.com> - 1.4.6-2
- pull fix for apr_mcast_hops from upstream

* Tue Feb 14 2012 Bojan Smojver <bojan@rexursive.com> - 1.4.6-1
- bump up to 1.4.6

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 13 2011 Joe Orton <jorton@redhat.com> - 1.4.5-2
- remove deepbind patch, should no longer be necessary

* Fri May 20 2011 Bojan Smojver <bojan@rexursive.com> - 1.4.5-1
- bump up to 1.4.5

* Tue May 10 2011 Bojan Smojver <bojan@rexursive.com> - 1.4.4-2
- fix top_builddir in apr_rules.mk

* Mon May  9 2011 Bojan Smojver <bojan@rexursive.com> - 1.4.4-1
- bump up to 1.4.4
- CVE-2011-0419

* Wed Mar  2 2011 Joe Orton <jorton@redhat.com> - 1.4.2-3
- work around alising issue in ring macros (upstream PR 50190)
- fix buildconf with newer libtool (#670621)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec  4 2010 Joe Orton <jorton@redhat.com> - 1.4.2-1
- update to 1.4.2
- always enable SCTP support (#659815)

* Sun Oct 25 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.9-3
- remove uuid/crypt libs from pkg-config file (#511522)

* Mon Sep 28 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.9-2
- revert use of accept4(), dup3() and epoll_create1()

* Fri Sep 25 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.9-1
- bump up to 1.3.9

* Thu Aug  6 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.8-1
- bump up to 1.3.8
- CVE-2009-2412
- allocator alignment fixes

* Sun Jul 26 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.7-2
- include apr_cv_sock_cloexec too

* Sun Jul 26 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.7-1
- bump up to 1.3.7

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.6-1
- bump up to 1.3.6

* Tue Jun 30 2009 Joe Orton <jorton@redhat.com> 1.3.5-5
- BR libuuid-devel instead of e2fsprogs-devel

* Mon Jun  8 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.5-4
- bump up to 1.3.5

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Joe Orton <jorton@redhat.com> 1.3.3
- fix build with libtool 2.2

* Fri Jan  2 2009 Joe Orton <jorton@redhat.com> 1.3.3
- rebuild

* Sat Aug 16 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.3-1
- bump up to 1.3.3

* Wed Jul 16 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-2
- ship find_apr.m4, fix bug #455189

* Thu Jun 19 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-1
- bump up to 1.3.2

* Sun Jun  1 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.0-1
- bump up to 1.3.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.12-2
- Autorebuild for GCC 4.3

* Mon Nov 26 2007 Bojan Smojver <bojan@rexursive.com> 1.2.12-1
- bump up to 1.2.12
- add dist
- remove a comment from apr-1.2.7-psprintfpi.patch (applied upstream)

* Tue Sep 18 2007 Joe Orton <jorton@redhat.com> 1.2.11-2
- fix %%check for non-multilib 64-bit platforms

* Sun Sep  9 2007 Bojan Smojver <bojan@rexursive.com> 1.2.11-1
- bump up to 1.2.11
- drop openlfs patch (fixed upstream)

* Sun Sep  2 2007 Joe Orton <jorton@redhat.com> 1.2.9-4
- fix API/ABI of 32-bit builds (#254241)

* Tue Aug 21 2007 Joe Orton <jorton@redhat.com> 1.2.9-2
- fix License

* Mon Jun 25 2007 Bojan Smojver <bojan@rexursive.com> 1.2.9-1
- bump up to 1.2.9

* Mon Jun  4 2007 Joe Orton <jorton@redhat.com> 1.2.8-7
- drop %%check section entirely; inappropriate to run in build env.

* Fri Mar 30 2007 Joe Orton <jorton@redhat.com> 1.2.8-6
- merge review (#225253): drop .a archive; drop use of CC/CXX,
  use BuildRequires; drop old Conflicts; URL reference for Source

* Thu Mar 22 2007 Joe Orton <jorton@redhat.com> 1.2.8-5
- drop the doxygen documentation (which causes multilib conflicts)

* Thu Feb 15 2007 Joe Orton <jorton@redhat.com> 1.2.8-4
- add BR for python

* Thu Feb 15 2007 Joe Orton <jorton@redhat.com> 1.2.8-3
- update to pick up new libtool, drop specific gcc requirement

* Mon Dec  4 2006 Joe Orton <jorton@redhat.com> 1.2.8-2
- update to 1.2.8

* Wed Jul 19 2006 Joe Orton <jorton@redhat.com> 1.2.7-10
- fix buildconf with autoconf 2.60 (#199067)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.2.7-9.1
- rebuild

* Mon Jun 19 2006 Joe Orton <jorton@redhat.com> 1.2.7-9
- add fix for use of %%pI with psprintf

* Fri May 26 2006 Jakub Jelinek <jakub@redhat.com> 1.2.7-8
- rebuilt with GCC 4.1.0

* Tue May 23 2006 Joe Orton <jorton@redhat.com> 1.2.7-7
- fix another multilib conflict (#192659)

* Tue May 16 2006 Joe Orton <jorton@redhat.com> 1.2.7-6
- BR e2fsprogs-devel for libuuid

* Mon May  8 2006 Joe Orton <jorton@redhat.com> 1.2.7-4
- use multilib parallel-installation wrapper hack for apr.h

* Tue May  2 2006 Joe Orton <jorton@redhat.com> 1.2.7-3
- fix installbuilddir in apr-1-config

* Tue May  2 2006 Joe Orton <jorton@redhat.com> 1.2.7-2
- update to 1.2.7
- use pkg-config in apr-1-config to make it libdir-agnostic

* Thu Apr  6 2006 Joe Orton <jorton@redhat.com> 1.2.6-2
- update to 1.2.6

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-7.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-7.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan  4 2006 Joe Orton <jorton@redhat.com> 1.2.2-7
- fix namespace pollution (r354824, r355464)

* Wed Jan  4 2006 Joe Orton <jorton@redhat.com> 1.2.2-6
- fix build with recent glibc (#176911)

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1.2.2-5.2
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  9 2005 Joe Orton <jorton@redhat.com> 1.2.2-5
- rebuild for new gcc

* Thu Dec  8 2005 Joe Orton <jorton@redhat.com> 1.2.2-4
- add apr_file_seek() fixes from upstream (r326593, r326597)

* Wed Dec  7 2005 Joe Orton <jorton@redhat.com> 1.2.2-3
- apr-1-config: strip more exports (#175124) 

* Tue Dec  6 2005 Joe Orton <jorton@redhat.com> 1.2.2-2
- avoid linking against -lrt
- don't print -L${libdir} in --libs output
- don't export -lcrypt/-luuid in .la file

* Fri Dec  2 2005 Joe Orton <jorton@redhat.com> 1.2.2-1
- update to 1.2.2

* Thu Nov 24 2005 Joe Orton <jorton@redhat.com> 0.9.7-3
- use RTLD_DEEPBIND in apr_dso_open by default

* Thu Oct 20 2005 Joe Orton <jorton@redhat.com> 0.9.7-2
- update to 0.9.7

* Fri Sep 30 2005 Florian La Roche <laroche@redhat.com>
- rebuild for new gcc

* Thu Sep 15 2005 Joe Orton <jorton@redhat.com> 0.9.6-6
- don't override CFLAGS at build time
- allow setting TCP_NODELAY and TCP_CORK concurrently
- use _exit() not exit() in child if exec*() fails (upstream #30913)

* Fri Sep  9 2005 Joe Orton <jorton@redhat.com> 0.9.6-5
- add from 0.9.x branch:
 * fix for apr_{uid,gid}_* error handling (r239592)
 * fix for apr_file_ write flushing (r267192)
- add backport for use of readdir64_r (r265032, r265681, r265684)

* Mon Jul 11 2005 Florian La Roche <laroche@redhat.com>
- rebuild

* Tue May 17 2005 Joe Orton <jorton@redhat.com> 0.9.6-3
- fix apr_procattr_child_*_set error handling

* Tue Mar  1 2005 Joe Orton <jorton@redhat.com> 0.9.6-2
- have apr-devel depend on specific version of gcc
- add NOTICE to docdir

* Wed Feb  9 2005 Joe Orton <jorton@redhat.com> 0.9.6-1
- update to 0.9.6

* Wed Feb  2 2005 Joe Orton <jorton@redhat.com> 0.9.5-4
- don't disable sendfile on s390 (IBM LTC, #146891)

* Mon Nov 22 2004 Joe Orton <jorton@redhat.com> 0.9.5-3
- really fix apr-config --srcdir

* Mon Nov 22 2004 Joe Orton <jorton@redhat.com> 0.9.5-2
- fix apr-config --srcdir again

* Sun Nov 21 2004 Joe Orton <jorton@redhat.com> 0.9.5-1
- update to 0.9.5

* Mon Sep 27 2004 Joe Orton <jorton@redhat.com> 0.9.4-24
- rebuild

* Wed Sep  1 2004 Joe Orton <jorton@redhat.com> 0.9.4-23
- have -devel require apr of same V-R

* Tue Aug 31 2004 Joe Orton <jorton@redhat.com> 0.9.4-22
- backport fixes from HEAD:
 * correct implementation of nested mutexes
 * support for POSIX semaphores on LP64 platforms

* Thu Jul 15 2004 Joe Orton <jorton@redhat.com> 0.9.4-21
- rebuild for another attempt at using sem_open

* Tue Jul 13 2004 Joe Orton <jorton@redhat.com> 0.9.4-20
- move sticky/suid bits outside APR_OS_DEFAULT bitmask (Greg Hudson)

* Thu Jul  1 2004 Joe Orton <jorton@redhat.com> 0.9.4-19
- rebuild

* Wed Jun 30 2004 Joe Orton <jorton@redhat.com> 0.9.4-18
- rebuild now /dev/shm is mounted

* Thu Jun 17 2004 Joe Orton <jorton@redhat.com> 0.9.4-17
- add fix for cleanup structure reuse (part of upstream #23567)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun 10 2004 Joe Orton <jorton@redhat.com> 0.9.4-15
- add support for setuid/setgid/sticky bits (André Malo)
- add apr_threadattr_{guardsize,stacksize}_set() (latter by Jeff Trawick)

* Mon Jun  7 2004 Joe Orton <jorton@redhat.com> 0.9.4-14
- enable posixsem and process-shared pthread mutex support, but
  ensure that sysvsem remains the default mechanism

* Mon May 24 2004 Joe Orton <jorton@redhat.com> 0.9.4-13
- entirely remove 2Gb file size limit from apr_file_copy();
  fixes "svnadmin hotcopy" on repos with >2Gb strings table
- work around getnameinfo bugs with v4-mapped addresses
- fix apr_time_exp_get() for dates in 2038 (Philip Martin)

* Thu May 13 2004 Joe Orton <jorton@redhat.com> 0.9.4-12
- use APR_LARGEFILE in apr_file_{copy,append}

* Wed Mar 24 2004 Joe Orton <jorton@redhat.com> 0.9.4-11
- add APR_LARGEFILE flag

* Mon Mar 15 2004 Joe Orton <jorton@redhat.com> 0.9.4-10
- fix configure check for mmap of /dev/zero
- just put -D_GNU_SOURCE in CPPFLAGS not _{BSD,SVID,XOPEN}_SOURCE

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 0.9.4-9.1
- rebuilt

* Thu Feb 19 2004 Joe Orton <jorton@redhat.com> 0.9.4-9
- undocument apr_dir_read() ordering constraint and fix tests

* Sun Feb 15 2004 Joe Orton <jorton@redhat.com> 0.9.4-8
- rebuilt without -Wall -Werror

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 0.9.4-7
- rebuilt

* Tue Feb  3 2004 Joe Orton <jorton@redhat.com> 0.9.4-6
- define apr_off_t as int/long/... to prevent it changing
  with _FILE_OFFSET_BITS on 32-bit platforms

* Mon Jan 12 2004 Joe Orton <jorton@redhat.com> 0.9.4-5
- add apr_temp_dir_get fixes from HEAD

* Thu Jan  8 2004 Joe Orton <jorton@redhat.com> 0.9.4-4
- ensure that libapr is linked against libpthread
- don't link libapr against -lnsl

* Thu Nov 13 2003 Joe Orton <jorton@redhat.com> 0.9.4-3
- -devel package no longer requires libtool

* Fri Oct  3 2003 Joe Orton <jorton@redhat.com> 0.9.4-2
- disable tests on x86_64 (#97611)

* Fri Oct  3 2003 Joe Orton <jorton@redhat.com> 0.9.4-1
- update to 0.9.4, enable tests
- ensure that libresolv is not used

* Sun Sep  7 2003 Joe Orton <jorton@redhat.com> 0.9.3-14
- use /dev/urandom (#103049)

* Thu Jul 24 2003 Joe Orton <jorton@redhat.com> 0.9.3-13
- add back CC=gcc, CXX=g++

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.3-12
- rebuild

* Mon Jul 14 2003 Joe Orton <jorton@redhat.com> 0.9.3-11
- work round useless autoconf 2.57 AC_DECL_SYS_SIGLIST

* Thu Jul 10 2003 Joe Orton <jorton@redhat.com> 0.9.3-10
- support --cc and --cpp arguments in apr-config

* Thu Jul  3 2003 Joe Orton <jorton@redhat.com> 0.9.3-9
- force libtool to use CC=gcc, CXX=g++

* Thu Jul  3 2003 Joe Orton <jorton@redhat.com> 0.9.3-8
- fix libtool location in apr_rules.mk

* Mon Jun 30 2003 Joe Orton <jorton@redhat.com> 0.9.3-7
- use AI_ADDRCONFIG in getaddrinfo() support (#73350)
- include a working libtool script rather than relying on
 /usr/bin/libtool (#97695)

* Wed Jun 18 2003 Joe Orton <jorton@redhat.com> 0.9.3-6
- don't use /usr/bin/libtool

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 20 2003 Joe Orton <jorton@redhat.com> 0.9.3-5
- add fix for psprintf memory corruption (CAN-2003-0245)
- remove executable bit from apr_poll.h

* Thu May  1 2003 Joe Orton <jorton@redhat.com> 0.9.3-4
- link libapr against libpthread
- make apr-devel conflict with old subversion-devel
- fix License

* Tue Apr 29 2003 Joe Orton <jorton@redhat.com> 0.9.3-3
- run ldconfig in post/postun

* Tue Apr 29 2003 Joe Orton <jorton@redhat.com> 0.9.3-2
- patch test suite to not care if IPv6 is disabled

* Mon Apr 28 2003 Joe Orton <jorton@redhat.com> 0.9.3-1
- initial build
